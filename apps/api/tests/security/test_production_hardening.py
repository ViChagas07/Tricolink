from __future__ import annotations

from dataclasses import replace
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from tricolink.core.config import Settings
from tricolink.main import create_app

from .helpers import cleanup_email, make_client, security_settings, unique_ip

pytestmark = pytest.mark.integration


def production_settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "app_env": "production",
        "cookie_secure": True,
        "jwt_secret": "j" * 48,
        "csrf_secret": "c" * 48,
        "session_secret": "s" * 48,
        "metrics_token": "m" * 48,
        "click_flusher_enabled": False,
        "frontend_origin": "http://frontend.test",
        "api_public_base_url": "http://api.test",
        "short_base_url": "https://short.test",
        "trusted_proxy_count": 1,
        "rl_auth_capacity": 1000,
        "rl_auth_refill_per_sec": 1000,
        "rl_create_capacity": 1000,
        "rl_create_refill_per_sec": 1000,
        "rl_global_capacity": 100_000,
        "rl_global_refill_per_sec": 100_000,
    }
    values.update(overrides)
    return replace(Settings.from_env(), **values)


def test_metrics_is_not_exposed_with_a_development_token() -> None:
    settings = production_settings(metrics_token="change-me")
    app: FastAPI = create_app(settings)
    client = make_client(app, forwarded_for=unique_ip())

    with client:
        response = client.get("/metrics", headers={"Authorization": "Bearer change-me"})

    assert response.status_code == 404
    assert "tricolink_http_requests_total" not in response.text


def test_docs_openapi_metrics_and_security_headers_in_production() -> None:
    settings = production_settings()
    app: FastAPI = create_app(settings)
    client = make_client(app, forwarded_for=unique_ip())

    with client:
        assert client.get("/docs").status_code == 404
        assert client.get("/openapi.json").status_code == 404

        no_token = client.get("/metrics")
        wrong_token = client.get(
            "/metrics",
            headers={"Authorization": "Bearer wrong"},
        )
        accepted = client.get(
            "/metrics",
            headers={"Authorization": f"Bearer {settings.metrics_token}"},
        )
        not_found = client.get("/api/v1/r/zzzzzz9")

    assert no_token.status_code == 401
    assert wrong_token.status_code == 401
    assert accepted.status_code == 200
    assert "text/plain" in accepted.headers["content-type"]
    assert accepted.headers["cache-control"] == "no-store"

    for response in (accepted, not_found):
        assert response.headers["x-content-type-options"] == "nosniff"
        assert response.headers["x-frame-options"] == "DENY"
        assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"
        assert response.headers["cross-origin-opener-policy"] == "same-origin"
        assert "camera=()" in response.headers["permissions-policy"]
        assert "max-age=63072000" in response.headers["strict-transport-security"]
        assert "default-src 'none'" in response.headers["content-security-policy"]
        assert "'unsafe-inline'" not in response.headers["content-security-policy"]
        assert "'unsafe-eval'" not in response.headers["content-security-policy"]

    assert not_found.status_code == 404
    assert not_found.headers["x-robots-tag"] == "noindex, nofollow"


def test_no_cors_headers_are_emitted() -> None:
    settings = production_settings()
    app = create_app(settings)
    client = make_client(app, forwarded_for=unique_ip())

    with client:
        preflight = client.options(
            "/api/v1/links",
            headers={
                "Origin": "https://evil.example",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )
        health = client.get("/health/live", headers={"Origin": "https://evil.example"})

    for response in (preflight, health):
        assert "access-control-allow-origin" not in response.headers
        assert "access-control-allow-credentials" not in response.headers
        assert "access-control-allow-methods" not in response.headers


def test_production_cookies_are_secure_and_auth_responses_are_not_cached() -> None:
    settings = production_settings()
    email = f"prod-{uuid4()}@example.com"
    password = "correct horse battery staple"
    app = create_app(settings)

    try:
        with make_client(
            app,
            forwarded_for=unique_ip(),
            base_url="https://testserver",
        ) as client:
            register = client.post(
                "/api/v1/auth/register",
                json={"email": email, "password": password},
                headers={"Origin": "http://frontend.test"},
            )
            assert register.status_code == 202, register.text
            assert register.headers["cache-control"] == "no-store"

            signed_in = client.post(
                "/api/v1/auth/login",
                json={"email": email, "password": password},
                headers={"Origin": "http://frontend.test"},
            )
            assert signed_in.status_code == 200, signed_in.text
            assert signed_in.headers["cache-control"] == "no-store"

            getter = getattr(signed_in.headers, "get_list", None) or signed_in.headers.getlist
            cookies = list(getter("set-cookie"))
            assert any(item.startswith("__Host-tl_access=") for item in cookies)
            assert any(item.startswith("__Secure-tl_refresh=") for item in cookies)
            assert all("Secure" in item for item in cookies)

            me = client.get("/api/v1/auth/me")
            assert me.status_code == 200
            assert me.headers["cache-control"] == "no-store"
    finally:
        cleanup_email(settings, email)


def test_unexpected_errors_do_not_leak_stack_traces_or_validation_inputs() -> None:
    settings = security_settings()
    app: FastAPI = create_app(settings)

    async def boom() -> None:
        raise RuntimeError("secret internal detail")

    app.add_api_route("/boom", boom)

    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/boom")
        validation = client.post(
            "/api/v1/links",
            json={"url": 123, "unknown": "SUPERSECRET-VALUE"},
        )

    assert response.status_code == 500
    assert response.json() == {
        "error": {"code": "internal_error", "message": "Internal server error"}
    }
    assert "secret internal detail" not in response.text
    assert "Traceback" not in response.text

    assert validation.status_code in {400, 422}
    assert "SUPERSECRET-VALUE" not in validation.text
    assert validation.json()["error"]["code"] in {"validation_error", "invalid_url"}
