# ADR 007: Row Level Security as Defense in Depth

## Status
Accepted

## Context
Application-level authorization checks can have bugs. Database-level enforcement provides a safety net against IDOR and SQL injection data leaks.

## Decision
Enable **Row Level Security (RLS) with `FORCE`** on `links` and `refresh_tokens` tables:

- Policies use session variable `app.current_user_id` (UUID)
- Set via `SET LOCAL` per transaction in `Database.unit_of_work()` / `Database.read()`
- Runtime role `tricolink_app`: `NOSUPERUSER NOBYPASSRLS`
- Migration role separate (admin, can create `citext`, run DDL)
- Anonymous links: visible only with exact `app.current_link_code` context

## Rationale
- **Defense in depth**: App checks ownership AND DB enforces it
- Even with SQL injection or logic bug, cross-user reads/writes return 0 rows
- `FORCE` applies to table owner too (unlike `ENABLE` alone)
- Minimal overhead: single `SET LOCAL` per transaction

## Consequences
- ✅ Independent RLS test proves: no context = 0 rows; context A ≠ context B; cross-user UPDATE/DELETE = 0 rows
- ✅ Runtime role non-superuser validated in tests
- ✅ Migration role separation documented for Render deploy
- ⚠️ `click_events` not protected by RLS (accepted risk R-04)
- ⚠️ Requires discipline: every DB call must set context correctly
- ⚠️ Admin operations (cleanup job) need `MIGRATION_DATABASE_URL` (bypasses RLS)

## References
- SECURITY.md §3 (Anti SQL Injection - RLS)
- CONTEXT.md §4 (Modelo de dados - RLS)
- PROGRESS.md P04 validation (RLS tests)
- AUDIT.md RLS independent proof section
- docs/deploy/render_app_role.sql