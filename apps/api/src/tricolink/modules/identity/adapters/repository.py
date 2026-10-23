from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from tricolink.infra.db import Database
from tricolink.infra.db.models import RefreshToken as RefreshTokenRow
from tricolink.infra.db.models import User as UserRow
from tricolink.infra.db.models import UserAvatar as UserAvatarRow
from tricolink.infra.db.rls import set_rls_context
from tricolink.modules.identity.application.ports import RotationResult, RotationStatus
from tricolink.modules.identity.domain.email import Email
from tricolink.modules.identity.domain.entities import AvatarImage, User
from tricolink.modules.identity.domain.errors import DuplicateUserError


class SqlAlchemyUserRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    async def get_by_id(self, user_id: UUID) -> User | None:
        async with self._database.read() as session:
            row = await session.get(UserRow, user_id)
        return _to_user(row) if row is not None else None

    async def get_by_email(self, email: Email) -> User | None:
        async with self._database.read() as session:
            row = await session.scalar(select(UserRow).where(UserRow.email == email.value))
        return _to_user(row) if row is not None else None

    async def get_by_google_sub(self, google_sub: str) -> User | None:
        async with self._database.read() as session:
            row = await session.scalar(select(UserRow).where(UserRow.google_sub == google_sub))
        return _to_user(row) if row is not None else None

    async def create(self, user: User) -> User:
        row = UserRow(
            id=user.id,
            email=user.email.value,
            password_hash=user.password_hash,
            google_sub=user.google_sub,
            display_name=user.display_name,
            locale=user.locale,
            google_avatar_url=user.google_avatar_url,
            avatar_updated_at=user.avatar_updated_at,
            is_active=user.is_active,
            created_at=user.created_at,
        )
        try:
            async with self._database.unit_of_work() as session:
                session.add(row)
                await session.flush()
        except IntegrityError as exc:
            raise DuplicateUserError() from exc
        return _to_user(row)

    async def link_google(
        self,
        user_id: UUID,
        *,
        google_sub: str,
        display_name: str | None,
    ) -> User | None:
        try:
            async with self._database.unit_of_work() as session:
                row = await session.scalar(
                    select(UserRow).where(UserRow.id == user_id).with_for_update()
                )
                if row is None:
                    return None
                row.google_sub = google_sub
                if row.display_name is None and display_name:
                    row.display_name = display_name
                await session.flush()
                await session.refresh(row)
        except IntegrityError as exc:
            raise DuplicateUserError() from exc
        return _to_user(row)

    async def update_profile(
        self,
        user_id: UUID,
        *,
        display_name: str | None,
        locale: str | None,
    ) -> User | None:
        async with self._database.unit_of_work() as session:
            row = await session.scalar(
                select(UserRow).where(UserRow.id == user_id).with_for_update()
            )
            if row is None:
                return None
            row.display_name = display_name
            row.locale = locale
            await session.flush()
            await session.refresh(row)
        return _to_user(row)

    async def update_google_avatar(
        self,
        user_id: UUID,
        *,
        google_avatar_url: str,
    ) -> User | None:
        async with self._database.unit_of_work() as session:
            row = await session.scalar(
                select(UserRow).where(UserRow.id == user_id).with_for_update()
            )
            if row is None:
                return None
            row.google_avatar_url = google_avatar_url
            await session.flush()
            await session.refresh(row)
        return _to_user(row)

    async def set_avatar(
        self,
        user_id: UUID,
        *,
        content_type: str,
        content: bytes,
        updated_at: datetime,
    ) -> User | None:
        async with self._database.unit_of_work() as session:
            await set_rls_context(session, user_id=user_id)
            await session.execute(
                pg_insert(UserAvatarRow)
                .values(
                    user_id=user_id,
                    content_type=content_type,
                    content=content,
                    updated_at=updated_at,
                )
                .on_conflict_do_update(
                    index_elements=[UserAvatarRow.user_id],
                    set_={
                        "content_type": content_type,
                        "content": content,
                        "updated_at": updated_at,
                    },
                )
            )
            row = await session.scalar(
                select(UserRow).where(UserRow.id == user_id).with_for_update()
            )
            if row is None:
                return None
            row.avatar_updated_at = updated_at
            await session.flush()
            await session.refresh(row)
        return _to_user(row)

    async def delete_avatar(self, user_id: UUID) -> User | None:
        async with self._database.unit_of_work() as session:
            await set_rls_context(session, user_id=user_id)
            await session.execute(delete(UserAvatarRow).where(UserAvatarRow.user_id == user_id))
            row = await session.scalar(
                select(UserRow).where(UserRow.id == user_id).with_for_update()
            )
            if row is None:
                return None
            row.avatar_updated_at = None
            await session.flush()
            await session.refresh(row)
        return _to_user(row)

    async def get_avatar(self, user_id: UUID) -> AvatarImage | None:
        async with self._database.read() as session:
            await set_rls_context(session, user_id=user_id)
            row = await session.get(UserAvatarRow, user_id)
        if row is None:
            return None
        return AvatarImage(content_type=row.content_type, content=row.content)


class SqlAlchemySessionRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    async def create_session(
        self,
        *,
        user_id: UUID,
        family_id: UUID,
        token_hash: str,
        expires_at: datetime,
        created_at: datetime,
    ) -> None:
        async with self._database.unit_of_work() as session:
            await set_rls_context(session, user_id=user_id)
            session.add(
                RefreshTokenRow(
                    id=uuid4(),
                    user_id=user_id,
                    family_id=family_id,
                    token_hash=token_hash,
                    expires_at=expires_at,
                    revoked_at=None,
                    created_at=created_at,
                )
            )

    async def rotate(
        self,
        *,
        token_hash: str,
        new_token_hash: str,
        new_expires_at: datetime,
        now: datetime,
    ) -> RotationResult:
        result = RotationResult(status=RotationStatus.INVALID)
        async with self._database.unit_of_work() as session:
            await set_rls_context(session, refresh_token_hash=token_hash)
            row = await session.scalar(
                select(RefreshTokenRow)
                .where(RefreshTokenRow.token_hash == token_hash)
                .with_for_update()
            )
            if row is None:
                return result

            await set_rls_context(
                session,
                user_id=row.user_id,
                refresh_family_id=row.family_id,
                refresh_token_hash=token_hash,
            )

            if row.revoked_at is not None:
                await _revoke_family(session, row.family_id, now)
                result = RotationResult(
                    status=RotationStatus.REUSED,
                    user_id=row.user_id,
                    family_id=row.family_id,
                )
                return result

            if row.expires_at <= now:
                await _revoke_family(session, row.family_id, now)
                result = RotationResult(
                    status=RotationStatus.EXPIRED,
                    user_id=row.user_id,
                    family_id=row.family_id,
                )
                return result

            row.revoked_at = now
            session.add(
                RefreshTokenRow(
                    id=uuid4(),
                    user_id=row.user_id,
                    family_id=row.family_id,
                    token_hash=new_token_hash,
                    expires_at=new_expires_at,
                    revoked_at=None,
                    created_at=now,
                )
            )
            result = RotationResult(
                status=RotationStatus.ROTATED,
                user_id=row.user_id,
                family_id=row.family_id,
            )
        return result

    async def revoke_family_by_hash(self, token_hash: str, now: datetime) -> bool:
        async with self._database.unit_of_work() as session:
            await set_rls_context(session, refresh_token_hash=token_hash)
            row = await session.scalar(
                select(RefreshTokenRow)
                .where(RefreshTokenRow.token_hash == token_hash)
                .with_for_update()
            )
            if row is None:
                return False
            await set_rls_context(
                session,
                user_id=row.user_id,
                refresh_family_id=row.family_id,
                refresh_token_hash=token_hash,
            )
            await _revoke_family(session, row.family_id, now)
            return True


async def _revoke_family(
    session: AsyncSession,
    family_id: UUID,
    now: datetime,
) -> None:
    await session.execute(
        update(RefreshTokenRow)
        .where(
            RefreshTokenRow.family_id == family_id,
            RefreshTokenRow.revoked_at.is_(None),
        )
        .values(revoked_at=now)
    )


def _to_user(row: UserRow) -> User:
    return User(
        id=row.id,
        email=Email.parse(row.email),
        password_hash=row.password_hash,
        google_sub=row.google_sub,
        display_name=row.display_name,
        locale=row.locale,
        is_active=row.is_active,
        created_at=row.created_at,
        google_avatar_url=row.google_avatar_url,
        avatar_updated_at=row.avatar_updated_at,
    )
