# Graph Report - Tricolink  (2026-10-22)

## Corpus Check
- 271 files · ~125,714 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: (none) 10, .toml 1, .ini 1)

## Summary
- 2192 nodes · 6798 edges · 98 communities (85 shown, 13 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 937 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `44980e6e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tricolink URL Shortener Product
- Token Bucket Rate Limiting
- AppError
- links/presentation/router.py
- Agent Workflow and Graphify
- Compose and P01 Infra
- test_schema_metadata.py
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
- Link
- repository.py
- test_click_pipeline.py
- login-form.tsx
- build_services
- identity/presentation/router.py
- .__init__
- Settings
- services.py
- dataclasses
- shorten-form.tsx
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
- BucketPolicy
- SqlAlchemyUserRepository
- test_rate_limit_dependency_sets_headers_and_429
- identity/domain/entities.py
- test_url_policy.py
- pytest
- build_app
- create_redis
- ClickFlusher
- test_redirect_click_failure.py
- request_context.py
- test_body_limit.py
- RateLimiter
- HostResolutionError
- security.py
- .__call__
- analytics/presentation/router.py
- logging.py
- token_bucket.js
- page.tsx
- Auditoria de segurança — P09
- value_objects.py
- Database
- Bulkhead
- sqlalchemy
- Auditoria item a item — SECURITY.md
- i18n-check.mjs
- google_login.py
- proxy.ts
- uuid
- structured-data.ts
- jittered_ttl
- starlette_types
- test_analytics_domain.py
- .publish

## God Nodes (most connected - your core abstractions)
1. `Settings` - 140 edges
2. `ShortCode` - 95 edges
3. `Link` - 82 edges
4. `create_app()` - 60 edges
5. `build_services()` - 54 edges
6. `User` - 45 edges
7. `Database` - 43 edges
8. `AppError` - 43 edges
9. `cn()` - 38 edges
10. `OriginalUrl` - 37 edges

## Surprising Connections (you probably didn't know these)
- `§2 Resiliência / anti-DDoS` --references--> `Settings`  [INFERRED]
  docs/security/AUDIT.md → apps/api/src/tricolink/core/config.py
- `Configuração de produção` --references--> `Settings`  [INFERRED]
  docs/security/AUDIT.md → apps/api/src/tricolink/core/config.py
- `§5 Autenticação, sessão e força bruta` --references--> `auth()`  [INFERRED]
  docs/security/AUDIT.md → apps/api/tests/unit/test_errors.py
- `§4 Anti XSS / injeção no front` --references--> `securityHeaders()`  [INFERRED]
  docs/security/AUDIT.md → apps/web/src/lib/security.ts
- `Achados corrigidos` --references--> `test_flusher_recreates_the_group_after_the_stream_is_lost()`  [EXTRACTED]
  docs/security/AUDIT.md → apps/api/tests/integration/test_click_pipeline.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Anti Cache Stampede Layer Set** — docs_agent_context_anti_cache_stampede, docs_agent_context_stale_while_revalidate, docs_agent_context_single_flight, docs_agent_context_negative_cache, docs_agent_security_bulkhead [EXTRACTED 1.00]
- **Redirect Hot Path Flow** — docs_agent_context_redirect_cache, docs_agent_context_302_redirect, docs_agent_context_click_stream, docs_agent_context_click_events_table, docs_agent_context_links_table [EXTRACTED 1.00]
- **Tricolink Docker Compose Development Stack** — docker_compose_postgres_service, docker_compose_redis_service, docker_compose_api_service, docker_compose_web_service, docker_compose_app_network, docker_compose_data_network [EXTRACTED 1.00]
- **P00 Graphify Bootstrap Pipeline** — docs_agent_progress_graphify_kilo_integration, docs_agent_progress_semantic_extraction_cache, docs_agent_progress_graph_artifacts, docs_agent_progress_phase_roadmap [INFERRED 0.85]
- **P01 Containerized Tooling and Validation** — docs_agent_progress_make_container_targets, docs_agent_progress_non_root_containers, docs_agent_progress_local_port_override, docs_agent_progress_p01_validation, docker_compose_api_service, docker_compose_web_service [INFERRED 0.85]
- **Defense in Depth Controls** — docs_agent_security_token_bucket, docs_agent_security_circuit_breaker, docs_agent_security_bulkhead, docs_agent_security_rls, docs_agent_context_url_policy [INFERRED 0.85]

## Communities (98 total, 13 thin omitted)

### Community 0 - "Tricolink URL Shortener Product"
Cohesion: 0.25
Nodes (8): click_events Table, Redis Stream Click Buffer, Non-Goals, Tricolink URL Shortener Product, Redirect and Cache Hot Path, URL Anti-Abuse Policy, SSRF Prevention, Design Tokens

### Community 1 - "Token Bucket Rate Limiting"
Cohesion: 0.24
Nodes (9): Daily Link Quotas, Negative Cache for Unknown Codes, Single-Flight Lock, Stale-While-Revalidate Caching, Brute Force Protection, Bulkhead Semaphores, Circuit Breaker, Rate Limit Buckets (+1 more)

### Community 2 - "AppError"
Cohesion: 0.20
Nodes (15): CreateLink, AliasReserved, AliasTaken, CodeGenerationFailed, DailyQuotaExceeded, InvalidAlias, InvalidCursor, InvalidExpiresAt (+7 more)

### Community 3 - "links/presentation/router.py"
Cohesion: 0.22
Nodes (17): get_cache(), get_current_user_optional(), get_rate_limiter(), get_services(), get_session(), settings_dependency(), create_link_rate_limit(), get_click_publisher() (+9 more)

### Community 4 - "Agent Workflow and Graphify"
Cohesion: 0.18
Nodes (8): graphify Slash Command, Mandatory Session Reading Order, CONTEXT.md Single Source of Truth, Graphify Context Engineering, Graphify Installation Commands, Per-Phase Graphify Routine, graphify query/path/explain Workflow, Tricolink README Stub (P11)

### Community 5 - "Compose and P01 Infra"
Cohesion: 0.16
Nodes (20): pnpm allowBuilds Allowlist, API Compose Service, app Network, data Network, postgres_data Volume, PostgreSQL 16 Compose Service, Redis 7 Compose Service, Web Compose Service (+12 more)

### Community 7 - "test_real_ip.py"
Cohesion: 0.14
Nodes (8): _forwarded_for(), RealIPMiddleware, resolve_real_ip(), _NeverRedis, test_middleware_sets_request_client_to_real_ip(), test_resolve_real_ip_counts_from_the_right(), test_resolve_real_ip_falls_back_when_header_is_invalid_or_short(), test_resolve_real_ip_without_trusted_proxies_ignores_header()

### Community 8 - "MemoryTokenBucket"
Cohesion: 0.22
Nodes (9): _BucketState, MemoryTokenBucket, DownRedis, FakeClock, test_memory_bucket_consumes_and_exhausts(), test_memory_bucket_never_exceeds_capacity(), test_memory_bucket_refills(), test_rate_limiter_falls_back_to_memory_when_redis_is_down() (+1 more)

### Community 9 - "logging.py"
Cohesion: 0.24
Nodes (3): MetricsMiddleware, _route_path(), record_request()

### Community 10 - "BodyLimitMiddleware"
Cohesion: 0.26
Nodes (3): BodyLimitMiddleware, _header_values(), _send_json()

### Community 11 - "httpx"
Cohesion: 0.25
Nodes (8): SecurityHeadersMiddleware, build_inner(), test_hsts_only_in_production(), test_request_id_accepts_only_safe_values(), test_request_id_is_generated_and_returned(), test_security_headers_are_added(), test_timeout_allows_fast_requests(), test_timeout_returns_504()

### Community 15 - "User"
Cohesion: 0.13
Nodes (9): AuthenticateAccess, UpdateMeCommand, InvalidProfile, SessionExpired, GetMe, UserRepository, _normalize_display_name(), _normalize_locale() (+1 more)

### Community 19 - "pytest"
Cohesion: 0.05
Nodes (13): CacheClient, CircuitBreaker, CircuitState, CircuitOpenError, FakeRedis, _sample(), test_cache_get_records_hit_and_miss(), test_cache_set_validates_ttl_and_delete() (+5 more)

### Community 20 - "stats_cache.py"
Cohesion: 0.07
Nodes (26): _breakdown(), _deserialize(), RedisStatsCache, _serialize(), SqlAlchemyStatsRepository, load(), RawStats, BreakdownItem (+18 more)

### Community 21 - "demo-dashboard.tsx"
Cohesion: 0.07
Nodes (38): BreakdownColumns, BreakdownRow, BreakdownTable(), BreakdownTableProps, columns, ClicksChart(), ClicksChartProps, ClicksPoint (+30 more)

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
Nodes (19): _CacheRead, _entry_from_link(), RedisLinkCache, CacheEntry, CacheUnavailable, ShortCode, _async_link(), cache_settings() (+11 more)

### Community 28 - "ClickEvent"
Cohesion: 0.21
Nodes (9): _parse_event(), _browser(), ClickEvent, extract_referrer_host(), normalize_country(), parse_user_agent(), UserAgentInfo, ClickPublisher (+1 more)

### Community 29 - "create_link"
Cohesion: 0.12
Nodes (14): create_link(), delete_link(), get_link(), _link_response(), links_overview(), list_links(), redirect_link(), _static_html() (+6 more)

### Community 30 - "pytest"
Cohesion: 0.08
Nodes (30): CreateLinkCommand, QuotaResult, CodeGenerator, AllowedQuota, test_code_generator_can_be_made_deterministic(), test_code_generator_uses_seven_base62_characters(), test_code_generator_validates_configuration(), build_create() (+22 more)

### Community 31 - "ref_next_intl"
Cohesion: 0.09
Nodes (30): AccountPage(), AccountPageProps, generateMetadata(), dynamic, generateMetadata(), inter, jakarta, LocaleLayout() (+22 more)

### Community 32 - "pytest"
Cohesion: 0.12
Nodes (24): LoginCommand, RegisterCommand, build_issuer(), build_login(), build_register(), FakeAccessTokens, FakeClock, FakeHasher (+16 more)

### Community 33 - "Link"
Cohesion: 0.08
Nodes (17): GetLinkStats, StatsCache, StatsRepository, get_get_link_stats(), DeleteLink, UpdateLinkCommand, LinkNotFound, GetLink (+9 more)

### Community 34 - "repository.py"
Cohesion: 0.08
Nodes (24): upgrade(), Base, Link, set_rls_context(), _escape_like(), _is_code_conflict(), SqlAlchemyLinkRepository, _to_domain() (+16 more)

### Community 35 - "test_click_pipeline.py"
Cohesion: 0.37
Nodes (10): ClickEvent, RedisClickPublisher, admin_settings(), DownRedis, make_link(), pipeline_settings(), test_flusher_persists_batch_and_increments_click_count(), test_flusher_recreates_the_group_after_the_stream_is_lost() (+2 more)

### Community 36 - "login-form.tsx"
Cohesion: 0.12
Nodes (29): first(), generateMetadata(), LoginPage(), LoginPageProps, AccountForm(), handleError(), handleLocaleChange(), handleProfileSubmit() (+21 more)

### Community 37 - "build_services"
Cohesion: 0.16
Nodes (12): build_services(), AuthSession, Logout, AccessTokenIssuer, Clock, RotationStatus, SessionRepository, RefreshSession (+4 more)

### Community 38 - "identity/presentation/router.py"
Cohesion: 0.15
Nodes (26): GoogleNotConfigured, get_authenticate_access(), get_get_me(), get_google_login(), get_google_oidc(), get_login(), get_logout(), get_refresh_session() (+18 more)

### Community 39 - ".__init__"
Cohesion: 0.06
Nodes (6): BadRequestError, ConflictError, GatewayTimeoutError, PayloadTooLargeError, ServiceUnavailableError, AuthorizationError

### Community 40 - "Settings"
Cohesion: 0.14
Nodes (13): Settings, generate_csrf_token(), clear_session_cookies(), set_csrf_cookie(), set_session_cookies(), build_session(), fast_hasher(), test_argon2_hasher_roundtrip_and_dummy() (+5 more)

### Community 41 - "services.py"
Cohesion: 0.11
Nodes (8): AnalyticsServices, IdentityServices, LinkServices, _own_hosts(), RedisDailyQuota, _seconds_until_next_utc_day(), SystemClock, utc_now()

### Community 42 - "dataclasses"
Cohesion: 0.13
Nodes (18): _rate_limit_error(), user_rate_limit(), dependency(), record_rate_limit_fallback(), record_rate_limited(), apply_rate_limit_headers(), client_ip(), _get_limiter() (+10 more)

### Community 43 - "shorten-form.tsx"
Cohesion: 0.10
Nodes (18): items, HeroSection(), CopyState, CreateLinkResponse, ERROR_KEYS, FormError, ShortenForm(), handleSubmit() (+10 more)

### Community 44 - "resolve_link.py"
Cohesion: 0.26
Nodes (9): ResolvedLink, _as_utc(), _entry_state(), _resolved_from_cache(), _resolved_from_link(), ResolveLink, _as_utc(), LinkState (+1 more)

### Community 45 - "Settings"
Cohesion: 0.12
Nodes (19): _boolean(), _env(), get_migration_database_url(), get_settings(), _integer(), _number(), SettingsError, _text() (+11 more)

### Community 46 - "create_app"
Cohesion: 0.05
Nodes (96): CurrentUser, get_current_user(), RefreshToken, User, create_app(), admin_settings(), cleanup(), run() (+88 more)

### Community 47 - "list_links.py"
Cohesion: 0.21
Nodes (8): LinkPage, _Unset, InvalidPagination, ListLinks, _normalize_query(), decode_cursor(), encode_cursor(), test_cursor_roundtrip_and_rejection()

### Community 48 - "Register"
Cohesion: 0.19
Nodes (8): AuthLocked, InvalidCredentials, InvalidEmail, WeakPassword, Login, AuthThrottle, PasswordHasher, Register

### Community 49 - "links-view.tsx"
Cohesion: 0.08
Nodes (43): LinkDetailPage(), LinkDetailPageProps, LinksLoading(), ExternalLink(), ExternalLinkProps, CopyLinkButton(), CopyLinkButtonProps, DeleteLinkDialog() (+35 more)

### Community 50 - "ref_next_intl"
Cohesion: 0.09
Nodes (31): LinkDetailError(), LocaleNotFound(), handleThemeChange(), AccountFormProps, Notice, BrandLogo(), Footer(), FinalCta() (+23 more)

### Community 51 - "api.ts"
Cohesion: 0.09
Nodes (30): navigation, user, api, ApiError, apiErrorFromResponse(), ApiErrorPayload, ApiRequestOptions, AuthResponseDto (+22 more)

### Community 52 - "adapters/google.py"
Cohesion: 0.27
Nodes (5): PyJwtAccessTokens, AccessClaims, IssuedAccessToken, test_access_jwt_contains_minimal_claims_and_validates(), test_expired_access_token_is_rejected()

### Community 53 - "google_callback"
Cohesion: 0.18
Nodes (9): GoogleOIDCClient, InvalidNextPath, google_callback(), _google_error_redirect(), google_login(), frontend_url(), safe_next_path(), test_safe_next_accepts_internal_paths() (+1 more)

### Community 54 - "test_identity_domain.py"
Cohesion: 0.21
Nodes (14): PasswordPolicy, google_claims(), test_email_is_nfkc_normalized_and_lowercased(), test_email_rejects_invalid_values(), test_email_rejects_non_string_and_too_long(), test_google_claims_accept_audience_list_and_string_verified(), test_google_claims_reject_untrusted_values(), test_google_claims_require_nonce() (+6 more)

### Community 55 - "Email"
Cohesion: 0.21
Nodes (8): Email, InvalidEmailError, InvalidGoogleIdentityError, WeakPasswordError, _display_name(), _number(), _string(), validate_google_claims()

### Community 56 - "config.py"
Cohesion: 0.12
Nodes (8): ping_redis(), unit_of_work(), record_cache_hit(), record_cache_miss(), record_circuit_state(), record_click_dropped(), record_clicks_flushed(), _retry_after()

### Community 57 - "error_handlers.py"
Cohesion: 0.19
Nodes (7): install_error_handlers(), handle_app_error(), handle_http_exception(), handle_unexpected_error(), handle_validation_error(), _json_error(), error_payload()

### Community 59 - "RedisAuthThrottle"
Cohesion: 0.16
Nodes (5): _digest(), RedisAuthThrottle, guarded(), operation(), ThrottleResult

### Community 60 - "BucketPolicy"
Cohesion: 0.15
Nodes (8): BucketPolicy, build_policies(), RedisTokenBucket, _reset_seconds(), TokenBucketBackend, test_lua_bucket_consumes_exhausts_and_refills(), test_lua_bucket_is_atomic_under_concurrency(), test_lua_bucket_keeps_keys_independent()

### Community 61 - "SqlAlchemyUserRepository"
Cohesion: 0.15
Nodes (8): _revoke_family(), SqlAlchemySessionRepository, SqlAlchemyUserRepository, _to_user(), RotationResult, User, DuplicateUserError, make_user()

### Community 62 - "test_rate_limit_dependency_sets_headers_and_429"
Cohesion: 0.18
Nodes (4): DownRedis, test_global_bucket_is_shared_across_clients(), DownRedis, test_rate_limit_dependency_sets_headers_and_429()

### Community 63 - "identity/domain/entities.py"
Cohesion: 0.27
Nodes (4): _as_utc(), RefreshTokenRecord, test_refresh_record_handles_naive_datetimes(), test_token_family_and_refresh_record_lifecycle()

### Community 64 - "test_url_policy.py"
Cohesion: 0.24
Nodes (13): is_blocked_ip(), build_policy(), test_is_blocked_ip_allows_only_global_addresses(), test_is_blocked_ip_blocks_non_global_addresses(), test_url_policy_accepts_public_urls(), test_url_policy_blocks_host_when_resolution_fails_or_is_empty(), test_url_policy_blocks_invalid_dns_answer(), test_url_policy_blocks_own_domain_and_subdomains_without_dns() (+5 more)

### Community 65 - "pytest"
Cohesion: 0.37
Nodes (12): operation(), policy(), test_credentials_controls_and_backslashes_are_blocked(), test_dns_rebinding_mixed_answers_are_all_checked(), test_forbidden_schemes_and_scheme_relative_urls_are_blocked(), test_global_ipv4_and_ipv6_answers_are_accepted(), test_obfuscated_or_internal_hostnames_are_blocked(), test_own_domain_and_subdomains_are_blocked_as_redirect_loops() (+4 more)

### Community 66 - "build_app"
Cohesion: 0.24
Nodes (8): NotFoundError, build_app(), missing(), test_app_error_uses_standard_envelope(), test_security_error_uses_standard_envelope(), test_unhandled_error_does_not_leak_stack_trace(), test_unknown_route_uses_standard_envelope(), test_validation_error_uses_standard_envelope()

### Community 67 - "create_redis"
Cohesion: 0.18
Nodes (7): close_redis(), create_redis(), redis_client(), run(), read_stream(), run(), redis_client()

### Community 69 - "test_redirect_click_failure.py"
Cohesion: 0.29
Nodes (5): BlockingPublisher, click_settings(), DownRedis, test_redirect_continues_and_metric_counts_dropped_click(), test_redirect_does_not_wait_for_click_publisher()

### Community 70 - "request_context.py"
Cohesion: 0.12
Nodes (6): capture_status(), _incoming_request_id(), RequestIDMiddleware, send_with_request_id(), send_with_headers(), send()

### Community 71 - "test_body_limit.py"
Cohesion: 0.33
Nodes (5): build_app(), test_accepts_body_at_limit(), test_invalid_content_length_is_rejected(), test_rejects_chunked_body_above_limit(), test_rejects_content_length_above_limit_before_reading()

### Community 72 - "RateLimiter"
Cohesion: 0.22
Nodes (3): GlobalRateLimitMiddleware, send_with_headers(), _headers()

### Community 73 - "HostResolutionError"
Cohesion: 0.19
Nodes (4): SystemHostResolver, HostResolutionError, FakeResolver, FakeResolver

### Community 74 - "security.py"
Cohesion: 0.44
Nodes (5): allowed_origins(), csrf_protect(), origin_guard(), validate_origin(), CsrfError

### Community 75 - ".__call__"
Cohesion: 0.29
Nodes (4): replay_body(), run(), tracked_send(), receive()

### Community 76 - "analytics/presentation/router.py"
Cohesion: 0.26
Nodes (4): link_stats(), LinkStatsResponse, StatsBreakdownResponse, StatsSeriesPointResponse

### Community 77 - "logging.py"
Cohesion: 0.31
Nodes (3): configure_logging(), get_logger(), lifespan()

### Community 79 - "token_bucket.js"
Cohesion: 0.21
Nodes (9): headers(), negative(), notFound, options, rateLimited, redirect(), stampede(), auth() (+1 more)

### Community 80 - "page.tsx"
Cohesion: 0.10
Nodes (26): dynamic, GET(), generateMetadata(), HomePage(), HomePageProps, sitemap(), Faq(), FaqEntry (+18 more)

### Community 81 - "Auditoria de segurança — P09"
Cohesion: 0.17
Nodes (11): Achados corrigidos, Achados residuais aceitos (com justificativa), Auditoria de segurança — P09, Como reproduzir, Conclusão, Configuração de produção, O que não foi possível testar / limitações honestas, Resumo executivo (+3 more)

### Community 82 - "value_objects.py"
Cohesion: 0.11
Nodes (21): _normalize_expiry(), InvalidShortCodeError, InvalidUrlError, ReservedAliasError, HostResolver, _normalize_own_host(), UrlPolicy, _normalize_host() (+13 more)

### Community 83 - "Database"
Cohesion: 0.11
Nodes (7): Database, test_database_ping_and_unit_of_work(), test_unit_of_work_rolls_back_on_error(), run(), run(), run(), run()

### Community 84 - "Bulkhead"
Cohesion: 0.10
Nodes (8): build_bulkheads(), Bulkhead, BulkheadRegistry, Argon2PasswordHasher, BulkheadFullError, test_bulkhead_limits_concurrency(), test_bulkhead_times_out_when_full(), test_bulkheads_are_named_and_independent()

### Community 85 - "sqlalchemy"
Cohesion: 0.32
Nodes (3): do_run_migrations(), run_async_migrations(), run_migrations_online()

### Community 86 - "Auditoria item a item — SECURITY.md"
Cohesion: 0.18
Nodes (10): test_runtime_role_has_rls_enforced(), test_only_config_module_reads_process_environment(), §10 Supply chain, §2 Resiliência / anti-DDoS, §3 Anti SQL Injection, §4 Anti XSS / injeção no front, §7 Credenciais e exposição, §8 Buffer overflow / limites (+2 more)

### Community 87 - "i18n-check.mjs"
Cohesion: 0.09
Nodes (16): appRoot, catalogs, errors, files, flattenKeys(), localeSet, messagesDir, reference (+8 more)

### Community 88 - "google_login.py"
Cohesion: 0.80
Nodes (3): InvalidGoogleLogin, LoginWithGoogle, GoogleIdentity

### Community 89 - "proxy.ts"
Cohesion: 0.13
Nodes (18): nextConfig, withNextIntl, buildRewrites(), isShortCodePath(), RESERVED_PATTERN, RESERVED_TOP_LEVEL, RewriteRule, RewritesConfig (+10 more)

### Community 92 - "uuid"
Cohesion: 0.11
Nodes (9): EmptyResolver, NoopCache, SequenceGenerator, NoopRecordClick, test_200_concurrent_cold_redirects_hit_the_database_once(), _link(), _resolved(), test_invalidation_generation_blocks_a_stale_cache_refresh() (+1 more)

### Community 93 - "structured-data.ts"
Cohesion: 0.24
Nodes (8): buildLandingStructuredData(), FaqItem, FaqPageNode, LandingStructuredData, LandingStructuredDataInput, faq, landingData(), WebApplicationNode

### Community 94 - "jittered_ttl"
Cohesion: 0.48
Nodes (3): jittered_ttl(), test_jittered_ttl_edge_cases(), test_jittered_ttl_stays_within_configured_range()

### Community 96 - "test_analytics_domain.py"
Cohesion: 0.47
Nodes (4): test_click_event_never_contains_raw_user_agent_or_ip(), test_extract_referrer_host(), test_normalize_country(), test_parse_user_agent()

### Community 97 - ".publish"
Cohesion: 0.50
Nodes (3): guarded(), operation(), guarded()

## Knowledge Gaps
- **18 isolated node(s):** `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching`, `lucide-react 1.60.0`, `minimumReleaseAgeExclude Policy` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 453 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `links/presentation/router.py`, `.__init__`, `pytest`, `stats_cache.py`, `http.py`, `ShortCode`, `create_link`, `repository.py`, `test_click_pipeline.py`, `build_services`, `identity/presentation/router.py`, `services.py`, `dataclasses`, `Settings`, `create_app`, `adapters/google.py`, `google_callback`, `config.py`, `RedisAuthThrottle`, `BucketPolicy`, `create_redis`, `ClickFlusher`, `test_redirect_click_failure.py`, `security.py`, `logging.py`, `Auditoria de segurança — P09`, `Database`, `Bulkhead`, `Auditoria item a item — SECURITY.md`, `adapters/google.py`, `uuid`?**
  _High betweenness centrality (0.236) - this node is a cross-community bridge._
- **Are the 98 inferred relationships involving `Settings` (e.g. with `settings_dependency()` and `configure_logging()`) actually correct?**
  _`Settings` has 98 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tricolink-api`, `Non-Goals`, `Stale-While-Revalidate Caching` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_real_ip.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1368421052631579 - nodes in this community are weakly interconnected._
- **Why does `§4 Anti XSS / injeção no front` connect `Auditoria item a item — SECURITY.md` to `proxy.ts`, `create_app`?**
  _High betweenness centrality (0.157) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `ShortCode` (e.g. with `GetLinkStats` and `RedisLinkCache`) actually correct?**
  _`ShortCode` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Should `User` be split into smaller, more focused modules?**
  _Cohesion score 0.13105413105413105 - nodes in this community are weakly interconnected._