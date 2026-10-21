from __future__ import annotations

from fastapi import Response

from tricolink.core.config import Settings
from tricolink.modules.identity.application.dto import AuthSession
from tricolink.modules.identity.application.tokens import generate_csrf_token


def set_session_cookies(
    response: Response,
    session: AuthSession,
    settings: Settings,
) -> str:
    response.set_cookie(
        key=settings.access_cookie_name,
        value=session.access_token,
        max_age=settings.access_token_ttl_min * 60,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        path="/",
        domain=settings.cookie_domain,
    )
    response.set_cookie(
        key=settings.refresh_cookie_name,
        value=session.refresh_token,
        max_age=settings.refresh_token_ttl_days * 86_400,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        path=settings.refresh_cookie_path,
        domain=settings.cookie_domain,
    )
    csrf_token = generate_csrf_token()
    set_csrf_cookie(response, csrf_token, settings)
    return csrf_token


def set_csrf_cookie(response: Response, token: str, settings: Settings) -> None:
    response.set_cookie(
        key=settings.csrf_cookie_name,
        value=token,
        max_age=settings.csrf_cookie_ttl_seconds,
        httponly=False,
        secure=settings.cookie_secure,
        samesite="lax",
        path="/",
        domain=settings.cookie_domain,
    )


def clear_session_cookies(response: Response, settings: Settings) -> None:
    for name, path in (
        (settings.access_cookie_name, "/"),
        (settings.refresh_cookie_name, settings.refresh_cookie_path),
        (settings.csrf_cookie_name, "/"),
    ):
        response.delete_cookie(
            key=name,
            path=path,
            domain=settings.cookie_domain,
            secure=settings.cookie_secure,
            httponly=name != settings.csrf_cookie_name,
            samesite="lax",
        )
