# Graph Report - Tricolink  (2026-10-21)

## Corpus Check
- Corpus is ~3,905 words - fits in a single context window. You may not need a graph.

## Summary
- 73 nodes · 121 edges · 7 communities
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 16 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Agent Workflow and Graphify
- Rate Limiting and Resilience
- Frontend i18n and Pages
- Security Hardening
- Redirect and Hot Path
- Architecture and Spec Governance
- Data Model and API

## God Nodes (most connected - your core abstractions)
1. `SECURITY.md Security Requirements` - 17 edges
2. `UI_SPEC.md Tricolink Interface` - 10 edges
3. `Mandatory Session Reading Order` - 7 edges
4. `CONTEXT.md Single Source of Truth` - 7 edges
5. `Graphify Context Engineering` - 7 edges
6. `Tricolink URL Shortener Product` - 6 edges
7. `REST API /api/v1 Contract` - 6 edges
8. `Code Standards` - 6 edges
9. `Token Bucket Rate Limiting` - 6 edges
10. `links Table` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Mandatory Session Reading Order` --references--> `CONTEXT.md Single Source of Truth`  [EXTRACTED]
  AGENTS.md → docs/agent/CONTEXT.md
- `Mandatory Session Reading Order` --references--> `SECURITY.md Security Requirements`  [EXTRACTED]
  AGENTS.md → docs/agent/SECURITY.md
- `Mandatory Session Reading Order` --references--> `UI_SPEC.md Tricolink Interface`  [EXTRACTED]
  AGENTS.md → docs/agent/UI_SPEC.md
- `CONTEXT.md Supremacy Rule` --rationale_for--> `CONTEXT.md Single Source of Truth`  [EXTRACTED]
  AGENTS.md → docs/agent/CONTEXT.md
- `graphify Slash Command` --references--> `Graphify Context Engineering`  [EXTRACTED]
  AGENTS.md → docs/agent/GRAPHIFY.md

## Hyperedges (group relationships)
- **Anti Cache Stampede Layer Set** — docs_agent_context_anti_cache_stampede, docs_agent_context_stale_while_revalidate, docs_agent_context_single_flight, docs_agent_context_negative_cache, docs_agent_security_bulkhead [EXTRACTED 1.00]
- **Redirect Hot Path Flow** — docs_agent_context_redirect_cache, docs_agent_context_302_redirect, docs_agent_context_click_stream, docs_agent_context_click_events_table, docs_agent_context_links_table [EXTRACTED 1.00]
- **Defense in Depth Controls** — docs_agent_security_token_bucket, docs_agent_security_circuit_breaker, docs_agent_security_bulkhead, docs_agent_security_rls, docs_agent_context_url_policy [INFERRED 0.85]

## Communities (7 total, 0 thin omitted)

### Community 0 - "Agent Workflow and Graphify"
Cohesion: 0.26
Nodes (10): graphify Slash Command, Mandatory Session Reading Order, Graphify Context Engineering, Graphify Installation Commands, Per-Phase Graphify Routine, graphify query/path/explain Workflow, Decisions Log, P00 Bootstrap SDD + Graphify (+2 more)

### Community 1 - "Rate Limiting and Resilience"
Cohesion: 0.21
Nodes (10): Daily Link Quotas, Negative Cache for Unknown Codes, Single-Flight Lock, Stale-While-Revalidate Caching, Not Validated Log, Brute Force Protection, Bulkhead Semaphores, Circuit Breaker (+2 more)

### Community 2 - "Frontend i18n and Pages"
Cohesion: 0.26
Nodes (12): Next.js Locale Routing and Rewrites, 11-Language i18n, UI/UX Summary, Pending Human Review, CSRF Double-Submit Protection, Account Page, UI_SPEC.md Tricolink Interface, Landing Page (+4 more)

### Community 3 - "Security Hardening"
Cohesion: 0.23
Nodes (11): Secrets via core/config.py, JWT and Rotating Refresh Sessions, Credential Hygiene, Google OIDC, Logical Buffer Overflow Limits, SECURITY.md Security Requirements, Row Level Security, Anti SQL Injection (+3 more)

### Community 4 - "Redirect and Hot Path"
Cohesion: 0.25
Nodes (8): click_events Table, Redis Stream Click Buffer, Non-Goals, Tricolink URL Shortener Product, Redirect and Cache Hot Path, URL Anti-Abuse Policy, SSRF Prevention, Design Tokens

### Community 5 - "Architecture and Spec Governance"
Cohesion: 0.29
Nodes (4): Modular Monolith with Clean Architecture, Monorepo Structure, CONTEXT.md Single Source of Truth, PROGRESS Bloqueios Section

### Community 6 - "Data Model and API"
Cohesion: 0.33
Nodes (7): 7-Char Base62 Code Generation, links Table, refresh_tokens Table, Reserved Alias List, REST API /api/v1 Contract, users Table, SEO Indexation Control

## Knowledge Gaps
- **8 isolated node(s):** `graphify Slash Command`, `Stale-While-Revalidate Caching`, `Reserved Alias List`, `7-Char Base62 Code Generation`, `Non-Goals` (+3 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 10 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SECURITY.md Security Requirements` connect `Security Hardening` to `Agent Workflow and Graphify`, `Rate Limiting and Resilience`, `Frontend i18n and Pages`, `Redirect and Hot Path`, `Data Model and API`?**
  _High betweenness centrality (0.393) - this node is a cross-community bridge._
- **What connects `graphify Slash Command`, `Stale-While-Revalidate Caching`, `Reserved Alias List` to the rest of the system?**
  _8 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Why does `Mandatory Session Reading Order` connect `Agent Workflow and Graphify` to `Frontend i18n and Pages`, `Security Hardening`, `Architecture and Spec Governance`?**
  _High betweenness centrality (0.342) - this node is a cross-community bridge._
- **Why does `UI_SPEC.md Tricolink Interface` connect `Frontend i18n and Pages` to `Agent Workflow and Graphify`, `Security Hardening`, `Redirect and Hot Path`?**
  _High betweenness centrality (0.185) - this node is a cross-community bridge._