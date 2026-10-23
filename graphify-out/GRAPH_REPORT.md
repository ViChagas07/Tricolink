# Graph Report - Tricolink  (2026-10-22)

## Corpus Check
- 285 files · ~167,016 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: (none) 10, .toml 1, .ini 1)

## Summary
- 2283 nodes · 6970 edges · 104 communities (95 shown, 9 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 956 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ae92d227`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tricolink URL Shortener Product
- Token Bucket Rate Limiting
- AppError
- identity/presentation/router.py
- Agent Workflow and Graphify
- Compose and P01 Infra
- db/models.py
- test_real_ip.py
- MemoryTokenBucket
- cleanup.py
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
- identity/adapters/repository.py
- api.ts
- build_services
- identity/presentation/router.py
- test_url_policy.py
- ClickFlusher
- build_services
- dataclasses
- pytest
- resolve_link.py
- Settings
- helpers.py
- list_links.py
- Register
- links-view.tsx
- ref_next_intl
- FakeSessionRepository
- adapters/google.py
- google_callback
- test_identity_domain.py
- Email
- config.py
- error_handlers.py
- ids.py
- starlette_types
- BucketPolicy
- User
- test_click_pipeline.py
- identity/domain/entities.py
- shorten-form.tsx
- OriginalUrl
- build_app
- test_links_api.py
- create_redis
- test_redirect_click_failure.py
- request_context.py
- test_body_limit.py
- RateLimiter
- CacheClient
- security.py
- test_link_cache.py
- token_bucket.js
- get_services
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
- create.js
- test_link_collision.py
- main.py
- HostResolutionError
- test_sentry.py
- .__call__
- opengraph-image.tsx
- Auditoria de segurança — P09
- .__call__
- Auditoria item a item — SECURITY.md
- storeTheme
- jittered_ttl
- google_login.py

## God Nodes (most connected - your core abstractions)
1. `Settings` - 149 edges
2. `ShortCode` - 95 edges
3. `Link` - 82 edges
4. `create_app()` - 61 edges
5. `build_services()` - 54 edges
6. `Database` - 45 edges
7. `User` - 45 edges
8. `AppError` - 43 edges
9. `OriginalUrl` - 37 edges
10. `cn()` - 37 edges

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

## Communities (104 total, 9 thin omitted)

### Community 0 - "Tricolink URL Shortener Product"
Cohesion: 0.25
Nodes (8): click_events Table, Redis Stream Click Buffer, Non-Goals, Tricolink URL Shortener Product, Redirect and Cache Hot Path, URL Anti-Abuse Policy, SSRF Prevention, Design Tokens

### Community 1 - "Token Bucket Rate Limiting"
Cohesion: 0.24
Nodes (9): Daily Link Quotas, Negative Cache for Unknown Codes, Single-Flight Lock, Stale-While-Revalidate Caching, Brute Force Protection, Bulkhead Semaphores, Circuit Breaker, Rate Limit Buckets (+1 more)

### Community 2 - "AppError"
Cohesion: 0.07
Nodes (22): CreateLink, AliasReserved, AliasTaken, CodeGenerationFailed, DailyQuotaExceeded, InvalidAlias, InvalidExpiresAt, InvalidTitle (+14 more)

### Community 3 - "identity/presentation/router.py"
Cohesion: 0.25
Nodes (9): get_authenticate_access(), get_get_me(), get_google_login(), get_google_oidc(), get_login(), get_logout(), get_refresh_session(), get_register() (+1 more)

### Community 4 - "Agent Workflow and Graphify"
Cohesion: 0.18
Nodes (8): graphify Slash Command, Mandatory Session Reading Order, CONTEXT.md Single Source of Truth, Graphify Context Engineering, Graphify Installation Commands, Per-Phase Graphify Routine, graphify query/path/explain Workflow, Tricolink README Stub (P11)

### Community 5 - "Compose and P01 Infra"
Cohesion: 0.16
Nodes (20): pnpm allowBuilds Allowlist, API Compose Service, app Network, data Network, postgres_data Volume, PostgreSQL 16 Compose Service, Redis 7 Compose Service, Web Compose Service (+12 more)

### Community 6 - "db/models.py"
Cohesion: 0.12
Nodes (8): upgrade(), Base, ClickEvent, User, SqlAlchemyStatsRepository, test_click_events_have_device_check_and_index(), test_links_have_required_constraints_and_indexes(), test_users_and_refresh_tokens_have_required_uniques()

### Community 7 - "test_real_ip.py"
Cohesion: 0.13
Nodes (9): _forwarded_for(), RealIPMiddleware, resolve_real_ip(), _normalize_host(), _NeverRedis, test_middleware_sets_request_client_to_real_ip(), test_resolve_real_ip_counts_from_the_right(), test_resolve_real_ip_falls_back_when_header_is_invalid_or_short() (+1 more)

### Community 8 - "MemoryTokenBucket"
Cohesion: 0.22
Nodes (9): _BucketState, MemoryTokenBucket, DownRedis, FakeClock, test_memory_bucket_consumes_and_exhausts(), test_memory_bucket_never_exceeds_capacity(), test_memory_bucket_refills(), test_rate_limiter_falls_back_to_memory_when_redis_is_down() (+1 more)

### Community 9 - "cleanup.py"
Cohesion: 0.15
Nodes (8): get_settings(), configure_logging(), get_logger(), CleanupResult, _delete_batch(), main(), run_cleanup(), lifespan()

### Community 10 - "BodyLimitMiddleware"
Cohesion: 0.26
Nodes (3): BodyLimitMiddleware, _header_values(), _send_json()

### Community 11 - "httpx"
Cohesion: 0.25
Nodes (8): SecurityHeadersMiddleware, build_inner(), test_hsts_only_in_production(), test_request_id_accepts_only_safe_values(), test_request_id_is_generated_and_returned(), test_security_headers_are_added(), test_timeout_allows_fast_requests(), test_timeout_returns_504()

### Community 15 - "User"
Cohesion: 0.44
Nodes (6): UpdateMeCommand, InvalidProfile, SessionExpired, _normalize_display_name(), _normalize_locale(), UpdateMe

### Community 18 - "database.py"
Cohesion: 0.14
Nodes (6): do_run_migrations(), run_async_migrations(), run_migrations_online(), create_engine(), create_session_factory(), unit_of_work()

### Community 19 - "pytest"
Cohesion: 0.06
Nodes (13): CircuitBreaker, CircuitState, _digest(), RedisAuthThrottle, guarded(), operation(), ThrottleResult, CircuitOpenError (+5 more)

### Community 20 - "stats_cache.py"
Cohesion: 0.06
Nodes (33): _breakdown(), _deserialize(), RedisStatsCache, _serialize(), GetLinkStats, load(), RawStats, StatsCache (+25 more)

### Community 21 - "demo-dashboard.tsx"
Cohesion: 0.08
Nodes (37): BreakdownColumns, BreakdownRow, BreakdownTable(), BreakdownTableProps, ClicksChart(), ClicksChartProps, ClicksPoint, ChartPlaceholder() (+29 more)

### Community 22 - "http.py"
Cohesion: 0.16
Nodes (10): Services, ping_redis(), _authorized(), _check_database(), _check_redis(), health_live(), health_ready(), HealthResponse (+2 more)

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
Cohesion: 0.13
Nodes (10): _CacheRead, _entry_from_link(), RedisLinkCache, CacheEntry, Link, ShortCode, CountingRepository, NoopRecordClick (+2 more)

### Community 28 - "ClickEvent"
Cohesion: 0.16
Nodes (13): _parse_event(), _browser(), ClickEvent, extract_referrer_host(), normalize_country(), parse_user_agent(), UserAgentInfo, ClickPublisher (+5 more)

### Community 29 - "create_link"
Cohesion: 0.16
Nodes (16): CurrentUser, get_current_user(), create_link(), delete_link(), get_link(), _link_response(), links_overview(), list_links() (+8 more)

### Community 30 - "test_links_application.py"
Cohesion: 0.13
Nodes (24): CreateLinkCommand, build_create(), build_link(), FakeCache, FakeClock, FakeGenerator, FakePublisher, FakeQuota (+16 more)

### Community 31 - "ref_next_intl"
Cohesion: 0.10
Nodes (39): AccountPage(), AccountPageProps, generateMetadata(), generateMetadata(), LinkDetailPage(), LinkDetailPageProps, generateMetadata(), LinksPage() (+31 more)

### Community 32 - "pytest"
Cohesion: 0.21
Nodes (23): LoginCommand, RegisterCommand, build_issuer(), build_login(), build_register(), FakeAccessTokens, FakeClock, FakeHasher (+15 more)

### Community 33 - "create_app"
Cohesion: 0.22
Nodes (21): create_app(), admin_settings(), cleanup(), run(), FakeGoogleOIDC, google_claims(), identity_settings(), login() (+13 more)

### Community 34 - "links/adapters/repository.py"
Cohesion: 0.13
Nodes (17): Link, _escape_like(), _is_code_conflict(), SqlAlchemyLinkRepository, _to_domain(), PageCursor, DuplicateCodeError, test_real_integrity_error_triggers_code_retry() (+9 more)

### Community 35 - "identity/adapters/repository.py"
Cohesion: 0.20
Nodes (7): RefreshToken, set_rls_context(), _revoke_family(), SqlAlchemySessionRepository, RotationResult, admin_settings(), test_rls_blocks_cross_user_reads_even_without_app_filter()

### Community 36 - "api.ts"
Cohesion: 0.07
Nodes (44): AccountForm(), handleError(), handleLocaleChange(), handleProfileSubmit(), FieldError, FieldErrors, FormError, LoginForm() (+36 more)

### Community 37 - "build_services"
Cohesion: 0.16
Nodes (10): AuthSession, Logout, AccessTokenIssuer, Clock, RotationStatus, SessionRepository, RefreshSession, SessionIssuer (+2 more)

### Community 38 - "identity/presentation/router.py"
Cohesion: 0.19
Nodes (16): _client_ip(), csrf_token(), login(), logout(), me(), refresh(), register(), update_me() (+8 more)

### Community 39 - "test_url_policy.py"
Cohesion: 0.21
Nodes (14): is_blocked_ip(), build_policy(), FakeResolver, test_is_blocked_ip_allows_only_global_addresses(), test_is_blocked_ip_blocks_non_global_addresses(), test_url_policy_accepts_public_urls(), test_url_policy_blocks_host_when_resolution_fails_or_is_empty(), test_url_policy_blocks_invalid_dns_answer() (+6 more)

### Community 40 - "ClickFlusher"
Cohesion: 0.18
Nodes (6): ClickFlusher, read_group(), guarded(), operation(), guarded(), Achados corrigidos

### Community 41 - "build_services"
Cohesion: 0.09
Nodes (11): AnalyticsServices, build_services(), IdentityServices, LinkServices, _own_hosts(), RedisDailyQuota, _seconds_until_next_utc_day(), build_policies() (+3 more)

### Community 42 - "dataclasses"
Cohesion: 0.13
Nodes (20): get_rate_limiter(), _rate_limit_error(), user_rate_limit(), dependency(), _headers(), record_rate_limit_fallback(), record_rate_limited(), apply_rate_limit_headers() (+12 more)

### Community 43 - "pytest"
Cohesion: 0.34
Nodes (13): operation(), InvalidUrlError, policy(), test_credentials_controls_and_backslashes_are_blocked(), test_dns_rebinding_mixed_answers_are_all_checked(), test_forbidden_schemes_and_scheme_relative_urls_are_blocked(), test_global_ipv4_and_ipv6_answers_are_accepted(), test_obfuscated_or_internal_hostnames_are_blocked() (+5 more)

### Community 44 - "resolve_link.py"
Cohesion: 0.22
Nodes (10): ResolvedLink, _Unset, _as_utc(), _entry_state(), _resolved_from_cache(), _resolved_from_link(), ResolveLink, _as_utc() (+2 more)

### Community 45 - "Settings"
Cohesion: 0.08
Nodes (33): _asyncpg_url(), _boolean(), _env(), get_migration_database_url(), _integer(), _number(), Settings, SettingsError (+25 more)

### Community 46 - "helpers.py"
Cohesion: 0.17
Nodes (33): cleanup(), cleanup_email(), make_client(), security_settings(), seed_link(), seed_user(), unique_ip(), csrf_headers() (+25 more)

### Community 47 - "list_links.py"
Cohesion: 0.23
Nodes (8): LinkPage, InvalidCursor, InvalidPagination, ListLinks, _normalize_query(), decode_cursor(), encode_cursor(), test_cursor_roundtrip_and_rejection()

### Community 48 - "Register"
Cohesion: 0.20
Nodes (4): InvalidCredentials, Login, AuthThrottle, PasswordHasher

### Community 49 - "links-view.tsx"
Cohesion: 0.08
Nodes (37): LinksLoading(), CopyLinkButton(), CopyLinkButtonProps, DeleteLinkDialog(), DeleteLinkDialogProps, EditErrors, EditLinkDialog(), handleSubmit() (+29 more)

### Community 50 - "ref_next_intl"
Cohesion: 0.10
Nodes (29): dynamic, generateMetadata(), inter, jakarta, LocaleLayout(), LocaleLayoutProps, LinkDetailError(), LocaleNotFound() (+21 more)

### Community 52 - "adapters/google.py"
Cohesion: 0.27
Nodes (5): PyJwtAccessTokens, AccessClaims, IssuedAccessToken, test_access_jwt_contains_minimal_claims_and_validates(), test_expired_access_token_is_rejected()

### Community 53 - "google_callback"
Cohesion: 0.15
Nodes (7): GoogleOIDCClient, GoogleNotConfigured, google_callback(), _google_error_redirect(), google_login(), frontend_url(), test_google_exchange_never_decodes_an_unverified_id_token()

### Community 54 - "test_identity_domain.py"
Cohesion: 0.20
Nodes (14): _number(), _string(), validate_google_claims(), google_claims(), test_email_is_nfkc_normalized_and_lowercased(), test_email_rejects_invalid_values(), test_email_rejects_non_string_and_too_long(), test_google_claims_accept_audience_list_and_string_verified() (+6 more)

### Community 55 - "Email"
Cohesion: 0.17
Nodes (12): AuthLocked, InvalidEmail, WeakPassword, Register, Email, InvalidEmailError, InvalidGoogleIdentityError, WeakPasswordError (+4 more)

### Community 56 - "config.py"
Cohesion: 0.17
Nodes (6): record_cache_hit(), record_cache_miss(), record_circuit_state(), record_click_dropped(), record_clicks_flushed(), _retry_after()

### Community 57 - "error_handlers.py"
Cohesion: 0.19
Nodes (7): install_error_handlers(), handle_app_error(), handle_http_exception(), handle_unexpected_error(), handle_validation_error(), _json_error(), error_payload()

### Community 59 - "starlette_types"
Cohesion: 0.15
Nodes (5): replay_body(), RequestTimeoutMiddleware, run(), tracked_send(), receive()

### Community 60 - "BucketPolicy"
Cohesion: 0.17
Nodes (7): BucketPolicy, RedisTokenBucket, _reset_seconds(), TokenBucketBackend, test_lua_bucket_consumes_exhausts_and_refills(), test_lua_bucket_is_atomic_under_concurrency(), test_lua_bucket_keeps_keys_independent()

### Community 61 - "User"
Cohesion: 0.12
Nodes (8): SqlAlchemyUserRepository, _to_user(), AuthenticateAccess, GetMe, UserRepository, User, DuplicateUserError, make_user()

### Community 62 - "test_click_pipeline.py"
Cohesion: 0.37
Nodes (9): RedisClickPublisher, admin_settings(), DownRedis, make_link(), pipeline_settings(), test_flusher_persists_batch_and_increments_click_count(), test_flusher_recreates_the_group_after_the_stream_is_lost(), test_flusher_retries_pending_entries() (+1 more)

### Community 63 - "identity/domain/entities.py"
Cohesion: 0.26
Nodes (5): _as_utc(), RefreshTokenRecord, TokenFamily, test_refresh_record_handles_naive_datetimes(), test_token_family_and_refresh_record_lifecycle()

### Community 64 - "shorten-form.tsx"
Cohesion: 0.06
Nodes (26): columns, ExternalLink(), ExternalLinkProps, BackToTop(), MockIntersectionObserver, observers, renderBackToTop(), CopyState (+18 more)

### Community 65 - "OriginalUrl"
Cohesion: 0.25
Nodes (14): OriginalUrl, _link(), _resolved(), test_link_state_accounts_for_expiry_and_active_flag(), test_link_with_updates_returns_a_new_entity(), test_original_url_keeps_ipv6_literal_brackets(), test_original_url_normalizes_idn_to_punycode(), test_original_url_normalizes_scheme_host_and_idn() (+6 more)

### Community 66 - "build_app"
Cohesion: 0.33
Nodes (6): build_app(), test_app_error_uses_standard_envelope(), test_security_error_uses_standard_envelope(), test_unhandled_error_does_not_leak_stack_trace(), test_unknown_route_uses_standard_envelope(), test_validation_error_uses_standard_envelope()

### Community 67 - "test_links_api.py"
Cohesion: 0.34
Nodes (13): api_settings(), cleanup(), direct_link(), seed_click(), seed_links(), seed_user(), test_anonymous_create_and_redirect(), test_create_rate_limit_returns_429() (+5 more)

### Community 68 - "create_redis"
Cohesion: 0.18
Nodes (7): close_redis(), create_redis(), redis_client(), run(), read_stream(), run(), redis_client()

### Community 69 - "test_redirect_click_failure.py"
Cohesion: 0.29
Nodes (5): BlockingPublisher, click_settings(), DownRedis, test_redirect_continues_and_metric_counts_dropped_click(), test_redirect_does_not_wait_for_click_publisher()

### Community 70 - "request_context.py"
Cohesion: 0.22
Nodes (3): _incoming_request_id(), RequestIDMiddleware, send_with_request_id()

### Community 71 - "test_body_limit.py"
Cohesion: 0.33
Nodes (5): build_app(), test_accepts_body_at_limit(), test_invalid_content_length_is_rejected(), test_rejects_chunked_body_above_limit(), test_rejects_content_length_above_limit_before_reading()

### Community 72 - "RateLimiter"
Cohesion: 0.10
Nodes (5): GlobalRateLimitMiddleware, DownRedis, test_global_bucket_is_shared_across_clients(), DownRedis, test_rate_limit_dependency_sets_headers_and_429()

### Community 73 - "CacheClient"
Cohesion: 0.13
Nodes (5): CacheClient, FakeRedis, _sample(), test_cache_get_records_hit_and_miss(), test_cache_set_validates_ttl_and_delete()

### Community 74 - "security.py"
Cohesion: 0.24
Nodes (9): InvalidNextPath, allowed_origins(), csrf_protect(), origin_guard(), safe_next_path(), validate_origin(), CsrfError, test_safe_next_accepts_internal_paths() (+1 more)

### Community 75 - "test_link_cache.py"
Cohesion: 0.32
Nodes (11): _async_link(), cache_settings(), cleanup(), make_link(), test_cold_stampede_uses_one_database_query(), loader(), test_invalidation_during_a_stale_refresh_cannot_repopulate_the_cache(), test_invalidation_forces_the_next_read_to_use_the_loader() (+3 more)

### Community 76 - "token_bucket.js"
Cohesion: 0.21
Nodes (9): headers(), negative(), notFound, options, rateLimited, redirect(), stampede(), auth() (+1 more)

### Community 77 - "get_services"
Cohesion: 0.21
Nodes (16): get_cache(), get_current_user_optional(), get_services(), get_session(), settings_dependency(), create_link_rate_limit(), get_click_publisher(), get_create_link() (+8 more)

### Community 79 - "redirect.js"
Cohesion: 0.13
Nodes (15): CODE_TTL_SECONDS, cold(), COLD_CODES, createIp(), options, otherStatuses, rateLimited, redirectDuration (+7 more)

### Community 80 - "page.tsx"
Cohesion: 0.08
Nodes (32): dynamic, GET(), generateMetadata(), HomePage(), HomePageProps, sitemap(), Faq(), FaqEntry (+24 more)

### Community 81 - "test_stats_api.py"
Cohesion: 0.58
Nodes (9): api_settings(), cleanup(), seed_clicks(), seed_link(), seed_user(), test_breakdowns_keep_top_ten_and_use_other_and_direct_sentinels(), test_stats_50k_clicks_benchmark(), test_stats_rate_limit_returns_429() (+1 more)

### Community 82 - "value_objects.py"
Cohesion: 0.07
Nodes (19): DeleteLink, UpdateLinkCommand, LinkNotFound, GetLink, GetLinksOverview, LinksOverview, CacheUnavailable, Clock (+11 more)

### Community 83 - "Database"
Cohesion: 0.09
Nodes (18): Database, test_cleanup_deletes_old_clicks_and_expired_links_idempotently(), run(), run(), run(), run(), acleanup(), acleanup_email() (+10 more)

### Community 84 - "Bulkhead"
Cohesion: 0.09
Nodes (10): build_bulkheads(), Bulkhead, BulkheadRegistry, Argon2PasswordHasher, BulkheadFullError, test_bulkhead_limits_concurrency(), test_bulkhead_times_out_when_full(), test_bulkheads_are_named_and_independent() (+2 more)

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
Cohesion: 0.10
Nodes (18): nextConfig, withNextIntl, routing, buildRewrites(), isShortCodePath(), RESERVED_PATTERN, RESERVED_TOP_LEVEL, RewriteRule (+10 more)

### Community 91 - "create.js"
Cohesion: 0.21
Nodes (10): create(), created, createDuration, createLink(), createWithSharedIp(), options, otherStatuses, rateLimited (+2 more)

### Community 92 - "test_link_collision.py"
Cohesion: 0.17
Nodes (4): AllowedQuota, EmptyResolver, NoopCache, SequenceGenerator

### Community 93 - "main.py"
Cohesion: 0.10
Nodes (8): init_sentry(), _scrub_event(), test_metrics_accepts_valid_token(), test_metrics_rejects_wrong_token(), test_metrics_requires_token(), production_settings(), test_body_limit_is_enforced_by_the_full_app(), test_docs_and_openapi_are_disabled_in_production()

### Community 94 - "HostResolutionError"
Cohesion: 0.22
Nodes (3): SystemHostResolver, HostResolutionError, FakeResolver

### Community 95 - "test_sentry.py"
Cohesion: 0.38
Nodes (3): test_sentry_is_disabled_without_a_dsn(), fake_init(), test_sentry_scrubs_request_data_and_disables_pii()

### Community 96 - ".__call__"
Cohesion: 0.25
Nodes (4): send_with_headers(), capture_status(), send_with_headers(), send()

### Community 97 - "opengraph-image.tsx"
Cohesion: 0.40
Nodes (3): alt, contentType, size

### Community 98 - "Auditoria de segurança — P09"
Cohesion: 0.18
Nodes (10): Achados residuais aceitos (com justificativa), Auditoria de segurança — P09, Como reproduzir, Conclusão, Configuração de produção, O que não foi possível testar / limitações honestas, Resumo executivo, RLS — prova independente (+2 more)

### Community 99 - ".__call__"
Cohesion: 0.22
Nodes (3): MetricsMiddleware, _route_path(), record_request()

### Community 100 - "Auditoria item a item — SECURITY.md"
Cohesion: 0.20
Nodes (10): test_only_config_module_reads_process_environment(), §10 Supply chain, §2 Resiliência / anti-DDoS, §3 Anti SQL Injection, §4 Anti XSS / injeção no front, §5 Autenticação, sessão e força bruta, §7 Credenciais e exposição, §8 Buffer overflow / limites (+2 more)

### Community 101 - "storeTheme"
Cohesion: 0.36
Nodes (8): handleThemeChange(), ThemeToggle(), toggleTheme(), applyTheme(), readTheme(), storeTheme(), Theme, THEME_STORAGE_KEY

### Community 102 - "jittered_ttl"
Cohesion: 0.48
Nodes (3): jittered_ttl(), test_jittered_ttl_edge_cases(), test_jittered_ttl_stays_within_configured_range()

### Community 103 - "google_login.py"
Cohesion: 0.62
Nodes (3): InvalidGoogleLogin, LoginWithGoogle, GoogleIdentity

## Knowledge Gaps
- **18 isolated node(s):** `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching`, `lucide-react 1.60.0`, `minimumReleaseAgeExclude Policy` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 501 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `identity/presentation/router.py`, `cleanup.py`, `database.py`, `pytest`, `stats_cache.py`, `http.py`, `ShortCode`, `create_link`, `create_app`, `links/adapters/repository.py`, `identity/adapters/repository.py`, `ClickFlusher`, `build_services`, `dataclasses`, `helpers.py`, `adapters/google.py`, `google_callback`, `config.py`, `test_click_pipeline.py`, `test_links_api.py`, `create_redis`, `test_redirect_click_failure.py`, `security.py`, `test_link_cache.py`, `get_services`, `test_stats_api.py`, `Database`, `Bulkhead`, `Deploy — Vercel (web) + Render (API/Postgres/Redis)`, `main.py`, `test_sentry.py`, `Auditoria de segurança — P09`, `Auditoria item a item — SECURITY.md`?**
  _High betweenness centrality (0.237) - this node is a cross-community bridge._
- **Are the 105 inferred relationships involving `Settings` (e.g. with `settings_dependency()` and `configure_logging()`) actually correct?**
  _`Settings` has 105 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `AppError` be split into smaller, more focused modules?**
  _Cohesion score 0.07231638418079096 - nodes in this community are weakly interconnected._
- **Why does `§4 Anti XSS / injeção no front` connect `Auditoria item a item — SECURITY.md` to `proxy.ts`, `helpers.py`?**
  _High betweenness centrality (0.158) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `ShortCode` (e.g. with `GetLinkStats` and `RedisLinkCache`) actually correct?**
  _`ShortCode` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Should `db/models.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11692307692307692 - nodes in this community are weakly interconnected._