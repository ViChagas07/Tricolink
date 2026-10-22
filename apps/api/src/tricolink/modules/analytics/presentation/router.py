from __future__ import annotations

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Path, Query

from tricolink.core.deps import CurrentUser, get_current_user, user_rate_limit
from tricolink.modules.analytics.application.get_link_stats import GetLinkStats
from tricolink.modules.analytics.presentation.dependencies import get_get_link_stats
from tricolink.modules.analytics.presentation.schemas import (
    LinkStatsResponse,
    StatsBreakdownResponse,
    StatsSeriesPointResponse,
)

_SHORT_CODE_PATTERN = r"^[A-Za-z0-9_-]{3,32}$"

router = APIRouter(prefix="/api/v1", tags=["analytics"])


@router.get("/links/{code}/stats", response_model=LinkStatsResponse)
async def link_stats(
    code: Annotated[str, Path(min_length=3, max_length=32, pattern=_SHORT_CODE_PATTERN)],
    current_user: CurrentUser = Depends(get_current_user),
    use_case: GetLinkStats = Depends(get_get_link_stats),
    range_key: Literal["7d", "30d", "90d"] = Query(default="30d", alias="range"),
    _: None = Depends(user_rate_limit("stats_list")),
) -> LinkStatsResponse:
    stats = await use_case.execute(code, current_user.id, range_key)
    return LinkStatsResponse(
        total=stats.total,
        series=[
            StatsSeriesPointResponse(date=point.date, clicks=point.clicks) for point in stats.series
        ],
        countries=[
            StatsBreakdownResponse(code=item.code, clicks=item.clicks, pct=item.pct)
            for item in stats.countries
        ],
        devices=[
            StatsBreakdownResponse(code=item.code, clicks=item.clicks, pct=item.pct)
            for item in stats.devices
        ],
        referrers=[
            StatsBreakdownResponse(code=item.code, clicks=item.clicks, pct=item.pct)
            for item in stats.referrers
        ],
    )
