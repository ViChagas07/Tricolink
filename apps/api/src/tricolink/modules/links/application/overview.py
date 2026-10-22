from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID

from tricolink.modules.links.application.ports import Clock, LinkRepository

RANGE_DAYS: dict[str, int] = {"7d": 7, "30d": 30, "90d": 90}
DEFAULT_RANGE = "30d"


@dataclass(frozen=True, slots=True)
class LinksOverview:
    total_clicks: int
    total_links: int
    range: str


class GetLinksOverview:
    def __init__(self, *, repository: LinkRepository, clock: Clock) -> None:
        self._repository = repository
        self._clock = clock

    async def execute(self, user_id: UUID, range_key: str = DEFAULT_RANGE) -> LinksOverview:
        days = RANGE_DAYS.get(range_key, RANGE_DAYS[DEFAULT_RANGE])
        since = self._clock.now() - timedelta(days=days)
        total_clicks = await self._repository.count_clicks_since(user_id, since)
        total_links = await self._repository.count_for_user(user_id)
        return LinksOverview(
            total_clicks=total_clicks,
            total_links=total_links,
            range=range_key if range_key in RANGE_DAYS else DEFAULT_RANGE,
        )
