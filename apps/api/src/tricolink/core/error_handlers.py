from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from tricolink.core.logging import get_logger
from tricolink.shared_kernel.errors import AppError, error_payload

logger = get_logger("tricolink.errors")

_HTTP_CODES: dict[int, tuple[str, str]] = {
    400: ("bad_request", "Bad request"),
    401: ("authentication_required", "Authentication required"),
    403: ("not_allowed", "Not allowed"),
    404: ("not_found", "Not found"),
    405: ("method_not_allowed", "Method not allowed"),
    409: ("conflict", "Conflict"),
    413: ("payload_too_large", "Payload too large"),
    415: ("unsupported_media_type", "Unsupported media type"),
    422: ("validation_error", "Validation failed"),
    429: ("rate_limited", "Too many requests"),
    500: ("internal_error", "Internal server error"),
    503: ("service_unavailable", "Service temporarily unavailable"),
    504: ("request_timeout", "Request timed out"),
}


def _json_error(
    status_code: int,
    code: str,
    message: str,
    *,
    details: Any = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=error_payload(code, message, details),
        headers=headers,
    )


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
        return _json_error(
            exc.status_code,
            exc.code,
            exc.message,
            details=exc.details,
            headers=exc.headers,
        )

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_exception(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        code, default_message = _HTTP_CODES.get(exc.status_code, ("http_error", "Request failed"))
        message = (
            exc.detail
            if isinstance(exc.detail, str) and exc.status_code < 500
            else (default_message)
        )
        return _json_error(
            exc.status_code,
            code,
            message,
            headers=dict(exc.headers) if exc.headers else None,
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
        details = [
            {
                "loc": list(error.get("loc", ())),
                "msg": error.get("msg", "Invalid value"),
                "type": error.get("type", "value_error"),
            }
            for error in exc.errors()
        ]
        return _json_error(
            422,
            "validation_error",
            "Request validation failed",
            details=details,
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(
            "unhandled_error",
            method=request.method,
            path=request.url.path,
            error_type=type(exc).__name__,
        )
        return _json_error(500, "internal_error", "Internal server error")
