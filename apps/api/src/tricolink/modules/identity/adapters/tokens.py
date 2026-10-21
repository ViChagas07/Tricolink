from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import jwt

from tricolink.core.config import Settings
from tricolink.modules.identity.application.ports import AccessClaims, IssuedAccessToken


class PyJwtAccessTokens:
    def __init__(self, settings: Settings) -> None:
        if settings.jwt_algorithm not in {"HS256", "HS384", "HS512"}:
            raise ValueError("JWT_ALGORITHM must be HS256, HS384 or HS512")
        self._secret = settings.jwt_secret
        self._algorithm = settings.jwt_algorithm
        self._ttl = timedelta(minutes=settings.access_token_ttl_min)

    def issue(self, user_id: UUID, now: datetime) -> IssuedAccessToken:
        issued_at = now.astimezone(UTC)
        expires_at = issued_at + self._ttl
        token = jwt.encode(
            {
                "sub": str(user_id),
                "jti": uuid4().hex,
                "iat": int(issued_at.timestamp()),
                "exp": int(expires_at.timestamp()),
            },
            self._secret,
            algorithm=self._algorithm,
        )
        return IssuedAccessToken(token=token, expires_at=expires_at)

    def decode(self, token: str) -> AccessClaims | None:
        try:
            payload = jwt.decode(
                token,
                self._secret,
                algorithms=[self._algorithm],
                options={
                    "require": ["sub", "jti", "iat", "exp"],
                    "verify_aud": False,
                },
            )
            user_id = UUID(str(payload["sub"]))
            issued_at = datetime.fromtimestamp(int(payload["iat"]), tz=UTC)
            expires_at = datetime.fromtimestamp(int(payload["exp"]), tz=UTC)
            jti = str(payload["jti"])
        except (jwt.PyJWTError, ValueError, TypeError, KeyError):
            return None
        return AccessClaims(
            user_id=user_id,
            jti=jti,
            issued_at=issued_at,
            expires_at=expires_at,
        )
