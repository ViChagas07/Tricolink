from __future__ import annotations

from datetime import timedelta

from tricolink.modules.identity.application.dto import AuthSession
from tricolink.modules.identity.application.errors import SessionExpired
from tricolink.modules.identity.application.ports import (
    AccessTokenIssuer,
    Clock,
    RotationStatus,
    SessionRepository,
    UserRepository,
)
from tricolink.modules.identity.application.tokens import (
    generate_refresh_token,
    hash_refresh_token,
)


class RefreshSession:
    def __init__(
        self,
        *,
        users: UserRepository,
        sessions: SessionRepository,
        access_tokens: AccessTokenIssuer,
        clock: Clock,
        refresh_ttl_days: int,
    ) -> None:
        self._users = users
        self._sessions = sessions
        self._access_tokens = access_tokens
        self._clock = clock
        self._refresh_ttl_days = refresh_ttl_days

    async def execute(self, refresh_token: str | None) -> AuthSession:
        if not refresh_token:
            raise SessionExpired()

        now = self._clock.now()
        new_refresh = generate_refresh_token()
        new_expires_at = now + timedelta(days=self._refresh_ttl_days)
        result = await self._sessions.rotate(
            token_hash=hash_refresh_token(refresh_token),
            new_token_hash=hash_refresh_token(new_refresh),
            new_expires_at=new_expires_at,
            now=now,
        )
        if result.status is not RotationStatus.ROTATED or result.user_id is None:
            raise SessionExpired()

        user = await self._users.get_by_id(result.user_id)
        if user is None or not user.is_active:
            raise SessionExpired()

        access = self._access_tokens.issue(user.id, now)
        return AuthSession(
            user=user,
            access_token=access.token,
            access_expires_at=access.expires_at,
            refresh_token=new_refresh,
            refresh_expires_at=new_expires_at,
        )
