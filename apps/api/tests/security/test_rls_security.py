from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import delete, select, text, update

from tricolink.core.config import Settings
from tricolink.infra.db import Database
from tricolink.infra.db.models import Link as LinkRow
from tricolink.infra.db.models import RefreshToken as RefreshTokenRow
from tricolink.infra.db.rls import set_rls_context
from tricolink.modules.identity.adapters.repository import SqlAlchemySessionRepository

from .helpers import acleanup, aseed_link, aseed_user, security_settings

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_runtime_role_has_rls_enforced() -> None:
    settings = Settings.from_env()
    database = Database(settings)
    try:
        async with database.read() as session:
            row = (
                await session.execute(
                    text(
                        "SELECT rolsuper, rolbypassrls "
                        "FROM pg_roles WHERE rolname = current_user"
                    )
                )
            ).one()
        assert row.rolsuper is False, "runtime role must not be a superuser"
        assert row.rolbypassrls is False, "runtime role must not bypass RLS"
    finally:
        await database.dispose()


@pytest.mark.asyncio
async def test_private_tables_return_nothing_without_rls_context() -> None:
    settings = security_settings()
    user = await aseed_user(settings)
    code = f"rl{uuid4().hex[:6]}"
    link = await aseed_link(settings, code=code, user_id=user)
    database = Database(settings)
    sessions = SqlAlchemySessionRepository(database)
    token_hash = uuid4().hex * 2
    await sessions.create_session(
        user_id=user,
        family_id=uuid4(),
        token_hash=token_hash,
        expires_at=datetime.now(UTC) + timedelta(days=1),
        created_at=datetime.now(UTC),
    )

    try:
        async with database.read() as session:
            assert (await session.scalars(select(LinkRow))).all() == []
            assert (await session.scalars(select(RefreshTokenRow))).all() == []
            assert (await session.execute(text("SELECT id FROM links"))).all() == []
            assert (
                await session.execute(text("SELECT token_hash FROM refresh_tokens"))
            ).all() == []

        async with database.read() as session:
            await set_rls_context(session, user_id=user)
            visible_links = (await session.scalars(select(LinkRow))).all()
            visible_tokens = (await session.scalars(select(RefreshTokenRow))).all()
        assert [row.code for row in visible_links] == [code]
        assert [row.token_hash for row in visible_tokens] == [token_hash]

        async with database.read() as session:
            await set_rls_context(session, user_id=uuid4())
            assert (await session.scalars(select(LinkRow))).all() == []
            assert (await session.scalars(select(RefreshTokenRow))).all() == []

        async with database.read() as session:
            await set_rls_context(session, link_code=code)
            assert [row.code for row in (await session.scalars(select(LinkRow))).all()] == [code]

        async with database.unit_of_work() as session:
            await set_rls_context(session, user_id=user)
            updated = await session.execute(
                update(LinkRow).where(LinkRow.code == code).values(title="same owner")
            )
            assert updated.rowcount == 1

        async with database.unit_of_work() as session:
            await set_rls_context(session, user_id=uuid4())
            updated = await session.execute(
                update(LinkRow).where(LinkRow.code == code).values(title="stolen")
            )
            assert updated.rowcount == 0
            deleted = await session.execute(delete(LinkRow).where(LinkRow.code == code))
            assert deleted.rowcount == 0

        async with database.read() as session:
            stored = await session.get(LinkRow, link.id)
        assert stored is None  # no context, RLS hides it
    finally:
        await database.dispose()
        await acleanup(settings, codes=[code], user_ids=[user])


@pytest.mark.asyncio
async def test_anonymous_links_are_not_visible_without_the_code_context() -> None:
    settings = security_settings()
    code = f"an{uuid4().hex[:6]}"
    await aseed_link(settings, code=code, user_id=None)
    database = Database(settings)

    try:
        async with database.read() as session:
            assert (await session.scalars(select(LinkRow))).all() == []

        async with database.read() as session:
            await set_rls_context(session, link_code=code)
            rows = (await session.scalars(select(LinkRow))).all()
        assert [row.code for row in rows] == [code]
    finally:
        await database.dispose()
        await acleanup(settings, codes=[code], user_ids=[])
