import asyncio
import uuid

import httpx
import pytest
import structlog
from fastapi import FastAPI

from tricolink.core.middleware.request_context import RequestIDMiddleware
from tricolink.core.middleware.security_headers import SecurityHeadersMiddleware
from tricolink.core.middleware.timeout import RequestTimeoutMiddleware


def build_inner() -> FastAPI:
    inner = FastAPI()

    @inner.get("/context")
    async def context() -> dict[str, str]:
        values = structlog.contextvars.get_contextvars()
        return {"request_id": str(values.get("request_id", ""))}

    @inner.get("/slow")
    async def slow() -> dict[str, str]:
        await asyncio.sleep(0.2)
        return {"status": "ok"}

    @inner.get("/fast")
    async def fast() -> dict[str, str]:
        return {"status": "ok"}

    return inner


@pytest.mark.asyncio
async def test_request_id_is_generated_and_returned() -> None:
    app = RequestIDMiddleware(build_inner())
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/context")

    request_id = response.headers["x-request-id"]
    uuid.UUID(request_id)
    assert response.json()["request_id"] == request_id


@pytest.mark.asyncio
async def test_request_id_accepts_only_safe_values() -> None:
    app = RequestIDMiddleware(build_inner())
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        valid = await client.get("/context", headers={"x-request-id": "abc.DEF-123_456"})
        invalid = await client.get("/context", headers={"x-request-id": "bad id\ninjected"})

    assert valid.headers["x-request-id"] == "abc.DEF-123_456"
    assert invalid.headers["x-request-id"] != "bad id\ninjected"
    uuid.UUID(invalid.headers["x-request-id"])


@pytest.mark.asyncio
async def test_security_headers_are_added() -> None:
    app = SecurityHeadersMiddleware(build_inner(), is_production=False)
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/fast")

    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"
    assert response.headers["cross-origin-opener-policy"] == "same-origin"
    assert "strict-transport-security" not in response.headers


@pytest.mark.asyncio
async def test_hsts_only_in_production() -> None:
    app = SecurityHeadersMiddleware(build_inner(), is_production=True)
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/fast")

    assert "max-age=" in response.headers["strict-transport-security"]


@pytest.mark.asyncio
async def test_timeout_returns_504() -> None:
    app = RequestTimeoutMiddleware(build_inner(), timeout_seconds=0.05)
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/slow")

    assert response.status_code == 504
    assert response.json()["error"]["code"] == "request_timeout"


@pytest.mark.asyncio
async def test_timeout_allows_fast_requests() -> None:
    app = RequestTimeoutMiddleware(build_inner(), timeout_seconds=1.0)
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/fast")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
