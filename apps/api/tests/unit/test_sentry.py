from __future__ import annotations

import pytest

from tricolink.core.config import Settings
from tricolink.infra.observability import sentry


def test_sentry_is_disabled_without_a_dsn(monkeypatch: pytest.MonkeyPatch) -> None:
    called = False

    def fake_init(**_: object) -> None:
        nonlocal called
        called = True

    monkeypatch.setattr(sentry.sentry_sdk, "init", fake_init)

    assert sentry.init_sentry(Settings()) is False
    assert called is False


def test_sentry_scrubs_request_data_and_disables_pii(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def fake_init(**kwargs: object) -> None:
        captured.update(kwargs)

    monkeypatch.setattr(sentry.sentry_sdk, "init", fake_init)

    assert sentry.init_sentry(Settings(sentry_dsn="https://key@sentry.example/1")) is True
    assert captured["dsn"] == "https://key@sentry.example/1"
    assert captured["send_default_pii"] is False
    assert captured["traces_sample_rate"] == 0.0

    before_send = captured["before_send"]
    assert callable(before_send)
    event = {
        "request": {
            "headers": {"Authorization": "Bearer secret"},
            "cookies": {"tl_access": "secret"},
            "data": {"password": "secret"},
        }
    }
    cleaned = before_send(event, {})
    assert cleaned["request"] == {}
