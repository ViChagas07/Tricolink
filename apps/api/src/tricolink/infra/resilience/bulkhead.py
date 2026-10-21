from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager

from tricolink.core.config import Settings
from tricolink.shared_kernel.security_errors import BulkheadFullError


class Bulkhead:
    """Named concurrency limiter backed by an asyncio semaphore."""

    def __init__(self, name: str, *, limit: int, acquire_timeout: float = 1.0) -> None:
        if limit < 1:
            raise ValueError("limit must be at least 1")
        if acquire_timeout <= 0:
            raise ValueError("acquire_timeout must be positive")
        self.name = name
        self.limit = limit
        self._acquire_timeout = acquire_timeout
        self._semaphore = asyncio.Semaphore(limit)

    @property
    def available(self) -> int:
        return self._semaphore._value  # noqa: SLF001 - read-only introspection for metrics

    @asynccontextmanager
    async def acquire(self) -> AsyncIterator[None]:
        try:
            await asyncio.wait_for(self._semaphore.acquire(), timeout=self._acquire_timeout)
        except TimeoutError as exc:
            raise BulkheadFullError(self.name) from exc
        try:
            yield
        finally:
            self._semaphore.release()


class BulkheadRegistry:
    def __init__(self, bulkheads: Mapping[str, Bulkhead]) -> None:
        self._bulkheads = dict(bulkheads)

    @property
    def names(self) -> frozenset[str]:
        return frozenset(self._bulkheads)

    def get(self, name: str) -> Bulkhead:
        return self._bulkheads[name]


def build_bulkheads(settings: Settings) -> BulkheadRegistry:
    timeout = settings.bulkhead_acquire_timeout_seconds
    return BulkheadRegistry(
        {
            "db_read": Bulkhead(
                "db_read", limit=settings.bulkhead_db_read, acquire_timeout=timeout
            ),
            "db_write": Bulkhead(
                "db_write", limit=settings.bulkhead_db_write, acquire_timeout=timeout
            ),
            "hashing": Bulkhead(
                "hashing", limit=settings.bulkhead_hashing, acquire_timeout=timeout
            ),
            "dns": Bulkhead("dns", limit=settings.bulkhead_dns, acquire_timeout=timeout),
        }
    )
