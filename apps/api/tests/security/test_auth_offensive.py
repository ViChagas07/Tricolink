from __future__ import annotations

import time
from statistics import median
from uuid import uuid4

import jwt
import pytest
from fastapi import FastAPI

from tricolink.main import create_app

from .helpers import (
    cleanup_email,
    make_client,
    security_settings,
    unique_ip,
)

pytestmark = pytest.mark.integration

PASSWORD = "correct horse battery staple"
ORIGIN = {"Origin": "http://frontend.test"}


def register(client: object, email: str) -> None:
    response = client.post(  # type: ignore[attr-defined]
        "/api/v1/auth/register",
        json={"email": email, "password": PASSWORD},
        headers=ORIGIN,
    )
    assert response.status_code == 202, response.text


def login(client: object, email: str, password: str = PASSWORD):  # type: ignore[no-untyped-def]
    return client.post(  # type: ignore[attr-defined]
        "/api/v1/auth/login",
        json={"email": email, "password": password},
        headers=ORIGIN,
    )


def csrf_headers(client: object) -> dict[str, str]:  # type: ignore[no-untyped-def]
    token = client.cookies.get("tl_csrf")  # type: ignore[attr-defined]
    assert token
    return {**ORIGIN, "X-CSRF-Token": token}


def test_jwt_tampering_alg_none_expiry_and_cookie_flags() -> None:
    settings = security_settings()
    email = f"jwt-{uuid4()}@example.com"
    app: FastAPI = create_app(settings)

    try:
        with make_client(app, forwarded_for=unique_ip()) as client:
            register(client, email)
            signed_in = login(client, email)
            assert signed_in.status_code == 200, signed_in.text
            assert "access_token" not in signed_in.text
            assert "refresh_token" not in signed_in.text

            getter = getattr(signed_in.headers, "get_list", None) or signed_in.headers.getlist
            cookies = list(getter("set-cookie"))
            access_cookie = next(item for item in cookies if item.startswith("tl_access="))
            refresh_cookie = next(item for item in cookies if item.startswith("tl_refresh="))
            csrf_cookie = next(item for item in cookies if item.startswith("tl_csrf="))
            assert "HttpOnly" in access_cookie
            assert "HttpOnly" in refresh_cookie
            assert "HttpOnly" not in csrf_cookie
            assert "SameSite=lax" in access_cookie
            assert "Path=/api/v1/auth" in refresh_cookie
            assert "Secure" not in access_cookie

            valid_access = client.cookies.get("tl_access")
            assert valid_access
            assert client.get("/api/v1/auth/me").status_code == 200

            payload = {
                "sub": "00000000-0000-0000-0000-000000000001",
                "jti": "forged",
                "iat": int(time.time()),
                "exp": int(time.time()) + 900,
            }
            alg_none = jwt.encode(payload, key="", algorithm="none")
            client.cookies.set("tl_access", alg_none)
            assert client.get("/api/v1/auth/me").status_code == 401

            wrong_secret = jwt.encode(payload, "x" * 48, algorithm="HS256")
            client.cookies.set("tl_access", wrong_secret)
            assert client.get("/api/v1/auth/me").status_code == 401

            expired = jwt.encode(
                {**payload, "exp": int(time.time()) - 1},
                settings.jwt_secret,
                algorithm="HS256",
            )
            client.cookies.set("tl_access", expired)
            assert client.get("/api/v1/auth/me").status_code == 401

            missing_claims = jwt.encode(
                {"sub": payload["sub"], "exp": int(time.time()) + 900},
                settings.jwt_secret,
                algorithm="HS256",
            )
            client.cookies.set("tl_access", missing_claims)
            assert client.get("/api/v1/auth/me").status_code == 401

            client.cookies.set("tl_access", f"{valid_access}tampered")
            assert client.get("/api/v1/auth/me").status_code == 401
    finally:
        cleanup_email(settings, email)


def test_csrf_origin_and_cross_site_mutations_are_rejected() -> None:
    settings = security_settings()
    email = f"csrf-{uuid4()}@example.com"
    app = create_app(settings)

    try:
        with make_client(app, forwarded_for=unique_ip()) as client:
            register(client, email)
            assert login(client, email).status_code == 200
            token = client.cookies.get("tl_csrf")
            assert token

            no_token = client.patch(
                "/api/v1/auth/me",
                json={"display_name": "Nope"},
                headers=ORIGIN,
            )
            assert no_token.status_code == 403
            assert no_token.json()["error"]["code"] == "invalid_csrf_token"

            wrong_token = client.patch(
                "/api/v1/auth/me",
                json={"display_name": "Nope"},
                headers={**ORIGIN, "X-CSRF-Token": f"{token}x"},
            )
            assert wrong_token.status_code == 403

            wrong_origin = client.patch(
                "/api/v1/auth/me",
                json={"display_name": "Nope"},
                headers={"Origin": "http://evil.test", "X-CSRF-Token": token},
            )
            assert wrong_origin.status_code == 403

            cross_site = client.patch(
                "/api/v1/auth/me",
                json={"display_name": "Nope"},
                headers={
                    **ORIGIN,
                    "X-CSRF-Token": token,
                    "Sec-Fetch-Site": "cross-site",
                },
            )
            assert cross_site.status_code == 403

            valid = client.patch(
                "/api/v1/auth/me",
                json={"display_name": "Allowed"},
                headers={**ORIGIN, "X-CSRF-Token": token},
            )
            assert valid.status_code == 200, valid.text
            assert valid.json()["display_name"] == "Allowed"
    finally:
        cleanup_email(settings, email)


def test_idor_sessions_and_link_ownership() -> None:
    settings = security_settings()
    email_a = f"owner-a-{uuid4()}@example.com"
    email_b = f"owner-b-{uuid4()}@example.com"
    app = create_app(settings)

    try:
        with make_client(app, forwarded_for=unique_ip()) as client_a:
            register(client_a, email_a)
            assert login(client_a, email_a).status_code == 200
            created = client_a.post(
                "/api/v1/links",
                json={"url": "https://93.184.216.34/owned", "title": "Owned"},
                headers=csrf_headers(client_a),
            )
            assert created.status_code == 201, created.text
            code = created.json()["code"]

            access_a = client_a.cookies.get("tl_access")
            assert access_a

            with make_client(create_app(settings), forwarded_for=unique_ip()) as client_b:
                register(client_b, email_b)
                assert login(client_b, email_b).status_code == 200

                assert client_b.get(f"/api/v1/links/{code}").status_code == 404
                assert client_b.get(f"/api/v1/links/{code}/stats").status_code == 404
                assert (
                    client_b.patch(
                        f"/api/v1/links/{code}",
                        json={"title": "Stolen"},
                        headers=csrf_headers(client_b),
                    ).status_code
                    == 404
                )
                assert (
                    client_b.delete(
                        f"/api/v1/links/{code}",
                        headers=csrf_headers(client_b),
                    ).status_code
                    == 404
                )
                listing = client_b.get("/api/v1/links")
                assert listing.status_code == 200
                assert all(item["code"] != code for item in listing.json()["items"])

                # Replacing the cookie with another user's valid session must
                # still not grant access to the first user's resources.
                access_b = client_b.cookies.get("tl_access")
                assert access_b
                client_b.cookies.set("tl_access", access_a)
                assert client_b.get("/api/v1/auth/me").status_code == 200
                assert client_b.get(f"/api/v1/links/{code}").status_code == 200

            client_a.cookies.set("tl_access", access_a)
            assert client_a.get(f"/api/v1/links/{code}").status_code == 200
    finally:
        cleanup_email(settings, email_a)
        cleanup_email(settings, email_b)


def test_refresh_reuse_revokes_the_whole_family_and_logout_revokes_refresh() -> None:
    settings = security_settings()
    email = f"family-{uuid4()}@example.com"
    app = create_app(settings)

    try:
        with make_client(app, forwarded_for=unique_ip()) as client:
            register(client, email)
            assert login(client, email).status_code == 200
            old_refresh = client.cookies.get("tl_refresh")
            assert old_refresh

            first = client.post("/api/v1/auth/refresh", headers=csrf_headers(client))
            assert first.status_code == 200, first.text
            new_refresh = client.cookies.get("tl_refresh")
            assert new_refresh and new_refresh != old_refresh

            reused = client.post(
                "/api/v1/auth/refresh",
                cookies={"tl_refresh": old_refresh, "tl_csrf": client.cookies.get("tl_csrf")},
                headers=csrf_headers(client),
            )
            assert reused.status_code == 401

            after_reuse = client.post(
                "/api/v1/auth/refresh",
                cookies={
                    "tl_refresh": new_refresh,
                    "tl_csrf": client.cookies.get("tl_csrf"),
                },
                headers=csrf_headers(client),
            )
            assert after_reuse.status_code == 401

            assert login(client, email).status_code == 200
            logout_refresh = client.cookies.get("tl_refresh")
            logout_csrf = client.cookies.get("tl_csrf")
            assert logout_refresh and logout_csrf
            logged_out = client.post(
                "/api/v1/auth/logout",
                headers={**ORIGIN, "X-CSRF-Token": logout_csrf},
            )
            assert logged_out.status_code == 204

            after_logout = client.post(
                "/api/v1/auth/refresh",
                cookies={"tl_refresh": logout_refresh, "tl_csrf": logout_csrf},
                headers={**ORIGIN, "X-CSRF-Token": logout_csrf},
            )
            assert after_logout.status_code == 401
    finally:
        cleanup_email(settings, email)


def test_login_and_register_brute_force_are_rate_limited() -> None:
    settings = security_settings(rl_auth_capacity=10, rl_auth_refill_per_sec=0)
    email = f"brute-{uuid4()}@example.com"
    app = create_app(settings)

    try:
        with make_client(app, forwarded_for=unique_ip()) as client:
            register(client, email)
            statuses = [login(client, email, "wrong password").status_code for _ in range(10)]
            assert 429 in statuses
            assert statuses.count(401) >= 1
    finally:
        cleanup_email(settings, email)

    register_settings = security_settings(rl_auth_capacity=10, rl_auth_refill_per_sec=0)
    register_app = create_app(register_settings)
    with make_client(register_app, forwarded_for=unique_ip()) as client:
        statuses = [
            client.post(
                "/api/v1/auth/register",
                json={"email": f"enumerate-{uuid4()}@example.com", "password": PASSWORD},
                headers=ORIGIN,
            ).status_code
            for _ in range(12)
        ]
    assert 429 in statuses


def test_progressive_lockout_after_repeated_failures() -> None:
    settings = security_settings(auth_lockout_threshold=2, rl_auth_capacity=1000)
    email = f"lockout-{uuid4()}@example.com"
    app = create_app(settings)

    try:
        with make_client(app, forwarded_for=unique_ip()) as client:
            register(client, email)
            statuses = [login(client, email, "wrong password").status_code for _ in range(5)]
        assert statuses[:2] == [401, 401]
        assert statuses[2] == 429
    finally:
        cleanup_email(settings, email)


def test_login_and_register_do_not_enumerate_emails_by_response() -> None:
    settings = security_settings(auth_lockout_threshold=1000, rl_auth_capacity=1000)
    existing = f"known-{uuid4()}@example.com"
    missing = f"missing-{uuid4()}@example.com"
    app = create_app(settings)

    try:
        with make_client(app, forwarded_for=unique_ip()) as client:
            register(client, existing)

            known = login(client, existing, "wrong password")
            unknown = login(client, missing, "wrong password")
            assert known.status_code == unknown.status_code == 401
            assert known.json() == unknown.json()
            assert known.json()["error"]["code"] == "invalid_credentials"

            new_email = f"new-{uuid4()}@example.com"
            first = client.post(
                "/api/v1/auth/register",
                json={"email": new_email, "password": PASSWORD},
                headers=ORIGIN,
            )
            duplicate = client.post(
                "/api/v1/auth/register",
                json={"email": new_email, "password": PASSWORD},
                headers=ORIGIN,
            )
            assert first.status_code == duplicate.status_code == 202
            assert first.json() == duplicate.json()
            cleanup_email(settings, new_email)
    finally:
        cleanup_email(settings, existing)


def test_login_timing_does_not_reveal_whether_the_email_exists() -> None:
    settings = security_settings(auth_lockout_threshold=1000, rl_auth_capacity=1000)
    existing = f"timing-{uuid4()}@example.com"
    missing = f"timing-missing-{uuid4()}@example.com"
    app = create_app(settings)

    try:
        with make_client(app, forwarded_for=unique_ip()) as client:
            register(client, existing)
            known_samples: list[float] = []
            unknown_samples: list[float] = []
            for _ in range(5):
                started = time.perf_counter()
                assert login(client, existing, "wrong password").status_code == 401
                known_samples.append(time.perf_counter() - started)

                started = time.perf_counter()
                assert login(client, missing, "wrong password").status_code == 401
                unknown_samples.append(time.perf_counter() - started)

        difference = abs(median(known_samples) - median(unknown_samples))
        assert difference < 0.05, (
            f"median timing difference {difference:.3f}s "
            f"(known={median(known_samples):.3f}s, unknown={median(unknown_samples):.3f}s)"
        )
    finally:
        cleanup_email(settings, existing)


def test_google_next_rejects_open_redirect_variants() -> None:
    settings = security_settings(
        google_client_id="test-client-id",
        google_client_secret="test-client-secret",
        google_redirect_uri="http://api.test/api/v1/auth/google/callback",
    )
    app = create_app(settings)

    with make_client(app, forwarded_for=unique_ip()) as client:
        for value in (
            "//evil.example",
            "https://evil.example/path",
            "/%2F%2Fevil.example",
            "/\\evil.example",
            "/%5cevil.example",
            "javascript:alert(1)",
            "///evil.example",
        ):
            response = client.get(
                "/api/v1/auth/google/login",
                params={"next": value},
                follow_redirects=False,
            )
            assert response.status_code == 400, (value, response.text)

        accepted = client.get(
            "/api/v1/auth/google/login",
            params={"next": "/links"},
            follow_redirects=False,
        )
        assert accepted.status_code == 302
        assert accepted.headers["location"].startswith(
            "https://accounts.google.com/o/oauth2/v2/auth?"
        )
