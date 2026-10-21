from __future__ import annotations

import asyncio
import json
import random
import time
import uuid
from collections.abc import Awaitable, Callable
from contextlib import suppress
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, TypeVar, cast

from redis.asyncio import Redis
from redis.exceptions import RedisError

from tricolink.core.config import Settings
from tricolink.infra.cache.jitter import jittered_ttl
from tricolink.infra.observability.metrics import record_cache_hit, record_cache_miss
from tricolink.infra.resilience import CircuitBreaker, CircuitOpenError
from tricolink.modules.links.application.ports import CacheEntry, CacheUnavailable
from tricolink.modules.links.domain.entities import Link
from tricolink.modules.links.domain.value_objects import ShortCode

T = TypeVar("T")

LINK_KEY = "tl:link:{code}"
LOCK_KEY = "tl:lock:{code}"
NEGATIVE_KEY = "tl:neg:{code}"
RELEASE_LOCK_LUA = """
if redis.call('get', KEYS[1]) == ARGV[1] then
  return redis.call('del', KEYS[1])
end
return 0
"""


@dataclass(frozen=True, slots=True)
class _CacheRead:
    entry: CacheEntry
    stale: bool


class RedisLinkCache:
    def __init__(
        self,
        redis: Redis,
        *,
        breaker: CircuitBreaker | None,
        settings: Settings,
        clock: Callable[[], float] = time.time,
        rng: random.Random | None = None,
    ) -> None:
        self._redis = redis
        self._breaker = breaker
        self._settings = settings
        self._clock = clock
        self._rng = rng or random.Random()
        self._timeout = settings.redis_timeout_seconds
        self._hard_ttl = settings.cache_hard_ttl_seconds
        self._soft_ttl = settings.cache_soft_ttl_seconds
        self._jitter_pct = settings.cache_jitter_pct
        self._negative_ttl = settings.negative_cache_ttl_seconds
        self._lock_ttl_ms = settings.lock_ttl_ms
        self._wait_timeout = settings.cache_wait_timeout_seconds

        self._flights: dict[str, asyncio.Task[CacheEntry | None]] = {}
        self._flights_guard = asyncio.Lock()
        self._refreshing: set[str] = set()
        self._refresh_tasks: set[asyncio.Task[None]] = set()

    async def resolve(
        self,
        code: ShortCode,
        loader: Callable[[], Awaitable[Link | None]],
    ) -> CacheEntry | None:
        flight = await self._get_or_create_flight(code, loader)
        return await asyncio.shield(flight)

    async def _get_or_create_flight(
        self,
        code: ShortCode,
        loader: Callable[[], Awaitable[Link | None]],
    ) -> asyncio.Task[CacheEntry | None]:
        async with self._flights_guard:
            existing = self._flights.get(code.value)
            if existing is not None:
                return existing
            task = asyncio.create_task(self._resolve_uncached(code, loader))
            self._flights[code.value] = task
            task.add_done_callback(lambda completed: self._finish_flight(code.value, completed))
            return task

    def _finish_flight(
        self,
        code: str,
        completed: asyncio.Task[CacheEntry | None],
    ) -> None:
        with suppress(BaseException):
            completed.exception()
        if self._flights.get(code) is completed:
            del self._flights[code]

    async def _resolve_uncached(
        self,
        code: ShortCode,
        loader: Callable[[], Awaitable[Link | None]],
    ) -> CacheEntry | None:
        try:
            read = await self._read(code)
            if read is not None:
                if read.stale:
                    self._schedule_refresh(code, loader)
                return read.entry

            if await self._is_negative(code):
                return None

            return await self._single_flight(code, loader)
        except (RedisError, TimeoutError, OSError, CircuitOpenError) as exc:
            raise CacheUnavailable() from exc

    async def invalidate(self, code: ShortCode) -> None:
        try:
            await self._redis_call(
                lambda: self._redis.delete(
                    LINK_KEY.format(code=code.value),
                    NEGATIVE_KEY.format(code=code.value),
                )
            )
        except (RedisError, TimeoutError, OSError, CircuitOpenError) as exc:
            raise CacheUnavailable() from exc

    async def store(
        self,
        link: Link,
        *,
        soft_ttl_seconds: int | None = None,
    ) -> None:
        await self._store(link, soft_ttl_override=soft_ttl_seconds)

    async def _single_flight(
        self,
        code: ShortCode,
        loader: Callable[[], Awaitable[Link | None]],
    ) -> CacheEntry | None:
        token = uuid.uuid4().hex
        if await self._acquire_lock(code.value, token):
            try:
                return await self._load_and_store(code, loader)
            finally:
                await self._release_lock(code.value, token)

        deadline = time.monotonic() + self._wait_timeout
        while time.monotonic() < deadline:
            await asyncio.sleep(0.005 + self._rng.random() * 0.01)
            read = await self._read(code)
            if read is not None:
                return read.entry
            if await self._is_negative(code):
                return None

        return await self._load_and_store(code, loader)

    async def _load_and_store(
        self,
        code: ShortCode,
        loader: Callable[[], Awaitable[Link | None]],
    ) -> CacheEntry | None:
        link = await loader()
        if link is None:
            await self._set_negative(code)
            return None
        entry = _entry_from_link(link)
        await self._store_link(code, entry)
        return entry

    async def _refresh(
        self,
        code: ShortCode,
        loader: Callable[[], Awaitable[Link | None]],
    ) -> None:
        token = uuid.uuid4().hex
        try:
            if not await self._acquire_lock(code.value, token):
                return
            try:
                await self._load_and_store(code, loader)
            finally:
                await self._release_lock(code.value, token)
        except Exception:
            # Stale data remains available; a refresh failure must not break redirects.
            return
        finally:
            self._refreshing.discard(code.value)

    def _schedule_refresh(
        self,
        code: ShortCode,
        loader: Callable[[], Awaitable[Link | None]],
    ) -> None:
        if code.value in self._refreshing:
            return
        self._refreshing.add(code.value)
        task = asyncio.create_task(self._refresh(code, loader))
        self._refresh_tasks.add(task)
        task.add_done_callback(self._refresh_tasks.discard)

    async def _read(self, code: ShortCode) -> _CacheRead | None:
        raw = await self._redis_call(lambda: self._redis.get(LINK_KEY.format(code=code.value)))
        if raw is None:
            record_cache_miss("link")
            return None

        try:
            payload = cast(dict[str, Any], json.loads(raw))
            entry = CacheEntry(
                link_id=int(payload["id"]),
                original_url=str(payload["u"]),
                expires_at=(
                    datetime.fromtimestamp(float(payload["e"]), tz=UTC)
                    if payload.get("e") is not None
                    else None
                ),
                is_active=bool(payload["s"]),
            )
            fresh_until = float(payload["sf"])
        except (ValueError, TypeError, KeyError, json.JSONDecodeError):
            await self._redis_call(lambda: self._redis.delete(LINK_KEY.format(code=code.value)))
            record_cache_miss("link")
            return None

        record_cache_hit("link")
        return _CacheRead(entry=entry, stale=self._clock() > fresh_until)

    async def _is_negative(self, code: ShortCode) -> bool:
        raw = await self._redis_call(lambda: self._redis.get(NEGATIVE_KEY.format(code=code.value)))
        return raw is not None

    async def _store_link(self, code: ShortCode, entry: CacheEntry) -> None:
        now = self._clock()
        soft_ttl = jittered_ttl(self._soft_ttl, self._jitter_pct, rng=self._rng)
        hard_ttl = jittered_ttl(self._hard_ttl, self._jitter_pct, rng=self._rng)
        if soft_ttl >= hard_ttl:
            soft_ttl = max(1, hard_ttl - 1)

        payload = json.dumps(
            {
                "id": entry.link_id,
                "u": entry.original_url,
                "e": entry.expires_at.timestamp() if entry.expires_at else None,
                "s": entry.is_active,
                "sf": now + soft_ttl,
            },
            separators=(",", ":"),
        )
        await self._redis_call(
            lambda: self._redis.set(
                LINK_KEY.format(code=code.value),
                payload,
                px=hard_ttl * 1000,
            )
        )

    async def _store(
        self,
        link: Link,
        *,
        soft_ttl_override: int | None,
    ) -> None:
        code = link.code
        if soft_ttl_override is None:
            await self._store_link(code, _entry_from_link(link))
            return
        # Test and maintenance helper: seed a custom freshness window.
        entry = _entry_from_link(link)
        now = self._clock()
        hard_ttl = jittered_ttl(self._hard_ttl, self._jitter_pct, rng=self._rng)
        payload = json.dumps(
            {
                "id": entry.link_id,
                "u": entry.original_url,
                "e": entry.expires_at.timestamp() if entry.expires_at else None,
                "s": entry.is_active,
                "sf": now + soft_ttl_override,
            },
            separators=(",", ":"),
        )
        await self._redis_call(
            lambda: self._redis.set(
                LINK_KEY.format(code=code.value),
                payload,
                px=hard_ttl * 1000,
            )
        )

    async def _set_negative(self, code: ShortCode) -> None:
        ttl = jittered_ttl(self._negative_ttl, self._jitter_pct, rng=self._rng)
        await self._redis_call(
            lambda: self._redis.set(
                NEGATIVE_KEY.format(code=code.value),
                "1",
                px=ttl * 1000,
            )
        )

    async def _acquire_lock(self, code: str, token: str) -> bool:
        result = await self._redis_call(
            lambda: self._redis.set(
                LOCK_KEY.format(code=code),
                token,
                nx=True,
                px=self._lock_ttl_ms,
            )
        )
        return bool(result)

    async def _release_lock(self, code: str, token: str) -> None:
        await self._redis_call(
            lambda: self._redis.eval(
                RELEASE_LOCK_LUA,
                1,
                LOCK_KEY.format(code=code),
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


def _entry_from_link(link: Link) -> CacheEntry:
    if link.id is None:
        raise ValueError("Cannot cache an unsaved link")
    return CacheEntry(
        link_id=link.id,
        original_url=link.original_url.value,
        expires_at=link.expires_at,
        is_active=link.is_active,
    )
