# Graph Report - Tricolink  (2026-10-21)

## Corpus Check
- Corpus is ~5,419 words - fits in a single context window. You may not need a graph.

## Summary
- 166 nodes · 233 edges · 18 communities (9 shown, 9 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 34 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Product Domain and Redirect
- Security and Rate Limits
- Web App and UI Components
- API Core and Health
- Agent Workflow and Graphify
- Compose and P01 Infra
- Alembic Migrations
- Shared Kernel Errors
- Project Phases and Graphify
- Logging Utility
- Clock Utility
- IDs Utility
- pnpm Release Policy
- PostCSS Tooling
- API Package

## God Nodes (most connected - your core abstractions)
1. `SECURITY.md Security Requirements` - 17 edges
2. `API Compose Service` - 11 edges
3. `Web Compose Service` - 10 edges
4. `UI_SPEC.md Tricolink Interface` - 10 edges
5. `get_settings()` - 7 edges
6. `CONTEXT.md Single Source of Truth` - 7 edges
7. `Settings` - 6 edges
8. `AppError` - 6 edges
9. `cn()` - 6 edges
10. `Mandatory Session Reading Order` - 6 edges

## Surprising Connections (you probably didn't know these)
- `P02 Security Foundation Phase` --conceptually_related_to--> `API Compose Service`  [INFERRED]
  docs/agent/PROGRESS.md → docker-compose.yml
- `pnpm allowBuilds Allowlist` --conceptually_related_to--> `Web Compose Service`  [INFERRED]
  apps/web/pnpm-workspace.yaml → docker-compose.yml
- `Python 3.11 and Poetry 2.4.1 Pin` --conceptually_related_to--> `API Compose Service`  [INFERRED]
  docs/agent/PROGRESS.md → docker-compose.yml
- `Frontend Stack Version Pins` --conceptually_related_to--> `Web Compose Service`  [INFERRED]
  docs/agent/PROGRESS.md → docker-compose.yml
- `Pending Human Review of AI Translations` --conceptually_related_to--> `Web Compose Service`  [INFERRED]
  docs/agent/PROGRESS.md → docker-compose.yml

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Anti Cache Stampede Layer Set** — docs_agent_context_anti_cache_stampede, docs_agent_context_stale_while_revalidate, docs_agent_context_single_flight, docs_agent_context_negative_cache, docs_agent_security_bulkhead [EXTRACTED 1.00]
- **Redirect Hot Path Flow** — docs_agent_context_redirect_cache, docs_agent_context_302_redirect, docs_agent_context_click_stream, docs_agent_context_click_events_table, docs_agent_context_links_table [EXTRACTED 1.00]
- **Tricolink Docker Compose Development Stack** — docker_compose_postgres_service, docker_compose_redis_service, docker_compose_api_service, docker_compose_web_service, docker_compose_app_network, docker_compose_data_network [EXTRACTED 1.00]
- **P00 Graphify Bootstrap Pipeline** — docs_agent_progress_graphify_kilo_integration, docs_agent_progress_semantic_extraction_cache, docs_agent_progress_graph_artifacts, docs_agent_progress_phase_roadmap [INFERRED 0.85]
- **P01 Containerized Tooling and Validation** — docs_agent_progress_make_container_targets, docs_agent_progress_non_root_containers, docs_agent_progress_local_port_override, docs_agent_progress_p01_validation, docker_compose_api_service, docker_compose_web_service [INFERRED 0.85]
- **Defense in Depth Controls** — docs_agent_security_token_bucket, docs_agent_security_circuit_breaker, docs_agent_security_bulkhead, docs_agent_security_rls, docs_agent_context_url_policy [INFERRED 0.85]

## Communities (18 total, 9 thin omitted)

### Community 0 - "Product Domain and Redirect"
Cohesion: 0.11
Nodes (26): 7-Char Base62 Code Generation, click_events Table, Redis Stream Click Buffer, Next.js Locale Routing and Rewrites, 11-Language i18n, links Table, Non-Goals, Tricolink URL Shortener Product (+18 more)

### Community 1 - "Security and Rate Limits"
Cohesion: 0.14
Nodes (20): Daily Link Quotas, Negative Cache for Unknown Codes, Single-Flight Lock, Stale-While-Revalidate Caching, Secrets via core/config.py, JWT and Rotating Refresh Sessions, Brute Force Protection, Bulkhead Semaphores (+12 more)

### Community 2 - "Web App and UI Components"
Cohesion: 0.12
Nodes (7): nextConfig, geist, metadata, RootLayout(), Button(), buttonVariants, cn()

### Community 3 - "API Core and Health"
Cohesion: 0.19
Nodes (6): get_settings(), Settings, settings_dependency(), create_app(), health_live(), HealthResponse

### Community 4 - "Agent Workflow and Graphify"
Cohesion: 0.14
Nodes (10): graphify Slash Command, Mandatory Session Reading Order, Modular Monolith with Clean Architecture, Monorepo Structure, CONTEXT.md Single Source of Truth, Graphify Context Engineering, Graphify Installation Commands, Per-Phase Graphify Routine (+2 more)

### Community 5 - "Compose and P01 Infra"
Cohesion: 0.23
Nodes (16): pnpm allowBuilds Allowlist, API Compose Service, app Network, data Network, postgres_data Volume, PostgreSQL 16 Compose Service, Redis 7 Compose Service, Web Compose Service (+8 more)

### Community 6 - "Alembic Migrations"
Cohesion: 0.24
Nodes (3): do_run_migrations(), run_async_migrations(), run_migrations_online()

### Community 7 - "Shared Kernel Errors"
Cohesion: 0.36
Nodes (3): AppError, AuthenticationError, AuthorizationError

### Community 8 - "Project Phases and Graphify"
Cohesion: 0.40
Nodes (4): Versioned Graphify P00 Artifacts, P02 Security Foundation Phase, P00-P11 Phase Roadmap, Graphify Semantic Extraction Cache

## Knowledge Gaps
- **18 isolated node(s):** `tricolink-api`, `graphify Slash Command`, `pnpm allowBuilds Allowlist`, `minimumReleaseAgeExclude Policy`, `lucide-react 1.60.0` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 51 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SECURITY.md Security Requirements` connect `Security and Rate Limits` to `Product Domain and Redirect`, `Agent Workflow and Graphify`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `API Compose Service` (e.g. with `Local Port Override 8001/3001` and `In-Container Make Targets`) actually correct?**
  _`API Compose Service` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `tricolink-api`, `graphify Slash Command`, `pnpm allowBuilds Allowlist` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Product Domain and Redirect` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._
- **Why does `Mandatory Session Reading Order` connect `Agent Workflow and Graphify` to `Product Domain and Redirect`, `Security and Rate Limits`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Web Compose Service` (e.g. with `pnpm allowBuilds Allowlist` and `Frontend Stack Version Pins`) actually correct?**
  _`Web Compose Service` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Should `Security and Rate Limits` be split into smaller, more focused modules?**
  _Cohesion score 0.13852813852813853 - nodes in this community are weakly interconnected._