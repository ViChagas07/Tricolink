# Graph Report - Tricolink  (2026-10-21)

## Corpus Check
- 151 files · ~41,219 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 16 file(s) not represented in the graph (top: (none) 13, .ini 1, .mako 1)

## Summary
- 1540 nodes · 4669 edges · 79 communities (64 shown, 15 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 754 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3ce38232`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tricolink URL Shortener Product
- Token Bucket Rate Limiting
- Web App and UI Components
- config.py
- Agent Workflow and Graphify
- Compose and P01 Infra
- identity/adapters/repository.py
- test_real_ip.py
- MemoryTokenBucket
- logging.py
- BodyLimitMiddleware
- httpx
- pnpm Release Policy
- PostCSS Tooling
- API Package
- collections_abc
- pytest
- observability/metrics.py
- User
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
- pytest
- ports.py
- repository.py
- value_objects.py
- register.py
- identity/application/ports.py
- identity/presentation/router.py
- create_link.py
- RedisAuthThrottle
- build_services
- flusher.py
- daily_quota.py
- resolve_link.py
- Settings
- create_app
- list_links.py
- Register
- test_real_integrity_error_triggers_code_retry
- sqlalchemy
- test_identity_domain.py
- adapters/google.py
- google_callback
- CacheClient
- test_link_cache.py
- asyncio
- error_handlers.py
- ids.py
- test_identity_adapters.py
- BucketPolicy
- build_app
- test_rate_limit_dependency_sets_headers_and_429
- identity/domain/entities.py
- AppError
- send
- uuid
- AuthSession
- Link
- test_redirect_click_failure.py
- request_context.py
- test_body_limit.py
- RateLimiter
- HostResolutionError
- security.py
- .__call__
- starlette_types
- Argon2PasswordHasher

## God Nodes (most connected - your core abstractions)
1. `Settings` - 112 edges
2. `ShortCode` - 84 edges
3. `Link` - 74 edges
4. `build_services()` - 50 edges
5. `User` - 45 edges
6. `AppError` - 43 edges
7. `get_services()` - 35 edges
8. `OriginalUrl` - 34 edges
9. `create_app()` - 33 edges
10. `UserRepository` - 31 edges

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

## Communities (79 total, 15 thin omitted)

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
Cohesion: 0.11
Nodes (20): _boolean(), _env(), get_migration_database_url(), get_settings(), _integer(), _number(), SettingsError, _text() (+12 more)

### Community 4 - "Agent Workflow and Graphify"
Cohesion: 0.18
Nodes (8): graphify Slash Command, Mandatory Session Reading Order, CONTEXT.md Single Source of Truth, Graphify Context Engineering, Graphify Installation Commands, Per-Phase Graphify Routine, graphify query/path/explain Workflow, Tricolink README Stub (P11)

### Community 5 - "Compose and P01 Infra"
Cohesion: 0.16
Nodes (20): pnpm allowBuilds Allowlist, API Compose Service, app Network, data Network, postgres_data Volume, PostgreSQL 16 Compose Service, Redis 7 Compose Service, Web Compose Service (+12 more)

### Community 6 - "identity/adapters/repository.py"
Cohesion: 0.07
Nodes (20): do_run_migrations(), run_async_migrations(), run_migrations_online(), Base, ClickEvent, Link, RefreshToken, User (+12 more)

### Community 7 - "test_real_ip.py"
Cohesion: 0.13
Nodes (9): _forwarded_for(), RealIPMiddleware, resolve_real_ip(), _NeverRedis, test_middleware_sets_request_client_to_real_ip(), test_resolve_real_ip_counts_from_the_right(), test_resolve_real_ip_falls_back_when_header_is_invalid_or_short(), test_resolve_real_ip_without_trusted_proxies_ignores_header() (+1 more)

### Community 8 - "MemoryTokenBucket"
Cohesion: 0.19
Nodes (10): _BucketState, MemoryTokenBucket, _reset_seconds(), DownRedis, FakeClock, test_memory_bucket_consumes_and_exhausts(), test_memory_bucket_never_exceeds_capacity(), test_memory_bucket_refills() (+2 more)

### Community 9 - "logging.py"
Cohesion: 0.21
Nodes (3): MetricsMiddleware, _route_path(), record_request()

### Community 10 - "BodyLimitMiddleware"
Cohesion: 0.26
Nodes (3): BodyLimitMiddleware, _header_values(), _send_json()

### Community 11 - "httpx"
Cohesion: 0.35
Nodes (7): build_inner(), test_hsts_only_in_production(), test_request_id_accepts_only_safe_values(), test_request_id_is_generated_and_returned(), test_security_headers_are_added(), test_timeout_allows_fast_requests(), test_timeout_returns_504()

### Community 18 - "collections_abc"
Cohesion: 0.11
Nodes (7): create_engine(), create_session_factory(), unit_of_work(), build_bulkheads(), Bulkhead, BulkheadRegistry, BulkheadFullError

### Community 19 - "pytest"
Cohesion: 0.08
Nodes (12): record_circuit_state(), CircuitBreaker, CircuitState, CircuitOpenError, test_bulkhead_limits_concurrency(), test_bulkhead_times_out_when_full(), test_bulkheads_are_named_and_independent(), fail() (+4 more)

### Community 20 - "observability/metrics.py"
Cohesion: 0.20
Nodes (4): FakeRedis, _sample(), test_cache_get_records_hit_and_miss(), test_cache_set_validates_ttl_and_delete()

### Community 21 - "User"
Cohesion: 0.13
Nodes (10): AuthenticateAccess, UpdateMeCommand, InvalidProfile, SessionExpired, GetMe, UserRepository, _normalize_display_name(), _normalize_locale() (+2 more)

### Community 22 - "http.py"
Cohesion: 0.20
Nodes (9): Services, _authorized(), _check_database(), _check_redis(), health_live(), health_ready(), HealthResponse, metrics() (+1 more)

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
Cohesion: 0.13
Nodes (11): jittered_ttl(), _CacheRead, _entry_from_link(), RedisLinkCache, CacheEntry, CacheUnavailable, ShortCode, test_jittered_ttl_edge_cases() (+3 more)

### Community 28 - "test_click_pipeline.py"
Cohesion: 0.05
Nodes (26): Database, ClickFlusher, guarded(), _parse_event(), RedisClickPublisher, operation(), _browser(), ClickEvent (+18 more)

### Community 29 - "router.py"
Cohesion: 0.06
Nodes (56): CurrentUser, get_cache(), get_current_user(), get_current_user_optional(), get_rate_limiter(), get_services(), get_session(), settings_dependency() (+48 more)

### Community 30 - "pytest"
Cohesion: 0.10
Nodes (27): CreateLinkCommand, CodeGenerator, test_code_generator_can_be_made_deterministic(), test_code_generator_uses_seven_base62_characters(), test_code_generator_validates_configuration(), build_create(), build_link(), FakeCache (+19 more)

### Community 32 - "pytest"
Cohesion: 0.08
Nodes (39): LoginCommand, RegisterCommand, DuplicateUserError, is_blocked_ip(), build_issuer(), build_login(), build_register(), FakeAccessTokens (+31 more)

### Community 33 - "ports.py"
Cohesion: 0.13
Nodes (10): DeleteLink, UpdateLinkCommand, LinkNotFound, GetLink, Clock, DailyQuota, LinkCache, LinkRepository (+2 more)

### Community 34 - "repository.py"
Cohesion: 0.18
Nodes (14): set_rls_context(), _escape_like(), _is_code_conflict(), SqlAlchemyLinkRepository, _to_domain(), PageCursor, DuplicateCodeError, run() (+6 more)

### Community 35 - "value_objects.py"
Cohesion: 0.12
Nodes (20): InvalidShortCodeError, InvalidUrlError, ReservedAliasError, HostResolver, _normalize_own_host(), UrlPolicy, _normalize_host(), OriginalUrl (+12 more)

### Community 36 - "register.py"
Cohesion: 0.26
Nodes (6): Email, InvalidEmailError, InvalidGoogleIdentityError, WeakPasswordError, _display_name(), PasswordPolicy

### Community 37 - "identity/application/ports.py"
Cohesion: 0.20
Nodes (8): Logout, AccessTokenIssuer, Clock, RotationStatus, SessionRepository, RefreshSession, generate_refresh_token(), hash_refresh_token()

### Community 38 - "identity/presentation/router.py"
Cohesion: 0.22
Nodes (16): GoogleNotConfigured, _client_ip(), login(), logout(), me(), refresh(), register(), update_me() (+8 more)

### Community 39 - "create_link.py"
Cohesion: 0.19
Nodes (13): CreateLink, AliasReserved, AliasTaken, CodeGenerationFailed, DailyQuotaExceeded, InvalidAlias, InvalidExpiresAt, InvalidTitle (+5 more)

### Community 40 - "RedisAuthThrottle"
Cohesion: 0.15
Nodes (6): _digest(), RedisAuthThrottle, guarded(), operation(), _retry_after(), ThrottleResult

### Community 41 - "build_services"
Cohesion: 0.17
Nodes (7): AnalyticsServices, build_services(), IdentityServices, LinkServices, _own_hosts(), SystemClock, utc_now()

### Community 42 - "flusher.py"
Cohesion: 0.19
Nodes (4): record_click_dropped(), record_clicks_flushed(), record_rate_limit_fallback(), record_rate_limited()

### Community 43 - "daily_quota.py"
Cohesion: 0.22
Nodes (3): RedisDailyQuota, _seconds_until_next_utc_day(), QuotaResult

### Community 44 - "resolve_link.py"
Cohesion: 0.21
Nodes (10): ResolvedLink, _Unset, _as_utc(), _entry_state(), _resolved_from_cache(), _resolved_from_link(), ResolveLink, _as_utc() (+2 more)

### Community 45 - "Settings"
Cohesion: 0.31
Nodes (5): Settings, generate_csrf_token(), clear_session_cookies(), set_csrf_cookie(), set_session_cookies()

### Community 46 - "create_app"
Cohesion: 0.07
Nodes (42): configure_logging(), get_logger(), create_app(), lifespan(), test_health_ready_checks_postgres_and_redis(), admin_settings(), cleanup(), run() (+34 more)

### Community 47 - "list_links.py"
Cohesion: 0.23
Nodes (8): LinkPage, InvalidCursor, InvalidPagination, ListLinks, _normalize_query(), decode_cursor(), encode_cursor(), test_cursor_roundtrip_and_rejection()

### Community 48 - "Register"
Cohesion: 0.18
Nodes (8): AuthLocked, InvalidCredentials, InvalidEmail, WeakPassword, Login, AuthThrottle, PasswordHasher, Register

### Community 49 - "test_real_integrity_error_triggers_code_retry"
Cohesion: 0.23
Nodes (5): AllowedQuota, EmptyResolver, NoopCache, SequenceGenerator, test_real_integrity_error_triggers_code_retry()

### Community 51 - "test_identity_domain.py"
Cohesion: 0.17
Nodes (16): _number(), _string(), validate_google_claims(), google_claims(), test_email_is_nfkc_normalized_and_lowercased(), test_email_rejects_invalid_values(), test_email_rejects_non_string_and_too_long(), test_google_claims_accept_audience_list_and_string_verified() (+8 more)

### Community 52 - "adapters/google.py"
Cohesion: 0.18
Nodes (5): PyJwtAccessTokens, AccessClaims, IssuedAccessToken, test_access_jwt_contains_minimal_claims_and_validates(), test_expired_access_token_is_rejected()

### Community 53 - "google_callback"
Cohesion: 0.22
Nodes (6): GoogleOIDCClient, csrf_token(), google_callback(), _google_error_redirect(), google_login(), frontend_url()

### Community 54 - "CacheClient"
Cohesion: 0.22
Nodes (3): CacheClient, record_cache_hit(), record_cache_miss()

### Community 55 - "test_link_cache.py"
Cohesion: 0.37
Nodes (9): cache_settings(), cleanup(), make_link(), test_cold_stampede_uses_one_database_query(), loader(), test_invalidation_forces_the_next_read_to_use_the_loader(), test_negative_cache_limits_missing_code_queries(), test_stale_value_is_served_while_one_refresh_runs() (+1 more)

### Community 56 - "asyncio"
Cohesion: 0.21
Nodes (6): close_redis(), create_redis(), ping_redis(), redis_client(), run(), read_stream()

### Community 57 - "error_handlers.py"
Cohesion: 0.19
Nodes (7): install_error_handlers(), handle_app_error(), handle_http_exception(), handle_unexpected_error(), handle_validation_error(), _json_error(), error_payload()

### Community 59 - "test_identity_adapters.py"
Cohesion: 0.18
Nodes (11): InvalidNextPath, safe_next_path(), build_session(), fast_hasher(), test_argon2_hasher_roundtrip_and_dummy(), test_clear_cookies_deletes_all_session_cookies(), test_cookie_prefix_disabled_when_domain_is_set(), test_cookies_are_httponly_except_csrf_and_samesite_lax() (+3 more)

### Community 60 - "BucketPolicy"
Cohesion: 0.23
Nodes (4): BucketPolicy, build_policies(), _reset_seconds(), TokenBucketBackend

### Community 61 - "build_app"
Cohesion: 0.22
Nodes (9): NotFoundError, build_app(), auth(), missing(), test_app_error_uses_standard_envelope(), test_security_error_uses_standard_envelope(), test_unhandled_error_does_not_leak_stack_trace(), test_unknown_route_uses_standard_envelope() (+1 more)

### Community 62 - "test_rate_limit_dependency_sets_headers_and_429"
Cohesion: 0.18
Nodes (4): DownRedis, test_global_bucket_is_shared_across_clients(), DownRedis, test_rate_limit_dependency_sets_headers_and_429()

### Community 63 - "identity/domain/entities.py"
Cohesion: 0.26
Nodes (5): _as_utc(), RefreshTokenRecord, TokenFamily, test_refresh_record_handles_naive_datetimes(), test_token_family_and_refresh_record_lifecycle()

### Community 64 - "AppError"
Cohesion: 0.24
Nodes (6): AppError, BadRequestError, ConflictError, GatewayTimeoutError, PayloadTooLargeError, ServiceUnavailableError

### Community 65 - "send"
Cohesion: 0.18
Nodes (5): capture_status(), send_with_request_id(), SecurityHeadersMiddleware, send_with_headers(), send()

### Community 66 - "uuid"
Cohesion: 0.36
Nodes (4): RedisTokenBucket, test_lua_bucket_consumes_exhausts_and_refills(), test_lua_bucket_is_atomic_under_concurrency(), test_lua_bucket_keeps_keys_independent()

### Community 67 - "AuthSession"
Cohesion: 0.42
Nodes (5): AuthSession, InvalidGoogleLogin, LoginWithGoogle, SessionIssuer, GoogleIdentity

### Community 68 - "Link"
Cohesion: 0.27
Nodes (4): Link, CountingRepository, NoopRecordClick, test_200_concurrent_cold_redirects_hit_the_database_once()

### Community 69 - "test_redirect_click_failure.py"
Cohesion: 0.29
Nodes (5): BlockingPublisher, click_settings(), DownRedis, test_redirect_continues_and_metric_counts_dropped_click(), test_redirect_does_not_wait_for_click_publisher()

### Community 71 - "test_body_limit.py"
Cohesion: 0.33
Nodes (5): build_app(), test_accepts_body_at_limit(), test_invalid_content_length_is_rejected(), test_rejects_chunked_body_above_limit(), test_rejects_content_length_above_limit_before_reading()

### Community 74 - "security.py"
Cohesion: 0.42
Nodes (5): allowed_origins(), csrf_protect(), origin_guard(), validate_origin(), CsrfError

### Community 75 - ".__call__"
Cohesion: 0.29
Nodes (4): replay_body(), run(), tracked_send(), receive()

## Knowledge Gaps
- **18 isolated node(s):** `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching`, `lucide-react 1.60.0`, `minimumReleaseAgeExclude Policy` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 282 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_services()` connect `build_services` to `identity/adapters/repository.py`, `MemoryTokenBucket`, `collections_abc`, `pytest`, `User`, `http.py`, `ShortCode`, `test_click_pipeline.py`, `pytest`, `ports.py`, `repository.py`, `value_objects.py`, `register.py`, `identity/application/ports.py`, `create_link.py`, `RedisAuthThrottle`, `daily_quota.py`, `resolve_link.py`, `Settings`, `create_app`, `list_links.py`, `Register`, `adapters/google.py`, `google_callback`, `CacheClient`, `asyncio`, `BucketPolicy`, `uuid`, `AuthSession`, `RateLimiter`, `HostResolutionError`, `Argon2PasswordHasher`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Are the 72 inferred relationships involving `Settings` (e.g. with `settings_dependency()` and `configure_logging()`) actually correct?**
  _`Settings` has 72 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Web App and UI Components` be split into smaller, more focused modules?**
  _Cohesion score 0.12380952380952381 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `config.py`, `identity/adapters/repository.py`, `collections_abc`, `pytest`, `http.py`, `ShortCode`, `test_click_pipeline.py`, `router.py`, `repository.py`, `identity/presentation/router.py`, `RedisAuthThrottle`, `build_services`, `flusher.py`, `create_app`, `test_real_integrity_error_triggers_code_retry`, `adapters/google.py`, `google_callback`, `test_link_cache.py`, `asyncio`, `test_identity_adapters.py`, `BucketPolicy`, `Link`, `test_redirect_click_failure.py`, `security.py`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Are the 35 inferred relationships involving `ShortCode` (e.g. with `RedisLinkCache` and `SqlAlchemyLinkRepository`) actually correct?**
  _`ShortCode` has 35 INFERRED edges - model-reasoned connections that need verification._
- **Should `config.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11092436974789915 - nodes in this community are weakly interconnected._