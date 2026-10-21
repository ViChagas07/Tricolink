from __future__ import annotations

import asyncio
import hashlib
import math
import time
import unicodedata
from collections.abc import Awaitable, Callable
from typing import TypeVar

from redis.asyncio import Redis
from redis.exceptions import RedisError

from tricolink.core.config import Settings
from tricolink.infra.ratelimit.models import RateLimitResult
from tricolink.infra.ratelimit.service import RateLimiter
from tricolink.infra.resilience import CircuitBreaker, CircuitOpenError
from tricolink.modules.identity.application.ports import ThrottleResult

T = TypeVar("T")

_INCREMENT_FAILURE_LUA = """
local current = redis.call('INCR', KEYS[1])
if current == 1 then
  redis.call('PEXPIRE', KEYS[1], ARGV[1])
end
return current
"""


class RedisAuthThrottle:
    """IP + normalized-email brute-force protection with temporary lockout."""

    def __init__(
        self,
        redis: Redis,
        *,
        limiter: RateLimiter,
        breaker: CircuitBreaker | None,
        settings: Settings,
    ) -> None:
        self._redis = redis
        self._limiter = limiter
        self._breaker = breaker
        self._timeout = settings.redis_timeout_seconds
        self._window_seconds = settings.auth_failure_window_seconds
        self._window_ms = self._window_seconds * 1000
        self._threshold = settings.auth_lockout_threshold
        self._lockout_seconds = settings.auth_lockout_seconds
        self._memory_failures: dict[str, tuple[float, int]] = {}
        self._memory_locks: dict[str, float] = {}

    async def check(self, *, ip: str, email: str) -> ThrottleResult:
        results = [
            await self._limiter.check("auth", f"email:{_digest(email)}"),
            await self._limiter.check("auth", f"ip:{_digest(ip)}"),
        ]
        denied = [result for result in results if not result.allowed]
        if denied:
            return ThrottleResult(
                allowed=False,
                retry_after_seconds=max(_retry_after(result) for result in denied),
            )

        lock_retry = max(
            await self._lock_retry(f"auth:lock:email:{_digest(email)}"),
            await self._lock_retry(f"auth:lock:ip:{_digest(ip)}"),
        )
        if lock_retry > 0:
            return ThrottleResult(allowed=False, retry_after_seconds=lock_retry)
        return ThrottleResult(allowed=True, retry_after_seconds=0)

    async def record_failure(self, *, ip: str, email: str) -> None:
        await self._record_key(f"auth:fail:email:{_digest(email)}")
        await self._record_key(f"auth:fail:ip:{_digest(ip)}")

    async def record_success(self, *, email: str) -> None:
        keys = (
            f"auth:fail:email:{_digest(email)}",
            f"auth:lock:email:{_digest(email)}",
        )

        async def operation() -> None:
            await self._redis.delete(*keys)

        try:
            await self._call(operation)
        except (RedisError, TimeoutError, OSError, CircuitOpenError):
            for key in keys:
                self._memory_failures.pop(key, None)
                self._memory_locks.pop(key, None)

    async def _record_key(self, key: str) -> None:
        async def operation() -> int:
            return int(
                await asyncio.wait_for(
                    self._redis.eval(
                        _INCREMENT_FAILURE_LUA,
                        1,
                        key,
                        self._window_ms,
                    ),
                    timeout=self._timeout,
                )
            )

        try:
            count = await self._call(operation)
        except (RedisError, TimeoutError, OSError, CircuitOpenError):
            count = self._memory_increment(key)

        if count >= self._threshold:
            await self._set_lock(key.replace(":fail:", ":lock:"))

    async def _lock_retry(self, key: str) -> int:
        async def operation() -> int:
            return int(await self._redis.pttl(key))

        try:
            pttl = await self._call(operation)
        except (RedisError, TimeoutError, OSError, CircuitOpenError):
            until = self._memory_locks.get(key, 0.0)
            return max(0, math.ceil(until - time.monotonic()))

        if pttl > 0:
            return max(1, math.ceil(pttl / 1000))
        if pttl == -1:
            return self._lockout_seconds
        return 0

    async def _set_lock(self, key: str) -> None:
        async def operation() -> None:
            await self._redis.set(
                key,
                "1",
                px=self._lockout_seconds * 1000,
            )

        try:
            await self._call(operation)
        except (RedisError, TimeoutError, OSError, CircuitOpenError):
            self._memory_locks[key] = time.monotonic() + self._lockout_seconds

    def _memory_increment(self, key: str) -> int:
        now = time.monotonic()
        if len(self._memory_failures) > 10_000:
            cutoff = now - self._window_seconds
            self._memory_failures = {
                stored_key: value
                for stored_key, value in self._memory_failures.items()
                if value[0] >= cutoff
            }
        updated_at, count = self._memory_failures.get(key, (now, 0))
        if now - updated_at > self._window_seconds:
            count = 0
        count += 1
        self._memory_failures[key] = (now, count)
        return count

    async def _call(self, operation: Callable[[], Awaitable[T]]) -> T:
        async def guarded() -> T:
            return await asyncio.wait_for(operation(), timeout=self._timeout)

        if self._breaker is None:
            return await guarded()
        async with self._breaker.guard():
            return await guarded()


def _digest(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).strip().lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:32]


def _retry_after(result: RateLimitResult) -> int:
    if result.retry_after_ms >= 0:
        return max(1, math.ceil(result.retry_after_ms / 1000))
    return max(1, result.reset_after_seconds)
