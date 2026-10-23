# Deploy — Vercel (web) + Render (API/Postgres/Redis)

Este documento é executável por outra pessoa. Ele descreve o caminho usado pelo projeto:
o Next.js roda na **Vercel**, a API FastAPI + Postgres + Key Value (Redis) rodam no
**Render**, e o GitHub Actions dispara os deploys. O `render.yaml` da raiz é o blueprint
do Render; o web usa o `next.config.ts` (sem `vercel.json`).

> **Não validado nesta máquina:** não há credenciais de Vercel/Render no ambiente local.
> O que foi validado: build de produção, `next start`, rewrites de links curtos, cookies
> `__Host-`, headers/CSP, E2E e o compose. Os passos abaixo marcam o que precisa ser
> confirmado no primeiro deploy real.

## 1. Arquitetura

```
navegador
  │  https://<web>.vercel.app/api/v1/*  (rewrite same-origin)
  ▼
Vercel (Next.js)
  │  API_INTERNAL_URL=https://tricolink-api.onrender.com
  ▼
Render Web Service (Docker, FastAPI)
  ├── Render Postgres (MIGRATION_DATABASE_URL admin / DATABASE_URL app role)
  └── Render Key Value (REDIS_URL)
        ▲
Render Cron (limpeza diária) ── Postgres admin
```

Links curtos: `https://<web>.vercel.app/<code>` → `next.config.ts` faz
`rewrites().afterFiles`/`fallback` para `${API_INTERNAL_URL}/api/v1/r/<code>` → API
responde `302` para a URL original. O rewrite externo é suportado pela Vercel; o
`<code>` de 7 caracteres não colide com rotas do Next nem com os locales.

## 2. Pré-requisitos

- Conta Render (Blueprint) e conta Vercel.
- Repositório no GitHub com este código.
- Domínio/URL final do web (pode ser o `.vercel.app`) e da API (`.onrender.com`).
- Um segredo forte para o role `tricolink_app` (gerencie no cofre; nunca no git).
- `psql` local ou o Shell do Render para rodar o SQL do role.
- Opcional: projeto Sentry (só o DSN) e Google OAuth Client.

## 3. Render — API, Postgres, Key Value e cron

1. Render Dashboard → **New** → **Blueprint** → selecione o repositório.
   O Render lê `render.yaml` e cria:
   - `tricolink-api` (Docker, `apps/api/Dockerfile`, target `runtime`);
   - `tricolink-db` (Postgres);
   - `tricolink-redis` (Key Value, rede privada);
   - `tricolink-cleanup` (cron diário, `03:00` UTC).
2. O Blueprint pedirá os valores `sync: false`. Preencha:
   - `DATABASE_URL`: comece com a connection string do **role de runtime**
     `tricolink_app` (veja o passo 3).
   - `FRONTEND_ORIGIN`: `https://<web>.vercel.app` (sem barra no fim).
   - `SHORT_BASE_URL`: `https://<web>.vercel.app`.
   - `API_PUBLIC_BASE_URL`: `https://tricolink-api.onrender.com`.
   - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI` (opcional).
     `GOOGLE_REDIRECT_URI=https://<web>.vercel.app/api/v1/auth/google/callback`
     (o callback passa pelo rewrite da Vercel, então o cookie é gravado no domínio
     do web, não no `onrender.com`).
   - `SENTRY_DSN` (opcional).
   - `TRUSTED_PROXY_COUNT=2` no blueprint. A cadeia é navegador → Vercel → Render;
     confirme no staging com o header `X-Forwarded-For` antes de confiar em IP real.
3. **Role de runtime (obrigatório para RLS):** conecte no Postgres do Render como
   usuário administrativo (`MIGRATION_DATABASE_URL`) e execute
   `docs/deploy/render_app_role.sql` com uma senha forte. O role é
   `NOSUPERUSER NOBYPASSRLS`, sem ownership das tabelas. Depois configure
   `DATABASE_URL=postgresql+asyncpg://tricolink_app:<senha>@<host>:5432/tricolink`
   (o `Settings` também aceita `postgresql://`, `postgres://`, `jdbc:postgresql://`,
   `postgresql+psycopg://` e valores entre aspas, normalizando todos para `+asyncpg`;
   cole o valor **sem aspas**).
   - Se as tabelas ainda não existem, rode o SQL antes do primeiro deploy; os
     `ALTER DEFAULT PRIVILEGES` cobrem as tabelas que as migrations criarem.
   - Se preferir criar o role depois do primeiro deploy, use o Shell do Render e
     faça um novo deploy com o `DATABASE_URL` do app role.
4. O `preDeployCommand: alembic upgrade head` roda as migrations a cada deploy usando
   `MIGRATION_DATABASE_URL` (admin). Não coloque o role de runtime em
   `MIGRATION_DATABASE_URL`.
5. O cron usa o mesmo `MIGRATION_DATABASE_URL` para apagar links expirados e
   `click_events` além de `CLICK_RETENTION_DAYS` (padrão 365). O job é idempotente.
6. Health check do Render: `GET /health/ready`. Logs: Render → serviço → Logs.
7. Para deploy manual sem GitHub Actions: Render Dashboard → serviço → **Manual Deploy**
   → **Deploy latest commit**. As migrations rodam no pre-deploy.

### 3.1 Variáveis do serviço `tricolink-api`

| Variável | Exemplo / origem | Obrigatória | Observação |
|---|---|---|---|
| `APP_ENV` | `production` | sim | desliga `/docs` e `/openapi.json` |
| `COOKIE_SECURE` | `true` | sim | `__Host-`/`__Secure-` |
| `COOKIE_DOMAIN` | vazio | não | mantenha vazio para `__Host-` |
| `TRUSTED_PROXY_COUNT` | `2` | sim | Vercel + proxy Render; confirme |
| `FRONTEND_ORIGIN` | `https://<web>` | sim | Origin/CSRF e redirect OAuth |
| `SHORT_BASE_URL` | `https://<web>` | sim | links exibidos |
| `API_PUBLIC_BASE_URL` | `https://tricolink-api.onrender.com` | sim | URL pública da API |
| `DATABASE_URL` | role `tricolink_app` | sim | runtime, RLS aplica |
| `MIGRATION_DATABASE_URL` | `fromDatabase` (admin) | sim | migrations/pre-deploy |
| `REDIS_URL` | `fromService` Key Value | sim | `redis://`/`rediss://` |
| `JWT_SECRET` | `generateValue` | sim | ≥32 chars |
| `CSRF_SECRET` | `generateValue` | sim | ≥32 chars |
| `SESSION_SECRET` | `generateValue` | sim | OAuth state/session |
| `METRICS_TOKEN` | `generateValue` | sim | `/metrics` Bearer |
| `GOOGLE_CLIENT_ID` | OAuth Client | não | ausente = botão Google desabilitado |
| `GOOGLE_CLIENT_SECRET` | OAuth Client | não | par com o ID |
| `GOOGLE_REDIRECT_URI` | `https://<web>/api/v1/auth/google/callback` | não | callback via Vercel |
| `SENTRY_DSN` | DSN | não | erros sem PII |
| `CLICK_RETENTION_DAYS` | `365` | não | retenção do cron |
| `CLEANUP_BATCH_SIZE` | `5000` | não | lote do cron |
| `RL_*`, `DB_*`, `REDIS_*`, `CIRCUIT_*` | defaults | não | ajuste por carga |

### 3.2 Variáveis do cron `tricolink-cleanup`

| Variável | Exemplo / origem | Obrigatória |
|---|---|---|
| `APP_ENV` | `production` | sim |
| `COOKIE_SECURE` | `true` | sim (validação de produção) |
| `DATABASE_URL` | role `tricolink_app` | sim |
| `MIGRATION_DATABASE_URL` | `fromDatabase` (admin) | sim (é o usado pelo job) |
| `JWT_SECRET` | `fromService` API | sim (validação de produção) |
| `CSRF_SECRET` | `fromService` API | sim |
| `SESSION_SECRET` | `fromService` API | sim |
| `METRICS_TOKEN` | `fromService` API | sim |
| `CLICK_RETENTION_DAYS` | `365` | sim |
| `CLEANUP_BATCH_SIZE` | `5000` | sim |

## 4. Vercel — web

1. Vercel → **Add New** → **Project** → importe o repositório.
2. **Root Directory:** `apps/web`. Framework: Next.js (detectado).
3. Install Command: `pnpm install --frozen-lockfile`. Build Command: `pnpm build`.
4. Environment Variables (Production e Preview):
   - `API_INTERNAL_URL=https://tricolink-api.onrender.com` (sem barra final; o build
     congela os rewrites).
   - `NEXT_PUBLIC_SITE_URL=https://<web>.vercel.app` (ou domínio custom).
   - `NEXT_PUBLIC_SHORT_BASE_URL=https://<web>.vercel.app` (se usado no client).
   - Não coloque `JWT_SECRET`, `DATABASE_URL`, `METRICS_TOKEN` nem
     `GOOGLE_CLIENT_SECRET` na Vercel. Só `NEXT_PUBLIC_*` chega ao browser.
5. Deploy e confirme:
   - `curl -I https://<web>/<code>` retorna `302` com `Location` da URL original
     (rewrite externo do link curto).
   - `curl -I https://<web>/api/v1/health`/`/health/ready` chega ao Render.
   - Login grava cookies `__Host-tl_access`/`__Secure-tl_refresh` no domínio do web.
   - `curl -sI https://<web>/en | grep -i content-security-policy` mostra nonce e
     nenhum `unsafe-inline`/`unsafe-eval` em `script-src`.
6. **Se um link curto der 404 na Vercel:** confirme que `API_INTERNAL_URL` está definido
   no ambiente de Production **e** Preview, que o build mais recente foi feito após a
   variável, e que o path não começa com `/api`, `/_next` ou um locale. O rewrite é
   `afterFiles`; não crie um arquivo `app/[code]/page.tsx` que capture o código.
   O comportamento foi validado localmente com `next build` + `next start`; a
   confirmação final é o `curl` acima no deployment real.
7. Domínio custom: aponte `www`/apex na Vercel e atualize `FRONTEND_ORIGIN`,
   `SHORT_BASE_URL`, `NEXT_PUBLIC_SITE_URL` e `GOOGLE_REDIRECT_URI` no Render.

## 5. GitHub Actions — deploy

`.github/workflows/deploy.yml` roda em **manual** (`workflow_dispatch`, escolha
`all`/`api`/`web`) ou em tag `v*`.

Secrets/variables necessárias no repositório (Settings → Secrets and variables →
Actions):

| Nome | Uso |
|---|---|
| `RENDER_DEPLOY_HOOK` | URL do deploy hook do serviço `tricolink-api` |
| `VERCEL_DEPLOY_HOOK` | URL do deploy hook do projeto web |
| `PRODUCTION_API_URL` | `https://tricolink-api.onrender.com` |
| `PRODUCTION_WEB_URL` | `https://<web>.vercel.app` |

O workflow dispara o hook e aguarda `GET /health/ready` (API) e `GET /en` (web) por até
10 minutos. O Render roda `alembic upgrade head` no pre-deploy; a Vercel builda o Next.

Para um deploy de tag:

```bash
git tag v1.0.0
git push origin v1.0.0
```

## 6. Observabilidade

- **Produção:** o Render expõe logs; `SENTRY_DSN` ativa o SDK com
  `send_default_pii=False` e scrub de headers/cookies/body. `/metrics` exige
  `Authorization: Bearer $METRICS_TOKEN`; não exponha o token no browser.
- **Local (perfil opcional):**

  ```bash
  make observability-up
  # Grafana: http://localhost:3002 (admin / GRAFANA_ADMIN_PASSWORD)
  # Prometheus: http://localhost:9090
  ```

  O target `make observability-up` copia o `METRICS_TOKEN` do container da API para
  `.secrets/metrics_token` (ignorado pelo git) e sobe Prometheus + Grafana com o
  dashboard `Tricolink` (RPS, latência p50/p95, 429 por bucket, cache hit ratio,
  circuit breaker e taxa de 5xx).

## 7. Limpeza e retenção

- Cron diário `python -m tricolink.jobs.cleanup` no Render (ou manual):
  `docker compose run --rm api python -m tricolink.jobs.cleanup`.
- Apaga `click_events` com `clicked_at < now() - CLICK_RETENTION_DAYS` (padrão 365)
  em lotes de `CLEANUP_BATCH_SIZE`, depois links com `expires_at < now()`.
- Idempotente: uma segunda execução retorna 0/0. Coberto por
  `tests/integration/test_cleanup.py`.
- O job precisa de `MIGRATION_DATABASE_URL` (admin) porque RLS bloqueia `DELETE`
  em `links` para o role de runtime sem contexto.

## 8. Checklist de verificação pós-deploy

- [ ] `GET https://<api>/health/live` e `/health/ready` → 200.
- [ ] `GET https://<api>/docs` e `/openapi.json` → 404.
- [ ] `GET https://<api>/metrics` sem token → 401; com token → 200.
- [ ] `GET https://<web>/<code>` → 302 para a URL original (link curto).
- [ ] Cadastro/login → cookies `__Host-`/`__Secure-` + `Secure` + `HttpOnly`.
- [ ] `/links` lista/edita/exclui; estatísticas atualizam após clique.
- [ ] Troca de idioma (incluindo `ar`) muda direção/conteúdo e mantém a política.
- [ ] Headers: HSTS, nosniff, COOP, Permissions-Policy e CSP com nonce.
- [ ] Cron executa e loga `cleanup_finished`; uma segunda execução zera contadores.
- [ ] `TRUSTED_PROXY_COUNT` confere o IP real no log de rate limit.
- [ ] Sentry recebe um erro de teste (se configurado) sem headers/cookies.

## 9. Limitações e custos

- O plano **free** do Render hiberna o web service após inatividade; o primeiro
  request após hibernar pode levar dezenas de segundos. Para produção, use um plano
  pago e `minInstances: 1`.
- O Postgres free do Render tem limites de retenção/armazenamento; para dados reais,
  use um plano pago e backups.
- A Vercel Hobby tem limites de build/banda; o rewrite externo consome função de
  borda. Para tráfego real, revise o plano.
- O `render.yaml` usa `autoDeployTrigger: "off"`: o deploy é feito pelo workflow ou
  manualmente, para evitar deploy duplicado. Remova essa linha se quiser auto-deploy
  no push da branch principal.
- `TRUSTED_PROXY_COUNT=2` é uma hipótese para a cadeia Vercel→Render; confirme os
  headers reais. Se a API for chamada diretamente (sem Vercel), o valor deve ser 1.
- A primeira aplicação de `render_app_role.sql` é manual; o Blueprint não cria roles
  de banco além do usuário administrador do Postgres.
- O `preDeployCommand` usa `MIGRATION_DATABASE_URL` no ambiente do serviço da API.
  Isso é necessário para as migrations, mas significa que um comprometimento do
  processo da API também vê a URL administrativa. Se isso for inaceitável, mova as
  migrations para um Render Job/cron separado e remova a URL admin do serviço web.
- O deploy real não foi executado nesta máquina (sem credenciais); os passos acima
  são a documentação executável e o que foi validado localmente está no
  `docs/perf/RESULTS.md` e nos workflows.
