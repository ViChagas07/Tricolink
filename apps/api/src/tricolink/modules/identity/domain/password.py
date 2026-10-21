from __future__ import annotations

import unicodedata
from dataclasses import dataclass

from tricolink.modules.identity.domain.email import Email
from tricolink.modules.identity.domain.errors import WeakPasswordError

MIN_PASSWORD_LENGTH = 10
MAX_PASSWORD_LENGTH = 128

COMMON_PASSWORDS = frozenset(
    {
        "1234567890",
        "12345678910",
        "abcdefghij",
        "admin12345",
        "letmein123",
        "password",
        "password1",
        "password12",
        "password123",
        "password1234",
        "qwertyuiop",
        "senha123456",
        "tricolink",
        "tricolink123",
        "welcome123",
        "welcome1234",
    }
)


@dataclass(frozen=True, slots=True)
class PasswordPolicy:
    min_length: int = MIN_PASSWORD_LENGTH
    max_length: int = MAX_PASSWORD_LENGTH

    def validate(self, password: str, *, email: Email | None = None) -> None:
        if not isinstance(password, str):
            raise WeakPasswordError("Password is invalid")
        if len(password) < self.min_length:
            raise WeakPasswordError(f"Password must have at least {self.min_length} characters")
        if len(password) > self.max_length:
            raise WeakPasswordError(f"Password must have at most {self.max_length} characters")
        if not password.strip():
            raise WeakPasswordError("Password is too weak")

        for char in password:
            if unicodedata.category(char)[0] == "C":
                raise WeakPasswordError("Password contains invalid characters")

        folded = password.casefold()
        if folded in COMMON_PASSWORDS or password.lower() in COMMON_PASSWORDS:
            raise WeakPasswordError("Password is too common")
        if len(set(password)) == 1:
            raise WeakPasswordError("Password is too predictable")

        if email is not None:
            local_part = email.value.split("@", 1)[0]
            if len(local_part) >= self.min_length and folded == local_part.casefold():
                raise WeakPasswordError("Password is too predictable")
