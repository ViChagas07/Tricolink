# Graph Report - Tricolink  (2026-10-23)

## Corpus Check
- 303 files · ~156,019 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 16 file(s) not represented in the graph (top: (none) 11, .toml 1, .ini 1)

## Summary
- 2496 nodes · 7423 edges · 113 communities (102 shown, 11 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 1001 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `53f874cb`
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
- CodeGenerator
- security_settings
- ClickFlusher
- BodyLimitMiddleware
- httpx
- pnpm Release Policy
- PostCSS Tooling
- Tricolink
- API Package
- test_link_cache.py
- test_identity_api.py
- stats_cache.py
- demo-dashboard.tsx
- deps.py
- SECURITY.md Security Requirements
- UI_SPEC.md Tricolink Interface
- Code Standards
- REST API /api/v1 Contract
- ShortCode
- ClickEvent
- create_link
- test_links_application.py
- isLocale
- test_identity_application.py
- pytest
- RedisAuthThrottle
- links/adapters/repository.py
- account-form.tsx
- build_services
- security.py
- CircuitBreaker
- logging.py
- services.py
- get_services
- .from_env
- LinkRepository
- MemoryTokenBucket
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
- redis_client
- test_real_integrity_error_triggers_code_retry
- ids.py
- test_click_pipeline.py
- uuid
- OriginalUrl
- identity/adapters/repository.py
- ADR 007: Row Level Security as Defense in Depth
- ref_vitest
- AppError
- cn
- test_links_api.py
- test_url_policy.py
- test_redirect_click_failure.py
- adapters/tokens.py
- Contributing to Tricolink
- Bulkhead
- test_database_ready.py
- stats_repository.py
- request_context.py
- test_real_ip.py
- seo.ts
- redirect.js
- sqlalchemy
- theme-sync.tsx
- ADR 002: 302 Redirect for Click Counting
- Database
- http.py
- Deploy — Vercel (web) + Render (API/Postgres/Redis)
- Resultados
- i18n-check.mjs
- ADR 003: SWR + Jitter + Single-Flight + Negative Cache
- proxy.ts
- User
- test_stats_api.py
- ADR 004: Async Click Pipeline with Redis Stream
- cleanup.py
- test_sentry.py
- ADR 005: Lua Token Bucket Rate Limiting
- ADR 001: Modular Monolith with Clean Architecture
- opengraph-image.tsx
- test_rate_limit_dependency_sets_headers_and_429
- helpers.py
- FakeUserRepository
- database.py
- send
- SqlAlchemyUserRepository
- FakeHasher
- Auditoria de segurança — P09
- send
- test_body_limit.py
- Auditoria item a item — SECURITY.md
- test_redirect_stampede.py
- HostResolutionError

## God Nodes (most connected - your core abstractions)
1. `Settings` - 155 edges
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
- `Limitações Conhecidas` --references--> `UrlPolicy`  [INFERRED]
  README.pt-BR.md → apps/api/src/tricolink/modules/links/domain/url_policy.py
- `Servidor Nunca Busca a URL do Usuário` --references--> `UrlPolicy`  [INFERRED]
  README.pt-BR.md → apps/api/src/tricolink/modules/links/domain/url_policy.py
- `3. Render — API, Postgres, Key Value e cron` --references--> `Settings`  [INFERRED]
  docs/deploy/DEPLOY.md → apps/api/src/tricolink/core/config.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Anti Cache Stampede Layer Set** — docs_agent_context_anti_cache_stampede, docs_agent_context_stale_while_revalidate, docs_agent_context_single_flight, docs_agent_context_negative_cache, docs_agent_security_bulkhead [EXTRACTED 1.00]
- **Redirect Hot Path Flow** — docs_agent_context_redirect_cache, docs_agent_context_302_redirect, docs_agent_context_click_stream, docs_agent_context_click_events_table, docs_agent_context_links_table [EXTRACTED 1.00]
- **Tricolink Docker Compose Development Stack** — docker_compose_postgres_service, docker_compose_redis_service, docker_compose_api_service, docker_compose_web_service, docker_compose_app_network, docker_compose_data_network [EXTRACTED 1.00]
- **P00 Graphify Bootstrap Pipeline** — docs_agent_progress_graphify_kilo_integration, docs_agent_progress_semantic_extraction_cache, docs_agent_progress_graph_artifacts, docs_agent_progress_phase_roadmap [INFERRED 0.85]
- **P01 Containerized Tooling and Validation** — docs_agent_progress_make_container_targets, docs_agent_progress_non_root_containers, docs_agent_progress_local_port_override, docs_agent_progress_p01_validation, docker_compose_api_service, docker_compose_web_service [INFERRED 0.85]
- **Defense in Depth Controls** — docs_agent_security_token_bucket, docs_agent_security_circuit_breaker, docs_agent_security_bulkhead, docs_agent_security_rls, docs_agent_context_url_policy [INFERRED 0.85]

## Communities (113 total, 11 thin omitted)

### Community 0 - "Tricolink URL Shortener Product"
Cohesion: 0.25
Nodes (8): click_events Table, Redis Stream Click Buffer, Non-Goals, Tricolink URL Shortener Product, Redirect and Cache Hot Path, URL Anti-Abuse Policy, SSRF Prevention, Design Tokens

### Community 1 - "Token Bucket Rate Limiting"
Cohesion: 0.24
Nodes (9): Daily Link Quotas, Negative Cache for Unknown Codes, Single-Flight Lock, Stale-While-Revalidate Caching, Brute Force Protection, Bulkhead Semaphores, Circuit Breaker, Rate Limit Buckets (+1 more)

### Community 2 - "identity/presentation/router.py"
Cohesion: 0.17
Nodes (22): CurrentUser, get_current_user(), _client_ip(), csrf_token(), delete_my_avatar(), get_my_avatar(), login(), logout() (+14 more)

### Community 3 - "shorten-form.tsx"
Cohesion: 0.12
Nodes (21): HeroSection(), CopyState, CreateLinkResponse, ERROR_KEYS, FormError, getOwnHosts(), ShortenForm(), handleSubmit() (+13 more)

### Community 4 - "Agent Workflow and Graphify"
Cohesion: 0.18
Nodes (8): graphify Slash Command, Mandatory Session Reading Order, CONTEXT.md Single Source of Truth, Graphify Context Engineering, Graphify Installation Commands, Per-Phase Graphify Routine, graphify query/path/explain Workflow, Tricolink README Stub (P11)

### Community 5 - "Compose and P01 Infra"
Cohesion: 0.16
Nodes (20): pnpm allowBuilds Allowlist, API Compose Service, app Network, data Network, postgres_data Volume, PostgreSQL 16 Compose Service, Redis 7 Compose Service, Web Compose Service (+12 more)

### Community 6 - "dataclasses"
Cohesion: 0.14
Nodes (10): _headers(), record_rate_limit_fallback(), record_rate_limited(), _reset_seconds(), RateLimitResult, BucketPolicy, build_policies(), _reset_seconds() (+2 more)

### Community 7 - "CodeGenerator"
Cohesion: 0.36
Nodes (4): CodeGenerator, test_code_generator_can_be_made_deterministic(), test_code_generator_uses_seven_base62_characters(), test_code_generator_validates_configuration()

### Community 8 - "security_settings"
Cohesion: 0.21
Nodes (27): cleanup_email(), make_client(), security_settings(), unique_ip(), csrf_headers(), login(), register(), test_csrf_origin_and_cross_site_mutations_are_rejected() (+19 more)

### Community 9 - "ClickFlusher"
Cohesion: 0.16
Nodes (6): ClickFlusher, read_group(), guarded(), operation(), guarded(), Achados corrigidos

### Community 10 - "BodyLimitMiddleware"
Cohesion: 0.26
Nodes (3): BodyLimitMiddleware, _header_values(), _send_json()

### Community 11 - "httpx"
Cohesion: 0.25
Nodes (8): SecurityHeadersMiddleware, build_inner(), test_hsts_only_in_production(), test_request_id_accepts_only_safe_values(), test_request_id_is_generated_and_returned(), test_security_headers_are_added(), test_timeout_allows_fast_requests(), test_timeout_returns_504()

### Community 15 - "Tricolink"
Cohesion: 0.05
Nodes (46): GET(), 1. Render (API + DB + Redis + Cron), 2. Vercel (Web), 302 vs 301, 3. GitHub Actions, ADRs, Alvos Make Úteis, API (+38 more)

### Community 18 - "test_link_cache.py"
Cohesion: 0.32
Nodes (11): _async_link(), cache_settings(), cleanup(), make_link(), test_cold_stampede_uses_one_database_query(), loader(), test_invalidation_during_a_stale_refresh_cannot_repopulate_the_cache(), test_invalidation_forces_the_next_read_to_use_the_loader() (+3 more)

### Community 19 - "test_identity_api.py"
Cohesion: 0.23
Nodes (21): create_app(), admin_settings(), cleanup(), run(), FakeGoogleOIDC, google_claims(), identity_settings(), login() (+13 more)

### Community 20 - "stats_cache.py"
Cohesion: 0.06
Nodes (33): _breakdown(), _deserialize(), RedisStatsCache, _serialize(), GetLinkStats, load(), RawStats, StatsCache (+25 more)

### Community 21 - "demo-dashboard.tsx"
Cohesion: 0.08
Nodes (37): BreakdownColumns, BreakdownRow, BreakdownTable(), BreakdownTableProps, ClicksChart(), ClicksChartProps, ClicksPoint, ChartPlaceholder() (+29 more)

### Community 22 - "deps.py"
Cohesion: 0.21
Nodes (14): _rate_limit_error(), user_rate_limit(), dependency(), apply_rate_limit_headers(), client_ip(), _get_limiter(), rate_limit(), dependency() (+6 more)

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
Nodes (15): jittered_ttl(), record_cache_hit(), record_cache_miss(), _CacheRead, _entry_from_link(), RedisLinkCache, CacheEntry, ShortCode (+7 more)

### Community 28 - "ClickEvent"
Cohesion: 0.10
Nodes (16): record_click_dropped(), record_clicks_flushed(), _parse_event(), _browser(), ClickEvent, extract_referrer_host(), normalize_country(), parse_user_agent() (+8 more)

### Community 29 - "create_link"
Cohesion: 0.11
Nodes (22): get_click_publisher(), get_create_link(), get_delete_link(), get_get_link(), get_links_overview(), get_list_links(), get_resolve_link(), get_update_link() (+14 more)

### Community 30 - "test_links_application.py"
Cohesion: 0.12
Nodes (24): CreateLinkCommand, build_create(), build_link(), FakeCache, FakeClock, FakeGenerator, FakePublisher, FakeQuota (+16 more)

### Community 31 - "isLocale"
Cohesion: 0.11
Nodes (37): AccountPage(), AccountPageProps, generateMetadata(), generateMetadata(), LinkDetailPage(), LinkDetailPageProps, generateMetadata(), LinksPage() (+29 more)

### Community 32 - "test_identity_application.py"
Cohesion: 0.29
Nodes (18): LoginCommand, build_issuer(), build_login(), FakeAccessTokens, FakeClock, FakeSessionRepository, FakeThrottle, test_authenticate_access_returns_active_user_or_none() (+10 more)

### Community 33 - "pytest"
Cohesion: 0.37
Nodes (12): operation(), policy(), test_credentials_controls_and_backslashes_are_blocked(), test_dns_rebinding_mixed_answers_are_all_checked(), test_forbidden_schemes_and_scheme_relative_urls_are_blocked(), test_global_ipv4_and_ipv6_answers_are_accepted(), test_obfuscated_or_internal_hostnames_are_blocked(), test_own_domain_and_subdomains_are_blocked_as_redirect_loops() (+4 more)

### Community 34 - "RedisAuthThrottle"
Cohesion: 0.16
Nodes (5): _digest(), RedisAuthThrottle, guarded(), operation(), ThrottleResult

### Community 35 - "links/adapters/repository.py"
Cohesion: 0.11
Nodes (17): set_rls_context(), _escape_like(), _is_code_conflict(), SqlAlchemyLinkRepository, _to_domain(), test_real_integrity_error_triggers_code_retry(), run(), admin_settings() (+9 more)

### Community 36 - "account-form.tsx"
Cohesion: 0.12
Nodes (22): AccountForm(), handleAvatarRemove(), handleAvatarSelected(), handleError(), handleLocaleChange(), handleProfileSubmit(), baseDto, baseUser (+14 more)

### Community 37 - "build_services"
Cohesion: 0.14
Nodes (15): build_services(), AuthenticateAccess, AuthSession, InvalidGoogleLogin, LoginWithGoogle, Logout, AccessTokenIssuer, Clock (+7 more)

### Community 38 - "security.py"
Cohesion: 0.13
Nodes (15): GoogleOIDCClient, GoogleNotConfigured, InvalidNextPath, google_callback(), _google_error_redirect(), google_login(), allowed_origins(), csrf_protect() (+7 more)

### Community 39 - "CircuitBreaker"
Cohesion: 0.05
Nodes (14): CacheClient, record_circuit_state(), CircuitBreaker, CircuitState, CircuitOpenError, FakeRedis, _sample(), test_cache_get_records_hit_and_miss() (+6 more)

### Community 40 - "logging.py"
Cohesion: 0.15
Nodes (6): configure_logging(), get_logger(), MetricsMiddleware, _route_path(), record_request(), lifespan()

### Community 41 - "services.py"
Cohesion: 0.09
Nodes (9): AnalyticsServices, IdentityServices, LinkServices, _own_hosts(), RedisDailyQuota, _seconds_until_next_utc_day(), QuotaResult, SystemClock (+1 more)

### Community 42 - "get_services"
Cohesion: 0.17
Nodes (17): get_cache(), get_current_user_optional(), get_services(), get_session(), settings_dependency(), get_authenticate_access(), get_get_avatar(), get_get_me() (+9 more)

### Community 43 - ".from_env"
Cohesion: 0.10
Nodes (30): _asyncpg_url(), _boolean(), _env(), get_migration_database_url(), get_settings(), _integer(), _is_strong_secret(), _number() (+22 more)

### Community 44 - "LinkRepository"
Cohesion: 0.09
Nodes (17): DeleteLink, UpdateLinkCommand, LinkNotFound, GetLink, GetLinksOverview, LinksOverview, CacheUnavailable, Clock (+9 more)

### Community 45 - "MemoryTokenBucket"
Cohesion: 0.22
Nodes (9): _BucketState, MemoryTokenBucket, DownRedis, FakeClock, test_memory_bucket_consumes_and_exhausts(), test_memory_bucket_never_exceeds_capacity(), test_memory_bucket_refills(), test_rate_limiter_falls_back_to_memory_when_redis_is_down() (+1 more)

### Community 46 - "create_app"
Cohesion: 0.10
Nodes (8): init_sentry(), _scrub_event(), test_metrics_accepts_valid_token(), test_metrics_rejects_wrong_token(), test_metrics_requires_token(), production_settings(), test_body_limit_is_enforced_by_the_full_app(), test_docs_and_openapi_are_disabled_in_production()

### Community 47 - "list_links.py"
Cohesion: 0.24
Nodes (9): LinkPage, InvalidCursor, InvalidPagination, ListLinks, _normalize_query(), decode_cursor(), encode_cursor(), PageCursor (+1 more)

### Community 48 - "register.py"
Cohesion: 0.19
Nodes (8): AuthLocked, InvalidCredentials, InvalidEmail, WeakPassword, Login, AuthThrottle, PasswordHasher, Register

### Community 49 - "test_identity_adapters.py"
Cohesion: 0.10
Nodes (13): generate_csrf_token(), clear_session_cookies(), set_csrf_cookie(), set_session_cookies(), build_session(), fast_hasher(), test_argon2_hasher_roundtrip_and_dummy(), test_clear_cookies_deletes_all_session_cookies() (+5 more)

### Community 50 - "cn"
Cohesion: 0.07
Nodes (43): dynamic, generateMetadata(), inter, jakarta, LocaleLayout(), LocaleLayoutProps, LinkDetailError(), LocaleNotFound() (+35 more)

### Community 51 - "api.ts"
Cohesion: 0.07
Nodes (37): FieldError, FieldErrors, FormError, LoginForm(), handleSubmit(), handleTabKeyDown(), switchMode(), LoginFormProps (+29 more)

### Community 52 - "error_handlers.py"
Cohesion: 0.12
Nodes (13): install_error_handlers(), handle_app_error(), handle_http_exception(), handle_unexpected_error(), handle_validation_error(), _json_error(), error_payload(), build_app() (+5 more)

### Community 53 - "links/domain/entities.py"
Cohesion: 0.22
Nodes (10): ResolvedLink, _Unset, _as_utc(), _entry_state(), _resolved_from_cache(), _resolved_from_link(), ResolveLink, _as_utc() (+2 more)

### Community 54 - "RefreshTokenRecord"
Cohesion: 0.29
Nodes (4): _as_utc(), RefreshTokenRecord, TokenFamily, test_token_family_and_refresh_record_lifecycle()

### Community 55 - "register.py"
Cohesion: 0.11
Nodes (24): Email, InvalidEmailError, InvalidGoogleIdentityError, WeakPasswordError, _display_name(), _number(), _picture_url(), _string() (+16 more)

### Community 56 - "redis_client"
Cohesion: 0.17
Nodes (4): close_redis(), ping_redis(), redis_client(), redis_client()

### Community 57 - "test_real_integrity_error_triggers_code_retry"
Cohesion: 0.18
Nodes (4): AllowedQuota, EmptyResolver, NoopCache, SequenceGenerator

### Community 59 - "test_click_pipeline.py"
Cohesion: 0.37
Nodes (10): ClickEvent, RedisClickPublisher, admin_settings(), DownRedis, make_link(), pipeline_settings(), test_flusher_persists_batch_and_increments_click_count(), test_flusher_recreates_the_group_after_the_stream_is_lost() (+2 more)

### Community 60 - "uuid"
Cohesion: 0.36
Nodes (4): RedisTokenBucket, test_lua_bucket_consumes_exhausts_and_refills(), test_lua_bucket_is_atomic_under_concurrency(), test_lua_bucket_keeps_keys_independent()

### Community 61 - "OriginalUrl"
Cohesion: 0.14
Nodes (18): InvalidUrlError, ReservedAliasError, HostResolver, _normalize_own_host(), _normalize_host(), OriginalUrl, _validate_hostname(), test_link_state_accounts_for_expiry_and_active_flag() (+10 more)

### Community 62 - "identity/adapters/repository.py"
Cohesion: 0.17
Nodes (10): Base, RefreshToken, User, UserAvatar, _revoke_family(), SqlAlchemySessionRepository, RotationResult, test_click_events_have_device_check_and_index() (+2 more)

### Community 63 - "ADR 007: Row Level Security as Defense in Depth"
Cohesion: 0.18
Nodes (7): ADR 007: Row Level Security as Defense in Depth, Consequences, Context, Decision, Rationale, References, Status

### Community 64 - "ref_vitest"
Cohesion: 0.10
Nodes (12): columns, ExternalLink(), ExternalLinkProps, BackToTop(), MockIntersectionObserver, observers, renderBackToTop(), items (+4 more)

### Community 65 - "AppError"
Cohesion: 0.06
Nodes (22): CreateLink, AliasReserved, AliasTaken, CodeGenerationFailed, DailyQuotaExceeded, InvalidAlias, InvalidExpiresAt, InvalidTitle (+14 more)

### Community 66 - "cn"
Cohesion: 0.11
Nodes (27): LinksLoading(), CopyLinkButton(), LinksSkeleton(), LinksSkeletonProps, LinkCard(), LinksView(), confirmDelete(), handleSave() (+19 more)

### Community 67 - "test_links_api.py"
Cohesion: 0.26
Nodes (16): api_settings(), cleanup(), direct_link(), seed_click(), run(), seed_links(), seed_user(), run() (+8 more)

### Community 68 - "test_url_policy.py"
Cohesion: 0.24
Nodes (13): is_blocked_ip(), build_policy(), test_is_blocked_ip_allows_only_global_addresses(), test_is_blocked_ip_blocks_non_global_addresses(), test_url_policy_accepts_public_urls(), test_url_policy_blocks_host_when_resolution_fails_or_is_empty(), test_url_policy_blocks_invalid_dns_answer(), test_url_policy_blocks_own_domain_and_subdomains_without_dns() (+5 more)

### Community 69 - "test_redirect_click_failure.py"
Cohesion: 0.29
Nodes (5): BlockingPublisher, click_settings(), DownRedis, test_redirect_continues_and_metric_counts_dropped_click(), test_redirect_does_not_wait_for_click_publisher()

### Community 70 - "adapters/tokens.py"
Cohesion: 0.27
Nodes (5): PyJwtAccessTokens, AccessClaims, IssuedAccessToken, test_access_jwt_contains_minimal_claims_and_validates(), test_expired_access_token_is_rejected()

### Community 71 - "Contributing to Tricolink"
Cohesion: 0.20
Nodes (9): Architecture Decision Records (ADR), Code Standards, Contributing to Tricolink, Conventional Commits, Development Workflow, License, Pull Request Checklist, Quick Start (+1 more)

### Community 72 - "Bulkhead"
Cohesion: 0.07
Nodes (17): build_bulkheads(), Bulkhead, BulkheadRegistry, Argon2PasswordHasher, BulkheadFullError, test_bulkhead_limits_concurrency(), test_bulkhead_times_out_when_full(), test_bulkheads_are_named_and_independent() (+9 more)

### Community 73 - "test_database_ready.py"
Cohesion: 0.23
Nodes (5): _database_with_schema(), _FakeConnection, _FakeEngine, test_check_ready_accepts_migrated_schema(), test_check_ready_rejects_missing_schema()

### Community 75 - "request_context.py"
Cohesion: 0.22
Nodes (3): _incoming_request_id(), RequestIDMiddleware, send_with_request_id()

### Community 76 - "test_real_ip.py"
Cohesion: 0.13
Nodes (9): _forwarded_for(), RealIPMiddleware, resolve_real_ip(), _NeverRedis, test_middleware_sets_request_client_to_real_ip(), test_resolve_real_ip_counts_from_the_right(), test_resolve_real_ip_falls_back_when_header_is_invalid_or_short(), test_resolve_real_ip_without_trusted_proxies_ignores_header() (+1 more)

### Community 77 - "seo.ts"
Cohesion: 0.08
Nodes (31): dynamic, generateMetadata(), HomePage(), HomePageProps, sitemap(), Faq(), FaqEntry, FaqProps (+23 more)

### Community 79 - "redirect.js"
Cohesion: 0.06
Nodes (32): headers(), negative(), notFound, options, rateLimited, redirect(), stampede(), create() (+24 more)

### Community 80 - "sqlalchemy"
Cohesion: 0.17
Nodes (5): do_run_migrations(), run_async_migrations(), run_migrations_online(), upgrade(), upgrade()

### Community 81 - "theme-sync.tsx"
Cohesion: 0.31
Nodes (10): handleThemeChange(), providers(), ThemeSync(), ThemeToggle(), toggleTheme(), applyTheme(), readTheme(), storeTheme() (+2 more)

### Community 82 - "ADR 002: 302 Redirect for Click Counting"
Cohesion: 0.25
Nodes (7): ADR 002: 302 Redirect for Click Counting, Consequences, Context, Decision, Rationale, References, Status

### Community 83 - "Database"
Cohesion: 0.16
Nodes (15): create_redis(), Database, Link, test_cleanup_deletes_old_clicks_and_expired_links_idempotently(), run(), run(), acleanup(), acleanup_email() (+7 more)

### Community 84 - "http.py"
Cohesion: 0.19
Nodes (9): Services, _authorized(), _check_database(), _check_redis(), health_live(), health_ready(), HealthResponse, metrics() (+1 more)

### Community 85 - "Deploy — Vercel (web) + Render (API/Postgres/Redis)"
Cohesion: 0.15
Nodes (12): 1. Arquitetura, 2. Pré-requisitos, 3.1 Variáveis do serviço `tricolink-api`, 3.2 Variáveis do cron `tricolink-cleanup`, 3. Render — API, Postgres, Key Value e cron, 4. Vercel — web, 5. GitHub Actions — deploy, 6. Observabilidade (+4 more)

### Community 86 - "Resultados"
Cohesion: 0.18
Nodes (10): Create — prova do token bucket (IP fixo, rampa 5→100 RPS, 55 s), Create — throughput (rampa 10→100 RPS, 55 s, IPs sintéticos por iteração), Leitura dos resultados, Metodologia, Redirect — cache frio (500 códigos, 50 VUs), Redirect — cache quente (rampa 50→150 RPS, 65 s), Redirect — prova do token bucket (IP fixo, rampa 20→300 RPS, 65 s), Reprodução (+2 more)

### Community 87 - "i18n-check.mjs"
Cohesion: 0.09
Nodes (16): appRoot, catalogs, errors, files, flattenKeys(), localeSet, messagesDir, reference (+8 more)

### Community 88 - "ADR 003: SWR + Jitter + Single-Flight + Negative Cache"
Cohesion: 0.25
Nodes (7): ADR 003: SWR + Jitter + Single-Flight + Negative Cache, Consequences, Context, Decision, Rationale, References, Status

### Community 89 - "proxy.ts"
Cohesion: 0.14
Nodes (17): nextConfig, withNextIntl, buildRewrites(), isShortCodePath(), RESERVED_PATTERN, RESERVED_TOP_LEVEL, RewriteRule, RewritesConfig (+9 more)

### Community 91 - "User"
Cohesion: 0.10
Nodes (16): GetAvatar, _matches_signature(), RemoveAvatar, SetAvatar, validate_avatar_image(), UpdateMeCommand, AvatarNotFound, InvalidProfile (+8 more)

### Community 92 - "test_stats_api.py"
Cohesion: 0.44
Nodes (11): api_settings(), cleanup(), seed_clicks(), run(), seed_link(), seed_user(), run(), test_breakdowns_keep_top_ten_and_use_other_and_direct_sentinels() (+3 more)

### Community 93 - "ADR 004: Async Click Pipeline with Redis Stream"
Cohesion: 0.25
Nodes (7): ADR 004: Async Click Pipeline with Redis Stream, Consequences, Context, Decision, Rationale, References, Status

### Community 94 - "cleanup.py"
Cohesion: 0.27
Nodes (4): CleanupResult, _delete_batch(), main(), run_cleanup()

### Community 95 - "test_sentry.py"
Cohesion: 0.38
Nodes (3): test_sentry_is_disabled_without_a_dsn(), fake_init(), test_sentry_scrubs_request_data_and_disables_pii()

### Community 96 - "ADR 005: Lua Token Bucket Rate Limiting"
Cohesion: 0.25
Nodes (7): ADR 005: Lua Token Bucket Rate Limiting, Consequences, Context, Decision, Rationale, References, Status

### Community 97 - "ADR 001: Modular Monolith with Clean Architecture"
Cohesion: 0.29
Nodes (6): ADR 001: Modular Monolith with Clean Architecture, Consequences, Context, Decision, References, Status

### Community 99 - "opengraph-image.tsx"
Cohesion: 0.40
Nodes (3): alt, contentType, size

### Community 100 - "test_rate_limit_dependency_sets_headers_and_429"
Cohesion: 0.10
Nodes (7): get_rate_limiter(), GlobalRateLimitMiddleware, RateLimiter, DownRedis, test_global_bucket_is_shared_across_clients(), DownRedis, test_rate_limit_dependency_sets_headers_and_429()

### Community 101 - "helpers.py"
Cohesion: 0.30
Nodes (10): build_app(), cleanup(), expires_in(), seed_click(), seed_link(), seed_user(), test_sqli_payloads_are_inert_in_every_input(), test_time_based_payload_does_not_execute_pg_sleep() (+2 more)

### Community 104 - "database.py"
Cohesion: 0.22
Nodes (3): create_engine(), create_session_factory(), unit_of_work()

### Community 105 - "send"
Cohesion: 0.15
Nodes (5): replay_body(), RequestTimeoutMiddleware, run(), tracked_send(), receive()

### Community 106 - "SqlAlchemyUserRepository"
Cohesion: 0.22
Nodes (4): SqlAlchemyUserRepository, _to_user(), DuplicateUserError, make_user()

### Community 107 - "FakeHasher"
Cohesion: 0.31
Nodes (7): RegisterCommand, build_register(), FakeHasher, test_register_creates_user_with_argon_hash_and_no_session(), test_register_duplicate_hashes_but_returns_same_success(), test_register_rejects_invalid_email(), test_register_rejects_weak_password_and_throttle()

### Community 108 - "Auditoria de segurança — P09"
Cohesion: 0.18
Nodes (10): Achados residuais aceitos (com justificativa), Auditoria de segurança — P09, Como reproduzir, Conclusão, Configuração de produção, O que não foi possível testar / limitações honestas, Resumo executivo, RLS — prova independente (+2 more)

### Community 109 - "send"
Cohesion: 0.25
Nodes (4): send_with_headers(), capture_status(), send_with_headers(), send()

### Community 111 - "test_body_limit.py"
Cohesion: 0.33
Nodes (5): build_app(), test_accepts_body_at_limit(), test_invalid_content_length_is_rejected(), test_rejects_chunked_body_above_limit(), test_rejects_content_length_above_limit_before_reading()

### Community 112 - "Auditoria item a item — SECURITY.md"
Cohesion: 0.17
Nodes (13): test_only_config_module_reads_process_environment(), auth(), §10 Supply chain, §1 Token Bucket, §2 Resiliência / anti-DDoS, §3 Anti SQL Injection, §4 Anti XSS / injeção no front, §5 Autenticação, sessão e força bruta (+5 more)

### Community 113 - "test_redirect_stampede.py"
Cohesion: 0.28
Nodes (3): CountingRepository, NoopRecordClick, test_200_concurrent_cold_redirects_hit_the_database_once()

### Community 116 - "HostResolutionError"
Cohesion: 0.17
Nodes (4): SystemHostResolver, HostResolutionError, FakeResolver, FakeResolver

## Knowledge Gaps
- **18 isolated node(s):** `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching`, `lucide-react 1.60.0`, `minimumReleaseAgeExclude Policy` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 608 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `.from_env` to `identity/presentation/router.py`, `dataclasses`, `security_settings`, `ClickFlusher`, `test_link_cache.py`, `test_identity_api.py`, `stats_cache.py`, `deps.py`, `ShortCode`, `ClickEvent`, `create_link`, `RedisAuthThrottle`, `links/adapters/repository.py`, `build_services`, `security.py`, `CircuitBreaker`, `logging.py`, `services.py`, `get_services`, `create_app`, `test_identity_adapters.py`, `redis_client`, `test_click_pipeline.py`, `test_links_api.py`, `test_redirect_click_failure.py`, `adapters/tokens.py`, `Bulkhead`, `test_database_ready.py`, `Database`, `http.py`, `Deploy — Vercel (web) + Render (API/Postgres/Redis)`, `test_stats_api.py`, `cleanup.py`, `test_sentry.py`, `helpers.py`, `database.py`, `Auditoria de segurança — P09`, `Auditoria item a item — SECURITY.md`, `test_redirect_stampede.py`?**
  _High betweenness centrality (0.171) - this node is a cross-community bridge._
- **Are the 110 inferred relationships involving `Settings` (e.g. with `settings_dependency()` and `configure_logging()`) actually correct?**
  _`Settings` has 110 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `shorten-form.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.11827956989247312 - nodes in this community are weakly interconnected._
- **Why does `§4 Anti XSS / injeção no front` connect `Auditoria item a item — SECURITY.md` to `security_settings`, `proxy.ts`?**
  _High betweenness centrality (0.150) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `ShortCode` (e.g. with `GetLinkStats` and `RedisLinkCache`) actually correct?**
  _`ShortCode` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Should `dataclasses` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._