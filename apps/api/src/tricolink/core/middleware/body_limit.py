from __future__ import annotations

import json

from starlette.types import ASGIApp, Message, Receive, Scope, Send


def _header_values(scope: Scope, name: bytes) -> list[bytes]:
    values: list[bytes] = []
    for key, value in scope.get("headers", []):
        if key.lower() == name:
            values.append(value)
    return values


async def _send_json(
    send: Send,
    status: int,
    code: str,
    message: str,
) -> None:
    body = json.dumps({"error": {"code": code, "message": message}}).encode("utf-8")
    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(body)).encode("ascii")),
            ],
        }
    )
    await send({"type": "http.response.body", "body": body})


class BodyLimitMiddleware:
    """Rejects oversized bodies before the application reads them.

    ``Content-Length`` is checked first (cheap rejection). Bodies without a
    reliable length are buffered up to the limit and replayed to the app, so a
    chunked request can never grow past ``max_body_bytes``.
    """

    def __init__(self, app: ASGIApp, *, max_body_bytes: int) -> None:
        if max_body_bytes < 1:
            raise ValueError("max_body_bytes must be positive")
        self._app = app
        self._max_body_bytes = max_body_bytes

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        if not await self._content_length_is_valid(scope, send):
            return

        body, disconnected = await self._read_bounded_body(receive, send)
        if body is None:
            return

        if disconnected:

            async def replay_disconnect() -> Message:
                return {"type": "http.disconnect"}

            await self._app(scope, replay_disconnect, send)
            return

        body_sent = False

        async def replay_body() -> Message:
            nonlocal body_sent
            if not body_sent:
                body_sent = True
                return {"type": "http.request", "body": body, "more_body": False}
            message = await receive()
            if message["type"] == "http.request":
                return {"type": "http.request", "body": b"", "more_body": False}
            return message

        await self._app(scope, replay_body, send)

    async def _content_length_is_valid(self, scope: Scope, send: Send) -> bool:
        content_lengths = _header_values(scope, b"content-length")
        if not content_lengths:
            return True

        parsed: list[int] = []
        for raw in content_lengths:
            try:
                parsed.append(int(raw.decode("ascii")))
            except (UnicodeDecodeError, ValueError):
                await _send_json(
                    send,
                    400,
                    "invalid_content_length",
                    "Invalid Content-Length header",
                )
                return False

        if len(set(parsed)) > 1:
            await _send_json(
                send,
                400,
                "invalid_content_length",
                "Conflicting Content-Length headers",
            )
            return False
        if parsed[0] < 0:
            await _send_json(
                send,
                400,
                "invalid_content_length",
                "Invalid Content-Length header",
            )
            return False
        if parsed[0] > self._max_body_bytes:
            await _send_json(
                send,
                413,
                "payload_too_large",
                f"Request body must not exceed {self._max_body_bytes} bytes",
            )
            return False
        return True

    async def _read_bounded_body(
        self,
        receive: Receive,
        send: Send,
    ) -> tuple[bytes | None, bool]:
        chunks: list[bytes] = []
        total = 0
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return b"".join(chunks), True
            if message["type"] != "http.request":
                continue
            chunk = message.get("body", b"")
            total += len(chunk)
            if total > self._max_body_bytes:
                await _send_json(
                    send,
                    413,
                    "payload_too_large",
                    f"Request body must not exceed {self._max_body_bytes} bytes",
                )
                return None, False
            chunks.append(chunk)
            if not message.get("more_body", False):
                return b"".join(chunks), False
