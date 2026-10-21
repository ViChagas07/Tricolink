from __future__ import annotations

from tricolink.modules.identity.application.ports import AccessTokenIssuer, UserRepository
from tricolink.modules.identity.domain.entities import User


class AuthenticateAccess:
    def __init__(
        self,
        *,
        access_tokens: AccessTokenIssuer,
        users: UserRepository,
    ) -> None:
        self._access_tokens = access_tokens
        self._users = users

    async def execute(self, token: str | None) -> User | None:
        if not token:
            return None
        claims = self._access_tokens.decode(token)
        if claims is None:
            return None
        user = await self._users.get_by_id(claims.user_id)
        if user is None or not user.is_active:
            return None
        return user
