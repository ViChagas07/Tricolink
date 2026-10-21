from __future__ import annotations

from uuid import uuid4

from tricolink.modules.identity.application.dto import AuthSession
from tricolink.modules.identity.application.errors import InvalidGoogleLogin
from tricolink.modules.identity.application.ports import Clock, UserRepository
from tricolink.modules.identity.application.session import SessionIssuer
from tricolink.modules.identity.domain.entities import User
from tricolink.modules.identity.domain.errors import DuplicateUserError
from tricolink.modules.identity.domain.google import GoogleIdentity


class LoginWithGoogle:
    def __init__(
        self,
        *,
        users: UserRepository,
        session_issuer: SessionIssuer,
        clock: Clock,
    ) -> None:
        self._users = users
        self._session_issuer = session_issuer
        self._clock = clock

    async def execute(self, identity: GoogleIdentity) -> AuthSession:
        if not identity.email_verified:
            raise InvalidGoogleLogin()

        user = await self._users.get_by_google_sub(identity.sub)
        if user is None:
            user = await self._find_or_link_or_create(identity)

        if user is None or not user.is_active:
            raise InvalidGoogleLogin()
        return await self._session_issuer.issue(user)

    async def _find_or_link_or_create(self, identity: GoogleIdentity) -> User | None:
        existing = await self._users.get_by_email(identity.email)
        if existing is not None:
            if existing.google_sub and existing.google_sub != identity.sub:
                raise InvalidGoogleLogin()
            try:
                return await self._users.link_google(
                    existing.id,
                    google_sub=identity.sub,
                    display_name=identity.display_name,
                )
            except DuplicateUserError:
                return await self._users.get_by_google_sub(identity.sub)

        new_user = User(
            id=uuid4(),
            email=identity.email,
            password_hash=None,
            google_sub=identity.sub,
            display_name=identity.display_name,
            locale=None,
            is_active=True,
            created_at=self._clock.now(),
        )
        try:
            return await self._users.create(new_user)
        except DuplicateUserError:
            return await self._users.get_by_google_sub(identity.sub)
