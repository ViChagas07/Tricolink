from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import date, datetime
from typing import Protocol
from uuid import UUID

from tricolink.modules.analytics.domain.stats import LinkStats


@dataclass(frozen=True, slots=True)
class RawStats:
    total: int
    series: list[tuple[date, int]]
    countries: list[tuple[str | None, int]]
    devices: list[tuple[str, int]]
    referrers: list[tuple[str, int]]
    direct_referrers: int


class StatsRepository(Protocol):
    async def collect(
        self,
        link_id: int,
        user_id: UUID,
        *,
        since: datetime,
        until: datetime,
    ) -> RawStats: ...


class StatsCache(Protocol):
    async def get_or_load(
        self,
        code: str,
        range_key: str,
        loader: Callable[[], Awaitable[LinkStats]],
    ) -> LinkStats: ...
