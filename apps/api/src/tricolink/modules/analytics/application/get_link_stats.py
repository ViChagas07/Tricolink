from __future__ import annotations

from uuid import UUID

from tricolink.modules.analytics.application.ports import StatsCache, StatsRepository
from tricolink.modules.analytics.domain.stats import (
    DEFAULT_RANGE,
    LinkStats,
    build_stats,
    build_window,
)
from tricolink.modules.links.application.errors import LinkNotFound
from tricolink.modules.links.application.ports import Clock, LinkRepository
from tricolink.modules.links.domain.errors import InvalidShortCodeError
from tricolink.modules.links.domain.value_objects import ShortCode


class GetLinkStats:
    def __init__(
        self,
        *,
        links: LinkRepository,
        stats: StatsRepository,
        cache: StatsCache,
        clock: Clock,
    ) -> None:
        self._links = links
        self._stats = stats
        self._cache = cache
        self._clock = clock

    async def execute(
        self,
        code_value: str,
        user_id: UUID,
        range_key: str = DEFAULT_RANGE,
    ) -> LinkStats:
        try:
            code = ShortCode(code_value)
        except InvalidShortCodeError as exc:
            raise LinkNotFound() from exc

        link = await self._links.get_for_user(code, user_id)
        if link is None or link.id is None:
            raise LinkNotFound()

        link_id = link.id
        window = build_window(range_key, self._clock.now())

        async def load() -> LinkStats:
            raw = await self._stats.collect(
                link_id,
                user_id,
                since=window.start,
                until=window.until,
            )
            return build_stats(
                total=raw.total,
                series=dict(raw.series),
                countries=raw.countries,
                devices=raw.devices,
                referrers=raw.referrers,
                direct_referrers=raw.direct_referrers,
                window=window,
            )

        return await self._cache.get_or_load(link_id, range_key, load)
