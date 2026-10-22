from __future__ import annotations

from datetime import UTC, date, datetime

import pytest

from tricolink.modules.analytics.domain.stats import (
    DIRECT_CODE,
    OTHER_CODE,
    SeriesPoint,
    build_stats,
    build_window,
    fill_series,
    top_breakdown,
)

NOW = datetime(2026, 10, 22, 15, 30, tzinfo=UTC)


def test_build_window_uses_utc_calendar_days() -> None:
    window = build_window("7d", NOW)

    assert window.days == 7
    assert window.start == datetime(2026, 10, 16, tzinfo=UTC)
    assert window.until == NOW
    assert window.dates() == [
        date(2026, 10, 16),
        date(2026, 10, 17),
        date(2026, 10, 18),
        date(2026, 10, 19),
        date(2026, 10, 20),
        date(2026, 10, 21),
        date(2026, 10, 22),
    ]


def test_build_window_rejects_unknown_range() -> None:
    with pytest.raises(ValueError):
        build_window("1y", NOW)


def test_fill_series_inserts_zero_for_missing_days() -> None:
    window = build_window("7d", NOW)

    points = fill_series(
        {
            date(2026, 10, 16): 2,
            date(2026, 10, 18): 4,
            date(2026, 10, 22): 1,
        },
        window,
    )

    assert len(points) == 7
    assert points[0] == SeriesPoint(date=date(2026, 10, 16), clicks=2)
    assert points[1] == SeriesPoint(date=date(2026, 10, 17), clicks=0)
    assert points[2] == SeriesPoint(date=date(2026, 10, 18), clicks=4)
    assert points[-1] == SeriesPoint(date=date(2026, 10, 22), clicks=1)


def test_top_breakdown_keeps_ten_and_folds_the_rest_into_other() -> None:
    rows = [(f"C{index:02d}", 100 - index) for index in range(12)]
    rows.append((None, 5))
    total = sum(clicks for _, clicks in rows)

    items = top_breakdown(rows, total)

    assert len(items) == 11
    assert items[0].code == "C00"
    assert items[-1].code == OTHER_CODE
    assert items[-1].clicks == total - sum(100 - index for index in range(10))
    assert abs(sum(item.pct for item in items) - 100.0) <= 0.5


def test_country_without_code_is_counted_only_in_other() -> None:
    items = top_breakdown([("BR", 3), (None, 7)], 10)

    assert [item.code for item in items] == ["BR", OTHER_CODE]
    assert items[1].clicks == 7


def test_null_referrer_becomes_direct_and_others_fold_into_other() -> None:
    window = build_window("30d", NOW)

    stats = build_stats(
        total=9,
        series={},
        countries=[("BR", 9)],
        devices=[("mobile", 9)],
        referrers=[("google.com", 3), ("instagram.com", 2)],
        direct_referrers=4,
        window=window,
    )

    assert stats.referrers[0].code == DIRECT_CODE
    assert stats.referrers[0].clicks == 4
    assert stats.referrers[-1].code == "instagram.com"
    assert len(stats.series) == 30


def test_empty_stats_have_zeroed_series_and_no_breakdown_rows() -> None:
    window = build_window("7d", NOW)

    stats = build_stats(
        total=0,
        series={},
        countries=[],
        devices=[],
        referrers=[],
        window=window,
    )

    assert stats.total == 0
    assert all(point.clicks == 0 for point in stats.series)
    assert stats.countries == []
    assert stats.devices == []
    assert stats.referrers == []
