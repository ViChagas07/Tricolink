from __future__ import annotations

import json

import pytest

from tricolink.core.deps import CurrentUser, get_current_user
from tricolink.main import create_app

from .helpers import (
    cleanup,
    make_client,
    security_settings,
    seed_user,
    unique_ip,
)

pytestmark = pytest.mark.integration


def test_deeply_nested_json_is_rejected_without_server_error() -> None:
    settings = security_settings()
    app = create_app(settings)
    payload = json.dumps({"url": "https://93.184.216.34/x", "x": [[[[0]]]]})

    with make_client(app, forwarded_for=unique_ip()) as client:
        response = client.post(
            "/api/v1/links",
            content=payload.replace("[[[[0]]]]", "[" * 2000 + "0" + "]" * 2000),
            headers={"Content-Type": "application/json"},
        )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "bad_request"
    assert response.status_code != 500


def test_oversized_body_is_rejected_before_it_is_parsed() -> None:
    settings = security_settings()
    app = create_app(settings)
    body = b'{"url":"https://93.184.216.34/x","title":"' + b"a" * 20_000 + b'"}'

    with make_client(app, forwarded_for=unique_ip()) as client:
        response = client.post(
            "/api/v1/links",
            content=body,
            headers={"Content-Type": "application/json"},
        )

    assert response.status_code == 413
    assert response.json()["error"]["code"] == "payload_too_large"


def test_field_and_page_limits_are_enforced() -> None:
    settings = security_settings()
    user = seed_user(settings)
    app = create_app(settings)
    app.dependency_overrides[get_current_user] = lambda: CurrentUser(id=user)

    try:
        with make_client(app, forwarded_for=unique_ip()) as client:
            title = client.post(
                "/api/v1/links",
                json={"url": "https://93.184.216.34/x", "title": "a" * 121},
            )
            query = client.get("/api/v1/links", params={"q": "a" * 101})
            limit = client.get("/api/v1/links", params={"limit": 51})
            url = client.post(
                "/api/v1/links",
                json={"url": "https://93.184.216.34/" + "a" * 2_049},
            )

        assert title.status_code == 422
        assert query.status_code == 422
        assert limit.status_code == 422
        assert url.status_code == 422
    finally:
        cleanup(settings, codes=[], user_ids=[user])
