# ADR 001: Modular Monolith with Clean Architecture

## Status
Accepted

## Context
Tricolink is a portfolio project demonstrating backend engineering skills. The codebase needs to be maintainable, testable, and showcase architectural discipline without the operational complexity of microservices.

## Decision
Use a **modular monolith** where each business capability (identity, links, analytics) is a separate module with its own Clean Architecture layers:
- **domain**: Pure business logic, no framework dependencies
- **application**: Use cases, ports (interfaces)
- **adapters**: Framework-specific implementations (SQLAlchemy, Redis, Authlib)
- **presentation**: FastAPI routers, Pydantic schemas

Dependencies point inward: domain → application → adapters → presentation. Shared kernel holds cross-cutting primitives (errors, clock, IDs).

## Consequences
- ✅ Single deployable unit, simple local dev (Docker Compose)
- ✅ Clear module boundaries, easy to extract later if needed
- ✅ Domain logic testable without FastAPI/DB/Redis
- ✅ Demonstrates Clean Architecture discipline
- ⚠️ All modules share process; one module's memory leak affects all
- ⚠️ Scaling requires replicating entire app (mitigated by stateless design)

## References
- CONTEXT.md §3 (monorepo structure)
- Graphify community "Tricolink URL Shortener Product"