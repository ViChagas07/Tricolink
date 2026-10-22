from __future__ import annotations

import asyncio
import json
import random
import time
import uuid
from collections.abc import Awaitable, Callable
from contextlib import suppress
from datetime import date
from typing import Any, TypeVar, cast

from redis.asyncio import Redis
from redis.exceptions import RedisError

from tricolink.core.config import Settings
from tricolink.infra.cache.jitter import jittered_ttl
from tricolink.infra.observability.metrics import record_cache_hit, record_cache_miss
from tricolink.infra.resilience import CircuitBreaker, CircuitOpenError
from tricolink.modules.analytics.domain.stats import BreakdownItem, LinkStats, SeriesPoint

T = TypeVar("T")

STATS_KEY = "tl:stats:{link_id}:{range}"
STATS_LOCK_KEY = "tl:stats:lock:{link_id}:{range}"
RELEASE_LOCK_LUA = """
if redis.call('get', KEYS[1]) == ARGV[1] then
  return redis.call('del', KEYS[1])
end
return 0
"""


class RedisStatsCache:
    """Short-lived cache for link statistics with in-process and Redis single-flight."""

    def __init__(
        self,
        redis: Redis,
        *,
        breaker: CircuitBreaker | None,
        settings: Settings,
        rng: random.Random | None = None,
    ) -> None:
        self._redis = redis
        self._breaker = breaker
        self._timeout = settings.redis_timeout_seconds
        self._ttl = settings.stats_cache_ttl_seconds
        self._jitter_pct = settings.cache_jitter_pct
        self._lock_ttl_ms = settings.lock_ttl_ms
        self._wait_timeout = settings.cache_wait_timeout_seconds
        self._rng = rng or random.Random()

        self._flights: dict[str, asyncio.Task[LinkStats]] = {}
        self._flights_guard = asyncio.Lock()

    async def get_or_load(
        self,
        link_id: int,
        range_key: str,
        loader: Callable[[], Awaitable[LinkStats]],
    ) -> LinkStats:
        key = STATS_KEY.format(link_id=link_id, range=range_key)
        flight = await self._get_or_create_flight(key, link_id, range_key, loader)
        return await asyncio.shield(flight)

    async def _get_or_create_flight(
        self,
        key: str,
        link_id: int,
        range_key: str,
        loader: Callable[[], Awaitable[LinkStats]],
    ) -> asyncio.Task[LinkStats]:
        async with self._flights_guard:
            existing = self._flights.get(key)
            if existing is not None:
                return existing
            task = asyncio.create_task(self._load_cached(key, link_id, range_key, loader))
            self._flights[key] = task
            task.add_done_callback(lambda completed: self._finish_flight(key, completed))
            return task

    def _finish_flight(self, key: str, completed: asyncio.Task[LinkStats]) -> None:
        with suppress(BaseException):
            completed.exception()
        if self._flights.get(key) is completed:
            del self._flights[key]

    async def _load_cached(
        self,
        key: str,
        link_id: int,
        range_key: str,
        loader: Callable[[], Awaitable[LinkStats]],
    ) -> LinkStats:
        try:
            cached = await self._read(key)
            if cached is not None:
                return cached
            return await self._single_flight(key, link_id, range_key, loader)
        except (RedisError, TimeoutError, OSError, CircuitOpenError):
            return await loader()

    async def _single_flight(
        self,
        key: str,
        link_id: int,
        range_key: str,
        loader: Callable[[], Awaitable[LinkStats]],
    ) -> LinkStats:
        token = uuid.uuid4().hex
        if await self._acquire_lock(link_id, range_key, token):
            try:
                return await self._load_and_store(key, loader)
            finally:
                await self._release_lock(link_id, range_key, token)

        deadline = time.monotonic() + self._wait_timeout
        while time.monotonic() < deadline:
            await asyncio.sleep(0.004 + self._rng.random() * 0.008)
            cached = await self._read(key)
            if cached is not None:
                return cached

        return await self._load_and_store(key, loader)

    async def _load_and_store(
        self,
        key: str,
        loader: Callable[[], Awaitable[LinkStats]],
    ) -> LinkStats:
        stats = await loader()
        await self._store(key, stats)
        return stats

    async def _read(self, key: str) -> LinkStats | None:
        raw = await self._redis_call(lambda: self._redis.get(key))
        if raw is None:
            record_cache_miss("stats")
            return None

        parsed = _deserialize(raw.decode() if isinstance(raw, bytes) else raw)
        if parsed is None:
            await self._redis_call(lambda: self._redis.delete(key))
            record_cache_miss("stats")
            return None
        record_cache_hit("stats")
        return parsed

    async def _store(self, key: str, stats: LinkStats) -> None:
        ttl = jittered_ttl(self._ttl, self._jitter_pct, rng=self._rng)
        await self._redis_call(
            lambda: self._redis.set(
                key,
                _serialize(stats),
                px=ttl * 1000,
            )
        )

    async def _acquire_lock(self, link_id: int, range_key: str, token: str) -> bool:
        result = await self._redis_call(
            lambda: self._redis.set(
                STATS_LOCK_KEY.format(link_id=link_id, range=range_key),
                token,
                nx=True,
                px=self._lock_ttl_ms,
            )
        )
        return bool(result)

    async def _release_lock(self, link_id: int, range_key: str, token: str) -> None:
        await self._redis_call(
            lambda: self._redis.eval(
                RELEASE_LOCK_LUA,
                1,
                STATS_LOCK_KEY.format(link_id=link_id, range=range_key),
                token,
            )
        )

    async def _redis_call(self, operation: Callable[[], Awaitable[T]]) -> T:
        async def guarded() -> T:
            return await asyncio.wait_for(operation(), timeout=self._timeout)

        if self._breaker is None:
            return await guarded()
        async with self._breaker.guard():
            return await guarded()


def _serialize(stats: LinkStats) -> str:
    return json.dumps(
        {
            "total": stats.total,
            "series": [[point.date.isoformat(), point.clicks] for point in stats.series],
            "countries": [[item.code, item.clicks, item.pct] for item in stats.countries],
            "devices": [[item.code, item.clicks, item.pct] for item in stats.devices],
            "referrers": [[item.code, item.clicks, item.pct] for item in stats.referrers],
        },
        separators=(",", ":"),
    )


def _deserialize(raw: str) -> LinkStats | None:
    try:
        payload = cast(dict[str, Any], json.loads(raw))
        return LinkStats(
            total=int(payload["total"]),
            series=[
                SeriesPoint(date=date.fromisoformat(str(day)), clicks=int(clicks))
                for day, clicks in payload["series"]
            ],
            countries=_breakdown(payload["countries"]),
            devices=_breakdown(payload["devices"]),
            referrers=_breakdown(payload["referrers"]),
        )
    except (ValueError, TypeError, KeyError, json.JSONDecodeError):
        return None


def _breakdown(value: Any) -> list[BreakdownItem]:
    return [
        BreakdownItem(code=str(code), clicks=int(clicks), pct=float(pct))
        for code, clicks, pct in value
    ]
