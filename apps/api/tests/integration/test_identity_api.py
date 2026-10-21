from __future__ import annotations

import asyncio
from dataclasses import replace
from typing import Any
from urllib.parse import parse_qs, urlsplit
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete, select

from tricolink.core.config import Settings
from tricolink.infra.db import Database
from tricolink.infra.db.models import Link as LinkRow
from tricolink.infra.db.models import RefreshToken as RefreshTokenRow
from tricolink.infra.db.models import User as UserRow
from tricolink.main import create_app
from tricolink.modules.identity.application import hash_refresh_token
from tricolink.modules.identity.presentation.dependencies import get_google_oidc

pytestmark = pytest.mark.integration


def identity_settings(**overrides: object) -> Settings:
    unique = uuid4().hex[:10]
    base = replace(
        Settings.from_env(),
        app_env="test",
        click_flusher_enabled=False,
        click_stream_key=f"test:auth-clicks:{unique}",
        click_stream_group=f"test-auth-clicks-{unique}",
        frontend_origin="http://frontend.test",
        api_public_base_url="http://api.test",
        short_base_url="https://short.test",
        cookie_secure=False,
        jwt_secret="j" * 48,
        csrf_secret="c" * 48,
        session_secret="s" * 48,
        trusted_proxy_count=1,
        rl_auth_capacity=1000,
        rl_auth_refill_per_sec=1000,
        rl_create_capacity=1000,
        rl_create_refill_per_sec=1000,
        rl_redirect_capacity=1000,
        rl_redirect_refill_per_sec=1000,
        rl_global_capacity=100_000,
        rl_global_refill_per_sec=100_000,
        rl_list_capacity=1000,
        rl_list_refill_per_sec=1000,
        argon2_time_cost=1,
        argon2_memory_kib=1_024,
        argon2_parallelism=1,
        argon2_hash_len=16,
        argon2_salt_len=8,
        auth_lockout_threshold=10,
        auth_failure_window_seconds=900,
        auth_lockout_seconds=900,
        google_client_id="test-client-id",
        google_client_secret="test-client-secret",
        google_redirect_uri="http://api.test/api/v1/auth/google/callback",
    )
    return replace(base, **overrides)


def admin_settings(settings: Settings) -> Settings:
    return replace(
        settings,
        database_url=settings.migration_database_url or settings.database_url,
    )


def cleanup(settings: Settings, *, email: str, codes: list[str]) -> None:
    async def run() -> None:
        database = Database(admin_settings(settings))
        try:
            async with database.unit_of_work() as session:
                if codes:
                    await session.execute(delete(LinkRow).where(LinkRow.code.in_(codes)))
                user_ids = (
                    await session.scalars(select(UserRow.id).where(UserRow.email == email))
                ).all()
                for user_id in user_ids:
                    await session.execute(delete(LinkRow).where(LinkRow.user_id == user_id))
                    await session.execute(delete(UserRow).where(UserRow.id == user_id))
        finally:
            await database.dispose()

    asyncio.run(run())


def make_client(app: Any) -> TestClient:
    forwarded = f"2001:db8::{uuid4().hex[:4]}:{uuid4().hex[:4]}:{uuid4().hex[:4]}:{uuid4().hex[:4]}"
    return TestClient(app, headers={"X-Forwarded-For": forwarded})


def login(client: TestClient, email: str, password: str) -> Any:
    return client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
        headers={"Origin": "http://frontend.test"},
    )


def set_cookie_headers(response: Any) -> list[str]:
    headers = response.headers
    getter = getattr(headers, "get_list", None) or headers.getlist
    return list(getter("set-cookie"))


def test_register_login_me_refresh_logout_flow() -> None:
    settings = identity_settings()
    email = f"flow-{uuid4()}@example.com"
    password = "correct horse battery staple"
    code: str | None = None
    try:
        app = create_app(settings)
        with make_client(app) as client:
            registered = client.post(
                "/api/v1/auth/register",
                json={"email": email, "password": password},
                headers={"Origin": "http://frontend.test"},
            )
            assert registered.status_code == 202, registered.text
            assert registered.json() == {"status": "registered"}
            assert not any("tl_access=" in header for header in set_cookie_headers(registered))

            failed = login(client, email, "wrong password")
            assert failed.status_code == 401
            assert failed.json()["error"]["code"] == "invalid_credentials"

            signed_in = login(client, email, password)
            assert signed_in.status_code == 200, signed_in.text
            assert "access_token" not in signed_in.text
            assert "refresh_token" not in signed_in.text
            cookies = set_cookie_headers(signed_in)
            access_cookie = next(header for header in cookies if header.startswith("tl_access="))
            refresh_cookie = next(header for header in cookies if header.startswith("tl_refresh="))
            csrf_cookie = next(header for header in cookies if header.startswith("tl_csrf="))
            assert "HttpOnly" in access_cookie
            assert "HttpOnly" in refresh_cookie
            assert "HttpOnly" not in csrf_cookie
            assert "SameSite=lax" in access_cookie

            me = client.get("/api/v1/auth/me")
            assert me.status_code == 200
            assert me.json()["email"] == email

            csrf = client.cookies.get("tl_csrf")
            assert csrf
            missing_csrf = client.patch(
                "/api/v1/auth/me",
                json={"display_name": "Changed"},
                headers={"Origin": "http://frontend.test"},
            )
            assert missing_csrf.status_code == 403
            assert missing_csrf.json()["error"]["code"] == "invalid_csrf_token"

            bad_origin_csrf = client.patch(
                "/api/v1/auth/me",
                json={"display_name": "Changed"},
                headers={
                    "Origin": "http://evil.test",
                    "X-CSRF-Token": csrf,
                },
            )
            assert bad_origin_csrf.status_code == 403

            updated = client.patch(
                "/api/v1/auth/me",
                json={"display_name": "Changed"},
                headers={
                    "Origin": "http://frontend.test",
                    "X-CSRF-Token": csrf,
                },
            )
            assert updated.status_code == 200, updated.text
            assert updated.json()["display_name"] == "Changed"

            created = client.post(
                "/api/v1/links",
                json={"url": "https://93.184.216.34/auth-flow"},
                headers={
                    "Origin": "http://frontend.test",
                    "X-CSRF-Token": csrf,
                },
            )
            assert created.status_code == 201, created.text
            code = created.json()["code"]

            listing = client.get("/api/v1/links")
            assert listing.status_code == 200
            assert listing.json()["items"][0]["code"] == code

            old_refresh = client.cookies.get("tl_refresh")
            assert old_refresh
            refreshed = client.post(
                "/api/v1/auth/refresh",
                headers={
                    "Origin": "http://frontend.test",
                    "X-CSRF-Token": csrf,
                },
            )
            assert refreshed.status_code == 200, refreshed.text
            new_refresh = client.cookies.get("tl_refresh")
            assert new_refresh and new_refresh != old_refresh
            csrf = client.cookies.get("tl_csrf")
            assert csrf

            logged_out = client.post(
                "/api/v1/auth/logout",
                headers={
                    "Origin": "http://frontend.test",
                    "X-CSRF-Token": csrf,
                },
            )
            assert logged_out.status_code == 204
            assert client.get("/api/v1/auth/me").status_code == 401
    finally:
        cleanup(settings, email=email, codes=[code] if code else [])


def test_refresh_reuse_revokes_the_family() -> None:
    settings = identity_settings()
    email = f"reuse-{uuid4()}@example.com"
    password = "correct horse battery staple"
    try:
        with make_client(create_app(settings)) as client:
            assert (
                client.post(
                    "/api/v1/auth/register",
                    json={"email": email, "password": password},
                    headers={"Origin": "http://frontend.test"},
                ).status_code
                == 202
            )
            assert login(client, email, password).status_code == 200

            old_refresh = client.cookies.get("tl_refresh")
            csrf = client.cookies.get("tl_csrf")
            assert old_refresh and csrf
            first = client.post(
                "/api/v1/auth/refresh",
                headers={
                    "Origin": "http://frontend.test",
                    "X-CSRF-Token": csrf,
                },
            )
            assert first.status_code == 200, first.text
            new_refresh = client.cookies.get("tl_refresh")
            assert new_refresh and new_refresh != old_refresh

            reused = client.post(
                "/api/v1/auth/refresh",
                cookies={"tl_refresh": old_refresh, "tl_csrf": csrf},
                headers={
                    "Origin": "http://frontend.test",
                    "X-CSRF-Token": csrf,
                },
            )
            assert reused.status_code == 401

            async def family_status() -> list[tuple[str, bool]]:
                database = Database(admin_settings(settings))
                try:
                    async with database.read() as session:
                        rows = (
                            await session.scalars(
                                select(RefreshTokenRow).where(
                                    RefreshTokenRow.token_hash.in_(
                                        [
                                            hash_refresh_token(old_refresh),
                                            hash_refresh_token(new_refresh),
                                        ]
                                    )
                                )
                            )
                        ).all()
                        return [(row.token_hash, row.revoked_at is not None) for row in rows]
                finally:
                    await database.dispose()

            statuses = asyncio.run(family_status())
            stored_hashes = {token_hash for token_hash, _ in statuses}
            assert statuses and all(revoked for _, revoked in statuses)
            assert old_refresh not in stored_hashes
            assert new_refresh not in stored_hashes
            assert hash_refresh_token(old_refresh) in stored_hashes
            assert hash_refresh_token(new_refresh) in stored_hashes
    finally:
        cleanup(settings, email=email, codes=[])


def test_login_rate_limit_after_repeated_failures() -> None:
    settings = identity_settings(
        rl_auth_capacity=5,
        rl_auth_refill_per_sec=0.0,
    )
    email = f"brute-{uuid4()}@example.com"
    password = "correct horse battery staple"
    try:
        with make_client(create_app(settings)) as client:
            client.post(
                "/api/v1/auth/register",
                json={"email": email, "password": password},
                headers={"Origin": "http://frontend.test"},
            )
            statuses = [login(client, email, "wrong password").status_code for _ in range(20)]

        assert 429 in statuses
        assert statuses.count(429) > 0
    finally:
        cleanup(settings, email=email, codes=[])


def test_progressive_lockout_returns_429_even_with_large_bucket() -> None:
    settings = identity_settings(
        rl_auth_capacity=1000,
        rl_auth_refill_per_sec=1000,
        auth_lockout_threshold=2,
    )
    email = f"lockout-{uuid4()}@example.com"
    password = "correct horse battery staple"
    try:
        with make_client(create_app(settings)) as client:
            client.post(
                "/api/v1/auth/register",
                json={"email": email, "password": password},
                headers={"Origin": "http://frontend.test"},
            )
            statuses = [login(client, email, "wrong password").status_code for _ in range(5)]
        assert statuses[:2] == [401, 401]
        assert statuses[2] == 429
    finally:
        cleanup(settings, email=email, codes=[])


def test_register_duplicate_is_indistinguishable_and_weak_password_rejected() -> None:
    settings = identity_settings()
    email = f"duplicate-{uuid4()}@example.com"
    password = "correct horse battery staple"
    try:
        with make_client(create_app(settings)) as client:
            first = client.post(
                "/api/v1/auth/register",
                json={"email": email, "password": password},
                headers={"Origin": "http://frontend.test"},
            )
            second = client.post(
                "/api/v1/auth/register",
                json={"email": email, "password": password},
                headers={"Origin": "http://frontend.test"},
            )
            weak = client.post(
                "/api/v1/auth/register",
                json={"email": f"weak-{uuid4()}@example.com", "password": "password123"},
                headers={"Origin": "http://frontend.test"},
            )
            bad_origin = client.post(
                "/api/v1/auth/register",
                json={"email": f"origin-{uuid4()}@example.com", "password": password},
                headers={"Origin": "http://evil.test"},
            )

        assert first.status_code == second.status_code == 202
        assert first.json() == second.json()
        assert weak.status_code == 400
        assert weak.json()["error"]["code"] == "weak_password"
        assert bad_origin.status_code == 403
    finally:
        cleanup(settings, email=email, codes=[])


def test_google_login_builds_state_nonce_and_pkce_and_rejects_unsafe_next() -> None:
    settings = identity_settings()
    with make_client(create_app(settings)) as client:
        response = client.get(
            "/api/v1/auth/google/login",
            params={"next": "/links"},
            follow_redirects=False,
        )
        blocked_double_slash = client.get(
            "/api/v1/auth/google/login",
            params={"next": "//evil.com"},
            follow_redirects=False,
        )
        blocked_absolute = client.get(
            "/api/v1/auth/google/login",
            params={"next": "https://evil.com"},
            follow_redirects=False,
        )

    assert response.status_code == 302
    location = response.headers["location"]
    assert location.startswith("https://accounts.google.com/o/oauth2/v2/auth?")
    assert "state=" in location
    assert "nonce=" in location
    assert "code_challenge=" in location
    assert "code_challenge_method=S256" in location
    assert blocked_double_slash.status_code == 400
    assert blocked_absolute.status_code == 400


def test_google_callback_rejects_bad_state() -> None:
    settings = identity_settings()
    with make_client(create_app(settings)) as client:
        login_response = client.get(
            "/api/v1/auth/google/login",
            params={"next": "/links"},
            follow_redirects=False,
        )
        assert login_response.status_code == 302
        callback = client.get(
            "/api/v1/auth/google/callback",
            params={"state": "bad-state", "code": "bad-code"},
            follow_redirects=False,
        )

    assert callback.status_code == 302
    assert callback.headers["location"].startswith("http://frontend.test/login?error=google")


class FakeGoogleOIDC:
    configured = True
    client_id = "test-client-id"

    def __init__(self, claims: dict[str, object]) -> None:
        self.claims = claims

    async def exchange(self, request: object) -> dict[str, object]:
        return self.claims


def google_claims(*, nonce: str, email: str, sub: str) -> dict[str, object]:
    from datetime import UTC, datetime, timedelta

    return {
        "iss": "https://accounts.google.com",
        "aud": "test-client-id",
        "exp": (datetime.now(UTC) + timedelta(minutes=5)).timestamp(),
        "nonce": nonce,
        "email_verified": True,
        "email": email,
        "sub": sub,
        "name": "Google User",
    }


def test_google_callback_success_links_user_and_rejects_bad_nonce() -> None:
    settings = identity_settings()
    email = f"google-{uuid4()}@example.com"
    app = create_app(settings)
    try:
        with make_client(app) as client:
            login_response = client.get(
                "/api/v1/auth/google/login",
                params={"next": "/links"},
                follow_redirects=False,
            )
            assert login_response.status_code == 302
            params = parse_qs(urlsplit(login_response.headers["location"]).query)
            state = params["state"][0]
            nonce = params["nonce"][0]

            bad_nonce_client = FakeGoogleOIDC(
                google_claims(nonce="wrong-nonce", email=email, sub="google-sub")
            )
            app.dependency_overrides[get_google_oidc] = lambda: bad_nonce_client
            rejected = client.get(
                "/api/v1/auth/google/callback",
                params={"state": state, "code": "code"},
                follow_redirects=False,
            )
            assert rejected.status_code == 302
            assert rejected.headers["location"].startswith(
                "http://frontend.test/login?error=google"
            )

            app.dependency_overrides.pop(get_google_oidc, None)
            login_response = client.get(
                "/api/v1/auth/google/login",
                params={"next": "/links"},
                follow_redirects=False,
            )
            params = parse_qs(urlsplit(login_response.headers["location"]).query)
            state = params["state"][0]
            nonce = params["nonce"][0]
            good = FakeGoogleOIDC(google_claims(nonce=nonce, email=email, sub="google-sub"))
            app.dependency_overrides[get_google_oidc] = lambda: good
            accepted = client.get(
                "/api/v1/auth/google/callback",
                params={"state": state, "code": "code"},
                follow_redirects=False,
            )

            assert accepted.status_code == 302
            assert accepted.headers["location"] == "http://frontend.test/links"
            me = client.get("/api/v1/auth/me")
            assert me.status_code == 200
            assert me.json()["email"] == email
            assert me.json()["display_name"] == "Google User"
    finally:
        cleanup(settings, email=email, codes=[])


def test_owner_isolation_with_real_sessions() -> None:
    settings = identity_settings()
    email_a = f"owner-a-{uuid4()}@example.com"
    email_b = f"owner-b-{uuid4()}@example.com"
    password = "correct horse battery staple"
    code: str | None = None
    try:
        with make_client(create_app(settings)) as client_a:
            assert (
                client_a.post(
                    "/api/v1/auth/register",
                    json={"email": email_a, "password": password},
                    headers={"Origin": "http://frontend.test"},
                ).status_code
                == 202
            )
            assert login(client_a, email_a, password).status_code == 200
            csrf_a = client_a.cookies.get("tl_csrf")
            assert csrf_a
            created = client_a.post(
                "/api/v1/links",
                json={"url": "https://93.184.216.34/owner"},
                headers={
                    "Origin": "http://frontend.test",
                    "X-CSRF-Token": csrf_a,
                },
            )
            assert created.status_code == 201, created.text
            code = created.json()["code"]

        with make_client(create_app(settings)) as client_b:
            assert (
                client_b.post(
                    "/api/v1/auth/register",
                    json={"email": email_b, "password": password},
                    headers={"Origin": "http://frontend.test"},
                ).status_code
                == 202
            )
            assert login(client_b, email_b, password).status_code == 200
            csrf_b = client_b.cookies.get("tl_csrf")
            assert csrf_b
            headers = {
                "Origin": "http://frontend.test",
                "X-CSRF-Token": csrf_b,
            }
            assert client_b.get(f"/api/v1/links/{code}").status_code == 404
            assert (
                client_b.patch(
                    f"/api/v1/links/{code}",
                    json={"title": "stolen"},
                    headers=headers,
                ).status_code
                == 404
            )
            assert (
                client_b.delete(
                    f"/api/v1/links/{code}",
                    headers=headers,
                ).status_code
                == 404
            )
    finally:
        cleanup(settings, email=email_a, codes=[code] if code else [])
        cleanup(settings, email=email_b, codes=[])
