# Graph Report - Tricolink  (2026-10-23)

## Corpus Check
- 285 files · ~141,886 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: (none) 10, .toml 1, .ini 1)

## Summary
- 2290 nodes · 6991 edges · 110 communities (96 shown, 14 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 958 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0c3fc947`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tricolink URL Shortener Product
- Token Bucket Rate Limiting
- test_link_cache.py
- shorten-form.tsx
- Agent Workflow and Graphify
- Compose and P01 Infra
- Database
- test_real_ip.py
- MemoryTokenBucket
- ClickFlusher
- BodyLimitMiddleware
- httpx
- pnpm Release Policy
- PostCSS Tooling
- links/presentation/router.py
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
- RedisLinkCache
- click.py
- create_link
- test_links_application.py
- ref_next_intl
- test_identity_application.py
- value_objects.py
- test_links_repository.py
- SqlAlchemyLinkRepository
- account-form.tsx
- build_services
- identity/presentation/router.py
- create_link.py
- test_identity_adapters.py
- build_services
- create_link_rate_limit
- ShortCode
- LinkRepository
- config.py
- create_app
- list_links.py
- register.py
- links-view.tsx
- ref_next_intl
- api.ts
- adapters/tokens.py
- google_callback
- RefreshTokenRecord
- register.py
- config.py
- logging.py
- ids.py
- .__call__
- BucketPolicy
- User
- sqlalchemy
- create.js
- ref_vitest
- OriginalUrl
- [locale]/page.tsx
- test_links_api.py
- pytest
- test_redirect_click_failure.py
- .__call__
- test_body_limit.py
- test_url_policy.py
- request_context.py
- security.py
- token_bucket.js
- error_handlers.py
- get_services
- redirect.js
- config.py
- proxy.ts
- redis_client
- helpers.py
- Bulkhead
- Deploy — Vercel (web) + Render (API/Postgres/Redis)
- Resultados
- i18n-check.mjs
- CodeGenerator
- proxy.ts
- Settings
- identity/adapters/repository.py
- sentry.py
- db/models.py
- test_sentry.py
- .__init__
- Argon2PasswordHasher
- Auditoria de segurança — P09
- env.py
- jittered_ttl
- HostResolutionError
- CacheClient
- dataclasses
- Auditoria item a item — SECURITY.md
- RateLimiter
- update_me.py
- redirect_link
- opengraph-image.tsx
- FakePublisher

## God Nodes (most connected - your core abstractions)
1. `Settings` - 151 edges
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
- `§1 Token Bucket` --references--> `auth()`  [INFERRED]
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

## Communities (110 total, 14 thin omitted)

### Community 0 - "Tricolink URL Shortener Product"
Cohesion: 0.25
Nodes (8): click_events Table, Redis Stream Click Buffer, Non-Goals, Tricolink URL Shortener Product, Redirect and Cache Hot Path, URL Anti-Abuse Policy, SSRF Prevention, Design Tokens

### Community 1 - "Token Bucket Rate Limiting"
Cohesion: 0.24
Nodes (9): Daily Link Quotas, Negative Cache for Unknown Codes, Single-Flight Lock, Stale-While-Revalidate Caching, Brute Force Protection, Bulkhead Semaphores, Circuit Breaker, Rate Limit Buckets (+1 more)

### Community 2 - "test_link_cache.py"
Cohesion: 0.21
Nodes (14): _async_link(), cache_settings(), cleanup(), make_link(), test_cold_stampede_uses_one_database_query(), loader(), test_invalidation_during_a_stale_refresh_cannot_repopulate_the_cache(), test_invalidation_forces_the_next_read_to_use_the_loader() (+6 more)

### Community 3 - "shorten-form.tsx"
Cohesion: 0.12
Nodes (22): CopyState, CreateLinkResponse, ERROR_KEYS, FormError, getOwnHosts(), ShortenForm(), handleSubmit(), handleUrlChange() (+14 more)

### Community 4 - "Agent Workflow and Graphify"
Cohesion: 0.18
Nodes (8): graphify Slash Command, Mandatory Session Reading Order, CONTEXT.md Single Source of Truth, Graphify Context Engineering, Graphify Installation Commands, Per-Phase Graphify Routine, graphify query/path/explain Workflow, Tricolink README Stub (P11)

### Community 5 - "Compose and P01 Infra"
Cohesion: 0.16
Nodes (20): pnpm allowBuilds Allowlist, API Compose Service, app Network, data Network, postgres_data Volume, PostgreSQL 16 Compose Service, Redis 7 Compose Service, Web Compose Service (+12 more)

### Community 6 - "Database"
Cohesion: 0.11
Nodes (7): create_redis(), Database, run(), run(), run(), read_stream(), run()

### Community 7 - "test_real_ip.py"
Cohesion: 0.14
Nodes (8): _forwarded_for(), RealIPMiddleware, resolve_real_ip(), _NeverRedis, test_middleware_sets_request_client_to_real_ip(), test_resolve_real_ip_counts_from_the_right(), test_resolve_real_ip_falls_back_when_header_is_invalid_or_short(), test_resolve_real_ip_without_trusted_proxies_ignores_header()

### Community 8 - "MemoryTokenBucket"
Cohesion: 0.20
Nodes (10): _BucketState, MemoryTokenBucket, _reset_seconds(), DownRedis, FakeClock, test_memory_bucket_consumes_and_exhausts(), test_memory_bucket_never_exceeds_capacity(), test_memory_bucket_refills() (+2 more)

### Community 9 - "ClickFlusher"
Cohesion: 0.13
Nodes (17): ClickFlusher, read_group(), guarded(), _parse_event(), RedisClickPublisher, operation(), guarded(), ClickEvent (+9 more)

### Community 10 - "BodyLimitMiddleware"
Cohesion: 0.26
Nodes (3): BodyLimitMiddleware, _header_values(), _send_json()

### Community 11 - "httpx"
Cohesion: 0.23
Nodes (8): RequestTimeoutMiddleware, build_inner(), test_hsts_only_in_production(), test_request_id_accepts_only_safe_values(), test_request_id_is_generated_and_returned(), test_security_headers_are_added(), test_timeout_allows_fast_requests(), test_timeout_returns_504()

### Community 15 - "links/presentation/router.py"
Cohesion: 0.26
Nodes (13): get_cache(), get_current_user_optional(), get_services(), get_session(), settings_dependency(), get_click_publisher(), get_create_link(), get_delete_link() (+5 more)

### Community 19 - "CircuitBreaker"
Cohesion: 0.06
Nodes (13): CircuitBreaker, CircuitState, _digest(), RedisAuthThrottle, guarded(), operation(), ThrottleResult, CircuitOpenError (+5 more)

### Community 20 - "stats_cache.py"
Cohesion: 0.05
Nodes (43): _breakdown(), _deserialize(), RedisStatsCache, _serialize(), GetLinkStats, load(), StatsCache, StatsRepository (+35 more)

### Community 21 - "demo-dashboard.tsx"
Cohesion: 0.07
Nodes (38): BreakdownColumns, BreakdownRow, BreakdownTable(), BreakdownTableProps, columns, ClicksChart(), ClicksChartProps, ClicksPoint (+30 more)

### Community 22 - "http.py"
Cohesion: 0.16
Nodes (11): Services, ping_redis(), _authorized(), _check_database(), _check_redis(), health_live(), health_ready(), HealthResponse (+3 more)

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

### Community 27 - "RedisLinkCache"
Cohesion: 0.16
Nodes (5): _CacheRead, _entry_from_link(), RedisLinkCache, CacheEntry, CacheUnavailable

### Community 28 - "click.py"
Cohesion: 0.15
Nodes (12): _browser(), extract_referrer_host(), normalize_country(), parse_user_agent(), UserAgentInfo, ClickPublisher, RecordClick, get_record_click() (+4 more)

### Community 29 - "create_link"
Cohesion: 0.18
Nodes (13): CurrentUser, get_current_user(), create_link(), get_link(), _link_response(), links_overview(), list_links(), update_link() (+5 more)

### Community 30 - "test_links_application.py"
Cohesion: 0.14
Nodes (24): CreateLinkCommand, UpdateLinkCommand, build_create(), build_link(), FakeCache, FakeClock, FakeGenerator, FakeQuota (+16 more)

### Community 31 - "ref_next_intl"
Cohesion: 0.08
Nodes (46): AccountPage(), AccountPageProps, generateMetadata(), dynamic, generateMetadata(), inter, jakarta, LocaleLayout() (+38 more)

### Community 32 - "test_identity_application.py"
Cohesion: 0.12
Nodes (24): LoginCommand, IssuedAccessToken, build_issuer(), build_login(), build_register(), FakeAccessTokens, FakeClock, FakeHasher (+16 more)

### Community 33 - "value_objects.py"
Cohesion: 0.18
Nodes (5): ReservedAliasError, HostResolver, _normalize_own_host(), _normalize_host(), _validate_hostname()

### Community 34 - "test_links_repository.py"
Cohesion: 0.47
Nodes (6): admin_settings(), build_link(), cleanup(), seed_user(), test_repository_crud_list_search_and_owner_filter(), test_repository_returns_none_for_non_owned_management_reads()

### Community 35 - "SqlAlchemyLinkRepository"
Cohesion: 0.12
Nodes (11): set_rls_context(), SqlAlchemyLinkRepository, EmptyResolver, SequenceGenerator, test_real_integrity_error_triggers_code_retry(), run(), admin_settings(), make_link() (+3 more)

### Community 36 - "account-form.tsx"
Cohesion: 0.09
Nodes (33): AccountForm(), handleError(), handleLocaleChange(), handleProfileSubmit(), handleThemeChange(), AccountFormProps, Notice, FieldError (+25 more)

### Community 37 - "build_services"
Cohesion: 0.13
Nodes (15): AuthSession, InvalidGoogleLogin, SessionExpired, LoginWithGoogle, Logout, Clock, RotationStatus, SessionRepository (+7 more)

### Community 38 - "identity/presentation/router.py"
Cohesion: 0.19
Nodes (16): _client_ip(), csrf_token(), login(), logout(), me(), refresh(), register(), update_me() (+8 more)

### Community 39 - "create_link.py"
Cohesion: 0.17
Nodes (17): CreateLink, AliasReserved, AliasTaken, CodeGenerationFailed, DailyQuotaExceeded, InvalidAlias, InvalidExpiresAt, InvalidTitle (+9 more)

### Community 40 - "test_identity_adapters.py"
Cohesion: 0.15
Nodes (7): build_session(), fast_hasher(), test_argon2_hasher_roundtrip_and_dummy(), test_cookie_prefix_disabled_when_domain_is_set(), test_cookies_are_httponly_except_csrf_and_samesite_lax(), test_google_exchange_never_decodes_an_unverified_id_token(), test_production_cookies_use_host_prefix_and_secure()

### Community 41 - "build_services"
Cohesion: 0.10
Nodes (10): AnalyticsServices, build_services(), IdentityServices, LinkServices, _own_hosts(), RedisDailyQuota, _seconds_until_next_utc_day(), QuotaResult (+2 more)

### Community 42 - "create_link_rate_limit"
Cohesion: 0.20
Nodes (16): _rate_limit_error(), user_rate_limit(), dependency(), _headers(), apply_rate_limit_headers(), client_ip(), _get_limiter(), rate_limit() (+8 more)

### Community 43 - "ShortCode"
Cohesion: 0.11
Nodes (13): _escape_like(), _to_domain(), DeleteLink, LinkNotFound, GetLink, Link, InvalidShortCodeError, ShortCode (+5 more)

### Community 44 - "LinkRepository"
Cohesion: 0.10
Nodes (16): ResolvedLink, _Unset, GetLinksOverview, LinksOverview, Clock, DailyQuota, LinkCache, LinkRepository (+8 more)

### Community 45 - "config.py"
Cohesion: 0.19
Nodes (14): get_settings(), test_database_ping_and_unit_of_work(), test_unit_of_work_rolls_back_on_error(), test_cleanup_retention_is_configurable(), test_development_enables_docs(), test_get_settings_is_cached(), test_misspelled_postgres_scheme_is_normalized(), test_postgres_urls_are_normalized_for_asyncpg() (+6 more)

### Community 46 - "create_app"
Cohesion: 0.07
Nodes (63): create_app(), test_health_ready_checks_postgres_and_redis(), admin_settings(), cleanup(), run(), FakeGoogleOIDC, google_claims(), identity_settings() (+55 more)

### Community 47 - "list_links.py"
Cohesion: 0.22
Nodes (9): LinkPage, InvalidCursor, InvalidPagination, ListLinks, _normalize_query(), decode_cursor(), encode_cursor(), PageCursor (+1 more)

### Community 48 - "register.py"
Cohesion: 0.18
Nodes (9): RegisterCommand, AuthLocked, InvalidCredentials, InvalidEmail, WeakPassword, Login, AuthThrottle, PasswordHasher (+1 more)

### Community 49 - "links-view.tsx"
Cohesion: 0.11
Nodes (27): LinksLoading(), CopyLinkButton(), LinksSkeleton(), LinksSkeletonProps, LinkCard(), LinksView(), confirmDelete(), handleSave() (+19 more)

### Community 50 - "ref_next_intl"
Cohesion: 0.11
Nodes (26): LinkDetailError(), LocaleNotFound(), BrandLogo(), Footer(), ControlVisual(), FeatureBlocks(), ShortLinkVisual(), StatsVisual() (+18 more)

### Community 51 - "api.ts"
Cohesion: 0.14
Nodes (21): ApiError, apiErrorFromResponse(), ApiErrorPayload, ApiRequestOptions, AuthResponseDto, CSRF_COOKIES, ensureCsrfToken(), fetchCsrfToken() (+13 more)

### Community 52 - "adapters/tokens.py"
Cohesion: 0.27
Nodes (4): PyJwtAccessTokens, AccessClaims, test_access_jwt_contains_minimal_claims_and_validates(), test_expired_access_token_is_rejected()

### Community 53 - "google_callback"
Cohesion: 0.24
Nodes (5): GoogleOIDCClient, google_callback(), _google_error_redirect(), google_login(), frontend_url()

### Community 54 - "RefreshTokenRecord"
Cohesion: 0.38
Nodes (3): _as_utc(), RefreshTokenRecord, test_refresh_record_handles_naive_datetimes()

### Community 55 - "register.py"
Cohesion: 0.11
Nodes (22): Email, InvalidEmailError, InvalidGoogleIdentityError, WeakPasswordError, _display_name(), _number(), _string(), validate_google_claims() (+14 more)

### Community 56 - "config.py"
Cohesion: 0.14
Nodes (9): unit_of_work(), record_cache_hit(), record_cache_miss(), record_circuit_state(), record_click_dropped(), record_clicks_flushed(), record_rate_limit_fallback(), record_rate_limited() (+1 more)

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
Cohesion: 0.12
Nodes (8): SqlAlchemyUserRepository, _to_user(), AuthenticateAccess, GetMe, AccessTokenIssuer, UserRepository, User, DuplicateUserError

### Community 62 - "sqlalchemy"
Cohesion: 0.13
Nodes (4): upgrade(), SqlAlchemyStatsRepository, RawStats, _is_code_conflict()

### Community 63 - "create.js"
Cohesion: 0.21
Nodes (10): create(), created, createDuration, createLink(), createWithSharedIp(), options, otherStatuses, rateLimited (+2 more)

### Community 64 - "ref_vitest"
Cohesion: 0.11
Nodes (12): ExternalLink(), ExternalLinkProps, items, authState, renderForm(), authState, navigation, renderNavbar() (+4 more)

### Community 65 - "OriginalUrl"
Cohesion: 0.25
Nodes (12): OriginalUrl, test_link_state_accounts_for_expiry_and_active_flag(), test_link_with_updates_returns_a_new_entity(), test_original_url_keeps_ipv6_literal_brackets(), test_original_url_normalizes_idn_to_punycode(), test_original_url_normalizes_scheme_host_and_idn(), test_original_url_rejects_invalid_host_shapes(), test_original_url_rejects_malformed_or_dangerous_values() (+4 more)

### Community 66 - "[locale]/page.tsx"
Cohesion: 0.07
Nodes (32): dynamic, GET(), generateMetadata(), HomePage(), HomePageProps, sitemap(), BackToTop(), MockIntersectionObserver (+24 more)

### Community 67 - "test_links_api.py"
Cohesion: 0.34
Nodes (13): api_settings(), cleanup(), direct_link(), seed_click(), seed_links(), seed_user(), test_anonymous_create_and_redirect(), test_create_rate_limit_returns_429() (+5 more)

### Community 68 - "pytest"
Cohesion: 0.34
Nodes (13): operation(), InvalidUrlError, policy(), test_credentials_controls_and_backslashes_are_blocked(), test_dns_rebinding_mixed_answers_are_all_checked(), test_forbidden_schemes_and_scheme_relative_urls_are_blocked(), test_global_ipv4_and_ipv6_answers_are_accepted(), test_obfuscated_or_internal_hostnames_are_blocked() (+5 more)

### Community 69 - "test_redirect_click_failure.py"
Cohesion: 0.26
Nodes (5): BlockingPublisher, click_settings(), DownRedis, test_redirect_continues_and_metric_counts_dropped_click(), test_redirect_does_not_wait_for_click_publisher()

### Community 71 - "test_body_limit.py"
Cohesion: 0.33
Nodes (5): build_app(), test_accepts_body_at_limit(), test_invalid_content_length_is_rejected(), test_rejects_chunked_body_above_limit(), test_rejects_content_length_above_limit_before_reading()

### Community 72 - "test_url_policy.py"
Cohesion: 0.24
Nodes (13): is_blocked_ip(), build_policy(), test_is_blocked_ip_allows_only_global_addresses(), test_is_blocked_ip_blocks_non_global_addresses(), test_url_policy_accepts_public_urls(), test_url_policy_blocks_host_when_resolution_fails_or_is_empty(), test_url_policy_blocks_invalid_dns_answer(), test_url_policy_blocks_own_domain_and_subdomains_without_dns() (+5 more)

### Community 73 - "request_context.py"
Cohesion: 0.22
Nodes (3): _incoming_request_id(), RequestIDMiddleware, send_with_request_id()

### Community 74 - "security.py"
Cohesion: 0.24
Nodes (9): InvalidNextPath, allowed_origins(), csrf_protect(), origin_guard(), safe_next_path(), validate_origin(), CsrfError, test_safe_next_accepts_internal_paths() (+1 more)

### Community 75 - "token_bucket.js"
Cohesion: 0.24
Nodes (8): headers(), negative(), notFound, options, rateLimited, redirect(), stampede(), §1 Token Bucket

### Community 76 - "error_handlers.py"
Cohesion: 0.12
Nodes (13): install_error_handlers(), handle_app_error(), handle_http_exception(), handle_unexpected_error(), handle_validation_error(), _json_error(), error_payload(), build_app() (+5 more)

### Community 77 - "get_services"
Cohesion: 0.37
Nodes (9): get_authenticate_access(), get_get_me(), get_google_login(), get_google_oidc(), get_login(), get_logout(), get_refresh_session(), get_register() (+1 more)

### Community 79 - "redirect.js"
Cohesion: 0.13
Nodes (15): CODE_TTL_SECONDS, cold(), COLD_CODES, createIp(), options, otherStatuses, rateLimited, redirectDuration (+7 more)

### Community 80 - "config.py"
Cohesion: 0.18
Nodes (11): _asyncpg_url(), _boolean(), _env(), get_migration_database_url(), _integer(), _number(), SettingsError, _text() (+3 more)

### Community 81 - "proxy.ts"
Cohesion: 0.33
Nodes (8): buildCspHeader(), CspOptions, securityHeaders(), config, createNonce(), intlMiddleware, proxy(), REFRESH_COOKIES

### Community 82 - "redis_client"
Cohesion: 0.22
Nodes (3): close_redis(), redis_client(), redis_client()

### Community 83 - "helpers.py"
Cohesion: 0.22
Nodes (13): AllowedQuota, acleanup(), acleanup_email(), admin_settings(), aseed_click(), aseed_link(), aseed_user(), expires_in() (+5 more)

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
Cohesion: 0.23
Nodes (9): nextConfig, withNextIntl, buildRewrites(), isShortCodePath(), RESERVED_PATTERN, RESERVED_TOP_LEVEL, RewriteRule, RewritesConfig (+1 more)

### Community 91 - "Settings"
Cohesion: 0.29
Nodes (6): Settings, generate_csrf_token(), clear_session_cookies(), set_csrf_cookie(), set_session_cookies(), test_clear_cookies_deletes_all_session_cookies()

### Community 92 - "identity/adapters/repository.py"
Cohesion: 0.42
Nodes (4): RefreshToken, _revoke_family(), SqlAlchemySessionRepository, RotationResult

### Community 94 - "db/models.py"
Cohesion: 0.15
Nodes (11): Base, ClickEvent, Link, User, CleanupResult, _delete_batch(), run_cleanup(), test_cleanup_deletes_old_clicks_and_expired_links_idempotently() (+3 more)

### Community 95 - "test_sentry.py"
Cohesion: 0.38
Nodes (3): test_sentry_is_disabled_without_a_dsn(), fake_init(), test_sentry_scrubs_request_data_and_disables_pii()

### Community 96 - ".__init__"
Cohesion: 0.07
Nodes (10): GoogleNotConfigured, AppError, BadRequestError, ConflictError, GatewayTimeoutError, NotFoundError, PayloadTooLargeError, ServiceUnavailableError (+2 more)

### Community 98 - "Auditoria de segurança — P09"
Cohesion: 0.18
Nodes (10): Achados residuais aceitos (com justificativa), Auditoria de segurança — P09, Como reproduzir, Conclusão, Configuração de produção, O que não foi possível testar / limitações honestas, Resumo executivo, RLS — prova independente (+2 more)

### Community 99 - "env.py"
Cohesion: 0.32
Nodes (3): do_run_migrations(), run_async_migrations(), run_migrations_online()

### Community 100 - "jittered_ttl"
Cohesion: 0.48
Nodes (3): jittered_ttl(), test_jittered_ttl_edge_cases(), test_jittered_ttl_stays_within_configured_range()

### Community 101 - "HostResolutionError"
Cohesion: 0.19
Nodes (4): SystemHostResolver, HostResolutionError, FakeResolver, FakeResolver

### Community 102 - "CacheClient"
Cohesion: 0.13
Nodes (5): CacheClient, FakeRedis, _sample(), test_cache_get_records_hit_and_miss(), test_cache_set_validates_ttl_and_delete()

### Community 104 - "Auditoria item a item — SECURITY.md"
Cohesion: 0.22
Nodes (9): test_only_config_module_reads_process_environment(), §10 Supply chain, §2 Resiliência / anti-DDoS, §3 Anti SQL Injection, §4 Anti XSS / injeção no front, §7 Credenciais e exposição, §8 Buffer overflow / limites, §9 SEO hijacking / indexação (+1 more)

### Community 105 - "RateLimiter"
Cohesion: 0.08
Nodes (9): get_rate_limiter(), GlobalRateLimitMiddleware, send_with_headers(), RateLimiter, DownRedis, test_global_bucket_is_shared_across_clients(), test_spoofed_xff_cannot_bypass_rate_limit(), DownRedis (+1 more)

### Community 106 - "update_me.py"
Cohesion: 0.46
Nodes (5): UpdateMeCommand, InvalidProfile, _normalize_display_name(), _normalize_locale(), UpdateMe

### Community 107 - "redirect_link"
Cohesion: 0.29
Nodes (3): delete_link(), redirect_link(), _static_html()

### Community 108 - "opengraph-image.tsx"
Cohesion: 0.40
Nodes (3): alt, contentType, size

## Knowledge Gaps
- **18 isolated node(s):** `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching`, `lucide-react 1.60.0`, `minimumReleaseAgeExclude Policy` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 502 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `test_link_cache.py`, `Database`, `ClickFlusher`, `links/presentation/router.py`, `database.py`, `CircuitBreaker`, `stats_cache.py`, `http.py`, `RedisLinkCache`, `create_link`, `test_links_repository.py`, `SqlAlchemyLinkRepository`, `test_identity_adapters.py`, `build_services`, `create_link_rate_limit`, `ShortCode`, `config.py`, `create_app`, `adapters/tokens.py`, `google_callback`, `config.py`, `logging.py`, `BucketPolicy`, `test_links_api.py`, `test_redirect_click_failure.py`, `security.py`, `get_services`, `config.py`, `redis_client`, `helpers.py`, `Bulkhead`, `Deploy — Vercel (web) + Render (API/Postgres/Redis)`, `sentry.py`, `db/models.py`, `test_sentry.py`, `Auditoria de segurança — P09`, `Auditoria item a item — SECURITY.md`?**
  _High betweenness centrality (0.248) - this node is a cross-community bridge._
- **Are the 107 inferred relationships involving `Settings` (e.g. with `settings_dependency()` and `configure_logging()`) actually correct?**
  _`Settings` has 107 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `shorten-form.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.11931818181818182 - nodes in this community are weakly interconnected._
- **Why does `§4 Anti XSS / injeção no front` connect `Auditoria item a item — SECURITY.md` to `proxy.ts`, `create_app`?**
  _High betweenness centrality (0.150) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `ShortCode` (e.g. with `GetLinkStats` and `RedisLinkCache`) actually correct?**
  _`ShortCode` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Should `Database` be split into smaller, more focused modules?**
  _Cohesion score 0.11428571428571428 - nodes in this community are weakly interconnected._