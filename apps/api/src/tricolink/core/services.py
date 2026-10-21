from __future__ import annotations

from dataclasses import dataclass

from redis.asyncio import Redis

from tricolink.core.config import Settings
from tricolink.infra.cache import CacheClient, close_redis, create_redis, ping_redis
from tricolink.infra.db import Database
from tricolink.infra.ratelimit import (
    MemoryTokenBucket,
    RateLimiter,
    RedisTokenBucket,
    build_policies,
)
from tricolink.infra.resilience import CircuitBreaker, build_bulkheads
from tricolink.infra.resilience.bulkhead import BulkheadRegistry


@dataclass(slots=True)
class Services:
    settings: Settings
    redis: Redis
    cache: CacheClient
    database: Database
    rate_limiter: RateLimiter
    redis_breaker: CircuitBreaker
    database_breaker: CircuitBreaker
    bulkheads: BulkheadRegistry

    async def redis_ping(self) -> None:
        async with self.redis_breaker.guard():
            await ping_redis(
                self.redis,
                timeout_seconds=self.settings.redis_timeout_seconds,
            )

    async def close(self) -> None:
        await close_redis(self.redis)
        await self.database.dispose()


def build_services(settings: Settings) -> Services:
    bulkheads = build_bulkheads(settings)
    redis_breaker = CircuitBreaker(
        "redis",
        failure_threshold=settings.circuit_breaker_failure_threshold,
        recovery_timeout=settings.circuit_breaker_recovery_timeout_seconds,
        half_open_max_calls=settings.circuit_breaker_half_open_max_calls,
    )
    database_breaker = CircuitBreaker(
        "postgres",
        failure_threshold=settings.circuit_breaker_failure_threshold,
        recovery_timeout=settings.circuit_breaker_recovery_timeout_seconds,
        half_open_max_calls=settings.circuit_breaker_half_open_max_calls,
    )
    redis = create_redis(settings)
    database = Database(
        settings,
        breaker=database_breaker,
        read_bulkhead=bulkheads.get("db_read"),
        write_bulkhead=bulkheads.get("db_write"),
    )
    limiter = RateLimiter(
        redis=RedisTokenBucket(redis),
        policies=build_policies(settings),
        memory=MemoryTokenBucket(),
        breaker=redis_breaker,
        redis_timeout_seconds=settings.redis_timeout_seconds,
    )
    return Services(
        settings=settings,
        redis=redis,
        cache=CacheClient(redis, namespace="cache"),
        database=database,
        rate_limiter=limiter,
        redis_breaker=redis_breaker,
        database_breaker=database_breaker,
        bulkheads=bulkheads,
    )
