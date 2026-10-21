# Graph Report - Tricolink  (2026-10-21)

## Corpus Check
- 73 files · ~15,603 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 13, .example 1, .ini 1)

## Summary
- 623 nodes · 1307 edges · 27 communities (21 shown, 6 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 193 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c6a9491f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tricolink URL Shortener Product
- Token Bucket Rate Limiting
- Web App and UI Components
- Settings
- Agent Workflow and Graphify
- Compose and P01 Infra
- env.py
- AppError
- BucketPolicy
- logging.py
- test_body_limit.py
- test_middlewares.py
- pnpm Release Policy
- PostCSS Tooling
- API Package
- services.py
- pytest
- observability/metrics.py
- test_real_ip.py
- http.py
- SECURITY.md Security Requirements
- UI_SPEC.md Tricolink Interface
- Code Standards
- REST API /api/v1 Contract

## God Nodes (most connected - your core abstractions)
1. `Settings` - 45 edges
2. `BucketPolicy` - 27 edges
3. `create_app()` - 22 edges
4. `RateLimiter` - 21 edges
5. `CircuitBreaker` - 21 edges
6. `MemoryTokenBucket` - 20 edges
7. `AppError` - 20 edges
8. `RateLimitResult` - 18 edges
9. `SECURITY.md Security Requirements` - 17 edges
10. `Services` - 15 edges

## Surprising Connections (you probably didn't know these)
- `P02 Security Foundation Phase` --conceptually_related_to--> `API Compose Service`  [INFERRED]
  docs/agent/PROGRESS.md → docker-compose.yml
- `Python 3.11 and Poetry 2.4.1 Pin` --conceptually_related_to--> `API Compose Service`  [INFERRED]
  docs/agent/PROGRESS.md → docker-compose.yml
- `pnpm allowBuilds Allowlist` --conceptually_related_to--> `Web Compose Service`  [INFERRED]
  apps/web/pnpm-workspace.yaml → docker-compose.yml
- `Frontend Stack Version Pins` --conceptually_related_to--> `Web Compose Service`  [INFERRED]
  docs/agent/PROGRESS.md → docker-compose.yml
- `Pending Human Review of AI Translations` --conceptually_related_to--> `Web Compose Service`  [INFERRED]
  docs/agent/PROGRESS.md → docker-compose.yml

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Anti Cache Stampede Layer Set** — docs_agent_context_anti_cache_stampede, docs_agent_context_stale_while_revalidate, docs_agent_context_single_flight, docs_agent_context_negative_cache, docs_agent_security_bulkhead [EXTRACTED 1.00]
- **Redirect Hot Path Flow** — docs_agent_context_redirect_cache, docs_agent_context_302_redirect, docs_agent_context_click_stream, docs_agent_context_click_events_table, docs_agent_context_links_table [EXTRACTED 1.00]
- **Tricolink Docker Compose Development Stack** — docker_compose_postgres_service, docker_compose_redis_service, docker_compose_api_service, docker_compose_web_service, docker_compose_app_network, docker_compose_data_network [EXTRACTED 1.00]
- **P00 Graphify Bootstrap Pipeline** — docs_agent_progress_graphify_kilo_integration, docs_agent_progress_semantic_extraction_cache, docs_agent_progress_graph_artifacts, docs_agent_progress_phase_roadmap [INFERRED 0.85]
- **P01 Containerized Tooling and Validation** — docs_agent_progress_make_container_targets, docs_agent_progress_non_root_containers, docs_agent_progress_local_port_override, docs_agent_progress_p01_validation, docker_compose_api_service, docker_compose_web_service [INFERRED 0.85]
- **Defense in Depth Controls** — docs_agent_security_token_bucket, docs_agent_security_circuit_breaker, docs_agent_security_bulkhead, docs_agent_security_rls, docs_agent_context_url_policy [INFERRED 0.85]

## Communities (27 total, 6 thin omitted)

### Community 0 - "Tricolink URL Shortener Product"
Cohesion: 0.25
Nodes (8): click_events Table, Redis Stream Click Buffer, Non-Goals, Tricolink URL Shortener Product, Redirect and Cache Hot Path, URL Anti-Abuse Policy, SSRF Prevention, Design Tokens

### Community 1 - "Token Bucket Rate Limiting"
Cohesion: 0.24
Nodes (9): Daily Link Quotas, Negative Cache for Unknown Codes, Single-Flight Lock, Stale-While-Revalidate Caching, Brute Force Protection, Bulkhead Semaphores, Circuit Breaker, Rate Limit Buckets (+1 more)

### Community 2 - "Web App and UI Components"
Cohesion: 0.12
Nodes (7): nextConfig, geist, metadata, RootLayout(), Button(), buttonVariants, cn()

### Community 3 - "Settings"
Cohesion: 0.06
Nodes (35): _boolean(), _env(), get_settings(), _integer(), _number(), Settings, SettingsError, _text() (+27 more)

### Community 4 - "Agent Workflow and Graphify"
Cohesion: 0.18
Nodes (8): graphify Slash Command, Mandatory Session Reading Order, CONTEXT.md Single Source of Truth, Graphify Context Engineering, Graphify Installation Commands, Per-Phase Graphify Routine, graphify query/path/explain Workflow, Tricolink README Stub (P11)

### Community 5 - "Compose and P01 Infra"
Cohesion: 0.16
Nodes (20): pnpm allowBuilds Allowlist, API Compose Service, app Network, data Network, postgres_data Volume, PostgreSQL 16 Compose Service, Redis 7 Compose Service, Web Compose Service (+12 more)

### Community 6 - "env.py"
Cohesion: 0.09
Nodes (13): do_run_migrations(), run_async_migrations(), run_migrations_online(), upgrade(), Base, ClickEvent, Link, RefreshToken (+5 more)

### Community 7 - "AppError"
Cohesion: 0.06
Nodes (27): install_error_handlers(), handle_app_error(), handle_http_exception(), handle_unexpected_error(), handle_validation_error(), _json_error(), AppError, BadRequestError (+19 more)

### Community 8 - "BucketPolicy"
Cohesion: 0.06
Nodes (34): GlobalRateLimitMiddleware, _headers(), record_rate_limit_fallback(), record_rate_limited(), apply_rate_limit_headers(), client_ip(), _get_limiter(), rate_limit() (+26 more)

### Community 9 - "logging.py"
Cohesion: 0.14
Nodes (6): configure_logging(), get_logger(), MetricsMiddleware, _route_path(), record_request(), lifespan()

### Community 10 - "test_body_limit.py"
Cohesion: 0.07
Nodes (16): BodyLimitMiddleware, replay_body(), _header_values(), _send_json(), send_with_headers(), capture_status(), send_with_headers(), run() (+8 more)

### Community 11 - "test_middlewares.py"
Cohesion: 0.09
Nodes (13): _incoming_request_id(), RequestIDMiddleware, send_with_request_id(), SecurityHeadersMiddleware, RequestTimeoutMiddleware, new_uuid(), build_inner(), test_hsts_only_in_production() (+5 more)

### Community 18 - "services.py"
Cohesion: 0.08
Nodes (12): get_cache(), get_rate_limiter(), get_services(), get_session(), settings_dependency(), create_engine(), create_session_factory(), unit_of_work() (+4 more)

### Community 19 - "pytest"
Cohesion: 0.11
Nodes (9): record_circuit_state(), CircuitBreaker, CircuitState, CircuitOpenError, fail(), test_breaker_half_open_failure_reopens(), test_breaker_half_open_success_closes(), test_breaker_opens_after_threshold_and_rejects_calls() (+1 more)

### Community 20 - "observability/metrics.py"
Cohesion: 0.12
Nodes (7): CacheClient, record_cache_hit(), record_cache_miss(), FakeRedis, _sample(), test_cache_get_records_hit_and_miss(), test_cache_set_validates_ttl_and_delete()

### Community 21 - "test_real_ip.py"
Cohesion: 0.13
Nodes (9): _forwarded_for(), RealIPMiddleware, resolve_real_ip(), _NeverRedis, test_middleware_sets_request_client_to_real_ip(), test_resolve_real_ip_counts_from_the_right(), test_resolve_real_ip_falls_back_when_header_is_invalid_or_short(), test_resolve_real_ip_without_trusted_proxies_ignores_header() (+1 more)

### Community 22 - "http.py"
Cohesion: 0.15
Nodes (10): Services, close_redis(), ping_redis(), _authorized(), _check_database(), _check_redis(), health_live(), health_ready() (+2 more)

### Community 23 - "SECURITY.md Security Requirements"
Cohesion: 0.31
Nodes (9): Next.js Locale Routing and Rewrites, JWT and Rotating Refresh Sessions, CSRF Double-Submit Protection, Google OIDC, Logical Buffer Overflow Limits, SECURITY.md Security Requirements, Row Level Security, Anti SQL Injection (+1 more)

### Community 24 - "UI_SPEC.md Tricolink Interface"
Cohesion: 0.36
Nodes (9): 11-Language i18n, UI/UX Summary, Account Page, UI_SPEC.md Tricolink Interface, Landing Page, Link Detail Page, Links List Page, Login Page (+1 more)

### Community 25 - "Code Standards"
Cohesion: 0.25
Nodes (6): Modular Monolith with Clean Architecture, Monorepo Structure, Secrets via core/config.py, Credential Hygiene, Anti XSS and CSP Nonce, States and Quality Targets

### Community 26 - "REST API /api/v1 Contract"
Cohesion: 0.33
Nodes (7): 7-Char Base62 Code Generation, links Table, refresh_tokens Table, Reserved Alias List, REST API /api/v1 Contract, users Table, SEO Indexation Control

## Knowledge Gaps
- **18 isolated node(s):** `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching`, `lucide-react 1.60.0`, `minimumReleaseAgeExclude Policy` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 163 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_app()` connect `Settings` to `AppError`, `BucketPolicy`, `logging.py`, `test_body_limit.py`, `test_middlewares.py`, `test_real_ip.py`, `http.py`?**
  _High betweenness centrality (0.122) - this node is a cross-community bridge._
- **Are the 28 inferred relationships involving `Settings` (e.g. with `settings_dependency()` and `configure_logging()`) actually correct?**
  _`Settings` has 28 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Web App and UI Components` be split into smaller, more focused modules?**
  _Cohesion score 0.12380952380952381 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `BucketPolicy`, `logging.py`, `services.py`, `http.py`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `BucketPolicy` (e.g. with `MemoryTokenBucket` and `_reset_seconds()`) actually correct?**
  _`BucketPolicy` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `Settings` be split into smaller, more focused modules?**
  _Cohesion score 0.06298904538341157 - nodes in this community are weakly interconnected._