from __future__ import annotations

from fastapi import Request

from tricolink.core.deps import get_services
from tricolink.modules.identity.adapters.google import GoogleOIDCClient
from tricolink.modules.identity.application import (
    AuthenticateAccess,
    GetAvatar,
    GetMe,
    Login,
    LoginWithGoogle,
    Logout,
    RefreshSession,
    Register,
    RemoveAvatar,
    SetAvatar,
    UpdateMe,
)


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


def get_get_avatar(request: Request) -> GetAvatar:
    return get_services(request).identity.get_avatar


def get_set_avatar(request: Request) -> SetAvatar:
    return get_services(request).identity.set_avatar


def get_remove_avatar(request: Request) -> RemoveAvatar:
    return get_services(request).identity.remove_avatar


def get_google_login(request: Request) -> LoginWithGoogle:
    return get_services(request).identity.google_login


def get_authenticate_access(request: Request) -> AuthenticateAccess:
    return get_services(request).identity.authenticate_access


def get_google_oidc(request: Request) -> GoogleOIDCClient:
    return get_services(request).identity.google_oidc
