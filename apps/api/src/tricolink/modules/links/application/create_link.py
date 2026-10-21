from __future__ import annotations

from contextlib import suppress
from datetime import datetime, timedelta
from uuid import UUID

from tricolink.modules.links.application.dto import CreateLinkCommand
from tricolink.modules.links.application.errors import (
    AliasReserved,
    AliasTaken,
    CodeGenerationFailed,
    DailyQuotaExceeded,
    InvalidAlias,
    LoginRequired,
)
from tricolink.modules.links.application.ports import (
    CacheUnavailable,
    Clock,
    DailyQuota,
    LinkCache,
    LinkRepository,
)
from tricolink.modules.links.application.validators import (
    normalize_expires_at,
    normalize_title,
    validate_url,
)
from tricolink.modules.links.domain.code_generator import CodeGenerator
from tricolink.modules.links.domain.entities import Link
from tricolink.modules.links.domain.errors import (
    DuplicateCodeError,
    InvalidShortCodeError,
)
from tricolink.modules.links.domain.url_policy import UrlPolicy
from tricolink.modules.links.domain.value_objects import OriginalUrl, ShortCode

_MAX_CODE_ATTEMPTS = 5


class CreateLink:
    def __init__(
        self,
        *,
        repository: LinkRepository,
        cache: LinkCache,
        url_policy: UrlPolicy,
        code_generator: CodeGenerator,
        quota: DailyQuota,
        clock: Clock,
        anon_daily_limit: int,
        user_daily_limit: int,
        anon_ttl_days: int,
    ) -> None:
        self._repository = repository
        self._cache = cache
        self._url_policy = url_policy
        self._code_generator = code_generator
        self._quota = quota
        self._clock = clock
        self._anon_daily_limit = anon_daily_limit
        self._user_daily_limit = user_daily_limit
        self._anon_ttl_days = anon_ttl_days

    async def execute(self, command: CreateLinkCommand) -> Link:
        original_url = await validate_url(self._url_policy, command.url)
        title = normalize_title(command.title)
        now = self._clock.now()
        expires_at: datetime | None

        if command.user_id is None:
            if (
                command.alias is not None
                or command.title is not None
                or command.expires_at is not None
            ):
                raise LoginRequired()
            expires_at = now + timedelta(days=self._anon_ttl_days)
            quota_scope = "anon"
            quota_key = command.client_ip
            quota_limit = self._anon_daily_limit
        else:
            expires_at = normalize_expires_at(command.expires_at, now)
            quota_scope = "user"
            quota_key = str(command.user_id)
            quota_limit = self._user_daily_limit

        alias_code: ShortCode | None = None
        if command.alias is not None:
            alias_code = self._parse_alias(command.alias)
            if ShortCode.is_reserved(alias_code.value):
                raise AliasReserved()

        quota_result = await self._quota.consume(quota_scope, quota_key, quota_limit)
        if not quota_result.allowed:
            raise DailyQuotaExceeded(quota_result.retry_after_seconds)

        if alias_code is not None:
            link = self._build_link(
                code=alias_code,
                original_url=original_url,
                title=title,
                user_id=command.user_id,
                expires_at=expires_at,
                is_custom_alias=True,
                now=now,
            )
            try:
                created = await self._repository.create(link)
            except DuplicateCodeError as exc:
                raise AliasTaken() from exc
            await self._invalidate(alias_code)
            return created

        for _ in range(_MAX_CODE_ATTEMPTS):
            code = ShortCode(self._code_generator.generate())
            if ShortCode.is_reserved(code.value):
                continue
            link = self._build_link(
                code=code,
                original_url=original_url,
                title=title,
                user_id=command.user_id,
                expires_at=expires_at,
                is_custom_alias=False,
                now=now,
            )
            try:
                created = await self._repository.create(link)
            except DuplicateCodeError:
                continue
            await self._invalidate(code)
            return created

        raise CodeGenerationFailed()

    def _build_link(
        self,
        *,
        code: ShortCode,
        original_url: OriginalUrl,
        title: str | None,
        user_id: UUID | None,
        expires_at: datetime | None,
        is_custom_alias: bool,
        now: datetime,
    ) -> Link:
        return Link(
            id=None,
            code=code,
            original_url=original_url,
            title=title,
            user_id=user_id,
            is_custom_alias=is_custom_alias,
            is_active=True,
            expires_at=expires_at,
            click_count=0,
            created_at=now,
            updated_at=now,
        )

    def _parse_alias(self, alias: str) -> ShortCode:
        try:
            return ShortCode(alias)
        except InvalidShortCodeError as exc:
            raise InvalidAlias() from exc

    async def _invalidate(self, code: ShortCode) -> None:
        with suppress(CacheUnavailable):
            await self._cache.invalidate(code)
