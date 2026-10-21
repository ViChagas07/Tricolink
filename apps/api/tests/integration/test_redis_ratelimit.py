import asyncio
import uuid

import pytest
from redis.asyncio import Redis

from tricolink.infra.ratelimit import BucketPolicy, RedisTokenBucket

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_lua_bucket_is_atomic_under_concurrency(redis_client: Redis) -> None:
    key = f"test:rl:{uuid.uuid4().hex}"
    bucket = RedisTokenBucket(redis_client)
    policy = BucketPolicy(capacity=10, refill_per_sec=0.0)

    results = await asyncio.gather(*(bucket.consume(key, policy) for _ in range(100)))

    assert sum(1 for result in results if result.allowed) == 10
    assert all(result.limit == 10 for result in results)
    await redis_client.delete(key)


@pytest.mark.asyncio
async def test_lua_bucket_consumes_exhausts_and_refills(redis_client: Redis) -> None:
    key = f"test:rl:{uuid.uuid4().hex}"
    bucket = RedisTokenBucket(redis_client)
    policy = BucketPolicy(capacity=5, refill_per_sec=50.0)

    first = [await bucket.consume(key, policy) for _ in range(5)]
    denied = await bucket.consume(key, policy)

    assert all(result.allowed for result in first)
    assert denied.allowed is False
    assert denied.retry_after_ms > 0

    await asyncio.sleep(0.15)
    assert (await bucket.consume(key, policy)).allowed
    await redis_client.delete(key)


@pytest.mark.asyncio
async def test_lua_bucket_keeps_keys_independent(redis_client: Redis) -> None:
    prefix = f"test:rl:{uuid.uuid4().hex}"
    bucket = RedisTokenBucket(redis_client)
    policy = BucketPolicy(capacity=1, refill_per_sec=0.0)

    assert (await bucket.consume(f"{prefix}:a", policy)).allowed
    assert not (await bucket.consume(f"{prefix}:a", policy)).allowed
    assert (await bucket.consume(f"{prefix}:b", policy)).allowed

    await redis_client.delete(f"{prefix}:a", f"{prefix}:b")
