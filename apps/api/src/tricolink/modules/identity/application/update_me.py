from __future__ import annotations

import unicodedata

from tricolink.modules.identity.application.dto import UpdateMeCommand
from tricolink.modules.identity.application.errors import InvalidProfile, SessionExpired
from tricolink.modules.identity.application.ports import UserRepository
from tricolink.modules.identity.domain.entities import User

ALLOWED_LOCALES = frozenset(
    {"pt-BR", "en", "es", "fr", "de", "it", "ja", "ko", "zh-CN", "ru", "ar"}
)


class UpdateMe:
    def __init__(self, *, users: UserRepository) -> None:
        self._users = users

    async def execute(self, command: UpdateMeCommand) -> User:
        current = await self._users.get_by_id(command.user_id)
        if current is None or not current.is_active:
            raise SessionExpired()

        display_name = current.display_name
        if command.set_display_name:
            display_name = _normalize_display_name(command.display_name)

        locale = current.locale
        if command.set_locale:
            locale = _normalize_locale(command.locale)

        updated = await self._users.update_profile(
            command.user_id,
            display_name=display_name,
            locale=locale,
        )
        if updated is None:
            raise SessionExpired()
        return updated


def _normalize_display_name(value: str | None) -> str | None:
    if value is None:
        return None
    candidate = value.strip()
    if not candidate:
        return None
    if len(candidate) > 80:
        raise InvalidProfile("Display name must not exceed 80 characters")
    if any(unicodedata.category(char)[0] == "C" for char in candidate):
        raise InvalidProfile("Display name contains invalid characters")
    return candidate


def _normalize_locale(value: str | None) -> str | None:
    if value is None:
        return None
    candidate = value.strip()
    if candidate not in ALLOWED_LOCALES:
        raise InvalidProfile("Unsupported locale")
    return candidate
