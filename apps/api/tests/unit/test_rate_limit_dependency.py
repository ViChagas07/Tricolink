import httpx
import pytest
from fastapi import Depends, FastAPI

from tricolink.core.error_handlers import install_error_handlers
from tricolink.infra.ratelimit import BucketPolicy, MemoryTokenBucket, rate_limit
from tricolink.infra.ratelimit.service import RateLimiter


class DownRedis:
    async def consume(self, key: str, policy: BucketPolicy, cost: int = 1) -> None:
        from redis.exceptions import ConnectionError as RedisConnectionError

        raise RedisConnectionError("down")


@pytest.mark.asyncio
async def test_rate_limit_dependency_sets_headers_and_429() -> None:
    app = FastAPI()
    install_error_handlers(app)
    app.state.rate_limiter = RateLimiter(
        redis=DownRedis(),  # type: ignore[arg-type]
        policies={"test": BucketPolicy(capacity=2, refill_per_sec=0.0)},
        memory=MemoryTokenBucket(),
    )
    dependency = rate_limit("test")

    @app.get("/limited", dependencies=[Depends(dependency)])
    async def limited() -> dict[str, str]:
        return {"status": "ok"}

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        first = await client.get("/limited")
        second = await client.get("/limited")
        third = await client.get("/limited")

    assert first.status_code == 200
    assert first.headers["ratelimit-limit"] == "2"
    assert first.headers["ratelimit-remaining"] == "1"
    assert second.headers["ratelimit-remaining"] == "0"
    assert third.status_code == 429
    assert third.json()["error"]["code"] == "rate_limited"
    assert third.headers["retry-after"] == "60"
