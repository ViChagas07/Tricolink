# Tricolink

Um encurtador de URL seguro, *privacy-first*, feito como projeto de portfólio demonstrando engenharia backend, hardening de segurança e UI polida.

**Cole uma URL longa → receba `https://seu-dominio.com/abc1234` → cada visita é um redirect 302 contado com estatísticas.**

[Demo](https://tricolink.vercel.app) · [API Docs](https://tricolink-api.onrender.com/docs) *(placeholder — faça seu próprio deploy)*

## Capturas de Tela

| Landing | Dashboard de Links | Detalhe / Estatísticas |
|---|---|---|
| ![Landing](docs/assets/landing.png) | ![Dashboard](docs/assets/dashboard.png) | ![Stats](docs/assets/stats.png) |

> **Adicione capturas reais:** rode o app localmente, tire prints em 1440×900 (claro e escuro), coloque em `docs/assets/` e atualize os caminhos acima.

---

## Como Funciona

```mermaid
flowchart TD
    A[Usuário cola URL longa] --> B{Autenticado?}
    B -->|Não| C[Anônimo: cota 5/dia, TTL 30 dias]
    B -->|Sim| D[Logado: cota 100/dia, sem expiração]
    C --> E[Valida política de URL]
    D --> E
    E --> F[Gera código de 7 chars base62\n(secrets, retry colisão ≤5)]
    F --> G[Salva no PostgreSQL\nUNIQUE code, RLS forçado]
    G --> H[Retorna URL curta]
    H --> I[Visitante acessa /{code}]
    I --> J[FastAPI /r/{code}]
    J --> K{Cache Redis hit?}
    K -->|Sim| L[Serve stale + refresh background\nSWR + jitter + single-flight]
    K -->|Não| M[Consulta PostgreSQL\n(lock + cache negativo)]
    L --> N[Redirect 302 para URL original]
    M --> N
    N --> O[Empurra evento de clique no Redis Stream\ntl:clicks (nunca bloqueia redirect)]
    O --> P[Flusher assíncrono grava em lote\nincrementa click_count]
```

---

## Stack

| Camada | Tecnologia |
|---|---|
| **Backend** | Python 3.11, FastAPI, Pydantic v2, SQLAlchemy 2 (async) + asyncpg, Alembic |
| **Banco** | PostgreSQL 16 |
| **Cache / Rate limiting** | Redis 7 (cache, token bucket via Lua, locks, stream de cliques) |
| **Auth** | E-mail/senha (argon2id) + Google OAuth2/OIDC (Authlib); JWT em cookies httpOnly |
| **Frontend** | Next.js 16 (App Router), TypeScript, Tailwind CSS, shadcn/ui, Zustand, next-intl, Recharts, lucide-react |
| **Infra** | Docker Compose (dev), GitHub Actions (CI/CD), deploy: Vercel (web) + Render (API, Postgres, Redis) |
| **Testes** | pytest + pytest-asyncio + httpx; Vitest; Playwright; k6 (carga) |
| **Observabilidade** | Prometheus (`/metrics` protegido), logs estruturados, Sentry (opcional) |

**Arquitetura:** Monolito modular com **Clean Architecture dentro de cada módulo** (domain → application → adapters → presentation). SOLID, tipagem estrita, sem `any`, SQL só via SQLAlchemy com parâmetros ligados.

---

## Arquitetura

```mermaid
graph TB
    subgraph API[FastAPI App]
        CORE[core/config.py\nÚnico leitor de env]
        MID[Stack de middlewares\nrequest-id → security headers → metrics → real-IP → timeout → balde global → body limit]
        MOD[Módulos]
        MOD --> ID[identity\nAuth, sessões, Google OIDC]
        MOD --> LK[links\nEncurtar, redirect, cache, cotas]
        MOD --> AN[analytics\nStats, click flusher]
        ID --> DOM_ID[domain]
        LK --> DOM_LK[domain]
        AN --> DOM_AN[domain]
        DOM_ID --> APP_ID[application]
        DOM_LK --> APP_LK[application]
        DOM_AN --> APP_AN[application]
        APP_ID --> AD_ID[adapters\nSQLAlchemy, Redis, Authlib]
        APP_LK --> AD_LK[adapters\nSQLAlchemy, Redis cache]
        APP_AN --> AD_AN[adapters\nSQLAlchemy, Redis cache]
        AD_ID --> PRES_ID[presentation\nFastAPI routers]
        AD_LK --> PRES_LK[presentation\nFastAPI routers]
        AD_AN --> PRES_AN[presentation\nFastAPI routers]
    end

    subgraph WEB[Next.js App]
        PROXY[proxy.ts\nCSP nonce, rewrites, locale]
        PAGES[App Router pages\n/[locale]/*]
        COMP[Components\nshadcn/ui + Tailwind]
        STORE[Zustand stores\nauth, theme]
        I18N[next-intl\n11 locales]
    end

    API <-- rewrites /api/v1/* --> WEB
    API <-- rewrites /:code --> WEB
    API --> PG[(PostgreSQL 16\nRLS FORCE)]
    API --> RD[(Redis 7)]
    WEB --> VERCEL[Vercel]
    API --> RENDER[Render]
```

---

## Início Rápido (Docker)

```bash
# 1. Clone e configure
git clone https://github.com/seu-org/tricolink.git
cd tricolink
cp .env.example .env
# Edite .env com seus segredos (JWT_SECRET, CSRF_SECRET, etc.)

# 2. Suba tudo
make up
# API: http://localhost:8000  |  Web: http://localhost:3000

# 3. Rode os testes
make test-api    # 400+ testes pytest
make test-web    # 100+ Vitest + 20 Playwright

# 4. Lint & type-check
make lint

# 5. Pare
make down
```

### Alvos Make Úteis

| Alvo | Descrição |
|---|---|
| `make up` | Sobe todos os serviços (builda imagens, roda migrations) |
| `make down` | Para e remove containers |
| `make logs` | Segue logs de todos os serviços |
| `make test-api` | Roda testes da API no container |
| `make test-web` | Roda testes do web no container |
| `make lint` | Ruff, mypy, ESLint, TypeScript check |
| `make format` | Auto-fix de formatação |
| `make migrate` | Roda migrations Alembic |
| `make coverage` | Cobertura API (≥85% global, ≥90% domain) |
| `make coverage-domain` | Cobertura só domain |
| `make cleanup` | Roda job de retenção de cliques/links |
| `make observability-up` | Sobe Prometheus + Grafana (portas 9091 / 3002) |

---

## Desenvolvimento Local (sem Docker)

### API
```bash
cd apps/api
poetry install
poetry run alembic upgrade head
poetry run uvicorn tricolink.main:create_app --reload --port 8000
```

### Web
```bash
cd apps/web
pnpm install
pnpm dev
# http://localhost:3000
```

> **Nota:** O Docker Compose é o caminho *validado*. Rodar local exige Postgres 16 e Redis 7 separados.

---

## Variáveis de Ambiente

Todos segredos são lidos **apenas** em `apps/api/src/tricolink/core/config.py` via `os.getenv()`. Nunca commite `.env`.

### API (obrigatórias)

| Variável | Descrição | Exemplo |
|---|---|---|
| `APP_ENV` | `development` \| `production` | `development` |
| `DATABASE_URL` | URL do DB runtime (role app, RLS) | `postgresql+asyncpg://user:pass@host:5432/db` |
| `MIGRATION_DATABASE_URL` | URL admin para migrations | `postgresql+asyncpg://admin:pass@host:5432/db` |
| `REDIS_URL` | Conexão Redis | `redis://redis:6379/0` |
| `JWT_SECRET` | ≥32 bytes aleatórios | `openssl rand -hex 32` |
| `CSRF_SECRET` | ≥32 bytes aleatórios | `openssl rand -hex 32` |
| `SESSION_SECRET` | ≥32 bytes aleatórios | `openssl rand -hex 32` |
| `FRONTEND_ORIGIN` | Origin do web para CORS/CSRF/OAuth | `http://localhost:3000` |
| `SHORT_BASE_URL` | Base para URLs curtas exibidas | `http://localhost:3000` |
| `API_PUBLIC_BASE_URL` | URL pública da API | `http://localhost:8000` |
| `COOKIE_SECURE` | `true` em produção | `false` |
| `TRUSTED_PROXY_COUNT` | Proxies confiáveis para `X-Forwarded-For` | `1` (dev), `2` (Vercel→Render) |

### Auth (opcionais mas recomendados)
| Variável | Descrição |
|---|---|
| `GOOGLE_CLIENT_ID` | Client ID do Google OAuth |
| `GOOGLE_CLIENT_SECRET` | Client secret do Google OAuth |
| `GOOGLE_REDIRECT_URI` | Deve bater exatamente com o Google Cloud Console |

### Rate Limiting & Cache (defaults mostrados)
| Variável | Default | Descrição |
|---|---|---|
| `RL_REDIRECT_CAPACITY` | 120 | Capacidade do balde redirect por IP |
| `RL_REDIRECT_REFILL_PER_SEC` | 20 | Taxa de refill do redirect |
| `RL_CREATE_CAPACITY` | 10 | Capacidade do balde create |
| `RL_CREATE_REFILL_PER_SEC` | 0.2 | Refill do create |
| `RL_AUTH_CAPACITY` | 5 | Capacidade auth (IP + e-mail) |
| `RL_AUTH_REFILL_PER_SEC` | 0.02 | Refill auth |
| `RL_GLOBAL_CAPACITY` | 2000 | Balde global load-shedding |
| `RL_GLOBAL_REFILL_PER_SEC` | 1000 | Refill global |
| `RL_LIST_CAPACITY` | 60 | Balde stats/list por usuário |
| `RL_LIST_REFILL_PER_SEC` | 1 | Refill stats/list |
| `CACHE_HARD_TTL_SECONDS` | 86400 | TTL duro cache redirect |
| `CACHE_SOFT_TTL_SECONDS` | 600 | TTL macio (gatilho SWR) |
| `CACHE_JITTER_PCT` | 0.15 | ±Jitter em todos TTLs |
| `NEGATIVE_CACHE_TTL_SECONDS` | 30 | TTL cache negativo (404) |
| `STATS_CACHE_TTL_SECONDS` | 30 | TTL cache stats |

### Web
| Variável | Descrição |
|---|---|
| `NEXT_PUBLIC_SITE_URL` | Origin público do web |
| `NEXT_PUBLIC_SHORT_BASE_URL` | Base URL curta para o client |
| `API_INTERNAL_URL` | URL interna da API (usada no build para rewrites) |

---

## Referência da API

Base path: `/api/v1` · JSON · Erros: `{ "error": { "code", "message", "details?" } }`

### Links
| Método | Endpoint | Auth | Descrição |
|---|---|---|---|
| `POST` | `/links` | Opcional | Cria link curto. Body: `{ url, alias?, title?, expires_at? }` (alias/title/expires exigem auth). Retorna `{ code, short_url, original_url, created_at, expires_at }` |
| `GET` | `/links` | Obrigatório | Lista links do usuário. Query: `cursor`, `limit` (máx 50), `q` (busca) |
| `GET` | `/links/overview` | Obrigatório | `{ total_clicks, total_links, range }` pro header. Query: `range=7d\|30d\|90d` |
| `GET` | `/links/{code}` | Obrigatório (dono) | Detalhes do link |
| `PATCH` | `/links/{code}` | Obrigatório (dono) | Atualiza `title`, `original_url`, `expires_at`, `is_active` |
| `DELETE` | `/links/{code}` | Obrigatório (dono) | Deleta link (404 se não for dono) |
| `GET` | `/links/{code}/stats` | Obrigatório (dono) | Stats: `{ total, series[{date,clicks}], countries[], devices[], referrers[] }`. Query: `range=7d\|30d\|90d` |

### Auth
| Método | Endpoint | Descrição |
|---|---|---|
| `POST` | `/auth/register` | Cadastro (202, sem sessão) |
| `POST` | `/auth/login` | Login (seta cookies httpOnly) |
| `POST` | `/auth/refresh` | Rotaciona refresh token |
| `POST` | `/auth/logout` | Revoga refresh, limpa cookies |
| `GET` | `/auth/me` | Usuário atual |
| `PATCH` | `/auth/me` | Atualiza `display_name`, `locale` |
| `GET` | `/auth/me/avatar` | Avatar personalizado (8 KB máx) |
| `PUT` | `/auth/me/avatar` | Upload avatar (base64 JPEG/PNG/WebP ≤12K chars) |
| `DELETE` | `/auth/me/avatar` | Remove avatar personalizado |
| `GET` | `/auth/google/login` | Inicia OAuth Google |
| `GET` | `/auth/google/callback` | Callback OAuth |

### Ops
| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/health/live` | Liveness probe |
| `GET` | `/health/ready` | Readiness (DB + Redis + tabelas) |
| `GET` | `/metrics` | Prometheus (Bearer `METRICS_TOKEN`) |

### Redirect (público)
| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/r/{code}` | **302** pra URL original; **404** se não existe; **410** se expirado/inativo. `Cache-Control: no-store`, `X-Robots-Tag: noindex, nofollow` |

---

## Internacionalização (i18n)

11 idiomas via `next-intl`:
- `en` (default), `pt-BR`, `es`, `fr`, `de`, `it`, `ja`, `ko`, `zh-CN`, `ru`, `ar` (RTL)

- `localePrefix: always` → todas URLs prefixadas (`/en/links`, `/pt-BR/links`)
- Detecção por Accept-Language ativada
- Mensagens em `apps/web/messages/<locale>.json` (namespaces: `nav`, `hero`, `demo`, `features`, `faq`, `auth`, `links`, `account`, `errors`, `footer`, `meta`)
- `pt-BR` e `en` são referência; demais são geradas por IA e **marcadas para revisão humana** (veja `PROGRESS.md`)
- CI falha se faltar chave: `pnpm i18n:check`
- Datas/números via `Intl`; `hreflang`, sitemap, OG por locale

---

## Testes

### API (pytest)
```bash
make test-api                              # Todos testes
docker compose run --rm api pytest -q tests/security   # Só suite segurança
docker compose run --rm api pytest --cov=tricolink --cov-fail-under=85
docker compose run --rm api pytest --cov=tricolink --cov-report=term-missing
```

**Gates (CI):**
- Cobertura global ≥ 85% (atual: **90,40%**)
- Cobertura domain ≥ 90% (atual: **96%**)
- Ruff, mypy, format check devem passar

### Web (Vitest + Playwright)
```bash
cd apps/web
pnpm test           # Unit/component (91 testes)
pnpm test:e2e       # Playwright (20 testes, Chromium)
pnpm lint           # ESLint
pnpm typecheck      # tsc --noEmit
pnpm i18n:check     # Todos 11 locales completos
```

### Carga (k6)
```bash
# Na raiz do repo, com API + Postgres + Redis rodando
docker compose exec -T redis redis-cli FLUSHDB
Get-Content -Raw loadtest/redirect.js | docker run --rm -i --network tricolink_app -e BASE_URL=http://api:8000 -e MODE=warm grafana/k6 run -
Get-Content -Raw loadtest/redirect.js | docker run --rm -i --network tricolink_app -e BASE_URL=http://api:8000 -e MODE=cold grafana/k6 run -
Get-Content -Raw loadtest/create.js   | docker run --rm -i --network tricolink_app -e BASE_URL=http://api:8000 -e MODE=throughput grafana/k6 run -
```

**Resultados reais (Docker Desktop, Ryzen 7 5800X, 16 GB):**
- Redirect warm: **101 RPS**, p50 **4,84 ms**, p95 **942 ms**, 0 429
- Redirect cold (500 códigos): **88,5 RPS**, p50 **342 ms**, 100% 302
- Redirect rate limit: **8.531 429** (83,2%)
- Create throughput: **72,7 RPS**, p50 **69,8 ms**
- Create rate limit (IP fixo): **2.530 429** (99,8%, cota diária 5)

> Metodologia completa e ressalvas em `docs/perf/RESULTS.md`. Números são locais, não extrapolação de produção.

---

## Deploy

**Caminho validado:** Vercel (web) + Render (API, Postgres, Redis) via GitHub Actions.

### 1. Render (API + DB + Redis + Cron)
1. Render Dashboard → **New → Blueprint** → selecione repo → lê `render.yaml`
2. Cria: `tricolink-api` (Docker, estágio `runtime`), `tricolink-db` (Postgres), `tricolink-redis` (Key Value), `tricolink-cleanup` (cron 03:00 UTC)
3. **Obrigatório:** Rode `docs/deploy/render_app_role.sql` na conexão admin do Postgres para criar role `tricolink_app` (`NOSUPERUSER NOBYPASSRLS`). Configure `DATABASE_URL` pra esse role.
4. Defina todas variáveis de `docs/deploy/DEPLOY.md §3.1` (JWT_SECRET, FRONTEND_ORIGIN, TRUSTED_PROXY_COUNT=2, etc.)
5. `preDeployCommand: alembic upgrade head` roda migrations usando `MIGRATION_DATABASE_URL` (admin)

### 2. Vercel (Web)
1. Importe repo → Root Directory: `apps/web`
2. Build Command: `pnpm build` (Turbopack)
3. Env vars (Production + Preview):
   - `API_INTERNAL_URL=https://tricolink-api.onrender.com`
   - `NEXT_PUBLIC_SITE_URL=https://seu-app.vercel.app`
   - `NEXT_PUBLIC_SHORT_BASE_URL=https://seu-app.vercel.app`
4. **Nenhum segredo** na Vercel (sem `NEXT_PUBLIC_` pra segredo)

### 3. GitHub Actions
- `.github/workflows/ci.yml`: lint, typecheck, test (API + Web), security (gitleaks, pip-audit, pnpm audit), Docker build
- `.github/workflows/deploy.yml`: manual (`workflow_dispatch`) ou tag `v*` → chama deploy hooks Render/Vercel → health checks

> **Ainda não executado no CI:** GitHub Actions runs, Render Blueprint apply, Vercel deploy. Veja `docs/deploy/DEPLOY.md` pra checklist completo.

---

## Decisões de Engenharia

### 302 vs 301
**302 (Found)** é usado nos redirects. Um 301 seria cacheado por navegadores/CDNs, quebrando contagem de cliques e tornando edições/expiração ineficazes. 302 garante que todo hit chega na API.

### Geração de Código e Colisões
- 7 chars base62 via `secrets` (criptograficamente seguro, não `random`)
- `UNIQUE(code)` no PostgreSQL; em `IntegrityError` retry até 5 vezes
- Alias custom: regex `^[A-Za-z0-9_-]{3,32}$` + lista reservada (rotas, locales, `admin`, `api`, etc.); 409 em conflito

### SWR + Jitter + Single-Flight + Cache Negativo (Por Quê?)
**Problema:** Cache stampede em chaves frias → *thundering herd* no PostgreSQL.
**Solução (3 camadas):**
1. **Stale-While-Revalidate:** TTL macio (600s) serve stale enquanto um refresh background roda; TTL duro (86400s) é expiração da chave Redis.
2. **Jitter (±15%)** em todos TTLs evita expiração sincronizada entre chaves.
3. **Single-flight:** Deduplicação em-processo + `SET NX PX` lock Redis cross-process. Só um loader bate no DB; outros esperam com jitter e relêem cache.
4. **Cache negativo** (`tl:neg:{code}`, 30s) pra códigos inexistentes bloqueia ataques de varredura/penetração de cache.

### Pipeline Assíncrono de Cliques (Redis Stream + Flusher)
- Redirect **nunca espera** INSERT. `XADD` no stream `tl:clicks` (fire-and-forget).
- Flusher background (task no lifespan) consome via consumer group, faz batch `click_events` INSERT + `links.click_count` UPDATE numa transação.
- Redis cai → evento descartado, métrica `clicks_dropped_total` incrementada, redirect continua.
- Flusher recria consumer group em `NOGROUP` (resiliência failover/FLUSHDB).
- Flusher invalida as três janelas de cache stats (`7d`, `30d`, `90d`) após commit → página de detalhe reflete `click_count` imediatamente.

### Token Bucket em Lua
Script Lua único atômico (`refill + consume`) usando `TIME` do Redis (clock server-side). Retorna `allowed, remaining, retry_after_ms`. Sem race conditions. Redis indisponível → circuit breaker abre → **fallback em memória por processo** (continua limitando, nunca "libera tudo").

### Circuit Breaker + Bulkhead
- **Circuit Breaker** (closed/open/half-open) nos clientes Redis e Postgres. Clock injetável pra testes. Half-open com sondas limitadas.
- **Bulkheads nomeados** (semáforos): `db_read` (20), `db_write` (10), `hashing` (4, argon2 em threadpool), `dns` (10). Impede que uma dependência saturada trave as outras.

### Servidor Nunca Busca a URL do Usuário
Superfície SSRF zero: a API **nunca** faz HTTP outbound pra URLs do usuário. `UrlPolicy` valida só na criação (resolve DNS + checa IPs, normaliza IDN, bloqueia privados/metadata/loopback/own-domain). Sem preview, sem fetch de título.

### Privacidade (Sem IP Armazenado)
- `click_events` guarda só: `country` (header edge `X-Vercel-IP-Country` / `CF-IPCountry`), `device`, `browser`, `referrer_host` (sem path/query).
- **Nenhum IP**, nenhum User-Agent bruto. LGPD/GDPR friendly por design.
- Cotas diárias hasheiam IP (SHA-256) no Redis; nenhum IP em claro persistido.

### Row Level Security (RLS)
- `links` e `refresh_tokens`: `RLS ENABLE` + `FORCE` com policies em `app.current_user_id` (setado via `SET LOCAL` por transação).
- Role runtime `tricolink_app` é `NOSUPERUSER NOBYPASSRLS`.
- Defesa em profundidade: app checa dono **e** DB força. Mesmo com SQL injection, leituras/escritas cross-user retornam 0 linhas.

---

## Resumo de Segurança

Auditoria completa em `docs/security/AUDIT.md` (P09). **Zero achados críticos/altos em aberto.**

| Área | Status |
|---|---|
| Token bucket (Lua, atômico) | ✅ Testado sob concorrência |
| Circuit breaker + bulkhead | ✅ Todas dependências |
| SQL injection | ✅ ORM only, RLS forçado, testes ofensivos passam |
| XSS / CSP | ✅ Nonce por request, `strict-dynamic`, sem `unsafe-inline` em `script-src` (`style-src-attr` exceção Recharts documentada) |
| Auth / força bruta | ✅ Argon2id OWASP, refresh rotativo, detecção reuso, baldes IP+e-mail, lockout, sem enumeração |
| SSRF / abuso URL | ✅ DNS resolve + todos IPs checados, bloqueia privados/metadata/own-domain, sem fetch outbound |
| Segredos | ✅ `.env` gitignored, gitleaks limpo, `os.getenv` só em `config.py`, sem segredos no bundle client |
| Supply chain | ✅ Lockfiles commitados, Dependabot, `pip-audit`/`pnpm audit --prod` limpos |

**Riscos residuais (aceitos, documentados):**
- R-01: Sem verificação de e-mail no cadastro local (squatting possível)
- R-02: Access JWT não revogado no logout (válido até `exp`, default 10 anos)
- R-03: Gap invalidação cache se Redis falha durante invalidação
- R-04: `click_events` sem RLS
- R-05: `/health/ready` isento do balde global
- R-06: `TRUSTED_PROXY_COUNT` confia na topologia
- R-10: `style-src-attr 'unsafe-inline'` pro Recharts

---

## Resumo de Performance

Medidas k6 reais (local Docker Desktop, **não produção**):

| Cenário | RPS | p50 | p95 | p99 | Notas |
|---|---:|---:|---:|---:|---|
| Redirect warm | **101** | **4,8 ms** | **942 ms** | 1,6 s | 0 429, 42 5xx (limite concorrência) |
| Redirect cold (500 códigos) | **88,5** | **342 ms** | 1,5 s | 1,5 s | 100% 302, single-flight evita stampede |
| Redirect rate limit | 157 | 2,5 ms | 177 ms | 2,2 s | **8.531 429** (83,2%) |
| Create throughput | **72,7** | **69,8 ms** | 881 ms | 1,1 s | 99,85% 201 |
| Create rate limit (IP fixo) | 46 | 3,2 ms | 21 ms | 158 ms | **2.530 429** (99,8%, cota diária) |

**Gargalo:** `--limit-concurrency 200` no Uvicorn dev. Produção (Gunicorn + WAF) muda o teto. **Não extrapole.**

Dados completos: `docs/perf/RESULTS.md`

---

## Roadmap

Honesto, não comprometido:

- [ ] Geração de QR Code pros links curtos
- [ ] Domínios customizados (traga seu domínio)
- [ ] Integração Safe Browsing API (checagem malware/phishing)
- [ ] Preservação / builder de parâmetros UTM
- [ ] Link-in-bio / Pages
- [ ] Suporte a times/workspaces
- [ ] Extensão de navegador
- [ ] API pública com tokens escopados
- [ ] Verificação de e-mail pra contas locais
- [ ] Denylist de access token (revogar no logout)

---

## Limitações Conhecidas

De `PROGRESS.md > Não validado` e revisões pendentes:

- **Sem execução real de CI/CD:** Workflows GitHub Actions passam `actionlint` mas nunca rodaram em runners GitHub.
- **Sem deploy em produção:** Render Blueprint, projeto Vercel, e hipótese `TRUSTED_PROXY_COUNT=2` não testados.
- **Sem validação Linux/macOS:** Todos containers testados só no Docker Desktop/Windows.
- **Sem testes Firefox/WebKit:** Playwright roda só Chromium.
- **Sem verificação de e-mail:** Cadastro local permite squatting (AUDIT R-01).
- **Access JWT não revogado no logout:** Válido até expiração (AUDIT R-02).
- **Cliques at-least-once:** Crash do flusher entre commit e `XACK` pode duplicar `click_events`/`click_count` (sem chave idempotência).
- **DNS não fixado:** `UrlPolicy` resolve na criação; mudanças posteriores de DNS não protegidas (mitigado por sem fetch outbound).
- **Google OIDC não testado contra IdP real:** Mockado nos testes apenas.
- **Role/SSL/citext Postgres gerenciado Render** não verificados.
- **Modo multiprocess Prometheus** não implementado (2 workers gunicorn → cada scrape vê métricas de um worker).
- **Lighthouse mobile Performance < 95:** Melhor 89 (LCP no logo hero). Desktop 99.
- **Traduções pendentes revisão humana:** `es`, `fr`, `de`, `it`, `ja`, `ko`, `zh-CN`, `ru`, `ar` (244 chaves total; `pt-BR`/`en` são referência).
- **Imagem Docker `runner` (web standalone)** não revalidada após fixes P10.
- **Limite de header** não testado ponta-a-ponta (default Uvicorn ~16 KB).

---

## ADRs

Veja `docs/ADR/` para Architecture Decision Records:
- `001-modular-monolith-clean-architecture.md`
- `002-302-redirect-for-click-counting.md`
- `003-swr-jitter-single-flight-negative-cache.md`
- `004-async-click-pipeline-redis-stream.md`
- `005-lua-token-bucket-rate-limiting.md`
- `006-circuit-breaker-bulkhead-resilience.md`
- `007-rls-defense-in-depth.md`

---

## Contribuindo

Veja `CONTRIBUTING.md` para diretrizes (commits convencionais, TDD, gates de lint, processo ADR).

---

## Licença

MIT — veja `LICENSE`.