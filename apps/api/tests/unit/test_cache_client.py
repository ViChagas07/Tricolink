from typing import cast

import pytest
from prometheus_client import REGISTRY
from redis.asyncio import Redis

from tricolink.infra.cache import CacheClient


class FakeRedis:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}
        self.last_ttl: int | None = None

    async def get(self, key: str) -> str | None:
        return self.values.get(key)

    async def set(self, key: str, value: str, *, ex: int) -> None:
        self.values[key] = value
        self.last_ttl = ex

    async def delete(self, *keys: str) -> int:
        removed = 0
        for key in keys:
            if key in self.values:
                del self.values[key]
                removed += 1
        return removed


def _sample(name: str, namespace: str) -> float:
    value = REGISTRY.get_sample_value(f"{name}_total", {"namespace": namespace})
    return value or 0.0


@pytest.mark.asyncio
async def test_cache_get_records_hit_and_miss() -> None:
    redis = FakeRedis()
    cache = CacheClient(cast(Redis, redis), namespace="test-cache")
    hits_before = _sample("tricolink_cache_hits", "test-cache")
    misses_before = _sample("tricolink_cache_misses", "test-cache")

    assert await cache.get("missing") is None
    await cache.set("key", "value", ttl_seconds=30)
    assert await cache.get("key") == "value"

    assert _sample("tricolink_cache_hits", "test-cache") == hits_before + 1
    assert _sample("tricolink_cache_misses", "test-cache") == misses_before + 1
    assert redis.last_ttl == 30


@pytest.mark.asyncio
async def test_cache_set_validates_ttl_and_delete() -> None:
    redis = FakeRedis()
    cache = CacheClient(cast(Redis, redis))

    with pytest.raises(ValueError):
        await cache.set("key", "value", ttl_seconds=0)

    assert await cache.delete() == 0
    await cache.set("a", "1", ttl_seconds=10)
    await cache.set("b", "2", ttl_seconds=10)
    assert await cache.delete("a", "b") == 2
