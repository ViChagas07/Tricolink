# ADR 004: Async Click Pipeline with Redis Stream

## Status
Accepted

## Context
Click tracking must not add latency to the redirect response. The redirect is on the hot path; any synchronous DB write would increase p50/p99.

## Decision
Fire-and-forget click ingestion via **Redis Stream** + background flusher:

1. Redirect handler: `XADD tl:clicks * ...` (non-blocking, ~sub-ms)
2. Background flusher (lifespan task): Consumes via consumer group `tricolink-flusher`
3. Flusher batches `click_events` INSERT + `links.click_count` UPDATE in single transaction
4. On commit, invalidates all three stats cache windows (`7d`, `30d`, `90d`)
5. Redis down → increment `clicks_dropped_total` metric, redirect continues
6. Flusher recreates consumer group on `NOGROUP` (failover/FLUSHDB resilience)

## Rationale
- **Redis Stream** provides durability (AOF) + consumer groups + exactly-once semantics (with `XACK`)
- **Batching** amortizes DB round-trips (500 events/batch, 1s max block)
- **Async** keeps redirect p50 at ~5ms (warm cache)
- **At-least-once** delivery accepted; duplicate `click_events`/`click_count` possible on flusher crash between commit and `XACK` (documented limitation)

## Consequences
- ✅ Redirect p50 4.8ms (warm), 342ms (cold) — DB write not on critical path
- ✅ Survives Redis restarts (consumer group recreation)
- ✅ Stats cache invalidated immediately after flush (no 30s stale window)
- ⚠️ At-least-once duplicates possible (no idempotency key implemented)
- ⚠️ Flusher consumer name hostname-based; dead consumer's pending events not auto-claimed (no `XAUTOCLAIM`)

## References
- CONTEXT.md §6 (Cliques - pipeline assíncrono)
- PROGRESS.md P03 validation (click pipeline tests)
- AUDIT.md F-05 (flusher resilience fixes)
- docs/perf/RESULTS.md (redirect latency numbers)