from dataclasses import replace

import pytest
from fastapi.testclient import TestClient

from tricolink.core.config import Settings
from tricolink.main import create_app

pytestmark = pytest.mark.integration


def test_health_ready_checks_postgres_and_redis() -> None:
    settings = replace(
        Settings.from_env(),
        click_flusher_enabled=False,
        click_stream_key="test:clicks:health",
    )
    with TestClient(create_app(settings)) as client:
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "checks": {"postgres": "ok", "redis": "ok"},
    }
