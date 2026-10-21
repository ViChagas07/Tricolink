from __future__ import annotations

import asyncio
import logging
import socket
from collections import Counter
from collections.abc import Awaitable, Callable
from contextlib import suppress
from datetime import UTC, datetime
from typing import Any, TypeVar, cast

from redis.asyncio import Redis
from redis.exceptions import RedisError, ResponseError
from sqlalchemy import select, update

from tricolink.core.config import Settings
from tricolink.infra.db import Database
from tricolink.infra.db.models import ClickEvent as ClickEventRow
from tricolink.infra.db.models import Link as LinkRow
from tricolink.infra.observability.metrics import record_clicks_flushed
from tricolink.infra.resilience import CircuitBreaker, CircuitOpenError
from tricolink.modules.analytics.domain.click import ClickEvent, normalize_country

T = TypeVar("T")
logger = logging.getLogger(__name__)

_ALLOWED_DEVICES = frozenset({"desktop", "mobile", "tablet", "bot", "unknown"})


class ClickFlusher:
    """Consumes `tl:clicks` in batches and persists aggregated click events."""

    def __init__(
        self,
        redis: Redis,
        database: Database,
        *,
        breaker: CircuitBreaker | None,
        settings: Settings,
    ) -> None:
        self._redis = redis
        self._database = database
        self._breaker = breaker
        self._stream_key = settings.click_stream_key
        self._group = settings.click_stream_group
        self._consumer = f"api-{socket.gethostname()}"
        self._batch_size = settings.click_flush_batch_size
        self._block_ms = settings.click_flush_block_ms
        self._timeout = settings.redis_timeout_seconds

        self._task: asyncio.Task[None] | None = None
        self._stop = asyncio.Event()
        self._group_ready = False
        self._backoff_seconds = 1.0

    async def start(self) -> None:
        if self._task is not None:
            return
        self._stop.clear()
        self._task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        self._stop.set()
        if self._task is None:
            return
        self._task.cancel()
        with suppress(asyncio.CancelledError):
            await self._task
        self._task = None

    async def run_once(self, *, block_ms: int | None = 10) -> int:
        await self._ensure_group()
        entries = await self._read("0", block_ms=None)
        if not any(items for _, items in entries):
            entries = await self._read(">", block_ms=block_ms)

        ids: list[str] = []
        events: list[ClickEvent] = []
        for _, items in entries:
            for entry_id, fields in items:
                ids.append(entry_id)
                parsed = _parse_event(fields)
                if parsed is not None:
                    events.append(parsed)

        if not ids:
            return 0
        if events:
            await self._persist(events)
        await self._ack(ids)
        return len(ids)

    async def _run(self) -> None:
        while not self._stop.is_set():
            try:
                await self.run_once(block_ms=self._block_ms)
                self._backoff_seconds = 1.0
            except asyncio.CancelledError:
                raise
            except (RedisError, TimeoutError, OSError, CircuitOpenError):
                await asyncio.sleep(self._backoff_seconds)
                self._backoff_seconds = min(10.0, self._backoff_seconds * 2)
            except Exception:
                logger.exception("click_flusher_failed")
                await asyncio.sleep(self._backoff_seconds)
                self._backoff_seconds = min(10.0, self._backoff_seconds * 2)

    async def _ensure_group(self) -> None:
        if self._group_ready:
            return
        try:
            await self._redis_call(
                lambda: self._redis.xgroup_create(
                    self._stream_key,
                    self._group,
                    id="0",
                    mkstream=True,
                )
            )
        except ResponseError as exc:
            if "BUSYGROUP" not in str(exc):
                raise
        self._group_ready = True

    async def _read(
        self,
        start_id: str,
        *,
        block_ms: int | None,
    ) -> list[tuple[str, list[tuple[str, dict[str, str]]]]]:
        raw = await self._redis_call(
            lambda: self._redis.xreadgroup(
                self._group,
                self._consumer,
                {self._stream_key: start_id},
                count=self._batch_size,
                block=block_ms,
            )
        )
        return cast(list[tuple[str, list[tuple[str, dict[str, str]]]]], raw or [])

    async def _persist(self, events: list[ClickEvent]) -> None:
        async with self._database.unit_of_work() as session:
            link_ids = {event.link_id for event in events}
            existing = set(
                (await session.scalars(select(LinkRow.id).where(LinkRow.id.in_(link_ids)))).all()
            )
            rows = [
                ClickEventRow(
                    link_id=event.link_id,
                    clicked_at=event.clicked_at,
                    country=event.country,
                    device=event.device,
                    browser=event.browser,
                    referrer_host=event.referrer_host,
                )
                for event in events
                if event.link_id in existing
            ]
            if rows:
                session.add_all(rows)
            counts = Counter(event.link_id for event in events if event.link_id in existing)
            for link_id, count in counts.items():
                await session.execute(
                    update(LinkRow)
                    .where(LinkRow.id == link_id)
                    .values(click_count=LinkRow.click_count + count)
                )
        record_clicks_flushed(len(rows))

    async def _ack(self, ids: list[str]) -> None:
        await self._redis_call(lambda: self._redis.xack(self._stream_key, self._group, *ids))
        await self._redis_call(lambda: self._redis.xdel(self._stream_key, *ids))

    async def _redis_call(self, operation: Callable[[], Awaitable[T]]) -> T:
        async def guarded() -> T:
            return await asyncio.wait_for(
                operation(),
                timeout=self._timeout + (self._block_ms / 1000) + 1,
            )

        if self._breaker is None:
            return await guarded()
        async with self._breaker.guard():
            return await guarded()


def _parse_event(fields: dict[str, Any]) -> ClickEvent | None:
    try:
        link_id = int(fields["link_id"])
        clicked_at = datetime.fromisoformat(str(fields["clicked_at"]))
    except (KeyError, TypeError, ValueError):
        return None

    if clicked_at.tzinfo is None:
        clicked_at = clicked_at.replace(tzinfo=UTC)

    device = str(fields.get("device") or "unknown")
    if device not in _ALLOWED_DEVICES:
        device = "unknown"

    return ClickEvent(
        link_id=link_id,
        clicked_at=clicked_at.astimezone(UTC),
        country=normalize_country(str(fields.get("country") or "") or None),
        device=cast(Any, device),
        browser=str(fields.get("browser") or "") or None,
        referrer_host=str(fields.get("referrer_host") or "") or None,
    )
