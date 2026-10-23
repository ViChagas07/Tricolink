from __future__ import annotations

import asyncio
import secrets
from typing import Literal

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from pydantic import BaseModel

from tricolink.core.logging import get_logger
from tricolink.core.services import Services
from tricolink.shared_kernel.security_errors import MetricsAuthenticationError

logger = get_logger("tricolink.ops")

router = APIRouter(tags=["ops"])


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"


@router.get("/health/live", response_model=HealthResponse)
async def health_live() -> HealthResponse:
    return HealthResponse()


@router.get("/health/ready")
async def health_ready(request: Request) -> JSONResponse:
    services: Services = request.app.state.services
    database_ok, redis_ok = await asyncio.gather(
        _check_database(services),
        _check_redis(services),
    )
    ready = database_ok and redis_ok
    return JSONResponse(
        status_code=200 if ready else 503,
        content={
            "status": "ready" if ready else "not_ready",
            "checks": {
                "postgres": "ok" if database_ok else "error",
                "redis": "ok" if redis_ok else "error",
            },
        },
    )


@router.get("/metrics")
async def metrics(request: Request) -> Response:
    services: Services = request.app.state.services
    if not services.settings.metrics_enabled:
        return Response(status_code=404)
    expected_token = services.settings.metrics_token
    if not _authorized(request, expected_token):
        raise MetricsAuthenticationError()
    return Response(
        content=generate_latest(),
        headers={"Content-Type": CONTENT_TYPE_LATEST},
    )


def _authorized(request: Request, expected_token: str | None) -> bool:
    if not expected_token:
        return False
    header = request.headers.get("authorization", "")
    scheme, separator, token = header.partition(" ")
    if not separator or scheme.lower() != "bearer" or not token:
        return False
    return secrets.compare_digest(token, expected_token)


async def _check_database(services: Services) -> bool:
    try:
        async with asyncio.timeout(services.settings.db_connect_timeout_seconds):
            await services.database.ping()
    except Exception as exc:
        logger.warning("readiness_database_failed", error_type=type(exc).__name__)
        return False
    return True


async def _check_redis(services: Services) -> bool:
    try:
        await services.redis_ping()
    except Exception as exc:
        logger.warning("readiness_redis_failed", error_type=type(exc).__name__)
        return False
    return True
