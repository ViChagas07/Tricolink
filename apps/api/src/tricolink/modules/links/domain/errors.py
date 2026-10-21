class InvalidShortCodeError(ValueError):
    """Raised when a short code does not match the public format."""


class InvalidUrlError(ValueError):
    """Raised when a URL violates the product URL policy."""


class ReservedAliasError(ValueError):
    """Raised when a custom alias collides with an application route."""


class DuplicateCodeError(ValueError):
    """Raised by the repository when the code unique constraint is violated."""
