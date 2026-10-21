class InvalidEmailError(ValueError):
    """Raised when an email address is not valid."""


class WeakPasswordError(ValueError):
    """Raised when a password does not meet the password policy."""


class InvalidGoogleIdentityError(ValueError):
    """Raised when Google OIDC claims cannot be trusted."""


class DuplicateUserError(ValueError):
    """Raised by the repository when an email or Google subject already exists."""
