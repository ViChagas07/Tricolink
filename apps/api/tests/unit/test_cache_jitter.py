import random

from tricolink.infra.cache.jitter import jittered_ttl


def test_jittered_ttl_stays_within_configured_range() -> None:
    for seed in range(2000):
        ttl = jittered_ttl(100, 0.15, rng=random.Random(seed))
        assert 85 <= ttl <= 115


def test_jittered_ttl_edge_cases() -> None:
    assert jittered_ttl(0, 0.15) == 1
    assert jittered_ttl(-5, 0.15) == 1
    assert jittered_ttl(100, 0) == 100
