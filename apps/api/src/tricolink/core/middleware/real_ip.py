from __future__ import annotations

import ipaddress

from starlette.types import ASGIApp, Receive, Scope, Send


def resolve_real_ip(peer_ip: str, forwarded_for: str | None, *, trusted_proxy_count: int) -> str:
    """Resolve the client address without trusting attacker-controlled entries.

    ``X-Forwarded-For`` grows to the right: each proxy appends the address it
    received the connection from. With ``N`` trusted proxies in front of the
    app, the real client is the ``N``-th entry from the right. Anything to the
    left of it was supplied by the client and must be ignored.
    """

    if trusted_proxy_count <= 0 or not forwarded_for:
        return peer_ip

    parts = [part.strip() for part in forwarded_for.split(",") if part.strip()]
    if len(parts) < trusted_proxy_count:
        return peer_ip

    candidate = parts[-trusted_proxy_count]
    try:
        return str(ipaddress.ip_address(candidate))
    except ValueError:
        return peer_ip


def _forwarded_for(scope: Scope) -> str | None:
    values = [
        value.decode("latin-1")
        for key, value in scope.get("headers", [])
        if key.lower() == b"x-forwarded-for"
    ]
    return ",".join(values) if values else None


class RealIPMiddleware:
    def __init__(self, app: ASGIApp, *, trusted_proxy_count: int) -> None:
        self._app = app
        self._trusted_proxy_count = trusted_proxy_count

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        client = scope.get("client")
        peer_ip = client[0] if client else "unknown"
        real_ip = resolve_real_ip(
            peer_ip,
            _forwarded_for(scope),
            trusted_proxy_count=self._trusted_proxy_count,
        )

        if real_ip != peer_ip:
            port = client[1] if client else 0
            scope["client"] = (real_ip, port)
        scope.setdefault("state", {})["real_ip"] = real_ip

        await self._app(scope, receive, send)
