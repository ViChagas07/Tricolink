from fastapi.testclient import TestClient

from tricolink.main import app


def test_health_live_returns_ok() -> None:
    with TestClient(app) as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
