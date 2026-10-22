from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import delete, func, select

from tests.security.helpers import security_settings
from tricolink.infra.db import Database
from tricolink.infra.db.models import ClickEvent as ClickEventRow
from tricolink.infra.db.models import Link as LinkRow
from tricolink.jobs.cleanup import run_cleanup


@pytest.mark.asyncio
async def test_cleanup_deletes_old_clicks_and_expired_links_idempotently() -> None:
    settings = security_settings(click_retention_days=365, cleanup_batch_size=2)
    admin = Database(
        replace(
            settings,
            database_url=settings.migration_database_url or settings.database_url,
        )
    )
    now = datetime.now(UTC)
    active_code = f"cl{uuid4().hex[:6]}"
    expired_code = f"cl{uuid4().hex[:6]}"
    active_id: int | None = None
    expired_id: int | None = None

    try:
        async with admin.unit_of_work() as session:
            active = LinkRow(
                code=active_code,
                original_url="https://93.184.216.34/cleanup-active",
                is_active=True,
                expires_at=None,
                click_count=0,
            )
            expired = LinkRow(
                code=expired_code,
                original_url="https://93.184.216.34/cleanup-expired",
                is_active=True,
                expires_at=now - timedelta(days=1),
                click_count=0,
            )
            session.add_all([active, expired])
            await session.flush()
            active_id = active.id
            expired_id = expired.id
            session.add_all(
                [
                    ClickEventRow(
                        link_id=active_id,
                        clicked_at=now - timedelta(days=400),
                        device="unknown",
                    )
                    for _ in range(5)
                ]
            )
            session.add(
                ClickEventRow(
                    link_id=active_id,
                    clicked_at=now - timedelta(days=1),
                    device="unknown",
                )
            )
            session.add(
                ClickEventRow(
                    link_id=expired_id,
                    clicked_at=now - timedelta(days=1),
                    device="unknown",
                )
            )

        first = await run_cleanup(settings, now=now, batch_size=2)
        assert first.click_events_deleted == 5
        assert first.expired_links_deleted == 1
        assert first.batches >= 4

        async with admin.read() as session:
            assert (
                await session.scalar(
                    select(func.count())
                    .select_from(ClickEventRow)
                    .where(ClickEventRow.link_id == active_id)
                )
                == 1
            )
            assert (
                await session.scalar(
                    select(func.count())
                    .select_from(ClickEventRow)
                    .where(ClickEventRow.link_id == expired_id)
                )
                == 0
            )
            assert await session.get(LinkRow, active_id) is not None
            assert await session.get(LinkRow, expired_id) is None

        second = await run_cleanup(settings, now=now, batch_size=2)
        assert second.click_events_deleted == 0
        assert second.expired_links_deleted == 0
    finally:
        async with admin.unit_of_work() as session:
            await session.execute(
                delete(LinkRow).where(LinkRow.code.in_([active_code, expired_code]))
            )
        await admin.dispose()
