from fastapi.testclient import TestClient

from tricolink.core.config import Settings
from tricolink.main import create_app


def test_metrics_requires_token() -> None:
    settings = Settings(app_env="test", metrics_token="metrics-secret-token")
    with TestClient(create_app(settings)) as client:
        response = client.get("/metrics")

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "authentication_required"


def test_metrics_rejects_wrong_token() -> None:
    settings = Settings(app_env="test", metrics_token="metrics-secret-token")
    with TestClient(create_app(settings)) as client:
        response = client.get("/metrics", headers={"Authorization": "Bearer wrong"})

    assert response.status_code == 401


def test_metrics_accepts_valid_token() -> None:
    settings = Settings(app_env="test", metrics_token="metrics-secret-token")
    with TestClient(create_app(settings)) as client:
        response = client.get(
            "/metrics",
            headers={"Authorization": "Bearer metrics-secret-token"},
        )

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "tricolink_http_requests_total" in response.text
