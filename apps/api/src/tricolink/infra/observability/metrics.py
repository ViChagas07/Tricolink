from __future__ import annotations

from prometheus_client import Counter, Gauge, Histogram

HTTP_REQUESTS = Counter(
    "tricolink_http_requests_total",
    "Total HTTP requests handled by the API.",
    labelnames=("method", "path", "status"),
)

HTTP_LATENCY = Histogram(
    "tricolink_http_request_duration_seconds",
    "HTTP request latency in seconds.",
    labelnames=("method", "path"),
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

RATE_LIMITED = Counter(
    "tricolink_rate_limited_total",
    "Requests rejected by a rate limit bucket.",
    labelnames=("scope",),
)

RATE_LIMIT_FALLBACKS = Counter(
    "tricolink_rate_limit_fallbacks_total",
    "Rate limit checks served by the in-memory fallback.",
)

CIRCUIT_STATE = Gauge(
    "tricolink_circuit_breaker_state",
    "Circuit breaker state (0=closed, 1=half_open, 2=open).",
    labelnames=("name",),
)

CIRCUIT_TRANSITIONS = Counter(
    "tricolink_circuit_breaker_transitions_total",
    "Circuit breaker state transitions.",
    labelnames=("name", "to"),
)

CACHE_HITS = Counter(
    "tricolink_cache_hits_total",
    "Cache lookups that returned a value.",
    labelnames=("namespace",),
)

CACHE_MISSES = Counter(
    "tricolink_cache_misses_total",
    "Cache lookups that missed.",
    labelnames=("namespace",),
)

_STATE_VALUES = {"closed": 0, "half_open": 1, "open": 2}


def record_request(method: str, path: str, status: int, duration_seconds: float) -> None:
    HTTP_REQUESTS.labels(method=method, path=path, status=str(status)).inc()
    HTTP_LATENCY.labels(method=method, path=path).observe(duration_seconds)


def record_rate_limited(scope: str) -> None:
    RATE_LIMITED.labels(scope=scope).inc()


def record_rate_limit_fallback() -> None:
    RATE_LIMIT_FALLBACKS.inc()


def record_circuit_state(name: str, state: str) -> None:
    CIRCUIT_STATE.labels(name=name).set(_STATE_VALUES[state])
    CIRCUIT_TRANSITIONS.labels(name=name, to=state).inc()


def record_cache_hit(namespace: str) -> None:
    CACHE_HITS.labels(namespace=namespace).inc()


def record_cache_miss(namespace: str) -> None:
    CACHE_MISSES.labels(namespace=namespace).inc()
