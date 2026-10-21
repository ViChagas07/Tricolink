from __future__ import annotations

import asyncio
import hashlib
from collections.abc import Callable
from datetime import UTC, datetime, timedelta

from redis.asyncio import Redis
from redis.exceptions import RedisError

from tricolink.infra.resilience import CircuitBreaker, CircuitOpenError
from tricolink.modules.links.application.ports import QuotaResult
from tricolink.shared_kernel.clock import utc_now

_QUOTA_LUA = """
local key = KEYS[1]
local ttl_ms = tonumber(ARGV[1])
local current = redis.call('INCR', key)
if current == 1 then
  redis.call('PEXPIRE', key, ttl_ms)
end
return current
"""


class RedisDailyQuota:
    def __init__(
        self,
        redis: Redis,
        *,
        breaker: CircuitBreaker | None = None,
        timeout_seconds: float = 2.0,
        clock: Callable[[], datetime] = utc_now,
    ) -> None:
        self._redis = redis
        self._breaker = breaker
        self._timeout_seconds = timeout_seconds
        self._clock = clock
        self._memory: dict[tuple[str, str, str], int] = {}
        self._memory_day = ""

    async def consume(self, scope: str, key: str, limit: int) -> QuotaResult:
        now = self._clock()
        if now.tzinfo is None:
            now = now.replace(tzinfo=UTC)
        now = now.astimezone(UTC)
        day = now.date().isoformat()
        retry_after = _seconds_until_next_utc_day(now)

        if limit < 1:
            return QuotaResult(
                allowed=False,
                used=0,
                limit=limit,
                retry_after_seconds=retry_after,
            )

        hashed_key = hashlib.sha256(f"{scope}:{key}".encode()).hexdigest()[:32]
        redis_key = f"quota:{day}:{scope}:{hashed_key}"
        try:
            used = await self._increment_redis(redis_key, retry_after)
        except (RedisError, TimeoutError, OSError, CircuitOpenError):
            used = self._increment_memory(day, scope, hashed_key)

        return QuotaResult(
            allowed=used <= limit,
            used=used,
            limit=limit,
            retry_after_seconds=retry_after,
        )

    async def _increment_redis(self, key: str, retry_after_seconds: int) -> int:
        async def operation() -> int:
            return int(
                await asyncio.wait_for(
                    self._redis.eval(
                        _QUOTA_LUA,
                        1,
                        key,
                        max(1000, retry_after_seconds * 1000),
                    ),
                    timeout=self._timeout_seconds,
                )
            )

        if self._breaker is None:
            return await operation()
        async with self._breaker.guard():
            return await operation()

    def _increment_memory(self, day: str, scope: str, key: str) -> int:
        if day != self._memory_day:
            self._memory.clear()
            self._memory_day = day
        memory_key = (day, scope, key)
        used = self._memory.get(memory_key, 0) + 1
        self._memory[memory_key] = used
        return used


def _seconds_until_next_utc_day(now: datetime) -> int:
    tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return max(1, int((tomorrow - now).total_seconds()))
