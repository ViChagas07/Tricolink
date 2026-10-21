from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from uuid import UUID, uuid4

from tricolink.modules.identity.domain.email import Email


@dataclass(frozen=True, slots=True)
class User:
    id: UUID
    email: Email
    password_hash: str | None
    google_sub: str | None
    display_name: str | None
    locale: str | None
    is_active: bool
    created_at: datetime

    @property
    def has_password(self) -> bool:
        return bool(self.password_hash)

    @property
    def is_google_linked(self) -> bool:
        return bool(self.google_sub)

    def link_google(self, google_sub: str, display_name: str | None) -> User:
        return replace(
            self,
            google_sub=google_sub,
            display_name=self.display_name or display_name,
        )

    def with_profile(
        self,
        *,
        display_name: str | None,
        locale: str | None,
    ) -> User:
        return replace(self, display_name=display_name, locale=locale)


@dataclass(frozen=True, slots=True)
class TokenFamily:
    id: UUID
    user_id: UUID

    @classmethod
    def create(cls, user_id: UUID) -> TokenFamily:
        return cls(id=uuid4(), user_id=user_id)


@dataclass(frozen=True, slots=True)
class RefreshTokenRecord:
    id: UUID
    user_id: UUID
    family_id: UUID
    token_hash: str
    expires_at: datetime
    revoked_at: datetime | None
    created_at: datetime

    @property
    def is_revoked(self) -> bool:
        return self.revoked_at is not None

    def is_expired(self, now: datetime) -> bool:
        return _as_utc(self.expires_at) <= _as_utc(now)

    def revoke(self, now: datetime) -> RefreshTokenRecord:
        return replace(self, revoked_at=now)


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)
