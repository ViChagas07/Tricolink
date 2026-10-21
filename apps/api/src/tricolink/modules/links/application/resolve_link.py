from __future__ import annotations

from datetime import UTC, datetime

from tricolink.modules.links.application.dto import ResolvedLink
from tricolink.modules.links.application.ports import (
    CacheEntry,
    CacheUnavailable,
    Clock,
    LinkCache,
    LinkRepository,
)
from tricolink.modules.links.domain.entities import Link, LinkState
from tricolink.modules.links.domain.errors import InvalidShortCodeError
from tricolink.modules.links.domain.value_objects import ShortCode


class ResolveLink:
    def __init__(
        self,
        *,
        repository: LinkRepository,
        cache: LinkCache,
        clock: Clock,
    ) -> None:
        self._repository = repository
        self._cache = cache
        self._clock = clock

    async def execute(self, code_value: str) -> ResolvedLink | None:
        try:
            code = ShortCode(code_value)
        except InvalidShortCodeError:
            return None

        try:
            entry = await self._cache.resolve(
                code,
                lambda: self._repository.get_by_code(code),
            )
        except CacheUnavailable:
            link = await self._repository.get_by_code(code)
            if link is None:
                return None
            return _resolved_from_link(link, self._clock.now())

        if entry is None:
            return None
        return _resolved_from_cache(entry, self._clock.now())


def _resolved_from_cache(entry: CacheEntry, now: datetime) -> ResolvedLink:
    return ResolvedLink(
        link_id=entry.link_id,
        original_url=entry.original_url,
        state=_entry_state(entry, now),
    )


def _entry_state(entry: CacheEntry, now: datetime) -> LinkState:
    if not entry.is_active:
        return LinkState.INACTIVE
    if entry.expires_at is not None and _as_utc(entry.expires_at) <= _as_utc(now):
        return LinkState.EXPIRED
    return LinkState.ACTIVE


def _resolved_from_link(link: Link, now: datetime) -> ResolvedLink | None:
    if link.id is None:
        return None
    return ResolvedLink(
        link_id=link.id,
        original_url=link.original_url.value,
        state=link.state(now),
    )


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)
