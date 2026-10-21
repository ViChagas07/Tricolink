import pytest
from fastapi.testclient import TestClient

from tricolink.core.config import Settings
from tricolink.main import create_app

pytestmark = pytest.mark.integration


def test_health_ready_checks_postgres_and_redis() -> None:
    with TestClient(create_app(Settings.from_env())) as client:
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "checks": {"postgres": "ok", "redis": "ok"},
    }
