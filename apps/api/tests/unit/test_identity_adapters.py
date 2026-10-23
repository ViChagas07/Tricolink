from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
import pytest
from fastapi import Response

from tricolink.core.config import Settings
from tricolink.infra.resilience import Bulkhead
from tricolink.modules.identity.adapters.google import GoogleOIDCClient
from tricolink.modules.identity.adapters.password import Argon2PasswordHasher
from tricolink.modules.identity.adapters.tokens import PyJwtAccessTokens
from tricolink.modules.identity.application import AuthSession, InvalidNextPath
from tricolink.modules.identity.domain import Email, User
from tricolink.modules.identity.presentation.cookies import (
    clear_session_cookies,
    set_session_cookies,
)
from tricolink.modules.identity.presentation.security import safe_next_path

NOW = datetime(2026, 10, 21, 12, 0, tzinfo=UTC)


def fast_hasher() -> Argon2PasswordHasher:
    return Argon2PasswordHasher(
        bulkhead=Bulkhead("hashing", limit=2),
        time_cost=1,
        memory_kib=1_024,
        parallelism=1,
        hash_len=16,
        salt_len=8,
    )


@pytest.mark.asyncio
async def test_argon2_hasher_roundtrip_and_dummy() -> None:
    hasher = fast_hasher()
    digest = await hasher.hash("correct horse battery staple")

    assert digest.startswith("$argon2id$")
    assert await hasher.verify("correct horse battery staple", digest) is True
    assert await hasher.verify("wrong password", digest) is False
    assert await hasher.verify("", digest) is False
    await hasher.verify_dummy("anything")
    await hasher.verify_dummy("anything")


def test_access_jwt_contains_minimal_claims_and_validates() -> None:
    settings = Settings(jwt_secret="s" * 48, jwt_algorithm="HS256")
    tokens = PyJwtAccessTokens(settings)
    user_id = uuid4()

    issued = tokens.issue(user_id, datetime.now(UTC))
    claims = tokens.decode(issued.token)

    assert claims is not None
    assert claims.user_id == user_id
    payload = jwt.decode(issued.token, settings.jwt_secret, algorithms=["HS256"])
    assert set(payload) == {"sub", "jti", "iat", "exp"}
    assert payload["sub"] == str(user_id)
    assert tokens.decode("not-a-token") is None

    other = PyJwtAccessTokens(Settings(jwt_secret="x" * 48, jwt_algorithm="HS256"))
    assert other.decode(issued.token) is None


@pytest.mark.asyncio
async def test_google_exchange_never_decodes_an_unverified_id_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = GoogleOIDCClient(
        Settings(google_client_id="client-id", google_client_secret="client-secret")
    )
    forged = jwt.encode(
        {"sub": "attacker", "email": "attacker@example.com", "email_verified": True},
        "not-the-google-key-but-long-enough-1234",
        algorithm="HS256",
    )

    async def fake_exchange(_: object) -> dict[str, object]:
        return {"id_token": forged}

    monkeypatch.setattr(client._oauth.google, "authorize_access_token", fake_exchange)
    with pytest.raises(ValueError):
        await client.exchange(object())

    async def fake_with_userinfo(_: object) -> dict[str, object]:
        return {"userinfo": {"sub": "verified", "email": "verified@example.com"}}

    monkeypatch.setattr(client._oauth.google, "authorize_access_token", fake_with_userinfo)
    assert await client.exchange(object()) == {
        "sub": "verified",
        "email": "verified@example.com",
    }


def test_expired_access_token_is_rejected() -> None:
    settings = Settings(jwt_secret="s" * 48, jwt_algorithm="HS256")
    tokens = PyJwtAccessTokens(settings)
    expired = jwt.encode(
        {
            "sub": "00000000-0000-0000-0000-000000000001",
            "jti": "jti",
            "iat": int((NOW - timedelta(hours=1)).timestamp()),
            "exp": int((NOW - timedelta(minutes=1)).timestamp()),
        },
        settings.jwt_secret,
        algorithm="HS256",
    )

    assert tokens.decode(expired) is None


def build_session() -> AuthSession:
    user = User(
        id=uuid4(),
        email=Email.parse("user@example.com"),
        password_hash=None,
        google_sub=None,
        display_name=None,
        locale=None,
        is_active=True,
        created_at=NOW,
    )
    return AuthSession(
        user=user,
        access_token="access-token",
        access_expires_at=NOW + timedelta(minutes=15),
        refresh_token="refresh-token",
        refresh_expires_at=NOW + timedelta(days=30),
    )


def test_cookies_are_httponly_except_csrf_and_samesite_lax() -> None:
    settings = Settings(cookie_secure=False)
    response = Response()
    set_session_cookies(response, build_session(), settings)
    cookies = response.headers.getlist("set-cookie")

    assert len(cookies) == 3
    access = next(cookie for cookie in cookies if cookie.startswith("tl_access="))
    refresh = next(cookie for cookie in cookies if cookie.startswith("tl_refresh="))
    csrf = next(cookie for cookie in cookies if cookie.startswith("tl_csrf="))
    assert "HttpOnly" in access
    assert "HttpOnly" in refresh
    assert "HttpOnly" not in csrf
    assert all("SameSite=lax" in cookie for cookie in cookies)
    assert all("Secure" not in cookie for cookie in cookies)
    assert "Path=/api/v1/auth" in refresh


def test_session_defaults_are_persistent() -> None:
    settings = Settings(cookie_secure=False)
    assert settings.access_token_ttl_min == 5_256_000
    assert settings.refresh_token_ttl_days == 3_650

    response = Response()
    set_session_cookies(response, build_session(), settings)
    cookies = response.headers.getlist("set-cookie")
    access = next(cookie for cookie in cookies if cookie.startswith("tl_access="))
    refresh = next(cookie for cookie in cookies if cookie.startswith("tl_refresh="))

    assert "Max-Age=315360000" in access
    assert "Max-Age=315360000" in refresh


def test_production_cookies_use_host_prefix_and_secure() -> None:
    settings = Settings(
        app_env="production",
        cookie_secure=True,
        jwt_secret="j" * 48,
        csrf_secret="c" * 48,
        session_secret="s" * 48,
        metrics_token="m" * 48,
    )
    response = Response()
    set_session_cookies(response, build_session(), settings)
    cookies = response.headers.getlist("set-cookie")

    assert any(cookie.startswith("__Host-tl_access=") for cookie in cookies)
    assert any(cookie.startswith("__Secure-tl_refresh=") for cookie in cookies)
    assert all("Secure" in cookie for cookie in cookies)


def test_clear_cookies_deletes_all_session_cookies() -> None:
    response = Response()
    clear_session_cookies(response, Settings())
    cookies = response.headers.getlist("set-cookie")

    assert len(cookies) == 3
    assert all("Max-Age=0" in cookie for cookie in cookies)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("/links", "/links"),
        ("/pt-BR/account?tab=1", "/pt-BR/account?tab=1"),
        (None, "/"),
        ("", "/"),
    ],
)
def test_safe_next_accepts_internal_paths(value: str | None, expected: str) -> None:
    assert safe_next_path(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "//evil.com",
        "https://evil.com",
        "http://evil.com/path",
        "/\\evil.com",
        "///evil.com",
        "/%5cevil.com",
        "/bad\x00path",
    ],
)
def test_safe_next_rejects_external_or_control_paths(value: str) -> None:
    with pytest.raises(InvalidNextPath):
        safe_next_path(value)


def test_cookie_prefix_disabled_when_domain_is_set() -> None:
    settings = replace(
        Settings(
            app_env="production",
            cookie_secure=True,
            jwt_secret="j" * 48,
            csrf_secret="c" * 48,
            session_secret="s" * 48,
            metrics_token="m" * 48,
        ),
        cookie_domain=".example.com",
    )
    assert settings.access_cookie_name == "tl_access"
