from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

from tricolink.core.config import Settings, get_settings


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"


def create_app(settings: Settings | None = None) -> FastAPI:
    current = settings or get_settings()
    is_production = current.app_env == "production"

    application = FastAPI(
        title="Tricolink API",
        version="0.1.0",
        docs_url=None if is_production else "/docs",
        redoc_url=None,
        openapi_url=None if is_production else "/openapi.json",
    )

    @application.get("/health/live", response_model=HealthResponse, tags=["ops"])
    async def health_live() -> HealthResponse:
        return HealthResponse()

    return application


app = create_app()
