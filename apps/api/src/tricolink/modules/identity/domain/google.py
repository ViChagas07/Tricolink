from __future__ import annotations

import secrets
import unicodedata
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime

from tricolink.modules.identity.domain.email import Email
from tricolink.modules.identity.domain.errors import (
    InvalidEmailError,
    InvalidGoogleIdentityError,
)

GOOGLE_ISSUERS = frozenset({"https://accounts.google.com", "accounts.google.com"})
_CLOCK_LEEWAY_SECONDS = 60


@dataclass(frozen=True, slots=True)
class GoogleIdentity:
    sub: str
    email: Email
    email_verified: bool
    display_name: str | None


def validate_google_claims(
    claims: Mapping[str, object],
    *,
    expected_nonce: str,
    client_id: str,
    now: datetime,
) -> GoogleIdentity:
    issuer = _string(claims.get("iss"))
    if issuer not in GOOGLE_ISSUERS:
        raise InvalidGoogleIdentityError("Invalid issuer")

    audience = claims.get("aud")
    audiences = [audience] if isinstance(audience, str) else audience
    if not isinstance(audiences, list) or client_id not in audiences:
        raise InvalidGoogleIdentityError("Invalid audience")

    exp = _number(claims.get("exp"))
    if exp is None or exp <= now.astimezone(UTC).timestamp() - _CLOCK_LEEWAY_SECONDS:
        raise InvalidGoogleIdentityError("Expired token")

    nonce = _string(claims.get("nonce"))
    if not nonce or not expected_nonce or not secrets.compare_digest(nonce, expected_nonce):
        raise InvalidGoogleIdentityError("Invalid nonce")

    verified = claims.get("email_verified")
    email_verified = verified is True or (
        isinstance(verified, str) and verified.strip().lower() == "true"
    )
    if not email_verified:
        raise InvalidGoogleIdentityError("Email is not verified")

    raw_email = _string(claims.get("email"))
    if not raw_email:
        raise InvalidGoogleIdentityError("Missing email")
    try:
        email = Email.parse(raw_email)
    except InvalidEmailError as exc:
        raise InvalidGoogleIdentityError("Invalid email") from exc

    sub = _string(claims.get("sub"))
    if not sub or len(sub) > 255:
        raise InvalidGoogleIdentityError("Missing subject")

    display_name = _display_name(claims.get("name"))
    return GoogleIdentity(
        sub=sub,
        email=email,
        email_verified=True,
        display_name=display_name,
    )


def _string(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _number(value: object) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _display_name(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    candidate = value.strip()
    if not candidate:
        return None
    if len(candidate) > 80:
        raise InvalidGoogleIdentityError("Display name is too long")
    if any(unicodedata.category(char)[0] == "C" for char in candidate):
        raise InvalidGoogleIdentityError("Display name is invalid")
    return candidate
