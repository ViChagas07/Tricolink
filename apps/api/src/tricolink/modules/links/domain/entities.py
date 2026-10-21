from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID

from tricolink.modules.links.domain.value_objects import OriginalUrl, ShortCode


class LinkState(StrEnum):
    ACTIVE = "active"
    EXPIRED = "expired"
    INACTIVE = "inactive"


@dataclass(frozen=True, slots=True)
class Link:
    id: int | None
    code: ShortCode
    original_url: OriginalUrl
    title: str | None
    user_id: UUID | None
    is_custom_alias: bool
    is_active: bool
    expires_at: datetime | None
    click_count: int
    created_at: datetime
    updated_at: datetime

    def state(self, now: datetime) -> LinkState:
        if not self.is_active:
            return LinkState.INACTIVE
        if self.expires_at is not None and _as_utc(self.expires_at) <= _as_utc(now):
            return LinkState.EXPIRED
        return LinkState.ACTIVE

    def with_updates(
        self,
        *,
        title: str | None,
        original_url: OriginalUrl,
        is_active: bool,
        expires_at: datetime | None,
        updated_at: datetime,
    ) -> Link:
        return replace(
            self,
            title=title,
            original_url=original_url,
            is_active=is_active,
            expires_at=expires_at,
            updated_at=updated_at,
        )


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)
