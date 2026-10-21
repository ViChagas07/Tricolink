import asyncio
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from redis.asyncio import Redis

from tricolink.core.config import Settings
from tricolink.modules.links.adapters.cache import (
    LINK_KEY,
    LOCK_KEY,
    NEGATIVE_KEY,
    RedisLinkCache,
)
from tricolink.modules.links.domain.entities import Link
from tricolink.modules.links.domain.value_objects import OriginalUrl, ShortCode

pytestmark = pytest.mark.integration


def cache_settings() -> Settings:
    return replace(
        Settings.from_env(),
        cache_hard_ttl_seconds=60,
        cache_soft_ttl_seconds=30,
        cache_jitter_pct=0.15,
        negative_cache_ttl_seconds=10,
        lock_ttl_ms=1_000,
        cache_wait_timeout_seconds=0.5,
    )


def make_link(code: str, url: str = "https://93.184.216.34/path") -> Link:
    now = datetime.now(UTC)
    return Link(
        id=42,
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


def unique_code() -> str:
    return f"c{uuid4().hex[:6]}"


async def cleanup(redis: Redis, code: str) -> None:
    await redis.delete(
        LINK_KEY.format(code=code),
        LOCK_KEY.format(code=code),
        NEGATIVE_KEY.format(code=code),
    )


@pytest.mark.asyncio
async def test_cold_stampede_uses_one_database_query(redis_client: Redis) -> None:
    code = unique_code()
    cache = RedisLinkCache(redis_client, breaker=None, settings=cache_settings())
    link = make_link(code)
    calls = 0

    async def loader() -> Link:
        nonlocal calls
        calls += 1
        await asyncio.sleep(0.02)
        return link

    try:
        results = await asyncio.gather(
            *(cache.resolve(ShortCode(code), loader) for _ in range(200))
        )
    finally:
        await cleanup(redis_client, code)

    assert calls == 1
    assert all(result is not None for result in results)
    assert all(result.link_id == 42 for result in results if result is not None)


@pytest.mark.asyncio
async def test_stale_value_is_served_while_one_refresh_runs(redis_client: Redis) -> None:
    code = unique_code()
    cache = RedisLinkCache(redis_client, breaker=None, settings=cache_settings())
    link = make_link(code)
    calls = 0
    started = asyncio.Event()
    release = asyncio.Event()

    async def loader() -> Link:
        nonlocal calls
        calls += 1
        started.set()
        await release.wait()
        return link

    try:
        await cache.store(link, soft_ttl_seconds=0)
        await asyncio.sleep(0.01)

        results = await asyncio.gather(*(cache.resolve(ShortCode(code), loader) for _ in range(50)))
        assert all(result is not None for result in results)
        await asyncio.wait_for(started.wait(), timeout=1)
        assert calls == 1

        release.set()
        await asyncio.sleep(0.1)
        refreshed = await cache.resolve(ShortCode(code), loader)
        assert refreshed is not None
        assert calls == 1
    finally:
        release.set()
        await cleanup(redis_client, code)


@pytest.mark.asyncio
async def test_negative_cache_limits_missing_code_queries(redis_client: Redis) -> None:
    code = unique_code()
    cache = RedisLinkCache(redis_client, breaker=None, settings=cache_settings())
    calls = 0

    async def loader() -> None:
        nonlocal calls
        calls += 1
        await asyncio.sleep(0.01)
        return None

    try:
        results = await asyncio.gather(
            *(cache.resolve(ShortCode(code), loader) for _ in range(1_000))
        )
    finally:
        await cleanup(redis_client, code)

    assert calls == 1
    assert all(result is None for result in results)


@pytest.mark.asyncio
async def test_invalidation_forces_the_next_read_to_use_the_loader(
    redis_client: Redis,
) -> None:
    code = unique_code()
    cache = RedisLinkCache(redis_client, breaker=None, settings=cache_settings())
    link = make_link(code)
    updated = make_link(code, "https://1.1.1.1/new")
    calls = 0

    async def loader() -> Link:
        nonlocal calls
        calls += 1
        return updated

    try:
        await cache.store(link)
        assert (await cache.resolve(ShortCode(code), loader)).original_url.endswith("/path")  # type: ignore[union-attr]

        await cache.invalidate(ShortCode(code))
        refreshed = await cache.resolve(ShortCode(code), loader)
        assert refreshed is not None
        assert refreshed.original_url == "https://1.1.1.1/new"
        assert calls == 1
    finally:
        await cleanup(redis_client, code)
