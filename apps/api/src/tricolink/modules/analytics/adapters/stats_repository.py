from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Date, cast, func, select

from tricolink.infra.db import Database
from tricolink.infra.db.models import ClickEvent as ClickEventRow
from tricolink.infra.db.rls import set_rls_context
from tricolink.modules.analytics.application.ports import RawStats

_BREAKDOWN_LIMIT = 11
_TOP_LIMIT = 10


class SqlAlchemyStatsRepository:
    """Reads click aggregates without per-link queries (no N+1)."""

    def __init__(self, database: Database) -> None:
        self._database = database

    async def collect(
        self,
        link_id: int,
        user_id: UUID,
        *,
        since: datetime,
        until: datetime,
    ) -> RawStats:
        filters = (
            ClickEventRow.link_id == link_id,
            ClickEventRow.clicked_at >= since,
            ClickEventRow.clicked_at < until,
        )
        clicks = func.count(ClickEventRow.id)
        day = cast(func.date_trunc("day", func.timezone("UTC", ClickEventRow.clicked_at)), Date)

        series_statement = (
            select(day.label("day"), clicks.label("clicks"))
            .where(*filters)
            .group_by(day)
            .order_by(day)
        )
        devices_statement = (
            select(ClickEventRow.device, clicks.label("clicks"))
            .where(*filters)
            .group_by(ClickEventRow.device)
            .order_by(clicks.desc(), ClickEventRow.device)
        )
        countries_statement = (
            select(ClickEventRow.country, clicks.label("clicks"))
            .where(*filters)
            .group_by(ClickEventRow.country)
            .order_by(clicks.desc(), ClickEventRow.country.asc().nulls_last())
            .limit(_BREAKDOWN_LIMIT)
        )
        referrers_statement = (
            select(ClickEventRow.referrer_host, clicks.label("clicks"))
            .where(*filters, ClickEventRow.referrer_host.is_not(None))
            .group_by(ClickEventRow.referrer_host)
            .order_by(clicks.desc(), ClickEventRow.referrer_host)
            .limit(_TOP_LIMIT)
        )
        direct_referrers_statement = select(clicks).where(
            *filters,
            ClickEventRow.referrer_host.is_(None),
        )

        async with self._database.read() as session:
            await set_rls_context(session, user_id=user_id)
            series_rows = (await session.execute(series_statement)).all()
            device_rows = (await session.execute(devices_statement)).all()
            country_rows = (await session.execute(countries_statement)).all()
            referrer_rows = (await session.execute(referrers_statement)).all()
            direct_referrers = await session.scalar(direct_referrers_statement)

        devices = [(str(device), int(count)) for device, count in device_rows]
        return RawStats(
            total=sum(count for _, count in devices),
            series=[(day_value, int(count)) for day_value, count in series_rows],
            countries=[(country, int(count)) for country, count in country_rows],
            devices=devices,
            referrers=[
                (str(host), int(count)) for host, count in referrer_rows if host is not None
            ],
            direct_referrers=int(direct_referrers or 0),
        )
