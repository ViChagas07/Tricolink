from __future__ import annotations

import unicodedata

from tricolink.modules.identity.application.dto import AuthSession, LoginCommand
from tricolink.modules.identity.application.errors import AuthLocked, InvalidCredentials
from tricolink.modules.identity.application.ports import (
    AuthThrottle,
    PasswordHasher,
    UserRepository,
)
from tricolink.modules.identity.application.session import SessionIssuer
from tricolink.modules.identity.domain.email import Email
from tricolink.modules.identity.domain.errors import InvalidEmailError


class Login:
    def __init__(
        self,
        *,
        users: UserRepository,
        hasher: PasswordHasher,
        throttle: AuthThrottle,
        session_issuer: SessionIssuer,
    ) -> None:
        self._users = users
        self._hasher = hasher
        self._throttle = throttle
        self._session_issuer = session_issuer

    async def execute(self, command: LoginCommand) -> AuthSession:
        throttle_key = unicodedata.normalize("NFKC", command.email).strip().lower() or "invalid"
        throttle = await self._throttle.check(
            ip=command.client_ip,
            email=throttle_key,
        )
        if not throttle.allowed:
            raise AuthLocked(throttle.retry_after_seconds)

        try:
            email = Email.parse(command.email)
        except InvalidEmailError:
            await self._fail(command.client_ip, throttle_key, command.password)
            raise InvalidCredentials() from None

        user = await self._users.get_by_email(email)
        if user is None or user.password_hash is None:
            await self._hasher.verify_dummy(command.password)
            await self._record_failure(command.client_ip, email.value)
            raise InvalidCredentials()

        valid = await self._hasher.verify(command.password, user.password_hash)
        if not valid or not user.is_active:
            await self._record_failure(command.client_ip, email.value)
            raise InvalidCredentials()

        await self._throttle.record_success(email=email.value)
        return await self._session_issuer.issue(user)

    async def _fail(self, ip: str, email: str, password: str) -> None:
        await self._hasher.verify_dummy(password)
        await self._record_failure(ip, email)

    async def _record_failure(self, ip: str, email: str) -> None:
        await self._throttle.record_failure(ip=ip, email=email)
