# ADR 003: SWR + Jitter + Single-Flight + Negative Cache

## Status
Accepted

## Context
The redirect hot path (`GET /r/{code}`) must serve millions of requests with minimal latency. Cold cache misses on popular or scanned codes create thundering herd problems on PostgreSQL.

## Decision
Combine four cache protection layers:

1. **Stale-While-Revalidate (SWR)**: Two TTLs per key
   - Soft TTL (`CACHE_SOFT_TTL_SECONDS` = 600s): serve stale, trigger background refresh
   - Hard TTL (`CACHE_HARD_TTL_SECONDS` = 86400s): Redis key expiry
2. **Jitter (±15%)** on all TTLs (`CACHE_JITTER_PCT`) to desynchronize expiration
3. **Single-flight**: In-process task deduplication + cross-process Redis lock (`SET NX PX LOCK_TTL_MS`). Only one loader hits DB; waiters re-read cache with jitter, fallback to DB via bulkhead on timeout.
4. **Negative cache** (`tl:neg:{code}`, `NEGATIVE_CACHE_TTL_SECONDS` = 30s) for non-existent codes to block scan/penetration attacks.

## Rationale
- SWR alone leaves window where all requests miss simultaneously after hard TTL
- Jitter alone doesn't prevent coordinated omission on cold keys
- Single-flight alone doesn't protect against cross-process stampede
- Negative cache alone doesn't help with valid but cold keys
- **Together** they eliminate stampede at every layer: cold miss, expired key, scan attack

## Consequences
- ✅ 200 concurrent cold redirects → 1 DB query (validated in `test_redirect_stampede.py`)
- ✅ 1000 non-existent codes → 1 DB query (negative cache)
- ✅ Background refresh never serves stale data after invalidation (P09: generation counter + Lua conditional store)
- ⚠️ Added complexity in cache adapter (`links/adapters/cache.py`)
- ⚠️ Cache wait timeout (`CACHE_WAIT_TIMEOUT_SECONDS` = 0.25s) adds tail latency under contention

## References
- CONTEXT.md §6 (Anti cache stampede)
- PROGRESS.md P03 validation (stampede tests)
- AUDIT.md F-03, F-04 (cache security fixes)