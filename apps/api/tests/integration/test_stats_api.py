from __future__ import annotations

import asyncio
import time
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from redis.asyncio import Redis
from sqlalchemy import delete, insert, select

from tricolink.core.config import Settings
from tricolink.core.deps import CurrentUser, get_current_user
from tricolink.infra.cache import create_redis
from tricolink.infra.db import Database
from tricolink.infra.db.models import ClickEvent as ClickEventRow
from tricolink.infra.db.models import Link as LinkRow
from tricolink.infra.db.models import User as UserRow
from tricolink.main import create_app
from tricolink.modules.analytics.adapters.stats_cache import (
    STATS_KEY,
    STATS_LOCK_KEY,
    RedisStatsCache,
)
from tricolink.modules.analytics.domain.stats import LinkStats, build_stats, build_window
from tricolink.modules.links.adapters.repository import SqlAlchemyLinkRepository
from tricolink.modules.links.domain.entities import Link
from tricolink.modules.links.domain.value_objects import OriginalUrl, ShortCode

pytestmark = pytest.mark.integration


def api_settings(**overrides: object) -> Settings:
    unique = uuid4().hex[:10]
    base = replace(
        Settings.from_env(),
        click_flusher_enabled=False,
        click_stream_key=f"test:clicks:{unique}",
        click_stream_group=f"test-clicks-{unique}",
        short_base_url="https://short.test",
        rl_redirect_capacity=1000,
        rl_redirect_refill_per_sec=1000,
        rl_create_capacity=1000,
        rl_create_refill_per_sec=1000,
        rl_global_capacity=100_000,
        rl_global_refill_per_sec=100_000,
        rl_list_capacity=1000,
        rl_list_refill_per_sec=1000,
        anon_daily_link_limit=1000,
        user_daily_link_limit=1000,
        trusted_proxy_count=1,
    )
    return replace(base, **overrides)


def seed_user(settings: Settings) -> UUID:
    user_id = uuid4()

    async def run() -> None:
        database = Database(settings)
        try:
            async with database.unit_of_work() as session:
                session.add(
                    UserRow(
                        id=user_id,
                        email=f"stats-{user_id}@example.com",
                        password_hash=None,
                    )
                )
        finally:
            await database.dispose()

    asyncio.run(run())
    return user_id


def seed_link(settings: Settings, code: str, user_id: UUID) -> int:
    now = datetime.now(UTC)
    link = Link(
        id=None,
        code=ShortCode(code),
        original_url=OriginalUrl.parse("https://93.184.216.34/stats"),
        title="Stats test",
        user_id=user_id,
        is_custom_alias=False,
        is_active=True,
        expires_at=None,
        click_count=0,
        created_at=now,
        updated_at=now,
    )

    async def run() -> int:
        database = Database(settings)
        repository = SqlAlchemyLinkRepository(database)
        try:
            created = await repository.create(link)
            assert created.id is not None
            return created.id
        finally:
            await database.dispose()

    return asyncio.run(run())


def seed_clicks(settings: Settings, link_id: int, rows: list[dict[str, object]]) -> None:
    admin_settings = replace(
        settings,
        database_url=settings.migration_database_url or settings.database_url,
    )

    async def run() -> None:
        database = Database(admin_settings)
        try:
            async with database.unit_of_work() as session:
                await session.execute(
                    insert(ClickEventRow),
                    [{"link_id": link_id, **row} for row in rows],
                )
        finally:
            await database.dispose()

    asyncio.run(run())


def cleanup(settings: Settings, *, codes: list[str], user_ids: list[UUID]) -> None:
    admin_settings = replace(
        settings,
        database_url=settings.migration_database_url or settings.database_url,
    )

    async def run() -> None:
        database = Database(admin_settings)
        link_ids: list[int] = []
        try:
            async with database.unit_of_work() as session:
                if codes:
                    link_ids = list(
                        (
                            await session.scalars(select(LinkRow.id).where(LinkRow.code.in_(codes)))
                        ).all()
                    )
                    await session.execute(delete(LinkRow).where(LinkRow.code.in_(codes)))
                for user_id in user_ids:
                    await session.execute(delete(UserRow).where(UserRow.id == user_id))
        finally:
            await database.dispose()

        redis = create_redis(settings)
        try:
            keys: list[str] = []
            for link_id in link_ids:
                for range_key in ("7d", "30d", "90d"):
                    keys.append(STATS_KEY.format(link_id=link_id, range=range_key))
                    keys.append(STATS_LOCK_KEY.format(link_id=link_id, range=range_key))
            if keys:
                await redis.delete(*keys)
        finally:
            await redis.aclose()

    asyncio.run(run())


def test_stats_series_fills_gaps_and_hides_other_users_links() -> None:
    settings = api_settings()
    owner = seed_user(settings)
    other = seed_user(settings)
    code = f"s{uuid4().hex[:8]}"
    link_id = seed_link(settings, code, owner)
    now = datetime.now(UTC)
    seed_clicks(
        settings,
        link_id,
        [
            {
                "clicked_at": now,
                "device": "mobile",
                "country": "BR",
                "referrer_host": "google.com",
            },
            {
                "clicked_at": now - timedelta(days=2),
                "device": "desktop",
                "country": "US",
                "referrer_host": None,
            },
            {
                "clicked_at": now - timedelta(days=3),
                "device": "tablet",
                "country": "DE",
                "referrer_host": "instagram.com",
            },
            {
                "clicked_at": now - timedelta(days=10),
                "device": "bot",
                "country": "JP",
                "referrer_host": "news.example.com",
            },
        ],
    )

    app = create_app(settings)
    app.dependency_overrides[get_current_user] = lambda: CurrentUser(id=owner)
    try:
        with TestClient(app) as client:
            response = client.get(f"/api/v1/links/{code}/stats", params={"range": "7d"})
            assert response.status_code == 200, response.text
            payload = response.json()

            assert payload["total"] == 3
            assert len(payload["series"]) == 7
            assert sum(point["clicks"] for point in payload["series"]) == 3
            assert any(point["clicks"] == 0 for point in payload["series"])
            assert {item["code"] for item in payload["countries"][:3]} == {"BR", "DE", "US"}

            invalid = client.get(f"/api/v1/links/{code}/stats", params={"range": "1y"})
            assert invalid.status_code == 422

            app.dependency_overrides[get_current_user] = lambda: CurrentUser(id=other)
            forbidden = client.get(f"/api/v1/links/{code}/stats")
            assert forbidden.status_code == 404
            assert forbidden.json()["error"]["code"] == "not_found"

            app.dependency_overrides.pop(get_current_user, None)
            anonymous = client.get(f"/api/v1/links/{code}/stats")
            assert anonymous.status_code == 401
    finally:
        cleanup(settings, codes=[code], user_ids=[owner, other])


def test_stats_rate_limit_returns_429() -> None:
    settings = api_settings(rl_list_capacity=1, rl_list_refill_per_sec=0.0)
    owner = seed_user(settings)
    code = f"r{uuid4().hex[:8]}"
    seed_link(settings, code, owner)

    app = create_app(settings)
    app.dependency_overrides[get_current_user] = lambda: CurrentUser(id=owner)
    try:
        with TestClient(app) as client:
            first = client.get(f"/api/v1/links/{code}/stats")
            second = client.get(f"/api/v1/links/{code}/stats")

            assert first.status_code == 200, first.text
            assert second.status_code == 429
            assert second.headers["ratelimit-limit"] == "1"
            assert second.json()["error"]["code"] == "rate_limited"
    finally:
        cleanup(settings, codes=[code], user_ids=[owner])


def test_breakdowns_keep_top_ten_and_use_other_and_direct_sentinels() -> None:
    settings = api_settings()
    owner = seed_user(settings)
    code = f"s{uuid4().hex[:8]}"
    link_id = seed_link(settings, code, owner)
    now = datetime.now(UTC)

    country_counts = [
        ("BR", 12),
        ("US", 11),
        ("DE", 10),
        ("JP", 9),
        ("FR", 8),
        ("GB", 7),
        ("IT", 6),
        ("ES", 5),
        ("CA", 4),
        ("MX", 3),
        ("AR", 2),
        ("CL", 1),
        (None, 2),
    ]
    referrer_counts = [
        (None, 24),
        ("google.com", 10),
        ("instagram.com", 9),
        ("news.example.com", 8),
        ("x.com", 7),
        ("facebook.com", 6),
        ("reddit.com", 5),
        ("linkedin.com", 4),
        ("youtube.com", 3),
        ("t.co", 2),
        ("whatsapp.com", 1),
        ("telegram.org", 1),
    ]
    devices = ["mobile", "desktop", "tablet", "bot", "unknown"]
    countries = [code_value for code_value, count in country_counts for _ in range(count)]
    referrers = [host for host, count in referrer_counts for _ in range(count)]
    total = len(countries)
    assert total == 80
    assert total == len(referrers)

    rows = [
        {
            "clicked_at": now - timedelta(minutes=index),
            "device": devices[index % len(devices)],
            "country": countries[index],
            "referrer_host": referrers[index],
        }
        for index in range(total)
    ]
    seed_clicks(settings, link_id, rows)

    app = create_app(settings)
    app.dependency_overrides[get_current_user] = lambda: CurrentUser(id=owner)
    try:
        with TestClient(app) as client:
            response = client.get(f"/api/v1/links/{code}/stats", params={"range": "30d"})
            assert response.status_code == 200, response.text
            payload = response.json()

            assert payload["total"] == 80
            assert len(payload["series"]) == 30

            countries_payload = payload["countries"]
            assert len(countries_payload) == 11
            assert countries_payload[-1]["code"] == "other"
            assert countries_payload[-1]["clicks"] == 5
            assert countries_payload[-1]["pct"] == pytest.approx(6.25, abs=0.1)

            referrers_payload = payload["referrers"]
            assert referrers_payload[0]["code"] == "direct"
            assert referrers_payload[0]["clicks"] == 24
            assert referrers_payload[0]["pct"] == pytest.approx(30.0, abs=0.1)
            assert referrers_payload[-1]["code"] == "other"
            assert referrers_payload[-1]["clicks"] == 1

            device_payload = payload["devices"]
            assert {item["code"] for item in device_payload} == set(devices)
            assert sum(item["clicks"] for item in device_payload) == 80
    finally:
        cleanup(settings, codes=[code], user_ids=[owner])


async def test_stats_cache_single_flight_and_ttl(redis_client: Redis) -> None:
    settings = api_settings(stats_cache_ttl_seconds=30)
    cache = RedisStatsCache(redis_client, breaker=None, settings=settings)
    link_id = uuid4().int % 10_000_000
    window = build_window("7d", datetime.now(UTC))
    expected = build_stats(
        total=3,
        series={},
        countries=[("BR", 3)],
        devices=[("mobile", 3)],
        referrers=[],
        direct_referrers=3,
        window=window,
    )
    calls = 0

    async def loader() -> LinkStats:
        nonlocal calls
        calls += 1
        await asyncio.sleep(0.05)
        return expected

    try:
        results = await asyncio.gather(
            *(cache.get_or_load(link_id, "7d", loader) for _ in range(25))
        )
        assert calls == 1
        assert all(result == expected for result in results)

        cached = await cache.get_or_load(link_id, "7d", loader)
        assert cached == expected
        assert calls == 1

        ttl = await redis_client.ttl(STATS_KEY.format(link_id=link_id, range="7d"))
        assert 0 < ttl <= 35
    finally:
        await redis_client.delete(
            STATS_KEY.format(link_id=link_id, range="7d"),
            STATS_LOCK_KEY.format(link_id=link_id, range="7d"),
        )


def test_stats_50k_clicks_benchmark() -> None:
    settings = api_settings()
    owner = seed_user(settings)
    code = f"p{uuid4().hex[:8]}"
    link_id = seed_link(settings, code, owner)
    now = datetime.now(UTC)
    countries = [f"{chr(65 + index // 26)}{chr(65 + index % 26)}" for index in range(40)]
    devices = ["desktop", "mobile", "tablet", "bot", "unknown"]
    referrers: list[str | None] = [None, "google.com", "instagram.com", "news.example.com"]
    referrers.extend(f"source{index}.example" for index in range(21))

    rows = [
        {
            "clicked_at": now - timedelta(days=index % 30, seconds=index % 3_600),
            "device": devices[index % len(devices)],
            "country": countries[index % len(countries)],
            "referrer_host": referrers[index % len(referrers)],
        }
        for index in range(50_000)
    ]
    seed_clicks(settings, link_id, rows)

    app = create_app(settings)
    app.dependency_overrides[get_current_user] = lambda: CurrentUser(id=owner)
    try:
        with TestClient(app) as client:
            started = time.perf_counter()
            response = client.get(f"/api/v1/links/{code}/stats", params={"range": "30d"})
            elapsed = time.perf_counter() - started

            assert response.status_code == 200, response.text
            payload = response.json()
            assert payload["total"] == 50_000
            assert len(payload["series"]) == 30
            assert sum(point["clicks"] for point in payload["series"]) == 50_000
            assert len(payload["countries"]) == 11
            assert len(payload["referrers"]) == 12
            assert payload["referrers"][-1]["code"] == "other"
            print(f"STATS_50K_MS={elapsed * 1000:.1f}")
    finally:
        cleanup(settings, codes=[code], user_ids=[owner])
