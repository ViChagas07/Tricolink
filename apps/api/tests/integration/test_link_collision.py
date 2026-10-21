from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy import delete

from tricolink.core.config import Settings
from tricolink.infra.db import Database
from tricolink.infra.db.models import Link as LinkRow
from tricolink.modules.links.adapters.repository import SqlAlchemyLinkRepository
from tricolink.modules.links.application import (
    CreateLink,
    CreateLinkCommand,
    QuotaResult,
)
from tricolink.modules.links.domain.entities import Link
from tricolink.modules.links.domain.url_policy import UrlPolicy
from tricolink.modules.links.domain.value_objects import OriginalUrl, ShortCode
from tricolink.shared_kernel.clock import SystemClock

pytestmark = pytest.mark.integration


class SequenceGenerator:
    def __init__(self, values: list[str]) -> None:
        self.values = list(values)

    def generate(self) -> str:
        return self.values.pop(0)


class AllowedQuota:
    async def consume(self, scope: str, key: str, limit: int) -> QuotaResult:
        return QuotaResult(
            allowed=True,
            used=1,
            limit=limit,
            retry_after_seconds=60,
        )


class NoopCache:
    async def invalidate(self, code: ShortCode) -> None:
        return None

    async def resolve(self, *args: object, **kwargs: object) -> object:
        return None


class EmptyResolver:
    async def resolve(self, host: str) -> list[str]:
        return []


@pytest.mark.asyncio
async def test_real_integrity_error_triggers_code_retry() -> None:
    settings = Settings.from_env()
    database = Database(settings)
    repository = SqlAlchemyLinkRepository(database)
    now = datetime.now(UTC)
    existing_code = f"x{uuid4().hex[:6]}"
    retry_code = f"r{uuid4().hex[:6]}"
    existing = Link(
        id=None,
        code=ShortCode(existing_code),
        original_url=OriginalUrl.parse("https://93.184.216.34/existing"),
        title=None,
        user_id=None,
        is_custom_alias=False,
        is_active=True,
        expires_at=None,
        click_count=0,
        created_at=now,
        updated_at=now,
    )
    generator = SequenceGenerator([existing_code, retry_code])
    use_case = CreateLink(
        repository=repository,
        cache=NoopCache(),  # type: ignore[arg-type]
        url_policy=UrlPolicy(resolver=EmptyResolver(), own_hosts=()),
        code_generator=generator,  # type: ignore[arg-type]
        quota=AllowedQuota(),
        clock=SystemClock(),
        anon_daily_limit=100,
        user_daily_limit=100,
        anon_ttl_days=30,
    )

    try:
        await repository.create(existing)
        created = await use_case.execute(
            CreateLinkCommand(
                url="https://93.184.216.34/new",
                user_id=None,
                client_ip="203.0.113.5",
            )
        )
        assert created.code.value == retry_code
        assert generator.values == []
        assert await repository.get_by_code(ShortCode(existing_code)) is not None
        assert await repository.get_by_code(ShortCode(retry_code)) is not None
    finally:
        admin = Database(
            replace(
                settings,
                database_url=settings.migration_database_url or settings.database_url,
            )
        )
        try:
            async with admin.unit_of_work() as session:
                await session.execute(
                    delete(LinkRow).where(LinkRow.code.in_([existing_code, retry_code]))
                )
        finally:
            await admin.dispose()
        await database.dispose()
