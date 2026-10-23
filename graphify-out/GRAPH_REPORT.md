# Graph Report - Tricolink  (2026-10-23)

## Corpus Check
- 286 files · ~142,744 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: (none) 10, .toml 1, .ini 1)

## Summary
- 2307 nodes · 7029 edges · 106 communities (94 shown, 12 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 960 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5c8e3908`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tricolink URL Shortener Product
- Token Bucket Rate Limiting
- test_link_cache.py
- shorten-form.tsx
- Agent Workflow and Graphify
- Compose and P01 Infra
- dataclasses
- AppError
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
- ratelimit/dependencies.py
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
- test_url_policy.py
- links/adapters/repository.py
- AccountForm
- build_services
- identity/presentation/router.py
- RedisAuthThrottle
- InvalidUrlError
- build_services
- links/presentation/router.py
- test_real_integrity_error_triggers_code_retry
- LinkRepository
- Settings
- security_settings
- list_links.py
- register.py
- links-view.tsx
- ref_next_intl
- api.ts
- error_handlers.py
- links/domain/entities.py
- identity/domain/entities.py
- register.py
- asyncio
- logging.py
- ids.py
- starlette_types
- BucketPolicy
- stats_repository.py
- identity/adapters/repository.py
- main.py
- ref_vitest
- OriginalUrl
- [locale]/page.tsx
- test_links_api.py
- create_redis
- test_redirect_click_failure.py
- HostResolutionError
- build_app
- token_bucket.js
- test_database_ready.py
- create.js
- request_context.py
- test_real_ip.py
- seo.ts
- redirect.js
- test_click_pipeline.py
- test_body_limit.py
- link_stats
- Database
- Bulkhead
- Deploy — Vercel (web) + Render (API/Postgres/Redis)
- Resultados
- i18n-check.mjs
- CodeGenerator
- proxy.ts
- update_me.py
- test_stats_api.py
- pytest
- db/models.py
- test_sentry.py
- .__init__
- .__call__
- Auditoria de segurança — P09
- env.py
- test_rate_limit_dependency_sets_headers_and_429
- HostResolver
- CacheClient
- opengraph-image.tsx
- .__call__
- UserRepository

## God Nodes (most connected - your core abstractions)
1. `Settings` - 154 edges
2. `ShortCode` - 95 edges
3. `Link` - 82 edges
4. `create_app()` - 63 edges
5. `build_services()` - 54 edges
6. `Database` - 47 edges
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

## Communities (106 total, 12 thin omitted)

### Community 0 - "Tricolink URL Shortener Product"
Cohesion: 0.25
Nodes (8): click_events Table, Redis Stream Click Buffer, Non-Goals, Tricolink URL Shortener Product, Redirect and Cache Hot Path, URL Anti-Abuse Policy, SSRF Prevention, Design Tokens

### Community 1 - "Token Bucket Rate Limiting"
Cohesion: 0.24
Nodes (9): Daily Link Quotas, Negative Cache for Unknown Codes, Single-Flight Lock, Stale-While-Revalidate Caching, Brute Force Protection, Bulkhead Semaphores, Circuit Breaker, Rate Limit Buckets (+1 more)

### Community 2 - "test_link_cache.py"
Cohesion: 0.30
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

### Community 6 - "dataclasses"
Cohesion: 0.15
Nodes (10): GlobalRateLimitMiddleware, _headers(), record_rate_limit_fallback(), record_rate_limited(), _reset_seconds(), RateLimitResult, RateLimiter, _retry_after() (+2 more)

### Community 7 - "AppError"
Cohesion: 0.10
Nodes (27): CreateLink, DeleteLink, UpdateLinkCommand, AliasReserved, AliasTaken, CodeGenerationFailed, DailyQuotaExceeded, InvalidAlias (+19 more)

### Community 8 - "MemoryTokenBucket"
Cohesion: 0.22
Nodes (9): _BucketState, MemoryTokenBucket, DownRedis, FakeClock, test_memory_bucket_consumes_and_exhausts(), test_memory_bucket_never_exceeds_capacity(), test_memory_bucket_refills(), test_rate_limiter_falls_back_to_memory_when_redis_is_down() (+1 more)

### Community 9 - "ClickFlusher"
Cohesion: 0.18
Nodes (6): ClickFlusher, read_group(), guarded(), operation(), guarded(), Achados corrigidos

### Community 10 - "BodyLimitMiddleware"
Cohesion: 0.26
Nodes (3): BodyLimitMiddleware, _header_values(), _send_json()

### Community 11 - "httpx"
Cohesion: 0.35
Nodes (7): build_inner(), test_hsts_only_in_production(), test_request_id_accepts_only_safe_values(), test_request_id_is_generated_and_returned(), test_security_headers_are_added(), test_timeout_allows_fast_requests(), test_timeout_returns_504()

### Community 15 - "login-form.tsx"
Cohesion: 0.15
Nodes (22): first(), generateMetadata(), LoginPage(), LoginPageProps, FieldError, FieldErrors, FormError, LoginForm() (+14 more)

### Community 19 - "CircuitBreaker"
Cohesion: 0.10
Nodes (3): CircuitBreaker, CircuitState, CircuitOpenError

### Community 20 - "stats_cache.py"
Cohesion: 0.09
Nodes (24): _breakdown(), _deserialize(), RedisStatsCache, _serialize(), load(), BreakdownItem, build_stats(), build_window() (+16 more)

### Community 21 - "demo-dashboard.tsx"
Cohesion: 0.08
Nodes (37): BreakdownColumns, BreakdownRow, BreakdownTable(), BreakdownTableProps, ClicksChart(), ClicksChartProps, ClicksPoint, ChartPlaceholder() (+29 more)

### Community 22 - "ratelimit/dependencies.py"
Cohesion: 0.19
Nodes (13): _rate_limit_error(), user_rate_limit(), dependency(), apply_rate_limit_headers(), client_ip(), _get_limiter(), rate_limit(), dependency() (+5 more)

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
Nodes (14): jittered_ttl(), _CacheRead, _entry_from_link(), RedisLinkCache, CacheEntry, Link, ShortCode, _link() (+6 more)

### Community 28 - "click.py"
Cohesion: 0.16
Nodes (13): _parse_event(), _browser(), ClickEvent, extract_referrer_host(), normalize_country(), parse_user_agent(), UserAgentInfo, ClickPublisher (+5 more)

### Community 29 - "create_link"
Cohesion: 0.13
Nodes (15): CurrentUser, create_link(), delete_link(), get_link(), _link_response(), links_overview(), list_links(), redirect_link() (+7 more)

### Community 30 - "test_links_application.py"
Cohesion: 0.09
Nodes (27): RedisDailyQuota, _seconds_until_next_utc_day(), CreateLinkCommand, QuotaResult, build_create(), build_link(), FakeCache, FakeClock (+19 more)

### Community 31 - "isLocale"
Cohesion: 0.18
Nodes (21): AccountPage(), AccountPageProps, generateMetadata(), generateMetadata(), LinkDetailPage(), LinkDetailPageProps, generateMetadata(), LinksPage() (+13 more)

### Community 32 - "test_identity_application.py"
Cohesion: 0.09
Nodes (29): PyJwtAccessTokens, LoginCommand, RegisterCommand, AccessClaims, IssuedAccessToken, test_access_jwt_contains_minimal_claims_and_validates(), test_expired_access_token_is_rejected(), build_issuer() (+21 more)

### Community 33 - "create_app"
Cohesion: 0.18
Nodes (24): create_app(), admin_settings(), cleanup(), run(), FakeGoogleOIDC, google_claims(), identity_settings(), login() (+16 more)

### Community 34 - "test_url_policy.py"
Cohesion: 0.24
Nodes (13): is_blocked_ip(), build_policy(), test_is_blocked_ip_allows_only_global_addresses(), test_is_blocked_ip_blocks_non_global_addresses(), test_url_policy_accepts_public_urls(), test_url_policy_blocks_host_when_resolution_fails_or_is_empty(), test_url_policy_blocks_invalid_dns_answer(), test_url_policy_blocks_own_domain_and_subdomains_without_dns() (+5 more)

### Community 35 - "links/adapters/repository.py"
Cohesion: 0.18
Nodes (10): _escape_like(), _is_code_conflict(), _to_domain(), PageCursor, admin_settings(), build_link(), cleanup(), seed_user() (+2 more)

### Community 36 - "AccountForm"
Cohesion: 0.23
Nodes (13): AccountForm(), handleError(), handleLocaleChange(), handleProfileSubmit(), handleThemeChange(), ThemeToggle(), toggleTheme(), applyTheme() (+5 more)

### Community 37 - "build_services"
Cohesion: 0.16
Nodes (8): Logout, AccessTokenIssuer, Clock, RotationStatus, SessionRepository, RefreshSession, generate_refresh_token(), hash_refresh_token()

### Community 38 - "identity/presentation/router.py"
Cohesion: 0.05
Nodes (52): GoogleOIDCClient, GoogleNotConfigured, InvalidNextPath, generate_csrf_token(), clear_session_cookies(), set_csrf_cookie(), set_session_cookies(), get_authenticate_access() (+44 more)

### Community 39 - "RedisAuthThrottle"
Cohesion: 0.16
Nodes (5): _digest(), RedisAuthThrottle, guarded(), operation(), ThrottleResult

### Community 40 - "InvalidUrlError"
Cohesion: 0.32
Nodes (13): operation(), InvalidUrlError, policy(), test_credentials_controls_and_backslashes_are_blocked(), test_dns_rebinding_mixed_answers_are_all_checked(), test_forbidden_schemes_and_scheme_relative_urls_are_blocked(), test_global_ipv4_and_ipv6_answers_are_accepted(), test_obfuscated_or_internal_hostnames_are_blocked() (+5 more)

### Community 41 - "build_services"
Cohesion: 0.16
Nodes (7): AnalyticsServices, build_services(), IdentityServices, LinkServices, _own_hosts(), SystemClock, utc_now()

### Community 42 - "links/presentation/router.py"
Cohesion: 0.25
Nodes (17): get_cache(), get_current_user(), get_current_user_optional(), get_rate_limiter(), get_services(), get_session(), settings_dependency(), get_click_publisher() (+9 more)

### Community 43 - "test_real_integrity_error_triggers_code_retry"
Cohesion: 0.12
Nodes (8): AllowedQuota, EmptyResolver, NoopCache, SequenceGenerator, test_real_integrity_error_triggers_code_retry(), CountingRepository, NoopRecordClick, test_200_concurrent_cold_redirects_hit_the_database_once()

### Community 44 - "LinkRepository"
Cohesion: 0.11
Nodes (8): GetLinkStats, StatsCache, StatsRepository, get_get_link_stats(), GetLink, GetLinksOverview, LinksOverview, LinkRepository

### Community 45 - "Settings"
Cohesion: 0.10
Nodes (29): _asyncpg_url(), _boolean(), _env(), get_migration_database_url(), get_settings(), _integer(), _is_strong_secret(), _number() (+21 more)

### Community 46 - "security_settings"
Cohesion: 0.15
Nodes (35): test_cleanup_deletes_old_clicks_and_expired_links_idempotently(), cleanup(), cleanup_email(), make_client(), security_settings(), seed_link(), seed_user(), unique_ip() (+27 more)

### Community 47 - "list_links.py"
Cohesion: 0.23
Nodes (8): LinkPage, InvalidCursor, InvalidPagination, ListLinks, _normalize_query(), decode_cursor(), encode_cursor(), test_cursor_roundtrip_and_rejection()

### Community 48 - "register.py"
Cohesion: 0.13
Nodes (14): AuthLocked, InvalidCredentials, InvalidEmail, WeakPassword, Login, AuthThrottle, PasswordHasher, Register (+6 more)

### Community 49 - "links-view.tsx"
Cohesion: 0.08
Nodes (34): LinksLoading(), ControlVisual(), FeatureBlocks(), ShortLinkVisual(), StatsVisual(), WEEKDAY_BARS, CopyLinkButton(), CopyLinkButtonProps (+26 more)

### Community 50 - "ref_next_intl"
Cohesion: 0.08
Nodes (34): dynamic, generateMetadata(), inter, jakarta, LocaleLayout(), LocaleLayoutProps, LocaleNotFound(), AccountFormProps (+26 more)

### Community 51 - "api.ts"
Cohesion: 0.07
Nodes (34): navigation, renderForm(), user, authState, renderForm(), api, ApiError, apiErrorFromResponse() (+26 more)

### Community 52 - "error_handlers.py"
Cohesion: 0.19
Nodes (7): install_error_handlers(), handle_app_error(), handle_http_exception(), handle_unexpected_error(), handle_validation_error(), _json_error(), error_payload()

### Community 53 - "links/domain/entities.py"
Cohesion: 0.20
Nodes (10): ResolvedLink, _Unset, _as_utc(), _entry_state(), _resolved_from_cache(), _resolved_from_link(), ResolveLink, _as_utc() (+2 more)

### Community 54 - "identity/domain/entities.py"
Cohesion: 0.17
Nodes (10): AuthSession, InvalidGoogleLogin, LoginWithGoogle, SessionIssuer, _as_utc(), RefreshTokenRecord, TokenFamily, GoogleIdentity (+2 more)

### Community 55 - "register.py"
Cohesion: 0.18
Nodes (16): InvalidGoogleIdentityError, _display_name(), _number(), _string(), validate_google_claims(), google_claims(), test_email_is_nfkc_normalized_and_lowercased(), test_email_rejects_invalid_values() (+8 more)

### Community 56 - "asyncio"
Cohesion: 0.13
Nodes (7): ping_redis(), unit_of_work(), record_cache_hit(), record_cache_miss(), record_circuit_state(), record_click_dropped(), record_clicks_flushed()

### Community 57 - "logging.py"
Cohesion: 0.24
Nodes (3): MetricsMiddleware, _route_path(), record_request()

### Community 59 - "starlette_types"
Cohesion: 0.13
Nodes (3): SecurityHeadersMiddleware, send_with_headers(), RequestTimeoutMiddleware

### Community 60 - "BucketPolicy"
Cohesion: 0.14
Nodes (9): BucketPolicy, build_policies(), RedisTokenBucket, _reset_seconds(), TokenBucketBackend, test_lua_bucket_consumes_exhausts_and_refills(), test_lua_bucket_is_atomic_under_concurrency(), test_lua_bucket_keeps_keys_independent() (+1 more)

### Community 62 - "identity/adapters/repository.py"
Cohesion: 0.22
Nodes (4): set_rls_context(), _revoke_family(), SqlAlchemySessionRepository, RotationResult

### Community 63 - "main.py"
Cohesion: 0.09
Nodes (8): configure_logging(), get_logger(), init_sentry(), _scrub_event(), lifespan(), production_settings(), test_body_limit_is_enforced_by_the_full_app(), test_docs_and_openapi_are_disabled_in_production()

### Community 64 - "ref_vitest"
Cohesion: 0.22
Nodes (4): columns, ExternalLink(), ExternalLinkProps, safeExternalHref()

### Community 65 - "OriginalUrl"
Cohesion: 0.25
Nodes (12): OriginalUrl, test_link_state_accounts_for_expiry_and_active_flag(), test_link_with_updates_returns_a_new_entity(), test_original_url_keeps_ipv6_literal_brackets(), test_original_url_normalizes_idn_to_punycode(), test_original_url_normalizes_scheme_host_and_idn(), test_original_url_rejects_invalid_host_shapes(), test_original_url_rejects_malformed_or_dangerous_values() (+4 more)

### Community 66 - "[locale]/page.tsx"
Cohesion: 0.09
Nodes (21): HomePage(), HomePageProps, BackToTop(), MockIntersectionObserver, observers, renderBackToTop(), Faq(), FaqEntry (+13 more)

### Community 67 - "test_links_api.py"
Cohesion: 0.28
Nodes (15): api_settings(), cleanup(), direct_link(), seed_click(), run(), seed_links(), seed_user(), run() (+7 more)

### Community 68 - "create_redis"
Cohesion: 0.18
Nodes (7): close_redis(), create_redis(), redis_client(), run(), read_stream(), run(), redis_client()

### Community 69 - "test_redirect_click_failure.py"
Cohesion: 0.29
Nodes (5): BlockingPublisher, click_settings(), DownRedis, test_redirect_continues_and_metric_counts_dropped_click(), test_redirect_does_not_wait_for_click_publisher()

### Community 70 - "HostResolutionError"
Cohesion: 0.19
Nodes (4): SystemHostResolver, HostResolutionError, FakeResolver, FakeResolver

### Community 71 - "build_app"
Cohesion: 0.24
Nodes (8): NotFoundError, build_app(), missing(), test_app_error_uses_standard_envelope(), test_security_error_uses_standard_envelope(), test_unhandled_error_does_not_leak_stack_trace(), test_unknown_route_uses_standard_envelope(), test_validation_error_uses_standard_envelope()

### Community 72 - "token_bucket.js"
Cohesion: 0.21
Nodes (9): headers(), negative(), notFound, options, rateLimited, redirect(), stampede(), auth() (+1 more)

### Community 73 - "test_database_ready.py"
Cohesion: 0.23
Nodes (5): _database_with_schema(), _FakeConnection, _FakeEngine, test_check_ready_accepts_migrated_schema(), test_check_ready_rejects_missing_schema()

### Community 74 - "create.js"
Cohesion: 0.21
Nodes (10): create(), created, createDuration, createLink(), createWithSharedIp(), options, otherStatuses, rateLimited (+2 more)

### Community 75 - "request_context.py"
Cohesion: 0.22
Nodes (3): _incoming_request_id(), RequestIDMiddleware, send_with_request_id()

### Community 76 - "test_real_ip.py"
Cohesion: 0.13
Nodes (9): _forwarded_for(), RealIPMiddleware, resolve_real_ip(), _normalize_host(), _NeverRedis, test_middleware_sets_request_client_to_real_ip(), test_resolve_real_ip_counts_from_the_right(), test_resolve_real_ip_falls_back_when_header_is_invalid_or_short() (+1 more)

### Community 77 - "seo.ts"
Cohesion: 0.17
Nodes (12): dynamic, GET(), generateMetadata(), sitemap(), buildLlmsTxt(), isProtectedPath(), languageAlternates(), localizedUrl() (+4 more)

### Community 79 - "redirect.js"
Cohesion: 0.13
Nodes (15): CODE_TTL_SECONDS, cold(), COLD_CODES, createIp(), options, otherStatuses, rateLimited, redirectDuration (+7 more)

### Community 80 - "test_click_pipeline.py"
Cohesion: 0.30
Nodes (12): RedisClickPublisher, SqlAlchemyLinkRepository, admin_settings(), DownRedis, make_link(), pipeline_settings(), test_flusher_persists_batch_and_increments_click_count(), test_flusher_recreates_the_group_after_the_stream_is_lost() (+4 more)

### Community 81 - "test_body_limit.py"
Cohesion: 0.33
Nodes (5): build_app(), test_accepts_body_at_limit(), test_invalid_content_length_is_rejected(), test_rejects_chunked_body_above_limit(), test_rejects_content_length_above_limit_before_reading()

### Community 82 - "link_stats"
Cohesion: 0.26
Nodes (4): link_stats(), LinkStatsResponse, StatsBreakdownResponse, StatsSeriesPointResponse

### Community 83 - "Database"
Cohesion: 0.14
Nodes (12): Database, acleanup(), admin_settings(), aseed_click(), aseed_link(), aseed_user(), expires_in(), seed_click() (+4 more)

### Community 84 - "Bulkhead"
Cohesion: 0.07
Nodes (17): Services, _authorized(), _check_database(), _check_redis(), health_live(), health_ready(), HealthResponse, metrics() (+9 more)

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
Cohesion: 0.27
Nodes (5): CodeGenerator, _validate_hostname(), test_code_generator_can_be_made_deterministic(), test_code_generator_uses_seven_base62_characters(), test_code_generator_validates_configuration()

### Community 89 - "proxy.ts"
Cohesion: 0.13
Nodes (18): nextConfig, withNextIntl, buildRewrites(), isShortCodePath(), RESERVED_PATTERN, RESERVED_TOP_LEVEL, RewriteRule, RewritesConfig (+10 more)

### Community 91 - "update_me.py"
Cohesion: 0.44
Nodes (6): UpdateMeCommand, InvalidProfile, SessionExpired, _normalize_display_name(), _normalize_locale(), UpdateMe

### Community 92 - "test_stats_api.py"
Cohesion: 0.44
Nodes (11): api_settings(), cleanup(), seed_clicks(), run(), seed_link(), seed_user(), run(), test_breakdowns_keep_top_ten_and_use_other_and_direct_sentinels() (+3 more)

### Community 93 - "pytest"
Cohesion: 0.56
Nodes (5): fail(), test_breaker_half_open_failure_reopens(), test_breaker_half_open_success_closes(), test_breaker_opens_after_threshold_and_rejects_calls(), test_half_open_allows_only_configured_probes()

### Community 94 - "db/models.py"
Cohesion: 0.10
Nodes (17): Base, ClickEvent, Link, RefreshToken, User, CleanupResult, _delete_batch(), main() (+9 more)

### Community 95 - "test_sentry.py"
Cohesion: 0.38
Nodes (3): test_sentry_is_disabled_without_a_dsn(), fake_init(), test_sentry_scrubs_request_data_and_disables_pii()

### Community 96 - ".__init__"
Cohesion: 0.07
Nodes (6): BadRequestError, ConflictError, GatewayTimeoutError, PayloadTooLargeError, ServiceUnavailableError, AuthorizationError

### Community 97 - ".__call__"
Cohesion: 0.29
Nodes (4): replay_body(), run(), tracked_send(), receive()

### Community 98 - "Auditoria de segurança — P09"
Cohesion: 0.10
Nodes (20): test_only_config_module_reads_process_environment(), §10 Supply chain, §2 Resiliência / anti-DDoS, §3 Anti SQL Injection, §4 Anti XSS / injeção no front, §5 Autenticação, sessão e força bruta, §7 Credenciais e exposição, §8 Buffer overflow / limites (+12 more)

### Community 99 - "env.py"
Cohesion: 0.19
Nodes (4): do_run_migrations(), run_async_migrations(), run_migrations_online(), upgrade()

### Community 102 - "CacheClient"
Cohesion: 0.16
Nodes (5): CacheClient, FakeRedis, _sample(), test_cache_get_records_hit_and_miss(), test_cache_set_validates_ttl_and_delete()

### Community 103 - "opengraph-image.tsx"
Cohesion: 0.40
Nodes (3): alt, contentType, size

### Community 105 - ".__call__"
Cohesion: 0.29
Nodes (3): send_with_headers(), capture_status(), send()

### Community 106 - "UserRepository"
Cohesion: 0.12
Nodes (7): SqlAlchemyUserRepository, _to_user(), AuthenticateAccess, GetMe, UserRepository, User, DuplicateUserError

## Knowledge Gaps
- **18 isolated node(s):** `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching`, `lucide-react 1.60.0`, `minimumReleaseAgeExclude Policy` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 508 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `test_link_cache.py`, `dataclasses`, `ClickFlusher`, `database.py`, `CircuitBreaker`, `stats_cache.py`, `ShortCode`, `create_link`, `test_identity_application.py`, `create_app`, `links/adapters/repository.py`, `identity/presentation/router.py`, `RedisAuthThrottle`, `build_services`, `links/presentation/router.py`, `test_real_integrity_error_triggers_code_retry`, `security_settings`, `asyncio`, `BucketPolicy`, `main.py`, `test_links_api.py`, `create_redis`, `test_redirect_click_failure.py`, `test_database_ready.py`, `test_click_pipeline.py`, `Database`, `Bulkhead`, `Deploy — Vercel (web) + Render (API/Postgres/Redis)`, `test_stats_api.py`, `db/models.py`, `test_sentry.py`, `Auditoria de segurança — P09`?**
  _High betweenness centrality (0.239) - this node is a cross-community bridge._
- **Are the 109 inferred relationships involving `Settings` (e.g. with `settings_dependency()` and `configure_logging()`) actually correct?**
  _`Settings` has 109 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `shorten-form.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.10661268556005399 - nodes in this community are weakly interconnected._
- **Why does `§4 Anti XSS / injeção no front` connect `Auditoria de segurança — P09` to `proxy.ts`, `security_settings`?**
  _High betweenness centrality (0.134) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `ShortCode` (e.g. with `GetLinkStats` and `RedisLinkCache`) actually correct?**
  _`ShortCode` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Should `dataclasses` be split into smaller, more focused modules?**
  _Cohesion score 0.1471264367816092 - nodes in this community are weakly interconnected._