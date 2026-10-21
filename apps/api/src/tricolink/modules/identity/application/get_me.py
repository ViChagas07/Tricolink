from __future__ import annotations

from uuid import UUID

from tricolink.modules.identity.application.errors import SessionExpired
from tricolink.modules.identity.application.ports import UserRepository
from tricolink.modules.identity.domain.entities import User


class GetMe:
    def __init__(self, *, users: UserRepository) -> None:
        self._users = users

    async def execute(self, user_id: UUID) -> User:
        user = await self._users.get_by_id(user_id)
        if user is None or not user.is_active:
            raise SessionExpired()
        return user
