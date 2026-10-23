from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol
from uuid import UUID

from tricolink.modules.identity.domain.email import Email
from tricolink.modules.identity.domain.entities import AvatarImage, User


@dataclass(frozen=True, slots=True)
class IssuedAccessToken:
    token: str
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class AccessClaims:
    user_id: UUID
    jti: str
    issued_at: datetime
    expires_at: datetime


class RotationStatus(StrEnum):
    ROTATED = "rotated"
    REUSED = "reused"
    EXPIRED = "expired"
    INVALID = "invalid"


@dataclass(frozen=True, slots=True)
class RotationResult:
    status: RotationStatus
    user_id: UUID | None = None
    family_id: UUID | None = None


@dataclass(frozen=True, slots=True)
class ThrottleResult:
    allowed: bool
    retry_after_seconds: int


class Clock(Protocol):
    def now(self) -> datetime: ...


class PasswordHasher(Protocol):
    async def hash(self, password: str) -> str: ...

    async def verify(self, password: str, password_hash: str) -> bool: ...

    async def verify_dummy(self, password: str) -> None: ...


class AccessTokenIssuer(Protocol):
    def issue(self, user_id: UUID, now: datetime) -> IssuedAccessToken: ...

    def decode(self, token: str) -> AccessClaims | None: ...


class UserRepository(Protocol):
    async def get_by_id(self, user_id: UUID) -> User | None: ...

    async def get_by_email(self, email: Email) -> User | None: ...

    async def get_by_google_sub(self, google_sub: str) -> User | None: ...

    async def create(self, user: User) -> User: ...

    async def link_google(
        self,
        user_id: UUID,
        *,
        google_sub: str,
        display_name: str | None,
    ) -> User | None: ...

    async def update_profile(
        self,
        user_id: UUID,
        *,
        display_name: str | None,
        locale: str | None,
    ) -> User | None: ...

    async def update_google_avatar(
        self,
        user_id: UUID,
        *,
        google_avatar_url: str,
    ) -> User | None: ...

    async def set_avatar(
        self,
        user_id: UUID,
        *,
        content_type: str,
        content: bytes,
        updated_at: datetime,
    ) -> User | None: ...

    async def delete_avatar(self, user_id: UUID) -> User | None: ...

    async def get_avatar(self, user_id: UUID) -> AvatarImage | None: ...


class SessionRepository(Protocol):
    async def create_session(
        self,
        *,
        user_id: UUID,
        family_id: UUID,
        token_hash: str,
        expires_at: datetime,
        created_at: datetime,
    ) -> None: ...

    async def rotate(
        self,
        *,
        token_hash: str,
        new_token_hash: str,
        new_expires_at: datetime,
        now: datetime,
    ) -> RotationResult: ...

    async def revoke_family_by_hash(self, token_hash: str, now: datetime) -> bool: ...


class AuthThrottle(Protocol):
    async def check(self, *, ip: str, email: str) -> ThrottleResult: ...

    async def record_failure(self, *, ip: str, email: str) -> None: ...

    async def record_success(self, *, email: str) -> None: ...
