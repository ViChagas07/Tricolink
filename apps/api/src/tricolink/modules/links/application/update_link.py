from __future__ import annotations

from contextlib import suppress
from datetime import datetime

from tricolink.modules.links.application.dto import Unset, UpdateLinkCommand
from tricolink.modules.links.application.errors import LinkNotFound
from tricolink.modules.links.application.ports import (
    CacheUnavailable,
    Clock,
    LinkCache,
    LinkRepository,
)
from tricolink.modules.links.application.validators import (
    normalize_expires_at,
    normalize_title,
    validate_url,
)
from tricolink.modules.links.domain.entities import Link
from tricolink.modules.links.domain.errors import InvalidShortCodeError
from tricolink.modules.links.domain.url_policy import UrlPolicy
from tricolink.modules.links.domain.value_objects import ShortCode


class UpdateLink:
    def __init__(
        self,
        *,
        repository: LinkRepository,
        cache: LinkCache,
        url_policy: UrlPolicy,
        clock: Clock,
    ) -> None:
        self._repository = repository
        self._cache = cache
        self._url_policy = url_policy
        self._clock = clock

    async def execute(self, command: UpdateLinkCommand) -> Link:
        try:
            code = ShortCode(command.code)
        except InvalidShortCodeError as exc:
            raise LinkNotFound() from exc

        current = await self._repository.get_for_user(code, command.user_id)
        if current is None:
            raise LinkNotFound()

        now = self._clock.now()
        changed = False

        title = current.title
        if not isinstance(command.title, Unset):
            title = normalize_title(command.title)
            changed = True

        original_url = current.original_url
        if not isinstance(command.original_url, Unset):
            original_url = await validate_url(self._url_policy, command.original_url)
            changed = True

        expires_at = current.expires_at
        if not isinstance(command.expires_at, Unset):
            expires_at = _normalize_expiry(command.expires_at, now)
            changed = True

        is_active = current.is_active
        if not isinstance(command.is_active, Unset):
            is_active = command.is_active
            changed = True

        if not changed:
            return current

        updated = current.with_updates(
            title=title,
            original_url=original_url,
            is_active=is_active,
            expires_at=expires_at,
            updated_at=now,
        )
        persisted = await self._repository.update(updated, command.user_id)
        if persisted is None:
            raise LinkNotFound()
        with suppress(CacheUnavailable):
            await self._cache.invalidate(code)
        return persisted


def _normalize_expiry(value: datetime | None, now: datetime) -> datetime | None:
    if value is None:
        return None
    return normalize_expires_at(value, now)
