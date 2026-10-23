# Graph Report - Tricolink  (2026-10-23)

## Corpus Check
- 285 files · ~140,924 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: (none) 10, .toml 1, .ini 1)

## Summary
- 2287 nodes · 6982 edges · 108 communities (94 shown, 14 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 957 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `51de9ab8`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tricolink URL Shortener Product
- Token Bucket Rate Limiting
- InvalidShortCodeError
- cn
- Agent Workflow and Graphify
- Compose and P01 Infra
- test_real_integrity_error_triggers_code_retry
- test_real_ip.py
- MemoryTokenBucket
- test_click_pipeline.py
- BodyLimitMiddleware
- httpx
- pnpm Release Policy
- PostCSS Tooling
- UserRepository
- API Package
- database.py
- CircuitBreaker
- stats_cache.py
- demo-dashboard.tsx
- http.py
- SECURITY.md Security Requirements
- UI_SPEC.md Tricolink Interface
- Code Standards
- REST API /api/v1 Contract
- ShortCode
- click.py
- create_link
- test_links_application.py
- ref_next_intl
- test_identity_application.py
- update_link.py
- links/adapters/repository.py
- test_rls.py
- account-form.tsx
- build_services
- identity/presentation/router.py
- create_link.py
- dataclasses
- build_services
- create_link_rate_limit
- LinkRepository
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
- identity/domain/entities.py
- register.py
- config.py
- logging.py
- ids.py
- .__call__
- BucketPolicy
- User
- RedisAuthThrottle
- daily_quota.py
- ref_vitest
- OriginalUrl
- layout.tsx
- test_links_api.py
- pytest
- test_redirect_click_failure.py
- .__call__
- test_body_limit.py
- test_url_policy.py
- CacheClient
- security.py
- build_app
- error_handlers.py
- deps.py
- redirect.js
- config.py
- test_stats_api.py
- Auditoria item a item — SECURITY.md
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
- db/models.py
- test_sentry.py
- AppError
- Argon2PasswordHasher
- Auditoria de segurança — P09
- env.py
- create.js
- HostResolutionError
- test_cache_client.py
- token_bucket.js
- test_circuit_breaker.py
- test_rate_limit_dependency_sets_headers_and_429
- opengraph-image.tsx

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
- `§3 Anti SQL Injection` --references--> `test_runtime_role_has_rls_enforced()`  [EXTRACTED]
  docs/security/AUDIT.md → apps/api/tests/security/test_rls_security.py
- `§4 Anti XSS / injeção no front` --references--> `securityHeaders()`  [INFERRED]
  docs/security/AUDIT.md → apps/web/src/lib/security.ts

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Anti Cache Stampede Layer Set** — docs_agent_context_anti_cache_stampede, docs_agent_context_stale_while_revalidate, docs_agent_context_single_flight, docs_agent_context_negative_cache, docs_agent_security_bulkhead [EXTRACTED 1.00]
- **Redirect Hot Path Flow** — docs_agent_context_redirect_cache, docs_agent_context_302_redirect, docs_agent_context_click_stream, docs_agent_context_click_events_table, docs_agent_context_links_table [EXTRACTED 1.00]
- **Tricolink Docker Compose Development Stack** — docker_compose_postgres_service, docker_compose_redis_service, docker_compose_api_service, docker_compose_web_service, docker_compose_app_network, docker_compose_data_network [EXTRACTED 1.00]
- **P00 Graphify Bootstrap Pipeline** — docs_agent_progress_graphify_kilo_integration, docs_agent_progress_semantic_extraction_cache, docs_agent_progress_graph_artifacts, docs_agent_progress_phase_roadmap [INFERRED 0.85]
- **P01 Containerized Tooling and Validation** — docs_agent_progress_make_container_targets, docs_agent_progress_non_root_containers, docs_agent_progress_local_port_override, docs_agent_progress_p01_validation, docker_compose_api_service, docker_compose_web_service [INFERRED 0.85]
- **Defense in Depth Controls** — docs_agent_security_token_bucket, docs_agent_security_circuit_breaker, docs_agent_security_bulkhead, docs_agent_security_rls, docs_agent_context_url_policy [INFERRED 0.85]

## Communities (108 total, 14 thin omitted)

### Community 0 - "Tricolink URL Shortener Product"
Cohesion: 0.25
Nodes (8): click_events Table, Redis Stream Click Buffer, Non-Goals, Tricolink URL Shortener Product, Redirect and Cache Hot Path, URL Anti-Abuse Policy, SSRF Prevention, Design Tokens

### Community 1 - "Token Bucket Rate Limiting"
Cohesion: 0.24
Nodes (9): Daily Link Quotas, Negative Cache for Unknown Codes, Single-Flight Lock, Stale-While-Revalidate Caching, Brute Force Protection, Bulkhead Semaphores, Circuit Breaker, Rate Limit Buckets (+1 more)

### Community 2 - "InvalidShortCodeError"
Cohesion: 0.21
Nodes (4): LinkNotFound, GetLink, InvalidShortCodeError, ReservedAliasError

### Community 3 - "cn"
Cohesion: 0.12
Nodes (21): HeroSection(), CopyState, CreateLinkResponse, ERROR_KEYS, FormError, ShortenForm(), handleSubmit(), DeleteLinkDialog() (+13 more)

### Community 4 - "Agent Workflow and Graphify"
Cohesion: 0.18
Nodes (8): graphify Slash Command, Mandatory Session Reading Order, CONTEXT.md Single Source of Truth, Graphify Context Engineering, Graphify Installation Commands, Per-Phase Graphify Routine, graphify query/path/explain Workflow, Tricolink README Stub (P11)

### Community 5 - "Compose and P01 Infra"
Cohesion: 0.16
Nodes (20): pnpm allowBuilds Allowlist, API Compose Service, app Network, data Network, postgres_data Volume, PostgreSQL 16 Compose Service, Redis 7 Compose Service, Web Compose Service (+12 more)

### Community 6 - "test_real_integrity_error_triggers_code_retry"
Cohesion: 0.21
Nodes (5): AllowedQuota, EmptyResolver, NoopCache, SequenceGenerator, test_real_integrity_error_triggers_code_retry()

### Community 7 - "test_real_ip.py"
Cohesion: 0.13
Nodes (9): _forwarded_for(), RealIPMiddleware, resolve_real_ip(), _NeverRedis, test_middleware_sets_request_client_to_real_ip(), test_resolve_real_ip_counts_from_the_right(), test_resolve_real_ip_falls_back_when_header_is_invalid_or_short(), test_resolve_real_ip_without_trusted_proxies_ignores_header() (+1 more)

### Community 8 - "MemoryTokenBucket"
Cohesion: 0.22
Nodes (9): _BucketState, MemoryTokenBucket, DownRedis, FakeClock, test_memory_bucket_consumes_and_exhausts(), test_memory_bucket_never_exceeds_capacity(), test_memory_bucket_refills(), test_rate_limiter_falls_back_to_memory_when_redis_is_down() (+1 more)

### Community 9 - "test_click_pipeline.py"
Cohesion: 0.13
Nodes (13): ClickFlusher, read_group(), _parse_event(), RedisClickPublisher, ClickEvent, admin_settings(), DownRedis, make_link() (+5 more)

### Community 10 - "BodyLimitMiddleware"
Cohesion: 0.26
Nodes (3): BodyLimitMiddleware, _header_values(), _send_json()

### Community 11 - "httpx"
Cohesion: 0.14
Nodes (10): RequestIDMiddleware, SecurityHeadersMiddleware, RequestTimeoutMiddleware, build_inner(), test_hsts_only_in_production(), test_request_id_accepts_only_safe_values(), test_request_id_is_generated_and_returned(), test_security_headers_are_added() (+2 more)

### Community 15 - "UserRepository"
Cohesion: 0.26
Nodes (7): UpdateMeCommand, InvalidProfile, SessionExpired, GetMe, _normalize_display_name(), _normalize_locale(), UpdateMe

### Community 19 - "CircuitBreaker"
Cohesion: 0.11
Nodes (4): record_circuit_state(), CircuitBreaker, CircuitState, CircuitOpenError

### Community 20 - "stats_cache.py"
Cohesion: 0.06
Nodes (35): guarded(), operation(), _breakdown(), _deserialize(), RedisStatsCache, guarded(), _serialize(), GetLinkStats (+27 more)

### Community 21 - "demo-dashboard.tsx"
Cohesion: 0.08
Nodes (37): BreakdownColumns, BreakdownRow, BreakdownTable(), BreakdownTableProps, ClicksChart(), ClicksChartProps, ClicksPoint, ChartPlaceholder() (+29 more)

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
Cohesion: 0.11
Nodes (18): jittered_ttl(), _CacheRead, _entry_from_link(), RedisLinkCache, CacheEntry, _async_link(), cache_settings(), cleanup() (+10 more)

### Community 28 - "click.py"
Cohesion: 0.16
Nodes (11): _browser(), extract_referrer_host(), normalize_country(), parse_user_agent(), UserAgentInfo, ClickPublisher, RecordClick, test_click_event_never_contains_raw_user_agent_or_ip() (+3 more)

### Community 29 - "create_link"
Cohesion: 0.17
Nodes (15): CurrentUser, create_link(), delete_link(), get_link(), _link_response(), links_overview(), list_links(), redirect_link() (+7 more)

### Community 30 - "test_links_application.py"
Cohesion: 0.13
Nodes (25): CreateLinkCommand, UpdateLinkCommand, build_create(), build_link(), FakeCache, FakeClock, FakeGenerator, FakePublisher (+17 more)

### Community 31 - "ref_next_intl"
Cohesion: 0.12
Nodes (32): AccountPage(), AccountPageProps, generateMetadata(), generateMetadata(), generateMetadata(), LinksPage(), LinksPageProps, first() (+24 more)

### Community 32 - "test_identity_application.py"
Cohesion: 0.13
Nodes (23): RegisterCommand, build_issuer(), build_login(), build_register(), FakeAccessTokens, FakeClock, FakeHasher, FakeSessionRepository (+15 more)

### Community 33 - "update_link.py"
Cohesion: 0.18
Nodes (9): InvalidExpiresAt, InvalidTitle, UrlNotAllowed, _normalize_expiry(), UpdateLink, normalize_expires_at(), normalize_title(), validate_url() (+1 more)

### Community 34 - "links/adapters/repository.py"
Cohesion: 0.12
Nodes (19): set_rls_context(), _escape_like(), _is_code_conflict(), SqlAlchemyLinkRepository, _to_domain(), PageCursor, Link, DuplicateCodeError (+11 more)

### Community 35 - "test_rls.py"
Cohesion: 0.21
Nodes (4): admin_settings(), make_link(), make_user(), test_rls_blocks_cross_user_reads_even_without_app_filter()

### Community 36 - "account-form.tsx"
Cohesion: 0.08
Nodes (39): AccountForm(), handleError(), handleLocaleChange(), handleProfileSubmit(), handleThemeChange(), AccountFormProps, Notice, FieldError (+31 more)

### Community 37 - "build_services"
Cohesion: 0.11
Nodes (12): AuthenticateAccess, Logout, AccessTokenIssuer, Clock, IssuedAccessToken, RotationResult, RotationStatus, SessionRepository (+4 more)

### Community 38 - "identity/presentation/router.py"
Cohesion: 0.14
Nodes (25): get_authenticate_access(), get_get_me(), get_google_login(), get_google_oidc(), get_login(), get_logout(), get_refresh_session(), get_register() (+17 more)

### Community 39 - "create_link.py"
Cohesion: 0.35
Nodes (7): CreateLink, AliasReserved, AliasTaken, CodeGenerationFailed, DailyQuotaExceeded, InvalidAlias, LoginRequired

### Community 40 - "dataclasses"
Cohesion: 0.12
Nodes (12): GlobalRateLimitMiddleware, send_with_headers(), _headers(), record_rate_limit_fallback(), record_rate_limited(), _retry_after_seconds(), _reset_seconds(), RateLimitResult (+4 more)

### Community 41 - "build_services"
Cohesion: 0.27
Nodes (6): AnalyticsServices, build_services(), IdentityServices, LinkServices, _own_hosts(), SystemClock

### Community 42 - "create_link_rate_limit"
Cohesion: 0.16
Nodes (11): get_current_user(), _rate_limit_error(), user_rate_limit(), dependency(), apply_rate_limit_headers(), client_ip(), _get_limiter(), rate_limit() (+3 more)

### Community 43 - "LinkRepository"
Cohesion: 0.15
Nodes (7): DeleteLink, GetLinksOverview, LinksOverview, Clock, DailyQuota, LinkCache, LinkRepository

### Community 44 - "resolve_link.py"
Cohesion: 0.21
Nodes (10): ResolvedLink, CacheUnavailable, _as_utc(), _entry_state(), _resolved_from_cache(), _resolved_from_link(), ResolveLink, _as_utc() (+2 more)

### Community 45 - "config.py"
Cohesion: 0.13
Nodes (20): get_settings(), Settings, close_redis(), redis_client(), test_database_ping_and_unit_of_work(), test_unit_of_work_rolls_back_on_error(), test_health_ready_checks_postgres_and_redis(), redis_client() (+12 more)

### Community 46 - "create_app"
Cohesion: 0.08
Nodes (60): create_app(), admin_settings(), cleanup(), run(), FakeGoogleOIDC, google_claims(), identity_settings(), login() (+52 more)

### Community 47 - "list_links.py"
Cohesion: 0.23
Nodes (8): LinkPage, InvalidCursor, InvalidPagination, ListLinks, _normalize_query(), decode_cursor(), encode_cursor(), test_cursor_roundtrip_and_rejection()

### Community 48 - "Register"
Cohesion: 0.17
Nodes (11): AuthSession, LoginCommand, AuthLocked, InvalidCredentials, InvalidGoogleLogin, LoginWithGoogle, Login, AuthThrottle (+3 more)

### Community 49 - "links-view.tsx"
Cohesion: 0.09
Nodes (31): LinkDetailPage(), LinkDetailPageProps, LinksLoading(), CopyLinkButton(), CopyLinkButtonProps, LinksSkeleton(), LinksSkeletonProps, LinkCard() (+23 more)

### Community 50 - "ref_next_intl"
Cohesion: 0.13
Nodes (20): LocaleLayout(), LinkDetailError(), LocaleNotFound(), BrandLogo(), Footer(), FinalCta(), LanguageSwitcher(), handleListKeyDown() (+12 more)

### Community 51 - "api.ts"
Cohesion: 0.15
Nodes (20): ApiError, apiErrorFromResponse(), ApiErrorPayload, ApiRequestOptions, AuthResponseDto, CSRF_COOKIES, ensureCsrfToken(), fetchCsrfToken() (+12 more)

### Community 52 - "adapters/tokens.py"
Cohesion: 0.27
Nodes (4): PyJwtAccessTokens, AccessClaims, test_access_jwt_contains_minimal_claims_and_validates(), test_expired_access_token_is_rejected()

### Community 53 - "google_callback"
Cohesion: 0.21
Nodes (6): GoogleOIDCClient, GoogleNotConfigured, google_callback(), _google_error_redirect(), google_login(), frontend_url()

### Community 54 - "identity/domain/entities.py"
Cohesion: 0.26
Nodes (5): _as_utc(), RefreshTokenRecord, TokenFamily, test_refresh_record_handles_naive_datetimes(), test_token_family_and_refresh_record_lifecycle()

### Community 55 - "register.py"
Cohesion: 0.10
Nodes (25): InvalidEmail, WeakPassword, Register, Email, InvalidEmailError, InvalidGoogleIdentityError, WeakPasswordError, _display_name() (+17 more)

### Community 56 - "config.py"
Cohesion: 0.12
Nodes (7): unit_of_work(), record_cache_hit(), record_cache_miss(), record_click_dropped(), record_clicks_flushed(), _Unset, NoopRecordClick

### Community 57 - "logging.py"
Cohesion: 0.14
Nodes (6): configure_logging(), get_logger(), MetricsMiddleware, _route_path(), record_request(), lifespan()

### Community 59 - ".__call__"
Cohesion: 0.29
Nodes (4): replay_body(), run(), tracked_send(), receive()

### Community 60 - "BucketPolicy"
Cohesion: 0.15
Nodes (8): BucketPolicy, build_policies(), RedisTokenBucket, _reset_seconds(), TokenBucketBackend, test_lua_bucket_consumes_exhausts_and_refills(), test_lua_bucket_is_atomic_under_concurrency(), test_lua_bucket_keeps_keys_independent()

### Community 61 - "User"
Cohesion: 0.16
Nodes (6): _revoke_family(), SqlAlchemySessionRepository, SqlAlchemyUserRepository, _to_user(), User, DuplicateUserError

### Community 62 - "RedisAuthThrottle"
Cohesion: 0.16
Nodes (5): _digest(), RedisAuthThrottle, guarded(), operation(), ThrottleResult

### Community 63 - "daily_quota.py"
Cohesion: 0.18
Nodes (4): RedisDailyQuota, _seconds_until_next_utc_day(), QuotaResult, utc_now()

### Community 64 - "ref_vitest"
Cohesion: 0.06
Nodes (33): generateMetadata(), HomePage(), HomePageProps, columns, ExternalLink(), ExternalLinkProps, BackToTop(), MockIntersectionObserver (+25 more)

### Community 65 - "OriginalUrl"
Cohesion: 0.15
Nodes (17): InvalidUrlError, HostResolver, _normalize_own_host(), _normalize_host(), OriginalUrl, _validate_hostname(), test_link_state_accounts_for_expiry_and_active_flag(), test_link_with_updates_returns_a_new_entity() (+9 more)

### Community 66 - "layout.tsx"
Cohesion: 0.10
Nodes (22): dynamic, GET(), dynamic, generateMetadata(), inter, jakarta, LocaleLayoutProps, sitemap() (+14 more)

### Community 67 - "test_links_api.py"
Cohesion: 0.18
Nodes (18): create_redis(), ping_redis(), api_settings(), cleanup(), run(), direct_link(), seed_click(), seed_links() (+10 more)

### Community 68 - "pytest"
Cohesion: 0.31
Nodes (13): operation(), FakeResolver, policy(), test_credentials_controls_and_backslashes_are_blocked(), test_dns_rebinding_mixed_answers_are_all_checked(), test_forbidden_schemes_and_scheme_relative_urls_are_blocked(), test_global_ipv4_and_ipv6_answers_are_accepted(), test_obfuscated_or_internal_hostnames_are_blocked() (+5 more)

### Community 69 - "test_redirect_click_failure.py"
Cohesion: 0.29
Nodes (5): BlockingPublisher, click_settings(), DownRedis, test_redirect_continues_and_metric_counts_dropped_click(), test_redirect_does_not_wait_for_click_publisher()

### Community 70 - ".__call__"
Cohesion: 0.17
Nodes (5): capture_status(), _incoming_request_id(), send_with_request_id(), send_with_headers(), send()

### Community 71 - "test_body_limit.py"
Cohesion: 0.33
Nodes (5): build_app(), test_accepts_body_at_limit(), test_invalid_content_length_is_rejected(), test_rejects_chunked_body_above_limit(), test_rejects_content_length_above_limit_before_reading()

### Community 72 - "test_url_policy.py"
Cohesion: 0.24
Nodes (13): is_blocked_ip(), build_policy(), test_is_blocked_ip_allows_only_global_addresses(), test_is_blocked_ip_blocks_non_global_addresses(), test_url_policy_accepts_public_urls(), test_url_policy_blocks_host_when_resolution_fails_or_is_empty(), test_url_policy_blocks_invalid_dns_answer(), test_url_policy_blocks_own_domain_and_subdomains_without_dns() (+5 more)

### Community 74 - "security.py"
Cohesion: 0.50
Nodes (5): allowed_origins(), csrf_protect(), origin_guard(), validate_origin(), CsrfError

### Community 75 - "build_app"
Cohesion: 0.33
Nodes (6): build_app(), test_app_error_uses_standard_envelope(), test_security_error_uses_standard_envelope(), test_unhandled_error_does_not_leak_stack_trace(), test_unknown_route_uses_standard_envelope(), test_validation_error_uses_standard_envelope()

### Community 76 - "error_handlers.py"
Cohesion: 0.19
Nodes (7): install_error_handlers(), handle_app_error(), handle_http_exception(), handle_unexpected_error(), handle_validation_error(), _json_error(), error_payload()

### Community 77 - "deps.py"
Cohesion: 0.17
Nodes (18): get_cache(), get_current_user_optional(), get_rate_limiter(), get_services(), get_session(), settings_dependency(), create_link_rate_limit(), get_click_publisher() (+10 more)

### Community 79 - "redirect.js"
Cohesion: 0.13
Nodes (15): CODE_TTL_SECONDS, cold(), COLD_CODES, createIp(), options, otherStatuses, rateLimited, redirectDuration (+7 more)

### Community 80 - "config.py"
Cohesion: 0.21
Nodes (9): _asyncpg_url(), _boolean(), _env(), get_migration_database_url(), _integer(), _number(), SettingsError, _text() (+1 more)

### Community 81 - "test_stats_api.py"
Cohesion: 0.58
Nodes (9): api_settings(), cleanup(), seed_clicks(), seed_link(), seed_user(), test_breakdowns_keep_top_ten_and_use_other_and_direct_sentinels(), test_stats_50k_clicks_benchmark(), test_stats_rate_limit_returns_429() (+1 more)

### Community 82 - "Auditoria item a item — SECURITY.md"
Cohesion: 0.17
Nodes (13): redirect(), test_only_config_module_reads_process_environment(), auth(), §10 Supply chain, §1 Token Bucket, §2 Resiliência / anti-DDoS, §3 Anti SQL Injection, §4 Anti XSS / injeção no front (+5 more)

### Community 83 - "Database"
Cohesion: 0.09
Nodes (24): Database, RefreshToken, User, run(), run(), run(), run(), acleanup() (+16 more)

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
Cohesion: 0.24
Nodes (6): CodeGenerator, test_code_generator_can_be_made_deterministic(), test_code_generator_uses_seven_base62_characters(), test_code_generator_validates_configuration(), test_reserved_aliases_cover_application_routes(), test_reserved_aliases_are_case_insensitive()

### Community 89 - "proxy.ts"
Cohesion: 0.14
Nodes (17): nextConfig, withNextIntl, buildRewrites(), isShortCodePath(), RESERVED_PATTERN, RESERVED_TOP_LEVEL, RewriteRule, RewritesConfig (+9 more)

### Community 91 - "Settings"
Cohesion: 0.19
Nodes (8): generate_csrf_token(), clear_session_cookies(), set_csrf_cookie(), set_session_cookies(), build_session(), test_clear_cookies_deletes_all_session_cookies(), test_cookies_are_httponly_except_csrf_and_samesite_lax(), test_production_cookies_use_host_prefix_and_secure()

### Community 92 - "test_identity_adapters.py"
Cohesion: 0.12
Nodes (8): InvalidNextPath, safe_next_path(), fast_hasher(), test_argon2_hasher_roundtrip_and_dummy(), test_cookie_prefix_disabled_when_domain_is_set(), test_google_exchange_never_decodes_an_unverified_id_token(), test_safe_next_accepts_internal_paths(), test_safe_next_rejects_external_or_control_paths()

### Community 94 - "db/models.py"
Cohesion: 0.10
Nodes (13): upgrade(), Base, ClickEvent, Link, CleanupResult, _delete_batch(), main(), run_cleanup() (+5 more)

### Community 95 - "test_sentry.py"
Cohesion: 0.38
Nodes (3): test_sentry_is_disabled_without_a_dsn(), fake_init(), test_sentry_scrubs_request_data_and_disables_pii()

### Community 96 - "AppError"
Cohesion: 0.09
Nodes (9): AppError, BadRequestError, ConflictError, GatewayTimeoutError, NotFoundError, PayloadTooLargeError, ServiceUnavailableError, AuthorizationError (+1 more)

### Community 98 - "Auditoria de segurança — P09"
Cohesion: 0.18
Nodes (10): Achados residuais aceitos (com justificativa), Auditoria de segurança — P09, Como reproduzir, Conclusão, Configuração de produção, O que não foi possível testar / limitações honestas, Resumo executivo, RLS — prova independente (+2 more)

### Community 99 - "env.py"
Cohesion: 0.32
Nodes (3): do_run_migrations(), run_async_migrations(), run_migrations_online()

### Community 100 - "create.js"
Cohesion: 0.21
Nodes (10): create(), created, createDuration, createLink(), createWithSharedIp(), options, otherStatuses, rateLimited (+2 more)

### Community 101 - "HostResolutionError"
Cohesion: 0.22
Nodes (3): SystemHostResolver, HostResolutionError, FakeResolver

### Community 102 - "test_cache_client.py"
Cohesion: 0.29
Nodes (4): FakeRedis, _sample(), test_cache_get_records_hit_and_miss(), test_cache_set_validates_ttl_and_delete()

### Community 103 - "token_bucket.js"
Cohesion: 0.28
Nodes (6): headers(), negative(), notFound, options, rateLimited, stampede()

### Community 104 - "test_circuit_breaker.py"
Cohesion: 0.54
Nodes (5): fail(), test_breaker_half_open_failure_reopens(), test_breaker_half_open_success_closes(), test_breaker_opens_after_threshold_and_rejects_calls(), test_half_open_allows_only_configured_probes()

### Community 106 - "opengraph-image.tsx"
Cohesion: 0.40
Nodes (3): alt, contentType, size

## Knowledge Gaps
- **18 isolated node(s):** `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching`, `lucide-react 1.60.0`, `minimumReleaseAgeExclude Policy` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 502 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `config.py` to `test_real_integrity_error_triggers_code_retry`, `test_click_pipeline.py`, `database.py`, `CircuitBreaker`, `stats_cache.py`, `http.py`, `ShortCode`, `create_link`, `links/adapters/repository.py`, `test_rls.py`, `identity/presentation/router.py`, `dataclasses`, `build_services`, `create_link_rate_limit`, `create_app`, `adapters/tokens.py`, `google_callback`, `config.py`, `logging.py`, `BucketPolicy`, `RedisAuthThrottle`, `test_links_api.py`, `test_redirect_click_failure.py`, `security.py`, `deps.py`, `config.py`, `test_stats_api.py`, `Auditoria item a item — SECURITY.md`, `Database`, `Bulkhead`, `Deploy — Vercel (web) + Render (API/Postgres/Redis)`, `Settings`, `test_identity_adapters.py`, `sentry.py`, `db/models.py`, `test_sentry.py`, `Auditoria de segurança — P09`, `.__init__`?**
  _High betweenness centrality (0.254) - this node is a cross-community bridge._
- **Are the 106 inferred relationships involving `Settings` (e.g. with `settings_dependency()` and `configure_logging()`) actually correct?**
  _`Settings` has 106 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `cn` be split into smaller, more focused modules?**
  _Cohesion score 0.11742424242424243 - nodes in this community are weakly interconnected._
- **Why does `securityHeaders()` connect `proxy.ts` to `Auditoria item a item — SECURITY.md`?**
  _High betweenness centrality (0.147) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `ShortCode` (e.g. with `GetLinkStats` and `RedisLinkCache`) actually correct?**
  _`ShortCode` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_real_ip.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1341991341991342 - nodes in this community are weakly interconnected._