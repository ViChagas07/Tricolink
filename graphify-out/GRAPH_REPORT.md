# Graph Report - Tricolink  (2026-10-23)

## Corpus Check
- 285 files · ~140,365 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: (none) 10, .toml 1, .ini 1)

## Summary
- 2286 nodes · 6981 edges · 102 communities (89 shown, 13 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 957 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d5145644`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tricolink URL Shortener Product
- Token Bucket Rate Limiting
- .__init__
- cn
- Agent Workflow and Graphify
- Compose and P01 Infra
- datetime
- test_real_ip.py
- MemoryTokenBucket
- stats_repository.py
- BodyLimitMiddleware
- httpx
- pnpm Release Policy
- PostCSS Tooling
- UserRepository
- API Package
- database.py
- pytest
- stats_cache.py
- demo-dashboard.tsx
- http.py
- SECURITY.md Security Requirements
- UI_SPEC.md Tricolink Interface
- Code Standards
- REST API /api/v1 Contract
- ShortCode
- ClickEvent
- create_link
- test_links_application.py
- ref_next_intl
- pytest
- login-form.tsx
- links/adapters/repository.py
- identity/adapters/repository.py
- AccountForm
- build_services
- identity/presentation/router.py
- AppError
- dataclasses
- build_services
- create_link_rate_limit
- ShortCode
- resolve_link.py
- config.py
- create_app
- list_links.py
- Register
- links-view.tsx
- ref_next_intl
- api.ts
- adapters/tokens.py
- google_callback
- test_identity_domain.py
- Email
- config.py
- logging.py
- ids.py
- .__call__
- BucketPolicy
- User
- RedisAuthThrottle
- google_login.py
- ref_vitest
- OriginalUrl
- [locale]/page.tsx
- test_links_api.py
- helpers.py
- test_redirect_click_failure.py
- request_context.py
- test_body_limit.py
- RateLimiter
- CacheClient
- security.py
- build_app
- error_handlers.py
- deps.py
- redirect.js
- create_redis
- test_stats_api.py
- db/models.py
- Database
- Bulkhead
- Deploy — Vercel (web) + Render (API/Postgres/Redis)
- Resultados
- i18n-check.mjs
- CodeGenerator
- proxy.ts
- Settings
- test_identity_adapters.py
- sentry.py
- cleanup.py
- test_sentry.py
- shared_kernel/errors.py
- Argon2PasswordHasher
- Auditoria de segurança — P09
- env.py
- starlette_types
- test_database.py

## God Nodes (most connected - your core abstractions)
1. `Settings` - 150 edges
2. `ShortCode` - 95 edges
3. `Link` - 82 edges
4. `create_app()` - 61 edges
5. `build_services()` - 54 edges
6. `Database` - 45 edges
7. `User` - 45 edges
8. `AppError` - 43 edges
9. `cn()` - 38 edges
10. `OriginalUrl` - 37 edges

## Surprising Connections (you probably didn't know these)
- `§2 Resiliência / anti-DDoS` --references--> `Settings`  [INFERRED]
  docs/security/AUDIT.md → apps/api/src/tricolink/core/config.py
- `Configuração de produção` --references--> `Settings`  [INFERRED]
  docs/security/AUDIT.md → apps/api/src/tricolink/core/config.py
- `3. Render — API, Postgres, Key Value e cron` --references--> `Settings`  [INFERRED]
  docs/deploy/DEPLOY.md → apps/api/src/tricolink/core/config.py
- `§1 Token Bucket` --references--> `redirect()`  [INFERRED]
  docs/security/AUDIT.md → apps/api/tests/load/token_bucket.js
- `§5 Autenticação, sessão e força bruta` --references--> `auth()`  [INFERRED]
  docs/security/AUDIT.md → apps/api/tests/unit/test_errors.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Anti Cache Stampede Layer Set** — docs_agent_context_anti_cache_stampede, docs_agent_context_stale_while_revalidate, docs_agent_context_single_flight, docs_agent_context_negative_cache, docs_agent_security_bulkhead [EXTRACTED 1.00]
- **Redirect Hot Path Flow** — docs_agent_context_redirect_cache, docs_agent_context_302_redirect, docs_agent_context_click_stream, docs_agent_context_click_events_table, docs_agent_context_links_table [EXTRACTED 1.00]
- **Tricolink Docker Compose Development Stack** — docker_compose_postgres_service, docker_compose_redis_service, docker_compose_api_service, docker_compose_web_service, docker_compose_app_network, docker_compose_data_network [EXTRACTED 1.00]
- **P00 Graphify Bootstrap Pipeline** — docs_agent_progress_graphify_kilo_integration, docs_agent_progress_semantic_extraction_cache, docs_agent_progress_graph_artifacts, docs_agent_progress_phase_roadmap [INFERRED 0.85]
- **P01 Containerized Tooling and Validation** — docs_agent_progress_make_container_targets, docs_agent_progress_non_root_containers, docs_agent_progress_local_port_override, docs_agent_progress_p01_validation, docker_compose_api_service, docker_compose_web_service [INFERRED 0.85]
- **Defense in Depth Controls** — docs_agent_security_token_bucket, docs_agent_security_circuit_breaker, docs_agent_security_bulkhead, docs_agent_security_rls, docs_agent_context_url_policy [INFERRED 0.85]

## Communities (102 total, 13 thin omitted)

### Community 0 - "Tricolink URL Shortener Product"
Cohesion: 0.25
Nodes (8): click_events Table, Redis Stream Click Buffer, Non-Goals, Tricolink URL Shortener Product, Redirect and Cache Hot Path, URL Anti-Abuse Policy, SSRF Prevention, Design Tokens

### Community 1 - "Token Bucket Rate Limiting"
Cohesion: 0.24
Nodes (9): Daily Link Quotas, Negative Cache for Unknown Codes, Single-Flight Lock, Stale-While-Revalidate Caching, Brute Force Protection, Bulkhead Semaphores, Circuit Breaker, Rate Limit Buckets (+1 more)

### Community 2 - ".__init__"
Cohesion: 0.12
Nodes (4): GoogleNotConfigured, AuthorizationError, BulkheadFullError, MetricsAuthenticationError

### Community 3 - "cn"
Cohesion: 0.12
Nodes (24): LocaleNotFound(), FinalCta(), CopyState, CreateLinkResponse, ERROR_KEYS, FormError, ShortenForm(), handleSubmit() (+16 more)

### Community 4 - "Agent Workflow and Graphify"
Cohesion: 0.18
Nodes (8): graphify Slash Command, Mandatory Session Reading Order, CONTEXT.md Single Source of Truth, Graphify Context Engineering, Graphify Installation Commands, Per-Phase Graphify Routine, graphify query/path/explain Workflow, Tricolink README Stub (P11)

### Community 5 - "Compose and P01 Infra"
Cohesion: 0.16
Nodes (20): pnpm allowBuilds Allowlist, API Compose Service, app Network, data Network, postgres_data Volume, PostgreSQL 16 Compose Service, Redis 7 Compose Service, Web Compose Service (+12 more)

### Community 6 - "datetime"
Cohesion: 0.10
Nodes (10): GetLinksOverview, LinksOverview, AllowedQuota, EmptyResolver, NoopCache, SequenceGenerator, test_real_integrity_error_triggers_code_retry(), CountingRepository (+2 more)

### Community 7 - "test_real_ip.py"
Cohesion: 0.13
Nodes (9): _forwarded_for(), RealIPMiddleware, resolve_real_ip(), _NeverRedis, test_middleware_sets_request_client_to_real_ip(), test_resolve_real_ip_counts_from_the_right(), test_resolve_real_ip_falls_back_when_header_is_invalid_or_short(), test_resolve_real_ip_without_trusted_proxies_ignores_header() (+1 more)

### Community 8 - "MemoryTokenBucket"
Cohesion: 0.14
Nodes (11): _BucketState, MemoryTokenBucket, DownRedis, test_rate_limit_dependency_sets_headers_and_429(), DownRedis, FakeClock, test_memory_bucket_consumes_and_exhausts(), test_memory_bucket_never_exceeds_capacity() (+3 more)

### Community 10 - "BodyLimitMiddleware"
Cohesion: 0.26
Nodes (3): BodyLimitMiddleware, _header_values(), _send_json()

### Community 11 - "httpx"
Cohesion: 0.23
Nodes (8): RequestTimeoutMiddleware, build_inner(), test_hsts_only_in_production(), test_request_id_accepts_only_safe_values(), test_request_id_is_generated_and_returned(), test_security_headers_are_added(), test_timeout_allows_fast_requests(), test_timeout_returns_504()

### Community 15 - "UserRepository"
Cohesion: 0.17
Nodes (8): UpdateMeCommand, InvalidProfile, SessionExpired, GetMe, UserRepository, _normalize_display_name(), _normalize_locale(), UpdateMe

### Community 18 - "database.py"
Cohesion: 0.24
Nodes (3): create_engine(), create_session_factory(), unit_of_work()

### Community 19 - "pytest"
Cohesion: 0.06
Nodes (11): RedisDailyQuota, _seconds_until_next_utc_day(), CircuitBreaker, CircuitState, QuotaResult, CircuitOpenError, fail(), test_breaker_half_open_failure_reopens() (+3 more)

### Community 20 - "stats_cache.py"
Cohesion: 0.06
Nodes (32): _breakdown(), _deserialize(), RedisStatsCache, _serialize(), GetLinkStats, load(), StatsCache, StatsRepository (+24 more)

### Community 21 - "demo-dashboard.tsx"
Cohesion: 0.07
Nodes (38): BreakdownColumns, BreakdownRow, BreakdownTable(), BreakdownTableProps, columns, ClicksChart(), ClicksChartProps, ClicksPoint (+30 more)

### Community 22 - "http.py"
Cohesion: 0.23
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
Cohesion: 0.11
Nodes (18): jittered_ttl(), _CacheRead, _entry_from_link(), RedisLinkCache, CacheEntry, _async_link(), cache_settings(), cleanup() (+10 more)

### Community 28 - "ClickEvent"
Cohesion: 0.08
Nodes (19): ClickFlusher, read_group(), guarded(), _parse_event(), operation(), guarded(), _browser(), ClickEvent (+11 more)

### Community 29 - "create_link"
Cohesion: 0.16
Nodes (16): CurrentUser, get_current_user(), create_link(), delete_link(), get_link(), _link_response(), links_overview(), list_links() (+8 more)

### Community 30 - "test_links_application.py"
Cohesion: 0.13
Nodes (24): CreateLinkCommand, DuplicateCodeError, build_create(), build_link(), FakeCache, FakeClock, FakeGenerator, FakeQuota (+16 more)

### Community 31 - "ref_next_intl"
Cohesion: 0.17
Nodes (23): AccountPage(), AccountPageProps, generateMetadata(), LocaleLayout(), generateMetadata(), LinkDetailPage(), LinkDetailPageProps, generateMetadata() (+15 more)

### Community 32 - "pytest"
Cohesion: 0.06
Nodes (53): SystemHostResolver, operation(), LoginCommand, RegisterCommand, HostResolutionError, is_blocked_ip(), FakeResolver, policy() (+45 more)

### Community 33 - "login-form.tsx"
Cohesion: 0.14
Nodes (23): first(), LoginPage(), LoginPageProps, FieldError, FieldErrors, FormError, LoginForm(), handleSubmit() (+15 more)

### Community 34 - "links/adapters/repository.py"
Cohesion: 0.10
Nodes (27): Link, set_rls_context(), RedisClickPublisher, _escape_like(), _is_code_conflict(), SqlAlchemyLinkRepository, _to_domain(), PageCursor (+19 more)

### Community 35 - "identity/adapters/repository.py"
Cohesion: 0.18
Nodes (4): upgrade(), _revoke_family(), SqlAlchemySessionRepository, RotationResult

### Community 36 - "AccountForm"
Cohesion: 0.23
Nodes (13): AccountForm(), handleError(), handleLocaleChange(), handleProfileSubmit(), handleThemeChange(), ThemeToggle(), toggleTheme(), applyTheme() (+5 more)

### Community 37 - "build_services"
Cohesion: 0.15
Nodes (11): AuthSession, Logout, AccessTokenIssuer, Clock, RotationStatus, SessionRepository, RefreshSession, SessionIssuer (+3 more)

### Community 38 - "identity/presentation/router.py"
Cohesion: 0.15
Nodes (25): get_authenticate_access(), get_get_me(), get_google_login(), get_google_oidc(), get_login(), get_logout(), get_refresh_session(), get_register() (+17 more)

### Community 39 - "AppError"
Cohesion: 0.12
Nodes (11): AliasReserved, AliasTaken, CodeGenerationFailed, DailyQuotaExceeded, InvalidAlias, InvalidCursor, InvalidExpiresAt, InvalidTitle (+3 more)

### Community 40 - "dataclasses"
Cohesion: 0.21
Nodes (9): _rate_limit_error(), record_rate_limit_fallback(), record_rate_limited(), _get_limiter(), _retry_after_seconds(), _reset_seconds(), RateLimitResult, RateLimiter (+1 more)

### Community 41 - "build_services"
Cohesion: 0.22
Nodes (7): AnalyticsServices, build_services(), IdentityServices, LinkServices, _own_hosts(), SystemClock, utc_now()

### Community 42 - "create_link_rate_limit"
Cohesion: 0.19
Nodes (10): user_rate_limit(), dependency(), apply_rate_limit_headers(), client_ip(), rate_limit(), dependency(), create_link_rate_limit(), _most_restrictive() (+2 more)

### Community 43 - "ShortCode"
Cohesion: 0.09
Nodes (21): CreateLink, DeleteLink, UpdateLinkCommand, LinkNotFound, GetLink, CacheUnavailable, Clock, DailyQuota (+13 more)

### Community 44 - "resolve_link.py"
Cohesion: 0.22
Nodes (10): ResolvedLink, _Unset, _as_utc(), _entry_state(), _resolved_from_cache(), _resolved_from_link(), ResolveLink, _as_utc() (+2 more)

### Community 45 - "config.py"
Cohesion: 0.13
Nodes (23): _asyncpg_url(), _boolean(), _env(), get_migration_database_url(), get_settings(), _integer(), _number(), SettingsError (+15 more)

### Community 46 - "create_app"
Cohesion: 0.07
Nodes (67): create_app(), admin_settings(), cleanup(), run(), FakeGoogleOIDC, google_claims(), identity_settings(), login() (+59 more)

### Community 47 - "list_links.py"
Cohesion: 0.27
Nodes (7): LinkPage, InvalidPagination, ListLinks, _normalize_query(), decode_cursor(), encode_cursor(), test_cursor_roundtrip_and_rejection()

### Community 48 - "Register"
Cohesion: 0.16
Nodes (8): AuthLocked, InvalidCredentials, InvalidEmail, WeakPassword, Login, AuthThrottle, PasswordHasher, Register

### Community 49 - "links-view.tsx"
Cohesion: 0.10
Nodes (28): LinksLoading(), CopyLinkButton(), CopyLinkButtonProps, LinksSkeleton(), LinksSkeletonProps, LinkCard(), LinksView(), confirmDelete() (+20 more)

### Community 50 - "ref_next_intl"
Cohesion: 0.09
Nodes (31): dynamic, generateMetadata(), inter, jakarta, LocaleLayoutProps, LinkDetailError(), AccountFormProps, Notice (+23 more)

### Community 51 - "api.ts"
Cohesion: 0.10
Nodes (26): navigation, user, api, ApiError, apiErrorFromResponse(), ApiErrorPayload, ApiRequestOptions, AuthResponseDto (+18 more)

### Community 52 - "adapters/tokens.py"
Cohesion: 0.27
Nodes (5): PyJwtAccessTokens, AccessClaims, IssuedAccessToken, test_access_jwt_contains_minimal_claims_and_validates(), test_expired_access_token_is_rejected()

### Community 53 - "google_callback"
Cohesion: 0.13
Nodes (9): GoogleOIDCClient, InvalidNextPath, google_callback(), _google_error_redirect(), google_login(), frontend_url(), safe_next_path(), test_safe_next_accepts_internal_paths() (+1 more)

### Community 54 - "test_identity_domain.py"
Cohesion: 0.13
Nodes (18): _as_utc(), RefreshTokenRecord, PasswordPolicy, google_claims(), test_email_is_nfkc_normalized_and_lowercased(), test_email_rejects_invalid_values(), test_email_rejects_non_string_and_too_long(), test_google_claims_accept_audience_list_and_string_verified() (+10 more)

### Community 55 - "Email"
Cohesion: 0.18
Nodes (8): Email, InvalidEmailError, InvalidGoogleIdentityError, WeakPasswordError, _display_name(), _number(), _string(), validate_google_claims()

### Community 56 - "config.py"
Cohesion: 0.15
Nodes (7): ping_redis(), record_cache_hit(), record_cache_miss(), record_circuit_state(), record_click_dropped(), record_clicks_flushed(), main()

### Community 57 - "logging.py"
Cohesion: 0.14
Nodes (6): configure_logging(), get_logger(), MetricsMiddleware, _route_path(), record_request(), lifespan()

### Community 59 - ".__call__"
Cohesion: 0.20
Nodes (7): replay_body(), capture_status(), send_with_headers(), run(), tracked_send(), receive(), send()

### Community 60 - "BucketPolicy"
Cohesion: 0.16
Nodes (8): BucketPolicy, build_policies(), RedisTokenBucket, _reset_seconds(), TokenBucketBackend, test_lua_bucket_consumes_exhausts_and_refills(), test_lua_bucket_is_atomic_under_concurrency(), test_lua_bucket_keeps_keys_independent()

### Community 61 - "User"
Cohesion: 0.17
Nodes (6): SqlAlchemyUserRepository, _to_user(), AuthenticateAccess, User, DuplicateUserError, make_user()

### Community 62 - "RedisAuthThrottle"
Cohesion: 0.16
Nodes (5): _digest(), RedisAuthThrottle, guarded(), operation(), ThrottleResult

### Community 63 - "google_login.py"
Cohesion: 0.62
Nodes (3): InvalidGoogleLogin, LoginWithGoogle, GoogleIdentity

### Community 64 - "ref_vitest"
Cohesion: 0.06
Nodes (23): ExternalLink(), ExternalLinkProps, BackToTop(), MockIntersectionObserver, observers, renderBackToTop(), authState, renderForm() (+15 more)

### Community 65 - "OriginalUrl"
Cohesion: 0.14
Nodes (18): InvalidUrlError, ReservedAliasError, HostResolver, _normalize_own_host(), _normalize_host(), OriginalUrl, _validate_hostname(), test_link_state_accounts_for_expiry_and_active_flag() (+10 more)

### Community 66 - "[locale]/page.tsx"
Cohesion: 0.08
Nodes (29): dynamic, GET(), generateMetadata(), HomePage(), HomePageProps, alt, contentType, size (+21 more)

### Community 67 - "test_links_api.py"
Cohesion: 0.34
Nodes (13): api_settings(), cleanup(), direct_link(), seed_click(), seed_links(), seed_user(), test_anonymous_create_and_redirect(), test_create_rate_limit_returns_429() (+5 more)

### Community 68 - "helpers.py"
Cohesion: 0.25
Nodes (9): acleanup(), aseed_link(), _link(), _resolved(), test_invalidation_generation_blocks_a_stale_cache_refresh(), test_stats_cache_is_scoped_by_link_id_and_does_not_leak_after_code_reuse(), test_anonymous_links_are_not_visible_without_the_code_context(), test_private_tables_return_nothing_without_rls_context() (+1 more)

### Community 69 - "test_redirect_click_failure.py"
Cohesion: 0.29
Nodes (5): BlockingPublisher, click_settings(), DownRedis, test_redirect_continues_and_metric_counts_dropped_click(), test_redirect_does_not_wait_for_click_publisher()

### Community 70 - "request_context.py"
Cohesion: 0.22
Nodes (3): _incoming_request_id(), RequestIDMiddleware, send_with_request_id()

### Community 71 - "test_body_limit.py"
Cohesion: 0.33
Nodes (5): build_app(), test_accepts_body_at_limit(), test_invalid_content_length_is_rejected(), test_rejects_chunked_body_above_limit(), test_rejects_content_length_above_limit_before_reading()

### Community 72 - "RateLimiter"
Cohesion: 0.14
Nodes (5): GlobalRateLimitMiddleware, send_with_headers(), _headers(), DownRedis, test_global_bucket_is_shared_across_clients()

### Community 73 - "CacheClient"
Cohesion: 0.13
Nodes (5): CacheClient, FakeRedis, _sample(), test_cache_get_records_hit_and_miss(), test_cache_set_validates_ttl_and_delete()

### Community 74 - "security.py"
Cohesion: 0.50
Nodes (5): allowed_origins(), csrf_protect(), origin_guard(), validate_origin(), CsrfError

### Community 75 - "build_app"
Cohesion: 0.18
Nodes (11): NotFoundError, AuthenticationError, build_app(), auth(), missing(), test_app_error_uses_standard_envelope(), test_security_error_uses_standard_envelope(), test_unhandled_error_does_not_leak_stack_trace() (+3 more)

### Community 76 - "error_handlers.py"
Cohesion: 0.19
Nodes (7): install_error_handlers(), handle_app_error(), handle_http_exception(), handle_unexpected_error(), handle_validation_error(), _json_error(), error_payload()

### Community 77 - "deps.py"
Cohesion: 0.19
Nodes (15): get_cache(), get_current_user_optional(), get_rate_limiter(), get_services(), get_session(), settings_dependency(), get_click_publisher(), get_create_link() (+7 more)

### Community 79 - "redirect.js"
Cohesion: 0.06
Nodes (32): headers(), negative(), notFound, options, rateLimited, redirect(), stampede(), create() (+24 more)

### Community 80 - "create_redis"
Cohesion: 0.18
Nodes (7): close_redis(), create_redis(), redis_client(), run(), read_stream(), run(), redis_client()

### Community 81 - "test_stats_api.py"
Cohesion: 0.58
Nodes (9): api_settings(), cleanup(), seed_clicks(), seed_link(), seed_user(), test_breakdowns_keep_top_ten_and_use_other_and_direct_sentinels(), test_stats_50k_clicks_benchmark(), test_stats_rate_limit_returns_429() (+1 more)

### Community 82 - "db/models.py"
Cohesion: 0.23
Nodes (6): Base, RefreshToken, User, test_click_events_have_device_check_and_index(), test_links_have_required_constraints_and_indexes(), test_users_and_refresh_tokens_have_required_uniques()

### Community 83 - "Database"
Cohesion: 0.14
Nodes (5): Database, run(), run(), run(), run()

### Community 84 - "Bulkhead"
Cohesion: 0.15
Nodes (6): build_bulkheads(), Bulkhead, BulkheadRegistry, test_bulkhead_limits_concurrency(), test_bulkhead_times_out_when_full(), test_bulkheads_are_named_and_independent()

### Community 85 - "Deploy — Vercel (web) + Render (API/Postgres/Redis)"
Cohesion: 0.15
Nodes (12): 1. Arquitetura, 2. Pré-requisitos, 3.1 Variáveis do serviço `tricolink-api`, 3.2 Variáveis do cron `tricolink-cleanup`, 3. Render — API, Postgres, Key Value e cron, 4. Vercel — web, 5. GitHub Actions — deploy, 6. Observabilidade (+4 more)

### Community 86 - "Resultados"
Cohesion: 0.18
Nodes (10): Create — prova do token bucket (IP fixo, rampa 5→100 RPS, 55 s), Create — throughput (rampa 10→100 RPS, 55 s, IPs sintéticos por iteração), Leitura dos resultados, Metodologia, Redirect — cache frio (500 códigos, 50 VUs), Redirect — cache quente (rampa 50→150 RPS, 65 s), Redirect — prova do token bucket (IP fixo, rampa 20→300 RPS, 65 s), Reprodução (+2 more)

### Community 87 - "i18n-check.mjs"
Cohesion: 0.09
Nodes (16): appRoot, catalogs, errors, files, flattenKeys(), localeSet, messagesDir, reference (+8 more)

### Community 88 - "CodeGenerator"
Cohesion: 0.36
Nodes (4): CodeGenerator, test_code_generator_can_be_made_deterministic(), test_code_generator_uses_seven_base62_characters(), test_code_generator_validates_configuration()

### Community 89 - "proxy.ts"
Cohesion: 0.14
Nodes (17): nextConfig, withNextIntl, buildRewrites(), isShortCodePath(), RESERVED_PATTERN, RESERVED_TOP_LEVEL, RewriteRule, RewritesConfig (+9 more)

### Community 91 - "Settings"
Cohesion: 0.25
Nodes (6): Settings, generate_csrf_token(), clear_session_cookies(), set_csrf_cookie(), set_session_cookies(), test_clear_cookies_deletes_all_session_cookies()

### Community 92 - "test_identity_adapters.py"
Cohesion: 0.21
Nodes (7): build_session(), fast_hasher(), test_argon2_hasher_roundtrip_and_dummy(), test_cookie_prefix_disabled_when_domain_is_set(), test_cookies_are_httponly_except_csrf_and_samesite_lax(), test_google_exchange_never_decodes_an_unverified_id_token(), test_production_cookies_use_host_prefix_and_secure()

### Community 94 - "cleanup.py"
Cohesion: 0.27
Nodes (5): ClickEvent, CleanupResult, _delete_batch(), run_cleanup(), test_cleanup_deletes_old_clicks_and_expired_links_idempotently()

### Community 95 - "test_sentry.py"
Cohesion: 0.38
Nodes (3): test_sentry_is_disabled_without_a_dsn(), fake_init(), test_sentry_scrubs_request_data_and_disables_pii()

### Community 96 - "shared_kernel/errors.py"
Cohesion: 0.18
Nodes (5): BadRequestError, ConflictError, GatewayTimeoutError, PayloadTooLargeError, ServiceUnavailableError

### Community 98 - "Auditoria de segurança — P09"
Cohesion: 0.10
Nodes (20): test_runtime_role_has_rls_enforced(), test_only_config_module_reads_process_environment(), §10 Supply chain, §2 Resiliência / anti-DDoS, §3 Anti SQL Injection, §4 Anti XSS / injeção no front, §7 Credenciais e exposição, §8 Buffer overflow / limites (+12 more)

### Community 99 - "env.py"
Cohesion: 0.32
Nodes (3): do_run_migrations(), run_async_migrations(), run_migrations_online()

## Knowledge Gaps
- **18 isolated node(s):** `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching`, `lucide-react 1.60.0`, `minimumReleaseAgeExclude Policy` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 501 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `datetime`, `database.py`, `pytest`, `stats_cache.py`, `http.py`, `ShortCode`, `ClickEvent`, `create_link`, `links/adapters/repository.py`, `identity/presentation/router.py`, `dataclasses`, `build_services`, `config.py`, `create_app`, `adapters/tokens.py`, `google_callback`, `config.py`, `logging.py`, `BucketPolicy`, `RedisAuthThrottle`, `test_links_api.py`, `helpers.py`, `test_redirect_click_failure.py`, `security.py`, `deps.py`, `create_redis`, `test_stats_api.py`, `Database`, `Bulkhead`, `Deploy — Vercel (web) + Render (API/Postgres/Redis)`, `test_identity_adapters.py`, `sentry.py`, `cleanup.py`, `test_sentry.py`, `Auditoria de segurança — P09`, `test_database.py`?**
  _High betweenness centrality (0.253) - this node is a cross-community bridge._
- **Are the 106 inferred relationships involving `Settings` (e.g. with `settings_dependency()` and `configure_logging()`) actually correct?**
  _`Settings` has 106 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `.__init__` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Why does `§4 Anti XSS / injeção no front` connect `Auditoria de segurança — P09` to `proxy.ts`, `create_app`?**
  _High betweenness centrality (0.148) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `ShortCode` (e.g. with `GetLinkStats` and `RedisLinkCache`) actually correct?**
  _`ShortCode` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Should `cn` be split into smaller, more focused modules?**
  _Cohesion score 0.11585365853658537 - nodes in this community are weakly interconnected._