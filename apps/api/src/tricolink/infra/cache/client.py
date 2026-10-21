from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar, cast

from redis.asyncio import Redis

from tricolink.infra.observability.metrics import record_cache_hit, record_cache_miss
from tricolink.infra.resilience import CircuitBreaker

T = TypeVar("T")


class CacheClient:
    """Thin cache wrapper that records hit/miss metrics and honors the breaker."""

    def __init__(
        self,
        redis: Redis,
        *,
        namespace: str = "cache",
        breaker: CircuitBreaker | None = None,
        timeout_seconds: float = 2.0,
    ) -> None:
        self._redis = redis
        self._namespace = namespace
        self._breaker = breaker
        self._timeout = timeout_seconds

    async def get(self, key: str) -> str | None:
        value = cast(str | None, await self._call(lambda: self._redis.get(key)))
        if value is None:
            record_cache_miss(self._namespace)
        else:
            record_cache_hit(self._namespace)
        return value

    async def set(self, key: str, value: str, *, ttl_seconds: int) -> None:
        if ttl_seconds < 1:
            raise ValueError("ttl_seconds must be positive")
        await self._call(lambda: self._redis.set(key, value, ex=ttl_seconds))

    async def delete(self, *keys: str) -> int:
        if not keys:
            return 0
        return int(await self._call(lambda: self._redis.delete(*keys)))

    async def _call(self, operation: Callable[[], Awaitable[T]]) -> T:
        async def guarded() -> T:
            return await asyncio.wait_for(operation(), timeout=self._timeout)

        if self._breaker is None:
            return await guarded()
        async with self._breaker.guard():
            return await guarded()
