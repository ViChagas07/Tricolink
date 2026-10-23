# Graph Report - Tricolink  (2026-10-23)

## Corpus Check
- 294 files · ~147,445 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: (none) 10, .toml 1, .ini 1)

## Summary
- 2381 nodes · 7304 edges · 106 communities (91 shown, 15 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 990 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bfd421da`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tricolink URL Shortener Product
- Token Bucket Rate Limiting
- identity/presentation/router.py
- shorten-form.tsx
- Agent Workflow and Graphify
- Compose and P01 Infra
- dataclasses
- create_link.py
- MemoryTokenBucket
- ClickFlusher
- BodyLimitMiddleware
- httpx
- pnpm Release Policy
- PostCSS Tooling
- login-form.tsx
- API Package
- test_link_cache.py
- Email
- stats_cache.py
- demo-dashboard.tsx
- deps.py
- SECURITY.md Security Requirements
- UI_SPEC.md Tricolink Interface
- Code Standards
- REST API /api/v1 Contract
- ShortCode
- click.py
- create_link
- test_links_application.py
- isLocale
- pytest
- deps.py
- AppError
- links/adapters/repository.py
- account-form.tsx
- build_services
- security.py
- CircuitBreaker
- .is_production
- build_services
- links/presentation/dependencies.py
- .from_env
- LinkRepository
- config.py
- create_app
- list_links.py
- register.py
- test_identity_adapters.py
- cn
- api.ts
- error_handlers.py
- links/domain/entities.py
- RefreshTokenRecord
- register.py
- asyncio
- test_real_integrity_error_triggers_code_retry
- ids.py
- test_click_pipeline.py
- uuid
- stats_repository.py
- identity/adapters/repository.py
- sentry.py
- ref_vitest
- value_objects.py
- cn
- test_links_api.py
- create_redis
- test_redirect_click_failure.py
- adapters/tokens.py
- build_app
- Bulkhead
- test_database_ready.py
- token_bucket.js
- request_context.py
- test_real_ip.py
- seo.ts
- redirect.js
- sqlalchemy
- theme-sync.tsx
- link_stats
- Database
- http.py
- Deploy — Vercel (web) + Render (API/Postgres/Redis)
- Resultados
- i18n-check.mjs
- test_global_bucket_is_shared_across_clients
- proxy.ts
- build_services
- test_stats_api.py
- RedisDailyQuota
- db/models.py
- test_sentry.py
- .__init__
- create.js
- jittered_ttl
- opengraph-image.tsx
- test_rate_limit_dependency_sets_headers_and_429
- Argon2PasswordHasher
- CacheClient
- test_database.py
- send
- User

## God Nodes (most connected - your core abstractions)
1. `Settings` - 154 edges
2. `ShortCode` - 95 edges
3. `Link` - 82 edges
4. `create_app()` - 64 edges
5. `build_services()` - 57 edges
6. `User` - 57 edges
7. `Database` - 47 edges
8. `AppError` - 44 edges
9. `UserRepository` - 43 edges
10. `cn()` - 40 edges

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

## Communities (106 total, 15 thin omitted)

### Community 0 - "Tricolink URL Shortener Product"
Cohesion: 0.25
Nodes (8): click_events Table, Redis Stream Click Buffer, Non-Goals, Tricolink URL Shortener Product, Redirect and Cache Hot Path, URL Anti-Abuse Policy, SSRF Prevention, Design Tokens

### Community 1 - "Token Bucket Rate Limiting"
Cohesion: 0.24
Nodes (9): Daily Link Quotas, Negative Cache for Unknown Codes, Single-Flight Lock, Stale-While-Revalidate Caching, Brute Force Protection, Bulkhead Semaphores, Circuit Breaker, Rate Limit Buckets (+1 more)

### Community 2 - "identity/presentation/router.py"
Cohesion: 0.14
Nodes (20): _client_ip(), csrf_token(), delete_my_avatar(), get_my_avatar(), login(), logout(), me(), refresh() (+12 more)

### Community 3 - "shorten-form.tsx"
Cohesion: 0.12
Nodes (23): CopyState, CreateLinkResponse, ERROR_KEYS, FormError, getOwnHosts(), ShortenForm(), handleSubmit(), handleUrlChange() (+15 more)

### Community 4 - "Agent Workflow and Graphify"
Cohesion: 0.18
Nodes (8): graphify Slash Command, Mandatory Session Reading Order, CONTEXT.md Single Source of Truth, Graphify Context Engineering, Graphify Installation Commands, Per-Phase Graphify Routine, graphify query/path/explain Workflow, Tricolink README Stub (P11)

### Community 5 - "Compose and P01 Infra"
Cohesion: 0.16
Nodes (20): pnpm allowBuilds Allowlist, API Compose Service, app Network, data Network, postgres_data Volume, PostgreSQL 16 Compose Service, Redis 7 Compose Service, Web Compose Service (+12 more)

### Community 6 - "dataclasses"
Cohesion: 0.16
Nodes (10): _headers(), record_rate_limit_fallback(), record_rate_limited(), _reset_seconds(), RateLimitResult, BucketPolicy, build_policies(), _reset_seconds() (+2 more)

### Community 7 - "create_link.py"
Cohesion: 0.19
Nodes (11): CreateLink, AliasReserved, AliasTaken, CodeGenerationFailed, DailyQuotaExceeded, InvalidAlias, LoginRequired, CodeGenerator (+3 more)

### Community 8 - "MemoryTokenBucket"
Cohesion: 0.22
Nodes (9): _BucketState, MemoryTokenBucket, DownRedis, FakeClock, test_memory_bucket_consumes_and_exhausts(), test_memory_bucket_never_exceeds_capacity(), test_memory_bucket_refills(), test_rate_limiter_falls_back_to_memory_when_redis_is_down() (+1 more)

### Community 9 - "ClickFlusher"
Cohesion: 0.13
Nodes (8): ClickFlusher, read_group(), guarded(), _parse_event(), operation(), guarded(), ClickEvent, FakePublisher

### Community 10 - "BodyLimitMiddleware"
Cohesion: 0.14
Nodes (10): BodyLimitMiddleware, replay_body(), _header_values(), _send_json(), build_app(), test_accepts_body_at_limit(), test_invalid_content_length_is_rejected(), receive() (+2 more)

### Community 11 - "httpx"
Cohesion: 0.17
Nodes (9): SecurityHeadersMiddleware, RequestTimeoutMiddleware, build_inner(), test_hsts_only_in_production(), test_request_id_accepts_only_safe_values(), test_request_id_is_generated_and_returned(), test_security_headers_are_added(), test_timeout_allows_fast_requests() (+1 more)

### Community 15 - "login-form.tsx"
Cohesion: 0.14
Nodes (23): first(), generateMetadata(), LoginPage(), LoginPageProps, FieldError, FieldErrors, FormError, LoginForm() (+15 more)

### Community 18 - "test_link_cache.py"
Cohesion: 0.20
Nodes (15): _async_link(), cache_settings(), cleanup(), make_link(), test_cold_stampede_uses_one_database_query(), loader(), test_invalidation_during_a_stale_refresh_cannot_repopulate_the_cache(), test_invalidation_forces_the_next_read_to_use_the_loader() (+7 more)

### Community 19 - "Email"
Cohesion: 0.20
Nodes (9): Email, InvalidEmailError, InvalidGoogleIdentityError, WeakPasswordError, _display_name(), _number(), _picture_url(), _string() (+1 more)

### Community 20 - "stats_cache.py"
Cohesion: 0.09
Nodes (25): _breakdown(), _deserialize(), RedisStatsCache, _serialize(), load(), RawStats, BreakdownItem, build_stats() (+17 more)

### Community 21 - "demo-dashboard.tsx"
Cohesion: 0.08
Nodes (37): BreakdownColumns, BreakdownRow, BreakdownTable(), BreakdownTableProps, ClicksChart(), ClicksChartProps, ClicksPoint, ChartPlaceholder() (+29 more)

### Community 22 - "deps.py"
Cohesion: 0.15
Nodes (15): get_cache(), get_current_user_optional(), get_rate_limiter(), get_session(), _rate_limit_error(), settings_dependency(), user_rate_limit(), dependency() (+7 more)

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
Cohesion: 0.14
Nodes (7): _CacheRead, _entry_from_link(), RedisLinkCache, CacheEntry, ShortCode, test_reserved_aliases_cover_application_routes(), test_reserved_aliases_are_case_insensitive()

### Community 28 - "click.py"
Cohesion: 0.27
Nodes (9): _browser(), extract_referrer_host(), normalize_country(), parse_user_agent(), UserAgentInfo, test_click_event_never_contains_raw_user_agent_or_ip(), test_extract_referrer_host(), test_normalize_country() (+1 more)

### Community 29 - "create_link"
Cohesion: 0.16
Nodes (16): CurrentUser, get_current_user(), create_link(), delete_link(), get_link(), _link_response(), links_overview(), list_links() (+8 more)

### Community 30 - "test_links_application.py"
Cohesion: 0.14
Nodes (23): CreateLinkCommand, build_create(), build_link(), FakeCache, FakeClock, FakeGenerator, FakeQuota, FakeRepository (+15 more)

### Community 31 - "isLocale"
Cohesion: 0.19
Nodes (19): AccountPage(), AccountPageProps, generateMetadata(), generateMetadata(), generateMetadata(), LinksPage(), LinksPageProps, isLocale() (+11 more)

### Community 32 - "pytest"
Cohesion: 0.06
Nodes (55): operation(), LoginCommand, RegisterCommand, IssuedAccessToken, HostResolutionError, is_blocked_ip(), FakeResolver, policy() (+47 more)

### Community 33 - "deps.py"
Cohesion: 0.38
Nodes (13): get_services(), get_authenticate_access(), get_get_avatar(), get_get_me(), get_google_login(), get_google_oidc(), get_login(), get_logout() (+5 more)

### Community 34 - "AppError"
Cohesion: 0.13
Nodes (10): AppError, BadRequestError, ConflictError, GatewayTimeoutError, PayloadTooLargeError, ServiceUnavailableError, AuthorizationError, BulkheadFullError (+2 more)

### Community 35 - "links/adapters/repository.py"
Cohesion: 0.17
Nodes (13): _escape_like(), _is_code_conflict(), SqlAlchemyLinkRepository, _to_domain(), PageCursor, run(), admin_settings(), build_link() (+5 more)

### Community 36 - "account-form.tsx"
Cohesion: 0.08
Nodes (33): AccountForm(), handleAvatarRemove(), handleAvatarSelected(), handleError(), handleLocaleChange(), handleProfileSubmit(), AccountFormProps, Notice (+25 more)

### Community 37 - "build_services"
Cohesion: 0.14
Nodes (14): AuthSession, InvalidGoogleLogin, LoginWithGoogle, Logout, AccessTokenIssuer, Clock, SessionRepository, RefreshSession (+6 more)

### Community 38 - "security.py"
Cohesion: 0.15
Nodes (14): GoogleOIDCClient, InvalidNextPath, google_callback(), _google_error_redirect(), google_login(), allowed_origins(), csrf_protect(), frontend_url() (+6 more)

### Community 39 - "CircuitBreaker"
Cohesion: 0.05
Nodes (14): record_circuit_state(), CircuitBreaker, CircuitState, _digest(), RedisAuthThrottle, guarded(), operation(), _retry_after() (+6 more)

### Community 41 - "build_services"
Cohesion: 0.22
Nodes (7): AnalyticsServices, build_services(), IdentityServices, LinkServices, _own_hosts(), SystemClock, utc_now()

### Community 42 - "links/presentation/dependencies.py"
Cohesion: 0.20
Nodes (12): create_link_rate_limit(), get_click_publisher(), get_create_link(), get_delete_link(), get_get_link(), get_links_overview(), get_list_links(), get_record_click() (+4 more)

### Community 43 - ".from_env"
Cohesion: 0.14
Nodes (19): get_settings(), Settings, create_engine(), create_session_factory(), test_health_ready_checks_postgres_and_redis(), test_cleanup_retention_is_configurable(), test_development_enables_docs(), test_get_settings_is_cached() (+11 more)

### Community 44 - "LinkRepository"
Cohesion: 0.10
Nodes (15): GetLinkStats, StatsCache, StatsRepository, DeleteLink, LinkNotFound, GetLink, GetLinksOverview, LinksOverview (+7 more)

### Community 45 - "config.py"
Cohesion: 0.21
Nodes (9): _asyncpg_url(), _boolean(), _env(), get_migration_database_url(), _integer(), _number(), SettingsError, _text() (+1 more)

### Community 46 - "create_app"
Cohesion: 0.05
Nodes (71): configure_logging(), get_logger(), MetricsMiddleware, _route_path(), record_request(), create_app(), lifespan(), admin_settings() (+63 more)

### Community 47 - "list_links.py"
Cohesion: 0.23
Nodes (8): LinkPage, InvalidCursor, InvalidPagination, ListLinks, _normalize_query(), decode_cursor(), encode_cursor(), test_cursor_roundtrip_and_rejection()

### Community 48 - "register.py"
Cohesion: 0.19
Nodes (8): AuthLocked, InvalidCredentials, InvalidEmail, WeakPassword, Login, AuthThrottle, PasswordHasher, Register

### Community 49 - "test_identity_adapters.py"
Cohesion: 0.10
Nodes (11): clear_session_cookies(), set_csrf_cookie(), set_session_cookies(), build_session(), fast_hasher(), test_argon2_hasher_roundtrip_and_dummy(), test_clear_cookies_deletes_all_session_cookies(), test_cookie_prefix_disabled_when_domain_is_set() (+3 more)

### Community 50 - "cn"
Cohesion: 0.12
Nodes (22): LocaleLayout(), LinkDetailError(), LocaleNotFound(), BrandLogo(), Footer(), FinalCta(), LanguageSwitcher(), handleListKeyDown() (+14 more)

### Community 51 - "api.ts"
Cohesion: 0.12
Nodes (24): navigation, user, api, ApiError, apiErrorFromResponse(), ApiErrorPayload, ApiRequestOptions, AuthResponseDto (+16 more)

### Community 52 - "error_handlers.py"
Cohesion: 0.19
Nodes (7): install_error_handlers(), handle_app_error(), handle_http_exception(), handle_unexpected_error(), handle_validation_error(), _json_error(), error_payload()

### Community 53 - "links/domain/entities.py"
Cohesion: 0.20
Nodes (9): ResolvedLink, _Unset, _as_utc(), _entry_state(), _resolved_from_cache(), _resolved_from_link(), _as_utc(), LinkState (+1 more)

### Community 54 - "RefreshTokenRecord"
Cohesion: 0.29
Nodes (4): _as_utc(), RefreshTokenRecord, test_refresh_record_handles_naive_datetimes(), test_token_family_and_refresh_record_lifecycle()

### Community 55 - "register.py"
Cohesion: 0.20
Nodes (14): PasswordPolicy, google_claims(), test_email_is_nfkc_normalized_and_lowercased(), test_email_rejects_invalid_values(), test_email_rejects_non_string_and_too_long(), test_google_claims_accept_audience_list_and_string_verified(), test_google_claims_reject_untrusted_values(), test_google_claims_require_nonce() (+6 more)

### Community 56 - "asyncio"
Cohesion: 0.16
Nodes (6): ping_redis(), unit_of_work(), record_cache_hit(), record_cache_miss(), record_click_dropped(), record_clicks_flushed()

### Community 57 - "test_real_integrity_error_triggers_code_retry"
Cohesion: 0.12
Nodes (8): AllowedQuota, EmptyResolver, NoopCache, SequenceGenerator, test_real_integrity_error_triggers_code_retry(), CountingRepository, NoopRecordClick, test_200_concurrent_cold_redirects_hit_the_database_once()

### Community 59 - "test_click_pipeline.py"
Cohesion: 0.37
Nodes (9): RedisClickPublisher, admin_settings(), DownRedis, make_link(), pipeline_settings(), test_flusher_persists_batch_and_increments_click_count(), test_flusher_recreates_the_group_after_the_stream_is_lost(), test_flusher_retries_pending_entries() (+1 more)

### Community 60 - "uuid"
Cohesion: 0.36
Nodes (4): RedisTokenBucket, test_lua_bucket_consumes_exhausts_and_refills(), test_lua_bucket_is_atomic_under_concurrency(), test_lua_bucket_keeps_keys_independent()

### Community 62 - "identity/adapters/repository.py"
Cohesion: 0.16
Nodes (8): set_rls_context(), _revoke_family(), SqlAlchemySessionRepository, RotationResult, RotationStatus, admin_settings(), make_link(), test_rls_blocks_cross_user_reads_even_without_app_filter()

### Community 64 - "ref_vitest"
Cohesion: 0.07
Nodes (21): columns, ExternalLink(), ExternalLinkProps, BackToTop(), MockIntersectionObserver, observers, renderBackToTop(), items (+13 more)

### Community 65 - "value_objects.py"
Cohesion: 0.09
Nodes (30): UpdateLinkCommand, InvalidExpiresAt, InvalidTitle, UrlNotAllowed, _normalize_expiry(), UpdateLink, normalize_expires_at(), normalize_title() (+22 more)

### Community 66 - "cn"
Cohesion: 0.08
Nodes (36): LinkDetailPage(), LinkDetailPageProps, LinksLoading(), ControlVisual(), FeatureBlocks(), ShortLinkVisual(), StatsVisual(), WEEKDAY_BARS (+28 more)

### Community 67 - "test_links_api.py"
Cohesion: 0.34
Nodes (13): api_settings(), cleanup(), direct_link(), seed_click(), seed_links(), seed_user(), test_anonymous_create_and_redirect(), test_create_rate_limit_returns_429() (+5 more)

### Community 68 - "create_redis"
Cohesion: 0.18
Nodes (7): close_redis(), create_redis(), redis_client(), run(), read_stream(), run(), redis_client()

### Community 69 - "test_redirect_click_failure.py"
Cohesion: 0.15
Nodes (7): ClickPublisher, RecordClick, BlockingPublisher, click_settings(), DownRedis, test_redirect_continues_and_metric_counts_dropped_click(), test_redirect_does_not_wait_for_click_publisher()

### Community 70 - "adapters/tokens.py"
Cohesion: 0.27
Nodes (4): PyJwtAccessTokens, AccessClaims, test_access_jwt_contains_minimal_claims_and_validates(), test_expired_access_token_is_rejected()

### Community 71 - "build_app"
Cohesion: 0.24
Nodes (8): NotFoundError, build_app(), missing(), test_app_error_uses_standard_envelope(), test_security_error_uses_standard_envelope(), test_unhandled_error_does_not_leak_stack_trace(), test_unknown_route_uses_standard_envelope(), test_validation_error_uses_standard_envelope()

### Community 72 - "Bulkhead"
Cohesion: 0.12
Nodes (7): SystemHostResolver, build_bulkheads(), Bulkhead, BulkheadRegistry, test_bulkhead_limits_concurrency(), test_bulkhead_times_out_when_full(), test_bulkheads_are_named_and_independent()

### Community 73 - "test_database_ready.py"
Cohesion: 0.23
Nodes (5): _database_with_schema(), _FakeConnection, _FakeEngine, test_check_ready_accepts_migrated_schema(), test_check_ready_rejects_missing_schema()

### Community 74 - "token_bucket.js"
Cohesion: 0.18
Nodes (10): AuthenticationError, headers(), negative(), notFound, options, rateLimited, redirect(), stampede() (+2 more)

### Community 75 - "request_context.py"
Cohesion: 0.22
Nodes (3): _incoming_request_id(), RequestIDMiddleware, send_with_request_id()

### Community 76 - "test_real_ip.py"
Cohesion: 0.13
Nodes (9): _forwarded_for(), RealIPMiddleware, resolve_real_ip(), _NeverRedis, test_middleware_sets_request_client_to_real_ip(), test_resolve_real_ip_counts_from_the_right(), test_resolve_real_ip_falls_back_when_header_is_invalid_or_short(), test_resolve_real_ip_without_trusted_proxies_ignores_header() (+1 more)

### Community 77 - "seo.ts"
Cohesion: 0.08
Nodes (30): dynamic, GET(), dynamic, generateMetadata(), inter, jakarta, LocaleLayoutProps, generateMetadata() (+22 more)

### Community 79 - "redirect.js"
Cohesion: 0.13
Nodes (15): CODE_TTL_SECONDS, cold(), COLD_CODES, createIp(), options, otherStatuses, rateLimited, redirectDuration (+7 more)

### Community 80 - "sqlalchemy"
Cohesion: 0.17
Nodes (5): do_run_migrations(), run_async_migrations(), run_migrations_online(), upgrade(), upgrade()

### Community 81 - "theme-sync.tsx"
Cohesion: 0.31
Nodes (10): handleThemeChange(), providers(), ThemeSync(), ThemeToggle(), toggleTheme(), applyTheme(), readTheme(), storeTheme() (+2 more)

### Community 82 - "link_stats"
Cohesion: 0.18
Nodes (5): get_get_link_stats(), link_stats(), LinkStatsResponse, StatsBreakdownResponse, StatsSeriesPointResponse

### Community 83 - "Database"
Cohesion: 0.11
Nodes (14): Database, run(), run(), run(), run(), acleanup(), admin_settings(), aseed_click() (+6 more)

### Community 84 - "http.py"
Cohesion: 0.23
Nodes (8): Services, _authorized(), _check_database(), _check_redis(), health_live(), health_ready(), HealthResponse, metrics()

### Community 85 - "Deploy — Vercel (web) + Render (API/Postgres/Redis)"
Cohesion: 0.15
Nodes (12): 1. Arquitetura, 2. Pré-requisitos, 3.1 Variáveis do serviço `tricolink-api`, 3.2 Variáveis do cron `tricolink-cleanup`, 3. Render — API, Postgres, Key Value e cron, 4. Vercel — web, 5. GitHub Actions — deploy, 6. Observabilidade (+4 more)

### Community 86 - "Resultados"
Cohesion: 0.18
Nodes (10): Create — prova do token bucket (IP fixo, rampa 5→100 RPS, 55 s), Create — throughput (rampa 10→100 RPS, 55 s, IPs sintéticos por iteração), Leitura dos resultados, Metodologia, Redirect — cache frio (500 códigos, 50 VUs), Redirect — cache quente (rampa 50→150 RPS, 65 s), Redirect — prova do token bucket (IP fixo, rampa 20→300 RPS, 65 s), Reprodução (+2 more)

### Community 87 - "i18n-check.mjs"
Cohesion: 0.09
Nodes (16): appRoot, catalogs, errors, files, flattenKeys(), localeSet, messagesDir, reference (+8 more)

### Community 88 - "test_global_bucket_is_shared_across_clients"
Cohesion: 0.15
Nodes (3): GlobalRateLimitMiddleware, DownRedis, test_global_bucket_is_shared_across_clients()

### Community 89 - "proxy.ts"
Cohesion: 0.06
Nodes (36): test_only_config_module_reads_process_environment(), nextConfig, withNextIntl, buildRewrites(), isShortCodePath(), RESERVED_PATTERN, RESERVED_TOP_LEVEL, RewriteRule (+28 more)

### Community 91 - "build_services"
Cohesion: 0.09
Nodes (15): GetAvatar, _matches_signature(), RemoveAvatar, SetAvatar, validate_avatar_image(), UpdateMeCommand, AvatarNotFound, InvalidProfile (+7 more)

### Community 92 - "test_stats_api.py"
Cohesion: 0.58
Nodes (9): api_settings(), cleanup(), seed_clicks(), seed_link(), seed_user(), test_breakdowns_keep_top_ten_and_use_other_and_direct_sentinels(), test_stats_50k_clicks_benchmark(), test_stats_rate_limit_returns_429() (+1 more)

### Community 93 - "RedisDailyQuota"
Cohesion: 0.23
Nodes (3): RedisDailyQuota, _seconds_until_next_utc_day(), QuotaResult

### Community 94 - "db/models.py"
Cohesion: 0.13
Nodes (15): Base, ClickEvent, Link, RefreshToken, User, UserAvatar, CleanupResult, _delete_batch() (+7 more)

### Community 95 - "test_sentry.py"
Cohesion: 0.38
Nodes (3): test_sentry_is_disabled_without_a_dsn(), fake_init(), test_sentry_scrubs_request_data_and_disables_pii()

### Community 97 - "create.js"
Cohesion: 0.21
Nodes (10): create(), created, createDuration, createLink(), createWithSharedIp(), options, otherStatuses, rateLimited (+2 more)

### Community 98 - "jittered_ttl"
Cohesion: 0.48
Nodes (3): jittered_ttl(), test_jittered_ttl_edge_cases(), test_jittered_ttl_stays_within_configured_range()

### Community 99 - "opengraph-image.tsx"
Cohesion: 0.40
Nodes (3): alt, contentType, size

### Community 102 - "CacheClient"
Cohesion: 0.15
Nodes (5): CacheClient, FakeRedis, _sample(), test_cache_get_records_hit_and_miss(), test_cache_set_validates_ttl_and_delete()

### Community 105 - "send"
Cohesion: 0.15
Nodes (6): send_with_headers(), capture_status(), send_with_headers(), run(), tracked_send(), send()

### Community 106 - "User"
Cohesion: 0.16
Nodes (6): SqlAlchemyUserRepository, _to_user(), AuthenticateAccess, User, DuplicateUserError, make_user()

## Knowledge Gaps
- **18 isolated node(s):** `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching`, `lucide-react 1.60.0`, `minimumReleaseAgeExclude Policy` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 520 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `.from_env` to `dataclasses`, `ClickFlusher`, `test_link_cache.py`, `stats_cache.py`, `deps.py`, `ShortCode`, `create_link`, `deps.py`, `links/adapters/repository.py`, `build_services`, `security.py`, `CircuitBreaker`, `.is_production`, `build_services`, `config.py`, `create_app`, `test_identity_adapters.py`, `asyncio`, `test_real_integrity_error_triggers_code_retry`, `test_click_pipeline.py`, `identity/adapters/repository.py`, `sentry.py`, `test_links_api.py`, `create_redis`, `test_redirect_click_failure.py`, `adapters/tokens.py`, `Bulkhead`, `test_database_ready.py`, `Database`, `http.py`, `Deploy — Vercel (web) + Render (API/Postgres/Redis)`, `proxy.ts`, `test_stats_api.py`, `db/models.py`, `test_sentry.py`, `test_database.py`?**
  _High betweenness centrality (0.193) - this node is a cross-community bridge._
- **Are the 109 inferred relationships involving `Settings` (e.g. with `settings_dependency()` and `configure_logging()`) actually correct?**
  _`Settings` has 109 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `identity/presentation/router.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._
- **Why does `§4 Anti XSS / injeção no front` connect `proxy.ts` to `create_app`?**
  _High betweenness centrality (0.153) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `ShortCode` (e.g. with `GetLinkStats` and `RedisLinkCache`) actually correct?**
  _`ShortCode` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Should `shorten-form.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.12299465240641712 - nodes in this community are weakly interconnected._