import httpx
import pytest
from fastapi import FastAPI

from tricolink.core.middleware.global_rate_limit import GlobalRateLimitMiddleware
from tricolink.infra.ratelimit import BucketPolicy, MemoryTokenBucket
from tricolink.infra.ratelimit.service import RateLimiter


class DownRedis:
    async def consume(self, key: str, policy: BucketPolicy, cost: int = 1) -> None:
        from redis.exceptions import ConnectionError as RedisConnectionError

        raise RedisConnectionError("down")


@pytest.mark.asyncio
async def test_global_bucket_is_shared_across_clients() -> None:
    inner = FastAPI()

    @inner.get("/ping")
    async def ping() -> dict[str, str]:
        return {"status": "ok"}

    limiter = RateLimiter(
        redis=DownRedis(),  # type: ignore[arg-type]
        policies={"global": BucketPolicy(capacity=2, refill_per_sec=0.0)},
        memory=MemoryTokenBucket(),
    )
    app = GlobalRateLimitMiddleware(inner, limiter)

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app, client=("10.0.0.1", 1)),
        base_url="http://test",
    ) as first_client:
        assert (await first_client.get("/ping")).status_code == 200
        assert (await first_client.get("/ping")).status_code == 200

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app, client=("10.0.0.2", 2)),
        base_url="http://test",
    ) as second_client:
        response = await second_client.get("/ping")

    assert response.status_code == 429
    assert response.json()["error"]["code"] == "rate_limited"
    assert response.headers["retry-after"] == "60"
    assert response.headers["ratelimit-limit"] == "2"
