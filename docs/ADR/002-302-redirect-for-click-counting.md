# ADR 002: 302 Redirect for Click Counting

## Status
Accepted

## Context
URL shorteners must count every visit. The HTTP status code for the redirect determines whether browsers/CDNs cache the response.

## Decision
Use **HTTP 302 (Found)** for all short link redirects (`GET /r/{code}`).

## Rationale
- **301 (Moved Permanently)** is aggressively cached by browsers and CDNs. Subsequent visits would never hit the API, breaking click counting and making link edits/expiration ineffective.
- **302 (Found)** is not cached by default. Every visit reaches the API, ensuring accurate analytics and respecting link mutations (PATCH/DELETE/expiry).
- Response headers: `Cache-Control: no-store`, `X-Robots-Tag: noindex, nofollow` reinforce no-caching and no-indexing.

## Consequences
- ✅ Accurate click counting on every visit
- ✅ Link edits, expiration, deactivation work immediately
- ✅ SEO-safe: `noindex, nofollow` prevents hijacking
- ⚠️ Slightly higher latency vs cached 301 (mitigated by Redis cache on hot path)

## References
- CONTEXT.md §5 (Redirect public endpoint)
- CONTEXT.md §6 (Redirect e cache - "Usar 302 não 301")
- SECURITY.md §9 (SEO hijacking)