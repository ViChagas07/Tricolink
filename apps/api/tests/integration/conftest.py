from collections.abc import AsyncIterator
from dataclasses import replace

import pytest
from redis.asyncio import Redis

from tricolink.core.config import Settings
from tricolink.infra.cache import close_redis, create_redis


@pytest.fixture
async def redis_client() -> AsyncIterator[Redis]:
    settings = replace(Settings.from_env(), redis_pool_max_connections=120)
    client = create_redis(settings)
    try:
        await client.ping()
    except Exception:
        await client.aclose()
        pytest.skip("Redis is not reachable")
    try:
        yield client
    finally:
        await close_redis(client)
