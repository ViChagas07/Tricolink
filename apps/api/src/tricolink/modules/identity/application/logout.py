from __future__ import annotations

from tricolink.modules.identity.application.ports import Clock, SessionRepository
from tricolink.modules.identity.application.tokens import hash_refresh_token


class Logout:
    def __init__(self, *, sessions: SessionRepository, clock: Clock) -> None:
        self._sessions = sessions
        self._clock = clock

    async def execute(self, refresh_token: str | None) -> None:
        if not refresh_token:
            return
        await self._sessions.revoke_family_by_hash(
            hash_refresh_token(refresh_token),
            self._clock.now(),
        )
