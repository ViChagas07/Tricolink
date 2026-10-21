from tricolink.shared_kernel.errors import AppError


class AuthenticationError(AppError):
    def __init__(self, message: str = "Authentication required") -> None:
        super().__init__(code="authentication_required", message=message, status_code=401)


class AuthorizationError(AppError):
    def __init__(self, message: str = "Not allowed") -> None:
        super().__init__(code="not_allowed", message=message, status_code=403)
