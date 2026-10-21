from __future__ import annotations

from tricolink.shared_kernel.errors import AppError


class AuthenticationError(AppError):
    def __init__(self, message: str = "Authentication required") -> None:
        super().__init__(
            code="authentication_required",
            message=message,
            status_code=401,
            headers={"WWW-Authenticate": "Bearer"},
        )


class AuthorizationError(AppError):
    def __init__(self, message: str = "Not allowed") -> None:
        super().__init__(code="not_allowed", message=message, status_code=403)


class CsrfError(AppError):
    def __init__(self, message: str = "Invalid CSRF token") -> None:
        super().__init__(code="invalid_csrf_token", message=message, status_code=403)


class RateLimitExceeded(AppError):
    def __init__(
        self,
        *,
        retry_after_seconds: int = 1,
        limit: int | None = None,
        remaining: int | None = None,
        reset_after_seconds: int | None = None,
        message: str = "Too many requests",
    ) -> None:
        headers: dict[str, str] = {"Retry-After": str(max(1, retry_after_seconds))}
        if limit is not None:
            headers["RateLimit-Limit"] = str(limit)
        if remaining is not None:
            headers["RateLimit-Remaining"] = str(max(0, remaining))
        if reset_after_seconds is not None:
            headers["RateLimit-Reset"] = str(max(0, reset_after_seconds))
        super().__init__(
            code="rate_limited",
            message=message,
            status_code=429,
            headers=headers,
        )


class MetricsAuthenticationError(AppError):
    def __init__(self, message: str = "Metrics access requires a valid token") -> None:
        super().__init__(
            code="authentication_required",
            message=message,
            status_code=401,
            headers={"WWW-Authenticate": "Bearer"},
        )


class CircuitOpenError(AppError):
    def __init__(self, dependency: str) -> None:
        super().__init__(
            code="circuit_open",
            message=f"{dependency} is temporarily unavailable",
            status_code=503,
            headers={"Retry-After": "5"},
        )


class BulkheadFullError(AppError):
    def __init__(self, name: str) -> None:
        super().__init__(
            code="service_busy",
            message=f"{name} capacity exhausted",
            status_code=503,
            headers={"Retry-After": "1"},
        )
