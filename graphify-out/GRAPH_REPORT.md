# Graph Report - Tricolink  (2026-10-22)

## Corpus Check
- 241 files · ~107,399 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: (none) 10, .ini 1, .mako 1)

## Summary
- 1921 nodes · 5747 edges · 95 communities (82 shown, 13 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 769 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ac13cd6a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tricolink URL Shortener Product
- Token Bucket Rate Limiting
- page.tsx
- config.py
- Agent Workflow and Graphify
- Compose and P01 Infra
- db/models.py
- test_real_ip.py
- MemoryTokenBucket
- logging.py
- BodyLimitMiddleware
- httpx
- pnpm Release Policy
- PostCSS Tooling
- User
- API Package
- flusher.py
- pytest
- observability/metrics.py
- demo-dashboard.tsx
- http.py
- SECURITY.md Security Requirements
- UI_SPEC.md Tricolink Interface
- Code Standards
- REST API /api/v1 Contract
- ShortCode
- ClickEvent
- links/presentation/router.py
- pytest
- ref_next_intl
- pytest
- ports.py
- repository.py
- test_click_pipeline.py
- register.py
- build_services
- identity/presentation/router.py
- AppError
- RedisAuthThrottle
- build_services
- dataclasses
- shorten-form.tsx
- resolve_link.py
- Settings
- create_app
- list_links.py
- Register
- links-view.tsx
- navbar.tsx
- api.ts
- adapters/google.py
- google_callback
- links/presentation/dependencies.py
- identity/application/ports.py
- asyncio
- error_handlers.py
- ids.py
- get_services
- BucketPolicy
- login-form.tsx
- test_rate_limit_dependency_sets_headers_and_429
- identity/domain/entities.py
- main.py
- account-form.tsx
- uuid
- test_link_cache.py
- ClickFlusher
- test_redirect_click_failure.py
- request_context.py
- test_body_limit.py
- RateLimiter
- HostResolutionError
- security.py
- .__call__
- starlette_types
- Argon2PasswordHasher
- opengraph-image.tsx
- page.tsx
- identity/presentation/router.py
- value_objects.py
- Database
- Bulkhead
- sqlalchemy
- asyncio
- i18n-check.mjs
- RedisDailyQuota
- proxy.ts
- test_links_repository.py
- SequenceGenerator
- unicodedata
- test_bulkhead.py

## God Nodes (most connected - your core abstractions)
1. `Settings` - 113 edges
2. `ShortCode` - 84 edges
3. `Link` - 74 edges
4. `build_services()` - 51 edges
5. `User` - 45 edges
6. `AppError` - 43 edges
7. `get_services()` - 36 edges
8. `cn()` - 36 edges
9. `OriginalUrl` - 34 edges
10. `create_app()` - 33 edges

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

## Communities (95 total, 13 thin omitted)

### Community 0 - "Tricolink URL Shortener Product"
Cohesion: 0.25
Nodes (8): click_events Table, Redis Stream Click Buffer, Non-Goals, Tricolink URL Shortener Product, Redirect and Cache Hot Path, URL Anti-Abuse Policy, SSRF Prevention, Design Tokens

### Community 1 - "Token Bucket Rate Limiting"
Cohesion: 0.24
Nodes (9): Daily Link Quotas, Negative Cache for Unknown Codes, Single-Flight Lock, Stale-While-Revalidate Caching, Brute Force Protection, Bulkhead Semaphores, Circuit Breaker, Rate Limit Buckets (+1 more)

### Community 2 - "page.tsx"
Cohesion: 0.12
Nodes (21): LocaleNotFound(), ControlVisual(), FeatureBlocks(), ShortLinkVisual(), StatsVisual(), WEEKDAY_BARS, FinalCta(), CopyLinkButtonProps (+13 more)

### Community 3 - "config.py"
Cohesion: 0.22
Nodes (8): _boolean(), _env(), get_migration_database_url(), _integer(), _number(), SettingsError, _text(), _text_or_empty()

### Community 4 - "Agent Workflow and Graphify"
Cohesion: 0.18
Nodes (8): graphify Slash Command, Mandatory Session Reading Order, CONTEXT.md Single Source of Truth, Graphify Context Engineering, Graphify Installation Commands, Per-Phase Graphify Routine, graphify query/path/explain Workflow, Tricolink README Stub (P11)

### Community 5 - "Compose and P01 Infra"
Cohesion: 0.16
Nodes (20): pnpm allowBuilds Allowlist, API Compose Service, app Network, data Network, postgres_data Volume, PostgreSQL 16 Compose Service, Redis 7 Compose Service, Web Compose Service (+12 more)

### Community 6 - "db/models.py"
Cohesion: 0.14
Nodes (11): Base, ClickEvent, Link, RefreshToken, User, admin_settings(), make_link(), test_rls_blocks_cross_user_reads_even_without_app_filter() (+3 more)

### Community 7 - "test_real_ip.py"
Cohesion: 0.14
Nodes (8): _forwarded_for(), RealIPMiddleware, resolve_real_ip(), _NeverRedis, test_middleware_sets_request_client_to_real_ip(), test_resolve_real_ip_counts_from_the_right(), test_resolve_real_ip_falls_back_when_header_is_invalid_or_short(), test_resolve_real_ip_without_trusted_proxies_ignores_header()

### Community 8 - "MemoryTokenBucket"
Cohesion: 0.20
Nodes (9): _BucketState, MemoryTokenBucket, DownRedis, FakeClock, test_memory_bucket_consumes_and_exhausts(), test_memory_bucket_never_exceeds_capacity(), test_memory_bucket_refills(), test_rate_limiter_falls_back_to_memory_when_redis_is_down() (+1 more)

### Community 9 - "logging.py"
Cohesion: 0.14
Nodes (6): configure_logging(), get_logger(), MetricsMiddleware, _route_path(), record_request(), lifespan()

### Community 10 - "BodyLimitMiddleware"
Cohesion: 0.26
Nodes (3): BodyLimitMiddleware, _header_values(), _send_json()

### Community 11 - "httpx"
Cohesion: 0.25
Nodes (8): SecurityHeadersMiddleware, build_inner(), test_hsts_only_in_production(), test_request_id_accepts_only_safe_values(), test_request_id_is_generated_and_returned(), test_security_headers_are_added(), test_timeout_allows_fast_requests(), test_timeout_returns_504()

### Community 15 - "User"
Cohesion: 0.13
Nodes (8): SqlAlchemyUserRepository, _to_user(), AuthenticateAccess, UserRepository, Email, User, DuplicateUserError, make_user()

### Community 18 - "flusher.py"
Cohesion: 0.24
Nodes (3): create_engine(), create_session_factory(), unit_of_work()

### Community 19 - "pytest"
Cohesion: 0.09
Nodes (8): CircuitBreaker, CircuitState, CircuitOpenError, fail(), test_breaker_half_open_failure_reopens(), test_breaker_half_open_success_closes(), test_breaker_opens_after_threshold_and_rejects_calls(), test_half_open_allows_only_configured_probes()

### Community 20 - "observability/metrics.py"
Cohesion: 0.16
Nodes (5): CacheClient, FakeRedis, _sample(), test_cache_get_records_hit_and_miss(), test_cache_set_validates_ttl_and_delete()

### Community 21 - "demo-dashboard.tsx"
Cohesion: 0.11
Nodes (20): BreakdownColumns, BreakdownRow, BreakdownTable(), BreakdownTableProps, columns, ClicksChartProps, ClicksPoint, ChartPlaceholder() (+12 more)

### Community 22 - "http.py"
Cohesion: 0.19
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
Cohesion: 0.12
Nodes (13): jittered_ttl(), _CacheRead, _entry_from_link(), RedisLinkCache, CacheEntry, CacheUnavailable, Link, ShortCode (+5 more)

### Community 28 - "ClickEvent"
Cohesion: 0.16
Nodes (13): _parse_event(), _browser(), ClickEvent, extract_referrer_host(), normalize_country(), parse_user_agent(), UserAgentInfo, ClickPublisher (+5 more)

### Community 29 - "links/presentation/router.py"
Cohesion: 0.13
Nodes (15): CurrentUser, create_link(), delete_link(), get_link(), _link_response(), links_overview(), list_links(), redirect_link() (+7 more)

### Community 30 - "pytest"
Cohesion: 0.10
Nodes (28): CreateLinkCommand, CodeGenerator, test_code_generator_can_be_made_deterministic(), test_code_generator_uses_seven_base62_characters(), test_code_generator_validates_configuration(), build_create(), build_link(), FakeCache (+20 more)

### Community 31 - "ref_next_intl"
Cohesion: 0.11
Nodes (29): AccountPage(), AccountPageProps, generateMetadata(), dynamic, generateMetadata(), inter, jakarta, LocaleLayout() (+21 more)

### Community 32 - "pytest"
Cohesion: 0.08
Nodes (39): LoginCommand, RegisterCommand, Logout, is_blocked_ip(), build_issuer(), build_login(), build_register(), FakeAccessTokens (+31 more)

### Community 33 - "ports.py"
Cohesion: 0.09
Nodes (14): DeleteLink, UpdateLinkCommand, LinkNotFound, GetLink, GetLinksOverview, LinksOverview, Clock, DailyQuota (+6 more)

### Community 34 - "repository.py"
Cohesion: 0.18
Nodes (10): set_rls_context(), _escape_like(), _is_code_conflict(), SqlAlchemyLinkRepository, _to_domain(), PageCursor, EmptyResolver, test_real_integrity_error_triggers_code_retry() (+2 more)

### Community 35 - "test_click_pipeline.py"
Cohesion: 0.36
Nodes (8): RedisClickPublisher, admin_settings(), DownRedis, make_link(), pipeline_settings(), test_flusher_persists_batch_and_increments_click_count(), test_flusher_retries_pending_entries(), test_publisher_drops_event_and_increments_metric_when_redis_is_down()

### Community 36 - "register.py"
Cohesion: 0.12
Nodes (21): InvalidEmailError, InvalidGoogleIdentityError, WeakPasswordError, _display_name(), _number(), _string(), validate_google_claims(), PasswordPolicy (+13 more)

### Community 37 - "build_services"
Cohesion: 0.15
Nodes (8): AccessTokenIssuer, Clock, RotationStatus, SessionRepository, RefreshSession, generate_csrf_token(), generate_refresh_token(), hash_refresh_token()

### Community 38 - "identity/presentation/router.py"
Cohesion: 0.23
Nodes (16): _client_ip(), csrf_token(), login(), logout(), me(), refresh(), register(), update_me() (+8 more)

### Community 39 - "AppError"
Cohesion: 0.07
Nodes (20): GoogleNotConfigured, CreateLink, AliasReserved, AliasTaken, CodeGenerationFailed, DailyQuotaExceeded, InvalidAlias, InvalidExpiresAt (+12 more)

### Community 40 - "RedisAuthThrottle"
Cohesion: 0.16
Nodes (5): _digest(), RedisAuthThrottle, guarded(), operation(), ThrottleResult

### Community 41 - "build_services"
Cohesion: 0.18
Nodes (7): AnalyticsServices, build_services(), IdentityServices, LinkServices, _own_hosts(), SystemClock, utc_now()

### Community 42 - "dataclasses"
Cohesion: 0.16
Nodes (10): record_cache_hit(), record_cache_miss(), record_circuit_state(), record_click_dropped(), record_clicks_flushed(), record_rate_limit_fallback(), record_rate_limited(), _seconds_until_next_utc_day() (+2 more)

### Community 43 - "shorten-form.tsx"
Cohesion: 0.14
Nodes (14): ExternalLink(), ExternalLinkProps, HeroSection(), CopyState, CreateLinkResponse, ERROR_KEYS, FormError, ShortenForm() (+6 more)

### Community 44 - "resolve_link.py"
Cohesion: 0.12
Nodes (13): ResolvedLink, _Unset, _as_utc(), _entry_state(), _resolved_from_cache(), _resolved_from_link(), ResolveLink, _as_utc() (+5 more)

### Community 45 - "Settings"
Cohesion: 0.13
Nodes (18): get_settings(), Settings, clear_session_cookies(), set_csrf_cookie(), set_session_cookies(), test_database_ping_and_unit_of_work(), test_unit_of_work_rolls_back_on_error(), test_health_ready_checks_postgres_and_redis() (+10 more)

### Community 46 - "create_app"
Cohesion: 0.23
Nodes (20): create_app(), admin_settings(), cleanup(), run(), FakeGoogleOIDC, google_claims(), identity_settings(), login() (+12 more)

### Community 47 - "list_links.py"
Cohesion: 0.31
Nodes (8): LinkPage, InvalidCursor, InvalidPagination, ListLinks, _normalize_query(), decode_cursor(), encode_cursor(), test_cursor_roundtrip_and_rejection()

### Community 48 - "Register"
Cohesion: 0.19
Nodes (8): AuthLocked, InvalidCredentials, InvalidEmail, WeakPassword, Login, AuthThrottle, PasswordHasher, Register

### Community 49 - "links-view.tsx"
Cohesion: 0.11
Nodes (26): LinksLoading(), CopyLinkButton(), LinksSkeleton(), LinksSkeletonProps, LinkCard(), LinksView(), confirmDelete(), handleSave() (+18 more)

### Community 50 - "navbar.tsx"
Cohesion: 0.23
Nodes (16): BrandLogo(), Footer(), LanguageSwitcher(), handleListKeyDown(), moveActive(), AccountMenu(), initialsFor(), Navbar() (+8 more)

### Community 51 - "api.ts"
Cohesion: 0.06
Nodes (36): navigation, user, items, authState, renderForm(), authState, navigation, renderNavbar() (+28 more)

### Community 52 - "adapters/google.py"
Cohesion: 0.14
Nodes (11): PyJwtAccessTokens, AccessClaims, IssuedAccessToken, build_session(), fast_hasher(), test_access_jwt_contains_minimal_claims_and_validates(), test_argon2_hasher_roundtrip_and_dummy(), test_cookie_prefix_disabled_when_domain_is_set() (+3 more)

### Community 53 - "google_callback"
Cohesion: 0.13
Nodes (8): GoogleOIDCClient, InvalidNextPath, google_callback(), _google_error_redirect(), google_login(), safe_next_path(), test_safe_next_accepts_internal_paths(), test_safe_next_rejects_external_or_control_paths()

### Community 54 - "links/presentation/dependencies.py"
Cohesion: 0.26
Nodes (8): client_ip(), _get_limiter(), rate_limit(), dependency(), _retry_after_seconds(), _rate_limit_error(), RateLimitExceeded, test_spoofed_xff_cannot_bypass_rate_limit()

### Community 55 - "identity/application/ports.py"
Cohesion: 0.36
Nodes (3): _revoke_family(), SqlAlchemySessionRepository, RotationResult

### Community 56 - "asyncio"
Cohesion: 0.18
Nodes (6): close_redis(), create_redis(), ping_redis(), redis_client(), run(), read_stream()

### Community 57 - "error_handlers.py"
Cohesion: 0.10
Nodes (17): install_error_handlers(), handle_app_error(), handle_http_exception(), handle_unexpected_error(), handle_validation_error(), _json_error(), error_payload(), NotFoundError (+9 more)

### Community 59 - "get_services"
Cohesion: 0.18
Nodes (18): get_current_user(), apply_rate_limit_headers(), user_rate_limit(), dependency(), create_link_rate_limit(), get_click_publisher(), get_create_link(), get_delete_link() (+10 more)

### Community 60 - "BucketPolicy"
Cohesion: 0.23
Nodes (5): _reset_seconds(), BucketPolicy, build_policies(), _reset_seconds(), TokenBucketBackend

### Community 61 - "login-form.tsx"
Cohesion: 0.15
Nodes (21): first(), generateMetadata(), LoginPage(), LoginPageProps, FieldError, FieldErrors, FormError, LoginForm() (+13 more)

### Community 63 - "identity/domain/entities.py"
Cohesion: 0.17
Nodes (10): AuthSession, InvalidGoogleLogin, LoginWithGoogle, SessionIssuer, _as_utc(), RefreshTokenRecord, TokenFamily, GoogleIdentity (+2 more)

### Community 64 - "main.py"
Cohesion: 0.14
Nodes (6): test_metrics_accepts_valid_token(), test_metrics_rejects_wrong_token(), test_metrics_requires_token(), production_settings(), test_body_limit_is_enforced_by_the_full_app(), test_docs_and_openapi_are_disabled_in_production()

### Community 65 - "account-form.tsx"
Cohesion: 0.18
Nodes (18): AccountForm(), handleError(), handleLocaleChange(), handleProfileSubmit(), handleThemeChange(), AccountFormProps, Notice, handleSubmit() (+10 more)

### Community 66 - "uuid"
Cohesion: 0.36
Nodes (4): RedisTokenBucket, test_lua_bucket_consumes_exhausts_and_refills(), test_lua_bucket_is_atomic_under_concurrency(), test_lua_bucket_keeps_keys_independent()

### Community 67 - "test_link_cache.py"
Cohesion: 0.37
Nodes (9): cache_settings(), cleanup(), make_link(), test_cold_stampede_uses_one_database_query(), loader(), test_invalidation_forces_the_next_read_to_use_the_loader(), test_negative_cache_limits_missing_code_queries(), test_stale_value_is_served_while_one_refresh_runs() (+1 more)

### Community 68 - "ClickFlusher"
Cohesion: 0.22
Nodes (3): ClickFlusher, guarded(), operation()

### Community 69 - "test_redirect_click_failure.py"
Cohesion: 0.29
Nodes (5): BlockingPublisher, click_settings(), DownRedis, test_redirect_continues_and_metric_counts_dropped_click(), test_redirect_does_not_wait_for_click_publisher()

### Community 70 - "request_context.py"
Cohesion: 0.20
Nodes (3): _incoming_request_id(), RequestIDMiddleware, send_with_request_id()

### Community 71 - "test_body_limit.py"
Cohesion: 0.33
Nodes (5): build_app(), test_accepts_body_at_limit(), test_invalid_content_length_is_rejected(), test_rejects_chunked_body_above_limit(), test_rejects_content_length_above_limit_before_reading()

### Community 72 - "RateLimiter"
Cohesion: 0.12
Nodes (6): GlobalRateLimitMiddleware, send_with_headers(), _headers(), RateLimiter, DownRedis, test_global_bucket_is_shared_across_clients()

### Community 74 - "security.py"
Cohesion: 0.42
Nodes (6): allowed_origins(), csrf_protect(), frontend_url(), origin_guard(), validate_origin(), CsrfError

### Community 75 - ".__call__"
Cohesion: 0.14
Nodes (7): replay_body(), capture_status(), send_with_headers(), run(), tracked_send(), receive(), send()

### Community 79 - "opengraph-image.tsx"
Cohesion: 0.40
Nodes (3): alt, contentType, size

### Community 80 - "page.tsx"
Cohesion: 0.08
Nodes (29): dynamic, GET(), generateMetadata(), HomePage(), HomePageProps, sitemap(), Faq(), FaqEntry (+21 more)

### Community 81 - "identity/presentation/router.py"
Cohesion: 0.20
Nodes (15): get_cache(), get_current_user_optional(), get_rate_limiter(), get_services(), get_session(), settings_dependency(), get_authenticate_access(), get_get_me() (+7 more)

### Community 82 - "value_objects.py"
Cohesion: 0.12
Nodes (20): validate_url(), InvalidUrlError, ReservedAliasError, HostResolver, _normalize_own_host(), UrlPolicy, _normalize_host(), OriginalUrl (+12 more)

### Community 83 - "Database"
Cohesion: 0.14
Nodes (3): Database, run(), run()

### Community 84 - "Bulkhead"
Cohesion: 0.23
Nodes (4): build_bulkheads(), Bulkhead, BulkheadRegistry, BulkheadFullError

### Community 85 - "sqlalchemy"
Cohesion: 0.19
Nodes (4): do_run_migrations(), run_async_migrations(), run_migrations_online(), upgrade()

### Community 86 - "asyncio"
Cohesion: 0.34
Nodes (13): api_settings(), cleanup(), direct_link(), seed_click(), seed_links(), seed_user(), test_anonymous_create_and_redirect(), test_create_rate_limit_returns_429() (+5 more)

### Community 87 - "i18n-check.mjs"
Cohesion: 0.13
Nodes (9): appRoot, catalogs, errors, files, flattenKeys(), localeSet, messagesDir, reference (+1 more)

### Community 88 - "RedisDailyQuota"
Cohesion: 0.27
Nodes (3): RedisDailyQuota, QuotaResult, AllowedQuota

### Community 89 - "proxy.ts"
Cohesion: 0.14
Nodes (17): nextConfig, withNextIntl, buildRewrites(), isShortCodePath(), RESERVED_PATTERN, RESERVED_TOP_LEVEL, RewriteRule, RewritesConfig (+9 more)

### Community 91 - "test_links_repository.py"
Cohesion: 0.44
Nodes (5): admin_settings(), build_link(), cleanup(), seed_user(), test_repository_returns_none_for_non_owned_management_reads()

### Community 93 - "unicodedata"
Cohesion: 0.21
Nodes (7): UpdateMeCommand, InvalidProfile, SessionExpired, GetMe, _normalize_display_name(), _normalize_locale(), UpdateMe

### Community 95 - "test_bulkhead.py"
Cohesion: 0.32
Nodes (3): test_bulkhead_limits_concurrency(), test_bulkhead_times_out_when_full(), test_bulkheads_are_named_and_independent()

## Knowledge Gaps
- **18 isolated node(s):** `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching`, `lucide-react 1.60.0`, `minimumReleaseAgeExclude Policy` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 402 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_services()` connect `build_services` to `MemoryTokenBucket`, `User`, `pytest`, `observability/metrics.py`, `http.py`, `ShortCode`, `ClickEvent`, `pytest`, `pytest`, `ports.py`, `repository.py`, `test_click_pipeline.py`, `register.py`, `build_services`, `AppError`, `RedisAuthThrottle`, `resolve_link.py`, `Settings`, `create_app`, `list_links.py`, `Register`, `adapters/google.py`, `google_callback`, `identity/application/ports.py`, `asyncio`, `BucketPolicy`, `identity/domain/entities.py`, `main.py`, `uuid`, `ClickFlusher`, `RateLimiter`, `HostResolutionError`, `Argon2PasswordHasher`, `value_objects.py`, `Database`, `Bulkhead`, `RedisDailyQuota`, `unicodedata`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Are the 73 inferred relationships involving `Settings` (e.g. with `settings_dependency()` and `configure_logging()`) actually correct?**
  _`Settings` has 73 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `page.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.12312312312312312 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `config.py`, `db/models.py`, `logging.py`, `flusher.py`, `pytest`, `http.py`, `ShortCode`, `links/presentation/router.py`, `repository.py`, `test_click_pipeline.py`, `build_services`, `identity/presentation/router.py`, `RedisAuthThrottle`, `build_services`, `dataclasses`, `resolve_link.py`, `create_app`, `adapters/google.py`, `google_callback`, `asyncio`, `get_services`, `BucketPolicy`, `main.py`, `test_link_cache.py`, `ClickFlusher`, `test_redirect_click_failure.py`, `security.py`, `identity/presentation/router.py`, `Database`, `Bulkhead`, `asyncio`, `test_links_repository.py`, `test_bulkhead.py`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Are the 35 inferred relationships involving `ShortCode` (e.g. with `RedisLinkCache` and `SqlAlchemyLinkRepository`) actually correct?**
  _`ShortCode` has 35 INFERRED edges - model-reasoned connections that need verification._
- **Should `db/models.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14492753623188406 - nodes in this community are weakly interconnected._