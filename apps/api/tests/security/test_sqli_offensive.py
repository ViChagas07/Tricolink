from __future__ import annotations

import time
from urllib.parse import quote
from uuid import uuid4

import pytest
from fastapi import FastAPI

from tricolink.core.deps import CurrentUser, get_current_user, get_current_user_optional
from tricolink.main import create_app

from .helpers import (
    cleanup,
    make_client,
    security_settings,
    seed_link,
    seed_user,
    unique_ip,
)

pytestmark = pytest.mark.integration

PAYLOADS = [
    "' OR 1=1--",
    "' OR '1'='1",
    "'; DROP TABLE links;--",
    "' UNION SELECT NULL, NULL, NULL--",
    "') OR ('1'='1",
    "admin'--",
    "1' AND (SELECT COUNT(*) FROM users) > 0--",
    "%' OR title LIKE '%",
    "_' OR 1=1--",
    "\\'; DROP TABLE users;--",
]


def test_sqli_payloads_are_inert_in_every_input() -> None:
    settings = security_settings()
    user = seed_user(settings)
    code = f"sq{uuid4().hex[:6]}"
    seed_link(settings, code=code, user_id=user)
    app: FastAPI = create_app(settings)
    app.dependency_overrides[get_current_user_optional] = lambda: CurrentUser(id=user)
    app.dependency_overrides[get_current_user] = lambda: CurrentUser(id=user)

    try:
        with make_client(app, forwarded_for=unique_ip()) as client:
            for payload in PAYLOADS:
                encoded = quote(payload, safe="")

                redirect = client.get(f"/api/v1/r/{encoded}", follow_redirects=False)
                assert redirect.status_code == 404, (payload, redirect.text)

                detail = client.get(f"/api/v1/links/{encoded}")
                assert detail.status_code == 404, (payload, detail.text)

                listing = client.get("/api/v1/links", params={"q": payload})
                assert listing.status_code == 200, (payload, listing.text)
                assert listing.json()["items"] == [], payload

                cursor = client.get("/api/v1/links", params={"cursor": payload})
                assert cursor.status_code == 400, (payload, cursor.text)
                assert cursor.json()["error"]["code"] == "invalid_cursor"

                alias = client.post(
                    "/api/v1/links",
                    json={"url": "https://93.184.216.34/x", "alias": payload},
                )
                assert alias.status_code == 422, (payload, alias.text)

                stats = client.get(f"/api/v1/links/{encoded}/stats")
                assert stats.status_code in {404, 422}, (payload, stats.text)

            wildcard = client.get("/api/v1/links", params={"q": "%"})
            assert wildcard.status_code == 200
            assert wildcard.json()["items"] == []
            underscore = client.get("/api/v1/links", params={"q": "_"})
            assert underscore.status_code == 200
            assert underscore.json()["items"] == []

            assert client.get(f"/api/v1/links/{code}").status_code == 200
    finally:
        cleanup(settings, codes=[code], user_ids=[user])


def test_sqli_payloads_in_auth_fields_do_not_break_the_flow() -> None:
    settings = security_settings()
    password = "correct horse battery staple"
    app = create_app(settings)

    with make_client(app, forwarded_for=unique_ip()) as client:
        for payload in PAYLOADS:
            login = client.post(
                "/api/v1/auth/login",
                json={"email": payload, "password": password},
                headers={"Origin": "http://frontend.test"},
            )
            assert login.status_code in {400, 401, 422}, (payload, login.text)
            assert login.json()["error"]["code"] != "internal_error"

            register = client.post(
                "/api/v1/auth/register",
                json={"email": payload, "password": password},
                headers={"Origin": "http://frontend.test"},
            )
            assert register.status_code in {400, 401, 422}, (payload, register.text)
            assert register.json()["error"]["code"] != "internal_error"

        me = client.get("/api/v1/auth/me")
        assert me.status_code == 401


def test_time_based_payload_does_not_execute_pg_sleep() -> None:
    settings = security_settings()
    user = seed_user(settings)
    code = f"tb{uuid4().hex[:6]}"
    seed_link(settings, code=code, user_id=user)
    app: FastAPI = create_app(settings)
    app.dependency_overrides[get_current_user] = lambda: CurrentUser(id=user)

    try:
        with make_client(app, forwarded_for=unique_ip()) as client:
            started = time.perf_counter()
            response = client.get(
                "/api/v1/links",
                params={"q": "'; SELECT pg_sleep(2);--"},
            )
            elapsed = time.perf_counter() - started

        assert response.status_code == 200
        assert elapsed < 1.5, f"time-based payload took {elapsed:.3f}s"
    finally:
        cleanup(settings, codes=[code], user_ids=[user])
