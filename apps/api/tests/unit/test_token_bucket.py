import asyncio

import pytest
from redis.exceptions import ConnectionError as RedisConnectionError

from tricolink.infra.ratelimit import BucketPolicy
from tricolink.infra.ratelimit.memory import MemoryTokenBucket
from tricolink.infra.ratelimit.service import RateLimiter


class FakeClock:
    def __init__(self) -> None:
        self.value = 1000.0

    def __call__(self) -> float:
        return self.value

    def advance(self, seconds: float) -> None:
        self.value += seconds


class DownRedis:
    async def consume(self, key: str, policy: BucketPolicy, cost: int = 1) -> None:
        raise RedisConnectionError("redis is down")


@pytest.mark.asyncio
async def test_memory_bucket_consumes_and_exhausts() -> None:
    clock = FakeClock()
    bucket = MemoryTokenBucket(clock=clock)
    policy = BucketPolicy(capacity=5, refill_per_sec=1.0)

    results = [await bucket.consume("rl:test:1", policy) for _ in range(5)]

    assert all(result.allowed for result in results)
    assert results[-1].remaining == 0

    denied = await bucket.consume("rl:test:1", policy)
    assert denied.allowed is False
    assert denied.remaining == 0
    assert denied.retry_after_ms == 1000


@pytest.mark.asyncio
async def test_memory_bucket_refills() -> None:
    clock = FakeClock()
    bucket = MemoryTokenBucket(clock=clock)
    policy = BucketPolicy(capacity=2, refill_per_sec=2.0)

    await bucket.consume("key", policy)
    await bucket.consume("key", policy)
    assert not (await bucket.consume("key", policy)).allowed

    clock.advance(1.0)
    assert (await bucket.consume("key", policy)).allowed
    assert (await bucket.consume("key", policy)).allowed
    assert not (await bucket.consume("key", policy)).allowed


@pytest.mark.asyncio
async def test_memory_bucket_never_exceeds_capacity() -> None:
    clock = FakeClock()
    bucket = MemoryTokenBucket(clock=clock)
    policy = BucketPolicy(capacity=3, refill_per_sec=0.0)

    results = await asyncio.gather(*(bucket.consume("key", policy) for _ in range(100)))

    assert sum(1 for result in results if result.allowed) == 3


@pytest.mark.asyncio
async def test_rate_limiter_falls_back_to_memory_when_redis_is_down() -> None:
    clock = FakeClock()
    memory = MemoryTokenBucket(clock=clock)
    limiter = RateLimiter(
        redis=DownRedis(),  # type: ignore[arg-type]
        policies={"test": BucketPolicy(capacity=4, refill_per_sec=1.0)},
        memory=memory,
    )

    results = await asyncio.gather(*(limiter.check("test", "1.2.3.4") for _ in range(20)))

    assert sum(1 for result in results if result.allowed) == 4
    assert all(result.degraded for result in results)


@pytest.mark.asyncio
async def test_rate_limiter_rejects_unknown_scope() -> None:
    limiter = RateLimiter(
        redis=DownRedis(),  # type: ignore[arg-type]
        policies={"test": BucketPolicy(capacity=1, refill_per_sec=1.0)},
        memory=MemoryTokenBucket(),
    )

    with pytest.raises(KeyError):
        await limiter.check("missing", "user")
