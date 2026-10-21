from __future__ import annotations

import json
import math

from starlette.types import ASGIApp, Message, Receive, Scope, Send

from tricolink.infra.ratelimit.models import RateLimitResult
from tricolink.infra.ratelimit.service import RateLimiter

DEFAULT_EXEMPT_PATHS = frozenset({"/health/live", "/health/ready", "/metrics"})
GLOBAL_BUCKET_KEY = "all"


class GlobalRateLimitMiddleware:
    """Global load-shedding bucket applied before the application router."""

    def __init__(
        self,
        app: ASGIApp,
        limiter: RateLimiter,
        *,
        exempt_paths: frozenset[str] = DEFAULT_EXEMPT_PATHS,
    ) -> None:
        self._app = app
        self._limiter = limiter
        self._exempt_paths = exempt_paths

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or scope.get("path", "") in self._exempt_paths:
            await self._app(scope, receive, send)
            return

        result = await self._limiter.check("global", GLOBAL_BUCKET_KEY)

        if not result.allowed:
            body = json.dumps(
                {
                    "error": {
                        "code": "rate_limited",
                        "message": "Too many requests",
                    }
                }
            ).encode("utf-8")
            await send(
                {
                    "type": "http.response.start",
                    "status": 429,
                    "headers": [
                        (b"content-type", b"application/json"),
                        (b"content-length", str(len(body)).encode("ascii")),
                        *[
                            (name.encode(), value.encode())
                            for name, value in _headers(result).items()
                        ],
                    ],
                }
            )
            await send({"type": "http.response.body", "body": body})
            return

        async def send_with_headers(message: Message) -> None:
            if message["type"] == "http.response.start":
                existing = {key.lower() for key, _ in message.get("headers", [])}
                headers = list(message.get("headers", []))
                headers.extend(
                    (name.encode(), value.encode())
                    for name, value in _headers(result).items()
                    if name.lower().encode() not in existing
                )
                message = {**message, "headers": headers}
            await send(message)

        await self._app(scope, receive, send_with_headers)


def _headers(result: RateLimitResult) -> dict[str, str]:
    headers = {
        "RateLimit-Limit": str(result.limit),
        "RateLimit-Remaining": str(result.remaining),
        "RateLimit-Reset": str(max(0, result.reset_after_seconds)),
    }
    if not result.allowed:
        retry_after = (
            max(1, math.ceil(result.retry_after_ms / 1000)) if result.retry_after_ms >= 0 else 60
        )
        headers["Retry-After"] = str(retry_after)
    return headers
