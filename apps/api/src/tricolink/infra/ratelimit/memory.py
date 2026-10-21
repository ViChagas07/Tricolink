from __future__ import annotations

import asyncio
import math
import time
from collections.abc import Callable
from dataclasses import dataclass

from tricolink.infra.ratelimit.models import RateLimitResult
from tricolink.infra.ratelimit.policies import BucketPolicy

_CLEANUP_INTERVAL = 1_024
_CLEANUP_THRESHOLD = 10_000


@dataclass(slots=True)
class _BucketState:
    tokens: float
    updated_at: float


class MemoryTokenBucket:
    """Per-process token bucket used when Redis is unavailable.

    This is a deliberate safe degradation: limits stay enforced, even though
    each process keeps its own counters.
    """

    def __init__(self, clock: Callable[[], float] = time.monotonic) -> None:
        self._clock = clock
        self._buckets: dict[str, _BucketState] = {}
        self._lock = asyncio.Lock()
        self._operations = 0

    @property
    def size(self) -> int:
        return len(self._buckets)

    async def consume(
        self,
        key: str,
        policy: BucketPolicy,
        cost: int = 1,
    ) -> RateLimitResult:
        now = self._clock()
        async with self._lock:
            state = self._buckets.get(key)
            if state is None:
                state = _BucketState(tokens=float(policy.capacity), updated_at=now)
                self._buckets[key] = state

            elapsed = max(0.0, now - state.updated_at)
            state.tokens = min(
                float(policy.capacity),
                state.tokens + elapsed * policy.refill_per_sec,
            )
            state.updated_at = now

            allowed = state.tokens >= cost
            if allowed:
                state.tokens -= cost

            remaining = max(0, math.floor(state.tokens))
            if allowed:
                retry_after_ms = 0
            elif policy.refill_per_sec > 0:
                retry_after_ms = math.ceil(((cost - state.tokens) / policy.refill_per_sec) * 1000)
            else:
                retry_after_ms = -1

            if allowed:
                reset_after_seconds = _reset_seconds(policy, remaining)
            elif retry_after_ms >= 0:
                reset_after_seconds = max(1, math.ceil(retry_after_ms / 1000))
            else:
                reset_after_seconds = policy.seconds_to_fill

            self._operations += 1
            if self._operations % _CLEANUP_INTERVAL == 0:
                self._cleanup(now)

            return RateLimitResult(
                allowed=allowed,
                limit=policy.capacity,
                remaining=remaining,
                retry_after_ms=retry_after_ms,
                reset_after_seconds=reset_after_seconds,
            )

    def _cleanup(self, now: float) -> None:
        if len(self._buckets) < _CLEANUP_THRESHOLD:
            return
        stale = [
            key
            for key, state in self._buckets.items()
            if now - state.updated_at > 3_600 and state.tokens >= 1
        ]
        for key in stale:
            del self._buckets[key]


def _reset_seconds(policy: BucketPolicy, remaining: int) -> int:
    if policy.refill_per_sec <= 0:
        return -1
    return max(0, math.ceil((policy.capacity - remaining) / policy.refill_per_sec))
