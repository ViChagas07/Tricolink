from __future__ import annotations

import asyncio
import json
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime, timedelta
from typing import Any, cast

import structlog
from sqlalchemy import CursorResult, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement

from tricolink.core.config import Settings, get_settings
from tricolink.core.logging import configure_logging
from tricolink.infra.db import Database
from tricolink.infra.db.models import ClickEvent, Link

logger = structlog.get_logger(__name__)


@dataclass(frozen=True, slots=True)
class CleanupResult:
    click_events_deleted: int
    expired_links_deleted: int
    cutoff: str
    batches: int


async def _delete_batch(
    session: AsyncSession,
    *,
    model: type[ClickEvent] | type[Link],
    condition: ColumnElement[bool],
    batch_size: int,
) -> int:
    ids = (await session.scalars(select(model.id).where(condition).limit(batch_size))).all()
    if not ids:
        return 0
    result = cast(CursorResult[Any], await session.execute(delete(model).where(model.id.in_(ids))))
    return result.rowcount or 0


async def run_cleanup(
    settings: Settings,
    *,
    now: datetime | None = None,
    click_retention_days: int | None = None,
    batch_size: int | None = None,
) -> CleanupResult:
    current = now or datetime.now(UTC)
    retention = click_retention_days or settings.click_retention_days
    limit = batch_size or settings.cleanup_batch_size
    cutoff = current - timedelta(days=retention)

    if settings.migration_database_url is None:
        logger.warning(
            "cleanup_without_migration_url",
            detail="expired links may be hidden by RLS",
        )

    admin = replace(
        settings,
        database_url=settings.migration_database_url or settings.database_url,
    )
    database = Database(admin)
    clicks = 0
    links = 0
    batches = 0

    try:
        while True:
            async with database.unit_of_work() as session:
                deleted = await _delete_batch(
                    session,
                    model=ClickEvent,
                    condition=ClickEvent.clicked_at < cutoff,
                    batch_size=limit,
                )
            batches += 1
            clicks += deleted
            if deleted < limit:
                break

        while True:
            async with database.unit_of_work() as session:
                deleted = await _delete_batch(
                    session,
                    model=Link,
                    condition=Link.expires_at.is_not(None) & (Link.expires_at < current),
                    batch_size=limit,
                )
            batches += 1
            links += deleted
            if deleted < limit:
                break
    finally:
        await database.dispose()

    result = CleanupResult(
        click_events_deleted=clicks,
        expired_links_deleted=links,
        cutoff=cutoff.isoformat(),
        batches=batches,
    )
    logger.info(
        "cleanup_finished",
        click_events_deleted=result.click_events_deleted,
        expired_links_deleted=result.expired_links_deleted,
        cutoff=result.cutoff,
    )
    return result


def main() -> int:
    settings = get_settings()
    configure_logging(settings)
    result = asyncio.run(run_cleanup(settings))
    print(json.dumps(asdict(result), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
