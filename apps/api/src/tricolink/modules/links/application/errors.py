from __future__ import annotations

from tricolink.shared_kernel.errors import AppError


class UrlNotAllowed(AppError):
    def __init__(self, message: str = "URL is not allowed") -> None:
        super().__init__(code="invalid_url", message=message, status_code=400)


class InvalidAlias(AppError):
    def __init__(self, message: str = "Alias must match ^[A-Za-z0-9_-]{3,32}$") -> None:
        super().__init__(code="invalid_alias", message=message, status_code=400)


class AliasReserved(AppError):
    def __init__(self) -> None:
        super().__init__(
            code="alias_reserved",
            message="This alias is reserved",
            status_code=409,
        )


class AliasTaken(AppError):
    def __init__(self) -> None:
        super().__init__(
            code="alias_taken",
            message="This alias is already in use",
            status_code=409,
        )


class CodeGenerationFailed(AppError):
    def __init__(self) -> None:
        super().__init__(
            code="code_generation_failed",
            message="Could not allocate a short code, try again",
            status_code=503,
        )


class LinkNotFound(AppError):
    def __init__(self) -> None:
        super().__init__(code="not_found", message="Link not found", status_code=404)


class InvalidCursor(AppError):
    def __init__(self) -> None:
        super().__init__(code="invalid_cursor", message="Invalid cursor", status_code=400)


class InvalidPagination(AppError):
    def __init__(self, message: str = "Limit must be between 1 and 50") -> None:
        super().__init__(code="invalid_pagination", message=message, status_code=400)


class InvalidTitle(AppError):
    def __init__(self, message: str = "Title is invalid") -> None:
        super().__init__(code="invalid_title", message=message, status_code=400)


class InvalidExpiresAt(AppError):
    def __init__(self, message: str = "Expiration must be in the future") -> None:
        super().__init__(code="invalid_expires_at", message=message, status_code=400)


class DailyQuotaExceeded(AppError):
    def __init__(self, retry_after_seconds: int) -> None:
        super().__init__(
            code="daily_quota_exceeded",
            message="Daily link creation quota exceeded",
            status_code=429,
            headers={"Retry-After": str(max(1, retry_after_seconds))},
        )


class LoginRequired(AppError):
    def __init__(self) -> None:
        super().__init__(
            code="login_required",
            message="Login is required to use this option",
            status_code=401,
            headers={"WWW-Authenticate": "Bearer"},
        )
