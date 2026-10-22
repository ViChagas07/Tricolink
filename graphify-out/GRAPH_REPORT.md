# Graph Report - Tricolink  (2026-10-22)

## Corpus Check
- 256 files · ~114,258 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: (none) 10, .ini 1, .mako 1)

## Summary
- 2050 nodes · 6184 edges · 93 communities (84 shown, 9 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 823 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fdb2a5d2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tricolink URL Shortener Product
- Token Bucket Rate Limiting
- ref_next_intl
- get_link_stats.py
- Agent Workflow and Graphify
- Compose and P01 Infra
- flusher.py
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
- stats_cache.py
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
- Link
- repository.py
- test_click_pipeline.py
- login-form.tsx
- build_services
- identity/presentation/router.py
- AppError
- Settings
- services.py
- dataclasses
- shorten-form.tsx
- resolve_link.py
- Settings
- create_app
- list_links.py
- Register
- links-view.tsx
- ref_next_intl
- api.ts
- adapters/google.py
- google_callback
- test_identity_domain.py
- test_rls.py
- asyncio
- error_handlers.py
- ids.py
- RedisAuthThrottle
- BucketPolicy
- SqlAlchemyUserRepository
- test_rate_limit_dependency_sets_headers_and_429
- identity/domain/entities.py
- main.py
- AccountForm
- build_app
- test_link_cache.py
- ClickFlusher
- test_redirect_click_failure.py
- request_context.py
- test_body_limit.py
- RateLimiter
- CacheClient
- security.py
- RequestTimeoutMiddleware
- CodeGenerator
- logging.py
- opengraph-image.tsx
- page.tsx
- identity/application/errors.py
- value_objects.py
- Database
- Bulkhead
- sqlalchemy
- asyncio
- i18n-check.mjs
- google_login.py
- proxy.ts
- test_real_integrity_error_triggers_code_retry

## God Nodes (most connected - your core abstractions)
1. `Settings` - 121 edges
2. `ShortCode` - 88 edges
3. `Link` - 75 edges
4. `build_services()` - 54 edges
5. `User` - 45 edges
6. `AppError` - 43 edges
7. `cn()` - 38 edges
8. `create_app()` - 37 edges
9. `LinkRepository` - 36 edges
10. `get_services()` - 35 edges

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

## Communities (93 total, 9 thin omitted)

### Community 0 - "Tricolink URL Shortener Product"
Cohesion: 0.25
Nodes (8): click_events Table, Redis Stream Click Buffer, Non-Goals, Tricolink URL Shortener Product, Redirect and Cache Hot Path, URL Anti-Abuse Policy, SSRF Prevention, Design Tokens

### Community 1 - "Token Bucket Rate Limiting"
Cohesion: 0.24
Nodes (9): Daily Link Quotas, Negative Cache for Unknown Codes, Single-Flight Lock, Stale-While-Revalidate Caching, Brute Force Protection, Bulkhead Semaphores, Circuit Breaker, Rate Limit Buckets (+1 more)

### Community 2 - "ref_next_intl"
Cohesion: 0.13
Nodes (12): dynamic, generateMetadata(), inter, jakarta, LocaleLayoutProps, AccountFormProps, Notice, defaultLocale (+4 more)

### Community 3 - "get_link_stats.py"
Cohesion: 0.14
Nodes (8): GetLinkStats, RawStats, StatsCache, StatsRepository, DeleteLink, LinkNotFound, GetLink, InvalidShortCodeError

### Community 4 - "Agent Workflow and Graphify"
Cohesion: 0.18
Nodes (8): graphify Slash Command, Mandatory Session Reading Order, CONTEXT.md Single Source of Truth, Graphify Context Engineering, Graphify Installation Commands, Per-Phase Graphify Routine, graphify query/path/explain Workflow, Tricolink README Stub (P11)

### Community 5 - "Compose and P01 Infra"
Cohesion: 0.16
Nodes (20): pnpm allowBuilds Allowlist, API Compose Service, app Network, data Network, postgres_data Volume, PostgreSQL 16 Compose Service, Redis 7 Compose Service, Web Compose Service (+12 more)

### Community 6 - "flusher.py"
Cohesion: 0.12
Nodes (8): upgrade(), Base, ClickEvent, RefreshToken, SqlAlchemyStatsRepository, test_click_events_have_device_check_and_index(), test_links_have_required_constraints_and_indexes(), test_users_and_refresh_tokens_have_required_uniques()

### Community 7 - "test_real_ip.py"
Cohesion: 0.13
Nodes (8): _forwarded_for(), RealIPMiddleware, resolve_real_ip(), _NeverRedis, test_middleware_sets_request_client_to_real_ip(), test_resolve_real_ip_counts_from_the_right(), test_resolve_real_ip_falls_back_when_header_is_invalid_or_short(), test_resolve_real_ip_without_trusted_proxies_ignores_header()

### Community 8 - "MemoryTokenBucket"
Cohesion: 0.13
Nodes (13): record_rate_limit_fallback(), record_rate_limited(), _BucketState, MemoryTokenBucket, RateLimiter, test_spoofed_xff_cannot_bypass_rate_limit(), DownRedis, FakeClock (+5 more)

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
Cohesion: 0.16
Nodes (5): build_services(), AuthenticateAccess, GetMe, UserRepository, User

### Community 18 - "flusher.py"
Cohesion: 0.23
Nodes (3): create_engine(), create_session_factory(), unit_of_work()

### Community 19 - "pytest"
Cohesion: 0.10
Nodes (9): record_circuit_state(), CircuitBreaker, CircuitState, CircuitOpenError, fail(), test_breaker_half_open_failure_reopens(), test_breaker_half_open_success_closes(), test_breaker_opens_after_threshold_and_rejects_calls() (+1 more)

### Community 20 - "stats_cache.py"
Cohesion: 0.10
Nodes (24): _breakdown(), _deserialize(), RedisStatsCache, _serialize(), load(), BreakdownItem, build_stats(), build_window() (+16 more)

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
Cohesion: 0.12
Nodes (11): jittered_ttl(), _CacheRead, _entry_from_link(), RedisLinkCache, CacheEntry, CacheUnavailable, Link, ShortCode (+3 more)

### Community 28 - "ClickEvent"
Cohesion: 0.14
Nodes (13): _parse_event(), _browser(), ClickEvent, extract_referrer_host(), normalize_country(), parse_user_agent(), UserAgentInfo, ClickPublisher (+5 more)

### Community 29 - "links/presentation/router.py"
Cohesion: 0.06
Nodes (47): CurrentUser, get_cache(), get_current_user(), get_current_user_optional(), get_rate_limiter(), get_services(), get_session(), settings_dependency() (+39 more)

### Community 30 - "pytest"
Cohesion: 0.13
Nodes (24): CreateLinkCommand, build_create(), build_link(), FakeCache, FakeClock, FakeGenerator, FakePublisher, FakeQuota (+16 more)

### Community 31 - "ref_next_intl"
Cohesion: 0.15
Nodes (23): AccountPage(), AccountPageProps, generateMetadata(), generateMetadata(), LinkDetailPage(), LinkDetailPageProps, generateMetadata(), LinksPage() (+15 more)

### Community 32 - "pytest"
Cohesion: 0.07
Nodes (40): SystemHostResolver, LoginCommand, RegisterCommand, HostResolutionError, is_blocked_ip(), build_issuer(), build_login(), build_register() (+32 more)

### Community 33 - "Link"
Cohesion: 0.12
Nodes (9): UpdateLinkCommand, GetLinksOverview, LinksOverview, Clock, DailyQuota, LinkCache, LinkRepository, _normalize_expiry() (+1 more)

### Community 34 - "repository.py"
Cohesion: 0.14
Nodes (16): Link, set_rls_context(), _escape_like(), _is_code_conflict(), SqlAlchemyLinkRepository, _to_domain(), PageCursor, DuplicateCodeError (+8 more)

### Community 35 - "test_click_pipeline.py"
Cohesion: 0.36
Nodes (8): RedisClickPublisher, admin_settings(), DownRedis, make_link(), pipeline_settings(), test_flusher_persists_batch_and_increments_click_count(), test_flusher_retries_pending_entries(), test_publisher_drops_event_and_increments_metric_when_redis_is_down()

### Community 36 - "login-form.tsx"
Cohesion: 0.14
Nodes (22): first(), generateMetadata(), LoginPage(), LoginPageProps, FieldError, FieldErrors, FormError, LoginForm() (+14 more)

### Community 37 - "build_services"
Cohesion: 0.17
Nodes (12): AuthSession, SessionExpired, Logout, AccessTokenIssuer, Clock, RotationStatus, SessionRepository, RefreshSession (+4 more)

### Community 38 - "identity/presentation/router.py"
Cohesion: 0.15
Nodes (26): GoogleNotConfigured, get_authenticate_access(), get_get_me(), get_google_login(), get_google_oidc(), get_login(), get_logout(), get_refresh_session() (+18 more)

### Community 39 - "AppError"
Cohesion: 0.07
Nodes (23): CreateLink, AliasReserved, AliasTaken, CodeGenerationFailed, DailyQuotaExceeded, InvalidAlias, InvalidExpiresAt, InvalidTitle (+15 more)

### Community 40 - "Settings"
Cohesion: 0.19
Nodes (8): generate_csrf_token(), clear_session_cookies(), set_csrf_cookie(), set_session_cookies(), build_session(), test_clear_cookies_deletes_all_session_cookies(), test_cookies_are_httponly_except_csrf_and_samesite_lax(), test_production_cookies_use_host_prefix_and_secure()

### Community 41 - "services.py"
Cohesion: 0.09
Nodes (9): AnalyticsServices, IdentityServices, LinkServices, _own_hosts(), RedisDailyQuota, _seconds_until_next_utc_day(), QuotaResult, SystemClock (+1 more)

### Community 42 - "dataclasses"
Cohesion: 0.17
Nodes (14): _rate_limit_error(), user_rate_limit(), dependency(), apply_rate_limit_headers(), client_ip(), _get_limiter(), rate_limit(), dependency() (+6 more)

### Community 43 - "shorten-form.tsx"
Cohesion: 0.08
Nodes (20): ExternalLink(), ExternalLinkProps, items, authState, renderForm(), authState, navigation, renderNavbar() (+12 more)

### Community 44 - "resolve_link.py"
Cohesion: 0.16
Nodes (12): ResolvedLink, _Unset, _as_utc(), _entry_state(), _resolved_from_cache(), _resolved_from_link(), ResolveLink, _as_utc() (+4 more)

### Community 45 - "Settings"
Cohesion: 0.12
Nodes (21): _boolean(), _env(), get_migration_database_url(), get_settings(), _integer(), _number(), Settings, SettingsError (+13 more)

### Community 46 - "create_app"
Cohesion: 0.21
Nodes (19): admin_settings(), cleanup(), run(), FakeGoogleOIDC, google_claims(), identity_settings(), login(), make_client() (+11 more)

### Community 47 - "list_links.py"
Cohesion: 0.23
Nodes (8): LinkPage, InvalidCursor, InvalidPagination, ListLinks, _normalize_query(), decode_cursor(), encode_cursor(), test_cursor_roundtrip_and_rejection()

### Community 48 - "Register"
Cohesion: 0.14
Nodes (12): AuthLocked, InvalidCredentials, InvalidEmail, WeakPassword, Login, AuthThrottle, PasswordHasher, Register (+4 more)

### Community 49 - "links-view.tsx"
Cohesion: 0.08
Nodes (40): LinksLoading(), handleSubmit(), DeleteLinkDialog(), DeleteLinkDialogProps, EditErrors, EditLinkDialog(), handleSubmit(), EditLinkDialogProps (+32 more)

### Community 50 - "ref_next_intl"
Cohesion: 0.12
Nodes (28): LocaleLayout(), LinkDetailError(), LocaleNotFound(), BrandLogo(), Footer(), FinalCta(), CopyState, CreateLinkResponse (+20 more)

### Community 51 - "api.ts"
Cohesion: 0.10
Nodes (28): navigation, renderForm(), user, api, ApiError, apiErrorFromResponse(), ApiErrorPayload, ApiRequestOptions (+20 more)

### Community 52 - "adapters/google.py"
Cohesion: 0.24
Nodes (6): PyJwtAccessTokens, AccessClaims, IssuedAccessToken, test_access_jwt_contains_minimal_claims_and_validates(), test_cookie_prefix_disabled_when_domain_is_set(), test_expired_access_token_is_rejected()

### Community 53 - "google_callback"
Cohesion: 0.18
Nodes (9): GoogleOIDCClient, InvalidNextPath, google_callback(), _google_error_redirect(), google_login(), frontend_url(), safe_next_path(), test_safe_next_accepts_internal_paths() (+1 more)

### Community 54 - "test_identity_domain.py"
Cohesion: 0.16
Nodes (18): InvalidGoogleIdentityError, _display_name(), _number(), _string(), validate_google_claims(), google_claims(), test_email_is_nfkc_normalized_and_lowercased(), test_email_rejects_invalid_values() (+10 more)

### Community 55 - "test_rls.py"
Cohesion: 0.24
Nodes (3): admin_settings(), make_link(), test_rls_blocks_cross_user_reads_even_without_app_filter()

### Community 56 - "asyncio"
Cohesion: 0.11
Nodes (6): close_redis(), ping_redis(), record_cache_hit(), record_cache_miss(), record_click_dropped(), redis_client()

### Community 57 - "error_handlers.py"
Cohesion: 0.12
Nodes (7): install_error_handlers(), handle_app_error(), handle_http_exception(), handle_unexpected_error(), handle_validation_error(), _json_error(), error_payload()

### Community 59 - "RedisAuthThrottle"
Cohesion: 0.16
Nodes (5): _digest(), RedisAuthThrottle, guarded(), operation(), ThrottleResult

### Community 60 - "BucketPolicy"
Cohesion: 0.16
Nodes (8): BucketPolicy, build_policies(), RedisTokenBucket, _reset_seconds(), TokenBucketBackend, test_lua_bucket_consumes_exhausts_and_refills(), test_lua_bucket_is_atomic_under_concurrency(), test_lua_bucket_keeps_keys_independent()

### Community 61 - "SqlAlchemyUserRepository"
Cohesion: 0.19
Nodes (8): User, _revoke_family(), SqlAlchemySessionRepository, SqlAlchemyUserRepository, _to_user(), RotationResult, DuplicateUserError, make_user()

### Community 62 - "test_rate_limit_dependency_sets_headers_and_429"
Cohesion: 0.18
Nodes (4): DownRedis, test_global_bucket_is_shared_across_clients(), DownRedis, test_rate_limit_dependency_sets_headers_and_429()

### Community 63 - "identity/domain/entities.py"
Cohesion: 0.29
Nodes (4): _as_utc(), RefreshTokenRecord, test_refresh_record_handles_naive_datetimes(), test_token_family_and_refresh_record_lifecycle()

### Community 64 - "main.py"
Cohesion: 0.21
Nodes (8): create_app(), test_health_ready_checks_postgres_and_redis(), test_metrics_accepts_valid_token(), test_metrics_rejects_wrong_token(), test_metrics_requires_token(), production_settings(), test_body_limit_is_enforced_by_the_full_app(), test_docs_and_openapi_are_disabled_in_production()

### Community 65 - "AccountForm"
Cohesion: 0.23
Nodes (13): AccountForm(), handleError(), handleLocaleChange(), handleProfileSubmit(), handleThemeChange(), ThemeToggle(), toggleTheme(), applyTheme() (+5 more)

### Community 66 - "build_app"
Cohesion: 0.24
Nodes (8): AuthenticationError, build_app(), auth(), test_app_error_uses_standard_envelope(), test_security_error_uses_standard_envelope(), test_unhandled_error_does_not_leak_stack_trace(), test_unknown_route_uses_standard_envelope(), test_validation_error_uses_standard_envelope()

### Community 67 - "test_link_cache.py"
Cohesion: 0.37
Nodes (9): cache_settings(), cleanup(), make_link(), test_cold_stampede_uses_one_database_query(), loader(), test_invalidation_forces_the_next_read_to_use_the_loader(), test_negative_cache_limits_missing_code_queries(), test_stale_value_is_served_while_one_refresh_runs() (+1 more)

### Community 68 - "ClickFlusher"
Cohesion: 0.16
Nodes (5): record_clicks_flushed(), ClickFlusher, guarded(), operation(), guarded()

### Community 69 - "test_redirect_click_failure.py"
Cohesion: 0.26
Nodes (5): BlockingPublisher, click_settings(), DownRedis, test_redirect_continues_and_metric_counts_dropped_click(), test_redirect_does_not_wait_for_click_publisher()

### Community 70 - "request_context.py"
Cohesion: 0.20
Nodes (3): _incoming_request_id(), RequestIDMiddleware, send_with_request_id()

### Community 71 - "test_body_limit.py"
Cohesion: 0.33
Nodes (5): build_app(), test_accepts_body_at_limit(), test_invalid_content_length_is_rejected(), test_rejects_chunked_body_above_limit(), test_rejects_content_length_above_limit_before_reading()

### Community 72 - "RateLimiter"
Cohesion: 0.22
Nodes (3): GlobalRateLimitMiddleware, send_with_headers(), _headers()

### Community 73 - "CacheClient"
Cohesion: 0.14
Nodes (5): CacheClient, FakeRedis, _sample(), test_cache_get_records_hit_and_miss(), test_cache_set_validates_ttl_and_delete()

### Community 74 - "security.py"
Cohesion: 0.38
Nodes (5): allowed_origins(), csrf_protect(), origin_guard(), validate_origin(), CsrfError

### Community 75 - "RequestTimeoutMiddleware"
Cohesion: 0.11
Nodes (8): replay_body(), capture_status(), send_with_headers(), RequestTimeoutMiddleware, run(), tracked_send(), receive(), send()

### Community 76 - "CodeGenerator"
Cohesion: 0.24
Nodes (6): CodeGenerator, test_code_generator_can_be_made_deterministic(), test_code_generator_uses_seven_base62_characters(), test_code_generator_validates_configuration(), test_reserved_aliases_cover_application_routes(), test_reserved_aliases_are_case_insensitive()

### Community 77 - "logging.py"
Cohesion: 0.31
Nodes (3): configure_logging(), get_logger(), lifespan()

### Community 79 - "opengraph-image.tsx"
Cohesion: 0.40
Nodes (3): alt, contentType, size

### Community 80 - "page.tsx"
Cohesion: 0.09
Nodes (25): dynamic, GET(), generateMetadata(), HomePage(), HomePageProps, sitemap(), Faq(), FaqEntry (+17 more)

### Community 81 - "identity/application/errors.py"
Cohesion: 0.42
Nodes (5): UpdateMeCommand, InvalidProfile, _normalize_display_name(), _normalize_locale(), UpdateMe

### Community 82 - "value_objects.py"
Cohesion: 0.13
Nodes (19): InvalidUrlError, ReservedAliasError, HostResolver, _normalize_own_host(), UrlPolicy, _normalize_host(), OriginalUrl, _validate_hostname() (+11 more)

### Community 83 - "Database"
Cohesion: 0.11
Nodes (9): create_redis(), Database, run(), run(), run(), read_stream(), run(), run() (+1 more)

### Community 84 - "Bulkhead"
Cohesion: 0.09
Nodes (10): build_bulkheads(), Bulkhead, BulkheadRegistry, Argon2PasswordHasher, BulkheadFullError, test_bulkhead_limits_concurrency(), test_bulkhead_times_out_when_full(), test_bulkheads_are_named_and_independent() (+2 more)

### Community 85 - "sqlalchemy"
Cohesion: 0.32
Nodes (3): do_run_migrations(), run_async_migrations(), run_migrations_online()

### Community 86 - "asyncio"
Cohesion: 0.34
Nodes (13): api_settings(), cleanup(), direct_link(), seed_click(), seed_links(), seed_user(), test_anonymous_create_and_redirect(), test_create_rate_limit_returns_429() (+5 more)

### Community 87 - "i18n-check.mjs"
Cohesion: 0.13
Nodes (9): appRoot, catalogs, errors, files, flattenKeys(), localeSet, messagesDir, reference (+1 more)

### Community 88 - "google_login.py"
Cohesion: 0.80
Nodes (3): InvalidGoogleLogin, LoginWithGoogle, GoogleIdentity

### Community 89 - "proxy.ts"
Cohesion: 0.13
Nodes (18): nextConfig, withNextIntl, buildRewrites(), isShortCodePath(), RESERVED_PATTERN, RESERVED_TOP_LEVEL, RewriteRule, RewritesConfig (+10 more)

### Community 92 - "test_real_integrity_error_triggers_code_retry"
Cohesion: 0.23
Nodes (5): AllowedQuota, EmptyResolver, NoopCache, SequenceGenerator, test_real_integrity_error_triggers_code_retry()

## Knowledge Gaps
- **18 isolated node(s):** `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching`, `lucide-react 1.60.0`, `minimumReleaseAgeExclude Policy` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 424 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `User`, `flusher.py`, `pytest`, `stats_cache.py`, `http.py`, `ShortCode`, `ClickEvent`, `links/presentation/router.py`, `repository.py`, `test_click_pipeline.py`, `identity/presentation/router.py`, `Settings`, `services.py`, `dataclasses`, `resolve_link.py`, `create_app`, `adapters/google.py`, `google_callback`, `test_rls.py`, `asyncio`, `error_handlers.py`, `RedisAuthThrottle`, `BucketPolicy`, `main.py`, `test_link_cache.py`, `ClickFlusher`, `test_redirect_click_failure.py`, `security.py`, `logging.py`, `Database`, `Bulkhead`, `asyncio`, `adapters/google.py`, `test_real_integrity_error_triggers_code_retry`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 79 inferred relationships involving `Settings` (e.g. with `settings_dependency()` and `configure_logging()`) actually correct?**
  _`Settings` has 79 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ref_next_intl` be split into smaller, more focused modules?**
  _Cohesion score 0.13227513227513227 - nodes in this community are weakly interconnected._
- **Why does `build_services()` connect `User` to `get_link_stats.py`, `flusher.py`, `MemoryTokenBucket`, `pytest`, `stats_cache.py`, `http.py`, `ShortCode`, `ClickEvent`, `pytest`, `Link`, `repository.py`, `test_click_pipeline.py`, `build_services`, `AppError`, `services.py`, `resolve_link.py`, `Settings`, `list_links.py`, `Register`, `adapters/google.py`, `google_callback`, `error_handlers.py`, `RedisAuthThrottle`, `BucketPolicy`, `SqlAlchemyUserRepository`, `main.py`, `ClickFlusher`, `CacheClient`, `CodeGenerator`, `identity/application/errors.py`, `value_objects.py`, `Database`, `Bulkhead`, `google_login.py`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Are the 37 inferred relationships involving `ShortCode` (e.g. with `GetLinkStats` and `RedisLinkCache`) actually correct?**
  _`ShortCode` has 37 INFERRED edges - model-reasoned connections that need verification._
- **Should `get_link_stats.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14245014245014245 - nodes in this community are weakly interconnected._