import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    app_env: str
    database_url: str
    redis_url: str
    frontend_origin: str


def get_settings() -> Settings:
    return Settings(
        app_env=os.getenv("APP_ENV", "development"),
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://tricolink:tricolink@localhost:5432/tricolink",
        ),
        redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        frontend_origin=os.getenv("FRONTEND_ORIGIN", "http://localhost:3000"),
    )
