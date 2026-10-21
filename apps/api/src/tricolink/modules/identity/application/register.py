from __future__ import annotations

import unicodedata
from uuid import uuid4

from tricolink.modules.identity.application.dto import RegisterCommand
from tricolink.modules.identity.application.errors import (
    AuthLocked,
    InvalidEmail,
    WeakPassword,
)
from tricolink.modules.identity.application.ports import (
    AuthThrottle,
    Clock,
    PasswordHasher,
    UserRepository,
)
from tricolink.modules.identity.domain.email import Email
from tricolink.modules.identity.domain.entities import User
from tricolink.modules.identity.domain.errors import (
    DuplicateUserError,
    InvalidEmailError,
    WeakPasswordError,
)
from tricolink.modules.identity.domain.password import PasswordPolicy


class Register:
    """Creates a password user with a deliberately generic response."""

    def __init__(
        self,
        *,
        users: UserRepository,
        password_policy: PasswordPolicy,
        hasher: PasswordHasher,
        throttle: AuthThrottle,
        clock: Clock,
    ) -> None:
        self._users = users
        self._password_policy = password_policy
        self._hasher = hasher
        self._throttle = throttle
        self._clock = clock

    async def execute(self, command: RegisterCommand) -> None:
        throttle_key = unicodedata.normalize("NFKC", command.email).strip().lower() or "invalid"
        throttle = await self._throttle.check(
            ip=command.client_ip,
            email=throttle_key,
        )
        if not throttle.allowed:
            raise AuthLocked(throttle.retry_after_seconds)

        try:
            email = Email.parse(command.email)
        except InvalidEmailError as exc:
            raise InvalidEmail() from exc

        try:
            self._password_policy.validate(command.password, email=email)
        except WeakPasswordError as exc:
            raise WeakPassword(str(exc)) from exc

        password_hash = await self._hasher.hash(command.password)
        user = User(
            id=uuid4(),
            email=email,
            password_hash=password_hash,
            google_sub=None,
            display_name=None,
            locale=None,
            is_active=True,
            created_at=self._clock.now(),
        )
        try:
            await self._users.create(user)
        except DuplicateUserError:
            # Same response and same hashing work as a new email.
            return None
        return None
