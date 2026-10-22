from __future__ import annotations

import asyncio
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete, select

from tricolink.core.config import Settings
from tricolink.core.deps import CurrentUser, get_current_user_optional
from tricolink.infra.cache import create_redis
from tricolink.infra.db import Database
from tricolink.infra.db.models import ClickEvent as ClickEventRow
from tricolink.infra.db.models import Link as LinkRow
from tricolink.infra.db.models import User as UserRow
from tricolink.main import create_app
from tricolink.modules.links.adapters.cache import LINK_KEY, LOCK_KEY, NEGATIVE_KEY
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
                        email=f"api-{user_id}@example.com",
                        password_hash=None,
                    )
                )
        finally:
            await database.dispose()

    asyncio.run(run())
    return user_id


def seed_links(settings: Settings, links: list[Link]) -> None:
    async def run() -> None:
        database = Database(settings)
        repository = SqlAlchemyLinkRepository(database)
        try:
            for link in links:
                await repository.create(link)
        finally:
            await database.dispose()

    asyncio.run(run())


def seed_click(settings: Settings, code: str, clicked_at: datetime) -> None:
    admin_settings = replace(
        settings,
        database_url=settings.migration_database_url or settings.database_url,
    )

    async def run() -> None:
        database = Database(admin_settings)
        try:
            async with database.unit_of_work() as session:
                link_id = await session.scalar(select(LinkRow.id).where(LinkRow.code == code))
                assert link_id is not None
                session.add(
                    ClickEventRow(
                        link_id=link_id,
                        clicked_at=clicked_at,
                        device="unknown",
                    )
                )
        finally:
            await database.dispose()

    asyncio.run(run())


def cleanup(
    settings: Settings,
    *,
    codes: list[str],
    user_ids: list[UUID],
) -> None:
    admin_settings = replace(
        settings,
        database_url=settings.migration_database_url or settings.database_url,
    )

    async def run() -> None:
        database = Database(admin_settings)
        try:
            async with database.unit_of_work() as session:
                if codes:
                    await session.execute(delete(LinkRow).where(LinkRow.code.in_(codes)))
                for user_id in user_ids:
                    await session.execute(delete(UserRow).where(UserRow.id == user_id))
        finally:
            await database.dispose()

        redis = create_redis(settings)
        try:
            keys: list[str] = []
            for code in codes:
                keys.extend(
                    (
                        LINK_KEY.format(code=code),
                        LOCK_KEY.format(code=code),
                        NEGATIVE_KEY.format(code=code),
                    )
                )
            keys.append(settings.click_stream_key)
            await redis.delete(*keys)
        finally:
            await redis.aclose()

    asyncio.run(run())


def direct_link(
    code: str,
    *,
    user_id: UUID | None = None,
    expires_at: datetime | None = None,
    is_active: bool = True,
) -> Link:
    now = datetime.now(UTC)
    return Link(
        id=None,
        code=ShortCode(code),
        original_url=OriginalUrl.parse("https://93.184.216.34/path"),
        title=None,
        user_id=user_id,
        is_custom_alias=False,
        is_active=is_active,
        expires_at=expires_at,
        click_count=0,
        created_at=now,
        updated_at=now,
    )


def test_anonymous_create_and_redirect() -> None:
    settings = api_settings()
    app = create_app(settings)
    code: str | None = None
    try:
        with TestClient(app) as client:
            created = client.post(
                "/api/v1/links",
                json={"url": "https://93.184.216.34/path"},
            )
            assert created.status_code == 201, created.text
            payload = created.json()
            code = payload["code"]
            assert payload["short_url"] == f"https://short.test/{code}"
            assert payload["original_url"] == "https://93.184.216.34/path"
            expires_at = datetime.fromisoformat(payload["expires_at"])
            assert expires_at > datetime.now(UTC) + timedelta(days=29)

            forbidden = client.post(
                "/api/v1/links",
                json={"url": "https://93.184.216.34/x", "alias": "custom-alias"},
            )
            assert forbidden.status_code == 401

            redirect = client.get(
                f"/api/v1/r/{code}",
                headers={
                    "user-agent": (
                        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                        "AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1"
                    ),
                    "cf-ipcountry": "br",
                    "referer": "https://news.example.com/path?q=secret",
                },
                follow_redirects=False,
            )
            assert redirect.status_code == 302
            assert redirect.headers["location"] == "https://93.184.216.34/path"
            assert redirect.headers["x-robots-tag"] == "noindex, nofollow"

        async def read_stream() -> list[tuple[str, dict[str, str]]]:
            redis = create_redis(settings)
            try:
                return await redis.xrange(settings.click_stream_key)
            finally:
                await redis.aclose()

        entries = asyncio.run(read_stream())
        assert len(entries) == 1
        assert entries[0][1]["country"] == "BR"
        assert entries[0][1]["device"] == "mobile"
        assert entries[0][1]["browser"] == "safari"
        assert entries[0][1]["referrer_host"] == "news.example.com"
        assert "iPhone" not in str(entries[0][1])
    finally:
        cleanup(settings, codes=[code] if code else [], user_ids=[])


def test_owner_crud_alias_rules_and_cache_invalidation() -> None:
    settings = api_settings()
    user = seed_user(settings)
    other = seed_user(settings)
    code = "my-alias"
    try:
        app = create_app(settings)
        app.dependency_overrides[get_current_user_optional] = lambda: CurrentUser(id=user)
        with TestClient(app) as client:
            created = client.post(
                "/api/v1/links",
                json={
                    "url": "https://93.184.216.34/path",
                    "alias": code,
                    "title": "My link",
                },
            )
            assert created.status_code == 201, created.text
            assert created.json()["code"] == code

            duplicate = client.post(
                "/api/v1/links",
                json={"url": "https://93.184.216.34/x", "alias": code},
            )
            assert duplicate.status_code == 409
            assert duplicate.json()["error"]["code"] == "alias_taken"

            reserved = client.post(
                "/api/v1/links",
                json={"url": "https://93.184.216.34/x", "alias": "login"},
            )
            assert reserved.status_code == 409
            assert reserved.json()["error"]["code"] == "alias_reserved"

            reserved_overview = client.post(
                "/api/v1/links",
                json={"url": "https://93.184.216.34/x", "alias": "overview"},
            )
            assert reserved_overview.status_code == 409
            assert reserved_overview.json()["error"]["code"] == "alias_reserved"

            listing = client.get("/api/v1/links")
            assert listing.status_code == 200
            assert listing.json()["items"][0]["code"] == code

            seed_click(settings, code, datetime.now(UTC) - timedelta(days=1))
            seed_click(settings, code, datetime.now(UTC) - timedelta(days=40))

            overview = client.get("/api/v1/links/overview")
            assert overview.status_code == 200, overview.text
            assert overview.json() == {
                "total_clicks": 1,
                "total_links": 1,
                "range": "30d",
            }
            wide_overview = client.get("/api/v1/links/overview", params={"range": "90d"})
            assert wide_overview.status_code == 200
            assert wide_overview.json()["total_clicks"] == 2

            first_redirect = client.get(f"/api/v1/r/{code}", follow_redirects=False)
            assert first_redirect.status_code == 302
            assert first_redirect.headers["location"] == "https://93.184.216.34/path"

            updated = client.patch(
                f"/api/v1/links/{code}",
                json={"original_url": "https://1.1.1.1/new", "title": "Updated"},
            )
            assert updated.status_code == 200, updated.text
            assert updated.json()["original_url"] == "https://1.1.1.1/new"

            second_redirect = client.get(f"/api/v1/r/{code}", follow_redirects=False)
            assert second_redirect.status_code == 302
            assert second_redirect.headers["location"] == "https://1.1.1.1/new"

            app.dependency_overrides[get_current_user_optional] = lambda: CurrentUser(id=other)
            assert client.get(f"/api/v1/links/{code}").status_code == 404
            assert (
                client.patch(f"/api/v1/links/{code}", json={"title": "hijack"}).status_code == 404
            )
            assert client.delete(f"/api/v1/links/{code}").status_code == 404

            app.dependency_overrides[get_current_user_optional] = lambda: CurrentUser(id=user)
            deleted = client.delete(f"/api/v1/links/{code}")
            assert deleted.status_code == 204

            gone = client.get(f"/api/v1/r/{code}", follow_redirects=False)
            assert gone.status_code == 404
            assert gone.headers["x-robots-tag"] == "noindex, nofollow"
    finally:
        cleanup(settings, codes=[code], user_ids=[user, other])


def test_expired_and_inactive_links_return_410() -> None:
    settings = api_settings()
    expired_code = "expired1"
    inactive_code = "inactive"
    seed_links(
        settings,
        [
            direct_link(
                expired_code,
                expires_at=datetime.now(UTC) - timedelta(seconds=1),
            ),
            direct_link(inactive_code, is_active=False),
        ],
    )
    try:
        with TestClient(create_app(settings)) as client:
            for code in (expired_code, inactive_code):
                response = client.get(f"/api/v1/r/{code}", follow_redirects=False)
                assert response.status_code == 410
                assert "text/html" in response.headers["content-type"]
                assert response.headers["x-robots-tag"] == "noindex, nofollow"
                assert "<html" in response.text
    finally:
        cleanup(settings, codes=[expired_code, inactive_code], user_ids=[])


def test_sqli_payloads_do_not_change_queries() -> None:
    settings = api_settings()
    user = seed_user(settings)
    code = "sqli001"
    try:
        app = create_app(settings)
        app.dependency_overrides[get_current_user_optional] = lambda: CurrentUser(id=user)
        with TestClient(app) as client:
            created = client.post(
                "/api/v1/links",
                json={"url": "https://93.184.216.34/path", "alias": code},
            )
            assert created.status_code == 201

            payload = "' OR 1=1--"
            listing = client.get("/api/v1/links", params={"q": payload})
            assert listing.status_code == 200
            assert listing.json()["items"] == []

            cursor = client.get("/api/v1/links", params={"cursor": payload})
            assert cursor.status_code == 400
            assert cursor.json()["error"]["code"] == "invalid_cursor"

            alias = client.post(
                "/api/v1/links",
                json={"url": "https://93.184.216.34/x", "alias": payload},
            )
            assert alias.status_code == 422

            invalid_url = client.post(
                "/api/v1/links",
                json={"url": "javascript:alert(1)"},
            )
            assert invalid_url.status_code == 400
            assert invalid_url.json()["error"]["code"] == "invalid_url"

            redirect = client.get("/api/v1/r/%27%20OR%201%3D1--")
            assert redirect.status_code == 404
            assert "text/html" in redirect.headers["content-type"]

            detail = client.get("/api/v1/links/%27%20OR%201%3D1--")
            assert detail.status_code == 404
    finally:
        cleanup(settings, codes=[code], user_ids=[user])


def unique_forwarded_ip() -> str:
    return f"2001:db8::{uuid4().hex[:4]}:{uuid4().hex[:4]}:{uuid4().hex[:4]}:{uuid4().hex[:4]}"


def test_create_rate_limit_returns_429() -> None:
    settings = api_settings(
        rl_create_capacity=1,
        rl_create_refill_per_sec=0.0,
    )
    code: str | None = None
    forwarded_for = unique_forwarded_ip()
    headers = {"x-forwarded-for": forwarded_for}
    try:
        with TestClient(create_app(settings)) as client:
            first = client.post(
                "/api/v1/links",
                json={"url": "https://93.184.216.34/rate"},
                headers=headers,
            )
            assert first.status_code == 201
            code = first.json()["code"]
            second = client.post(
                "/api/v1/links",
                json={"url": "https://93.184.216.34/rate2"},
                headers=headers,
            )

        assert second.status_code == 429
        assert second.json()["error"]["code"] == "rate_limited"
        assert second.headers["ratelimit-limit"] == "1"
    finally:
        cleanup(settings, codes=[code] if code else [], user_ids=[])


def test_redirect_rate_limit_returns_429() -> None:
    settings = api_settings(
        rl_redirect_capacity=1,
        rl_redirect_refill_per_sec=0.0,
    )
    code = "limit01"
    seed_links(settings, [direct_link(code)])
    forwarded_for = unique_forwarded_ip()
    headers = {"x-forwarded-for": forwarded_for}
    try:
        with TestClient(create_app(settings)) as client:
            first = client.get(
                f"/api/v1/r/{code}",
                headers=headers,
                follow_redirects=False,
            )
            second = client.get(
                f"/api/v1/r/{code}",
                headers=headers,
                follow_redirects=False,
            )

        assert first.status_code == 302
        assert second.status_code == 429
        assert second.headers["retry-after"]
        assert second.headers["ratelimit-limit"] == "1"
        assert second.json()["error"]["code"] == "rate_limited"
    finally:
        cleanup(settings, codes=[code], user_ids=[])
