from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class AppError(Exception):
    """Base application error rendered as ``{"error": {code, message}}``."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        *,
        details: Any = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        self.headers = dict(headers) if headers else None


class BadRequestError(AppError):
    def __init__(self, message: str = "Bad request", *, code: str = "bad_request") -> None:
        super().__init__(code=code, message=message, status_code=400)


class NotFoundError(AppError):
    def __init__(self, message: str = "Not found") -> None:
        super().__init__(code="not_found", message=message, status_code=404)


class ConflictError(AppError):
    def __init__(self, message: str = "Conflict") -> None:
        super().__init__(code="conflict", message=message, status_code=409)


class PayloadTooLargeError(AppError):
    def __init__(self, message: str = "Payload too large") -> None:
        super().__init__(code="payload_too_large", message=message, status_code=413)


class ServiceUnavailableError(AppError):
    def __init__(self, message: str = "Service temporarily unavailable") -> None:
        super().__init__(code="service_unavailable", message=message, status_code=503)


class GatewayTimeoutError(AppError):
    def __init__(self, message: str = "Request timed out") -> None:
        super().__init__(code="request_timeout", message=message, status_code=504)


def error_payload(code: str, message: str, details: Any = None) -> dict[str, Any]:
    error: dict[str, Any] = {"code": code, "message": message}
    if details is not None:
        error["details"] = details
    return {"error": error}
