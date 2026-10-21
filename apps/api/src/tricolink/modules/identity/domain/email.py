from __future__ import annotations

import unicodedata
from dataclasses import dataclass

from email_validator import EmailNotValidError, validate_email

from tricolink.modules.identity.domain.errors import InvalidEmailError

MAX_EMAIL_LENGTH = 254


@dataclass(frozen=True, slots=True)
class Email:
    value: str

    @classmethod
    def parse(cls, raw: str) -> Email:
        if not isinstance(raw, str):
            raise InvalidEmailError("Email must be a string")

        normalized = unicodedata.normalize("NFKC", raw).strip().lower()
        if not normalized or len(normalized) > MAX_EMAIL_LENGTH:
            raise InvalidEmailError("Email is invalid")

        try:
            result = validate_email(
                normalized,
                check_deliverability=False,
                allow_smtputf8=True,
            )
        except EmailNotValidError as exc:
            raise InvalidEmailError("Email is invalid") from exc

        value = result.normalized.lower()
        if len(value) > MAX_EMAIL_LENGTH:
            raise InvalidEmailError("Email is invalid")
        return cls(value=value)

    def __str__(self) -> str:
        return self.value
