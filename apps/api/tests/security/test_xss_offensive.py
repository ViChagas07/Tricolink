from __future__ import annotations

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
    seed_user,
    unique_ip,
)

pytestmark = pytest.mark.integration

TITLE_PAYLOADS = [
    "<script>alert(1)</script>",
    '"><img src=x onerror=alert(1)>',
    "javascript:alert(1)",
    "data:text/html,<script>alert(1)</script>",
    "<svg/onload=alert(1)>",
    "'><iframe srcdoc='<script>alert(1)</script>'>",
    "&lt;script&gt;alert(1)&lt;/script&gt;",
]

ALIAS_PAYLOADS = [
    "<script>",
    '"><img src=x onerror=alert(1)>',
    "javascript:alert(1)",
    "../../etc/passwd",
]

URL_PAYLOADS = [
    "javascript:alert(1)",
    "data:text/html,<script>alert(1)</script>",
    "vbscript:msgbox(1)",
    "file:///etc/passwd",
    "ftp://example.com/file",
    "//evil.example/path",
    "http://user:pass@example.com/",
    "https://93.184.216.34/%0d%0aX-Injected: 1",
    "https://93.184.216.34/\u202e",
    "https://93.184.216.34/\x00",
]


def test_titles_are_stored_as_inert_text_and_never_reflected_as_html() -> None:
    settings = security_settings()
    user = seed_user(settings)
    app: FastAPI = create_app(settings)
    app.dependency_overrides[get_current_user_optional] = lambda: CurrentUser(id=user)
    app.dependency_overrides[get_current_user] = lambda: CurrentUser(id=user)
    codes: list[str] = []

    try:
        with make_client(app, forwarded_for=unique_ip()) as client:
            for payload in TITLE_PAYLOADS:
                alias = f"x{uuid4().hex[:8]}"
                codes.append(alias)
                response = client.post(
                    "/api/v1/links",
                    json={
                        "url": "https://93.184.216.34/xss",
                        "alias": alias,
                        "title": payload,
                    },
                )
                assert response.status_code == 201, (payload, response.text)
                assert response.headers["content-type"].startswith("application/json")
                assert response.json()["title"] == payload

            listing = client.get("/api/v1/links", params={"limit": 50})
            assert listing.status_code == 200
            assert listing.headers["content-type"].startswith("application/json")
            stored = {item["code"]: item["title"] for item in listing.json()["items"]}
            for code in codes:
                assert stored[code] in TITLE_PAYLOADS

            for payload in ("\u202eRTL spoof", "bad\x00title"):
                rejected = client.post(
                    "/api/v1/links",
                    json={"url": "https://93.184.216.34/xss", "title": payload},
                )
                assert rejected.status_code == 400, (payload, rejected.text)
                assert rejected.json()["error"]["code"] == "invalid_title"

            oversized = client.post(
                "/api/v1/links",
                json={"url": "https://93.184.216.34/xss", "title": "a" * 121},
            )
            assert oversized.status_code == 422
    finally:
        cleanup(settings, codes=codes, user_ids=[user])


def test_alias_and_url_payloads_are_rejected() -> None:
    settings = security_settings()
    user = seed_user(settings)
    app: FastAPI = create_app(settings)
    app.dependency_overrides[get_current_user_optional] = lambda: CurrentUser(id=user)

    try:
        with make_client(app, forwarded_for=unique_ip()) as client:
            for payload in ALIAS_PAYLOADS:
                response = client.post(
                    "/api/v1/links",
                    json={"url": "https://93.184.216.34/x", "alias": payload},
                )
                assert response.status_code == 422, (payload, response.text)

            for payload in URL_PAYLOADS:
                response = client.post("/api/v1/links", json={"url": payload})
                assert response.status_code == 400, (payload, response.text)
                assert response.json()["error"]["code"] == "invalid_url"
    finally:
        cleanup(settings, codes=[], user_ids=[user])


def test_html_error_pages_do_not_reflect_the_requested_code() -> None:
    settings = security_settings()
    app = create_app(settings)
    payload = quote("<img src=x onerror=alert(1)>", safe="")

    with make_client(app, forwarded_for=unique_ip()) as client:
        response = client.get(f"/api/v1/r/{payload}", follow_redirects=False)

    assert response.status_code == 404
    assert response.headers["content-type"].startswith("text/html")
    assert "<img" not in response.text
    assert "onerror" not in response.text
    assert response.headers["x-content-type-options"] == "nosniff"
