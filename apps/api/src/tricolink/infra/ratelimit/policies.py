from __future__ import annotations

import math
from dataclasses import dataclass

from tricolink.core.config import Settings

MAX_TTL_MS = 86_400_000


@dataclass(frozen=True, slots=True)
class BucketPolicy:
    capacity: int
    refill_per_sec: float

    def __post_init__(self) -> None:
        if self.capacity < 1:
            raise ValueError("capacity must be at least 1")
        if self.refill_per_sec < 0:
            raise ValueError("refill_per_sec cannot be negative")

    @property
    def ttl_ms(self) -> int:
        if self.refill_per_sec <= 0:
            return MAX_TTL_MS
        seconds_to_fill = (self.capacity / self.refill_per_sec) * 2
        return min(MAX_TTL_MS, max(60_000, math.ceil(seconds_to_fill * 1000)))

    @property
    def seconds_to_fill(self) -> int:
        if self.refill_per_sec <= 0:
            return -1
        return math.ceil(self.capacity / self.refill_per_sec)


def build_policies(settings: Settings) -> dict[str, BucketPolicy]:
    return {
        "redirect": BucketPolicy(
            capacity=settings.rl_redirect_capacity,
            refill_per_sec=settings.rl_redirect_refill_per_sec,
        ),
        "create": BucketPolicy(
            capacity=settings.rl_create_capacity,
            refill_per_sec=settings.rl_create_refill_per_sec,
        ),
        "auth": BucketPolicy(
            capacity=settings.rl_auth_capacity,
            refill_per_sec=settings.rl_auth_refill_per_sec,
        ),
        "global": BucketPolicy(
            capacity=settings.rl_global_capacity,
            refill_per_sec=settings.rl_global_refill_per_sec,
        ),
        "stats_list": BucketPolicy(
            capacity=settings.rl_list_capacity,
            refill_per_sec=settings.rl_list_refill_per_sec,
        ),
    }
