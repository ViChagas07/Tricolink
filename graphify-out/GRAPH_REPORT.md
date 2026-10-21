# Graph Report - Tricolink  (2026-10-21)

## Corpus Check
- 218 files · ~63,964 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 13 file(s) not represented in the graph (top: (none) 10, .ini 1, .mako 1)

## Summary
- 1774 nodes · 5223 edges · 92 communities (79 shown, 13 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 755 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `efa1d157`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tricolink URL Shortener Product
- Token Bucket Rate Limiting
- page.tsx
- config.py
- Agent Workflow and Graphify
- Compose and P01 Infra
- value_objects.py
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
- .__init__
- pytest
- ports.py
- repository.py
- value_objects.py
- register.py
- build_services
- identity/presentation/router.py
- AppError
- RedisAuthThrottle
- services.py
- dataclasses
- shorten-form.tsx
- resolve_link.py
- Settings
- create_app
- list_links.py
- Register
- NoopCache
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
- build_app
- test_rate_limit_dependency_sets_headers_and_429
- identity/domain/entities.py
- main.py
- language-switcher.tsx
- uuid
- AuthSession
- shared_kernel/errors.py
- test_redirect_click_failure.py
- request_context.py
- test_body_limit.py
- RateLimiter
- HostResolutionError
- security.py
- .__call__
- starlette_types
- Argon2PasswordHasher
- ref_vitest
- page.tsx
- identity/presentation/router.py
- create_link.py
- Database
- Bulkhead
- test_identity_adapters.py
- asyncio
- i18n-check.mjs
- logging.py
- proxy.ts
- unicodedata
- test_bulkhead.py

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

## Communities (92 total, 13 thin omitted)

### Community 0 - "Tricolink URL Shortener Product"
Cohesion: 0.25
Nodes (8): click_events Table, Redis Stream Click Buffer, Non-Goals, Tricolink URL Shortener Product, Redirect and Cache Hot Path, URL Anti-Abuse Policy, SSRF Prevention, Design Tokens

### Community 1 - "Token Bucket Rate Limiting"
Cohesion: 0.24
Nodes (9): Daily Link Quotas, Negative Cache for Unknown Codes, Single-Flight Lock, Stale-While-Revalidate Caching, Brute Force Protection, Bulkhead Semaphores, Circuit Breaker, Rate Limit Buckets (+1 more)

### Community 2 - "page.tsx"
Cohesion: 0.21
Nodes (10): LocaleNotFound(), ControlVisual(), FeatureBlocks(), ShortLinkVisual(), StatsVisual(), WEEKDAY_BARS, FinalCta(), Button() (+2 more)

### Community 3 - "config.py"
Cohesion: 0.13
Nodes (18): _boolean(), _env(), get_migration_database_url(), get_settings(), _integer(), _number(), SettingsError, _text() (+10 more)

### Community 4 - "Agent Workflow and Graphify"
Cohesion: 0.18
Nodes (8): graphify Slash Command, Mandatory Session Reading Order, CONTEXT.md Single Source of Truth, Graphify Context Engineering, Graphify Installation Commands, Per-Phase Graphify Routine, graphify query/path/explain Workflow, Tricolink README Stub (P11)

### Community 5 - "Compose and P01 Infra"
Cohesion: 0.16
Nodes (20): pnpm allowBuilds Allowlist, API Compose Service, app Network, data Network, postgres_data Volume, PostgreSQL 16 Compose Service, Redis 7 Compose Service, Web Compose Service (+12 more)

### Community 6 - "value_objects.py"
Cohesion: 0.10
Nodes (9): upgrade(), Base, _escape_like(), _normalize_host(), _validate_hostname(), AllowedQuota, SequenceGenerator, NoopRecordClick (+1 more)

### Community 7 - "test_real_ip.py"
Cohesion: 0.14
Nodes (8): _forwarded_for(), RealIPMiddleware, resolve_real_ip(), _NeverRedis, test_middleware_sets_request_client_to_real_ip(), test_resolve_real_ip_counts_from_the_right(), test_resolve_real_ip_falls_back_when_header_is_invalid_or_short(), test_resolve_real_ip_without_trusted_proxies_ignores_header()

### Community 8 - "MemoryTokenBucket"
Cohesion: 0.22
Nodes (9): _BucketState, MemoryTokenBucket, DownRedis, FakeClock, test_memory_bucket_consumes_and_exhausts(), test_memory_bucket_never_exceeds_capacity(), test_memory_bucket_refills(), test_rate_limiter_falls_back_to_memory_when_redis_is_down() (+1 more)

### Community 9 - "logging.py"
Cohesion: 0.24
Nodes (3): MetricsMiddleware, _route_path(), record_request()

### Community 10 - "BodyLimitMiddleware"
Cohesion: 0.26
Nodes (3): BodyLimitMiddleware, _header_values(), _send_json()

### Community 11 - "httpx"
Cohesion: 0.25
Nodes (8): SecurityHeadersMiddleware, build_inner(), test_hsts_only_in_production(), test_request_id_accepts_only_safe_values(), test_request_id_is_generated_and_returned(), test_security_headers_are_added(), test_timeout_allows_fast_requests(), test_timeout_returns_504()

### Community 15 - "User"
Cohesion: 0.14
Nodes (8): User, SqlAlchemyUserRepository, _to_user(), AuthenticateAccess, UserRepository, User, DuplicateUserError, make_user()

### Community 18 - "flusher.py"
Cohesion: 0.13
Nodes (6): do_run_migrations(), run_async_migrations(), run_migrations_online(), create_engine(), create_session_factory(), unit_of_work()

### Community 19 - "pytest"
Cohesion: 0.10
Nodes (9): record_circuit_state(), CircuitBreaker, CircuitState, CircuitOpenError, fail(), test_breaker_half_open_failure_reopens(), test_breaker_half_open_success_closes(), test_breaker_opens_after_threshold_and_rejects_calls() (+1 more)

### Community 20 - "observability/metrics.py"
Cohesion: 0.13
Nodes (5): CacheClient, FakeRedis, _sample(), test_cache_get_records_hit_and_miss(), test_cache_set_validates_ttl_and_delete()

### Community 21 - "demo-dashboard.tsx"
Cohesion: 0.11
Nodes (20): BreakdownColumns, BreakdownRow, BreakdownTable(), BreakdownTableProps, columns, ClicksChartProps, ClicksPoint, ChartPlaceholder() (+12 more)

### Community 22 - "http.py"
Cohesion: 0.21
Nodes (8): Services, _authorized(), _check_database(), _check_redis(), health_live(), health_ready(), HealthResponse, metrics()

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
Nodes (16): jittered_ttl(), _CacheRead, _entry_from_link(), RedisLinkCache, CacheEntry, cache_settings(), cleanup(), make_link() (+8 more)

### Community 28 - "ClickEvent"
Cohesion: 0.06
Nodes (28): ClickEvent, ClickFlusher, guarded(), _parse_event(), RedisClickPublisher, operation(), _browser(), ClickEvent (+20 more)

### Community 29 - "links/presentation/router.py"
Cohesion: 0.13
Nodes (12): create_link(), delete_link(), get_link(), _link_response(), list_links(), redirect_link(), _static_html(), update_link() (+4 more)

### Community 30 - "pytest"
Cohesion: 0.10
Nodes (27): CreateLinkCommand, CodeGenerator, test_code_generator_can_be_made_deterministic(), test_code_generator_uses_seven_base62_characters(), test_code_generator_validates_configuration(), build_create(), build_link(), FakeCache (+19 more)

### Community 31 - ".__init__"
Cohesion: 0.10
Nodes (3): InvalidAlias, InvalidExpiresAt, LoginRequired

### Community 32 - "pytest"
Cohesion: 0.06
Nodes (51): LoginCommand, RegisterCommand, is_blocked_ip(), build_issuer(), build_login(), build_register(), FakeAccessTokens, FakeClock (+43 more)

### Community 33 - "ports.py"
Cohesion: 0.11
Nodes (16): DeleteLink, UpdateLinkCommand, LinkNotFound, GetLink, CacheUnavailable, Clock, DailyQuota, LinkCache (+8 more)

### Community 34 - "repository.py"
Cohesion: 0.15
Nodes (17): Link, set_rls_context(), _is_code_conflict(), SqlAlchemyLinkRepository, _to_domain(), PageCursor, EmptyResolver, test_real_integrity_error_triggers_code_retry() (+9 more)

### Community 35 - "value_objects.py"
Cohesion: 0.27
Nodes (13): OriginalUrl, make_link(), test_link_state_accounts_for_expiry_and_active_flag(), test_link_with_updates_returns_a_new_entity(), test_original_url_keeps_ipv6_literal_brackets(), test_original_url_normalizes_idn_to_punycode(), test_original_url_normalizes_scheme_host_and_idn(), test_original_url_rejects_invalid_host_shapes() (+5 more)

### Community 36 - "register.py"
Cohesion: 0.22
Nodes (9): Email, InvalidEmailError, InvalidGoogleIdentityError, WeakPasswordError, _display_name(), _number(), _string(), validate_google_claims() (+1 more)

### Community 37 - "build_services"
Cohesion: 0.23
Nodes (7): build_services(), Logout, AccessTokenIssuer, Clock, SessionRepository, RefreshSession, SessionIssuer

### Community 38 - "identity/presentation/router.py"
Cohesion: 0.20
Nodes (17): GoogleNotConfigured, _client_ip(), csrf_token(), login(), logout(), me(), refresh(), register() (+9 more)

### Community 39 - "AppError"
Cohesion: 0.11
Nodes (9): AliasReserved, AliasTaken, CodeGenerationFailed, DailyQuotaExceeded, InvalidTitle, UrlNotAllowed, AppError, AuthorizationError (+1 more)

### Community 40 - "RedisAuthThrottle"
Cohesion: 0.16
Nodes (5): _digest(), RedisAuthThrottle, guarded(), operation(), ThrottleResult

### Community 41 - "services.py"
Cohesion: 0.10
Nodes (9): AnalyticsServices, IdentityServices, LinkServices, _own_hosts(), RedisDailyQuota, _seconds_until_next_utc_day(), QuotaResult, SystemClock (+1 more)

### Community 42 - "dataclasses"
Cohesion: 0.16
Nodes (9): record_cache_hit(), record_cache_miss(), record_click_dropped(), record_clicks_flushed(), record_rate_limit_fallback(), record_rate_limited(), _reset_seconds(), RateLimitResult (+1 more)

### Community 43 - "shorten-form.tsx"
Cohesion: 0.14
Nodes (14): ExternalLink(), ExternalLinkProps, HeroSection(), CopyState, CreateLinkResponse, ERROR_KEYS, FormError, ShortenForm() (+6 more)

### Community 44 - "resolve_link.py"
Cohesion: 0.22
Nodes (10): ResolvedLink, _Unset, _as_utc(), _entry_state(), _resolved_from_cache(), _resolved_from_link(), ResolveLink, _as_utc() (+2 more)

### Community 45 - "Settings"
Cohesion: 0.24
Nodes (8): Settings, clear_session_cookies(), set_csrf_cookie(), set_session_cookies(), build_session(), test_clear_cookies_deletes_all_session_cookies(), test_cookies_are_httponly_except_csrf_and_samesite_lax(), test_production_cookies_use_host_prefix_and_secure()

### Community 46 - "create_app"
Cohesion: 0.28
Nodes (17): create_app(), cleanup(), FakeGoogleOIDC, google_claims(), identity_settings(), login(), make_client(), set_cookie_headers() (+9 more)

### Community 47 - "list_links.py"
Cohesion: 0.25
Nodes (8): LinkPage, InvalidCursor, InvalidPagination, ListLinks, _normalize_query(), decode_cursor(), encode_cursor(), test_cursor_roundtrip_and_rejection()

### Community 48 - "Register"
Cohesion: 0.17
Nodes (8): AuthLocked, InvalidCredentials, InvalidEmail, WeakPassword, Login, AuthThrottle, PasswordHasher, Register

### Community 50 - "navbar.tsx"
Cohesion: 0.14
Nodes (22): dynamic, generateMetadata(), inter, jakarta, LocaleLayout(), LocaleLayoutProps, BrandLogo(), Footer() (+14 more)

### Community 51 - "api.ts"
Cohesion: 0.11
Nodes (24): api, ApiError, apiErrorFromResponse(), ApiErrorPayload, ApiRequestOptions, AuthResponseDto, CSRF_COOKIES, ensureCsrfToken() (+16 more)

### Community 52 - "adapters/google.py"
Cohesion: 0.26
Nodes (5): PyJwtAccessTokens, AccessClaims, IssuedAccessToken, test_access_jwt_contains_minimal_claims_and_validates(), test_expired_access_token_is_rejected()

### Community 53 - "google_callback"
Cohesion: 0.18
Nodes (7): GoogleOIDCClient, InvalidNextPath, google_callback(), _google_error_redirect(), google_login(), frontend_url(), safe_next_path()

### Community 54 - "links/presentation/dependencies.py"
Cohesion: 0.21
Nodes (12): apply_rate_limit_headers(), client_ip(), _get_limiter(), rate_limit(), dependency(), _retry_after_seconds(), _rate_limit_error(), user_rate_limit() (+4 more)

### Community 55 - "identity/application/ports.py"
Cohesion: 0.28
Nodes (5): RefreshToken, _revoke_family(), SqlAlchemySessionRepository, RotationResult, RotationStatus

### Community 56 - "asyncio"
Cohesion: 0.21
Nodes (6): close_redis(), create_redis(), ping_redis(), redis_client(), run(), read_stream()

### Community 57 - "error_handlers.py"
Cohesion: 0.19
Nodes (7): install_error_handlers(), handle_app_error(), handle_http_exception(), handle_unexpected_error(), handle_validation_error(), _json_error(), error_payload()

### Community 59 - "get_services"
Cohesion: 0.18
Nodes (18): CurrentUser, get_cache(), get_current_user(), get_current_user_optional(), get_rate_limiter(), get_session(), settings_dependency(), create_link_rate_limit() (+10 more)

### Community 60 - "BucketPolicy"
Cohesion: 0.16
Nodes (6): BucketPolicy, build_policies(), _reset_seconds(), RateLimiter, TokenBucketBackend, test_spoofed_xff_cannot_bypass_rate_limit()

### Community 61 - "build_app"
Cohesion: 0.22
Nodes (9): NotFoundError, build_app(), auth(), missing(), test_app_error_uses_standard_envelope(), test_security_error_uses_standard_envelope(), test_unhandled_error_does_not_leak_stack_trace(), test_unknown_route_uses_standard_envelope() (+1 more)

### Community 62 - "test_rate_limit_dependency_sets_headers_and_429"
Cohesion: 0.18
Nodes (4): DownRedis, test_global_bucket_is_shared_across_clients(), DownRedis, test_rate_limit_dependency_sets_headers_and_429()

### Community 63 - "identity/domain/entities.py"
Cohesion: 0.16
Nodes (9): AuthSession, generate_csrf_token(), generate_refresh_token(), hash_refresh_token(), _as_utc(), RefreshTokenRecord, TokenFamily, test_refresh_record_handles_naive_datetimes() (+1 more)

### Community 64 - "main.py"
Cohesion: 0.13
Nodes (7): test_health_ready_checks_postgres_and_redis(), test_metrics_accepts_valid_token(), test_metrics_rejects_wrong_token(), test_metrics_requires_token(), production_settings(), test_body_limit_is_enforced_by_the_full_app(), test_docs_and_openapi_are_disabled_in_production()

### Community 65 - "language-switcher.tsx"
Cohesion: 0.12
Nodes (14): dynamic, GET(), defaultLocale, Locale, localeLabels, locales, getPathname, redirect (+6 more)

### Community 66 - "uuid"
Cohesion: 0.36
Nodes (4): RedisTokenBucket, test_lua_bucket_consumes_exhausts_and_refills(), test_lua_bucket_is_atomic_under_concurrency(), test_lua_bucket_keeps_keys_independent()

### Community 67 - "AuthSession"
Cohesion: 0.80
Nodes (3): InvalidGoogleLogin, LoginWithGoogle, GoogleIdentity

### Community 68 - "shared_kernel/errors.py"
Cohesion: 0.18
Nodes (5): BadRequestError, ConflictError, GatewayTimeoutError, PayloadTooLargeError, ServiceUnavailableError

### Community 69 - "test_redirect_click_failure.py"
Cohesion: 0.29
Nodes (5): BlockingPublisher, click_settings(), DownRedis, test_redirect_continues_and_metric_counts_dropped_click(), test_redirect_does_not_wait_for_click_publisher()

### Community 71 - "test_body_limit.py"
Cohesion: 0.33
Nodes (5): build_app(), test_accepts_body_at_limit(), test_invalid_content_length_is_rejected(), test_rejects_chunked_body_above_limit(), test_rejects_content_length_above_limit_before_reading()

### Community 72 - "RateLimiter"
Cohesion: 0.22
Nodes (3): GlobalRateLimitMiddleware, send_with_headers(), _headers()

### Community 74 - "security.py"
Cohesion: 0.44
Nodes (5): allowed_origins(), csrf_protect(), origin_guard(), validate_origin(), CsrfError

### Community 75 - ".__call__"
Cohesion: 0.13
Nodes (8): replay_body(), capture_status(), send_with_request_id(), send_with_headers(), run(), tracked_send(), receive(), send()

### Community 79 - "ref_vitest"
Cohesion: 0.12
Nodes (9): items, authState, renderForm(), authState, navigation, renderNavbar(), dto, getMe (+1 more)

### Community 80 - "page.tsx"
Cohesion: 0.14
Nodes (18): generateMetadata(), HomePage(), HomePageProps, sitemap(), Faq(), FaqEntry, FaqProps, languageAlternates() (+10 more)

### Community 81 - "identity/presentation/router.py"
Cohesion: 0.42
Nodes (10): get_services(), get_authenticate_access(), get_get_me(), get_google_login(), get_google_oidc(), get_login(), get_logout(), get_refresh_session() (+2 more)

### Community 82 - "create_link.py"
Cohesion: 0.12
Nodes (12): CreateLink, _normalize_expiry(), normalize_expires_at(), normalize_title(), validate_url(), DuplicateCodeError, InvalidShortCodeError, InvalidUrlError (+4 more)

### Community 83 - "Database"
Cohesion: 0.11
Nodes (7): Database, test_database_ping_and_unit_of_work(), test_unit_of_work_rolls_back_on_error(), admin_settings(), run(), family_status(), run()

### Community 84 - "Bulkhead"
Cohesion: 0.16
Nodes (5): build_bulkheads(), Bulkhead, BulkheadRegistry, BulkheadFullError, test_bulkheads_are_named_and_independent()

### Community 85 - "test_identity_adapters.py"
Cohesion: 0.22
Nodes (5): fast_hasher(), test_argon2_hasher_roundtrip_and_dummy(), test_cookie_prefix_disabled_when_domain_is_set(), test_safe_next_accepts_internal_paths(), test_safe_next_rejects_external_or_control_paths()

### Community 86 - "asyncio"
Cohesion: 0.36
Nodes (12): api_settings(), cleanup(), direct_link(), seed_links(), seed_user(), test_anonymous_create_and_redirect(), test_create_rate_limit_returns_429(), test_expired_and_inactive_links_return_410() (+4 more)

### Community 87 - "i18n-check.mjs"
Cohesion: 0.13
Nodes (9): appRoot, catalogs, errors, files, flattenKeys(), localeSet, messagesDir, reference (+1 more)

### Community 88 - "logging.py"
Cohesion: 0.31
Nodes (3): configure_logging(), get_logger(), lifespan()

### Community 89 - "proxy.ts"
Cohesion: 0.11
Nodes (20): nextConfig, withNextIntl, alt, contentType, size, buildRewrites(), isShortCodePath(), RESERVED_PATTERN (+12 more)

### Community 93 - "unicodedata"
Cohesion: 0.27
Nodes (7): UpdateMeCommand, InvalidProfile, SessionExpired, GetMe, _normalize_display_name(), _normalize_locale(), UpdateMe

## Knowledge Gaps
- **18 isolated node(s):** `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching`, `lucide-react 1.60.0`, `minimumReleaseAgeExclude Policy` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 364 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_services()` connect `build_services` to `MemoryTokenBucket`, `User`, `pytest`, `observability/metrics.py`, `http.py`, `ShortCode`, `ClickEvent`, `pytest`, `ports.py`, `repository.py`, `register.py`, `RedisAuthThrottle`, `services.py`, `resolve_link.py`, `Settings`, `create_app`, `list_links.py`, `Register`, `adapters/google.py`, `google_callback`, `identity/application/ports.py`, `asyncio`, `BucketPolicy`, `main.py`, `uuid`, `AuthSession`, `HostResolutionError`, `Argon2PasswordHasher`, `create_link.py`, `Database`, `Bulkhead`, `unicodedata`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Are the 72 inferred relationships involving `Settings` (e.g. with `settings_dependency()` and `configure_logging()`) actually correct?**
  _`Settings` has 72 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `config.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12688172043010754 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `config.py`, `value_objects.py`, `flusher.py`, `pytest`, `http.py`, `ShortCode`, `ClickEvent`, `links/presentation/router.py`, `ports.py`, `repository.py`, `build_services`, `identity/presentation/router.py`, `RedisAuthThrottle`, `services.py`, `dataclasses`, `create_app`, `adapters/google.py`, `google_callback`, `asyncio`, `get_services`, `BucketPolicy`, `identity/domain/entities.py`, `main.py`, `test_redirect_click_failure.py`, `security.py`, `Database`, `Bulkhead`, `test_identity_adapters.py`, `asyncio`, `logging.py`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Are the 35 inferred relationships involving `ShortCode` (e.g. with `RedisLinkCache` and `SqlAlchemyLinkRepository`) actually correct?**
  _`ShortCode` has 35 INFERRED edges - model-reasoned connections that need verification._
- **Should `value_objects.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10241820768136557 - nodes in this community are weakly interconnected._