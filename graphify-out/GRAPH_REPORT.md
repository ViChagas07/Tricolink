# Graph Report - Tricolink  (2026-10-23)

## Corpus Check
- 285 files · ~142,169 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: (none) 10, .toml 1, .ini 1)

## Summary
- 2294 nodes · 7006 edges · 110 communities (98 shown, 12 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 959 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `23bd7cf2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tricolink URL Shortener Product
- Token Bucket Rate Limiting
- test_link_cache.py
- shorten-form.tsx
- Agent Workflow and Graphify
- Compose and P01 Infra
- cleanup.py
- test_real_ip.py
- MemoryTokenBucket
- ClickFlusher
- BodyLimitMiddleware
- httpx
- pnpm Release Policy
- PostCSS Tooling
- login-form.tsx
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
- isLocale
- test_identity_application.py
- create_app
- test_links_repository.py
- links/adapters/repository.py
- AccountForm
- build_services
- identity/presentation/router.py
- RedisAuthThrottle
- test_identity_adapters.py
- build_services
- deps.py
- test_real_integrity_error_triggers_code_retry
- LinkRepository
- Settings
- security_settings
- list_links.py
- register.py
- links-view.tsx
- ref_next_intl
- api.ts
- adapters/tokens.py
- links/domain/entities.py
- RefreshTokenRecord
- register.py
- config.py
- logging.py
- ids.py
- .__call__
- BucketPolicy
- User
- ClickEvent
- main.py
- ref_vitest
- value_objects.py
- [locale]/page.tsx
- test_links_api.py
- pytest
- test_redirect_click_failure.py
- .__call__
- test_body_limit.py
- test_url_policy.py
- request_context.py
- security.py
- register.py
- error_handlers.py
- seo.ts
- redirect.js
- test_click_pipeline.py
- RedisDailyQuota
- link_stats
- Database
- Bulkhead
- Deploy — Vercel (web) + Render (API/Postgres/Redis)
- Resultados
- i18n-check.mjs
- CodeGenerator
- proxy.ts
- Settings
- test_stats_api.py
- sentry.py
- db/models.py
- test_sentry.py
- .__init__
- Argon2PasswordHasher
- Auditoria de segurança — P09
- env.py
- CacheClient
- HostResolutionError
- CacheClient
- test_production_hardening.py
- Auditoria item a item — SECURITY.md
- RateLimiter
- UserRepository
- test_circuit_breaker.py
- opengraph-image.tsx
- google_login.py

## God Nodes (most connected - your core abstractions)
1. `Settings` - 153 edges
2. `ShortCode` - 95 edges
3. `Link` - 82 edges
4. `create_app()` - 63 edges
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
- `§3 Anti SQL Injection` --references--> `test_runtime_role_has_rls_enforced()`  [EXTRACTED]
  docs/security/AUDIT.md → apps/api/tests/security/test_rls_security.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Anti Cache Stampede Layer Set** — docs_agent_context_anti_cache_stampede, docs_agent_context_stale_while_revalidate, docs_agent_context_single_flight, docs_agent_context_negative_cache, docs_agent_security_bulkhead [EXTRACTED 1.00]
- **Redirect Hot Path Flow** — docs_agent_context_redirect_cache, docs_agent_context_302_redirect, docs_agent_context_click_stream, docs_agent_context_click_events_table, docs_agent_context_links_table [EXTRACTED 1.00]
- **Tricolink Docker Compose Development Stack** — docker_compose_postgres_service, docker_compose_redis_service, docker_compose_api_service, docker_compose_web_service, docker_compose_app_network, docker_compose_data_network [EXTRACTED 1.00]
- **P00 Graphify Bootstrap Pipeline** — docs_agent_progress_graphify_kilo_integration, docs_agent_progress_semantic_extraction_cache, docs_agent_progress_graph_artifacts, docs_agent_progress_phase_roadmap [INFERRED 0.85]
- **P01 Containerized Tooling and Validation** — docs_agent_progress_make_container_targets, docs_agent_progress_non_root_containers, docs_agent_progress_local_port_override, docs_agent_progress_p01_validation, docker_compose_api_service, docker_compose_web_service [INFERRED 0.85]
- **Defense in Depth Controls** — docs_agent_security_token_bucket, docs_agent_security_circuit_breaker, docs_agent_security_bulkhead, docs_agent_security_rls, docs_agent_context_url_policy [INFERRED 0.85]

## Communities (110 total, 12 thin omitted)

### Community 0 - "Tricolink URL Shortener Product"
Cohesion: 0.25
Nodes (8): click_events Table, Redis Stream Click Buffer, Non-Goals, Tricolink URL Shortener Product, Redirect and Cache Hot Path, URL Anti-Abuse Policy, SSRF Prevention, Design Tokens

### Community 1 - "Token Bucket Rate Limiting"
Cohesion: 0.24
Nodes (9): Daily Link Quotas, Negative Cache for Unknown Codes, Single-Flight Lock, Stale-While-Revalidate Caching, Brute Force Protection, Bulkhead Semaphores, Circuit Breaker, Rate Limit Buckets (+1 more)

### Community 2 - "test_link_cache.py"
Cohesion: 0.32
Nodes (11): _async_link(), cache_settings(), cleanup(), make_link(), test_cold_stampede_uses_one_database_query(), loader(), test_invalidation_during_a_stale_refresh_cannot_repopulate_the_cache(), test_invalidation_forces_the_next_read_to_use_the_loader() (+3 more)

### Community 3 - "shorten-form.tsx"
Cohesion: 0.11
Nodes (24): LinkDetailError(), CopyState, CreateLinkResponse, ERROR_KEYS, FormError, getOwnHosts(), ShortenForm(), handleSubmit() (+16 more)

### Community 4 - "Agent Workflow and Graphify"
Cohesion: 0.18
Nodes (8): graphify Slash Command, Mandatory Session Reading Order, CONTEXT.md Single Source of Truth, Graphify Context Engineering, Graphify Installation Commands, Per-Phase Graphify Routine, graphify query/path/explain Workflow, Tricolink README Stub (P11)

### Community 5 - "Compose and P01 Infra"
Cohesion: 0.16
Nodes (20): pnpm allowBuilds Allowlist, API Compose Service, app Network, data Network, postgres_data Volume, PostgreSQL 16 Compose Service, Redis 7 Compose Service, Web Compose Service (+12 more)

### Community 6 - "cleanup.py"
Cohesion: 0.27
Nodes (4): CleanupResult, _delete_batch(), main(), run_cleanup()

### Community 7 - "test_real_ip.py"
Cohesion: 0.14
Nodes (8): _forwarded_for(), RealIPMiddleware, resolve_real_ip(), _NeverRedis, test_middleware_sets_request_client_to_real_ip(), test_resolve_real_ip_counts_from_the_right(), test_resolve_real_ip_falls_back_when_header_is_invalid_or_short(), test_resolve_real_ip_without_trusted_proxies_ignores_header()

### Community 8 - "MemoryTokenBucket"
Cohesion: 0.16
Nodes (10): MemoryTokenBucket, RateLimiter, test_spoofed_xff_cannot_bypass_rate_limit(), DownRedis, FakeClock, test_memory_bucket_consumes_and_exhausts(), test_memory_bucket_never_exceeds_capacity(), test_memory_bucket_refills() (+2 more)

### Community 9 - "ClickFlusher"
Cohesion: 0.19
Nodes (5): ClickFlusher, read_group(), guarded(), operation(), guarded()

### Community 10 - "BodyLimitMiddleware"
Cohesion: 0.26
Nodes (3): BodyLimitMiddleware, _header_values(), _send_json()

### Community 11 - "httpx"
Cohesion: 0.23
Nodes (8): RequestTimeoutMiddleware, build_inner(), test_hsts_only_in_production(), test_request_id_accepts_only_safe_values(), test_request_id_is_generated_and_returned(), test_security_headers_are_added(), test_timeout_allows_fast_requests(), test_timeout_returns_504()

### Community 15 - "login-form.tsx"
Cohesion: 0.15
Nodes (22): first(), generateMetadata(), LoginPage(), LoginPageProps, FieldError, FieldErrors, FormError, LoginForm() (+14 more)

### Community 18 - "database.py"
Cohesion: 0.24
Nodes (3): create_engine(), create_session_factory(), unit_of_work()

### Community 19 - "CircuitBreaker"
Cohesion: 0.12
Nodes (3): CircuitBreaker, CircuitState, CircuitOpenError

### Community 20 - "stats_cache.py"
Cohesion: 0.09
Nodes (26): record_cache_hit(), record_cache_miss(), _breakdown(), _deserialize(), RedisStatsCache, _serialize(), load(), BreakdownItem (+18 more)

### Community 21 - "demo-dashboard.tsx"
Cohesion: 0.08
Nodes (37): BreakdownColumns, BreakdownRow, BreakdownTable(), BreakdownTableProps, ClicksChart(), ClicksChartProps, ClicksPoint, ChartPlaceholder() (+29 more)

### Community 22 - "http.py"
Cohesion: 0.09
Nodes (17): Services, close_redis(), create_redis(), ping_redis(), _authorized(), _check_database(), _check_redis(), health_live() (+9 more)

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
Nodes (17): jittered_ttl(), _CacheRead, _entry_from_link(), RedisLinkCache, CacheEntry, CacheUnavailable, Link, ShortCode (+9 more)

### Community 28 - "click.py"
Cohesion: 0.16
Nodes (13): _parse_event(), _browser(), ClickEvent, extract_referrer_host(), normalize_country(), parse_user_agent(), UserAgentInfo, ClickPublisher (+5 more)

### Community 29 - "create_link"
Cohesion: 0.17
Nodes (15): CurrentUser, create_link(), delete_link(), get_link(), _link_response(), links_overview(), list_links(), redirect_link() (+7 more)

### Community 30 - "test_links_application.py"
Cohesion: 0.13
Nodes (24): CreateLinkCommand, build_create(), build_link(), FakeCache, FakeClock, FakeGenerator, FakePublisher, FakeQuota (+16 more)

### Community 31 - "isLocale"
Cohesion: 0.18
Nodes (21): AccountPage(), AccountPageProps, generateMetadata(), generateMetadata(), LinkDetailPage(), LinkDetailPageProps, generateMetadata(), LinksPage() (+13 more)

### Community 32 - "test_identity_application.py"
Cohesion: 0.12
Nodes (24): LoginCommand, RegisterCommand, build_issuer(), build_login(), build_register(), FakeAccessTokens, FakeClock, FakeHasher (+16 more)

### Community 33 - "create_app"
Cohesion: 0.23
Nodes (20): create_app(), admin_settings(), cleanup(), run(), FakeGoogleOIDC, google_claims(), identity_settings(), login() (+12 more)

### Community 34 - "test_links_repository.py"
Cohesion: 0.42
Nodes (6): admin_settings(), build_link(), cleanup(), seed_user(), test_repository_crud_list_search_and_owner_filter(), test_repository_returns_none_for_non_owned_management_reads()

### Community 35 - "links/adapters/repository.py"
Cohesion: 0.20
Nodes (7): set_rls_context(), _escape_like(), _is_code_conflict(), SqlAlchemyLinkRepository, _to_domain(), run(), run()

### Community 36 - "AccountForm"
Cohesion: 0.23
Nodes (13): AccountForm(), handleError(), handleLocaleChange(), handleProfileSubmit(), handleThemeChange(), ThemeToggle(), toggleTheme(), applyTheme() (+5 more)

### Community 37 - "build_services"
Cohesion: 0.15
Nodes (12): build_services(), AuthenticateAccess, AuthSession, Logout, AccessTokenIssuer, Clock, RotationStatus, SessionRepository (+4 more)

### Community 38 - "identity/presentation/router.py"
Cohesion: 0.14
Nodes (27): GoogleNotConfigured, get_authenticate_access(), get_get_me(), get_google_login(), get_google_oidc(), get_login(), get_logout(), get_refresh_session() (+19 more)

### Community 39 - "RedisAuthThrottle"
Cohesion: 0.16
Nodes (5): _digest(), RedisAuthThrottle, guarded(), operation(), ThrottleResult

### Community 40 - "test_identity_adapters.py"
Cohesion: 0.15
Nodes (7): build_session(), fast_hasher(), test_argon2_hasher_roundtrip_and_dummy(), test_cookie_prefix_disabled_when_domain_is_set(), test_cookies_are_httponly_except_csrf_and_samesite_lax(), test_google_exchange_never_decodes_an_unverified_id_token(), test_production_cookies_use_host_prefix_and_secure()

### Community 41 - "build_services"
Cohesion: 0.14
Nodes (6): AnalyticsServices, IdentityServices, LinkServices, _own_hosts(), SystemClock, utc_now()

### Community 42 - "deps.py"
Cohesion: 0.11
Nodes (31): get_cache(), get_current_user(), get_current_user_optional(), get_rate_limiter(), get_services(), get_session(), _rate_limit_error(), settings_dependency() (+23 more)

### Community 43 - "test_real_integrity_error_triggers_code_retry"
Cohesion: 0.21
Nodes (5): AllowedQuota, EmptyResolver, NoopCache, SequenceGenerator, test_real_integrity_error_triggers_code_retry()

### Community 44 - "LinkRepository"
Cohesion: 0.08
Nodes (16): GetLinkStats, StatsCache, StatsRepository, DeleteLink, UpdateLinkCommand, LinkNotFound, GetLink, GetLinksOverview (+8 more)

### Community 45 - "Settings"
Cohesion: 0.11
Nodes (29): _asyncpg_url(), _boolean(), _env(), get_migration_database_url(), get_settings(), _integer(), _is_strong_secret(), _number() (+21 more)

### Community 46 - "security_settings"
Cohesion: 0.22
Nodes (28): cleanup(), cleanup_email(), make_client(), security_settings(), seed_user(), unique_ip(), csrf_headers(), login() (+20 more)

### Community 47 - "list_links.py"
Cohesion: 0.22
Nodes (9): LinkPage, InvalidCursor, InvalidPagination, ListLinks, _normalize_query(), decode_cursor(), encode_cursor(), PageCursor (+1 more)

### Community 48 - "register.py"
Cohesion: 0.17
Nodes (8): AuthLocked, InvalidCredentials, InvalidEmail, WeakPassword, Login, AuthThrottle, PasswordHasher, Register

### Community 49 - "links-view.tsx"
Cohesion: 0.08
Nodes (34): LinksLoading(), ControlVisual(), FeatureBlocks(), ShortLinkVisual(), StatsVisual(), WEEKDAY_BARS, CopyLinkButton(), CopyLinkButtonProps (+26 more)

### Community 50 - "ref_next_intl"
Cohesion: 0.08
Nodes (34): dynamic, generateMetadata(), inter, jakarta, LocaleLayout(), LocaleLayoutProps, LocaleNotFound(), AccountFormProps (+26 more)

### Community 51 - "api.ts"
Cohesion: 0.07
Nodes (34): navigation, renderForm(), user, authState, renderForm(), api, ApiError, apiErrorFromResponse() (+26 more)

### Community 52 - "adapters/tokens.py"
Cohesion: 0.27
Nodes (5): PyJwtAccessTokens, AccessClaims, IssuedAccessToken, test_access_jwt_contains_minimal_claims_and_validates(), test_expired_access_token_is_rejected()

### Community 53 - "links/domain/entities.py"
Cohesion: 0.20
Nodes (10): ResolvedLink, _Unset, _as_utc(), _entry_state(), _resolved_from_cache(), _resolved_from_link(), ResolveLink, _as_utc() (+2 more)

### Community 54 - "RefreshTokenRecord"
Cohesion: 0.26
Nodes (5): _as_utc(), RefreshTokenRecord, TokenFamily, test_refresh_record_handles_naive_datetimes(), test_token_family_and_refresh_record_lifecycle()

### Community 55 - "register.py"
Cohesion: 0.18
Nodes (17): _number(), _string(), validate_google_claims(), PasswordPolicy, google_claims(), test_email_is_nfkc_normalized_and_lowercased(), test_email_rejects_invalid_values(), test_email_rejects_non_string_and_too_long() (+9 more)

### Community 56 - "config.py"
Cohesion: 0.19
Nodes (6): record_circuit_state(), record_click_dropped(), record_clicks_flushed(), record_rate_limit_fallback(), record_rate_limited(), _retry_after()

### Community 57 - "logging.py"
Cohesion: 0.15
Nodes (6): configure_logging(), get_logger(), MetricsMiddleware, _route_path(), record_request(), lifespan()

### Community 59 - ".__call__"
Cohesion: 0.20
Nodes (7): replay_body(), send_with_headers(), capture_status(), run(), tracked_send(), receive(), send()

### Community 60 - "BucketPolicy"
Cohesion: 0.14
Nodes (12): _headers(), _BucketState, _reset_seconds(), RateLimitResult, BucketPolicy, build_policies(), RedisTokenBucket, _reset_seconds() (+4 more)

### Community 61 - "User"
Cohesion: 0.15
Nodes (9): User, _revoke_family(), SqlAlchemySessionRepository, SqlAlchemyUserRepository, _to_user(), RotationResult, User, DuplicateUserError (+1 more)

### Community 62 - "ClickEvent"
Cohesion: 0.31
Nodes (3): ClickEvent, SqlAlchemyStatsRepository, RawStats

### Community 63 - "main.py"
Cohesion: 0.13
Nodes (6): test_metrics_accepts_valid_token(), test_metrics_rejects_wrong_token(), test_metrics_requires_token(), production_settings(), test_body_limit_is_enforced_by_the_full_app(), test_docs_and_openapi_are_disabled_in_production()

### Community 64 - "ref_vitest"
Cohesion: 0.22
Nodes (4): columns, ExternalLink(), ExternalLinkProps, safeExternalHref()

### Community 65 - "value_objects.py"
Cohesion: 0.12
Nodes (19): InvalidUrlError, ReservedAliasError, HostResolver, _normalize_own_host(), UrlPolicy, _normalize_host(), OriginalUrl, _validate_hostname() (+11 more)

### Community 66 - "[locale]/page.tsx"
Cohesion: 0.09
Nodes (21): HomePage(), HomePageProps, BackToTop(), MockIntersectionObserver, observers, renderBackToTop(), Faq(), FaqEntry (+13 more)

### Community 67 - "test_links_api.py"
Cohesion: 0.35
Nodes (13): api_settings(), cleanup(), direct_link(), seed_click(), seed_links(), seed_user(), test_anonymous_create_and_redirect(), test_create_rate_limit_returns_429() (+5 more)

### Community 68 - "pytest"
Cohesion: 0.31
Nodes (13): operation(), FakeResolver, policy(), test_credentials_controls_and_backslashes_are_blocked(), test_dns_rebinding_mixed_answers_are_all_checked(), test_forbidden_schemes_and_scheme_relative_urls_are_blocked(), test_global_ipv4_and_ipv6_answers_are_accepted(), test_obfuscated_or_internal_hostnames_are_blocked() (+5 more)

### Community 69 - "test_redirect_click_failure.py"
Cohesion: 0.29
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
Cohesion: 0.13
Nodes (13): GoogleOIDCClient, InvalidNextPath, google_callback(), _google_error_redirect(), allowed_origins(), csrf_protect(), frontend_url(), origin_guard() (+5 more)

### Community 75 - "register.py"
Cohesion: 0.26
Nodes (5): Email, InvalidEmailError, InvalidGoogleIdentityError, WeakPasswordError, _display_name()

### Community 76 - "error_handlers.py"
Cohesion: 0.11
Nodes (15): install_error_handlers(), handle_app_error(), handle_http_exception(), handle_unexpected_error(), handle_validation_error(), _json_error(), error_payload(), NotFoundError (+7 more)

### Community 77 - "seo.ts"
Cohesion: 0.17
Nodes (12): dynamic, GET(), generateMetadata(), sitemap(), buildLlmsTxt(), isProtectedPath(), languageAlternates(), localizedUrl() (+4 more)

### Community 79 - "redirect.js"
Cohesion: 0.06
Nodes (32): headers(), negative(), notFound, options, rateLimited, redirect(), stampede(), create() (+24 more)

### Community 80 - "test_click_pipeline.py"
Cohesion: 0.37
Nodes (9): RedisClickPublisher, admin_settings(), DownRedis, make_link(), pipeline_settings(), test_flusher_persists_batch_and_increments_click_count(), test_flusher_recreates_the_group_after_the_stream_is_lost(), test_flusher_retries_pending_entries() (+1 more)

### Community 81 - "RedisDailyQuota"
Cohesion: 0.21
Nodes (3): RedisDailyQuota, _seconds_until_next_utc_day(), QuotaResult

### Community 82 - "link_stats"
Cohesion: 0.21
Nodes (4): link_stats(), LinkStatsResponse, StatsBreakdownResponse, StatsSeriesPointResponse

### Community 83 - "Database"
Cohesion: 0.10
Nodes (19): Database, test_cleanup_deletes_old_clicks_and_expired_links_idempotently(), run(), run(), run(), run(), acleanup(), admin_settings() (+11 more)

### Community 84 - "Bulkhead"
Cohesion: 0.14
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
Cohesion: 0.13
Nodes (18): nextConfig, withNextIntl, buildRewrites(), isShortCodePath(), RESERVED_PATTERN, RESERVED_TOP_LEVEL, RewriteRule, RewritesConfig (+10 more)

### Community 91 - "Settings"
Cohesion: 0.24
Nodes (5): generate_csrf_token(), clear_session_cookies(), set_csrf_cookie(), set_session_cookies(), test_clear_cookies_deletes_all_session_cookies()

### Community 92 - "test_stats_api.py"
Cohesion: 0.58
Nodes (9): api_settings(), cleanup(), seed_clicks(), seed_link(), seed_user(), test_breakdowns_keep_top_ten_and_use_other_and_direct_sentinels(), test_stats_50k_clicks_benchmark(), test_stats_rate_limit_returns_429() (+1 more)

### Community 94 - "db/models.py"
Cohesion: 0.11
Nodes (11): upgrade(), Base, Link, RefreshToken, admin_settings(), make_link(), test_rls_blocks_cross_user_reads_even_without_app_filter(), acleanup_email() (+3 more)

### Community 95 - "test_sentry.py"
Cohesion: 0.38
Nodes (3): test_sentry_is_disabled_without_a_dsn(), fake_init(), test_sentry_scrubs_request_data_and_disables_pii()

### Community 96 - ".__init__"
Cohesion: 0.07
Nodes (21): CreateLink, AliasReserved, AliasTaken, CodeGenerationFailed, DailyQuotaExceeded, InvalidAlias, InvalidExpiresAt, InvalidTitle (+13 more)

### Community 98 - "Auditoria de segurança — P09"
Cohesion: 0.18
Nodes (10): Achados residuais aceitos (com justificativa), Auditoria de segurança — P09, Como reproduzir, Conclusão, Configuração de produção, O que não foi possível testar / limitações honestas, Resumo executivo, RLS — prova independente (+2 more)

### Community 99 - "env.py"
Cohesion: 0.32
Nodes (3): do_run_migrations(), run_async_migrations(), run_migrations_online()

### Community 101 - "HostResolutionError"
Cohesion: 0.19
Nodes (3): SystemHostResolver, HostResolutionError, FakeResolver

### Community 102 - "CacheClient"
Cohesion: 0.25
Nodes (4): FakeRedis, _sample(), test_cache_get_records_hit_and_miss(), test_cache_set_validates_ttl_and_delete()

### Community 103 - "test_production_hardening.py"
Cohesion: 0.39
Nodes (6): production_settings(), test_docs_openapi_metrics_and_security_headers_in_production(), test_metrics_is_not_exposed_with_a_development_token(), test_no_cors_headers_are_emitted(), test_production_cookies_are_secure_and_auth_responses_are_not_cached(), test_unexpected_errors_do_not_leak_stack_traces_or_validation_inputs()

### Community 104 - "Auditoria item a item — SECURITY.md"
Cohesion: 0.18
Nodes (11): test_only_config_module_reads_process_environment(), auth(), §10 Supply chain, §1 Token Bucket, §2 Resiliência / anti-DDoS, §3 Anti SQL Injection, §4 Anti XSS / injeção no front, §7 Credenciais e exposição (+3 more)

### Community 105 - "RateLimiter"
Cohesion: 0.10
Nodes (5): GlobalRateLimitMiddleware, DownRedis, test_global_bucket_is_shared_across_clients(), DownRedis, test_rate_limit_dependency_sets_headers_and_429()

### Community 106 - "UserRepository"
Cohesion: 0.17
Nodes (8): UpdateMeCommand, InvalidProfile, SessionExpired, GetMe, UserRepository, _normalize_display_name(), _normalize_locale(), UpdateMe

### Community 107 - "test_circuit_breaker.py"
Cohesion: 0.54
Nodes (5): fail(), test_breaker_half_open_failure_reopens(), test_breaker_half_open_success_closes(), test_breaker_opens_after_threshold_and_rejects_calls(), test_half_open_allows_only_configured_probes()

### Community 108 - "opengraph-image.tsx"
Cohesion: 0.40
Nodes (3): alt, contentType, size

### Community 109 - "google_login.py"
Cohesion: 0.80
Nodes (3): InvalidGoogleLogin, LoginWithGoogle, GoogleIdentity

## Knowledge Gaps
- **18 isolated node(s):** `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching`, `lucide-react 1.60.0`, `minimumReleaseAgeExclude Policy` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 502 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `test_link_cache.py`, `cleanup.py`, `ClickFlusher`, `database.py`, `CircuitBreaker`, `stats_cache.py`, `http.py`, `ShortCode`, `create_link`, `create_app`, `test_links_repository.py`, `build_services`, `identity/presentation/router.py`, `RedisAuthThrottle`, `test_identity_adapters.py`, `build_services`, `deps.py`, `test_real_integrity_error_triggers_code_retry`, `security_settings`, `adapters/tokens.py`, `config.py`, `logging.py`, `BucketPolicy`, `main.py`, `test_links_api.py`, `test_redirect_click_failure.py`, `security.py`, `test_click_pipeline.py`, `Database`, `Bulkhead`, `Deploy — Vercel (web) + Render (API/Postgres/Redis)`, `Settings`, `test_stats_api.py`, `sentry.py`, `db/models.py`, `test_sentry.py`, `Auditoria de segurança — P09`, `test_production_hardening.py`, `Auditoria item a item — SECURITY.md`?**
  _High betweenness centrality (0.255) - this node is a cross-community bridge._
- **Are the 108 inferred relationships involving `Settings` (e.g. with `settings_dependency()` and `configure_logging()`) actually correct?**
  _`Settings` has 108 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `shorten-form.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.10661268556005399 - nodes in this community are weakly interconnected._
- **Why does `§4 Anti XSS / injeção no front` connect `Auditoria item a item — SECURITY.md` to `proxy.ts`, `security_settings`?**
  _High betweenness centrality (0.154) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `ShortCode` (e.g. with `GetLinkStats` and `RedisLinkCache`) actually correct?**
  _`ShortCode` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_real_ip.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1368421052631579 - nodes in this community are weakly interconnected._