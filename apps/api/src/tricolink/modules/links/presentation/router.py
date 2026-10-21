from __future__ import annotations

from typing import cast

from fastapi import APIRouter, Depends, Query, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse

from tricolink.core.config import Settings
from tricolink.core.deps import (
    CurrentUser,
    get_current_user,
    get_current_user_optional,
    settings_dependency,
)
from tricolink.infra.ratelimit import client_ip, rate_limit
from tricolink.modules.links.application import (
    UNSET,
    CreateLink,
    CreateLinkCommand,
    DeleteLink,
    GetLink,
    LinkPage,
    ListLinks,
    RecordClick,
    ResolvedLink,
    ResolveLink,
    UpdateLink,
    UpdateLinkCommand,
)
from tricolink.modules.links.domain.entities import Link, LinkState
from tricolink.modules.links.presentation.dependencies import (
    create_link_rate_limit,
    get_create_link,
    get_delete_link,
    get_get_link,
    get_list_links,
    get_record_click,
    get_resolve_link,
    get_update_link,
    user_rate_limit,
)
from tricolink.modules.links.presentation.schemas import (
    CreateLinkRequest,
    LinkResponse,
    ListLinksResponse,
    UpdateLinkRequest,
)

router = APIRouter(prefix="/api/v1", tags=["links"])

_NOT_FOUND_HTML = b"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Link not found</title></head>
<body><main><h1>Link not found</h1><p>This short link does not exist.</p></main></body></html>
"""
_GONE_HTML = b"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Link unavailable</title></head>
<body><main><h1>Link unavailable</h1>
<p>This short link expired or was disabled.</p></main></body></html>
"""


@router.post("/links", response_model=LinkResponse, status_code=status.HTTP_201_CREATED)
async def create_link(
    payload: CreateLinkRequest,
    request: Request,
    current_user: CurrentUser | None = Depends(get_current_user_optional),
    use_case: CreateLink = Depends(get_create_link),
    settings: Settings = Depends(settings_dependency),
    _: None = Depends(create_link_rate_limit),
) -> LinkResponse:
    link = await use_case.execute(
        CreateLinkCommand(
            url=payload.url,
            user_id=current_user.id if current_user else None,
            client_ip=client_ip(request),
            alias=payload.alias,
            title=payload.title,
            expires_at=payload.expires_at,
        )
    )
    return _link_response(link, settings)


@router.get("/links", response_model=ListLinksResponse)
async def list_links(
    current_user: CurrentUser = Depends(get_current_user),
    use_case: ListLinks = Depends(get_list_links),
    settings: Settings = Depends(settings_dependency),
    limit: int = Query(default=20, ge=1, le=50),
    cursor: str | None = Query(default=None, max_length=256),
    q: str | None = Query(default=None, max_length=100),
    _: None = Depends(user_rate_limit("stats_list")),
) -> ListLinksResponse:
    page: LinkPage = await use_case.execute(
        user_id=current_user.id,
        cursor=cursor,
        limit=limit,
        query=q,
    )
    return ListLinksResponse(
        items=[_link_response(link, settings) for link in page.items],
        next_cursor=page.next_cursor,
    )


@router.get("/links/{code}", response_model=LinkResponse)
async def get_link(
    code: str,
    current_user: CurrentUser = Depends(get_current_user),
    use_case: GetLink = Depends(get_get_link),
    settings: Settings = Depends(settings_dependency),
    _: None = Depends(user_rate_limit("stats_list")),
) -> LinkResponse:
    link = await use_case.execute(code, current_user.id)
    return _link_response(link, settings)


@router.patch("/links/{code}", response_model=LinkResponse)
async def update_link(
    code: str,
    payload: UpdateLinkRequest,
    current_user: CurrentUser = Depends(get_current_user),
    use_case: UpdateLink = Depends(get_update_link),
    settings: Settings = Depends(settings_dependency),
    _: None = Depends(user_rate_limit("stats_list")),
) -> LinkResponse:
    fields = payload.model_fields_set
    command = UpdateLinkCommand(
        code=code,
        user_id=current_user.id,
        title=payload.title if "title" in fields else UNSET,
        original_url=(cast(str, payload.original_url) if "original_url" in fields else UNSET),
        expires_at=payload.expires_at if "expires_at" in fields else UNSET,
        is_active=cast(bool, payload.is_active) if "is_active" in fields else UNSET,
    )
    link = await use_case.execute(command)
    return _link_response(link, settings)


@router.delete("/links/{code}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_link(
    code: str,
    current_user: CurrentUser = Depends(get_current_user),
    use_case: DeleteLink = Depends(get_delete_link),
    _: None = Depends(user_rate_limit("stats_list")),
) -> Response:
    await use_case.execute(code, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/r/{code}", dependencies=[Depends(rate_limit("redirect"))])
async def redirect_link(
    code: str,
    request: Request,
    response: Response,
    resolve: ResolveLink = Depends(get_resolve_link),
    record_click: RecordClick = Depends(get_record_click),
) -> Response:
    resolved: ResolvedLink | None = await resolve.execute(code)
    if resolved is None:
        return _static_html(404, _NOT_FOUND_HTML)
    if resolved.state is not LinkState.ACTIVE:
        return _static_html(410, _GONE_HTML)

    await record_click.execute(
        link_id=resolved.link_id,
        user_agent=request.headers.get("user-agent"),
        country=request.headers.get("x-vercel-ip-country") or request.headers.get("cf-ipcountry"),
        referrer=request.headers.get("referer"),
    )

    redirect = RedirectResponse(
        url=resolved.original_url,
        status_code=302,
        headers={
            "X-Robots-Tag": "noindex, nofollow",
            "Cache-Control": "no-store",
        },
    )
    for name, value in response.headers.items():
        redirect.headers.setdefault(name, value)
    return redirect


def _static_html(status_code: int, body: bytes) -> HTMLResponse:
    return HTMLResponse(
        content=body,
        status_code=status_code,
        headers={
            "X-Robots-Tag": "noindex, nofollow",
            "Cache-Control": "no-store",
        },
    )


def _link_response(link: Link, settings: Settings) -> LinkResponse:
    short_base = settings.short_base_url.rstrip("/")
    return LinkResponse(
        code=link.code.value,
        short_url=f"{short_base}/{link.code.value}",
        original_url=link.original_url.value,
        title=link.title,
        created_at=link.created_at,
        expires_at=link.expires_at,
        is_active=link.is_active,
        click_count=link.click_count,
    )
