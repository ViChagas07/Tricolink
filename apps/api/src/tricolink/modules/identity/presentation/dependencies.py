from __future__ import annotations

import math
from collections.abc import Awaitable, Callable

from fastapi import Depends, Request, Response

from tricolink.core.deps import CurrentUser, get_current_user, get_services
from tricolink.infra.ratelimit.dependencies import apply_rate_limit_headers
from tricolink.infra.ratelimit.models import RateLimitResult
from tricolink.modules.identity.adapters.google import GoogleOIDCClient
from tricolink.modules.identity.application import (
    AuthenticateAccess,
    GetMe,
    Login,
    LoginWithGoogle,
    Logout,
    RefreshSession,
    Register,
    UpdateMe,
)
from tricolink.shared_kernel.security_errors import RateLimitExceeded


def get_register(request: Request) -> Register:
    return get_services(request).identity.register


def get_login(request: Request) -> Login:
    return get_services(request).identity.login


def get_refresh_session(request: Request) -> RefreshSession:
    return get_services(request).identity.refresh_session


def get_logout(request: Request) -> Logout:
    return get_services(request).identity.logout


def get_get_me(request: Request) -> GetMe:
    return get_services(request).identity.get_me


def get_update_me(request: Request) -> UpdateMe:
    return get_services(request).identity.update_me


def get_google_login(request: Request) -> LoginWithGoogle:
    return get_services(request).identity.google_login


def get_authenticate_access(request: Request) -> AuthenticateAccess:
    return get_services(request).identity.authenticate_access


def get_google_oidc(request: Request) -> GoogleOIDCClient:
    return get_services(request).identity.google_oidc


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
