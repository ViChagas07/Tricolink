from fastapi.testclient import TestClient

from tricolink.core.config import Settings
from tricolink.main import create_app


def production_settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "app_env": "production",
        "cookie_secure": True,
        "jwt_secret": "j" * 48,
        "csrf_secret": "c" * 48,
        "session_secret": "s" * 48,
        "metrics_token": "m" * 48,
    }
    values.update(overrides)
    return Settings(**values)  # type: ignore[arg-type]


def test_docs_and_openapi_are_disabled_in_production() -> None:
    with TestClient(create_app(production_settings())) as client:
        docs = client.get("/docs")
        openapi = client.get("/openapi.json")

    assert docs.status_code == 404
    assert openapi.status_code == 404
    assert docs.json()["error"]["code"] == "not_found"


def test_body_limit_is_enforced_by_the_full_app() -> None:
    settings = Settings(app_env="test", max_body_bytes=128)
    with TestClient(create_app(settings)) as client:
        response = client.post("/health/live", content=b"x" * 129)

    assert response.status_code == 413
    assert response.json()["error"]["code"] == "payload_too_large"
