# CONTEXT.md — Tricolink (fonte única da verdade)

## 1. Produto
**Tricolink** é um encurtador de URL (projeto de portfólio, foco em engenharia backend + segurança + UI polida).
Fluxo: o usuário cola uma URL longa → recebe `https://<dominio>/<codigo>` → quem acessa o link curto é
redirecionado (HTTP 302) e o clique é registrado para estatísticas.
Interface inspirada na página de encurtador do Bitly, em versão **mediana** (sem QR Code, Pages, UTM, domínio próprio, IA, planos pagos).
Identidade visual: cores do EC Bahia (azul, branco e vermelho). **Não usar escudo/marca do clube**, só as cores.

## 2. Stack (decidida — não trocar)
| Camada | Tecnologia |
|---|---|
| Backend | Python 3.11 (Poetry), FastAPI, Pydantic v2, SQLAlchemy 2 assíncrono + asyncpg, Alembic |
| Banco | PostgreSQL 16 |
| Cache/limites | Redis 7 (cache, token bucket via Lua, locks, buffer de cliques) |
| Auth | e-mail+senha (argon2id) + Google OAuth2/OIDC (Authlib); JWT em cookies httpOnly |
| Frontend | Next.js (App Router, TypeScript), Tailwind CSS, shadcn/ui, Zustand, next-intl, Recharts, lucide-react |
| Infra | Docker Compose (dev), GitHub Actions (CI/CD), deploy: Vercel (web) + Render ou similar (api, postgres, redis) |
| Testes | TDD: pytest + pytest-asyncio + httpx; Vitest; Playwright; k6 (carga) |
| Observabilidade | Prometheus (`/metrics` protegido), logs estruturados, Sentry opcional |

Arquitetura: **monolito modular**, com **Clean Architecture dentro de cada módulo** (domain → application → adapters → presentation). SOLID e Clean Code. Evitar N+1 (eager loading). Credenciais só por variáveis de ambiente, lidas com `os.getenv()` num único arquivo (`core/config.py`); nunca hardcoded.

## 3. Estrutura do monorepo
```
repo/
├─ apps/
│  ├─ api/                      # FastAPI
│  │  ├─ pyproject.toml
│  │  ├─ alembic/ + alembic.ini
│  │  ├─ src/tricolink/
│  │  │  ├─ main.py
│  │  │  ├─ core/               # config.py, logging.py, middleware/, deps.py
│  │  │  ├─ shared_kernel/      # errors.py, security_errors.py, clock.py, ids.py
│  │  │  ├─ infra/              # db/, cache/, ratelimit/, resilience/, observability/
│  │  │  └─ modules/
│  │  │     ├─ identity/        # domain/ application/ adapters/ presentation/
│  │  │     ├─ links/           # idem
│  │  │     └─ analytics/       # idem
│  │  └─ tests/ (unit/, integration/, security/)
│  └─ web/                      # Next.js
│     ├─ messages/              # 11 idiomas
│     ├─ src/app/[locale]/...
│     ├─ src/components/ src/lib/ src/stores/ src/i18n/
│     └─ public/
├─ docs/agent/                  # esta pasta (SDD)
├─ docs/security/               # AUDIT.md (fase P09)
├─ docker-compose.yml  Makefile  .env.example  .github/workflows/
└─ graphify-out/
```

## 4. Modelo de dados (PostgreSQL)
- `users`: id UUID PK, email CITEXT UNIQUE NOT NULL, password_hash TEXT NULL (NULL se só Google), google_sub TEXT UNIQUE NULL, display_name VARCHAR(80), locale VARCHAR(8), is_active BOOL default true, created_at TIMESTAMPTZ.
- `refresh_tokens`: id UUID PK, user_id FK, family_id UUID, token_hash TEXT UNIQUE (SHA-256), expires_at, revoked_at NULL, created_at. (rotação + detecção de reuso por família)
- `links`: id BIGSERIAL PK, code VARCHAR(32) UNIQUE NOT NULL (case-sensitive), original_url TEXT NOT NULL CHECK(char_length<=2048), title VARCHAR(120) NULL, user_id UUID NULL FK (NULL = anônimo), is_custom_alias BOOL, is_active BOOL default true, expires_at TIMESTAMPTZ NULL, click_count BIGINT default 0, created_at, updated_at. CHECK `code ~ '^[A-Za-z0-9_-]{3,32}$'`. Índices: UNIQUE(code), (user_id, created_at DESC), (expires_at) parcial.
- `click_events`: id BIGSERIAL PK, link_id FK, clicked_at TIMESTAMPTZ, country CHAR(2) NULL, device VARCHAR(10) (desktop|mobile|tablet|bot|unknown), browser VARCHAR(30) NULL, referrer_host VARCHAR(255) NULL. Índice (link_id, clicked_at). **Não armazenar IP** (privacidade/LGPD). País vem de header do edge (`X-Vercel-IP-Country` / `CF-IPCountry`) quando existir; senão NULL. Sem consulta a serviço externo.

## 5. API REST (`/api/v1`, JSON, erros no formato `{ "error": { "code", "message", "details?" } }`)
Links:
- `POST /links` — cria (anônimo permitido). Body: `{ url, alias?, title?, expires_at? }` (alias/title/expires só para logados). Resp: `{ code, short_url, original_url, created_at, expires_at }`
- `GET /links?cursor=&limit=&q=` — lista do usuário (paginação por cursor, limit máx 50)
- `GET /links/overview?range=7d|30d|90d` — `{ total_clicks, total_links, range }` do usuário (cabeçalho de `/links`)
- `GET /links/{code}` · `PATCH /links/{code}` (title, original_url, expires_at, is_active) · `DELETE /links/{code}` — só o dono (404 se não for dono, para não vazar existência)
- `GET /links/{code}/stats?range=7d|30d|90d` — `{ total, series[{date,clicks}], countries[], devices[], referrers[] }`
Auth: `POST /auth/register` · `POST /auth/login` · `POST /auth/refresh` · `POST /auth/logout` · `GET /auth/me` · `PATCH /auth/me` · `GET /auth/google/login` · `GET /auth/google/callback`
Ops: `GET /health/live` · `GET /health/ready` · `GET /metrics` (token)
Redirect (público): `GET /r/{code}` → 302 `Location: <original_url>`; 404 (inexistente) / 410 (expirado/inativo) com HTML estático mínimo, `X-Robots-Tag: noindex`.

## 6. Redirect e cache (caminho quente)
- Código gerado: 7 chars base62 via `secrets` (nunca `random`). UNIQUE no banco; em colisão (IntegrityError) tentar de novo até 5 vezes.
- Alias customizado: regex `^[A-Za-z0-9_-]{3,32}$`; lista reservada (login, account, links, api, r, en, pt-br, es, fr, de, it, ja, ko, zh-cn, ru, ar, admin, static, _next, favicon.ico, robots.txt, sitemap.xml, llms.txt…); 409 se existir.
- Usar **302** (não 301) para que o navegador não faça cache e os cliques sejam contados. Documentar a decisão no README.
- Chaves Redis: `tl:link:{code}` (JSON `{id,u,e,s}`), `tl:lock:{code}`, `tl:neg:{code}`, `tl:clicks` (Stream).
- **Anti cache stampede (três camadas combinadas):**
  1. **Stale-While-Revalidate:** TTL duro `CACHE_HARD_TTL_SECONDS`; TTL macio `CACHE_SOFT_TTL_SECONDS`. Passou do macio → serve o valor em cache e atualiza em background, protegido por lock.
  2. **Jitter** de ±`CACHE_JITTER_PCT` em todos os TTLs (evita expiração simultânea).
  3. **Single-flight:** em miss total, só quem pegar `SET tl:lock:{code} NX PX LOCK_TTL_MS` consulta o banco; os demais esperam curtos intervalos (com jitter) e releem o cache; se estourar o tempo, caem para o banco via Bulkhead.
  - **Cache negativo** (`tl:neg:{code}`, TTL curto) para códigos inexistentes (anti-varredura/penetração de cache).
- PATCH/DELETE/expiração → invalidar `tl:link:{code}` imediatamente.
- Expiração é checada na hora do redirect mesmo com cache (campo `e`).
- **Cliques**: o redirect NUNCA espera o INSERT. Empurra evento no Redis Stream `tl:clicks`; um flusher assíncrono (task no lifespan) grava em lote em `click_events` e incrementa `links.click_count` (UPDATE em lote). Redis fora do ar → descartar evento com métrica `clicks_dropped_total` (redirect continua).
- Política de URL (anti-abuso): só `http`/`https`; máx 2048; sem credenciais embutidas (`user:pass@`); host obrigatório; bloquear localhost, IPs privados/loopback/link-local/metadata (resolver DNS e checar todos os IPs); bloquear URLs que apontem para o próprio domínio do Tricolink (loop); normalizar IDN/punycode; rejeitar caracteres de controle.
- Cotas: anônimo `ANON_DAILY_LINK_LIMIT`/dia por IP (links anônimos expiram em `ANON_LINK_TTL_DAYS`); logado `USER_DAILY_LINK_LIMIT`/dia.

## 7. Roteamento frontend (next-intl, prefixo de locale sempre)
`/[locale]` (landing) · `/[locale]/login` · `/[locale]/account` · `/[locale]/links` · `/[locale]/links/[code]` (detalhe/estatísticas) · `/[locale]/link-unavailable` (opcional).
Links curtos ficam na raiz: `/{code}` → como não existe página, `next.config` usa **`rewrites().fallback`** para encaminhar `/:code` → `${API_INTERNAL_URL}/api/v1/r/:code` (o middleware do next-intl **não** pode capturar esses caminhos: `matcher` só para `/` e `/(<locales>)/:path*`). O navegador só fala com o domínio do frontend (`/api/v1/*` também via rewrites).
Rotas de `/links*` e `/account` exigem login (redirecionar para `/login?next=...` com `next` validado contra open redirect: só caminhos internos começando com `/` e não `//`).

## 8. i18n (next-intl)
- 11 idiomas: `pt-BR`, `en`, `es`, `fr`, `de`, `it`, `ja`, `ko`, `zh-CN`, `ru`, `ar` (árabe com layout RTL; usar propriedades lógicas do CSS — `ms-*`, `ps-*`, `text-start`).
- `defaultLocale: 'en'`, detecção por Accept-Language ativada, `localePrefix: 'always'`.
- Mensagens em `apps/web/messages/<locale>.json`, namespaces por tela (`nav`, `hero`, `demo`, `features`, `faq`, `auth`, `links`, `account`, `errors`, `footer`, `meta`).
- `pt-BR` e `en` são as versões de referência; as demais são geradas e marcadas para revisão humana no `PROGRESS.md`.
- Script `pnpm i18n:check` falha o CI se faltar chave em qualquer idioma.
- Datas/números com `Intl` via next-intl. Metadados (title/description/OG), `hreflang` e sitemap por idioma.

## 9. UI/UX (resumo — detalhes em UI_SPEC.md)
Navbar: igual à do AImaginator (logo no canto superior esquerdo, seletor de idiomas ao lado, itens à direita), **sem a rota Galeria** e com **"Links"** no lugar de "Estúdio". Landing: navbar → hero com barra de URL → demonstração do painel → blocos de recursos → FAQ → CTA → rodapé. Login e Account semelhantes aos do Bitly.

## 10. Não-objetivos (não implementar)
QR Code, Pages/link-na-bio, UTM, domínios customizados, planos pagos, IA, extensão de navegador, app mobile, equipes/workspaces.
