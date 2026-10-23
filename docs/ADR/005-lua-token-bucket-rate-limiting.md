# ADR 005: Lua Token Bucket Rate Limiting

## Status
Accepted

## Context
Rate limiting must be precise, low-latency, and survive Redis failures without "allowing all" traffic.

## Decision
Implement token bucket as a **single atomic Lua script** running on Redis:

```lua
-- Refill based on Redis TIME (server clock)
-- Consume atomically
-- Return: allowed (0/1), remaining, retry_after_ms
```

- One script per bucket type (redirect, create, auth, global, stats/list)
- Key pattern: `rl:{scope}:{id}` where id = hashed IP or user_id
- Redis down → Circuit Breaker opens → **in-memory fallback per process** (still enforces limits, never "fail open")
- Daily quotas (anonymous/logged) use separate Redis keys with midnight UTC expiry

## Rationale
- **Lua atomicity**: Refill + consume in one round-trip, no race conditions
- **Redis TIME**: Server-side clock avoids client clock skew
- **In-memory fallback**: Degraded but safe; per-process counters prevent total bypass
- **Headers**: `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`, `Retry-After` on 429

## Consequences
- ✅ 100 parallel requests respect capacity exactly (validated)
- ✅ 8,531 429s on redirect rate limit test (83.2%)
- ✅ 2,530 429s on create rate limit (99.8%, daily quota)
- ✅ Circuit breaker + fallback tested under Redis failure
- ⚠️ In-memory fallback is per-process (not global); acceptable for dev, production behind WAF
- ⚠️ Lua script complexity; tested via `test_token_bucket.py` and k6

## References
- SECURITY.md §1 (Token Bucket)
- CONTEXT.md §6 (Quotas e Token Bucket)
- PROGRESS.md P02 validation (token bucket tests)
- AUDIT.md §1 (Token Bucket audit)