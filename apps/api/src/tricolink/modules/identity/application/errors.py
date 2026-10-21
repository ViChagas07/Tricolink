from __future__ import annotations

from tricolink.shared_kernel.errors import AppError


class InvalidCredentials(AppError):
    def __init__(self) -> None:
        super().__init__(
            code="invalid_credentials",
            message="Invalid email or password",
            status_code=401,
            headers={"WWW-Authenticate": "Bearer"},
        )


class SessionExpired(AppError):
    def __init__(self) -> None:
        super().__init__(
            code="authentication_required",
            message="Session is invalid or expired",
            status_code=401,
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidEmail(AppError):
    def __init__(self, message: str = "Email is invalid") -> None:
        super().__init__(code="invalid_email", message=message, status_code=400)


class WeakPassword(AppError):
    def __init__(self, message: str = "Password is too weak") -> None:
        super().__init__(code="weak_password", message=message, status_code=400)


class AuthLocked(AppError):
    def __init__(self, retry_after_seconds: int) -> None:
        super().__init__(
            code="too_many_attempts",
            message="Too many attempts, try again later",
            status_code=429,
            headers={"Retry-After": str(max(1, retry_after_seconds))},
        )


class InvalidGoogleLogin(AppError):
    def __init__(self, message: str = "Google authentication failed") -> None:
        super().__init__(code="google_auth_failed", message=message, status_code=401)


class GoogleNotConfigured(AppError):
    def __init__(self) -> None:
        super().__init__(
            code="google_not_configured",
            message="Google login is not configured",
            status_code=503,
        )


class InvalidNextPath(AppError):
    def __init__(self) -> None:
        super().__init__(
            code="invalid_next",
            message="Next path must be an internal path",
            status_code=400,
        )


class InvalidProfile(AppError):
    def __init__(self, message: str = "Profile is invalid") -> None:
        super().__init__(code="invalid_profile", message=message, status_code=400)
