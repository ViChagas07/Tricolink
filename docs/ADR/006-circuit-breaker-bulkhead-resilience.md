# ADR 006: Circuit Breaker + Bulkhead Resilience

## Status
Accepted

## Context
External dependencies (PostgreSQL, Redis, DNS resolver, argon2 hashing) can become slow or unavailable. Failures must not cascade or exhaust resources.

## Decision
Two complementary patterns:

### Circuit Breaker (per dependency)
- States: `closed` (normal) → `open` (fast fail) → `half_open` (probe)
- Configurable: failure threshold (5), recovery timeout (15s), half-open max calls (1)
- Injectable clock for deterministic tests
- Applied to: Redis client, PostgreSQL client

### Bulkhead (named semaphores)
- `db_read`: 20 concurrent
- `db_write`: 10 concurrent
- `hashing`: 4 concurrent (argon2 in threadpool)
- `dns`: 10 concurrent (UrlPolicy DNS resolution)
- Acquire timeout: 1s (configurable)
- Rejection → `BulkheadFullError` → 503/429 fast

## Rationale
- Circuit breaker prevents hammering a failing dependency
- Bulkhead isolates failure domains: slow DNS won't block DB writes; heavy hashing won't starve reads
- Together they implement **defense in depth** for resilience

## Consequences
- ✅ Load shedding via global bucket + bulkheads protects DB under load
- ✅ Tests verify state transitions, concurrency limits, timeouts
- ✅ DNS resolution for URL policy runs under bulkhead (prevents rebinding DoS)
- ⚠️ Adds latency overhead (semaphore acquire) on every DB/Redis call
- ⚠️ Half-open probe success from pre-opening call doesn't close circuit (by design)

## References
- SECURITY.md §2 (Resiliência / anti-DDoS)
- CONTEXT.md §2 (Bulkheads nomeados)
- PROGRESS.md P02 validation (circuit breaker, bulkhead tests)
- AUDIT.md §2 (Resiliência audit)