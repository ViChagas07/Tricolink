import asyncio

import pytest

from tricolink.infra.resilience import CircuitBreaker, CircuitOpenError, CircuitState


async def fail() -> None:
    raise RuntimeError("dependency down")


@pytest.mark.asyncio
async def test_breaker_opens_after_threshold_and_rejects_calls() -> None:
    now = 0.0
    breaker = CircuitBreaker(
        "redis",
        failure_threshold=2,
        recovery_timeout=10.0,
        clock=lambda: now,
    )

    assert breaker.state is CircuitState.CLOSED

    for _ in range(2):
        with pytest.raises(RuntimeError):
            await breaker.call(fail)

    assert breaker.state is CircuitState.OPEN
    with pytest.raises(CircuitOpenError):
        await breaker.call(fail)


@pytest.mark.asyncio
async def test_breaker_half_open_success_closes() -> None:
    now = 0.0
    breaker = CircuitBreaker(
        "redis",
        failure_threshold=1,
        recovery_timeout=5.0,
        clock=lambda: now,
    )
    with pytest.raises(RuntimeError):
        await breaker.call(fail)
    assert breaker.state is CircuitState.OPEN

    now = 5.1
    result = await breaker.call(asyncio.sleep, 0, result="ok")

    assert result == "ok"
    assert breaker.state is CircuitState.CLOSED


@pytest.mark.asyncio
async def test_breaker_half_open_failure_reopens() -> None:
    now = 0.0
    breaker = CircuitBreaker(
        "postgres",
        failure_threshold=1,
        recovery_timeout=5.0,
        clock=lambda: now,
    )
    with pytest.raises(RuntimeError):
        await breaker.call(fail)

    now = 5.1
    with pytest.raises(RuntimeError):
        await breaker.call(fail)

    assert breaker.state is CircuitState.OPEN


@pytest.mark.asyncio
async def test_half_open_allows_only_configured_probes() -> None:
    now = 0.0
    breaker = CircuitBreaker(
        "postgres",
        failure_threshold=1,
        recovery_timeout=1.0,
        half_open_max_calls=1,
        clock=lambda: now,
    )
    with pytest.raises(RuntimeError):
        await breaker.call(fail)
    now = 2.0

    entered = asyncio.Event()
    release = asyncio.Event()

    async def probe() -> None:
        async with breaker.guard():
            entered.set()
            await release.wait()

    task = asyncio.create_task(probe())
    await entered.wait()

    with pytest.raises(CircuitOpenError):
        async with breaker.guard():
            pass

    release.set()
    await task
    assert breaker.state is CircuitState.CLOSED
