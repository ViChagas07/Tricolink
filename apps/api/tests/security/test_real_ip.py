import httpx
import pytest
from fastapi import Depends, FastAPI, Request

from tricolink.core.error_handlers import install_error_handlers
from tricolink.core.middleware.real_ip import RealIPMiddleware, resolve_real_ip
from tricolink.infra.ratelimit import BucketPolicy, RateLimiter, rate_limit
from tricolink.infra.ratelimit.memory import MemoryTokenBucket


def test_resolve_real_ip_without_trusted_proxies_ignores_header() -> None:
    assert resolve_real_ip("10.0.0.5", "1.2.3.4", trusted_proxy_count=0) == "10.0.0.5"


def test_resolve_real_ip_counts_from_the_right() -> None:
    assert (
        resolve_real_ip(
            "10.0.0.5",
            "spoofed, 203.0.113.9",
            trusted_proxy_count=1,
        )
        == "203.0.113.9"
    )
    assert (
        resolve_real_ip(
            "10.0.0.5",
            "1.2.3.4, 203.0.113.9, 198.51.100.7",
            trusted_proxy_count=2,
        )
        == "203.0.113.9"
    )


def test_resolve_real_ip_falls_back_when_header_is_invalid_or_short() -> None:
    assert resolve_real_ip("10.0.0.5", "not-an-ip", trusted_proxy_count=1) == "10.0.0.5"
    assert resolve_real_ip("10.0.0.5", "203.0.113.9", trusted_proxy_count=2) == "10.0.0.5"


@pytest.mark.asyncio
async def test_middleware_sets_request_client_to_real_ip() -> None:
    inner = FastAPI()

    @inner.get("/ip")
    async def ip(request: Request) -> dict[str, str | None]:
        return {
            "client": request.client.host if request.client else None,
            "real_ip": getattr(request.state, "real_ip", None),
        }

    app = RealIPMiddleware(inner, trusted_proxy_count=1)
    transport = httpx.ASGITransport(app=app, client=("10.0.0.5", 1234))

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/ip",
            headers={"x-forwarded-for": "1.2.3.4, 203.0.113.9"},
        )

    assert response.json() == {"client": "203.0.113.9", "real_ip": "203.0.113.9"}


@pytest.mark.asyncio
async def test_spoofed_xff_cannot_bypass_rate_limit() -> None:
    inner = FastAPI()
    install_error_handlers(inner)
    inner.state.rate_limiter = RateLimiter(
        redis=_NeverRedis(),  # type: ignore[arg-type]
        policies={"redirect": BucketPolicy(capacity=2, refill_per_sec=0.0)},
        memory=MemoryTokenBucket(),
    )

    @inner.get("/ping", dependencies=[Depends(rate_limit("redirect"))])
    async def ping() -> dict[str, str]:
        return {"status": "ok"}

    app = RealIPMiddleware(inner, trusted_proxy_count=1)
    transport = httpx.ASGITransport(app=app, client=("10.0.0.5", 1234))

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        first = await client.get("/ping", headers={"x-forwarded-for": "1.1.1.1, 203.0.113.9"})
        second = await client.get("/ping", headers={"x-forwarded-for": "2.2.2.2, 203.0.113.9"})
        third = await client.get("/ping", headers={"x-forwarded-for": "3.3.3.3, 203.0.113.9"})

    assert first.status_code == 200
    assert second.status_code == 200
    assert third.status_code == 429
    assert third.json()["error"]["code"] == "rate_limited"


class _NeverRedis:
    async def consume(self, *args: object, **kwargs: object) -> None:
        from redis.exceptions import ConnectionError as RedisConnectionError

        raise RedisConnectionError("down")
