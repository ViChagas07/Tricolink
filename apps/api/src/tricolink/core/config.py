"""Application settings.

This module is the only place in the API allowed to read process environment
variables. Everything else receives a ``Settings`` instance.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

DEFAULT_DATABASE_URL = "postgresql+asyncpg://tricolink:tricolink@localhost:5432/tricolink"
DEFAULT_REDIS_URL = "redis://localhost:6379/0"

DEV_JWT_SECRET = "dev-insecure-jwt-secret-change-before-production-0001"
DEV_CSRF_SECRET = "dev-insecure-csrf-secret-change-before-production-0002"
DEV_SESSION_SECRET = "dev-insecure-session-secret-change-before-production-0003"
DEV_METRICS_TOKEN = "dev-insecure-metrics-token-change-before-production-0004"

_VALID_ENVIRONMENTS = frozenset({"development", "test", "staging", "production"})
_SECRET_FIELDS = ("jwt_secret", "csrf_secret", "session_secret", "metrics_token")
_MIN_SECRET_LENGTH = 32


class SettingsError(RuntimeError):
    """Raised when the environment is invalid or unsafe for the target environment."""


def _env(name: str) -> str | None:
    return os.getenv(name)


def _text(name: str, default: str | None = None) -> str | None:
    raw = _env(name)
    if raw is None:
        return default
    value = raw.strip()
    return value or None


def _text_or_empty(name: str, default: str) -> str:
    return _text(name, default) or ""


def _integer(name: str, default: int) -> int:
    raw = _env(name)
    if raw is None or not raw.strip():
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise SettingsError(f"{name} must be an integer") from exc


def _number(name: str, default: float) -> float:
    raw = _env(name)
    if raw is None or not raw.strip():
        return default
    try:
        return float(raw)
    except ValueError as exc:
        raise SettingsError(f"{name} must be a number") from exc


def _boolean(name: str, default: bool) -> bool:
    raw = _env(name)
    if raw is None or not raw.strip():
        return default
    value = raw.strip().lower()
    if value in {"1", "true", "yes", "on"}:
        return True
    if value in {"0", "false", "no", "off"}:
        return False
    raise SettingsError(f"{name} must be a boolean")


@dataclass(frozen=True, slots=True)
class Settings:
    app_env: str = "development"
    log_level: str = "INFO"

    database_url: str = DEFAULT_DATABASE_URL
    redis_url: str = DEFAULT_REDIS_URL

    frontend_origin: str = "http://localhost:3000"
    short_base_url: str = "http://localhost:3000"
    api_public_base_url: str = "http://localhost:8000"

    jwt_secret: str = DEV_JWT_SECRET
    jwt_algorithm: str = "HS256"
    access_token_ttl_min: int = 15
    refresh_token_ttl_days: int = 30
    csrf_secret: str = DEV_CSRF_SECRET
    session_secret: str = DEV_SESSION_SECRET
    cookie_secure: bool = False
    cookie_domain: str | None = None
    google_client_id: str | None = None
    google_client_secret: str | None = None
    google_redirect_uri: str | None = None

    trusted_proxy_count: int = 1

    cache_hard_ttl_seconds: int = 86_400
    cache_soft_ttl_seconds: int = 600
    cache_jitter_pct: float = 0.15
    negative_cache_ttl_seconds: int = 30
    lock_ttl_ms: int = 5_000
    cache_wait_timeout_seconds: float = 0.25

    dns_timeout_seconds: float = 2.0

    click_stream_key: str = "tl:clicks"
    click_stream_group: str = "tricolink-flusher"
    click_stream_maxlen: int = 100_000
    click_flush_batch_size: int = 500
    click_flush_block_ms: int = 1_000
    click_publish_timeout_seconds: float = 0.2
    click_flusher_enabled: bool = True

    anon_daily_link_limit: int = 5
    user_daily_link_limit: int = 100
    anon_link_ttl_days: int = 30

    rl_redirect_capacity: int = 120
    rl_redirect_refill_per_sec: float = 20.0
    rl_create_capacity: int = 10
    rl_create_refill_per_sec: float = 0.2
    rl_auth_capacity: int = 5
    rl_auth_refill_per_sec: float = 0.02
    rl_global_capacity: int = 2_000
    rl_global_refill_per_sec: float = 1_000.0
    rl_list_capacity: int = 60
    rl_list_refill_per_sec: float = 1.0

    max_body_bytes: int = 16_384
    request_timeout_seconds: float = 10.0

    sentry_dsn: str | None = None
    metrics_token: str = DEV_METRICS_TOKEN

    db_pool_size: int = 10
    db_max_overflow: int = 10
    db_pool_timeout_seconds: float = 5.0
    db_pool_recycle_seconds: int = 1_800
    db_connect_timeout_seconds: float = 5.0
    db_command_timeout_seconds: float = 10.0

    redis_pool_max_connections: int = 50
    redis_timeout_seconds: float = 2.0
    redis_connect_timeout_seconds: float = 2.0

    circuit_breaker_failure_threshold: int = 5
    circuit_breaker_recovery_timeout_seconds: float = 15.0
    circuit_breaker_half_open_max_calls: int = 1

    bulkhead_db_read: int = 20
    bulkhead_db_write: int = 10
    bulkhead_hashing: int = 4
    bulkhead_dns: int = 10
    bulkhead_acquire_timeout_seconds: float = 1.0

    def __post_init__(self) -> None:
        if self.app_env not in _VALID_ENVIRONMENTS:
            raise SettingsError(f"APP_ENV must be one of {sorted(_VALID_ENVIRONMENTS)}")
        if not self.database_url.startswith("postgresql+asyncpg://"):
            raise SettingsError("DATABASE_URL must use the postgresql+asyncpg driver")
        if not (self.redis_url.startswith("redis://") or self.redis_url.startswith("rediss://")):
            raise SettingsError("REDIS_URL must start with redis:// or rediss://")
        if self.trusted_proxy_count < 0:
            raise SettingsError("TRUSTED_PROXY_COUNT cannot be negative")
        if self.max_body_bytes < 1:
            raise SettingsError("MAX_BODY_BYTES must be positive")
        if self.request_timeout_seconds <= 0:
            raise SettingsError("REQUEST_TIMEOUT_SECONDS must be positive")

        positive_integers = {
            "CACHE_HARD_TTL_SECONDS": self.cache_hard_ttl_seconds,
            "CACHE_SOFT_TTL_SECONDS": self.cache_soft_ttl_seconds,
            "NEGATIVE_CACHE_TTL_SECONDS": self.negative_cache_ttl_seconds,
            "LOCK_TTL_MS": self.lock_ttl_ms,
            "ACCESS_TOKEN_TTL_MIN": self.access_token_ttl_min,
            "REFRESH_TOKEN_TTL_DAYS": self.refresh_token_ttl_days,
            "RL_REDIRECT_CAPACITY": self.rl_redirect_capacity,
            "RL_CREATE_CAPACITY": self.rl_create_capacity,
            "RL_AUTH_CAPACITY": self.rl_auth_capacity,
            "RL_GLOBAL_CAPACITY": self.rl_global_capacity,
            "RL_LIST_CAPACITY": self.rl_list_capacity,
            "DB_POOL_SIZE": self.db_pool_size,
            "REDIS_POOL_MAX_CONNECTIONS": self.redis_pool_max_connections,
            "CIRCUIT_BREAKER_FAILURE_THRESHOLD": self.circuit_breaker_failure_threshold,
            "BULKHEAD_DB_READ": self.bulkhead_db_read,
            "BULKHEAD_DB_WRITE": self.bulkhead_db_write,
            "BULKHEAD_HASHING": self.bulkhead_hashing,
            "BULKHEAD_DNS": self.bulkhead_dns,
            "CLICK_STREAM_MAXLEN": self.click_stream_maxlen,
            "CLICK_FLUSH_BATCH_SIZE": self.click_flush_batch_size,
            "CLICK_FLUSH_BLOCK_MS": self.click_flush_block_ms,
        }
        for name, value in positive_integers.items():
            if value < 1:
                raise SettingsError(f"{name} must be at least 1")

        non_negative_numbers = {
            "CACHE_JITTER_PCT": self.cache_jitter_pct,
            "RL_REDIRECT_REFILL_PER_SEC": self.rl_redirect_refill_per_sec,
            "RL_CREATE_REFILL_PER_SEC": self.rl_create_refill_per_sec,
            "RL_AUTH_REFILL_PER_SEC": self.rl_auth_refill_per_sec,
            "RL_GLOBAL_REFILL_PER_SEC": self.rl_global_refill_per_sec,
            "RL_LIST_REFILL_PER_SEC": self.rl_list_refill_per_sec,
        }
        for name, number_value in non_negative_numbers.items():
            if number_value < 0:
                raise SettingsError(f"{name} cannot be negative")

        positive_numbers = {
            "DB_POOL_TIMEOUT_SECONDS": self.db_pool_timeout_seconds,
            "DB_CONNECT_TIMEOUT_SECONDS": self.db_connect_timeout_seconds,
            "DB_COMMAND_TIMEOUT_SECONDS": self.db_command_timeout_seconds,
            "REDIS_TIMEOUT_SECONDS": self.redis_timeout_seconds,
            "REDIS_CONNECT_TIMEOUT_SECONDS": self.redis_connect_timeout_seconds,
            "CIRCUIT_BREAKER_RECOVERY_TIMEOUT_SECONDS": (
                self.circuit_breaker_recovery_timeout_seconds
            ),
            "BULKHEAD_ACQUIRE_TIMEOUT_SECONDS": self.bulkhead_acquire_timeout_seconds,
            "CACHE_WAIT_TIMEOUT_SECONDS": self.cache_wait_timeout_seconds,
            "DNS_TIMEOUT_SECONDS": self.dns_timeout_seconds,
            "CLICK_PUBLISH_TIMEOUT_SECONDS": self.click_publish_timeout_seconds,
        }
        for name, positive_value in positive_numbers.items():
            if positive_value <= 0:
                raise SettingsError(f"{name} must be positive")

        if self.db_max_overflow < 0:
            raise SettingsError("DB_MAX_OVERFLOW cannot be negative")
        if self.anon_link_ttl_days < 1:
            raise SettingsError("ANON_LINK_TTL_DAYS must be at least 1")
        if self.cache_soft_ttl_seconds > self.cache_hard_ttl_seconds:
            raise SettingsError("CACHE_SOFT_TTL_SECONDS cannot exceed CACHE_HARD_TTL_SECONDS")

        if self.app_env == "production":
            self._validate_production()

    @property
    def docs_enabled(self) -> bool:
        return self.app_env != "production"

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    def _validate_production(self) -> None:
        for field in _SECRET_FIELDS:
            value: str = getattr(self, field)
            if not value or len(value) < _MIN_SECRET_LENGTH:
                raise SettingsError(
                    f"{field.upper()} must be set with at least {_MIN_SECRET_LENGTH} characters "
                    "in production"
                )
            if value.startswith("dev-insecure-") or "change-me" in value:
                raise SettingsError(f"{field.upper()} still contains a development placeholder")
        if not self.cookie_secure:
            raise SettingsError("COOKIE_SECURE must be true in production")
        if self.google_client_id and not self.google_client_secret:
            raise SettingsError("GOOGLE_CLIENT_SECRET is required when GOOGLE_CLIENT_ID is set")
        if self.google_client_secret and not self.google_client_id:
            raise SettingsError("GOOGLE_CLIENT_ID is required when GOOGLE_CLIENT_SECRET is set")

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            app_env=_text("APP_ENV", "development") or "development",
            log_level=_text("LOG_LEVEL", "INFO") or "INFO",
            database_url=_text("DATABASE_URL", DEFAULT_DATABASE_URL) or DEFAULT_DATABASE_URL,
            redis_url=_text("REDIS_URL", DEFAULT_REDIS_URL) or DEFAULT_REDIS_URL,
            frontend_origin=_text("FRONTEND_ORIGIN", "http://localhost:3000")
            or "http://localhost:3000",
            short_base_url=_text("SHORT_BASE_URL", "http://localhost:3000")
            or "http://localhost:3000",
            api_public_base_url=_text("API_PUBLIC_BASE_URL", "http://localhost:8000")
            or "http://localhost:8000",
            jwt_secret=_text_or_empty("JWT_SECRET", DEV_JWT_SECRET),
            jwt_algorithm=_text("JWT_ALGORITHM", "HS256") or "HS256",
            access_token_ttl_min=_integer("ACCESS_TOKEN_TTL_MIN", 15),
            refresh_token_ttl_days=_integer("REFRESH_TOKEN_TTL_DAYS", 30),
            csrf_secret=_text_or_empty("CSRF_SECRET", DEV_CSRF_SECRET),
            session_secret=_text_or_empty("SESSION_SECRET", DEV_SESSION_SECRET),
            cookie_secure=_boolean("COOKIE_SECURE", False),
            cookie_domain=_text("COOKIE_DOMAIN"),
            google_client_id=_text("GOOGLE_CLIENT_ID"),
            google_client_secret=_text("GOOGLE_CLIENT_SECRET"),
            google_redirect_uri=_text("GOOGLE_REDIRECT_URI"),
            trusted_proxy_count=_integer("TRUSTED_PROXY_COUNT", 1),
            cache_hard_ttl_seconds=_integer("CACHE_HARD_TTL_SECONDS", 86_400),
            cache_soft_ttl_seconds=_integer("CACHE_SOFT_TTL_SECONDS", 600),
            cache_jitter_pct=_number("CACHE_JITTER_PCT", 0.15),
            negative_cache_ttl_seconds=_integer("NEGATIVE_CACHE_TTL_SECONDS", 30),
            lock_ttl_ms=_integer("LOCK_TTL_MS", 5_000),
            cache_wait_timeout_seconds=_number("CACHE_WAIT_TIMEOUT_SECONDS", 0.25),
            dns_timeout_seconds=_number("DNS_TIMEOUT_SECONDS", 2.0),
            click_stream_key=_text("CLICK_STREAM_KEY", "tl:clicks") or "tl:clicks",
            click_stream_group=_text("CLICK_STREAM_GROUP", "tricolink-flusher")
            or "tricolink-flusher",
            click_stream_maxlen=_integer("CLICK_STREAM_MAXLEN", 100_000),
            click_flush_batch_size=_integer("CLICK_FLUSH_BATCH_SIZE", 500),
            click_flush_block_ms=_integer("CLICK_FLUSH_BLOCK_MS", 1_000),
            click_publish_timeout_seconds=_number("CLICK_PUBLISH_TIMEOUT_SECONDS", 0.2),
            click_flusher_enabled=_boolean("CLICK_FLUSHER_ENABLED", True),
            anon_daily_link_limit=_integer("ANON_DAILY_LINK_LIMIT", 5),
            user_daily_link_limit=_integer("USER_DAILY_LINK_LIMIT", 100),
            anon_link_ttl_days=_integer("ANON_LINK_TTL_DAYS", 30),
            rl_redirect_capacity=_integer("RL_REDIRECT_CAPACITY", 120),
            rl_redirect_refill_per_sec=_number("RL_REDIRECT_REFILL_PER_SEC", 20.0),
            rl_create_capacity=_integer("RL_CREATE_CAPACITY", 10),
            rl_create_refill_per_sec=_number("RL_CREATE_REFILL_PER_SEC", 0.2),
            rl_auth_capacity=_integer("RL_AUTH_CAPACITY", 5),
            rl_auth_refill_per_sec=_number("RL_AUTH_REFILL_PER_SEC", 0.02),
            rl_global_capacity=_integer("RL_GLOBAL_CAPACITY", 2_000),
            rl_global_refill_per_sec=_number("RL_GLOBAL_REFILL_PER_SEC", 1_000.0),
            rl_list_capacity=_integer("RL_LIST_CAPACITY", 60),
            rl_list_refill_per_sec=_number("RL_LIST_REFILL_PER_SEC", 1.0),
            max_body_bytes=_integer("MAX_BODY_BYTES", 16_384),
            request_timeout_seconds=_number("REQUEST_TIMEOUT_SECONDS", 10.0),
            sentry_dsn=_text("SENTRY_DSN"),
            metrics_token=_text_or_empty("METRICS_TOKEN", DEV_METRICS_TOKEN),
            db_pool_size=_integer("DB_POOL_SIZE", 10),
            db_max_overflow=_integer("DB_MAX_OVERFLOW", 10),
            db_pool_timeout_seconds=_number("DB_POOL_TIMEOUT_SECONDS", 5.0),
            db_pool_recycle_seconds=_integer("DB_POOL_RECYCLE_SECONDS", 1_800),
            db_connect_timeout_seconds=_number("DB_CONNECT_TIMEOUT_SECONDS", 5.0),
            db_command_timeout_seconds=_number("DB_COMMAND_TIMEOUT_SECONDS", 10.0),
            redis_pool_max_connections=_integer("REDIS_POOL_MAX_CONNECTIONS", 50),
            redis_timeout_seconds=_number("REDIS_TIMEOUT_SECONDS", 2.0),
            redis_connect_timeout_seconds=_number("REDIS_CONNECT_TIMEOUT_SECONDS", 2.0),
            circuit_breaker_failure_threshold=_integer("CIRCUIT_BREAKER_FAILURE_THRESHOLD", 5),
            circuit_breaker_recovery_timeout_seconds=_number(
                "CIRCUIT_BREAKER_RECOVERY_TIMEOUT_SECONDS", 15.0
            ),
            circuit_breaker_half_open_max_calls=_integer("CIRCUIT_BREAKER_HALF_OPEN_MAX_CALLS", 1),
            bulkhead_db_read=_integer("BULKHEAD_DB_READ", 20),
            bulkhead_db_write=_integer("BULKHEAD_DB_WRITE", 10),
            bulkhead_hashing=_integer("BULKHEAD_HASHING", 4),
            bulkhead_dns=_integer("BULKHEAD_DNS", 10),
            bulkhead_acquire_timeout_seconds=_number("BULKHEAD_ACQUIRE_TIMEOUT_SECONDS", 1.0),
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings.from_env()
