from __future__ import annotations

import math
from collections.abc import AsyncIterator, Awaitable, Callable
from dataclasses import dataclass
from typing import cast
from uuid import UUID

from fastapi import Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from tricolink.core.config import Settings
from tricolink.core.services import Services
from tricolink.infra.cache import CacheClient
from tricolink.infra.ratelimit import RateLimiter
from tricolink.infra.ratelimit.dependencies import apply_rate_limit_headers
from tricolink.infra.ratelimit.models import RateLimitResult
from tricolink.shared_kernel.security_errors import AuthenticationError, RateLimitExceeded


@dataclass(frozen=True, slots=True)
class CurrentUser:
    id: UUID
    email: str | None = None
    display_name: str | None = None
    locale: str | None = None


def settings_dependency(request: Request) -> Settings:
    return get_services(request).settings


def get_services(request: Request) -> Services:
    return cast(Services, request.app.state.services)


def get_cache(request: Request) -> CacheClient:
    return get_services(request).cache


def get_rate_limiter(request: Request) -> RateLimiter:
    return get_services(request).rate_limiter


async def get_current_user_optional(request: Request) -> CurrentUser | None:
    services = get_services(request)
    token = request.cookies.get(services.settings.access_cookie_name)
    if not token:
        return None
    user = await services.identity.authenticate_access.execute(token)
    if user is None:
        return None
    return CurrentUser(
        id=user.id,
        email=user.email.value,
        display_name=user.display_name,
        locale=user.locale,
    )


async def get_current_user(
    user: CurrentUser | None = Depends(get_current_user_optional),
) -> CurrentUser:
    if user is None:
        raise AuthenticationError()
    return user


def user_rate_limit(scope: str) -> Callable[..., Awaitable[None]]:
    async def dependency(
        request: Request,
        response: Response,
        user: CurrentUser = Depends(get_current_user),
    ) -> None:
        limiter = get_services(request).rate_limiter
        result = await limiter.check(scope, f"user:{user.id}")
        apply_rate_limit_headers(response, result)
        if not result.allowed:
            raise _rate_limit_error(result)

    return dependency


def _rate_limit_error(result: RateLimitResult) -> RateLimitExceeded:
    retry_after = (
        max(1, math.ceil(result.retry_after_ms / 1000))
        if result.retry_after_ms >= 0
        else max(1, result.reset_after_seconds)
    )
    return RateLimitExceeded(
        retry_after_seconds=retry_after,
        limit=result.limit,
        remaining=result.remaining,
        reset_after_seconds=result.reset_after_seconds,
    )


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    async with get_services(request).database.session_factory() as session:
        yield session
