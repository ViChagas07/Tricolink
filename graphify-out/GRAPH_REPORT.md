# Graph Report - Tricolink  (2026-10-22)

## Corpus Check
- 283 files · ~132,951 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: (none) 10, .toml 1, .ini 1)

## Summary
- 2276 nodes · 6956 edges · 99 communities (85 shown, 14 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 956 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `51a76117`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tricolink URL Shortener Product
- Token Bucket Rate Limiting
- AppError
- deps.py
- Agent Workflow and Graphify
- Compose and P01 Infra
- dataclasses
- test_real_ip.py
- MemoryTokenBucket
- logging.py
- BodyLimitMiddleware
- httpx
- pnpm Release Policy
- PostCSS Tooling
- User
- API Package
- .__init__
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
- pytest
- ref_next_intl
- pytest
- LinkRepository
- links/adapters/repository.py
- identity/adapters/repository.py
- account-form.tsx
- build_services
- identity/presentation/router.py
- .__init__
- Settings
- services.py
- dataclasses
- ref_vitest
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
- Email
- config.py
- error_handlers.py
- ids.py
- RedisAuthThrottle
- RedisTokenBucket
- User
- test_rate_limit_dependency_sets_headers_and_429
- identity/domain/entities.py
- shorten-form.tsx
- OriginalUrl
- build_app
- test_links_api.py
- .from_env
- test_redirect_click_failure.py
- request_context.py
- test_body_limit.py
- RateLimiter
- CacheClient
- security.py
- test_link_cache.py
- get_link_stats.py
- create_link_rate_limit
- redirect.js
- page.tsx
- test_stats_api.py
- value_objects.py
- Database
- Bulkhead
- Deploy — Vercel (web) + Render (API/Postgres/Redis)
- Resultados
- i18n-check.mjs
- CodeGenerator
- proxy.ts
- test_identity_adapters.py
- test_real_integrity_error_triggers_code_retry
- sentry.py
- Argon2PasswordHasher
- test_sentry.py
- .__call__
- opengraph-image.tsx
- redis_client

## God Nodes (most connected - your core abstractions)
1. `Settings` - 149 edges
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
- `§3 Anti SQL Injection` --references--> `test_runtime_role_has_rls_enforced()`  [EXTRACTED]
  docs/security/AUDIT.md → apps/api/tests/security/test_rls_security.py
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

## Communities (99 total, 14 thin omitted)

### Community 0 - "Tricolink URL Shortener Product"
Cohesion: 0.25
Nodes (8): click_events Table, Redis Stream Click Buffer, Non-Goals, Tricolink URL Shortener Product, Redirect and Cache Hot Path, URL Anti-Abuse Policy, SSRF Prevention, Design Tokens

### Community 1 - "Token Bucket Rate Limiting"
Cohesion: 0.24
Nodes (9): Daily Link Quotas, Negative Cache for Unknown Codes, Single-Flight Lock, Stale-While-Revalidate Caching, Brute Force Protection, Bulkhead Semaphores, Circuit Breaker, Rate Limit Buckets (+1 more)

### Community 2 - "AppError"
Cohesion: 0.19
Nodes (14): CreateLink, AliasReserved, AliasTaken, CodeGenerationFailed, DailyQuotaExceeded, InvalidAlias, InvalidExpiresAt, InvalidTitle (+6 more)

### Community 3 - "deps.py"
Cohesion: 0.18
Nodes (17): get_cache(), get_current_user(), get_current_user_optional(), get_rate_limiter(), get_services(), get_session(), settings_dependency(), get_authenticate_access() (+9 more)

### Community 4 - "Agent Workflow and Graphify"
Cohesion: 0.18
Nodes (8): graphify Slash Command, Mandatory Session Reading Order, CONTEXT.md Single Source of Truth, Graphify Context Engineering, Graphify Installation Commands, Per-Phase Graphify Routine, graphify query/path/explain Workflow, Tricolink README Stub (P11)

### Community 5 - "Compose and P01 Infra"
Cohesion: 0.16
Nodes (20): pnpm allowBuilds Allowlist, API Compose Service, app Network, data Network, postgres_data Volume, PostgreSQL 16 Compose Service, Redis 7 Compose Service, Web Compose Service (+12 more)

### Community 6 - "dataclasses"
Cohesion: 0.11
Nodes (13): Base, ClickEvent, Link, User, CleanupResult, _delete_batch(), main(), run_cleanup() (+5 more)

### Community 7 - "test_real_ip.py"
Cohesion: 0.12
Nodes (10): _forwarded_for(), RealIPMiddleware, resolve_real_ip(), _normalize_host(), _NeverRedis, test_middleware_sets_request_client_to_real_ip(), test_resolve_real_ip_counts_from_the_right(), test_resolve_real_ip_falls_back_when_header_is_invalid_or_short() (+2 more)

### Community 8 - "MemoryTokenBucket"
Cohesion: 0.22
Nodes (9): _BucketState, MemoryTokenBucket, DownRedis, FakeClock, test_memory_bucket_consumes_and_exhausts(), test_memory_bucket_never_exceeds_capacity(), test_memory_bucket_refills(), test_rate_limiter_falls_back_to_memory_when_redis_is_down() (+1 more)

### Community 9 - "logging.py"
Cohesion: 0.14
Nodes (6): configure_logging(), get_logger(), MetricsMiddleware, _route_path(), record_request(), lifespan()

### Community 10 - "BodyLimitMiddleware"
Cohesion: 0.26
Nodes (3): BodyLimitMiddleware, _header_values(), _send_json()

### Community 11 - "httpx"
Cohesion: 0.17
Nodes (9): SecurityHeadersMiddleware, RequestTimeoutMiddleware, build_inner(), test_hsts_only_in_production(), test_request_id_accepts_only_safe_values(), test_request_id_is_generated_and_returned(), test_security_headers_are_added(), test_timeout_allows_fast_requests() (+1 more)

### Community 15 - "User"
Cohesion: 0.27
Nodes (7): UpdateMeCommand, InvalidProfile, SessionExpired, GetMe, _normalize_display_name(), _normalize_locale(), UpdateMe

### Community 19 - "pytest"
Cohesion: 0.06
Nodes (10): RedisDailyQuota, _seconds_until_next_utc_day(), CircuitBreaker, CircuitState, QuotaResult, fail(), test_breaker_half_open_failure_reopens(), test_breaker_half_open_success_closes() (+2 more)

### Community 20 - "stats_cache.py"
Cohesion: 0.11
Nodes (21): RedisStatsCache, _serialize(), load(), BreakdownItem, build_stats(), build_window(), fill_series(), full_breakdown() (+13 more)

### Community 21 - "demo-dashboard.tsx"
Cohesion: 0.07
Nodes (38): BreakdownColumns, BreakdownRow, BreakdownTable(), BreakdownTableProps, columns, ClicksChart(), ClicksChartProps, ClicksPoint (+30 more)

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
Nodes (15): jittered_ttl(), _CacheRead, _entry_from_link(), RedisLinkCache, _to_domain(), CacheEntry, Link, ShortCode (+7 more)

### Community 28 - "ClickEvent"
Cohesion: 0.09
Nodes (18): ClickFlusher, read_group(), guarded(), _parse_event(), operation(), guarded(), _browser(), ClickEvent (+10 more)

### Community 29 - "create_link"
Cohesion: 0.11
Nodes (25): CurrentUser, LinkState, get_click_publisher(), get_create_link(), get_delete_link(), get_get_link(), get_links_overview(), get_list_links() (+17 more)

### Community 30 - "pytest"
Cohesion: 0.06
Nodes (53): SystemHostResolver, CreateLinkCommand, InvalidUrlError, HostResolutionError, is_blocked_ip(), FakeResolver, policy(), test_credentials_controls_and_backslashes_are_blocked() (+45 more)

### Community 31 - "ref_next_intl"
Cohesion: 0.12
Nodes (33): AccountPage(), AccountPageProps, generateMetadata(), generateMetadata(), LinkDetailPage(), LinkDetailPageProps, generateMetadata(), LinksPage() (+25 more)

### Community 32 - "pytest"
Cohesion: 0.12
Nodes (24): LoginCommand, RegisterCommand, build_issuer(), build_login(), build_register(), FakeAccessTokens, FakeClock, FakeHasher (+16 more)

### Community 33 - "LinkRepository"
Cohesion: 0.15
Nodes (7): DeleteLink, GetLinksOverview, LinksOverview, Clock, DailyQuota, LinkCache, LinkRepository

### Community 34 - "links/adapters/repository.py"
Cohesion: 0.12
Nodes (22): RedisClickPublisher, _escape_like(), _is_code_conflict(), SqlAlchemyLinkRepository, PageCursor, DuplicateCodeError, admin_settings(), DownRedis (+14 more)

### Community 35 - "identity/adapters/repository.py"
Cohesion: 0.10
Nodes (11): upgrade(), RefreshToken, set_rls_context(), SqlAlchemyStatsRepository, _revoke_family(), SqlAlchemySessionRepository, RotationResult, admin_settings() (+3 more)

### Community 36 - "account-form.tsx"
Cohesion: 0.09
Nodes (31): AccountForm(), handleError(), handleLocaleChange(), handleProfileSubmit(), handleThemeChange(), AccountFormProps, Notice, FieldError (+23 more)

### Community 37 - "build_services"
Cohesion: 0.15
Nodes (12): AuthSession, InvalidGoogleLogin, LoginWithGoogle, Logout, Clock, RotationStatus, SessionRepository, RefreshSession (+4 more)

### Community 38 - "identity/presentation/router.py"
Cohesion: 0.23
Nodes (16): _client_ip(), csrf_token(), login(), logout(), me(), refresh(), register(), update_me() (+8 more)

### Community 39 - ".__init__"
Cohesion: 0.07
Nodes (6): BadRequestError, ConflictError, GatewayTimeoutError, PayloadTooLargeError, ServiceUnavailableError, AuthorizationError

### Community 40 - "Settings"
Cohesion: 0.29
Nodes (6): Settings, generate_csrf_token(), clear_session_cookies(), set_csrf_cookie(), set_session_cookies(), test_clear_cookies_deletes_all_session_cookies()

### Community 41 - "services.py"
Cohesion: 0.22
Nodes (7): AnalyticsServices, build_services(), IdentityServices, LinkServices, _own_hosts(), SystemClock, utc_now()

### Community 42 - "dataclasses"
Cohesion: 0.14
Nodes (14): _rate_limit_error(), _headers(), record_rate_limit_fallback(), record_rate_limited(), _get_limiter(), _retry_after_seconds(), _reset_seconds(), RateLimitResult (+6 more)

### Community 43 - "ref_vitest"
Cohesion: 0.08
Nodes (21): navigation, renderForm(), user, items, authState, renderForm(), authState, navigation (+13 more)

### Community 44 - "resolve_link.py"
Cohesion: 0.26
Nodes (8): ResolvedLink, CacheUnavailable, _as_utc(), _entry_state(), _resolved_from_cache(), _resolved_from_link(), ResolveLink, StaticResolve

### Community 45 - "Settings"
Cohesion: 0.18
Nodes (11): _asyncpg_url(), _boolean(), _env(), get_migration_database_url(), _integer(), _number(), SettingsError, _text() (+3 more)

### Community 46 - "create_app"
Cohesion: 0.07
Nodes (61): create_app(), test_health_ready_checks_postgres_and_redis(), admin_settings(), cleanup(), run(), FakeGoogleOIDC, google_claims(), identity_settings() (+53 more)

### Community 47 - "list_links.py"
Cohesion: 0.23
Nodes (8): LinkPage, InvalidCursor, InvalidPagination, ListLinks, _normalize_query(), decode_cursor(), encode_cursor(), test_cursor_roundtrip_and_rejection()

### Community 48 - "Register"
Cohesion: 0.17
Nodes (8): AuthLocked, InvalidCredentials, InvalidEmail, WeakPassword, Login, AuthThrottle, PasswordHasher, Register

### Community 49 - "links-view.tsx"
Cohesion: 0.08
Nodes (40): LinksLoading(), LocaleNotFound(), CopyLinkButton(), CopyLinkButtonProps, DeleteLinkDialog(), DeleteLinkDialogProps, EditErrors, EditLinkDialog() (+32 more)

### Community 50 - "ref_next_intl"
Cohesion: 0.10
Nodes (29): dynamic, generateMetadata(), inter, jakarta, LocaleLayout(), LocaleLayoutProps, LinkDetailError(), BrandLogo() (+21 more)

### Community 51 - "api.ts"
Cohesion: 0.15
Nodes (20): ApiError, apiErrorFromResponse(), ApiErrorPayload, ApiRequestOptions, AuthResponseDto, CSRF_COOKIES, ensureCsrfToken(), fetchCsrfToken() (+12 more)

### Community 52 - "adapters/google.py"
Cohesion: 0.27
Nodes (5): PyJwtAccessTokens, AccessClaims, IssuedAccessToken, test_access_jwt_contains_minimal_claims_and_validates(), test_expired_access_token_is_rejected()

### Community 53 - "google_callback"
Cohesion: 0.14
Nodes (9): GoogleOIDCClient, GoogleNotConfigured, google_callback(), _google_error_redirect(), google_login(), test_google_exchange_never_decodes_an_unverified_id_token(), Achados corrigidos, Achados residuais aceitos (com justificativa) (+1 more)

### Community 54 - "test_identity_domain.py"
Cohesion: 0.19
Nodes (13): google_claims(), test_email_is_nfkc_normalized_and_lowercased(), test_email_rejects_invalid_values(), test_email_rejects_non_string_and_too_long(), test_google_claims_accept_audience_list_and_string_verified(), test_google_claims_reject_untrusted_values(), test_google_claims_require_nonce(), test_google_claims_validate_and_normalize() (+5 more)

### Community 55 - "Email"
Cohesion: 0.21
Nodes (9): Email, InvalidEmailError, InvalidGoogleIdentityError, WeakPasswordError, _display_name(), _number(), _string(), validate_google_claims() (+1 more)

### Community 56 - "config.py"
Cohesion: 0.13
Nodes (10): unit_of_work(), record_cache_hit(), record_cache_miss(), record_circuit_state(), record_click_dropped(), record_clicks_flushed(), _breakdown(), _deserialize() (+2 more)

### Community 57 - "error_handlers.py"
Cohesion: 0.19
Nodes (7): install_error_handlers(), handle_app_error(), handle_http_exception(), handle_unexpected_error(), handle_validation_error(), _json_error(), error_payload()

### Community 59 - "RedisAuthThrottle"
Cohesion: 0.15
Nodes (6): _digest(), RedisAuthThrottle, guarded(), operation(), _retry_after(), ThrottleResult

### Community 60 - "RedisTokenBucket"
Cohesion: 0.36
Nodes (4): RedisTokenBucket, test_lua_bucket_consumes_exhausts_and_refills(), test_lua_bucket_is_atomic_under_concurrency(), test_lua_bucket_keeps_keys_independent()

### Community 61 - "User"
Cohesion: 0.13
Nodes (7): SqlAlchemyUserRepository, _to_user(), AuthenticateAccess, AccessTokenIssuer, UserRepository, User, DuplicateUserError

### Community 63 - "identity/domain/entities.py"
Cohesion: 0.26
Nodes (5): _as_utc(), RefreshTokenRecord, TokenFamily, test_refresh_record_handles_naive_datetimes(), test_token_family_and_refresh_record_lifecycle()

### Community 64 - "shorten-form.tsx"
Cohesion: 0.15
Nodes (14): ExternalLink(), ExternalLinkProps, HeroSection(), CopyState, CreateLinkResponse, ERROR_KEYS, FormError, ShortenForm() (+6 more)

### Community 65 - "OriginalUrl"
Cohesion: 0.20
Nodes (13): _as_utc(), OriginalUrl, test_link_state_accounts_for_expiry_and_active_flag(), test_link_with_updates_returns_a_new_entity(), test_original_url_keeps_ipv6_literal_brackets(), test_original_url_normalizes_idn_to_punycode(), test_original_url_normalizes_scheme_host_and_idn(), test_original_url_rejects_invalid_host_shapes() (+5 more)

### Community 66 - "build_app"
Cohesion: 0.24
Nodes (8): NotFoundError, build_app(), missing(), test_app_error_uses_standard_envelope(), test_security_error_uses_standard_envelope(), test_unhandled_error_does_not_leak_stack_trace(), test_unknown_route_uses_standard_envelope(), test_validation_error_uses_standard_envelope()

### Community 67 - "test_links_api.py"
Cohesion: 0.21
Nodes (19): create_redis(), api_settings(), cleanup(), run(), direct_link(), seed_click(), run(), seed_links() (+11 more)

### Community 68 - ".from_env"
Cohesion: 0.16
Nodes (13): get_settings(), redis_client(), test_database_ping_and_unit_of_work(), test_unit_of_work_rolls_back_on_error(), test_cleanup_retention_is_configurable(), test_development_enables_docs(), test_get_settings_is_cached(), test_postgres_urls_are_normalized_for_asyncpg() (+5 more)

### Community 69 - "test_redirect_click_failure.py"
Cohesion: 0.29
Nodes (5): BlockingPublisher, click_settings(), DownRedis, test_redirect_continues_and_metric_counts_dropped_click(), test_redirect_does_not_wait_for_click_publisher()

### Community 70 - "request_context.py"
Cohesion: 0.22
Nodes (3): _incoming_request_id(), RequestIDMiddleware, send_with_request_id()

### Community 71 - "test_body_limit.py"
Cohesion: 0.13
Nodes (12): replay_body(), send_with_headers(), capture_status(), run(), tracked_send(), build_app(), test_accepts_body_at_limit(), test_invalid_content_length_is_rejected() (+4 more)

### Community 72 - "RateLimiter"
Cohesion: 0.15
Nodes (3): GlobalRateLimitMiddleware, DownRedis, test_global_bucket_is_shared_across_clients()

### Community 73 - "CacheClient"
Cohesion: 0.14
Nodes (5): CacheClient, FakeRedis, _sample(), test_cache_get_records_hit_and_miss(), test_cache_set_validates_ttl_and_delete()

### Community 74 - "security.py"
Cohesion: 0.22
Nodes (10): InvalidNextPath, allowed_origins(), csrf_protect(), frontend_url(), origin_guard(), safe_next_path(), validate_origin(), CsrfError (+2 more)

### Community 75 - "test_link_cache.py"
Cohesion: 0.32
Nodes (11): _async_link(), cache_settings(), cleanup(), make_link(), test_cold_stampede_uses_one_database_query(), loader(), test_invalidation_during_a_stale_refresh_cannot_repopulate_the_cache(), test_invalidation_forces_the_next_read_to_use_the_loader() (+3 more)

### Community 76 - "get_link_stats.py"
Cohesion: 0.13
Nodes (9): GetLinkStats, RawStats, StatsCache, StatsRepository, get_get_link_stats(), link_stats(), LinkStatsResponse, StatsBreakdownResponse (+1 more)

### Community 77 - "create_link_rate_limit"
Cohesion: 0.19
Nodes (10): user_rate_limit(), dependency(), apply_rate_limit_headers(), client_ip(), rate_limit(), dependency(), create_link_rate_limit(), _most_restrictive() (+2 more)

### Community 79 - "redirect.js"
Cohesion: 0.06
Nodes (34): headers(), negative(), notFound, options, rateLimited, redirect(), stampede(), auth() (+26 more)

### Community 80 - "page.tsx"
Cohesion: 0.10
Nodes (25): dynamic, GET(), generateMetadata(), HomePage(), HomePageProps, sitemap(), Faq(), FaqEntry (+17 more)

### Community 81 - "test_stats_api.py"
Cohesion: 0.44
Nodes (11): api_settings(), cleanup(), seed_clicks(), run(), seed_link(), seed_user(), run(), test_breakdowns_keep_top_ten_and_use_other_and_direct_sentinels() (+3 more)

### Community 82 - "value_objects.py"
Cohesion: 0.11
Nodes (11): UpdateLinkCommand, LinkNotFound, GetLink, _normalize_expiry(), UpdateLink, InvalidShortCodeError, ReservedAliasError, HostResolver (+3 more)

### Community 83 - "Database"
Cohesion: 0.13
Nodes (17): Database, acleanup(), acleanup_email(), admin_settings(), aseed_click(), aseed_link(), aseed_user(), expires_in() (+9 more)

### Community 84 - "Bulkhead"
Cohesion: 0.13
Nodes (7): build_bulkheads(), Bulkhead, BulkheadRegistry, BulkheadFullError, test_bulkhead_limits_concurrency(), test_bulkhead_times_out_when_full(), test_bulkheads_are_named_and_independent()

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
Cohesion: 0.06
Nodes (34): test_only_config_module_reads_process_environment(), nextConfig, withNextIntl, buildRewrites(), isShortCodePath(), RESERVED_PATTERN, RESERVED_TOP_LEVEL, RewriteRule (+26 more)

### Community 91 - "test_identity_adapters.py"
Cohesion: 0.19
Nodes (6): build_session(), fast_hasher(), test_argon2_hasher_roundtrip_and_dummy(), test_cookie_prefix_disabled_when_domain_is_set(), test_cookies_are_httponly_except_csrf_and_samesite_lax(), test_production_cookies_use_host_prefix_and_secure()

### Community 92 - "test_real_integrity_error_triggers_code_retry"
Cohesion: 0.12
Nodes (8): do_run_migrations(), run_async_migrations(), run_migrations_online(), AllowedQuota, EmptyResolver, NoopCache, SequenceGenerator, test_real_integrity_error_triggers_code_retry()

### Community 95 - "test_sentry.py"
Cohesion: 0.38
Nodes (3): test_sentry_is_disabled_without_a_dsn(), fake_init(), test_sentry_scrubs_request_data_and_disables_pii()

### Community 97 - "opengraph-image.tsx"
Cohesion: 0.40
Nodes (3): alt, contentType, size

## Knowledge Gaps
- **18 isolated node(s):** `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching`, `lucide-react 1.60.0`, `minimumReleaseAgeExclude Policy` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 498 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `deps.py`, `dataclasses`, `logging.py`, `.__init__`, `pytest`, `stats_cache.py`, `http.py`, `ShortCode`, `ClickEvent`, `create_link`, `links/adapters/repository.py`, `identity/adapters/repository.py`, `identity/presentation/router.py`, `services.py`, `dataclasses`, `Settings`, `create_app`, `adapters/google.py`, `google_callback`, `config.py`, `RedisAuthThrottle`, `test_links_api.py`, `.from_env`, `test_redirect_click_failure.py`, `security.py`, `test_link_cache.py`, `test_stats_api.py`, `Database`, `Bulkhead`, `Deploy — Vercel (web) + Render (API/Postgres/Redis)`, `proxy.ts`, `test_identity_adapters.py`, `test_real_integrity_error_triggers_code_retry`, `sentry.py`, `test_sentry.py`, `redis_client`?**
  _High betweenness centrality (0.244) - this node is a cross-community bridge._
- **Are the 105 inferred relationships involving `Settings` (e.g. with `settings_dependency()` and `configure_logging()`) actually correct?**
  _`Settings` has 105 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `dataclasses` be split into smaller, more focused modules?**
  _Cohesion score 0.11174242424242424 - nodes in this community are weakly interconnected._
- **Why does `§4 Anti XSS / injeção no front` connect `proxy.ts` to `create_app`?**
  _High betweenness centrality (0.142) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `ShortCode` (e.g. with `GetLinkStats` and `RedisLinkCache`) actually correct?**
  _`ShortCode` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_real_ip.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12318840579710146 - nodes in this community are weakly interconnected._