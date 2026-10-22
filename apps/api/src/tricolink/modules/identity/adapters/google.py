from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

from authlib.integrations.starlette_client import OAuth  # type: ignore[import-untyped]
from starlette.requests import Request
from starlette.responses import RedirectResponse

from tricolink.core.config import Settings

GOOGLE_AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs"
GOOGLE_ISSUER = "https://accounts.google.com"


class GoogleOIDCClient:
    def __init__(self, settings: Settings) -> None:
        self._client_id = settings.google_client_id
        self._client_secret = settings.google_client_secret
        self._configured = bool(self._client_id and self._client_secret)
        self.redirect_uri = settings.google_redirect_uri or (
            settings.api_public_base_url.rstrip("/") + "/api/v1/auth/google/callback"
        )
        self._oauth = OAuth()
        if self._configured:
            self._oauth.register(
                "google",
                client_id=self._client_id,
                client_secret=self._client_secret,
                authorize_url=GOOGLE_AUTHORIZE_URL,
                access_token_url=GOOGLE_TOKEN_URL,
                jwks_uri=GOOGLE_JWKS_URL,
                issuer=GOOGLE_ISSUER,
                id_token_signing_alg_values_supported=["RS256"],
                client_kwargs={
                    "scope": "openid email profile",
                    "code_challenge_method": "S256",
                },
            )

    @property
    def configured(self) -> bool:
        return self._configured

    @property
    def client_id(self) -> str:
        return self._client_id or ""

    async def authorize(self, request: Request, *, nonce: str) -> RedirectResponse:
        redirect = await self._oauth.google.authorize_redirect(
            request,
            self.redirect_uri,
            nonce=nonce,
        )
        return cast(RedirectResponse, redirect)

    async def exchange(self, request: Request) -> Mapping[str, object]:
        token: dict[str, Any] = await self._oauth.google.authorize_access_token(request)
        userinfo = token.get("userinfo")
        if not isinstance(userinfo, Mapping) or not userinfo:
            # Never fall back to decoding the id_token without signature
            # verification: Authlib only trusts claims it has validated.
            raise ValueError("Google returned no verified identity claims")
        return dict(userinfo)
