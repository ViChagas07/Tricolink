from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from uuid import UUID

from tricolink.modules.analytics.domain.click import ClickEvent
from tricolink.modules.links.domain.entities import Link
from tricolink.modules.links.domain.value_objects import ShortCode


@dataclass(frozen=True, slots=True)
class PageCursor:
    created_at: datetime
    link_id: int


@dataclass(frozen=True, slots=True)
class CacheEntry:
    link_id: int
    original_url: str
    expires_at: datetime | None
    is_active: bool


@dataclass(frozen=True, slots=True)
class QuotaResult:
    allowed: bool
    used: int
    limit: int
    retry_after_seconds: int


class CacheUnavailable(Exception):
    """Raised when the cache cannot answer and the caller must fall back to the DB."""


class LinkRepository(Protocol):
    async def create(self, link: Link) -> Link: ...

    async def get_by_code(self, code: ShortCode) -> Link | None: ...

    async def get_for_user(self, code: ShortCode, user_id: UUID) -> Link | None: ...

    async def list_for_user(
        self,
        user_id: UUID,
        *,
        cursor: PageCursor | None,
        limit: int,
        query: str | None,
    ) -> list[Link]: ...

    async def update(self, link: Link, user_id: UUID) -> Link | None: ...

    async def delete(self, code: ShortCode, user_id: UUID) -> bool: ...

    async def count_clicks_since(self, user_id: UUID, since: datetime) -> int: ...

    async def count_for_user(self, user_id: UUID) -> int: ...


class LinkCache(Protocol):
    async def resolve(
        self,
        code: ShortCode,
        loader: Callable[[], Awaitable[Link | None]],
    ) -> CacheEntry | None: ...

    async def invalidate(self, code: ShortCode) -> None: ...


class Clock(Protocol):
    def now(self) -> datetime: ...


class DailyQuota(Protocol):
    async def consume(self, scope: str, key: str, limit: int) -> QuotaResult: ...


class ClickPublisher(Protocol):
    async def publish(self, event: ClickEvent) -> bool: ...
