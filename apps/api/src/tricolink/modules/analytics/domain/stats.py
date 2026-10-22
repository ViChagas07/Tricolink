from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta

RANGE_DAYS: dict[str, int] = {"7d": 7, "30d": 30, "90d": 90}
DEFAULT_RANGE = "30d"
OTHER_CODE = "other"
DIRECT_CODE = "direct"
TOP_LIMIT = 10


@dataclass(frozen=True, slots=True)
class StatsWindow:
    range_key: str
    days: int
    start: datetime
    until: datetime

    def dates(self) -> list[date]:
        first = self.start.astimezone(UTC).date()
        return [first + timedelta(days=offset) for offset in range(self.days)]


@dataclass(frozen=True, slots=True)
class SeriesPoint:
    date: date
    clicks: int


@dataclass(frozen=True, slots=True)
class BreakdownItem:
    code: str
    clicks: int
    pct: float


@dataclass(frozen=True, slots=True)
class LinkStats:
    total: int
    series: list[SeriesPoint]
    countries: list[BreakdownItem]
    devices: list[BreakdownItem]
    referrers: list[BreakdownItem]


def build_window(range_key: str, now: datetime) -> StatsWindow:
    days = RANGE_DAYS.get(range_key)
    if days is None:
        raise ValueError(f"unsupported range: {range_key}")

    current = now.astimezone(UTC)
    start_date = current.date() - timedelta(days=days - 1)
    start = datetime.combine(start_date, time.min, tzinfo=UTC)
    return StatsWindow(
        range_key=range_key,
        days=days,
        start=start,
        until=current,
    )


def fill_series(counts: Mapping[date, int], window: StatsWindow) -> list[SeriesPoint]:
    return [SeriesPoint(date=day, clicks=counts.get(day, 0)) for day in window.dates()]


def top_breakdown(
    rows: Sequence[tuple[str | None, int]],
    total: int,
    *,
    limit: int = TOP_LIMIT,
) -> list[BreakdownItem]:
    ordered = sorted(rows, key=lambda row: (-row[1], row[0] or ""))
    head = [row for row in ordered if row[0] is not None][:limit]
    items = [
        BreakdownItem(code=label, clicks=clicks, pct=_pct(clicks, total))
        for label, clicks in head
        if label is not None
    ]
    remainder = total - sum(clicks for _, clicks in head)
    if remainder > 0:
        items.append(BreakdownItem(code=OTHER_CODE, clicks=remainder, pct=_pct(remainder, total)))
    return items


def referrer_breakdown(
    rows: Sequence[tuple[str, int]],
    direct_clicks: int,
    total: int,
    *,
    limit: int = TOP_LIMIT,
) -> list[BreakdownItem]:
    ordered = sorted(rows, key=lambda row: (-row[1], row[0]))
    head = ordered[:limit]
    items = [
        BreakdownItem(code=label, clicks=clicks, pct=_pct(clicks, total)) for label, clicks in head
    ]
    if direct_clicks > 0:
        items.append(
            BreakdownItem(code=DIRECT_CODE, clicks=direct_clicks, pct=_pct(direct_clicks, total))
        )
    items.sort(key=lambda item: (-item.clicks, item.code))
    remainder = total - sum(clicks for _, clicks in head) - direct_clicks
    if remainder > 0:
        items.append(BreakdownItem(code=OTHER_CODE, clicks=remainder, pct=_pct(remainder, total)))
    return items


def full_breakdown(
    rows: Sequence[tuple[str | None, int]],
    total: int,
    *,
    missing_code: str,
) -> list[BreakdownItem]:
    ordered = sorted(rows, key=lambda row: (-row[1], row[0] or ""))
    return [
        BreakdownItem(
            code=label or missing_code,
            clicks=clicks,
            pct=_pct(clicks, total),
        )
        for label, clicks in ordered
    ]


def build_stats(
    *,
    total: int,
    series: Mapping[date, int],
    countries: Sequence[tuple[str | None, int]],
    devices: Sequence[tuple[str | None, int]],
    referrers: Sequence[tuple[str, int]],
    direct_referrers: int = 0,
    window: StatsWindow,
) -> LinkStats:
    return LinkStats(
        total=total,
        series=fill_series(series, window),
        countries=top_breakdown(countries, total),
        devices=full_breakdown(devices, total, missing_code="unknown"),
        referrers=referrer_breakdown(referrers, direct_referrers, total),
    )


def _pct(clicks: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round(clicks / total * 100, 1)
