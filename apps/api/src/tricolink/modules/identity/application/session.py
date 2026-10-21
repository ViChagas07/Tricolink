from __future__ import annotations

from datetime import timedelta

from tricolink.modules.identity.application.dto import AuthSession
from tricolink.modules.identity.application.ports import (
    AccessTokenIssuer,
    Clock,
    SessionRepository,
)
from tricolink.modules.identity.application.tokens import (
    generate_refresh_token,
    hash_refresh_token,
)
from tricolink.modules.identity.domain.entities import TokenFamily, User


class SessionIssuer:
    def __init__(
        self,
        *,
        access_tokens: AccessTokenIssuer,
        sessions: SessionRepository,
        clock: Clock,
        refresh_ttl_days: int,
    ) -> None:
        self._access_tokens = access_tokens
        self._sessions = sessions
        self._clock = clock
        self._refresh_ttl_days = refresh_ttl_days

    async def issue(self, user: User) -> AuthSession:
        now = self._clock.now()
        access = self._access_tokens.issue(user.id, now)
        refresh_token = generate_refresh_token()
        refresh_expires_at = now + timedelta(days=self._refresh_ttl_days)
        family = TokenFamily.create(user.id)
        await self._sessions.create_session(
            user_id=user.id,
            family_id=family.id,
            token_hash=hash_refresh_token(refresh_token),
            expires_at=refresh_expires_at,
            created_at=now,
        )
        return AuthSession(
            user=user,
            access_token=access.token,
            access_expires_at=access.expires_at,
            refresh_token=refresh_token,
            refresh_expires_at=refresh_expires_at,
        )
