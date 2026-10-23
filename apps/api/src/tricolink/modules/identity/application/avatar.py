from __future__ import annotations

from uuid import UUID

from tricolink.modules.identity.application.errors import (
    AvatarNotFound,
    InvalidProfile,
    SessionExpired,
)
from tricolink.modules.identity.application.ports import Clock, UserRepository
from tricolink.modules.identity.domain.entities import AvatarImage, User

ALLOWED_AVATAR_TYPES = frozenset({"image/jpeg", "image/png", "image/webp"})
MAX_AVATAR_BYTES = 8_192


class SetAvatar:
    def __init__(self, *, users: UserRepository, clock: Clock) -> None:
        self._users = users
        self._clock = clock

    async def execute(self, user_id: UUID, *, content_type: str, content: bytes) -> User:
        validate_avatar_image(content_type, content)
        updated = await self._users.set_avatar(
            user_id,
            content_type=content_type,
            content=content,
            updated_at=self._clock.now(),
        )
        if updated is None:
            raise SessionExpired()
        return updated


class RemoveAvatar:
    def __init__(self, *, users: UserRepository) -> None:
        self._users = users

    async def execute(self, user_id: UUID) -> User:
        updated = await self._users.delete_avatar(user_id)
        if updated is None:
            raise SessionExpired()
        return updated


class GetAvatar:
    def __init__(self, *, users: UserRepository) -> None:
        self._users = users

    async def execute(self, user_id: UUID) -> AvatarImage:
        image = await self._users.get_avatar(user_id)
        if image is None:
            raise AvatarNotFound()
        return image


def validate_avatar_image(content_type: str, content: bytes) -> None:
    if content_type not in ALLOWED_AVATAR_TYPES:
        raise InvalidProfile("Unsupported avatar image type")
    if not content or len(content) > MAX_AVATAR_BYTES:
        raise InvalidProfile("Avatar image must be at most 8 KB")
    if not _matches_signature(content_type, content):
        raise InvalidProfile("Avatar image is invalid")


def _matches_signature(content_type: str, content: bytes) -> bool:
    if content_type == "image/jpeg":
        return content.startswith(b"\xff\xd8\xff")
    if content_type == "image/png":
        return content.startswith(b"\x89PNG\r\n\x1a\n")
    if content_type == "image/webp":
        return len(content) >= 12 and content[:4] == b"RIFF" and content[8:12] == b"WEBP"
    return False
