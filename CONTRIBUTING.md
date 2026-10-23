# Contributing to Tricolink

Thank you for considering a contribution! This project follows a disciplined workflow to maintain quality.

## Quick Start

```bash
git clone https://github.com/your-org/tricolink.git
cd tricolink
cp .env.example .env
# Fill in secrets (JWT_SECRET, CSRF_SECRET, etc.)
make up
make test-api
make test-web
make lint
```

## Development Workflow

1. **Create an issue** describing the problem or feature
2. **Fork & branch**: `git checkout -b feat/your-feature` or `fix/your-fix`
3. **TDD**: Write failing test → implement → refactor
4. **Verify locally**:
   - `make test-api` (all pytest pass)
   - `make test-web` (Vitest + Playwright pass)
   - `make lint` (ruff, mypy, ESLint, tsc all clean)
   - `make coverage` (global ≥85%, domain ≥90%)
5. **Commit** with conventional commits
6. **Open PR** with description linking the issue

## Conventional Commits

All commits must follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(links): add custom alias validation
fix(auth): prevent refresh token reuse
test(analytics): add stats cache invalidation test
docs(readme): update deploy instructions
refactor(core): extract Settings into frozen dataclass
chore(deps): update pydantic to v2.10
```

Scope = module (`links`, `identity`, `analytics`, `core`, `infra`, `web`) or cross-cutting (`docs`, `deps`, `ci`).

## Code Standards

- **Python**: Ruff (format + lint), mypy strict, type hints everywhere, no `any`
- **TypeScript**: ESLint + Prettier, strict mode, no `any`
- **SQL**: Only SQLAlchemy ORM/Core with bound parameters; zero f-string SQL
- **Tests**: Every new endpoint needs auth-negative test, rate-limit test, schema validation
- **Security**: No `dangerouslySetInnerHTML`, no `eval`, no secrets in client bundle
- **Accessibility**: POUR principles, visible focus, ARIA, `prefers-reduced-motion`

## Architecture Decision Records (ADR)

Significant architectural decisions require an ADR in `docs/ADR/`:
1. Copy `docs/ADR/000-template.md` (if exists) or create new numbered file
2. Include: Status, Context, Decision, Rationale, Consequences, References
3. Link ADR in PR description

## Pull Request Checklist

- [ ] All tests pass (`make test-api && make test-web`)
- [ ] Lint clean (`make lint`)
- [ ] Coverage gates met (`make coverage`)
- [ ] Conventional commit messages
- [ ] No secrets in diff
- [ ] ADR added if architectural change
- [ ] `PROGRESS.md` updated if phase work
- [ ] `CONTEXT.md` updated if stack/data model/API changed

## Security

- Report vulnerabilities privately via GitHub Security Advisories
- Never commit `.env`, `.env.render`, or any secrets
- `gitleaks` runs in CI; false positives must be resolved in `.gitleaks.toml`

## License

By contributing, you agree your contributions will be licensed under the MIT License (see `LICENSE`).