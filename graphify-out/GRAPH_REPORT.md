# Graph Report - Tricolink  (2026-10-23)

## Corpus Check
- 285 files · ~141,563 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: (none) 10, .toml 1, .ini 1)

## Summary
- 2289 nodes · 6987 edges · 107 communities (95 shown, 12 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 957 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e23c17f2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tricolink URL Shortener Product
- Token Bucket Rate Limiting
- test_link_cache.py
- SqlAlchemyLinkRepository
- Agent Workflow and Graphify
- Compose and P01 Infra
- test_real_integrity_error_triggers_code_retry
- test_real_ip.py
- MemoryTokenBucket
- ClickFlusher
- BodyLimitMiddleware
- httpx
- pnpm Release Policy
- PostCSS Tooling
- AppError
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
- update_link.py
- test_links_repository.py
- identity/adapters/repository.py
- account-form.tsx
- build_services
- identity/presentation/router.py
- create_link.py
- GlobalRateLimitMiddleware
- build_services
- create_link_rate_limit
- ShortCode
- resolve_link.py
- config.py
- create_app
- list_links.py
- register.py
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
- sqlalchemy
- analytics/presentation/router.py
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
- build_app
- error_handlers.py
- get_services
- redirect.js
- config.py
- links/adapters/repository.py
- redis_client
- Database
- Bulkhead
- Deploy — Vercel (web) + Render (API/Postgres/Redis)
- Resultados
- i18n-check.mjs
- CodeGenerator
- proxy.ts
- Settings
- Clock
- main.py
- db/models.py
- test_sentry.py
- .__init__
- Argon2PasswordHasher
- Auditoria de segurança — P09
- env.py
- jittered_ttl
- HostResolutionError
- CacheClient
- test_redirect_stampede.py
- starlette_types
- test_rate_limit_dependency_sets_headers_and_429
- BulkheadFullError

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

## Communities (107 total, 12 thin omitted)

### Community 0 - "Tricolink URL Shortener Product"
Cohesion: 0.25
Nodes (8): click_events Table, Redis Stream Click Buffer, Non-Goals, Tricolink URL Shortener Product, Redirect and Cache Hot Path, URL Anti-Abuse Policy, SSRF Prevention, Design Tokens

### Community 1 - "Token Bucket Rate Limiting"
Cohesion: 0.24
Nodes (9): Daily Link Quotas, Negative Cache for Unknown Codes, Single-Flight Lock, Stale-While-Revalidate Caching, Brute Force Protection, Bulkhead Semaphores, Circuit Breaker, Rate Limit Buckets (+1 more)

### Community 2 - "test_link_cache.py"
Cohesion: 0.30
Nodes (11): _async_link(), cache_settings(), cleanup(), make_link(), test_cold_stampede_uses_one_database_query(), loader(), test_invalidation_during_a_stale_refresh_cannot_repopulate_the_cache(), test_invalidation_forces_the_next_read_to_use_the_loader() (+3 more)

### Community 3 - "SqlAlchemyLinkRepository"
Cohesion: 0.30
Nodes (12): RedisClickPublisher, SqlAlchemyLinkRepository, admin_settings(), DownRedis, make_link(), pipeline_settings(), test_flusher_persists_batch_and_increments_click_count(), test_flusher_recreates_the_group_after_the_stream_is_lost() (+4 more)

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
Cohesion: 0.14
Nodes (8): _forwarded_for(), RealIPMiddleware, resolve_real_ip(), _NeverRedis, test_middleware_sets_request_client_to_real_ip(), test_resolve_real_ip_counts_from_the_right(), test_resolve_real_ip_falls_back_when_header_is_invalid_or_short(), test_resolve_real_ip_without_trusted_proxies_ignores_header()

### Community 8 - "MemoryTokenBucket"
Cohesion: 0.15
Nodes (11): get_rate_limiter(), MemoryTokenBucket, RateLimiter, test_spoofed_xff_cannot_bypass_rate_limit(), DownRedis, FakeClock, test_memory_bucket_consumes_and_exhausts(), test_memory_bucket_never_exceeds_capacity() (+3 more)

### Community 9 - "ClickFlusher"
Cohesion: 0.16
Nodes (5): ClickFlusher, read_group(), guarded(), operation(), guarded()

### Community 10 - "BodyLimitMiddleware"
Cohesion: 0.26
Nodes (3): BodyLimitMiddleware, _header_values(), _send_json()

### Community 11 - "httpx"
Cohesion: 0.35
Nodes (7): build_inner(), test_hsts_only_in_production(), test_request_id_accepts_only_safe_values(), test_request_id_is_generated_and_returned(), test_security_headers_are_added(), test_timeout_allows_fast_requests(), test_timeout_returns_504()

### Community 15 - "AppError"
Cohesion: 0.17
Nodes (7): AppError, BadRequestError, ConflictError, GatewayTimeoutError, PayloadTooLargeError, ServiceUnavailableError, MetricsAuthenticationError

### Community 19 - "CircuitBreaker"
Cohesion: 0.05
Nodes (13): CircuitBreaker, CircuitState, _digest(), RedisAuthThrottle, guarded(), operation(), ThrottleResult, CircuitOpenError (+5 more)

### Community 20 - "stats_cache.py"
Cohesion: 0.09
Nodes (34): _breakdown(), _deserialize(), RedisStatsCache, _serialize(), BreakdownItem, build_stats(), build_window(), fill_series() (+26 more)

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

### Community 27 - "RedisLinkCache"
Cohesion: 0.21
Nodes (4): _CacheRead, _entry_from_link(), RedisLinkCache, CacheEntry

### Community 28 - "click.py"
Cohesion: 0.12
Nodes (15): record_clicks_flushed(), _parse_event(), _browser(), ClickEvent, extract_referrer_host(), normalize_country(), parse_user_agent(), UserAgentInfo (+7 more)

### Community 29 - "create_link"
Cohesion: 0.11
Nodes (23): CurrentUser, get_click_publisher(), get_create_link(), get_delete_link(), get_get_link(), get_links_overview(), get_list_links(), get_resolve_link() (+15 more)

### Community 30 - "test_links_application.py"
Cohesion: 0.12
Nodes (25): CreateLinkCommand, UpdateLinkCommand, build_create(), build_link(), FakeCache, FakeClock, FakeGenerator, FakePublisher (+17 more)

### Community 31 - "ref_next_intl"
Cohesion: 0.12
Nodes (34): AccountPage(), AccountPageProps, generateMetadata(), generateMetadata(), LinkDetailPage(), LinkDetailPageProps, generateMetadata(), LinksPage() (+26 more)

### Community 32 - "test_identity_application.py"
Cohesion: 0.12
Nodes (24): LoginCommand, RegisterCommand, build_issuer(), build_login(), build_register(), FakeAccessTokens, FakeClock, FakeHasher (+16 more)

### Community 33 - "update_link.py"
Cohesion: 0.14
Nodes (8): _normalize_expiry(), normalize_expires_at(), validate_url(), ReservedAliasError, HostResolver, is_blocked_ip(), _normalize_own_host(), UrlPolicy

### Community 34 - "test_links_repository.py"
Cohesion: 0.42
Nodes (6): admin_settings(), build_link(), cleanup(), seed_user(), test_repository_crud_list_search_and_owner_filter(), test_repository_returns_none_for_non_owned_management_reads()

### Community 35 - "identity/adapters/repository.py"
Cohesion: 0.12
Nodes (9): set_rls_context(), _revoke_family(), SqlAlchemySessionRepository, RotationResult, RotationStatus, admin_settings(), make_link(), make_user() (+1 more)

### Community 36 - "account-form.tsx"
Cohesion: 0.12
Nodes (26): AccountForm(), handleError(), handleLocaleChange(), handleProfileSubmit(), handleThemeChange(), AccountFormProps, Notice, FieldError (+18 more)

### Community 37 - "build_services"
Cohesion: 0.11
Nodes (11): AuthenticateAccess, SessionExpired, GetMe, Logout, AccessTokenIssuer, Clock, SessionRepository, UserRepository (+3 more)

### Community 38 - "identity/presentation/router.py"
Cohesion: 0.23
Nodes (16): _client_ip(), csrf_token(), login(), logout(), me(), refresh(), register(), update_me() (+8 more)

### Community 39 - "create_link.py"
Cohesion: 0.26
Nodes (10): CreateLink, AliasReserved, AliasTaken, CodeGenerationFailed, DailyQuotaExceeded, InvalidAlias, InvalidTitle, LoginRequired (+2 more)

### Community 40 - "GlobalRateLimitMiddleware"
Cohesion: 0.22
Nodes (3): GlobalRateLimitMiddleware, send_with_headers(), _headers()

### Community 41 - "build_services"
Cohesion: 0.08
Nodes (14): AnalyticsServices, build_services(), IdentityServices, LinkServices, _own_hosts(), RedisDailyQuota, GetLinkStats, load() (+6 more)

### Community 42 - "create_link_rate_limit"
Cohesion: 0.21
Nodes (15): _rate_limit_error(), user_rate_limit(), dependency(), apply_rate_limit_headers(), client_ip(), _get_limiter(), rate_limit(), dependency() (+7 more)

### Community 43 - "ShortCode"
Cohesion: 0.12
Nodes (12): DeleteLink, LinkNotFound, GetLink, DailyQuota, LinkCache, LinkRepository, UpdateLink, Link (+4 more)

### Community 44 - "resolve_link.py"
Cohesion: 0.19
Nodes (10): ResolvedLink, _Unset, CacheUnavailable, _as_utc(), _entry_state(), _resolved_from_cache(), _resolved_from_link(), ResolveLink (+2 more)

### Community 45 - "config.py"
Cohesion: 0.21
Nodes (17): get_settings(), Settings, test_database_ping_and_unit_of_work(), test_unit_of_work_rolls_back_on_error(), test_health_ready_checks_postgres_and_redis(), test_cleanup_retention_is_configurable(), test_development_enables_docs(), test_get_settings_is_cached() (+9 more)

### Community 46 - "create_app"
Cohesion: 0.08
Nodes (67): create_app(), admin_settings(), cleanup(), run(), FakeGoogleOIDC, google_claims(), identity_settings(), login() (+59 more)

### Community 47 - "list_links.py"
Cohesion: 0.22
Nodes (9): LinkPage, InvalidCursor, InvalidPagination, ListLinks, _normalize_query(), decode_cursor(), encode_cursor(), PageCursor (+1 more)

### Community 48 - "register.py"
Cohesion: 0.13
Nodes (13): AuthLocked, InvalidCredentials, InvalidEmail, WeakPassword, Login, AuthThrottle, PasswordHasher, Register (+5 more)

### Community 49 - "links-view.tsx"
Cohesion: 0.07
Nodes (42): LinkDetailError(), LinksLoading(), LocaleNotFound(), CopyLinkButton(), CopyLinkButtonProps, DeleteLinkDialog(), DeleteLinkDialogProps, EditErrors (+34 more)

### Community 50 - "ref_next_intl"
Cohesion: 0.09
Nodes (30): dynamic, GET(), dynamic, generateMetadata(), inter, jakarta, LocaleLayout(), LocaleLayoutProps (+22 more)

### Community 51 - "api.ts"
Cohesion: 0.10
Nodes (28): navigation, renderForm(), user, api, ApiError, apiErrorFromResponse(), ApiErrorPayload, ApiRequestOptions (+20 more)

### Community 52 - "adapters/tokens.py"
Cohesion: 0.27
Nodes (5): PyJwtAccessTokens, AccessClaims, IssuedAccessToken, test_access_jwt_contains_minimal_claims_and_validates(), test_expired_access_token_is_rejected()

### Community 53 - "google_callback"
Cohesion: 0.18
Nodes (5): GoogleOIDCClient, google_callback(), _google_error_redirect(), google_login(), frontend_url()

### Community 54 - "identity/domain/entities.py"
Cohesion: 0.17
Nodes (10): AuthSession, InvalidGoogleLogin, LoginWithGoogle, SessionIssuer, _as_utc(), RefreshTokenRecord, TokenFamily, GoogleIdentity (+2 more)

### Community 55 - "register.py"
Cohesion: 0.15
Nodes (18): InvalidGoogleIdentityError, _display_name(), _number(), _string(), validate_google_claims(), google_claims(), test_email_is_nfkc_normalized_and_lowercased(), test_email_rejects_invalid_values() (+10 more)

### Community 56 - "config.py"
Cohesion: 0.11
Nodes (10): ping_redis(), unit_of_work(), record_cache_hit(), record_cache_miss(), record_circuit_state(), record_click_dropped(), record_rate_limit_fallback(), record_rate_limited() (+2 more)

### Community 57 - "logging.py"
Cohesion: 0.14
Nodes (6): configure_logging(), get_logger(), MetricsMiddleware, _route_path(), record_request(), lifespan()

### Community 59 - ".__call__"
Cohesion: 0.29
Nodes (4): replay_body(), run(), tracked_send(), receive()

### Community 60 - "BucketPolicy"
Cohesion: 0.14
Nodes (10): _BucketState, _reset_seconds(), BucketPolicy, build_policies(), RedisTokenBucket, _reset_seconds(), TokenBucketBackend, test_lua_bucket_consumes_exhausts_and_refills() (+2 more)

### Community 61 - "User"
Cohesion: 0.15
Nodes (8): SqlAlchemyUserRepository, _to_user(), UpdateMeCommand, InvalidProfile, _normalize_display_name(), _normalize_locale(), UpdateMe, User

### Community 62 - "sqlalchemy"
Cohesion: 0.20
Nodes (3): upgrade(), SqlAlchemyStatsRepository, RawStats

### Community 63 - "analytics/presentation/router.py"
Cohesion: 0.23
Nodes (5): get_current_user(), link_stats(), LinkStatsResponse, StatsBreakdownResponse, StatsSeriesPointResponse

### Community 64 - "ref_vitest"
Cohesion: 0.06
Nodes (28): ExternalLink(), ExternalLinkProps, BackToTop(), MockIntersectionObserver, observers, renderBackToTop(), items, CopyState (+20 more)

### Community 65 - "OriginalUrl"
Cohesion: 0.23
Nodes (13): _as_utc(), OriginalUrl, test_link_state_accounts_for_expiry_and_active_flag(), test_link_with_updates_returns_a_new_entity(), test_original_url_keeps_ipv6_literal_brackets(), test_original_url_normalizes_idn_to_punycode(), test_original_url_normalizes_scheme_host_and_idn(), test_original_url_rejects_invalid_host_shapes() (+5 more)

### Community 66 - "[locale]/page.tsx"
Cohesion: 0.07
Nodes (34): generateMetadata(), HomePage(), HomePageProps, alt, contentType, size, sitemap(), Faq() (+26 more)

### Community 67 - "test_links_api.py"
Cohesion: 0.26
Nodes (16): api_settings(), cleanup(), direct_link(), seed_click(), run(), seed_links(), seed_user(), run() (+8 more)

### Community 68 - "pytest"
Cohesion: 0.37
Nodes (12): operation(), policy(), test_credentials_controls_and_backslashes_are_blocked(), test_dns_rebinding_mixed_answers_are_all_checked(), test_forbidden_schemes_and_scheme_relative_urls_are_blocked(), test_global_ipv4_and_ipv6_answers_are_accepted(), test_obfuscated_or_internal_hostnames_are_blocked(), test_own_domain_and_subdomains_are_blocked_as_redirect_loops() (+4 more)

### Community 69 - "test_redirect_click_failure.py"
Cohesion: 0.26
Nodes (5): BlockingPublisher, click_settings(), DownRedis, test_redirect_continues_and_metric_counts_dropped_click(), test_redirect_does_not_wait_for_click_publisher()

### Community 70 - ".__call__"
Cohesion: 0.18
Nodes (4): capture_status(), SecurityHeadersMiddleware, send_with_headers(), send()

### Community 71 - "test_body_limit.py"
Cohesion: 0.33
Nodes (5): build_app(), test_accepts_body_at_limit(), test_invalid_content_length_is_rejected(), test_rejects_chunked_body_above_limit(), test_rejects_content_length_above_limit_before_reading()

### Community 72 - "test_url_policy.py"
Cohesion: 0.29
Nodes (13): InvalidUrlError, build_policy(), test_is_blocked_ip_allows_only_global_addresses(), test_is_blocked_ip_blocks_non_global_addresses(), test_url_policy_accepts_public_urls(), test_url_policy_blocks_host_when_resolution_fails_or_is_empty(), test_url_policy_blocks_invalid_dns_answer(), test_url_policy_blocks_own_domain_and_subdomains_without_dns() (+5 more)

### Community 73 - "request_context.py"
Cohesion: 0.22
Nodes (3): _incoming_request_id(), RequestIDMiddleware, send_with_request_id()

### Community 74 - "security.py"
Cohesion: 0.24
Nodes (9): InvalidNextPath, allowed_origins(), csrf_protect(), origin_guard(), safe_next_path(), validate_origin(), CsrfError, test_safe_next_accepts_internal_paths() (+1 more)

### Community 75 - "build_app"
Cohesion: 0.24
Nodes (8): NotFoundError, build_app(), missing(), test_app_error_uses_standard_envelope(), test_security_error_uses_standard_envelope(), test_unhandled_error_does_not_leak_stack_trace(), test_unknown_route_uses_standard_envelope(), test_validation_error_uses_standard_envelope()

### Community 76 - "error_handlers.py"
Cohesion: 0.19
Nodes (7): install_error_handlers(), handle_app_error(), handle_http_exception(), handle_unexpected_error(), handle_validation_error(), _json_error(), error_payload()

### Community 77 - "get_services"
Cohesion: 0.23
Nodes (14): get_cache(), get_current_user_optional(), get_services(), get_session(), settings_dependency(), get_authenticate_access(), get_get_me(), get_google_login() (+6 more)

### Community 79 - "redirect.js"
Cohesion: 0.06
Nodes (33): headers(), negative(), notFound, options, rateLimited, redirect(), stampede(), §1 Token Bucket (+25 more)

### Community 80 - "config.py"
Cohesion: 0.21
Nodes (9): _asyncpg_url(), _boolean(), _env(), get_migration_database_url(), _integer(), _number(), SettingsError, _text() (+1 more)

### Community 81 - "links/adapters/repository.py"
Cohesion: 0.29
Nodes (3): _escape_like(), _is_code_conflict(), _to_domain()

### Community 82 - "redis_client"
Cohesion: 0.22
Nodes (3): close_redis(), redis_client(), redis_client()

### Community 83 - "Database"
Cohesion: 0.12
Nodes (17): create_redis(), Database, run(), run(), acleanup(), admin_settings(), aseed_click(), aseed_link() (+9 more)

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
Cohesion: 0.23
Nodes (6): CodeGenerator, _normalize_host(), _validate_hostname(), test_code_generator_can_be_made_deterministic(), test_code_generator_uses_seven_base62_characters(), test_code_generator_validates_configuration()

### Community 89 - "proxy.ts"
Cohesion: 0.14
Nodes (17): nextConfig, withNextIntl, buildRewrites(), isShortCodePath(), RESERVED_PATTERN, RESERVED_TOP_LEVEL, RewriteRule, RewritesConfig (+9 more)

### Community 91 - "Settings"
Cohesion: 0.12
Nodes (12): generate_csrf_token(), clear_session_cookies(), set_csrf_cookie(), set_session_cookies(), build_session(), fast_hasher(), test_argon2_hasher_roundtrip_and_dummy(), test_clear_cookies_deletes_all_session_cookies() (+4 more)

### Community 92 - "Clock"
Cohesion: 0.39
Nodes (3): GetLinksOverview, LinksOverview, Clock

### Community 93 - "main.py"
Cohesion: 0.10
Nodes (8): init_sentry(), _scrub_event(), test_metrics_accepts_valid_token(), test_metrics_rejects_wrong_token(), test_metrics_requires_token(), production_settings(), test_body_limit_is_enforced_by_the_full_app(), test_docs_and_openapi_are_disabled_in_production()

### Community 94 - "db/models.py"
Cohesion: 0.13
Nodes (14): Base, ClickEvent, Link, RefreshToken, User, CleanupResult, _delete_batch(), main() (+6 more)

### Community 95 - "test_sentry.py"
Cohesion: 0.38
Nodes (3): test_sentry_is_disabled_without_a_dsn(), fake_init(), test_sentry_scrubs_request_data_and_disables_pii()

### Community 96 - ".__init__"
Cohesion: 0.08
Nodes (4): GoogleNotConfigured, InvalidExpiresAt, UrlNotAllowed, AuthorizationError

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
Cohesion: 0.14
Nodes (5): CacheClient, FakeRedis, _sample(), test_cache_get_records_hit_and_miss(), test_cache_set_validates_ttl_and_delete()

### Community 103 - "test_redirect_stampede.py"
Cohesion: 0.38
Nodes (3): CountingRepository, NoopRecordClick, test_200_concurrent_cold_redirects_hit_the_database_once()

### Community 105 - "test_rate_limit_dependency_sets_headers_and_429"
Cohesion: 0.18
Nodes (4): DownRedis, test_global_bucket_is_shared_across_clients(), DownRedis, test_rate_limit_dependency_sets_headers_and_429()

## Knowledge Gaps
- **18 isolated node(s):** `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching`, `lucide-react 1.60.0`, `minimumReleaseAgeExclude Policy` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 502 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `config.py` to `test_link_cache.py`, `SqlAlchemyLinkRepository`, `test_real_integrity_error_triggers_code_retry`, `ClickFlusher`, `database.py`, `CircuitBreaker`, `stats_cache.py`, `http.py`, `RedisLinkCache`, `click.py`, `create_link`, `test_links_repository.py`, `identity/adapters/repository.py`, `identity/presentation/router.py`, `build_services`, `create_link_rate_limit`, `create_app`, `adapters/tokens.py`, `google_callback`, `config.py`, `logging.py`, `BucketPolicy`, `test_links_api.py`, `test_redirect_click_failure.py`, `security.py`, `get_services`, `config.py`, `redis_client`, `Database`, `Bulkhead`, `Deploy — Vercel (web) + Render (API/Postgres/Redis)`, `Settings`, `main.py`, `db/models.py`, `test_sentry.py`, `Auditoria de segurança — P09`, `test_redirect_stampede.py`?**
  _High betweenness centrality (0.264) - this node is a cross-community bridge._
- **Are the 106 inferred relationships involving `Settings` (e.g. with `settings_dependency()` and `configure_logging()`) actually correct?**
  _`Settings` has 106 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_real_ip.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1368421052631579 - nodes in this community are weakly interconnected._
- **Why does `§4 Anti XSS / injeção no front` connect `create_app` to `proxy.ts`?**
  _High betweenness centrality (0.145) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `ShortCode` (e.g. with `GetLinkStats` and `RedisLinkCache`) actually correct?**
  _`ShortCode` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Should `CircuitBreaker` be split into smaller, more focused modules?**
  _Cohesion score 0.054098360655737705 - nodes in this community are weakly interconnected._