from __future__ import annotations

import secrets
import unicodedata
from urllib.parse import unquote, urlsplit

from fastapi import Request

from tricolink.core.config import Settings
from tricolink.core.deps import get_services
from tricolink.modules.identity.application.errors import InvalidNextPath
from tricolink.shared_kernel.security_errors import CsrfError

_MUTATING_METHODS = frozenset({"POST", "PATCH", "DELETE", "PUT"})


def allowed_origins(settings: Settings) -> frozenset[str]:
    origins: set[str] = set()
    for value in (
        settings.frontend_origin,
        settings.api_public_base_url,
        settings.short_base_url,
    ):
        try:
            parts = urlsplit(value)
        except ValueError:
            continue
        if parts.scheme and parts.netloc:
            origins.add(f"{parts.scheme.lower()}://{parts.netloc.lower()}")
    return frozenset(origins)


def validate_origin(
    request: Request,
    settings: Settings,
    *,
    required: bool,
) -> None:
    origin = request.headers.get("origin")
    sec_fetch_site = (request.headers.get("sec-fetch-site") or "").lower()

    if sec_fetch_site == "cross-site":
        raise CsrfError()

    if origin:
        normalized = origin.rstrip("/").lower()
        if normalized not in allowed_origins(settings):
            raise CsrfError()
        return

    if not required:
        return

    if sec_fetch_site not in {"same-origin", "same-site"}:
        raise CsrfError()


async def origin_guard(request: Request) -> None:
    validate_origin(request, get_services(request).settings, required=False)


async def csrf_protect(request: Request) -> None:
    if request.method.upper() not in _MUTATING_METHODS:
        return

    services = get_services(request)
    settings = services.settings
    has_auth_cookie = bool(
        request.cookies.get(settings.access_cookie_name)
        or request.cookies.get(settings.refresh_cookie_name)
    )
    if not has_auth_cookie:
        return

    validate_origin(request, settings, required=True)

    cookie = request.cookies.get(settings.csrf_cookie_name)
    header = request.headers.get("x-csrf-token")
    if not cookie or not header or not secrets.compare_digest(cookie, header):
        raise CsrfError()


def safe_next_path(value: str | None, *, default: str = "/account") -> str:
    if value is None or value == "":
        return default
    if not value.startswith("/") or value.startswith("//"):
        raise InvalidNextPath()

    decoded = unquote(value)
    if decoded.startswith("//") or "\\" in decoded:
        raise InvalidNextPath()
    if any(unicodedata.category(char)[0] == "C" for char in decoded):
        raise InvalidNextPath()

    try:
        parts = urlsplit(value)
    except ValueError as exc:
        raise InvalidNextPath() from exc
    if parts.scheme or parts.netloc:
        raise InvalidNextPath()
    return value


def frontend_url(settings: Settings, path: str) -> str:
    return settings.frontend_origin.rstrip("/") + path
