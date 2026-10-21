from __future__ import annotations

import unicodedata
from datetime import UTC, datetime

from tricolink.modules.links.application.errors import (
    InvalidExpiresAt,
    InvalidTitle,
    UrlNotAllowed,
)
from tricolink.modules.links.domain.errors import InvalidUrlError
from tricolink.modules.links.domain.url_policy import UrlPolicy
from tricolink.modules.links.domain.value_objects import OriginalUrl


def normalize_title(value: str | None) -> str | None:
    if value is None:
        return None
    if len(value) > 120:
        raise InvalidTitle("Title must not exceed 120 characters")
    if any(unicodedata.category(char)[0] == "C" for char in value):
        raise InvalidTitle("Title must not contain control characters")
    stripped = value.strip()
    return stripped or None


def normalize_expires_at(value: datetime | None, now: datetime) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    normalized = value.astimezone(UTC)
    if normalized <= now:
        raise InvalidExpiresAt()
    return normalized


async def validate_url(policy: UrlPolicy, raw_url: str) -> OriginalUrl:
    try:
        return await policy.validate(raw_url)
    except InvalidUrlError as exc:
        raise UrlNotAllowed() from exc
