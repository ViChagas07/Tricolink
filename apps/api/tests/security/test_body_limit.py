import json
from collections.abc import AsyncIterator

import httpx
import pytest
from fastapi import FastAPI, Request

from tricolink.core.middleware.body_limit import BodyLimitMiddleware


def build_app(max_body_bytes: int = 100) -> BodyLimitMiddleware:
    inner = FastAPI()

    @inner.post("/echo")
    async def echo(request: Request) -> dict[str, int]:
        body = await request.body()
        return {"size": len(body)}

    return BodyLimitMiddleware(inner, max_body_bytes=max_body_bytes)


@pytest.mark.asyncio
async def test_rejects_content_length_above_limit_before_reading() -> None:
    app = build_app(100)
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/echo", content=b"x" * 101)

    assert response.status_code == 413
    assert response.json()["error"]["code"] == "payload_too_large"


@pytest.mark.asyncio
async def test_rejects_chunked_body_above_limit() -> None:
    app = build_app(100)
    transport = httpx.ASGITransport(app=app)

    async def chunks() -> AsyncIterator[bytes]:
        yield b"x" * 60
        yield b"x" * 60

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/echo", content=chunks())

    assert response.status_code == 413
    assert response.json()["error"]["code"] == "payload_too_large"


@pytest.mark.asyncio
async def test_accepts_body_at_limit() -> None:
    app = build_app(100)
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/echo", content=b"x" * 100)

    assert response.status_code == 200
    assert response.json() == {"size": 100}


@pytest.mark.asyncio
async def test_invalid_content_length_is_rejected() -> None:
    called = False

    async def inner(scope: object, receive: object, send: object) -> None:
        nonlocal called
        called = True

    app = BodyLimitMiddleware(inner, max_body_bytes=100)  # type: ignore[arg-type]
    sent: list[dict[str, object]] = []

    async def receive() -> dict[str, object]:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message: dict[str, object]) -> None:
        sent.append(message)

    scope = {
        "type": "http",
        "headers": [(b"content-length", b"not-a-number")],
    }
    await app(scope, receive, send)  # type: ignore[arg-type]

    assert called is False
    assert sent[0]["status"] == 400
    payload = json.loads(sent[1]["body"])  # type: ignore[arg-type]
    assert payload["error"]["code"] == "invalid_content_length"
