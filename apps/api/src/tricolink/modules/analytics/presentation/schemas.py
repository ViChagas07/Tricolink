from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class StatsSeriesPointResponse(BaseModel):
    date: date
    clicks: int


class StatsBreakdownResponse(BaseModel):
    code: str
    clicks: int
    pct: float


class LinkStatsResponse(BaseModel):
    total: int
    series: list[StatsSeriesPointResponse]
    countries: list[StatsBreakdownResponse]
    devices: list[StatsBreakdownResponse]
    referrers: list[StatsBreakdownResponse]
