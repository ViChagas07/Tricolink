from __future__ import annotations

import asyncio
from collections.abc import Mapping
from dataclasses import replace
from typing import Protocol

from redis.exceptions import RedisError

from tricolink.infra.observability.metrics import (
    record_rate_limit_fallback,
    record_rate_limited,
)
from tricolink.infra.ratelimit.memory import MemoryTokenBucket
from tricolink.infra.ratelimit.models import RateLimitResult
from tricolink.infra.ratelimit.policies import BucketPolicy
from tricolink.infra.resilience import CircuitBreaker, CircuitOpenError


class TokenBucketBackend(Protocol):
    async def consume(
        self,
        key: str,
        policy: BucketPolicy,
        cost: int = 1,
    ) -> RateLimitResult: ...


class RateLimiter:
    """Token bucket service with Redis primary and in-memory fallback."""

    def __init__(
        self,
        *,
        redis: TokenBucketBackend,
        policies: Mapping[str, BucketPolicy],
        memory: MemoryTokenBucket,
        breaker: CircuitBreaker | None = None,
        redis_timeout_seconds: float = 2.0,
    ) -> None:
        self._redis = redis
        self._policies = dict(policies)
        self._memory = memory
        self._breaker = breaker
        self._redis_timeout_seconds = redis_timeout_seconds

    @property
    def policies(self) -> Mapping[str, BucketPolicy]:
        return self._policies

    async def check(
        self,
        scope: str,
        key: str,
        cost: int = 1,
    ) -> RateLimitResult:
        if cost < 1:
            raise ValueError("cost must be at least 1")
        policy = self._policies[scope]
        bucket_key = f"rl:{scope}:{key}"

        try:
            result = await self._consume_redis(bucket_key, policy, cost)
        except (RedisError, TimeoutError, OSError, CircuitOpenError):
            record_rate_limit_fallback()
            result = replace(
                await self._memory.consume(bucket_key, policy, cost),
                degraded=True,
            )

        if not result.allowed:
            record_rate_limited(scope)
        return result

    async def _consume_redis(
        self,
        key: str,
        policy: BucketPolicy,
        cost: int,
    ) -> RateLimitResult:
        async def operation() -> RateLimitResult:
            return await asyncio.wait_for(
                self._redis.consume(key, policy, cost),
                timeout=self._redis_timeout_seconds,
            )

        if self._breaker is None:
            return await operation()
        async with self._breaker.guard():
            return await operation()
