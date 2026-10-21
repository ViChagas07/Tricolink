from __future__ import annotations

from uuid import UUID

from sqlalchemy import and_, delete, or_, select
from sqlalchemy.exc import IntegrityError

from tricolink.infra.db import Database
from tricolink.infra.db.models import Link as LinkRow
from tricolink.infra.db.rls import set_rls_context
from tricolink.modules.links.application.ports import PageCursor
from tricolink.modules.links.domain.entities import Link
from tricolink.modules.links.domain.errors import DuplicateCodeError
from tricolink.modules.links.domain.value_objects import OriginalUrl, ShortCode

_CODE_CONSTRAINT = "uq_links_code"


class SqlAlchemyLinkRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    async def create(self, link: Link) -> Link:
        row = LinkRow(
            code=link.code.value,
            original_url=link.original_url.value,
            title=link.title,
            user_id=link.user_id,
            is_custom_alias=link.is_custom_alias,
            is_active=link.is_active,
            expires_at=link.expires_at,
            click_count=link.click_count,
            created_at=link.created_at,
            updated_at=link.updated_at,
        )
        try:
            async with self._database.unit_of_work() as session:
                await set_rls_context(
                    session,
                    user_id=link.user_id,
                    link_code=link.code.value,
                )
                session.add(row)
                await session.flush()
        except IntegrityError as exc:
            if _is_code_conflict(exc):
                raise DuplicateCodeError(link.code.value) from exc
            raise
        return _to_domain(row)

    async def get_by_code(self, code: ShortCode) -> Link | None:
        async with self._database.read() as session:
            await set_rls_context(session, link_code=code.value)
            row = await session.scalar(select(LinkRow).where(LinkRow.code == code.value))
        return _to_domain(row) if row is not None else None

    async def get_for_user(self, code: ShortCode, user_id: UUID) -> Link | None:
        async with self._database.read() as session:
            await set_rls_context(session, user_id=user_id)
            row = await session.scalar(
                select(LinkRow).where(
                    LinkRow.code == code.value,
                    LinkRow.user_id == user_id,
                )
            )
        return _to_domain(row) if row is not None else None

    async def list_for_user(
        self,
        user_id: UUID,
        *,
        cursor: PageCursor | None,
        limit: int,
        query: str | None,
    ) -> list[Link]:
        statement = select(LinkRow).where(LinkRow.user_id == user_id)
        if query:
            pattern = f"%{_escape_like(query)}%"
            statement = statement.where(
                or_(
                    LinkRow.code.ilike(pattern, escape="\\"),
                    LinkRow.title.ilike(pattern, escape="\\"),
                )
            )
        if cursor is not None:
            statement = statement.where(
                or_(
                    LinkRow.created_at < cursor.created_at,
                    and_(
                        LinkRow.created_at == cursor.created_at,
                        LinkRow.id < cursor.link_id,
                    ),
                )
            )
        statement = statement.order_by(LinkRow.created_at.desc(), LinkRow.id.desc()).limit(limit)

        async with self._database.read() as session:
            await set_rls_context(session, user_id=user_id)
            rows = (await session.scalars(statement)).all()
        return [_to_domain(row) for row in rows]

    async def update(self, link: Link, user_id: UUID) -> Link | None:
        async with self._database.unit_of_work() as session:
            await set_rls_context(session, user_id=user_id)
            row = await session.scalar(
                select(LinkRow)
                .where(LinkRow.code == link.code.value, LinkRow.user_id == user_id)
                .with_for_update()
            )
            if row is None:
                return None
            row.title = link.title
            row.original_url = link.original_url.value
            row.is_active = link.is_active
            row.expires_at = link.expires_at
            row.updated_at = link.updated_at
            await session.flush()
            await session.refresh(row)
        return _to_domain(row)

    async def delete(self, code: ShortCode, user_id: UUID) -> bool:
        async with self._database.unit_of_work() as session:
            await set_rls_context(session, user_id=user_id)
            deleted_id = await session.scalar(
                delete(LinkRow)
                .where(LinkRow.code == code.value, LinkRow.user_id == user_id)
                .returning(LinkRow.id)
            )
        return deleted_id is not None


def _to_domain(row: LinkRow) -> Link:
    return Link(
        id=row.id,
        code=ShortCode(row.code),
        original_url=OriginalUrl.parse(row.original_url),
        title=row.title,
        user_id=row.user_id,
        is_custom_alias=row.is_custom_alias,
        is_active=row.is_active,
        expires_at=row.expires_at,
        click_count=row.click_count,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _escape_like(value: str) -> str:
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def _is_code_conflict(exc: IntegrityError) -> bool:
    original = exc.orig
    constraint = getattr(original, "constraint_name", None)
    return constraint == _CODE_CONSTRAINT or _CODE_CONSTRAINT in str(original)
