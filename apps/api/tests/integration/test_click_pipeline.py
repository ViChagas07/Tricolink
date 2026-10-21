from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from typing import cast
from uuid import uuid4

import pytest
from prometheus_client import REGISTRY
from redis.asyncio import Redis
from redis.exceptions import ConnectionError as RedisConnectionError
from sqlalchemy import delete, func, select

from tricolink.core.config import Settings
from tricolink.infra.db import Database
from tricolink.infra.db.models import ClickEvent as ClickEventRow
from tricolink.infra.db.models import Link as LinkRow
from tricolink.modules.analytics.adapters import ClickFlusher, RedisClickPublisher
from tricolink.modules.analytics.domain.click import ClickEvent
from tricolink.modules.links.adapters.repository import SqlAlchemyLinkRepository
from tricolink.modules.links.domain.entities import Link
from tricolink.modules.links.domain.value_objects import OriginalUrl, ShortCode

pytestmark = pytest.mark.integration


def pipeline_settings() -> Settings:
    unique = uuid4().hex[:10]
    return replace(
        Settings.from_env(),
        click_stream_key=f"test:clicks:{unique}",
        click_stream_group=f"test-group-{unique}",
        click_stream_maxlen=1_000,
        click_flush_batch_size=10,
        click_flush_block_ms=10,
        click_publish_timeout_seconds=1.0,
    )


def make_link(code: str) -> Link:
    now = datetime.now(UTC)
    return Link(
        id=None,
        code=ShortCode(code),
        original_url=OriginalUrl.parse("https://93.184.216.34/path"),
        title=None,
        user_id=None,
        is_custom_alias=False,
        is_active=True,
        expires_at=None,
        click_count=0,
        created_at=now,
        updated_at=now,
    )


class DownRedis:
    async def xadd(self, *args: object, **kwargs: object) -> None:
        raise RedisConnectionError("down")


@pytest.mark.asyncio
async def test_publisher_drops_event_and_increments_metric_when_redis_is_down() -> None:
    settings = pipeline_settings()
    publisher = RedisClickPublisher(
        cast(Redis, DownRedis()),
        breaker=None,
        settings=settings,
    )
    before = (
        REGISTRY.get_sample_value(
            "tricolink_clicks_dropped_total",
            {"reason": "redis_unavailable"},
        )
        or 0
    )

    published = await publisher.publish(
        ClickEvent(
            link_id=1,
            clicked_at=datetime.now(UTC),
            country="BR",
            device="mobile",
            browser="safari",
            referrer_host="example.com",
        )
    )

    after = (
        REGISTRY.get_sample_value(
            "tricolink_clicks_dropped_total",
            {"reason": "redis_unavailable"},
        )
        or 0
    )
    assert published is False
    assert after == before + 1


@pytest.mark.asyncio
async def test_flusher_persists_batch_and_increments_click_count(
    redis_client: Redis,
) -> None:
    settings = pipeline_settings()
    database = Database(settings)
    repository = SqlAlchemyLinkRepository(database)
    publisher = RedisClickPublisher(redis_client, breaker=None, settings=settings)
    flusher = ClickFlusher(redis_client, database, breaker=None, settings=settings)
    code = f"p{uuid4().hex[:6]}"
    link = await repository.create(make_link(code))

    try:
        assert link.id is not None
        assert await publisher.publish(
            ClickEvent(
                link_id=link.id,
                clicked_at=datetime.now(UTC),
                country="BR",
                device="mobile",
                browser="safari",
                referrer_host="news.example.com",
            )
        )
        assert await publisher.publish(
            ClickEvent(
                link_id=link.id,
                clicked_at=datetime.now(UTC) + timedelta(seconds=1),
                country=None,
                device="desktop",
                browser="chrome",
                referrer_host=None,
            )
        )
        assert await publisher.publish(
            ClickEvent(
                link_id=999_999_999,
                clicked_at=datetime.now(UTC),
                country=None,
                device="unknown",
                browser=None,
                referrer_host=None,
            )
        )
        assert await redis_client.xlen(settings.click_stream_key) == 3

        processed = await flusher.run_once(block_ms=50)
        assert processed == 3

        async with database.read() as session:
            events = (
                await session.scalars(select(ClickEventRow).where(ClickEventRow.link_id == link.id))
            ).all()
            click_count = await session.scalar(
                select(LinkRow.click_count).where(LinkRow.id == link.id)
            )

        assert len(events) == 2
        assert click_count == 2
        assert {event.device for event in events} == {"mobile", "desktop"}
        assert await redis_client.xlen(settings.click_stream_key) == 0
    finally:
        async with database.unit_of_work() as session:
            await session.execute(
                delete(ClickEventRow).where(ClickEventRow.link_id == (link.id or -1))
            )
            await session.execute(delete(LinkRow).where(LinkRow.code == code))
        await redis_client.delete(settings.click_stream_key)
        await database.dispose()


@pytest.mark.asyncio
async def test_flusher_retries_pending_entries(redis_client: Redis) -> None:
    settings = pipeline_settings()
    database = Database(settings)
    repository = SqlAlchemyLinkRepository(database)
    publisher = RedisClickPublisher(redis_client, breaker=None, settings=settings)
    flusher = ClickFlusher(redis_client, database, breaker=None, settings=settings)
    code = f"q{uuid4().hex[:6]}"
    link = await repository.create(make_link(code))

    try:
        assert link.id is not None
        await publisher.publish(
            ClickEvent(
                link_id=link.id,
                clicked_at=datetime.now(UTC),
                country="US",
                device="desktop",
                browser="firefox",
                referrer_host=None,
            )
        )
        # Deliver once without processing, then process the pending entry.
        await flusher._ensure_group()  # noqa: SLF001
        await flusher._read(">", block_ms=10)  # noqa: SLF001
        processed = await flusher.run_once(block_ms=10)
        assert processed == 1

        async with database.read() as session:
            count = await session.scalar(
                select(func.count())
                .select_from(ClickEventRow)
                .where(ClickEventRow.link_id == link.id)
            )
        assert count == 1
    finally:
        async with database.unit_of_work() as session:
            await session.execute(
                delete(ClickEventRow).where(ClickEventRow.link_id == (link.id or -1))
            )
            await session.execute(delete(LinkRow).where(LinkRow.code == code))
        await redis_client.delete(settings.click_stream_key)
        await database.dispose()
