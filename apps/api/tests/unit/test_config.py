from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from tricolink.core.config import Settings, SettingsError, get_settings

API_ROOT = Path(__file__).resolve().parents[2]


def test_settings_are_immutable() -> None:
    settings = Settings()

    with pytest.raises(FrozenInstanceError):
        settings.max_body_bytes = 1  # type: ignore[misc]


def test_settings_parse_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("MAX_BODY_BYTES", "2048")
    monkeypatch.setenv("TRUSTED_PROXY_COUNT", "2")
    monkeypatch.setenv("REQUEST_TIMEOUT_SECONDS", "3.5")
    monkeypatch.setenv("RL_REDIRECT_CAPACITY", "77")
    monkeypatch.setenv("RL_REDIRECT_REFILL_PER_SEC", "0.75")
    monkeypatch.setenv("COOKIE_SECURE", "true")

    settings = Settings.from_env()

    assert settings.app_env == "test"
    assert settings.max_body_bytes == 2048
    assert settings.trusted_proxy_count == 2
    assert settings.request_timeout_seconds == 3.5
    assert settings.rl_redirect_capacity == 77
    assert settings.rl_redirect_refill_per_sec == 0.75
    assert settings.cookie_secure is True


def test_postgres_urls_are_normalized_for_asyncpg(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@db:5432/app")
    monkeypatch.setenv("MIGRATION_DATABASE_URL", "postgres://user:pass@db:5432/app")

    settings = Settings.from_env()

    assert settings.database_url == "postgresql+asyncpg://user:pass@db:5432/app"
    assert settings.migration_database_url == "postgresql+asyncpg://user:pass@db:5432/app"


def test_quoted_and_driver_specific_postgres_urls_are_normalized(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DATABASE_URL", '"postgresql://user:pass@db:5432/app"')
    monkeypatch.setenv("MIGRATION_DATABASE_URL", "'postgresql+psycopg://user:pass@db:5432/app'")

    settings = Settings.from_env()

    assert settings.database_url == "postgresql+asyncpg://user:pass@db:5432/app"
    assert settings.migration_database_url == "postgresql+asyncpg://user:pass@db:5432/app"


def test_misspelled_postgres_scheme_is_normalized(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresq+asyncpg://user:pass@db:5432/app")

    settings = Settings.from_env()

    assert settings.database_url == "postgresql+asyncpg://user:pass@db:5432/app"


def test_cleanup_retention_is_configurable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CLICK_RETENTION_DAYS", "30")
    monkeypatch.setenv("CLEANUP_BATCH_SIZE", "250")

    settings = Settings.from_env()

    assert settings.click_retention_days == 30
    assert settings.cleanup_batch_size == 250


def test_production_requires_real_secrets(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    for name in ("JWT_SECRET", "CSRF_SECRET", "SESSION_SECRET", "METRICS_TOKEN"):
        monkeypatch.delenv(name, raising=False)

    with pytest.raises(SettingsError):
        Settings.from_env()


def test_production_rejects_placeholder_secrets(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("COOKIE_SECURE", "true")
    monkeypatch.setenv("JWT_SECRET", "change-me-min-32-bytes-random")
    monkeypatch.setenv("CSRF_SECRET", "x" * 40)
    monkeypatch.setenv("SESSION_SECRET", "y" * 40)
    monkeypatch.setenv("METRICS_TOKEN", "z" * 40)

    with pytest.raises(SettingsError):
        Settings.from_env()


def test_production_accepts_strong_secrets(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("COOKIE_SECURE", "true")
    monkeypatch.setenv("JWT_SECRET", "j" * 48)
    monkeypatch.setenv("CSRF_SECRET", "c" * 48)
    monkeypatch.setenv("SESSION_SECRET", "s" * 48)
    monkeypatch.setenv("METRICS_TOKEN", "m" * 48)

    settings = Settings.from_env()

    assert settings.app_env == "production"
    assert settings.docs_enabled is False


def test_development_enables_docs() -> None:
    assert Settings(app_env="development").docs_enabled is True
    assert Settings(app_env="test").docs_enabled is True


def test_invalid_app_env_is_rejected() -> None:
    with pytest.raises(SettingsError):
        Settings(app_env="prod")


def test_negative_trusted_proxy_count_is_rejected() -> None:
    with pytest.raises(SettingsError):
        Settings(trusted_proxy_count=-1)


def test_only_config_module_reads_process_environment() -> None:
    offenders: list[str] = []
    for root in (API_ROOT / "src", API_ROOT / "alembic"):
        for path in root.rglob("*.py"):
            if path.name == "config.py":
                continue
            text = path.read_text(encoding="utf-8")
            if "os.getenv" in text or "os.environ" in text:
                offenders.append(str(path.relative_to(API_ROOT)))

    assert offenders == []


def test_get_settings_is_cached(monkeypatch: pytest.MonkeyPatch) -> None:
    get_settings.cache_clear()
    monkeypatch.setenv("MAX_BODY_BYTES", "1234")
    first = get_settings()
    monkeypatch.setenv("MAX_BODY_BYTES", "9999")
    second = get_settings()
    get_settings.cache_clear()

    assert first is second
    assert second.max_body_bytes == 1234
