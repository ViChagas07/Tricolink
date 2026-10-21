from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest
from sqlalchemy import delete, select, update

from tricolink.core.config import Settings
from tricolink.infra.db import Database
from tricolink.infra.db.models import Link as LinkRow
from tricolink.infra.db.models import RefreshToken as RefreshTokenRow
from tricolink.infra.db.models import User as UserRow
from tricolink.infra.db.rls import set_rls_context
from tricolink.modules.identity.adapters.repository import (
    SqlAlchemySessionRepository,
    SqlAlchemyUserRepository,
)
from tricolink.modules.identity.domain import Email, User
from tricolink.modules.links.adapters.repository import SqlAlchemyLinkRepository
from tricolink.modules.links.domain import Link
from tricolink.modules.links.domain.value_objects import OriginalUrl, ShortCode

pytestmark = pytest.mark.integration


def admin_settings(settings: Settings) -> Settings:
    return replace(
        settings,
        database_url=settings.migration_database_url or settings.database_url,
    )


async def make_user(users: SqlAlchemyUserRepository, email: str) -> User:
    return await users.create(
        User(
            id=uuid4(),
            email=Email.parse(email),
            password_hash=None,
            google_sub=None,
            display_name=None,
            locale=None,
            is_active=True,
            created_at=datetime.now(UTC),
        )
    )


async def make_link(
    links: SqlAlchemyLinkRepository,
    *,
    code: str,
    user_id: UUID,
) -> Link:
    now = datetime.now(UTC)
    return await links.create(
        Link(
            id=None,
            code=ShortCode(code),
            original_url=OriginalUrl.parse("https://93.184.216.34/path"),
            title=None,
            user_id=user_id,
            is_custom_alias=False,
            is_active=True,
            expires_at=None,
            click_count=0,
            created_at=now,
            updated_at=now,
        )
    )


@pytest.mark.asyncio
async def test_rls_blocks_cross_user_reads_even_without_app_filter() -> None:
    settings = Settings.from_env()
    database = Database(settings)
    users = SqlAlchemyUserRepository(database)
    links = SqlAlchemyLinkRepository(database)
    sessions = SqlAlchemySessionRepository(database)
    user_a = await make_user(users, f"rls-a-{uuid4()}@example.com")
    user_b = await make_user(users, f"rls-b-{uuid4()}@example.com")
    code_a = f"a{uuid4().hex[:6]}"
    code_b = f"b{uuid4().hex[:6]}"
    hash_a = uuid4().hex * 2
    hash_b = uuid4().hex * 2
    now = datetime.now(UTC)

    try:
        await make_link(links, code=code_a, user_id=user_a.id)
        await make_link(links, code=code_b, user_id=user_b.id)
        await sessions.create_session(
            user_id=user_a.id,
            family_id=uuid4(),
            token_hash=hash_a,
            expires_at=now + timedelta(days=1),
            created_at=now,
        )
        await sessions.create_session(
            user_id=user_b.id,
            family_id=uuid4(),
            token_hash=hash_b,
            expires_at=now + timedelta(days=1),
            created_at=now,
        )

        # No context => default deny.
        async with database.read() as session:
            assert (await session.scalars(select(LinkRow))).all() == []
            assert (await session.scalars(select(RefreshTokenRow))).all() == []

        # Owner context, deliberately without any application WHERE clause.
        async with database.read() as session:
            await set_rls_context(session, user_id=user_a.id)
            visible_links = (await session.scalars(select(LinkRow))).all()
            visible_tokens = (await session.scalars(select(RefreshTokenRow))).all()

        assert [row.code for row in visible_links] == [code_a]
        assert [row.token_hash for row in visible_tokens] == [hash_a]

        # Public redirect context sees only the requested code.
        async with database.read() as session:
            await set_rls_context(session, link_code=code_b)
            public = (await session.scalars(select(LinkRow))).all()
        assert [row.code for row in public] == [code_b]

        # The refresh lookup can see only the presented hash before login.
        async with database.read() as session:
            await set_rls_context(session, refresh_token_hash=hash_b)
            token = await session.scalar(
                select(RefreshTokenRow).where(RefreshTokenRow.token_hash == hash_b)
            )
        assert token is not None and token.user_id == user_b.id

        # Cross-user mutation is blocked by RLS as well.
        async with database.unit_of_work() as session:
            await set_rls_context(session, user_id=user_a.id)
            result = await session.execute(
                update(LinkRow).where(LinkRow.code == code_b).values(title="stolen")
            )
            assert result.rowcount == 0
    finally:
        admin = Database(admin_settings(settings))
        try:
            async with admin.unit_of_work() as session:
                await session.execute(
                    delete(RefreshTokenRow).where(RefreshTokenRow.token_hash.in_([hash_a, hash_b]))
                )
                await session.execute(delete(LinkRow).where(LinkRow.code.in_([code_a, code_b])))
                await session.execute(delete(UserRow).where(UserRow.id.in_([user_a.id, user_b.id])))
        finally:
            await admin.dispose()
        await database.dispose()
