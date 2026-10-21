# Graph Report - Tricolink  (2026-10-21)

## Corpus Check
- 115 files · ~29,362 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 13, .example 1, .ini 1)

## Summary
- 1128 nodes · 3176 edges · 55 communities (46 shown, 9 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 522 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f4626260`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tricolink URL Shortener Product
- Token Bucket Rate Limiting
- Web App and UI Components
- config.py
- Agent Workflow and Graphify
- Compose and P01 Infra
- db/models.py
- error_handlers.py
- BucketPolicy
- logging.py
- test_body_limit.py
- test_redirect_click_failure.py
- pnpm Release Policy
- PostCSS Tooling
- API Package
- Bulkhead
- pytest
- observability/metrics.py
- http.py
- SECURITY.md Security Requirements
- UI_SPEC.md Tricolink Interface
- Code Standards
- REST API /api/v1 Contract
- ShortCode
- test_click_pipeline.py
- router.py
- pytest
- .__init__
- test_url_policy.py
- ports.py
- repository.py
- value_objects.py
- update_link.py
- OriginalUrl
- Database
- create_link.py
- build_services
- cache.py
- daily_quota.py
- resolve_link.py
- Settings
- test_links_api.py
- list_links.py
- main.py
- test_link_collision.py
- sqlalchemy
- collections_abc
- logging.py
- CacheClient
- test_links_repository.py
- create_redis
- ids.py

## God Nodes (most connected - your core abstractions)
1. `ShortCode` - 83 edges
2. `Link` - 74 edges
3. `Settings` - 72 edges
4. `build_services()` - 33 edges
5. `OriginalUrl` - 33 edges
6. `AppError` - 33 edges
7. `RedisLinkCache` - 31 edges
8. `CreateLink` - 30 edges
9. `LinkRepository` - 28 edges
10. `BucketPolicy` - 27 edges

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

## Communities (55 total, 9 thin omitted)

### Community 0 - "Tricolink URL Shortener Product"
Cohesion: 0.25
Nodes (8): click_events Table, Redis Stream Click Buffer, Non-Goals, Tricolink URL Shortener Product, Redirect and Cache Hot Path, URL Anti-Abuse Policy, SSRF Prevention, Design Tokens

### Community 1 - "Token Bucket Rate Limiting"
Cohesion: 0.24
Nodes (9): Daily Link Quotas, Negative Cache for Unknown Codes, Single-Flight Lock, Stale-While-Revalidate Caching, Brute Force Protection, Bulkhead Semaphores, Circuit Breaker, Rate Limit Buckets (+1 more)

### Community 2 - "Web App and UI Components"
Cohesion: 0.12
Nodes (7): nextConfig, geist, metadata, RootLayout(), Button(), buttonVariants, cn()

### Community 3 - "config.py"
Cohesion: 0.15
Nodes (16): _boolean(), _env(), _integer(), _number(), SettingsError, _text(), _text_or_empty(), test_development_enables_docs() (+8 more)

### Community 4 - "Agent Workflow and Graphify"
Cohesion: 0.18
Nodes (8): graphify Slash Command, Mandatory Session Reading Order, CONTEXT.md Single Source of Truth, Graphify Context Engineering, Graphify Installation Commands, Per-Phase Graphify Routine, graphify query/path/explain Workflow, Tricolink README Stub (P11)

### Community 5 - "Compose and P01 Infra"
Cohesion: 0.16
Nodes (20): pnpm allowBuilds Allowlist, API Compose Service, app Network, data Network, postgres_data Volume, PostgreSQL 16 Compose Service, Redis 7 Compose Service, Web Compose Service (+12 more)

### Community 6 - "db/models.py"
Cohesion: 0.23
Nodes (7): Base, Link, RefreshToken, User, test_click_events_have_device_check_and_index(), test_links_have_required_constraints_and_indexes(), test_users_and_refresh_tokens_have_required_uniques()

### Community 7 - "error_handlers.py"
Cohesion: 0.06
Nodes (23): install_error_handlers(), handle_app_error(), handle_http_exception(), handle_unexpected_error(), handle_validation_error(), _json_error(), _forwarded_for(), RealIPMiddleware (+15 more)

### Community 8 - "BucketPolicy"
Cohesion: 0.06
Nodes (29): GlobalRateLimitMiddleware, send_with_headers(), _headers(), capture_status(), record_rate_limit_fallback(), record_rate_limited(), _get_limiter(), _retry_after_seconds() (+21 more)

### Community 9 - "logging.py"
Cohesion: 0.21
Nodes (3): MetricsMiddleware, _route_path(), record_request()

### Community 10 - "test_body_limit.py"
Cohesion: 0.10
Nodes (12): BodyLimitMiddleware, replay_body(), _header_values(), _send_json(), run(), tracked_send(), build_app(), test_accepts_body_at_limit() (+4 more)

### Community 11 - "test_redirect_click_failure.py"
Cohesion: 0.06
Nodes (22): _incoming_request_id(), RequestIDMiddleware, send_with_request_id(), SecurityHeadersMiddleware, send_with_headers(), RequestTimeoutMiddleware, RedisTokenBucket, BlockingPublisher (+14 more)

### Community 18 - "Bulkhead"
Cohesion: 0.14
Nodes (7): build_bulkheads(), Bulkhead, BulkheadRegistry, BulkheadFullError, test_bulkhead_limits_concurrency(), test_bulkhead_times_out_when_full(), test_bulkheads_are_named_and_independent()

### Community 19 - "pytest"
Cohesion: 0.09
Nodes (8): CircuitBreaker, CircuitState, CircuitOpenError, fail(), test_breaker_half_open_failure_reopens(), test_breaker_half_open_success_closes(), test_breaker_opens_after_threshold_and_rejects_calls(), test_half_open_allows_only_configured_probes()

### Community 20 - "observability/metrics.py"
Cohesion: 0.21
Nodes (4): FakeRedis, _sample(), test_cache_get_records_hit_and_miss(), test_cache_set_validates_ttl_and_delete()

### Community 22 - "http.py"
Cohesion: 0.14
Nodes (11): Services, close_redis(), ping_redis(), _authorized(), _check_database(), _check_redis(), health_live(), health_ready() (+3 more)

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

### Community 27 - "ShortCode"
Cohesion: 0.09
Nodes (22): jittered_ttl(), _CacheRead, _entry_from_link(), RedisLinkCache, CacheEntry, Link, ShortCode, cache_settings() (+14 more)

### Community 28 - "test_click_pipeline.py"
Cohesion: 0.07
Nodes (26): ClickEvent, ClickFlusher, guarded(), _parse_event(), RedisClickPublisher, operation(), _browser(), ClickEvent (+18 more)

### Community 29 - "router.py"
Cohesion: 0.08
Nodes (39): CurrentUser, get_cache(), get_current_user(), get_current_user_optional(), get_rate_limiter(), get_services(), get_session(), settings_dependency() (+31 more)

### Community 30 - "pytest"
Cohesion: 0.11
Nodes (27): CreateLinkCommand, CodeGenerator, test_code_generator_can_be_made_deterministic(), test_code_generator_uses_seven_base62_characters(), test_code_generator_validates_configuration(), build_create(), build_link(), FakeCache (+19 more)

### Community 31 - ".__init__"
Cohesion: 0.08
Nodes (9): BadRequestError, ConflictError, GatewayTimeoutError, NotFoundError, PayloadTooLargeError, ServiceUnavailableError, AuthorizationError, CsrfError (+1 more)

### Community 32 - "test_url_policy.py"
Cohesion: 0.13
Nodes (16): SystemHostResolver, HostResolutionError, is_blocked_ip(), build_policy(), FakeResolver, test_is_blocked_ip_allows_only_global_addresses(), test_is_blocked_ip_blocks_non_global_addresses(), test_url_policy_accepts_public_urls() (+8 more)

### Community 33 - "ports.py"
Cohesion: 0.14
Nodes (7): DeleteLink, GetLink, CacheUnavailable, Clock, DailyQuota, LinkCache, LinkRepository

### Community 34 - "repository.py"
Cohesion: 0.22
Nodes (9): _escape_like(), _is_code_conflict(), SqlAlchemyLinkRepository, _to_domain(), PageCursor, DuplicateCodeError, test_real_integrity_error_triggers_code_retry(), run() (+1 more)

### Community 35 - "value_objects.py"
Cohesion: 0.16
Nodes (7): InvalidShortCodeError, InvalidUrlError, ReservedAliasError, HostResolver, _normalize_own_host(), _normalize_host(), _validate_hostname()

### Community 36 - "update_link.py"
Cohesion: 0.21
Nodes (10): UpdateLinkCommand, InvalidExpiresAt, InvalidTitle, LinkNotFound, _normalize_expiry(), UpdateLink, normalize_expires_at(), normalize_title() (+2 more)

### Community 37 - "OriginalUrl"
Cohesion: 0.23
Nodes (13): _as_utc(), OriginalUrl, test_link_state_accounts_for_expiry_and_active_flag(), test_link_with_updates_returns_a_new_entity(), test_original_url_keeps_ipv6_literal_brackets(), test_original_url_normalizes_idn_to_punycode(), test_original_url_normalizes_scheme_host_and_idn(), test_original_url_rejects_invalid_host_shapes() (+5 more)

### Community 38 - "Database"
Cohesion: 0.13
Nodes (4): Database, test_database_ping_and_unit_of_work(), test_unit_of_work_rolls_back_on_error(), run()

### Community 39 - "create_link.py"
Cohesion: 0.28
Nodes (9): CreateLink, AliasReserved, AliasTaken, CodeGenerationFailed, DailyQuotaExceeded, InvalidAlias, LoginRequired, UrlNotAllowed (+1 more)

### Community 41 - "build_services"
Cohesion: 0.20
Nodes (6): AnalyticsServices, build_services(), LinkServices, _own_hosts(), SystemClock, utc_now()

### Community 42 - "cache.py"
Cohesion: 0.28
Nodes (4): record_cache_hit(), record_cache_miss(), record_click_dropped(), record_clicks_flushed()

### Community 43 - "daily_quota.py"
Cohesion: 0.18
Nodes (4): RedisDailyQuota, _seconds_until_next_utc_day(), QuotaResult, AllowedQuota

### Community 44 - "resolve_link.py"
Cohesion: 0.27
Nodes (9): ResolvedLink, _Unset, _as_utc(), _entry_state(), _resolved_from_cache(), _resolved_from_link(), ResolveLink, LinkState (+1 more)

### Community 45 - "Settings"
Cohesion: 0.20
Nodes (6): Settings, create_engine(), create_session_factory(), test_metrics_accepts_valid_token(), test_metrics_rejects_wrong_token(), test_metrics_requires_token()

### Community 46 - "test_links_api.py"
Cohesion: 0.39
Nodes (12): create_app(), api_settings(), cleanup(), direct_link(), seed_links(), seed_user(), test_anonymous_create_and_redirect(), test_create_rate_limit_returns_429() (+4 more)

### Community 47 - "list_links.py"
Cohesion: 0.27
Nodes (7): LinkPage, InvalidCursor, InvalidPagination, ListLinks, _normalize_query(), decode_cursor(), encode_cursor()

### Community 48 - "main.py"
Cohesion: 0.18
Nodes (5): get_settings(), test_health_ready_checks_postgres_and_redis(), production_settings(), test_body_limit_is_enforced_by_the_full_app(), test_docs_and_openapi_are_disabled_in_production()

### Community 49 - "test_link_collision.py"
Cohesion: 0.16
Nodes (4): EmptyResolver, SequenceGenerator, NoopRecordClick, test_200_concurrent_cold_redirects_hit_the_database_once()

### Community 50 - "sqlalchemy"
Cohesion: 0.19
Nodes (4): do_run_migrations(), run_async_migrations(), run_migrations_online(), upgrade()

### Community 53 - "logging.py"
Cohesion: 0.31
Nodes (3): configure_logging(), get_logger(), lifespan()

### Community 55 - "test_links_repository.py"
Cohesion: 0.50
Nodes (4): build_link(), cleanup(), seed_user(), test_repository_returns_none_for_non_owned_management_reads()

### Community 56 - "create_redis"
Cohesion: 0.33
Nodes (4): create_redis(), redis_client(), run(), read_stream()

## Knowledge Gaps
- **18 isolated node(s):** `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching`, `lucide-react 1.60.0`, `minimumReleaseAgeExclude Policy` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 228 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `config.py`, `BucketPolicy`, `test_redirect_click_failure.py`, `Bulkhead`, `pytest`, `http.py`, `ShortCode`, `test_click_pipeline.py`, `router.py`, `repository.py`, `Database`, `build_services`, `cache.py`, `test_links_api.py`, `main.py`, `test_link_collision.py`, `collections_abc`, `logging.py`, `test_links_repository.py`, `create_redis`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Are the 34 inferred relationships involving `ShortCode` (e.g. with `RedisLinkCache` and `SqlAlchemyLinkRepository`) actually correct?**
  _`ShortCode` has 34 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Web App and UI Components` be split into smaller, more focused modules?**
  _Cohesion score 0.12380952380952381 - nodes in this community are weakly interconnected._
- **Why does `build_services()` connect `build_services` to `BucketPolicy`, `test_redirect_click_failure.py`, `Bulkhead`, `pytest`, `http.py`, `ShortCode`, `test_click_pipeline.py`, `pytest`, `test_url_policy.py`, `ports.py`, `repository.py`, `update_link.py`, `Database`, `create_link.py`, `daily_quota.py`, `resolve_link.py`, `Settings`, `test_links_api.py`, `list_links.py`, `main.py`, `CacheClient`, `create_redis`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Are the 29 inferred relationships involving `Link` (e.g. with `_entry_from_link()` and `RedisLinkCache`) actually correct?**
  _`Link` has 29 INFERRED edges - model-reasoned connections that need verification._
- **Should `config.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1452991452991453 - nodes in this community are weakly interconnected._