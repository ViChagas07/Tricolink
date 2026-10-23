# Tricolink

A secure, privacy-first URL shortener built as a portfolio project demonstrating backend engineering, security hardening, and polished UI.

**Paste a long URL → get `https://your-domain.com/abc1234` → every visit is a counted 302 redirect with stats.**

[Demo](https://tricolink.vercel.app) · [API Docs](https://tricolink-api.onrender.com/docs) *(placeholder — deploy your own)*

## Screenshots

| Landing | Links Dashboard | Link Detail / Stats |
|---|---|---|
| ![Landing](docs/assets/landing.png) | ![Dashboard](docs/assets/dashboard.png) | ![Stats](docs/assets/stats.png) |

> **Add real screenshots:** run the app locally, take screenshots at 1440×900 (light & dark), drop them in `docs/assets/`, and update the paths above.

---

## How It Works

```mermaid
flowchart TD
    A[User pastes long URL] --> B{Authenticated?}
    B -->|No| C[Anonymous: quota 5/day, 30-day TTL]
    B -->|Yes| D[Logged in: quota 100/day, no expiry]
    C --> E[Validate URL policy]
    D --> E
    E --> F[Generate 7-char base62 code\n(secrets, collision retry ≤5)]
    F --> G[Store in PostgreSQL\nUNIQUE code, RLS enforced]
    G --> H[Return short URL]
    H --> I[Visitor hits /{code}]
    I --> J[FastAPI /r/{code}]
    J --> K{Redis cache hit?}
    K -->|Yes| L[Serve stale + background refresh\nSWR + jitter + single-flight]
    K -->|No| M[Query PostgreSQL\n(lock + negative cache)]
    L --> N[302 redirect to original URL]
    M --> N
    N --> O[Push click event to Redis Stream\ntl:clicks (never blocks redirect)]
    O --> P[Async flusher batches writes\nincrements click_count]
```

---

## Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, FastAPI, Pydantic v2, SQLAlchemy 2 (async) + asyncpg, Alembic |
| **Database** | PostgreSQL 16 |
| **Cache / Rate limiting** | Redis 7 (cache, token bucket via Lua, locks, click stream) |
| **Auth** | Email/password (argon2id) + Google OAuth2/OIDC (Authlib); JWT in httpOnly cookies |
| **Frontend** | Next.js 16 (App Router), TypeScript, Tailwind CSS, shadcn/ui, Zustand, next-intl, Recharts, lucide-react |
| **Infra** | Docker Compose (dev), GitHub Actions (CI/CD), deploy: Vercel (web) + Render (API, Postgres, Redis) |
| **Tests** | pytest + pytest-asyncio + httpx; Vitest; Playwright; k6 (load) |
| **Observability** | Prometheus (`/metrics` protected), structured logs, Sentry (optional) |

**Architecture:** Modular monolith with **Clean Architecture inside each module** (domain → application → adapters → presentation). SOLID, strict typing, no `any`, SQL only via SQLAlchemy with bound parameters.

---

## Architecture

```mermaid
graph TB
    subgraph API[FastAPI App]
        CORE[core/config.py\nSingle env reader]
        MID[Middleware stack\nrequest-id → security headers → metrics → real-IP → timeout → global bucket → body limit]
        MOD[Modules]
        MOD --> ID[identity\nAuth, sessions, Google OIDC]
        MOD --> LK[links\nShorten, redirect, cache, quotas]
        MOD --> AN[analytics\nStats, click flusher]
        ID --> DOM_ID[domain]
        LK --> DOM_LK[domain]
        AN --> DOM_AN[domain]
        DOM_ID --> APP_ID[application]
        DOM_LK --> APP_LK[application]
        DOM_AN --> APP_AN[application]
        APP_ID --> AD_ID[adapters\nSQLAlchemy, Redis, Authlib]
        APP_LK --> AD_LK[adapters\nSQLAlchemy, Redis cache]
        APP_AN --> AD_AN[adapters\nSQLAlchemy, Redis cache]
        AD_ID --> PRES_ID[presentation\nFastAPI routers]
        AD_LK --> PRES_LK[presentation\nFastAPI routers]
        AD_AN --> PRES_AN[presentation\nFastAPI routers]
    end

    subgraph WEB[Next.js App]
        PROXY[proxy.ts\nCSP nonce, rewrites, locale]
        PAGES[App Router pages\n/[locale]/*]
        COMP[Components\nshadcn/ui + Tailwind]
        STORE[Zustand stores\nauth, theme]
        I18N[next-intl\n11 locales]
    end

    API <-- rewrites /api/v1/* --> WEB
    API <-- rewrites /:code --> WEB
    API --> PG[(PostgreSQL 16\nRLS FORCE)]
    API --> RD[(Redis 7)]
    WEB --> VERCEL[Vercel]
    API --> RENDER[Render]
```

---

## Quick Start (Docker)

```bash
# 1. Clone and configure
git clone https://github.com/your-org/tricolink.git
cd tricolink
cp .env.example .env
# Edit .env with your secrets (JWT_SECRET, CSRF_SECRET, etc.)

# 2. Start everything
make up
# API: http://localhost:8000  |  Web: http://localhost:3000

# 3. Run tests
make test-api    # 400+ pytest tests
make test-web    # 100+ Vitest + 20 Playwright

# 4. Lint & type-check
make lint

# 5. Stop
make down
```

### Useful Make Targets

| Target | Description |
|---|---|
| `make up` | Start all services (builds images, runs migrations) |
| `make down` | Stop and remove containers |
| `make logs` | Tail logs from all services |
| `make test-api` | Run API tests in container |
| `make test-web` | Run web tests in container |
| `make lint` | Ruff, mypy, ESLint, TypeScript check |
| `make format` | Auto-fix formatting |
| `make migrate` | Run Alembic migrations |
| `make coverage` | API coverage (≥85% global, ≥90% domain) |
| `make coverage-domain` | Domain-only coverage |
| `make cleanup` | Run click/link retention job |
| `make observability-up` | Start Prometheus + Grafana (port 9091 / 3002) |

---

## Local Development (without Docker)

### API
```bash
cd apps/api
poetry install
poetry run alembic upgrade head
poetry run uvicorn tricolink.main:create_app --reload --port 8000
```

### Web
```bash
cd apps/web
pnpm install
pnpm dev
# http://localhost:3000
```

> **Note:** The Docker Compose setup is the *validated* path. Local runs require Postgres 16 and Redis 7 running separately.

---

## Environment Variables

All secrets are read **only** in `apps/api/src/tricolink/core/config.py` via `os.getenv()`. Never commit `.env`.

### API (required)

| Variable | Description | Example |
|---|---|---|
| `APP_ENV` | `development` \| `production` | `development` |
| `DATABASE_URL` | Runtime DB URL (app role, RLS) | `postgresql+asyncpg://user:pass@host:5432/db` |
| `MIGRATION_DATABASE_URL` | Admin DB URL for migrations | `postgresql+asyncpg://admin:pass@host:5432/db` |
| `REDIS_URL` | Redis connection | `redis://redis:6379/0` |
| `JWT_SECRET` | ≥32 random bytes | `openssl rand -hex 32` |
| `CSRF_SECRET` | ≥32 random bytes | `openssl rand -hex 32` |
| `SESSION_SECRET` | ≥32 random bytes | `openssl rand -hex 32` |
| `FRONTEND_ORIGIN` | Web origin for CORS/CSRF/OAuth | `http://localhost:3000` |
| `SHORT_BASE_URL` | Base for displayed short URLs | `http://localhost:3000` |
| `API_PUBLIC_BASE_URL` | Public API URL | `http://localhost:8000` |
| `COOKIE_SECURE` | `true` in production | `false` |
| `TRUSTED_PROXY_COUNT` | Proxies to trust for `X-Forwarded-For` | `1` (dev), `2` (Vercel→Render) |

### Auth (optional but recommended)
| Variable | Description |
|---|---|
| `GOOGLE_CLIENT_ID` | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret |
| `GOOGLE_REDIRECT_URI` | Must match Google Cloud Console exactly |

### Rate Limiting & Cache (defaults shown)
| Variable | Default | Description |
|---|---|---|
| `RL_REDIRECT_CAPACITY` | 120 | Redirect bucket capacity per IP |
| `RL_REDIRECT_REFILL_PER_SEC` | 20 | Redirect bucket refill rate |
| `RL_CREATE_CAPACITY` | 10 | Create bucket capacity |
| `RL_CREATE_REFILL_PER_SEC` | 0.2 | Create bucket refill |
| `RL_AUTH_CAPACITY` | 5 | Auth bucket capacity (IP + email) |
| `RL_AUTH_REFILL_PER_SEC` | 0.02 | Auth bucket refill |
| `RL_GLOBAL_CAPACITY` | 2000 | Global load-shedding bucket |
| `RL_GLOBAL_REFILL_PER_SEC` | 1000 | Global refill |
| `RL_LIST_CAPACITY` | 60 | Stats/list bucket per user |
| `RL_LIST_REFILL_PER_SEC` | 1 | Stats/list refill |
| `CACHE_HARD_TTL_SECONDS` | 86400 | Hard TTL for redirect cache |
| `CACHE_SOFT_TTL_SECONDS` | 600 | Soft TTL (SWR trigger) |
| `CACHE_JITTER_PCT` | 0.15 | ±Jitter on all TTLs |
| `NEGATIVE_CACHE_TTL_SECONDS` | 30 | TTL for 404 codes |
| `STATS_CACHE_TTL_SECONDS` | 30 | Stats cache TTL |

### Web
| Variable | Description |
|---|---|
| `NEXT_PUBLIC_SITE_URL` | Public web origin |
| `NEXT_PUBLIC_SHORT_BASE_URL` | Short URL base for client |
| `API_INTERNAL_URL` | Internal API URL (used at build time for rewrites) |

---

## API Reference

Base path: `/api/v1` · JSON · Errors: `{ "error": { "code", "message", "details?" } }`

### Links
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/links` | Optional | Create short link. Body: `{ url, alias?, title?, expires_at? }` (alias/title/expires require auth). Returns `{ code, short_url, original_url, created_at, expires_at }` |
| `GET` | `/links` | Required | List user's links. Query: `cursor`, `limit` (max 50), `q` (search) |
| `GET` | `/links/overview` | Required | `{ total_clicks, total_links, range }` for header. Query: `range=7d\|30d\|90d` |
| `GET` | `/links/{code}` | Required (owner) | Get link details |
| `PATCH` | `/links/{code}` | Required (owner) | Update `title`, `original_url`, `expires_at`, `is_active` |
| `DELETE` | `/links/{code}` | Required (owner) | Delete link (404 if not owner) |
| `GET` | `/links/{code}/stats` | Required (owner) | Stats: `{ total, series[{date,clicks}], countries[], devices[], referrers[] }`. Query: `range=7d\|30d\|90d` |

### Auth
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Register (202, no session) |
| `POST` | `/auth/login` | Login (sets httpOnly cookies) |
| `POST` | `/auth/refresh` | Rotate refresh token |
| `POST` | `/auth/logout` | Revoke refresh, clear cookies |
| `GET` | `/auth/me` | Current user |
| `PATCH` | `/auth/me` | Update `display_name`, `locale` |
| `GET` | `/auth/me/avatar` | Custom avatar bytes (8 KB max) |
| `PUT` | `/auth/me/avatar` | Upload avatar (base64 JPEG/PNG/WebP ≤12K chars) |
| `DELETE` | `/auth/me/avatar` | Remove custom avatar |
| `GET` | `/auth/google/login` | Start Google OAuth |
| `GET` | `/auth/google/callback` | OAuth callback |

### Ops
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health/live` | Liveness probe |
| `GET` | `/health/ready` | Readiness (DB + Redis + tables) |
| `GET` | `/metrics` | Prometheus (Bearer `METRICS_TOKEN`) |

### Redirect (public)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/r/{code}` | **302** to original URL; **404** if not found; **410** if expired/inactive. `Cache-Control: no-store`, `X-Robots-Tag: noindex, nofollow` |

---

## Internationalization (i18n)

11 languages via `next-intl`:
- `en` (default), `pt-BR`, `es`, `fr`, `de`, `it`, `ja`, `ko`, `zh-CN`, `ru`, `ar` (RTL)

- `localePrefix: always` → all URLs prefixed (`/en/links`, `/pt-BR/links`)
- Accept-Language detection enabled
- Messages in `apps/web/messages/<locale>.json` (namespaces: `nav`, `hero`, `demo`, `features`, `faq`, `auth`, `links`, `account`, `errors`, `footer`, `meta`)
- `pt-BR` and `en` are reference; others are AI-generated and **marked for human review** (see `PROGRESS.md`)
- CI fails on missing keys: `pnpm i18n:check`
- Dates/numbers via `Intl`; `hreflang`, sitemap, OG per locale

---

## Testing

### API (pytest)
```bash
make test-api                    # All tests
docker compose run --rm api pytest -q tests/security   # Security suite only
docker compose run --rm api pytest --cov=tricolink --cov-fail-under=85
docker compose run --rm api pytest --cov=tricolink --cov-report=term-missing
```

**Gates (CI):**
- Global coverage ≥ 85% (current: **90.40%**)
- Domain coverage ≥ 90% (current: **96%**)
- Ruff, mypy, format check must pass

### Web (Vitest + Playwright)
```bash
cd apps/web
pnpm test           # Unit/component (91 tests)
pnpm test:e2e       # Playwright (20 tests, Chromium)
pnpm lint           # ESLint
pnpm typecheck      # tsc --noEmit
pnpm i18n:check     # All 11 locales complete
```

### Load (k6)
```bash
# From repo root, with API + Postgres + Redis running
docker compose exec -T redis redis-cli FLUSHDB
Get-Content -Raw loadtest/redirect.js | docker run --rm -i --network tricolink_app -e BASE_URL=http://api:8000 -e MODE=warm grafana/k6 run -
Get-Content -Raw loadtest/redirect.js | docker run --rm -i --network tricolink_app -e BASE_URL=http://api:8000 -e MODE=cold grafana/k6 run -
Get-Content -Raw loadtest/create.js   | docker run --rm -i --network tricolink_app -e BASE_URL=http://api:8000 -e MODE=throughput grafana/k6 run -
```

**Real results (Docker Desktop, Ryzen 7 5800X, 16 GB):**
- Redirect warm: **101 RPS**, p50 **4.84 ms**, p95 **942 ms**, 0 429
- Redirect cold (500 codes): **88.5 RPS**, p50 **342 ms**, 100% 302
- Redirect rate limit: **8,531 429** (83.2%)
- Create throughput: **72.7 RPS**, p50 **69.8 ms**
- Create rate limit (IP fixed): **2,530 429** (99.8%, daily quota 5)

> Full methodology and caveats in `docs/perf/RESULTS.md`. Numbers are local, not production extrapolations.

---

## Deploy

**Validated path:** Vercel (web) + Render (API, Postgres, Redis) via GitHub Actions.

### 1. Render (API + DB + Redis + Cron)
1. Render Dashboard → **New → Blueprint** → select repo → reads `render.yaml`
2. Creates: `tricolink-api` (Docker, `runtime` stage), `tricolink-db` (Postgres), `tricolink-redis` (Key Value), `tricolink-cleanup` (cron 03:00 UTC)
3. **Required:** Run `docs/deploy/render_app_role.sql` on the Postgres admin connection to create the `tricolink_app` role (`NOSUPERUSER NOBYPASSRLS`). Set `DATABASE_URL` to this role.
4. Set all variables from `docs/deploy/DEPLOY.md §3.1` (JWT_SECRET, FRONTEND_ORIGIN, TRUSTED_PROXY_COUNT=2, etc.)
5. `preDeployCommand: alembic upgrade head` runs migrations using `MIGRATION_DATABASE_URL` (admin)

### 2. Vercel (Web)
1. Import repo → Root Directory: `apps/web`
2. Build Command: `pnpm build` (Turbopack)
3. Env vars (Production + Preview):
   - `API_INTERNAL_URL=https://tricolink-api.onrender.com`
   - `NEXT_PUBLIC_SITE_URL=https://your-app.vercel.app`
   - `NEXT_PUBLIC_SHORT_BASE_URL=https://your-app.vercel.app`
4. **No secrets** in Vercel (no `NEXT_PUBLIC_` for secrets)

### 3. GitHub Actions
- `.github/workflows/ci.yml`: lint, typecheck, test (API + Web), security (gitleaks, pip-audit, pnpm audit), Docker build
- `.github/workflows/deploy.yml`: manual (`workflow_dispatch`) or tag `v*` → calls Render/Vercel deploy hooks → health checks

> **Not yet executed in CI:** GitHub Actions runs, Render Blueprint apply, Vercel deploy. See `docs/deploy/DEPLOY.md` for full checklist.

---

## Engineering Decisions

### 302 vs 301
**302 (Found)** is used for redirects. A 301 would be cached by browsers/CDNs, breaking click counting and making link edits/expiration ineffective. 302 ensures every hit reaches the API.

### Code Generation & Collisions
- 7-character base62 via `secrets` (cryptographically secure, not `random`)
- `UNIQUE(code)` in PostgreSQL; on `IntegrityError` retry up to 5 times
- Custom alias: regex `^[A-Za-z0-9_-]{3,32}$` + reserved list (routes, locales, `admin`, `api`, etc.); 409 on conflict

### SWR + Jitter + Single-Flight + Negative Cache (Why?)
**Problem:** Cache stampede on cold keys → thundering herd on PostgreSQL.
**Solution (3 layers):**
1. **Stale-While-Revalidate:** Soft TTL (600s) serves stale data while one background refresh runs; hard TTL (86400s) is the Redis key expiry.
2. **Jitter (±15%)** on all TTLs prevents synchronized expiration across keys.
3. **Single-flight:** In-process task deduplication + `SET NX PX` Redis lock across processes. Only one loader hits the DB; others wait with jitter and re-read cache.
4. **Negative cache** (`tl:neg:{code}`, 30s) for non-existent codes blocks scan/penetration attacks.

### Async Click Pipeline (Redis Stream + Flusher)
- Redirect **never waits** for INSERT. `XADD` to `tl:clicks` stream (fire-and-forget).
- Background flusher (lifespan task) consumes via consumer group, batches `click_events` INSERT + `links.click_count` UPDATE in one transaction.
- Redis down → event dropped, metric `clicks_dropped_total` incremented, redirect continues.
- Flusher recreates consumer group on `NOGROUP` (failover/FLUSHDB resilience).
- Flusher invalidates all three stats cache windows (`7d`, `30d`, `90d`) after commit → detail page reflects `click_count` immediately.

### Token Bucket in Lua
Single atomic Lua script (`refill + consume`) using Redis `TIME` (server-side clock). Returns `allowed, remaining, retry_after_ms`. No race conditions. Redis down → circuit breaker opens → **in-memory fallback per process** (still rate-limits, never "allow all").

### Circuit Breaker + Bulkhead
- **Circuit Breaker** (closed/open/half-open) on Redis and Postgres clients. Clock injectable for tests. Half-open probes limited.
- **Named Bulkheads** (semaphores): `db_read` (20), `db_write` (10), `hashing` (4, argon2 in threadpool), `dns` (10). Prevents one saturated dependency from starving others.

### Server Never Fetches User URLs
Zero SSRF surface: the API **never** makes outbound HTTP to user-supplied URLs. `UrlPolicy` validates at create time only (DNS resolve + IP checks, IDN normalization, block private/metadata/loopback/own-domain). No preview, no title fetch.

### Privacy (No IP Stored)
- `click_events` stores only: `country` (from edge header `X-Vercel-IP-Country` / `CF-IPCountry`), `device`, `browser`, `referrer_host` (no path/query).
- **No IP**, no raw User-Agent. LGPD/GDPR friendly by design.
- Daily quotas hash IP (SHA-256) in Redis; no plaintext IP persisted.

### Row Level Security (RLS)
- `links` and `refresh_tokens`: `RLS ENABLE` + `FORCE` with policies on `app.current_user_id` (set via `SET LOCAL` per transaction).
- Runtime role `tricolink_app` is `NOSUPERUSER NOBYPASSRLS`.
- Defense in depth: app checks ownership **and** DB enforces it. Even with SQL injection, cross-user reads/writes return 0 rows.

---

## Security Summary

Full audit in `docs/security/AUDIT.md` (P09). **Zero critical/high findings open.**

| Area | Status |
|---|---|
| Token bucket (Lua, atomic) | ✅ Tested under concurrency |
| Circuit breaker + bulkhead | ✅ All dependencies |
| SQL injection | ✅ ORM only, RLS enforced, offensive tests pass |
| XSS / CSP | ✅ Nonce per request, `strict-dynamic`, no `unsafe-inline` in `script-src` (`style-src-attr` exception for Recharts documented) |
| Auth / brute force | ✅ Argon2id OWASP, rotating refresh, reuse detection, IP+email buckets, lockout, no enumeration |
| SSRF / URL abuse | ✅ DNS resolve + all IPs checked, block private/metadata/own-domain, no outbound fetch |
| Secrets | ✅ `.env` gitignored, gitleaks clean, `os.getenv` only in `config.py`, no secrets in client bundle |
| Supply chain | ✅ Lockfiles committed, Dependabot, `pip-audit`/`pnpm audit --prod` clean |

**Residual risks (accepted, documented):**
- R-01: No email verification on local signup (squatting possible)
- R-02: Access JWT not revoked on logout (valid until `exp`, default 10 years)
- R-03: Cache invalidation gap if Redis fails during invalidation
- R-04: `click_events` lacks RLS
- R-05: `/health/ready` exempt from global bucket
- R-06: `TRUSTED_PROXY_COUNT` trusts topology
- R-10: `style-src-attr 'unsafe-inline'` for Recharts

---

## Performance Summary

Real k6 measurements (local Docker Desktop, **not production**):

| Scenario | RPS | p50 | p95 | p99 | Notes |
|---|---:|---:|---:|---:|---|
| Redirect warm | **101** | **4.8 ms** | **942 ms** | 1.6 s | 0 429, 42 5xx (concurrency limit) |
| Redirect cold (500 codes) | **88.5** | **342 ms** | 1.5 s | 1.5 s | 100% 302, single-flight prevents stampede |
| Redirect rate limit | 157 | 2.5 ms | 177 ms | 2.2 s | **8,531 429** (83.2%) |
| Create throughput | **72.7** | **69.8 ms** | 881 ms | 1.1 s | 99.85% 201 |
| Create rate limit (IP fixed) | 46 | 3.2 ms | 21 ms | 158 ms | **2,530 429** (99.8%, daily quota) |

**Bottleneck:** `--limit-concurrency 200` on dev Uvicorn. Production (Gunicorn + WAF) changes the ceiling. **Do not extrapolate.**

Full data: `docs/perf/RESULTS.md`

---

## Roadmap

Honest, not committed:

- [ ] QR Code generation for short links
- [ ] Custom domains (bring your own domain)
- [ ] Safe Browsing API integration (malware/phishing check)
- [ ] UTM parameter preservation / builder
- [ ] Link-in-bio / Pages
- [ ] Team/workspace support
- [ ] Browser extension
- [ ] Public API with scoped tokens
- [ ] Email verification for local accounts
- [ ] Access token denylist (revoke on logout)

---

## Known Limitations

From `PROGRESS.md > Não validado` and pending reviews:

- **No real CI/CD execution:** GitHub Actions workflows pass `actionlint` but never ran on GitHub runners.
- **No production deploy:** Render Blueprint, Vercel project, and `TRUSTED_PROXY_COUNT=2` hypothesis untested.
- **No Linux/macOS validation:** All containers tested on Docker Desktop/Windows only.
- **No Firefox/WebKit tests:** Playwright runs Chromium only.
- **No email verification:** Local signup allows squatting (AUDIT R-01).
- **Access JWT not revoked on logout:** Valid until expiry (AUDIT R-02).
- **At-least-once clicks:** Flusher crash between commit and `XACK` can duplicate `click_events`/`click_count` (no idempotency key).
- **DNS not pinned:** `UrlPolicy` resolves at create time; later DNS changes not protected (mitigated by no outbound fetch).
- **Google OIDC not tested against real IdP:** Mocked in tests only.
- **Render managed Postgres role/SSL/citext** not verified.
- **Prometheus multiprocess mode** not implemented (2 gunicorn workers → each scrape sees one worker's metrics).
- **Lighthouse mobile Performance < 95:** Best 89 (LCP on hero logo). Desktop 99.
- **Translations pending human review:** `es`, `fr`, `de`, `it`, `ja`, `ko`, `zh-CN`, `ru`, `ar` (244 keys total; `pt-BR`/`en` are reference).
- **Docker `runner` image (standalone web)** not revalidated after P10 fixes.
- **Header size limit** not tested end-to-end (Uvicorn default ~16 KB).

---

## ADRs

See `docs/ADR/` for Architecture Decision Records:
- `001-modular-monolith-clean-architecture.md`
- `002-302-redirect-for-click-counting.md`
- `003-swr-jitter-single-flight-negative-cache.md`
- `004-async-click-pipeline-redis-stream.md`
- `005-lua-token-bucket-rate-limiting.md`
- `006-circuit-breaker-bulkhead-resilience.md`
- `007-rls-defense-in-depth.md`

---

## Contributing

See `CONTRIBUTING.md` for guidelines (conventional commits, TDD, lint gates, ADR process).

---

## License

MIT — see `LICENSE`.