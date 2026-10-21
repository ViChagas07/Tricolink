from __future__ import annotations

import time

from starlette.types import ASGIApp, Message, Receive, Scope, Send

from tricolink.core.logging import get_logger
from tricolink.infra.observability.metrics import record_request

logger = get_logger("tricolink.request")


class MetricsMiddleware:
    """Records request counters/latency and one structured access log line."""

    def __init__(self, app: ASGIApp) -> None:
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        started = time.perf_counter()
        status = 500

        async def capture_status(message: Message) -> None:
            nonlocal status
            if message["type"] == "http.response.start":
                status = int(message["status"])
            await send(message)

        try:
            await self._app(scope, receive, capture_status)
        finally:
            path = _route_path(scope)
            method = str(scope.get("method", "UNKNOWN"))
            duration = time.perf_counter() - started
            record_request(method, path, status, duration)
            logger.info(
                "http_request",
                method=method,
                path=path,
                status=status,
                duration_ms=round(duration * 1000, 2),
            )


def _route_path(scope: Scope) -> str:
    route = scope.get("route")
    if route is None:
        return "unmatched"
    return str(getattr(route, "path", "unmatched"))
