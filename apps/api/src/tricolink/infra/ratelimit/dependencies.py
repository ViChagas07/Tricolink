from __future__ import annotations

import math
from collections.abc import Awaitable, Callable
from typing import cast

from fastapi import Request, Response

from tricolink.infra.ratelimit.models import RateLimitResult
from tricolink.infra.ratelimit.service import RateLimiter
from tricolink.shared_kernel.security_errors import RateLimitExceeded


def client_ip(request: Request) -> str:
    if request.client is None:
        return "unknown"
    return request.client.host


def _get_limiter(request: Request) -> RateLimiter:
    return cast(RateLimiter, request.app.state.rate_limiter)


def apply_rate_limit_headers(response: Response, result: RateLimitResult) -> None:
    response.headers["RateLimit-Limit"] = str(result.limit)
    response.headers["RateLimit-Remaining"] = str(result.remaining)
    response.headers["RateLimit-Reset"] = str(max(0, result.reset_after_seconds))


def _retry_after_seconds(result: RateLimitResult) -> int:
    if result.retry_after_ms >= 0:
        return max(1, math.ceil(result.retry_after_ms / 1000))
    if result.reset_after_seconds > 0:
        return result.reset_after_seconds
    return 60


def rate_limit(
    scope: str,
    *,
    cost: int = 1,
    key_func: Callable[[Request], str] | None = None,
) -> Callable[[Request, Response], Awaitable[None]]:
    """Build a FastAPI dependency for one rate limit bucket."""

    async def dependency(request: Request, response: Response) -> None:
        limiter = _get_limiter(request)
        key = key_func(request) if key_func is not None else client_ip(request)
        result = await limiter.check(scope, key, cost)
        apply_rate_limit_headers(response, result)
        if not result.allowed:
            raise RateLimitExceeded(
                retry_after_seconds=_retry_after_seconds(result),
                limit=result.limit,
                remaining=result.remaining,
                reset_after_seconds=result.reset_after_seconds,
            )

    return dependency
