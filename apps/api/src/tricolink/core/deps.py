from __future__ import annotations

from collections.abc import AsyncIterator
from typing import cast

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from tricolink.core.config import Settings
from tricolink.core.services import Services
from tricolink.infra.cache import CacheClient
from tricolink.infra.ratelimit import RateLimiter


def settings_dependency(request: Request) -> Settings:
    return get_services(request).settings


def get_services(request: Request) -> Services:
    return cast(Services, request.app.state.services)


def get_cache(request: Request) -> CacheClient:
    return get_services(request).cache


def get_rate_limiter(request: Request) -> RateLimiter:
    return get_services(request).rate_limiter


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    async with get_services(request).database.session_factory() as session:
        yield session
