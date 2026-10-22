from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from redis.asyncio import Redis

from tricolink.infra.db import Database
from tricolink.modules.analytics.adapters.stats_cache import STATS_KEY, RedisStatsCache
from tricolink.modules.analytics.adapters.stats_repository import SqlAlchemyStatsRepository
from tricolink.modules.analytics.application.get_link_stats import GetLinkStats
from tricolink.modules.links.adapters.cache import (
    GENERATION_KEY,
    LINK_KEY,
    NEGATIVE_KEY,
    RedisLinkCache,
)
from tricolink.modules.links.adapters.repository import SqlAlchemyLinkRepository
from tricolink.modules.links.domain.entities import Link
from tricolink.modules.links.domain.value_objects import OriginalUrl, ShortCode
from tricolink.shared_kernel.clock import SystemClock

from .helpers import acleanup, aseed_click, aseed_link, aseed_user, security_settings

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_stats_cache_is_scoped_by_link_id_and_does_not_leak_after_code_reuse(
    redis_client: Redis,
) -> None:
    settings = security_settings()
    owner_a = await aseed_user(settings)
    owner_b = await aseed_user(settings)
    code = f"re{uuid4().hex[:6]}"
    link_a = await aseed_link(settings, code=code, user_id=owner_a)
    assert link_a.id is not None
    for _ in range(5):
        await aseed_click(settings, link_id=link_a.id)

    database = Database(settings)
    repository = SqlAlchemyLinkRepository(database)
    cache = RedisStatsCache(redis_client, breaker=None, settings=settings)
    use_case = GetLinkStats(
        links=repository,
        stats=SqlAlchemyStatsRepository(database),
        cache=cache,
        clock=SystemClock(),
    )

    try:
        before = await use_case.execute(code, owner_a)
        assert before.total == 5
        assert await redis_client.exists(STATS_KEY.format(link_id=link_a.id, range="30d"))

        assert await repository.delete(ShortCode(code), owner_a)
        link_b = await aseed_link(settings, code=code, user_id=owner_b)
        assert link_b.id is not None and link_b.id != link_a.id

        after = await use_case.execute(code, owner_b)
        assert after.total == 0
        assert after.series
        assert await redis_client.exists(STATS_KEY.format(link_id=link_b.id, range="30d"))
        await redis_client.delete(STATS_KEY.format(link_id=link_a.id, range="30d"))
    finally:
        await database.dispose()
        await acleanup(settings, codes=[code], user_ids=[owner_a, owner_b])


@pytest.mark.asyncio
async def test_invalidation_generation_blocks_a_stale_cache_refresh(redis_client: Redis) -> None:
    settings = security_settings()
    code = f"iv{uuid4().hex[:6]}"
    cache = RedisLinkCache(redis_client, breaker=None, settings=settings)
    old = _link(code, "https://93.184.216.34/old")
    fresh = _link(code, "https://1.1.1.1/new")
    started = asyncio.Event()
    release = asyncio.Event()

    async def stale_loader() -> Link:
        started.set()
        await release.wait()
        return old

    try:
        await cache.store(old, soft_ttl_seconds=0)
        await asyncio.sleep(0.01)
        assert (await cache.resolve(ShortCode(code), stale_loader)) is not None
        await asyncio.wait_for(started.wait(), timeout=1)

        await cache.invalidate(ShortCode(code))
        generation = await redis_client.get(GENERATION_KEY.format(code=code))
        assert generation is not None and int(generation) >= 1
        assert await redis_client.exists(LINK_KEY.format(code=code)) == 0
        assert await redis_client.exists(NEGATIVE_KEY.format(code=code)) == 0

        release.set()
        await asyncio.sleep(0.1)

        resolved = await cache.resolve(ShortCode(code), lambda: _resolved(fresh))
        assert resolved is not None
        assert resolved.original_url == "https://1.1.1.1/new"
    finally:
        release.set()
        await redis_client.delete(
            LINK_KEY.format(code=code),
            NEGATIVE_KEY.format(code=code),
            GENERATION_KEY.format(code=code),
        )


def _link(code: str, url: str) -> Link:
    now = datetime.now(UTC)
    return Link(
        id=uuid4().int % 10_000_000,
        code=ShortCode(code),
        original_url=OriginalUrl.parse(url),
        title=None,
        user_id=None,
        is_custom_alias=False,
        is_active=True,
        expires_at=now + timedelta(days=1),
        click_count=0,
        created_at=now,
        updated_at=now,
    )


async def _resolved(link: Link) -> Link:
    return link
