import asyncio

import pytest

from tricolink.core.config import Settings
from tricolink.infra.resilience import Bulkhead, BulkheadFullError, build_bulkheads


@pytest.mark.asyncio
async def test_bulkhead_limits_concurrency() -> None:
    bulkhead = Bulkhead("db_read", limit=2, acquire_timeout=1.0)
    inside = 0
    max_inside = 0
    lock = asyncio.Lock()

    async def worker() -> None:
        nonlocal inside, max_inside
        async with bulkhead.acquire():
            async with lock:
                inside += 1
                max_inside = max(max_inside, inside)
            await asyncio.sleep(0.02)
            async with lock:
                inside -= 1

    await asyncio.gather(*(worker() for _ in range(10)))

    assert max_inside == 2
    assert bulkhead.available == 2


@pytest.mark.asyncio
async def test_bulkhead_times_out_when_full() -> None:
    bulkhead = Bulkhead("hashing", limit=1, acquire_timeout=0.02)
    release = asyncio.Event()

    async def holder() -> None:
        async with bulkhead.acquire():
            await release.wait()

    task = asyncio.create_task(holder())
    await asyncio.sleep(0)

    with pytest.raises(BulkheadFullError):
        async with bulkhead.acquire():
            pass

    release.set()
    await task


def test_bulkheads_are_named_and_independent() -> None:
    registry = build_bulkheads(Settings())

    assert set(registry.names) == {"db_read", "db_write", "hashing", "dns"}
    assert registry.get("db_read") is not registry.get("db_write")
    assert registry.get("db_read").limit == Settings().bulkhead_db_read

    with pytest.raises(KeyError):
        registry.get("unknown")
