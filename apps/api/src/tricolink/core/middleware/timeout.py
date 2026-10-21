from __future__ import annotations

import asyncio
import json

from starlette.types import ASGIApp, Message, Receive, Scope, Send


class RequestTimeoutMiddleware:
    """Caps the total time spent inside the application for one request."""

    def __init__(self, app: ASGIApp, *, timeout_seconds: float) -> None:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self._app = app
        self._timeout_seconds = timeout_seconds

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        response_started = False

        async def tracked_send(message: Message) -> None:
            nonlocal response_started
            if message["type"] == "http.response.start":
                response_started = True
            await send(message)

        async def run() -> None:
            await self._app(scope, receive, tracked_send)

        task: asyncio.Task[None] = asyncio.create_task(run())
        try:
            await asyncio.wait_for(task, timeout=self._timeout_seconds)
        except TimeoutError:
            if response_started:
                return
            body = json.dumps(
                {
                    "error": {
                        "code": "request_timeout",
                        "message": "Request timed out",
                    }
                }
            ).encode("utf-8")
            await send(
                {
                    "type": "http.response.start",
                    "status": 504,
                    "headers": [
                        (b"content-type", b"application/json"),
                        (b"content-length", str(len(body)).encode("ascii")),
                    ],
                }
            )
            await send({"type": "http.response.body", "body": body})
