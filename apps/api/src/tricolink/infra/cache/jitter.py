from __future__ import annotations

import random

_RNG = random.Random()


def jittered_ttl(
    base_seconds: int,
    jitter_pct: float,
    *,
    rng: random.Random | None = None,
) -> int:
    if base_seconds <= 0:
        return 1
    if jitter_pct <= 0:
        return base_seconds
    source = rng or _RNG
    factor = 1 + source.uniform(-jitter_pct, jitter_pct)
    return max(1, int(round(base_seconds * factor)))
