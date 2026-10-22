from __future__ import annotations

import asyncio
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from fastapi.testclient import TestClient
from redis.asyncio import Redis
from sqlalchemy import delete, select

from tricolink.core.config import Settings
from tricolink.infra.cache import create_redis
from tricolink.infra.db import Database
from tricolink.infra.db.models import ClickEvent as ClickEventRow
from tricolink.infra.db.models import Link as LinkRow
from tricolink.infra.db.models import RefreshToken as RefreshTokenRow
from tricolink.infra.db.models import User as UserRow
from tricolink.main import create_app
from tricolink.modules.analytics.adapters.stats_cache import STATS_KEY, STATS_LOCK_KEY
from tricolink.modules.links.adapters.cache import (
    GENERATION_KEY,
    LINK_KEY,
    LOCK_KEY,
    NEGATIVE_KEY,
)
from tricolink.modules.links.adapters.repository import SqlAlchemyLinkRepository
from tricolink.modules.links.domain.entities import Link
from tricolink.modules.links.domain.value_objects import OriginalUrl, ShortCode

DESTINATION = "https://93.184.216.34/security"


def security_settings(**overrides: object) -> Settings:
    unique = uuid4().hex[:10]
    base = replace(
        Settings.from_env(),
        app_env="test",
        click_flusher_enabled=False,
        click_stream_key=f"test:security-clicks:{unique}",
        click_stream_group=f"test-security-clicks-{unique}",
        frontend_origin="http://frontend.test",
        api_public_base_url="http://api.test",
        short_base_url="https://short.test",
        cookie_secure=False,
        jwt_secret="j" * 48,
        csrf_secret="c" * 48,
        session_secret="s" * 48,
        metrics_token="m" * 48,
        trusted_proxy_count=1,
        rl_auth_capacity=1000,
        rl_auth_refill_per_sec=1000,
        rl_create_capacity=1000,
        rl_create_refill_per_sec=1000,
        rl_redirect_capacity=1000,
        rl_redirect_refill_per_sec=1000,
        rl_global_capacity=100_000,
        rl_global_refill_per_sec=100_000,
        rl_list_capacity=1000,
        rl_list_refill_per_sec=1000,
        anon_daily_link_limit=1000,
        user_daily_link_limit=1000,
        argon2_time_cost=1,
        argon2_memory_kib=1_024,
        argon2_parallelism=1,
        argon2_hash_len=16,
        argon2_salt_len=8,
        auth_lockout_threshold=100,
    )
    return replace(base, **overrides)


def admin_settings(settings: Settings) -> Settings:
    return replace(
        settings,
        database_url=settings.migration_database_url or settings.database_url,
    )


def unique_ip() -> str:
    return f"2001:db8::{uuid4().hex[:4]}:{uuid4().hex[:4]}:{uuid4().hex[:4]}:{uuid4().hex[:4]}"


def make_client(
    app: object,
    *,
    forwarded_for: str | None = None,
    base_url: str = "http://testserver",
) -> TestClient:
    headers = {"X-Forwarded-For": forwarded_for} if forwarded_for else None
    return TestClient(app, headers=headers, base_url=base_url)


async def aseed_user(settings: Settings, *, email: str | None = None) -> UUID:
    user_id = uuid4()
    database = Database(settings)
    try:
        async with database.unit_of_work() as session:
            session.add(
                UserRow(
                    id=user_id,
                    email=email or f"security-{user_id}@example.com",
                    password_hash=None,
                )
            )
    finally:
        await database.dispose()
    return user_id


def seed_user(settings: Settings, *, email: str | None = None) -> UUID:
    return asyncio.run(aseed_user(settings, email=email))


async def aseed_link(
    settings: Settings,
    *,
    code: str,
    user_id: UUID | None = None,
    url: str = DESTINATION,
    title: str | None = "Security seed",
) -> Link:
    now = datetime.now(UTC)
    link = Link(
        id=None,
        code=ShortCode(code),
        original_url=OriginalUrl.parse(url),
        title=title,
        user_id=user_id,
        is_custom_alias=False,
        is_active=True,
        expires_at=None,
        click_count=0,
        created_at=now,
        updated_at=now,
    )
    database = Database(settings)
    repository = SqlAlchemyLinkRepository(database)
    try:
        return await repository.create(link)
    finally:
        await database.dispose()


def seed_link(
    settings: Settings,
    *,
    code: str,
    user_id: UUID | None = None,
    url: str = DESTINATION,
    title: str | None = "Security seed",
) -> Link:
    return asyncio.run(aseed_link(settings, code=code, user_id=user_id, url=url, title=title))


async def aseed_click(
    settings: Settings,
    *,
    link_id: int,
    clicked_at: datetime | None = None,
) -> None:
    database = Database(admin_settings(settings))
    try:
        async with database.unit_of_work() as session:
            session.add(
                ClickEventRow(
                    link_id=link_id,
                    clicked_at=clicked_at or datetime.now(UTC),
                    device="unknown",
                )
            )
    finally:
        await database.dispose()


def seed_click(settings: Settings, *, link_id: int, clicked_at: datetime | None = None) -> None:
    asyncio.run(aseed_click(settings, link_id=link_id, clicked_at=clicked_at))


async def acleanup(settings: Settings, *, codes: list[str], user_ids: list[UUID]) -> None:
    database = Database(admin_settings(settings))
    link_ids: list[int] = []
    try:
        async with database.unit_of_work() as session:
            if codes:
                link_ids = list(
                    (await session.scalars(select(LinkRow.id).where(LinkRow.code.in_(codes)))).all()
                )
                await session.execute(delete(LinkRow).where(LinkRow.code.in_(codes)))
            for user_id in user_ids:
                await session.execute(
                    delete(RefreshTokenRow).where(RefreshTokenRow.user_id == user_id)
                )
                await session.execute(delete(UserRow).where(UserRow.id == user_id))
    finally:
        await database.dispose()

    redis: Redis = create_redis(settings)
    try:
        keys: list[str] = []
        for code in codes:
            keys.extend(
                (
                    LINK_KEY.format(code=code),
                    LOCK_KEY.format(code=code),
                    NEGATIVE_KEY.format(code=code),
                    GENERATION_KEY.format(code=code),
                )
            )
        for link_id in link_ids:
            for range_key in ("7d", "30d", "90d"):
                keys.append(STATS_KEY.format(link_id=link_id, range=range_key))
                keys.append(STATS_LOCK_KEY.format(link_id=link_id, range=range_key))
        if keys:
            await redis.delete(*keys)
    finally:
        await redis.aclose()


def cleanup(settings: Settings, *, codes: list[str], user_ids: list[UUID]) -> None:
    asyncio.run(acleanup(settings, codes=codes, user_ids=user_ids))


async def acleanup_email(settings: Settings, email: str) -> None:
    database = Database(admin_settings(settings))
    try:
        async with database.unit_of_work() as session:
            user_ids = list(
                (await session.scalars(select(UserRow.id).where(UserRow.email == email))).all()
            )
            for user_id in user_ids:
                await session.execute(
                    delete(RefreshTokenRow).where(RefreshTokenRow.user_id == user_id)
                )
                await session.execute(delete(LinkRow).where(LinkRow.user_id == user_id))
                await session.execute(delete(UserRow).where(UserRow.id == user_id))
    finally:
        await database.dispose()


def cleanup_email(settings: Settings, email: str) -> None:
    asyncio.run(acleanup_email(settings, email))


def build_app(settings: Settings) -> object:
    return create_app(settings)


def expires_in(days: int = 1) -> datetime:
    return datetime.now(UTC) + timedelta(days=days)
