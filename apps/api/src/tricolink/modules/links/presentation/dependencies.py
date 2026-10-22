from __future__ import annotations

import math

from fastapi import Depends, Request, Response

from tricolink.core.deps import (
    CurrentUser,
    get_current_user_optional,
    get_services,
)
from tricolink.infra.ratelimit.dependencies import apply_rate_limit_headers, client_ip
from tricolink.infra.ratelimit.models import RateLimitResult
from tricolink.modules.analytics.adapters import RedisClickPublisher
from tricolink.modules.links.application import (
    CreateLink,
    DeleteLink,
    GetLink,
    GetLinksOverview,
    ListLinks,
    RecordClick,
    ResolveLink,
    UpdateLink,
)
from tricolink.shared_kernel.security_errors import RateLimitExceeded


def get_create_link(request: Request) -> CreateLink:
    return get_services(request).links.create_link


def get_get_link(request: Request) -> GetLink:
    return get_services(request).links.get_link


def get_list_links(request: Request) -> ListLinks:
    return get_services(request).links.list_links


def get_links_overview(request: Request) -> GetLinksOverview:
    return get_services(request).links.get_overview


def get_update_link(request: Request) -> UpdateLink:
    return get_services(request).links.update_link


def get_delete_link(request: Request) -> DeleteLink:
    return get_services(request).links.delete_link


def get_resolve_link(request: Request) -> ResolveLink:
    return get_services(request).links.resolve_link


def get_record_click(request: Request) -> RecordClick:
    return get_services(request).record_click


def get_click_publisher(request: Request) -> RedisClickPublisher:
    return get_services(request).analytics.publisher


async def create_link_rate_limit(
    request: Request,
    response: Response,
    user: CurrentUser | None = Depends(get_current_user_optional),
) -> None:
    limiter = get_services(request).rate_limiter
    results = [await limiter.check("create", client_ip(request))]
    if user is not None:
        results.append(await limiter.check("create", f"user:{user.id}"))

    result = _most_restrictive(results)
    apply_rate_limit_headers(response, result)
    if any(not item.allowed for item in results):
        raise _rate_limit_error(result)


def _most_restrictive(results: list[RateLimitResult]) -> RateLimitResult:
    return min(results, key=lambda result: (result.allowed, result.remaining))


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
