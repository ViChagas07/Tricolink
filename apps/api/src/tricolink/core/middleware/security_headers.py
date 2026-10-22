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

# The API only returns JSON, metrics text and the static 404/410 HTML pages.
# A deny-by-default CSP costs nothing for those documents and neutralises the
# HTML pages if they ever regress. Docs/Swagger stay out of production.
_PRODUCTION_CSP = (
    b"content-security-policy",
    b"default-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'",
)

_NO_STORE_PREFIXES = ("/api/v1/auth", "/metrics")


class SecurityHeadersMiddleware:
    def __init__(self, app: ASGIApp, *, is_production: bool) -> None:
        self._app = app
        self._headers = (
            (*_BASE_HEADERS, _HSTS_HEADER, _PRODUCTION_CSP)
            if is_production
            else _BASE_HEADERS
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        path = str(scope.get("path", ""))

        async def send_with_headers(message: Message) -> None:
            if message["type"] == "http.response.start":
                existing = {key.lower() for key, _ in message.get("headers", [])}
                headers = list(message.get("headers", []))
                headers.extend((key, value) for key, value in self._headers if key not in existing)
                if (
                    any(path.startswith(prefix) for prefix in _NO_STORE_PREFIXES)
                    and b"cache-control" not in existing
                ):
                    headers.append((b"cache-control", b"no-store"))
                message = {**message, "headers": headers}
            await send(message)

        await self._app(scope, receive, send_with_headers)
