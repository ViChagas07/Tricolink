from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest
from sqlalchemy import delete

from tricolink.core.config import Settings
from tricolink.infra.db import Database
from tricolink.infra.db.models import Link as LinkRow
from tricolink.infra.db.models import User as UserRow
from tricolink.modules.links.adapters.repository import SqlAlchemyLinkRepository
from tricolink.modules.links.application.ports import PageCursor
from tricolink.modules.links.domain.entities import Link
from tricolink.modules.links.domain.value_objects import OriginalUrl, ShortCode

pytestmark = pytest.mark.integration


def build_link(
    code: str,
    *,
    user_id: UUID | None,
    created_at: datetime,
    title: str | None = None,
    url: str = "https://93.184.216.34/path",
) -> Link:
    return Link(
        id=None,
        code=ShortCode(code),
        original_url=OriginalUrl.parse(url),
        title=title,
        user_id=user_id,
        is_custom_alias=False,
        is_active=True,
        expires_at=None,
        click_count=0,
        created_at=created_at,
        updated_at=created_at,
    )


async def seed_user(database: Database) -> UUID:
    user_id = uuid4()
    async with database.unit_of_work() as session:
        session.add(
            UserRow(
                id=user_id,
                email=f"links-{user_id}@example.com",
                password_hash=None,
            )
        )
    return user_id


async def cleanup(database: Database, codes: list[str], user_id: UUID | None) -> None:
    async with database.unit_of_work() as session:
        await session.execute(delete(LinkRow).where(LinkRow.code.in_(codes)))
        if user_id is not None:
            await session.execute(delete(UserRow).where(UserRow.id == user_id))


@pytest.mark.asyncio
async def test_repository_crud_list_search_and_owner_filter() -> None:
    database = Database(Settings.from_env())
    repository = SqlAlchemyLinkRepository(database)
    user_id = await seed_user(database)
    other_id = await seed_user(database)
    now = datetime.now(UTC)
    codes = ["repo001", "repo002", "repo003"]

    try:
        for index, code in enumerate(codes):
            await repository.create(
                build_link(
                    code,
                    user_id=user_id,
                    created_at=now - timedelta(minutes=index),
                    title=f"Title {index}",
                )
            )

        found = await repository.get_by_code(ShortCode(codes[0]))
        assert found is not None
        assert found.user_id == user_id

        assert await repository.get_for_user(ShortCode(codes[0]), other_id) is None

        page = await repository.list_for_user(
            user_id,
            cursor=None,
            limit=2,
            query=None,
        )
        assert [item.code.value for item in page] == ["repo001", "repo002"]
        second = await repository.list_for_user(
            user_id,
            cursor=PageCursor(created_at=page[-1].created_at, link_id=page[-1].id or 0),
            limit=2,
            query=None,
        )
        assert [item.code.value for item in second] == ["repo003"]

        search = await repository.list_for_user(
            user_id,
            cursor=None,
            limit=10,
            query="title 1",
        )
        assert [item.code.value for item in search] == ["repo002"]

        wildcard = await repository.list_for_user(
            user_id,
            cursor=None,
            limit=10,
            query="%",
        )
        assert wildcard == []

        sqli = await repository.list_for_user(
            user_id,
            cursor=None,
            limit=10,
            query="' OR 1=1--",
        )
        assert sqli == []

        target = page[0]
        updated = await repository.update(
            target.with_updates(
                title="changed",
                original_url=OriginalUrl.parse("https://1.1.1.1/changed"),
                is_active=False,
                expires_at=now + timedelta(days=1),
                updated_at=now,
            ),
            user_id,
        )
        assert updated is not None
        assert updated.title == "changed"
        assert updated.is_active is False

        assert await repository.update(target, other_id) is None
        assert await repository.delete(ShortCode(codes[2]), other_id) is False
        assert await repository.delete(ShortCode(codes[2]), user_id) is True
        assert await repository.get_by_code(ShortCode(codes[2])) is None
    finally:
        await cleanup(database, codes, user_id)
        await cleanup(database, [], other_id)
        await database.dispose()


@pytest.mark.asyncio
async def test_repository_returns_none_for_non_owned_management_reads() -> None:
    database = Database(Settings.from_env())
    repository = SqlAlchemyLinkRepository(database)
    owner = await seed_user(database)
    other = await seed_user(database)
    code = "repo010"
    try:
        await repository.create(build_link(code, user_id=owner, created_at=datetime.now(UTC)))
        assert await repository.get_for_user(ShortCode(code), other) is None
    finally:
        await cleanup(database, [code], owner)
        await cleanup(database, [], other)
        await database.dispose()
