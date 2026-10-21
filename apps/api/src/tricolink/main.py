from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from tricolink.core.config import Settings, get_settings
from tricolink.core.error_handlers import install_error_handlers
from tricolink.core.logging import configure_logging
from tricolink.core.middleware import (
    BodyLimitMiddleware,
    GlobalRateLimitMiddleware,
    MetricsMiddleware,
    RealIPMiddleware,
    RequestIDMiddleware,
    RequestTimeoutMiddleware,
    SecurityHeadersMiddleware,
)
from tricolink.core.services import Services, build_services
from tricolink.infra.observability.http import router as ops_router
from tricolink.modules.links.presentation import router as links_router


def create_app(
    settings: Settings | None = None,
    services: Services | None = None,
) -> FastAPI:
    current = settings or get_settings()
    current_services = services or build_services(current)
    configure_logging(current)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        configure_logging(current)
        await current_services.start()
        try:
            yield
        finally:
            await current_services.close()

    application = FastAPI(
        title="Tricolink API",
        version="0.1.0",
        docs_url="/docs" if current.docs_enabled else None,
        redoc_url=None,
        openapi_url="/openapi.json" if current.docs_enabled else None,
        lifespan=lifespan,
    )
    application.state.settings = current
    application.state.services = current_services
    application.state.rate_limiter = current_services.rate_limiter

    install_error_handlers(application)
    application.include_router(ops_router)
    application.include_router(links_router)

    application.add_middleware(
        BodyLimitMiddleware,
        max_body_bytes=current.max_body_bytes,
    )
    application.add_middleware(
        GlobalRateLimitMiddleware,
        limiter=current_services.rate_limiter,
    )
    application.add_middleware(
        RequestTimeoutMiddleware,
        timeout_seconds=current.request_timeout_seconds,
    )
    application.add_middleware(
        RealIPMiddleware,
        trusted_proxy_count=current.trusted_proxy_count,
    )
    application.add_middleware(MetricsMiddleware)
    application.add_middleware(
        SecurityHeadersMiddleware,
        is_production=current.is_production,
    )
    application.add_middleware(RequestIDMiddleware)
    return application


app = create_app()
