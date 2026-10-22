from __future__ import annotations

import asyncio
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import httpx
import pytest

from tricolink.core.config import Settings
from tricolink.infra.cache import create_redis
from tricolink.main import create_app
from tricolink.modules.links.adapters.cache import (
    GENERATION_KEY,
    LINK_KEY,
    LOCK_KEY,
    NEGATIVE_KEY,
    RedisLinkCache,
)
from tricolink.modules.links.application import ResolveLink
from tricolink.modules.links.domain.entities import Link
from tricolink.modules.links.domain.value_objects import OriginalUrl, ShortCode
from tricolink.modules.links.presentation.dependencies import (
    get_record_click,
    get_resolve_link,
)

pytestmark = pytest.mark.integration


class CountingRepository:
    def __init__(self, link: Link) -> None:
        self.link = link
        self.calls = 0

    async def get_by_code(self, code: ShortCode) -> Link | None:
        self.calls += 1
        await asyncio.sleep(0.02)
        return self.link


class NoopRecordClick:
    async def execute(self, **kwargs: object) -> None:
        return None


@pytest.mark.asyncio
async def test_200_concurrent_cold_redirects_hit_the_database_once() -> None:
    code = f"s{uuid4().hex[:6]}"
    settings = replace(
        Settings.from_env(),
        click_flusher_enabled=False,
        click_stream_key=f"test:stampede:{uuid4().hex[:10]}",
        short_base_url="https://short.test",
        cache_wait_timeout_seconds=2.0,
        rl_redirect_capacity=1000,
        rl_redirect_refill_per_sec=1000,
        rl_global_capacity=100_000,
        rl_global_refill_per_sec=100_000,
    )
    now = datetime.now(UTC)
    link = Link(
        id=99,
        code=ShortCode(code),
        original_url=OriginalUrl.parse("https://93.184.216.34/cold"),
        title=None,
        user_id=None,
        is_custom_alias=False,
        is_active=True,
        expires_at=now + timedelta(days=1),
        click_count=0,
        created_at=now,
        updated_at=now,
    )
    repository = CountingRepository(link)
    redis = create_redis(settings)
    cache = RedisLinkCache(redis, breaker=None, settings=settings)
    app = create_app(settings)
    app.dependency_overrides[get_resolve_link] = lambda: ResolveLink(
        repository=repository,
        cache=cache,
        clock=app.state.services.links.clock,
    )
    app.dependency_overrides[get_record_click] = NoopRecordClick

    try:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            responses = await asyncio.gather(*(client.get(f"/api/v1/r/{code}") for _ in range(200)))

        assert repository.calls == 1
        assert all(response.status_code == 302 for response in responses)
        assert all(
            response.headers["location"] == "https://93.184.216.34/cold" for response in responses
        )
    finally:
        await redis.delete(
            LINK_KEY.format(code=code),
            LOCK_KEY.format(code=code),
            NEGATIVE_KEY.format(code=code),
            GENERATION_KEY.format(code=code),
        )
        await redis.aclose()
        await app.state.services.close()
