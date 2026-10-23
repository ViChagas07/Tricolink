from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest

from tricolink.modules.identity.application import (
    AuthenticateAccess,
    AuthLocked,
    AvatarNotFound,
    GetAvatar,
    GetMe,
    InvalidCredentials,
    InvalidEmail,
    InvalidGoogleLogin,
    InvalidProfile,
    Login,
    LoginCommand,
    LoginWithGoogle,
    Logout,
    RefreshSession,
    Register,
    RegisterCommand,
    RemoveAvatar,
    RotationResult,
    RotationStatus,
    SessionExpired,
    SessionIssuer,
    SetAvatar,
    UpdateMe,
    UpdateMeCommand,
    WeakPassword,
    hash_refresh_token,
    validate_avatar_image,
)
from tricolink.modules.identity.application.ports import IssuedAccessToken, ThrottleResult
from tricolink.modules.identity.domain import (
    AvatarImage,
    Email,
    GoogleIdentity,
    PasswordPolicy,
    User,
)

NOW = datetime(2026, 10, 21, 12, 0, tzinfo=UTC)


class FakeClock:
    def __init__(self, now: datetime = NOW) -> None:
        self.value = now

    def now(self) -> datetime:
        return self.value


class FakeUserRepository:
    def __init__(self) -> None:
        self.users: dict[UUID, User] = {}
        self.avatars: dict[UUID, AvatarImage] = {}
        self.duplicate = False
        self.create_calls = 0
        self.link_calls = 0

    async def get_by_id(self, user_id: UUID) -> User | None:
        return self.users.get(user_id)

    async def get_by_email(self, email: Email) -> User | None:
        return next((u for u in self.users.values() if u.email.value == email.value), None)

    async def get_by_google_sub(self, google_sub: str) -> User | None:
        return next((u for u in self.users.values() if u.google_sub == google_sub), None)

    async def create(self, user: User) -> User:
        from tricolink.modules.identity.domain.errors import DuplicateUserError

        self.create_calls += 1
        if self.duplicate:
            raise DuplicateUserError()
        self.users[user.id] = user
        return user

    async def link_google(
        self,
        user_id: UUID,
        *,
        google_sub: str,
        display_name: str | None,
    ) -> User | None:
        from tricolink.modules.identity.domain.errors import DuplicateUserError

        self.link_calls += 1
        if self.duplicate:
            raise DuplicateUserError()
        user = self.users.get(user_id)
        if user is None:
            return None
        linked = user.link_google(google_sub, display_name)
        self.users[user_id] = linked
        return linked

    async def update_profile(
        self,
        user_id: UUID,
        *,
        display_name: str | None,
        locale: str | None,
    ) -> User | None:
        user = self.users.get(user_id)
        if user is None:
            return None
        updated = user.with_profile(display_name=display_name, locale=locale)
        self.users[user_id] = updated
        return updated

    async def update_google_avatar(
        self,
        user_id: UUID,
        *,
        google_avatar_url: str,
    ) -> User | None:
        user = self.users.get(user_id)
        if user is None:
            return None
        updated = replace(user, google_avatar_url=google_avatar_url)
        self.users[user_id] = updated
        return updated

    async def set_avatar(
        self,
        user_id: UUID,
        *,
        content_type: str,
        content: bytes,
        updated_at: datetime,
    ) -> User | None:
        user = self.users.get(user_id)
        if user is None:
            return None
        self.avatars[user_id] = AvatarImage(content_type=content_type, content=content)
        updated = replace(user, avatar_updated_at=updated_at)
        self.users[user_id] = updated
        return updated

    async def delete_avatar(self, user_id: UUID) -> User | None:
        user = self.users.get(user_id)
        if user is None:
            return None
        self.avatars.pop(user_id, None)
        updated = replace(user, avatar_updated_at=None)
        self.users[user_id] = updated
        return updated

    async def get_avatar(self, user_id: UUID) -> AvatarImage | None:
        return self.avatars.get(user_id)


class FakeSessionRepository:
    def __init__(self) -> None:
        self.records: dict[str, dict[str, object]] = {}
        self.next_id = 1

    async def create_session(
        self,
        *,
        user_id: UUID,
        family_id: UUID,
        token_hash: str,
        expires_at: datetime,
        created_at: datetime,
    ) -> None:
        self.records[token_hash] = {
            "user_id": user_id,
            "family_id": family_id,
            "expires_at": expires_at,
            "revoked": False,
        }

    async def rotate(
        self,
        *,
        token_hash: str,
        new_token_hash: str,
        new_expires_at: datetime,
        now: datetime,
    ) -> RotationResult:
        record = self.records.get(token_hash)
        if record is None:
            return RotationResult(status=RotationStatus.INVALID)

        if record["revoked"]:
            self._revoke_family(record["family_id"], now)
            return RotationResult(
                status=RotationStatus.REUSED,
                user_id=record["user_id"],  # type: ignore[arg-type]
                family_id=record["family_id"],  # type: ignore[arg-type]
            )
        if record["expires_at"] <= now:  # type: ignore[operator]
            self._revoke_family(record["family_id"], now)
            return RotationResult(
                status=RotationStatus.EXPIRED,
                user_id=record["user_id"],  # type: ignore[arg-type]
                family_id=record["family_id"],  # type: ignore[arg-type]
            )

        record["revoked"] = True
        self.records[new_token_hash] = {
            "user_id": record["user_id"],
            "family_id": record["family_id"],
            "expires_at": new_expires_at,
            "revoked": False,
        }
        return RotationResult(
            status=RotationStatus.ROTATED,
            user_id=record["user_id"],  # type: ignore[arg-type]
            family_id=record["family_id"],  # type: ignore[arg-type]
        )

    async def revoke_family_by_hash(self, token_hash: str, now: datetime) -> bool:
        record = self.records.get(token_hash)
        if record is None:
            return False
        self._revoke_family(record["family_id"], now)
        return True

    def _revoke_family(self, family_id: object, now: datetime) -> None:
        for record in self.records.values():
            if record["family_id"] == family_id:
                record["revoked"] = True


class FakeHasher:
    def __init__(self, *, valid: bool = True) -> None:
        self.valid = valid
        self.hash_calls: list[str] = []
        self.verify_calls = 0
        self.dummy_calls = 0

    async def hash(self, password: str) -> str:
        self.hash_calls.append(password)
        return f"hash:{password}"

    async def verify(self, password: str, password_hash: str) -> bool:
        self.verify_calls += 1
        return self.valid and password_hash == f"hash:{password}"

    async def verify_dummy(self, password: str) -> None:
        self.dummy_calls += 1


class FakeAccessTokens:
    def issue(self, user_id: UUID, now: datetime) -> IssuedAccessToken:
        return IssuedAccessToken(
            token=f"access:{user_id}",
            expires_at=now + timedelta(minutes=15),
        )

    def decode(self, token: str) -> object:
        from tricolink.modules.identity.application.ports import AccessClaims

        if not token.startswith("access:"):
            return None
        return AccessClaims(
            user_id=UUID(token.removeprefix("access:")),
            jti="jti",
            issued_at=NOW,
            expires_at=NOW + timedelta(minutes=15),
        )


class FakeThrottle:
    def __init__(self, allowed: bool = True) -> None:
        self.allowed = allowed
        self.checks: list[tuple[str, str]] = []
        self.failures: list[tuple[str, str]] = []
        self.successes: list[str] = []

    async def check(self, *, ip: str, email: str) -> ThrottleResult:
        self.checks.append((ip, email))
        return ThrottleResult(allowed=self.allowed, retry_after_seconds=30)

    async def record_failure(self, *, ip: str, email: str) -> None:
        self.failures.append((ip, email))

    async def record_success(self, *, email: str) -> None:
        self.successes.append(email)


def user(
    *,
    email: str = "user@example.com",
    password: str | None = "hashed",
    google_sub: str | None = None,
    is_active: bool = True,
    display_name: str | None = None,
    locale: str | None = None,
) -> User:
    return User(
        id=uuid4(),
        email=Email.parse(email),
        password_hash=f"hash:{password}" if password else None,
        google_sub=google_sub,
        display_name=display_name,
        locale=locale,
        is_active=is_active,
        created_at=NOW,
    )


def build_issuer(
    users: FakeUserRepository,
    sessions: FakeSessionRepository,
    tokens: FakeAccessTokens,
    clock: FakeClock,
) -> SessionIssuer:
    return SessionIssuer(
        access_tokens=tokens,
        sessions=sessions,
        clock=clock,
        refresh_ttl_days=30,
    )


def build_register(
    users: FakeUserRepository,
    hasher: FakeHasher,
    throttle: FakeThrottle | None = None,
    clock: FakeClock | None = None,
) -> Register:
    return Register(
        users=users,
        password_policy=PasswordPolicy(),
        hasher=hasher,
        throttle=throttle or FakeThrottle(),
        clock=clock or FakeClock(),
    )


@pytest.mark.asyncio
async def test_register_creates_user_with_argon_hash_and_no_session() -> None:
    users = FakeUserRepository()
    hasher = FakeHasher()
    register = build_register(users, hasher)

    result = await register.execute(
        RegisterCommand(
            email="User@Example.com",
            password="correct horse battery staple",
            client_ip="203.0.113.9",
        )
    )

    assert result is None
    assert len(users.users) == 1
    stored = next(iter(users.users.values()))
    assert stored.email.value == "user@example.com"
    assert stored.password_hash == "hash:correct horse battery staple"
    assert hasher.hash_calls


@pytest.mark.asyncio
async def test_register_duplicate_hashes_but_returns_same_success() -> None:
    users = FakeUserRepository()
    users.duplicate = True
    hasher = FakeHasher()
    register = build_register(users, hasher)

    result = await register.execute(
        RegisterCommand(
            email="user@example.com",
            password="correct horse battery staple",
            client_ip="203.0.113.9",
        )
    )

    assert result is None
    assert users.create_calls == 1
    assert len(hasher.hash_calls) == 1


@pytest.mark.asyncio
async def test_register_rejects_weak_password_and_throttle() -> None:
    users = FakeUserRepository()
    hasher = FakeHasher()
    register = build_register(users, hasher)

    with pytest.raises(WeakPassword):
        await register.execute(
            RegisterCommand(
                email="user@example.com",
                password="password123",
                client_ip="203.0.113.9",
            )
        )
    assert hasher.hash_calls == []

    locked = build_register(users, hasher, throttle=FakeThrottle(allowed=False))
    with pytest.raises(AuthLocked):
        await locked.execute(
            RegisterCommand(
                email="user@example.com",
                password="correct horse battery staple",
                client_ip="203.0.113.9",
            )
        )


@pytest.mark.asyncio
async def test_register_rejects_invalid_email() -> None:
    with pytest.raises(InvalidEmail):
        await build_register(FakeUserRepository(), FakeHasher()).execute(
            RegisterCommand(
                email="not-an-email",
                password="correct horse battery staple",
                client_ip="203.0.113.9",
            )
        )


def build_login(
    users: FakeUserRepository,
    sessions: FakeSessionRepository,
    hasher: FakeHasher,
    throttle: FakeThrottle | None = None,
    clock: FakeClock | None = None,
) -> Login:
    tokens = FakeAccessTokens()
    issuer = build_issuer(users, sessions, tokens, clock or FakeClock())
    return Login(
        users=users,
        hasher=hasher,
        throttle=throttle or FakeThrottle(),
        session_issuer=issuer,
    )


@pytest.mark.asyncio
async def test_login_issues_tokens_and_stores_only_refresh_hash() -> None:
    users = FakeUserRepository()
    account = user(password="correct horse battery staple")
    users.users[account.id] = account
    sessions = FakeSessionRepository()
    hasher = FakeHasher()
    throttle = FakeThrottle()
    login = build_login(users, sessions, hasher, throttle)

    session = await login.execute(
        LoginCommand(
            email="user@example.com",
            password="correct horse battery staple",
            client_ip="203.0.113.9",
        )
    )

    assert session.user.id == account.id
    assert session.access_token.startswith("access:")
    assert session.refresh_token not in sessions.records
    assert hash_refresh_token(session.refresh_token) in sessions.records
    assert throttle.successes == ["user@example.com"]


@pytest.mark.asyncio
async def test_login_unknown_and_wrong_password_use_dummy_and_generic_error() -> None:
    users = FakeUserRepository()
    sessions = FakeSessionRepository()
    hasher = FakeHasher()
    throttle = FakeThrottle()
    login = build_login(users, sessions, hasher, throttle)

    with pytest.raises(InvalidCredentials):
        await login.execute(
            LoginCommand(
                email="missing@example.com",
                password="correct horse battery staple",
                client_ip="203.0.113.9",
            )
        )
    assert hasher.dummy_calls == 1
    assert throttle.failures

    account = user(password="right password")
    users.users[account.id] = account
    with pytest.raises(InvalidCredentials):
        await login.execute(
            LoginCommand(
                email="user@example.com",
                password="wrong password",
                client_ip="203.0.113.9",
            )
        )
    assert sessions.records == {}

    with pytest.raises(InvalidCredentials):
        await login.execute(
            LoginCommand(
                email="not-an-email",
                password="correct horse battery staple",
                client_ip="203.0.113.9",
            )
        )
    assert hasher.dummy_calls == 2


@pytest.mark.asyncio
async def test_login_locked_and_inactive() -> None:
    users = FakeUserRepository()
    sessions = FakeSessionRepository()
    hasher = FakeHasher()

    locked = build_login(users, sessions, hasher, FakeThrottle(allowed=False))
    with pytest.raises(AuthLocked):
        await locked.execute(
            LoginCommand(
                email="user@example.com",
                password="correct horse battery staple",
                client_ip="203.0.113.9",
            )
        )
    assert hasher.verify_calls == 0

    inactive = user(is_active=False)
    users.users[inactive.id] = inactive
    with pytest.raises(InvalidCredentials):
        await build_login(users, sessions, hasher).execute(
            LoginCommand(
                email="user@example.com",
                password="hashed",
                client_ip="203.0.113.9",
            )
        )


@pytest.mark.asyncio
async def test_refresh_rotation_reuse_and_logout() -> None:
    users = FakeUserRepository()
    account = user()
    users.users[account.id] = account
    sessions = FakeSessionRepository()
    tokens = FakeAccessTokens()
    clock = FakeClock()
    build_issuer(users, sessions, tokens, clock)
    login = build_login(users, sessions, FakeHasher(), clock=clock)
    first = await login.execute(
        LoginCommand(
            email="user@example.com",
            password="hashed",
            client_ip="ip",
        )
    )
    refresh = RefreshSession(
        users=users,
        sessions=sessions,
        access_tokens=tokens,
        clock=clock,
        refresh_ttl_days=30,
    )

    second = await refresh.execute(first.refresh_token)
    assert second.refresh_token != first.refresh_token
    assert sessions.records[hash_refresh_token(first.refresh_token)]["revoked"] is True

    with pytest.raises(SessionExpired):
        await refresh.execute(first.refresh_token)

    family_id = sessions.records[hash_refresh_token(second.refresh_token)]["family_id"]
    assert all(
        record["revoked"] is True
        for record in sessions.records.values()
        if record["family_id"] == family_id
    )

    assert await Logout(sessions=sessions, clock=clock).execute("") is None


@pytest.mark.asyncio
async def test_refresh_expired_and_logout_revoke() -> None:
    users = FakeUserRepository()
    account = user()
    users.users[account.id] = account
    sessions = FakeSessionRepository()
    tokens = FakeAccessTokens()
    clock = FakeClock()
    issuer = build_issuer(users, sessions, tokens, clock)
    session = await issuer.issue(account)
    record = sessions.records[hash_refresh_token(session.refresh_token)]
    record["expires_at"] = NOW - timedelta(seconds=1)

    refresh = RefreshSession(
        users=users,
        sessions=sessions,
        access_tokens=tokens,
        clock=clock,
        refresh_ttl_days=30,
    )
    with pytest.raises(SessionExpired):
        await refresh.execute(None)
    with pytest.raises(SessionExpired):
        await refresh.execute(session.refresh_token)

    other = await issuer.issue(account)
    await Logout(sessions=sessions, clock=clock).execute(other.refresh_token)
    assert sessions.records[hash_refresh_token(other.refresh_token)]["revoked"] is True


@pytest.mark.asyncio
async def test_get_me_and_update_me() -> None:
    users = FakeUserRepository()
    account = user()
    users.users[account.id] = account
    getter = GetMe(users=users)
    updater = UpdateMe(users=users)

    assert (await getter.execute(account.id)).id == account.id
    updated = await updater.execute(
        UpdateMeCommand(
            user_id=account.id,
            display_name="  New Name  ",
            locale="pt-BR",
            set_display_name=True,
            set_locale=True,
        )
    )
    assert updated.display_name == "New Name"
    assert updated.locale == "pt-BR"

    with pytest.raises(InvalidProfile):
        await updater.execute(
            UpdateMeCommand(
                user_id=account.id,
                locale="xx",
                set_locale=True,
            )
        )
    cleared = await updater.execute(
        UpdateMeCommand(
            user_id=account.id,
            display_name=None,
            locale=None,
            set_display_name=True,
            set_locale=True,
        )
    )
    assert cleared.display_name is None
    assert cleared.locale is None

    with pytest.raises(InvalidProfile):
        await updater.execute(
            UpdateMeCommand(
                user_id=account.id,
                display_name="a" * 81,
                set_display_name=True,
            )
        )
    with pytest.raises(InvalidProfile):
        await updater.execute(
            UpdateMeCommand(
                user_id=account.id,
                display_name="bad\x00name",
                set_display_name=True,
            )
        )
    with pytest.raises(SessionExpired):
        await getter.execute(uuid4())


@pytest.mark.asyncio
async def test_google_login_creates_links_and_rejects_unverified() -> None:
    users = FakeUserRepository()
    sessions = FakeSessionRepository()
    tokens = FakeAccessTokens()
    clock = FakeClock()
    issuer = build_issuer(users, sessions, tokens, clock)
    google = LoginWithGoogle(users=users, session_issuer=issuer, clock=clock)
    identity = GoogleIdentity(
        sub="google-sub",
        email=Email.parse("google@example.com"),
        email_verified=True,
        display_name="Google User",
    )

    session = await google.execute(identity)
    assert session.user.google_sub == "google-sub"
    assert session.user.password_hash is None

    existing = user(email="existing@example.com", password=None)
    users.users[existing.id] = existing
    linked = await google.execute(replace(identity, sub="other-sub", email=existing.email))
    assert linked.user.google_sub == "other-sub"

    with pytest.raises(InvalidGoogleLogin):
        await google.execute(replace(identity, email_verified=False))

    blocked = user(email="blocked@example.com", google_sub="different")
    users.users[blocked.id] = blocked
    with pytest.raises(InvalidGoogleLogin):
        await google.execute(replace(identity, sub="another", email=blocked.email))

    password_account = user(email="password@example.com", password="secret")
    users.users[password_account.id] = password_account
    with pytest.raises(InvalidGoogleLogin):
        await google.execute(replace(identity, sub="pre-hijack", email=password_account.email))
    assert users.users[password_account.id].google_sub is None


@pytest.mark.asyncio
async def test_google_login_persists_picture_and_keeps_custom_avatar() -> None:
    users = FakeUserRepository()
    sessions = FakeSessionRepository()
    tokens = FakeAccessTokens()
    clock = FakeClock()
    issuer = build_issuer(users, sessions, tokens, clock)
    google = LoginWithGoogle(users=users, session_issuer=issuer, clock=clock)
    identity = GoogleIdentity(
        sub="google-sub",
        email=Email.parse("google-picture@example.com"),
        email_verified=True,
        display_name="Google User",
        picture_url="https://lh3.googleusercontent.com/a/photo=s96-c",
    )

    session = await google.execute(identity)
    assert session.user.google_avatar_url == identity.picture_url

    custom = await users.set_avatar(
        session.user.id,
        content_type="image/png",
        content=b"\x89PNG\r\n\x1a\ncustom",
        updated_at=NOW,
    )
    assert custom is not None and custom.has_custom_avatar

    refreshed = await google.execute(
        replace(identity, picture_url="https://lh3.googleusercontent.com/a/new=s96-c")
    )
    assert refreshed.user.has_custom_avatar
    assert refreshed.user.google_avatar_url == "https://lh3.googleusercontent.com/a/new=s96-c"


@pytest.mark.asyncio
async def test_avatar_set_get_remove_flow_and_validation() -> None:
    users = FakeUserRepository()
    account = user()
    users.users[account.id] = account
    clock = FakeClock()
    set_avatar = SetAvatar(users=users, clock=clock)
    get_avatar = GetAvatar(users=users)
    remove_avatar = RemoveAvatar(users=users)
    png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 8

    updated = await set_avatar.execute(account.id, content_type="image/png", content=png)
    assert updated.has_custom_avatar
    image = await get_avatar.execute(account.id)
    assert image == AvatarImage(content_type="image/png", content=png)

    removed = await remove_avatar.execute(account.id)
    assert not removed.has_custom_avatar
    with pytest.raises(AvatarNotFound):
        await get_avatar.execute(account.id)

    with pytest.raises(InvalidProfile):
        await set_avatar.execute(account.id, content_type="image/svg+xml", content=png)
    with pytest.raises(InvalidProfile):
        await set_avatar.execute(account.id, content_type="image/png", content=b"not-a-png")
    with pytest.raises(InvalidProfile):
        await set_avatar.execute(account.id, content_type="image/png", content=png + b"x" * 8_192)
    validate_avatar_image("image/jpeg", b"\xff\xd8\xff\xe0")
    validate_avatar_image("image/webp", b"RIFF\x00\x00\x00\x00WEBP")


@pytest.mark.asyncio
async def test_authenticate_access_returns_active_user_or_none() -> None:
    users = FakeUserRepository()
    account = user()
    users.users[account.id] = account
    authenticator = AuthenticateAccess(
        access_tokens=FakeAccessTokens(),
        users=users,
    )

    assert (await authenticator.execute(f"access:{account.id}")).id == account.id
    assert await authenticator.execute("bad") is None
    assert await authenticator.execute(None) is None

    inactive = user(is_active=False)
    users.users[inactive.id] = inactive
    assert await authenticator.execute(f"access:{inactive.id}") is None
