from __future__ import annotations

import asyncio
import time
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager, suppress
from enum import StrEnum
from typing import ParamSpec, TypeVar

from tricolink.infra.observability.metrics import record_circuit_state
from tricolink.shared_kernel.security_errors import CircuitOpenError

P = ParamSpec("P")
R = TypeVar("R")


class CircuitState(StrEnum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    """Async circuit breaker with closed/open/half-open states.

    The clock is injectable so state transitions can be tested without sleeping.
    """

    def __init__(
        self,
        name: str,
        *,
        failure_threshold: int = 5,
        recovery_timeout: float = 15.0,
        half_open_max_calls: int = 1,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if failure_threshold < 1:
            raise ValueError("failure_threshold must be at least 1")
        if recovery_timeout <= 0:
            raise ValueError("recovery_timeout must be positive")
        if half_open_max_calls < 1:
            raise ValueError("half_open_max_calls must be at least 1")
        self.name = name
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._half_open_max_calls = half_open_max_calls
        self._clock = clock
        self._state = CircuitState.CLOSED
        self._failures = 0
        self._opened_at = 0.0
        self._half_open_calls = 0
        self._lock = asyncio.Lock()
        record_circuit_state(self.name, self._state.value)

    @property
    def state(self) -> CircuitState:
        return self._state

    @property
    def failures(self) -> int:
        return self._failures

    async def before_request(self) -> None:
        async with self._lock:
            if self._state is CircuitState.OPEN:
                if self._clock() - self._opened_at < self._recovery_timeout:
                    raise CircuitOpenError(self.name)
                self._transition(CircuitState.HALF_OPEN)
                self._half_open_calls = 0

            if self._state is CircuitState.HALF_OPEN:
                if self._half_open_calls >= self._half_open_max_calls:
                    raise CircuitOpenError(self.name)
                self._half_open_calls += 1

    async def record_success(self) -> None:
        async with self._lock:
            if self._state is CircuitState.OPEN:
                # A call that started before the breaker opened must not close it.
                return
            self._failures = 0
            self._half_open_calls = 0
            if self._state is CircuitState.HALF_OPEN:
                self._transition(CircuitState.CLOSED)

    async def record_failure(self) -> None:
        async with self._lock:
            if self._state is CircuitState.HALF_OPEN:
                self._open()
                return
            if self._state is CircuitState.CLOSED:
                self._failures += 1
                if self._failures >= self._failure_threshold:
                    self._open()

    async def call(self, func: Callable[P, Awaitable[R]], *args: P.args, **kwargs: P.kwargs) -> R:
        await self.before_request()
        try:
            result = await func(*args, **kwargs)
        except BaseException:
            await self._record_failure_safely()
            raise
        else:
            await self.record_success()
            return result

    @asynccontextmanager
    async def guard(self) -> AsyncIterator[None]:
        await self.before_request()
        try:
            yield
        except BaseException:
            await self._record_failure_safely()
            raise
        else:
            await self.record_success()

    async def _record_failure_safely(self) -> None:
        with suppress(Exception):  # pragma: no cover - defensive during shutdown
            await self.record_failure()

    def _open(self) -> None:
        self._opened_at = self._clock()
        self._half_open_calls = 0
        self._transition(CircuitState.OPEN)

    def _transition(self, state: CircuitState) -> None:
        self._state = state
        record_circuit_state(self.name, state.value)
