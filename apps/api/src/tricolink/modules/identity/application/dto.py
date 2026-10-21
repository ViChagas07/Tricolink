from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from tricolink.modules.identity.domain.entities import User


@dataclass(frozen=True, slots=True)
class AuthSession:
    user: User
    access_token: str
    access_expires_at: datetime
    refresh_token: str
    refresh_expires_at: datetime


@dataclass(frozen=True, slots=True)
class RegisterCommand:
    email: str
    password: str
    client_ip: str


@dataclass(frozen=True, slots=True)
class LoginCommand:
    email: str
    password: str
    client_ip: str


@dataclass(frozen=True, slots=True)
class UpdateMeCommand:
    user_id: UUID
    display_name: str | None = None
    locale: str | None = None
    set_display_name: bool = False
    set_locale: bool = False
