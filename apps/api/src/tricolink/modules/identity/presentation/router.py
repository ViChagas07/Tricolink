from __future__ import annotations

import secrets
from urllib.parse import parse_qs, urlsplit

from fastapi import APIRouter, Depends, Query, Request, Response, status
from fastapi.responses import RedirectResponse

from tricolink.core.config import Settings
from tricolink.core.deps import CurrentUser, get_current_user, user_rate_limit
from tricolink.core.logging import get_logger
from tricolink.infra.ratelimit import rate_limit
from tricolink.modules.identity.adapters.google import GoogleOIDCClient
from tricolink.modules.identity.application import (
    GetMe,
    Login,
    LoginCommand,
    LoginWithGoogle,
    Logout,
    RefreshSession,
    Register,
    RegisterCommand,
    UpdateMe,
    UpdateMeCommand,
)
from tricolink.modules.identity.application.errors import (
    GoogleNotConfigured,
    InvalidGoogleLogin,
    InvalidNextPath,
)
from tricolink.modules.identity.domain.entities import User
from tricolink.modules.identity.domain.google import validate_google_claims
from tricolink.modules.identity.presentation.cookies import (
    clear_session_cookies,
    set_csrf_cookie,
    set_session_cookies,
)
from tricolink.modules.identity.presentation.dependencies import (
    get_get_me,
    get_google_login,
    get_google_oidc,
    get_login,
    get_logout,
    get_refresh_session,
    get_register,
    get_update_me,
)
from tricolink.modules.identity.presentation.schemas import (
    AuthResponse,
    CsrfResponse,
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    UpdateMeRequest,
    UserResponse,
)
from tricolink.modules.identity.presentation.security import (
    csrf_protect,
    frontend_url,
    origin_guard,
    safe_next_path,
)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
logger = get_logger("tricolink.identity")


@router.get("/csrf", response_model=CsrfResponse)
async def csrf_token(
    request: Request,
    response: Response,
    _: None = Depends(rate_limit("auth")),
) -> CsrfResponse:
    settings = request.app.state.services.settings
    token = secrets.token_urlsafe(32)
    set_csrf_cookie(response, token, settings)
    return CsrfResponse(csrf_token=token)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(origin_guard)],
)
async def register(
    payload: RegisterRequest,
    request: Request,
    use_case: Register = Depends(get_register),
) -> RegisterResponse:
    await use_case.execute(
        RegisterCommand(
            email=payload.email,
            password=payload.password,
            client_ip=_client_ip(request),
        )
    )
    return RegisterResponse()


@router.post(
    "/login",
    response_model=AuthResponse,
    dependencies=[Depends(origin_guard)],
)
async def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    use_case: Login = Depends(get_login),
) -> AuthResponse:
    session = await use_case.execute(
        LoginCommand(
            email=payload.email,
            password=payload.password,
            client_ip=_client_ip(request),
        )
    )
    set_session_cookies(response, session, request.app.state.services.settings)
    return AuthResponse(user=_user_response(session.user))


@router.post(
    "/refresh",
    response_model=AuthResponse,
    dependencies=[Depends(csrf_protect), Depends(rate_limit("auth"))],
)
async def refresh(
    request: Request,
    response: Response,
    use_case: RefreshSession = Depends(get_refresh_session),
) -> AuthResponse:
    settings = request.app.state.services.settings
    session = await use_case.execute(request.cookies.get(settings.refresh_cookie_name))
    set_session_cookies(response, session, settings)
    return AuthResponse(user=_user_response(session.user))


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(csrf_protect), Depends(rate_limit("auth"))],
)
async def logout(
    request: Request,
    response: Response,
    use_case: Logout = Depends(get_logout),
) -> Response:
    settings = request.app.state.services.settings
    await use_case.execute(request.cookies.get(settings.refresh_cookie_name))
    clear_session_cookies(response, settings)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get(
    "/me",
    response_model=UserResponse,
    dependencies=[Depends(user_rate_limit("stats_list"))],
)
async def me(
    user: CurrentUser = Depends(get_current_user),
    use_case: GetMe = Depends(get_get_me),
) -> UserResponse:
    return _user_response(await use_case.execute(user.id))


@router.patch(
    "/me",
    response_model=UserResponse,
    dependencies=[Depends(csrf_protect), Depends(user_rate_limit("stats_list"))],
)
async def update_me(
    payload: UpdateMeRequest,
    user: CurrentUser = Depends(get_current_user),
    use_case: UpdateMe = Depends(get_update_me),
) -> UserResponse:
    fields = payload.model_fields_set
    updated = await use_case.execute(
        UpdateMeCommand(
            user_id=user.id,
            display_name=payload.display_name,
            locale=payload.locale,
            set_display_name="display_name" in fields,
            set_locale="locale" in fields,
        )
    )
    return _user_response(updated)


@router.get("/google/login", dependencies=[Depends(rate_limit("auth"))])
async def google_login(
    request: Request,
    next_path: str | None = Query(default=None, alias="next", max_length=512),
    oidc: GoogleOIDCClient = Depends(get_google_oidc),
) -> RedirectResponse:
    if not oidc.configured:
        raise GoogleNotConfigured()

    safe_path = safe_next_path(next_path)
    nonce = secrets.token_urlsafe(32)
    request.session["oauth_next"] = safe_path
    request.session["oauth_nonce"] = nonce
    redirect = await oidc.authorize(request, nonce=nonce)
    location = redirect.headers.get("location", "")
    state = parse_qs(urlsplit(location).query).get("state", [""])[0]
    if not state:
        raise InvalidGoogleLogin()
    request.session["oauth_state"] = state
    return redirect


@router.get("/google/callback", dependencies=[Depends(rate_limit("auth"))])
async def google_callback(
    request: Request,
    oidc: GoogleOIDCClient = Depends(get_google_oidc),
    use_case: LoginWithGoogle = Depends(get_google_login),
) -> RedirectResponse:
    services = request.app.state.services
    settings = services.settings
    if not oidc.configured:
        return _google_error_redirect(settings)

    expected_state = request.session.pop("oauth_state", None)
    expected_nonce = request.session.pop("oauth_nonce", None)
    next_raw = request.session.pop("oauth_next", "/account")
    state = request.query_params.get("state", "")

    if (
        not expected_state
        or not expected_nonce
        or not state
        or not secrets.compare_digest(state, expected_state)
    ):
        return _google_error_redirect(settings)

    try:
        safe_path = safe_next_path(str(next_raw))
    except InvalidNextPath:
        safe_path = "/account"

    try:
        claims = await oidc.exchange(request)
        identity = validate_google_claims(
            claims,
            expected_nonce=expected_nonce,
            client_id=oidc.client_id,
            now=services.identity.clock.now(),
        )
        session = await use_case.execute(identity)
    except Exception as exc:
        logger.warning(
            "google_oauth_failed",
            error_type=type(exc).__name__,
            error=str(exc)[:300],
        )
        return _google_error_redirect(settings)

    redirect = RedirectResponse(
        frontend_url(settings, safe_path),
        status_code=status.HTTP_302_FOUND,
    )
    set_session_cookies(redirect, session, settings)
    return redirect


def _google_error_redirect(settings: Settings) -> RedirectResponse:
    return RedirectResponse(
        f"{settings.frontend_origin.rstrip('/')}/login?error=google",
        status_code=status.HTTP_302_FOUND,
    )


def _user_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.email.value,
        display_name=user.display_name,
        locale=user.locale,
        is_active=user.is_active,
        created_at=user.created_at,
    )


def _client_ip(request: Request) -> str:
    if request.client is None:
        return "unknown"
    return request.client.host
