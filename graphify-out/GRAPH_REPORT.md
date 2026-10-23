# Graph Report - Tricolink  (2026-10-23)

## Corpus Check
- 285 files · ~140,033 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: (none) 10, .toml 1, .ini 1)

## Summary
- 2285 nodes · 6974 edges · 103 communities (91 shown, 12 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 956 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `402fb7f0`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tricolink URL Shortener Product
- Token Bucket Rate Limiting
- AppError
- identity/presentation/router.py
- Agent Workflow and Graphify
- Compose and P01 Infra
- datetime
- test_real_ip.py
- MemoryTokenBucket
- ClickEvent
- BodyLimitMiddleware
- httpx
- pnpm Release Policy
- PostCSS Tooling
- User
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
- create_app
- links/adapters/repository.py
- SqlAlchemySessionRepository
- api.ts
- build_services
- identity/presentation/router.py
- test_url_policy.py
- ClickFlusher
- build_services
- ratelimit/dependencies.py
- value_objects.py
- resolve_link.py
- config.py
- helpers.py
- list_links.py
- Register
- links-view.tsx
- ref_next_intl
- api.ts
- test_identity_adapters.py
- google_callback
- test_identity_domain.py
- Email
- config.py
- error_handlers.py
- ids.py
- .__call__
- BucketPolicy
- User
- test_click_pipeline.py
- identity/domain/entities.py
- shorten-form.tsx
- OriginalUrl
- seo.ts
- test_links_api.py
- helpers.py
- test_redirect_click_failure.py
- request_context.py
- test_body_limit.py
- RateLimiter
- CacheClient
- security.py
- test_link_cache.py
- fastapi
- deps.py
- redirect.js
- page.tsx
- test_stats_api.py
- LinkRepository
- Database
- Bulkhead
- Deploy — Vercel (web) + Render (API/Postgres/Redis)
- Resultados
- i18n-check.mjs
- CodeGenerator
- proxy.ts
- Settings
- .from_env
- main.py
- test_sqli_offensive.py
- test_sentry.py
- uuid
- opengraph-image.tsx
- Auditoria de segurança — P09
- env.py
- test_rate_limit_dependency_sets_headers_and_429
- starlette_types
- test_database.py

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
- `§1 Token Bucket` --references--> `redirect()`  [INFERRED]
  docs/security/AUDIT.md → apps/api/tests/load/token_bucket.js
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

## Communities (103 total, 12 thin omitted)

### Community 0 - "Tricolink URL Shortener Product"
Cohesion: 0.25
Nodes (8): click_events Table, Redis Stream Click Buffer, Non-Goals, Tricolink URL Shortener Product, Redirect and Cache Hot Path, URL Anti-Abuse Policy, SSRF Prevention, Design Tokens

### Community 1 - "Token Bucket Rate Limiting"
Cohesion: 0.24
Nodes (9): Daily Link Quotas, Negative Cache for Unknown Codes, Single-Flight Lock, Stale-While-Revalidate Caching, Brute Force Protection, Bulkhead Semaphores, Circuit Breaker, Rate Limit Buckets (+1 more)

### Community 2 - "AppError"
Cohesion: 0.07
Nodes (11): GoogleNotConfigured, AppError, BadRequestError, ConflictError, GatewayTimeoutError, NotFoundError, PayloadTooLargeError, ServiceUnavailableError (+3 more)

### Community 3 - "identity/presentation/router.py"
Cohesion: 0.37
Nodes (10): get_services(), get_authenticate_access(), get_get_me(), get_google_login(), get_google_oidc(), get_login(), get_logout(), get_refresh_session() (+2 more)

### Community 4 - "Agent Workflow and Graphify"
Cohesion: 0.18
Nodes (8): graphify Slash Command, Mandatory Session Reading Order, CONTEXT.md Single Source of Truth, Graphify Context Engineering, Graphify Installation Commands, Per-Phase Graphify Routine, graphify query/path/explain Workflow, Tricolink README Stub (P11)

### Community 5 - "Compose and P01 Infra"
Cohesion: 0.16
Nodes (20): pnpm allowBuilds Allowlist, API Compose Service, app Network, data Network, postgres_data Volume, PostgreSQL 16 Compose Service, Redis 7 Compose Service, Web Compose Service (+12 more)

### Community 6 - "datetime"
Cohesion: 0.08
Nodes (17): upgrade(), Base, RefreshToken, User, AllowedQuota, EmptyResolver, NoopCache, SequenceGenerator (+9 more)

### Community 7 - "test_real_ip.py"
Cohesion: 0.14
Nodes (8): _forwarded_for(), RealIPMiddleware, resolve_real_ip(), _NeverRedis, test_middleware_sets_request_client_to_real_ip(), test_resolve_real_ip_counts_from_the_right(), test_resolve_real_ip_falls_back_when_header_is_invalid_or_short(), test_resolve_real_ip_without_trusted_proxies_ignores_header()

### Community 8 - "MemoryTokenBucket"
Cohesion: 0.22
Nodes (9): _BucketState, MemoryTokenBucket, DownRedis, FakeClock, test_memory_bucket_consumes_and_exhausts(), test_memory_bucket_never_exceeds_capacity(), test_memory_bucket_refills(), test_rate_limiter_falls_back_to_memory_when_redis_is_down() (+1 more)

### Community 9 - "ClickEvent"
Cohesion: 0.16
Nodes (5): ClickEvent, _delete_batch(), SqlAlchemyStatsRepository, test_click_events_have_device_check_and_index(), test_links_have_required_constraints_and_indexes()

### Community 10 - "BodyLimitMiddleware"
Cohesion: 0.26
Nodes (3): BodyLimitMiddleware, _header_values(), _send_json()

### Community 11 - "httpx"
Cohesion: 0.25
Nodes (8): SecurityHeadersMiddleware, build_inner(), test_hsts_only_in_production(), test_request_id_accepts_only_safe_values(), test_request_id_is_generated_and_returned(), test_security_headers_are_added(), test_timeout_allows_fast_requests(), test_timeout_returns_504()

### Community 15 - "User"
Cohesion: 0.46
Nodes (5): UpdateMeCommand, InvalidProfile, _normalize_display_name(), _normalize_locale(), UpdateMe

### Community 18 - "database.py"
Cohesion: 0.15
Nodes (6): get_settings(), create_engine(), create_session_factory(), unit_of_work(), CleanupResult, main()

### Community 19 - "pytest"
Cohesion: 0.06
Nodes (13): CircuitBreaker, CircuitState, _digest(), RedisAuthThrottle, guarded(), operation(), ThrottleResult, CircuitOpenError (+5 more)

### Community 20 - "stats_cache.py"
Cohesion: 0.08
Nodes (28): _breakdown(), _deserialize(), RedisStatsCache, _serialize(), GetLinkStats, load(), RawStats, StatsCache (+20 more)

### Community 21 - "demo-dashboard.tsx"
Cohesion: 0.08
Nodes (37): BreakdownColumns, BreakdownRow, BreakdownTable(), BreakdownTableProps, ClicksChart(), ClicksChartProps, ClicksPoint, ChartPlaceholder() (+29 more)

### Community 22 - "http.py"
Cohesion: 0.10
Nodes (12): Services, close_redis(), ping_redis(), _authorized(), _check_database(), _check_redis(), health_live(), health_ready() (+4 more)

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
Cohesion: 0.10
Nodes (13): jittered_ttl(), _CacheRead, _entry_from_link(), RedisLinkCache, CacheEntry, CacheUnavailable, Link, ShortCode (+5 more)

### Community 28 - "ClickEvent"
Cohesion: 0.19
Nodes (10): _browser(), extract_referrer_host(), normalize_country(), parse_user_agent(), UserAgentInfo, RecordClick, test_click_event_never_contains_raw_user_agent_or_ip(), test_extract_referrer_host() (+2 more)

### Community 29 - "create_link"
Cohesion: 0.12
Nodes (23): CurrentUser, create_link_rate_limit(), get_click_publisher(), get_create_link(), get_delete_link(), get_get_link(), get_links_overview(), get_list_links() (+15 more)

### Community 30 - "test_links_application.py"
Cohesion: 0.10
Nodes (26): RedisDailyQuota, CreateLinkCommand, QuotaResult, build_create(), build_link(), FakeCache, FakeClock, FakeGenerator (+18 more)

### Community 31 - "ref_next_intl"
Cohesion: 0.11
Nodes (35): AccountPage(), AccountPageProps, generateMetadata(), generateMetadata(), LinkDetailPage(), LinkDetailPageProps, generateMetadata(), LinksPage() (+27 more)

### Community 32 - "pytest"
Cohesion: 0.12
Nodes (24): LoginCommand, RegisterCommand, build_issuer(), build_login(), build_register(), FakeAccessTokens, FakeClock, FakeHasher (+16 more)

### Community 33 - "create_app"
Cohesion: 0.23
Nodes (20): create_app(), admin_settings(), cleanup(), run(), FakeGoogleOIDC, google_claims(), identity_settings(), login() (+12 more)

### Community 34 - "links/adapters/repository.py"
Cohesion: 0.12
Nodes (18): Link, set_rls_context(), _escape_like(), _is_code_conflict(), SqlAlchemyLinkRepository, _to_domain(), PageCursor, run() (+10 more)

### Community 35 - "SqlAlchemySessionRepository"
Cohesion: 0.39
Nodes (3): _revoke_family(), SqlAlchemySessionRepository, RotationResult

### Community 36 - "api.ts"
Cohesion: 0.08
Nodes (38): AccountForm(), handleError(), handleLocaleChange(), handleProfileSubmit(), handleThemeChange(), AccountFormProps, Notice, FieldError (+30 more)

### Community 37 - "build_services"
Cohesion: 0.15
Nodes (10): AuthenticateAccess, SessionExpired, Logout, AccessTokenIssuer, Clock, RotationStatus, SessionRepository, RefreshSession (+2 more)

### Community 38 - "identity/presentation/router.py"
Cohesion: 0.20
Nodes (18): InvalidNextPath, _client_ip(), csrf_token(), google_login(), login(), logout(), me(), refresh() (+10 more)

### Community 39 - "test_url_policy.py"
Cohesion: 0.15
Nodes (27): operation(), InvalidUrlError, is_blocked_ip(), policy(), test_credentials_controls_and_backslashes_are_blocked(), test_dns_rebinding_mixed_answers_are_all_checked(), test_forbidden_schemes_and_scheme_relative_urls_are_blocked(), test_global_ipv4_and_ipv6_answers_are_accepted() (+19 more)

### Community 40 - "ClickFlusher"
Cohesion: 0.13
Nodes (7): record_clicks_flushed(), ClickFlusher, read_group(), guarded(), _parse_event(), operation(), guarded()

### Community 41 - "build_services"
Cohesion: 0.18
Nodes (7): AnalyticsServices, build_services(), IdentityServices, LinkServices, _own_hosts(), SystemClock, utc_now()

### Community 42 - "ratelimit/dependencies.py"
Cohesion: 0.26
Nodes (9): _rate_limit_error(), client_ip(), _get_limiter(), rate_limit(), dependency(), _retry_after_seconds(), _reset_seconds(), _rate_limit_error() (+1 more)

### Community 43 - "value_objects.py"
Cohesion: 0.10
Nodes (22): CreateLink, DeleteLink, AliasReserved, AliasTaken, CodeGenerationFailed, DailyQuotaExceeded, InvalidAlias, InvalidExpiresAt (+14 more)

### Community 44 - "resolve_link.py"
Cohesion: 0.16
Nodes (12): ResolvedLink, _Unset, _as_utc(), _entry_state(), _resolved_from_cache(), _resolved_from_link(), ResolveLink, _as_utc() (+4 more)

### Community 45 - "config.py"
Cohesion: 0.21
Nodes (9): _asyncpg_url(), _boolean(), _env(), get_migration_database_url(), _integer(), _number(), SettingsError, _text() (+1 more)

### Community 46 - "helpers.py"
Cohesion: 0.24
Nodes (25): cleanup_email(), make_client(), security_settings(), unique_ip(), csrf_headers(), login(), register(), test_csrf_origin_and_cross_site_mutations_are_rejected() (+17 more)

### Community 47 - "list_links.py"
Cohesion: 0.23
Nodes (8): LinkPage, InvalidCursor, InvalidPagination, ListLinks, _normalize_query(), decode_cursor(), encode_cursor(), test_cursor_roundtrip_and_rejection()

### Community 48 - "Register"
Cohesion: 0.21
Nodes (4): InvalidCredentials, Login, AuthThrottle, PasswordHasher

### Community 49 - "links-view.tsx"
Cohesion: 0.08
Nodes (41): LinksLoading(), LocaleNotFound(), FinalCta(), CopyLinkButton(), CopyLinkButtonProps, DeleteLinkDialog(), DeleteLinkDialogProps, EditErrors (+33 more)

### Community 50 - "ref_next_intl"
Cohesion: 0.11
Nodes (24): dynamic, generateMetadata(), inter, jakarta, LocaleLayout(), LocaleLayoutProps, LinkDetailError(), BrandLogo() (+16 more)

### Community 51 - "api.ts"
Cohesion: 0.15
Nodes (20): ApiError, apiErrorFromResponse(), ApiErrorPayload, ApiRequestOptions, AuthResponseDto, CSRF_COOKIES, ensureCsrfToken(), fetchCsrfToken() (+12 more)

### Community 52 - "test_identity_adapters.py"
Cohesion: 0.11
Nodes (12): PyJwtAccessTokens, AccessClaims, IssuedAccessToken, build_session(), fast_hasher(), test_access_jwt_contains_minimal_claims_and_validates(), test_argon2_hasher_roundtrip_and_dummy(), test_cookie_prefix_disabled_when_domain_is_set() (+4 more)

### Community 53 - "google_callback"
Cohesion: 0.17
Nodes (4): GoogleOIDCClient, google_callback(), _google_error_redirect(), frontend_url()

### Community 54 - "test_identity_domain.py"
Cohesion: 0.17
Nodes (16): _number(), _string(), validate_google_claims(), google_claims(), test_email_is_nfkc_normalized_and_lowercased(), test_email_rejects_invalid_values(), test_email_rejects_non_string_and_too_long(), test_google_claims_accept_audience_list_and_string_verified() (+8 more)

### Community 55 - "Email"
Cohesion: 0.20
Nodes (10): AuthLocked, InvalidEmail, WeakPassword, Register, Email, InvalidEmailError, InvalidGoogleIdentityError, WeakPasswordError (+2 more)

### Community 56 - "config.py"
Cohesion: 0.19
Nodes (7): record_cache_hit(), record_cache_miss(), record_circuit_state(), record_click_dropped(), record_rate_limited(), _seconds_until_next_utc_day(), _retry_after()

### Community 57 - "error_handlers.py"
Cohesion: 0.07
Nodes (19): install_error_handlers(), handle_app_error(), handle_http_exception(), handle_unexpected_error(), handle_validation_error(), _json_error(), configure_logging(), get_logger() (+11 more)

### Community 59 - ".__call__"
Cohesion: 0.12
Nodes (9): replay_body(), send_with_headers(), capture_status(), send_with_request_id(), send_with_headers(), run(), tracked_send(), receive() (+1 more)

### Community 60 - "BucketPolicy"
Cohesion: 0.18
Nodes (5): BucketPolicy, build_policies(), _reset_seconds(), TokenBucketBackend, test_spoofed_xff_cannot_bypass_rate_limit()

### Community 61 - "User"
Cohesion: 0.14
Nodes (6): SqlAlchemyUserRepository, _to_user(), GetMe, UserRepository, User, DuplicateUserError

### Community 62 - "test_click_pipeline.py"
Cohesion: 0.36
Nodes (10): RedisClickPublisher, ClickEvent, admin_settings(), DownRedis, make_link(), pipeline_settings(), test_flusher_persists_batch_and_increments_click_count(), test_flusher_recreates_the_group_after_the_stream_is_lost() (+2 more)

### Community 63 - "identity/domain/entities.py"
Cohesion: 0.18
Nodes (10): AuthSession, InvalidGoogleLogin, LoginWithGoogle, SessionIssuer, _as_utc(), RefreshTokenRecord, TokenFamily, GoogleIdentity (+2 more)

### Community 64 - "shorten-form.tsx"
Cohesion: 0.09
Nodes (22): columns, ExternalLink(), ExternalLinkProps, items, CopyState, CreateLinkResponse, ERROR_KEYS, FormError (+14 more)

### Community 65 - "OriginalUrl"
Cohesion: 0.16
Nodes (15): HostResolver, _normalize_own_host(), UrlPolicy, OriginalUrl, test_link_state_accounts_for_expiry_and_active_flag(), test_link_with_updates_returns_a_new_entity(), test_original_url_keeps_ipv6_literal_brackets(), test_original_url_normalizes_idn_to_punycode() (+7 more)

### Community 66 - "seo.ts"
Cohesion: 0.17
Nodes (13): dynamic, GET(), sitemap(), locales, buildLlmsTxt(), isPrivatePath(), isProtectedPath(), languageAlternates() (+5 more)

### Community 67 - "test_links_api.py"
Cohesion: 0.34
Nodes (13): api_settings(), cleanup(), direct_link(), seed_click(), seed_links(), seed_user(), test_anonymous_create_and_redirect(), test_create_rate_limit_returns_429() (+5 more)

### Community 68 - "helpers.py"
Cohesion: 0.22
Nodes (12): aseed_click(), aseed_link(), aseed_user(), build_app(), expires_in(), seed_click(), _link(), _resolved() (+4 more)

### Community 69 - "test_redirect_click_failure.py"
Cohesion: 0.26
Nodes (5): BlockingPublisher, click_settings(), DownRedis, test_redirect_continues_and_metric_counts_dropped_click(), test_redirect_does_not_wait_for_click_publisher()

### Community 71 - "test_body_limit.py"
Cohesion: 0.33
Nodes (5): build_app(), test_accepts_body_at_limit(), test_invalid_content_length_is_rejected(), test_rejects_chunked_body_above_limit(), test_rejects_content_length_above_limit_before_reading()

### Community 72 - "RateLimiter"
Cohesion: 0.14
Nodes (7): GlobalRateLimitMiddleware, _headers(), record_rate_limit_fallback(), RateLimitResult, RateLimiter, DownRedis, test_global_bucket_is_shared_across_clients()

### Community 73 - "CacheClient"
Cohesion: 0.13
Nodes (5): CacheClient, FakeRedis, _sample(), test_cache_get_records_hit_and_miss(), test_cache_set_validates_ttl_and_delete()

### Community 74 - "security.py"
Cohesion: 0.29
Nodes (8): allowed_origins(), csrf_protect(), origin_guard(), safe_next_path(), validate_origin(), CsrfError, test_safe_next_accepts_internal_paths(), test_safe_next_rejects_external_or_control_paths()

### Community 75 - "test_link_cache.py"
Cohesion: 0.32
Nodes (11): _async_link(), cache_settings(), cleanup(), make_link(), test_cold_stampede_uses_one_database_query(), loader(), test_invalidation_during_a_stale_refresh_cannot_repopulate_the_cache(), test_invalidation_forces_the_next_read_to_use_the_loader() (+3 more)

### Community 76 - "fastapi"
Cohesion: 0.19
Nodes (5): get_get_link_stats(), link_stats(), LinkStatsResponse, StatsBreakdownResponse, StatsSeriesPointResponse

### Community 77 - "deps.py"
Cohesion: 0.20
Nodes (10): get_cache(), get_current_user(), get_current_user_optional(), get_rate_limiter(), get_session(), settings_dependency(), user_rate_limit(), dependency() (+2 more)

### Community 79 - "redirect.js"
Cohesion: 0.06
Nodes (32): headers(), negative(), notFound, options, rateLimited, redirect(), stampede(), create() (+24 more)

### Community 80 - "page.tsx"
Cohesion: 0.09
Nodes (25): generateMetadata(), HomePage(), HomePageProps, BackToTop(), MockIntersectionObserver, observers, renderBackToTop(), Faq() (+17 more)

### Community 81 - "test_stats_api.py"
Cohesion: 0.58
Nodes (9): api_settings(), cleanup(), seed_clicks(), seed_link(), seed_user(), test_breakdowns_keep_top_ten_and_use_other_and_direct_sentinels(), test_stats_50k_clicks_benchmark(), test_stats_rate_limit_returns_429() (+1 more)

### Community 82 - "LinkRepository"
Cohesion: 0.10
Nodes (10): UpdateLinkCommand, GetLinksOverview, LinksOverview, ClickPublisher, Clock, DailyQuota, LinkCache, LinkRepository (+2 more)

### Community 83 - "Database"
Cohesion: 0.10
Nodes (11): create_redis(), Database, run_cleanup(), test_cleanup_deletes_old_clicks_and_expired_links_idempotently(), run(), run(), run(), read_stream() (+3 more)

### Community 84 - "Bulkhead"
Cohesion: 0.07
Nodes (11): SystemHostResolver, build_bulkheads(), Bulkhead, BulkheadRegistry, Argon2PasswordHasher, HostResolutionError, BulkheadFullError, FakeResolver (+3 more)

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
Cohesion: 0.29
Nodes (6): Settings, generate_csrf_token(), clear_session_cookies(), set_csrf_cookie(), set_session_cookies(), test_clear_cookies_deletes_all_session_cookies()

### Community 92 - ".from_env"
Cohesion: 0.24
Nodes (11): test_cleanup_retention_is_configurable(), test_development_enables_docs(), test_get_settings_is_cached(), test_invalid_app_env_is_rejected(), test_negative_trusted_proxy_count_is_rejected(), test_postgres_urls_are_normalized_for_asyncpg(), test_production_accepts_strong_secrets(), test_production_rejects_placeholder_secrets() (+3 more)

### Community 93 - "main.py"
Cohesion: 0.09
Nodes (9): init_sentry(), _scrub_event(), test_health_ready_checks_postgres_and_redis(), test_metrics_accepts_valid_token(), test_metrics_rejects_wrong_token(), test_metrics_requires_token(), production_settings(), test_body_limit_is_enforced_by_the_full_app() (+1 more)

### Community 94 - "test_sqli_offensive.py"
Cohesion: 0.39
Nodes (8): cleanup(), seed_link(), seed_user(), test_field_and_page_limits_are_enforced(), test_sqli_payloads_are_inert_in_every_input(), test_time_based_payload_does_not_execute_pg_sleep(), test_alias_and_url_payloads_are_rejected(), test_titles_are_stored_as_inert_text_and_never_reflected_as_html()

### Community 95 - "test_sentry.py"
Cohesion: 0.38
Nodes (3): test_sentry_is_disabled_without_a_dsn(), fake_init(), test_sentry_scrubs_request_data_and_disables_pii()

### Community 96 - "uuid"
Cohesion: 0.36
Nodes (4): RedisTokenBucket, test_lua_bucket_consumes_exhausts_and_refills(), test_lua_bucket_is_atomic_under_concurrency(), test_lua_bucket_keeps_keys_independent()

### Community 97 - "opengraph-image.tsx"
Cohesion: 0.40
Nodes (3): alt, contentType, size

### Community 98 - "Auditoria de segurança — P09"
Cohesion: 0.10
Nodes (21): test_only_config_module_reads_process_environment(), auth(), §10 Supply chain, §1 Token Bucket, §2 Resiliência / anti-DDoS, §4 Anti XSS / injeção no front, §5 Autenticação, sessão e força bruta, §7 Credenciais e exposição (+13 more)

### Community 99 - "env.py"
Cohesion: 0.32
Nodes (3): do_run_migrations(), run_async_migrations(), run_migrations_online()

## Knowledge Gaps
- **18 isolated node(s):** `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching`, `lucide-react 1.60.0`, `minimumReleaseAgeExclude Policy` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 502 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `datetime`, `database.py`, `pytest`, `stats_cache.py`, `http.py`, `ShortCode`, `create_link`, `create_app`, `links/adapters/repository.py`, `identity/presentation/router.py`, `ClickFlusher`, `build_services`, `config.py`, `helpers.py`, `test_identity_adapters.py`, `google_callback`, `config.py`, `error_handlers.py`, `BucketPolicy`, `test_click_pipeline.py`, `test_links_api.py`, `helpers.py`, `test_redirect_click_failure.py`, `security.py`, `test_link_cache.py`, `deps.py`, `test_stats_api.py`, `LinkRepository`, `Database`, `Bulkhead`, `Deploy — Vercel (web) + Render (API/Postgres/Redis)`, `.from_env`, `main.py`, `test_sqli_offensive.py`, `test_sentry.py`, `Auditoria de segurança — P09`, `test_database.py`?**
  _High betweenness centrality (0.238) - this node is a cross-community bridge._
- **Are the 105 inferred relationships involving `Settings` (e.g. with `settings_dependency()` and `configure_logging()`) actually correct?**
  _`Settings` has 105 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `AppError` be split into smaller, more focused modules?**
  _Cohesion score 0.06504065040650407 - nodes in this community are weakly interconnected._
- **Why does `§4 Anti XSS / injeção no front` connect `Auditoria de segurança — P09` to `proxy.ts`, `helpers.py`?**
  _High betweenness centrality (0.152) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `ShortCode` (e.g. with `GetLinkStats` and `RedisLinkCache`) actually correct?**
  _`ShortCode` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Should `datetime` be split into smaller, more focused modules?**
  _Cohesion score 0.08456659619450317 - nodes in this community are weakly interconnected._