from __future__ import annotations

from starlette.types import ASGIApp, Message, Receive, Scope, Send

_BASE_HEADERS: tuple[tuple[bytes, bytes], ...] = (
    (b"x-content-type-options", b"nosniff"),
    (b"x-frame-options", b"DENY"),
    (b"referrer-policy", b"strict-origin-when-cross-origin"),
    (
        b"permissions-policy",
        b"camera=(), microphone=(), geolocation=(), payment=(), usb=()",
    ),
    (b"cross-origin-opener-policy", b"same-origin"),
)

_HSTS_HEADER = (
    b"strict-transport-security",
    b"max-age=63072000; includeSubDomains; preload",
)


class SecurityHeadersMiddleware:
    def __init__(self, app: ASGIApp, *, is_production: bool) -> None:
        self._app = app
        self._headers = (*_BASE_HEADERS, _HSTS_HEADER) if is_production else _BASE_HEADERS

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        async def send_with_headers(message: Message) -> None:
            if message["type"] == "http.response.start":
                existing = {key.lower() for key, _ in message.get("headers", [])}
                headers = list(message.get("headers", []))
                headers.extend((key, value) for key, value in self._headers if key not in existing)
                message = {**message, "headers": headers}
            await send(message)

        await self._app(scope, receive, send_with_headers)
