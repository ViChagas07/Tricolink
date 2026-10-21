from __future__ import annotations

from typing import cast

from redis.asyncio import Redis

from tricolink.infra.observability.metrics import record_cache_hit, record_cache_miss


class CacheClient:
    """Thin cache wrapper that records hit/miss metrics."""

    def __init__(self, redis: Redis, *, namespace: str = "cache") -> None:
        self._redis = redis
        self._namespace = namespace

    async def get(self, key: str) -> str | None:
        value = cast(str | None, await self._redis.get(key))
        if value is None:
            record_cache_miss(self._namespace)
        else:
            record_cache_hit(self._namespace)
        return value

    async def set(self, key: str, value: str, *, ttl_seconds: int) -> None:
        if ttl_seconds < 1:
            raise ValueError("ttl_seconds must be positive")
        await self._redis.set(key, value, ex=ttl_seconds)

    async def delete(self, *keys: str) -> int:
        if not keys:
            return 0
        return int(await self._redis.delete(*keys))
