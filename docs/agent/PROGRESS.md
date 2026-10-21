# PROGRESS.md

## Fases
- [x] P00 Bootstrap SDD + Graphify
- [x] P01 Monorepo, Docker e tooling
- [x] P02 Backend: fundação + núcleo de segurança (token bucket, circuit breaker, bulkhead, middlewares)
- [x] P03 Links: encurtar, redirecionar, cache anti-stampede, cliques
- [x] P04 Identity: cadastro/login, Google OIDC, sessões, anti brute force
- [x] P05 Frontend: fundação, next-intl (11 idiomas), navbar, API client, CSP
- [ ] P06 Landing page (hero, demo, recursos, FAQ, SEO/AEO/GEO)
- [ ] P07 Login, Account e Links (lista com código gerado)
- [ ] P08 Estatísticas (backend + página de detalhe)
- [ ] P09 Hardening de segurança + auditoria
- [ ] P10 Testes E2E/carga, CI/CD e deploy
- [ ] P11 README final e documentação

## Decisões
- Graphify 0.9.91 já estava instalado via `uv tool`; usei a integração nativa do Kilo (`graphify kilo install`) em vez de `graphify opencode install`, porque este é o agente atual. Isso instalou skill/command globais e registrou `.kilo/plugins/graphify.js` + seção always-on em `AGENTS.md`, sem alterar a ordem de leitura original.
- A extração semântica dos 8 documentos foi feita por um subagente de extração do Graphify (o backend Gemini não tinha o SDK `openai`/`google-genai` no ambiente isolado do `uv tool`). O cache semântico ficou em `graphify-out/cache/`, ignorado pelo git.
- Grafo P00 gerado e versionado em `graphify-out/` (`GRAPH_REPORT.md`, `graph.json`, `graph.html`).
- P01 usa Python preso a 3.11 (`>=3.11,<3.12`) e Poetry 2.4.1; `poetry.lock` e `pnpm-lock.yaml` foram commitados.
- Frontend: Next.js 16.4.2, React 19.3.1, Tailwind 4.3.3, TypeScript 5.9.3, pnpm 12.8.1 e Vitest 5.0.5. ESLint ficou em 9.39.5 porque os plugins do `eslint-config-next` ainda não declaram suporte ao ESLint 10.
- shadcn/ui inicializado com o preset `base-nova`, tema neutro. Isso adicionou `@base-ui/react`, `shadcn` (também usado por `shadcn/tailwind.css`), `tw-animate-css`, `class-variance-authority`, `clsx` e `tailwind-merge` às dependências do web.
- O `.env` local usa `API_PORT=8001` e `WEB_PORT=3001` porque as portas 8000/3000 já estão ocupadas por outros projetos nesta máquina. O `.env.example` mantém 8000/3000 como padrão do projeto; a alteração é só local e não versionada.
- GNU Make 4.4.1 foi instalado via winget para executar e validar os alvos do `Makefile`.
- Os alvos `make` rodam lint/testes dentro dos containers de desenvolvimento, garantindo as mesmas versões do runtime. `postgres` e `redis` também foram fixados com `user:` não-root no Compose.
- P02: `Settings` é um dataclass congelado; `Settings.from_env()` é o único leitor de ambiente (via `_env()` em `core/config.py`), cacheado com `lru_cache`. Em `production`, segredos ausentes/curtos/placeholder e `COOKIE_SECURE=false` derrubam a inicialização. `/docs` e `/openapi.json` só existem fora de produção.
- P02: logging com structlog (JSON em produção, console em dev) e `request_id` em contextvars. O log de acesso grava só método, rota-template, status e duração; query string, corpo e headers não são logados.
- P02: SQLAlchemy 2 assíncrono com pool (`DB_POOL_SIZE`/`DB_MAX_OVERFLOW`), `pool_pre_ping`, timeouts do asyncpg e `statement_timeout`. `Database.unit_of_work()` aplica o bulkhead de escrita e faz commit/rollback.
- P02: a migração inicial `0001_initial_schema` cria `citext`, as quatro tabelas do CONTEXT §4, CHECKs, FKs, UNIQUEs e índices (incluindo `(user_id, created_at DESC)` e o índice parcial de `expires_at`). Os nomes dos CHECKs usam o sufixo sem `ck_` no código da migração porque a naming convention do SQLAlchemy já prefixa com `ck_<tabela>_`.
- P02: token bucket usa um único script Lua com `TIME` do Redis (refill + consume atômicos). O TTL da chave é 2x o tempo de recarga. Redis indisponível/estourado/circuito aberto → token bucket em memória por processo, com `asyncio.Lock`; a degradação continua limitando (nunca libera geral).
- P02: o circuit breaker tem estados closed/open/half_open, clock injetável e limite de sondas no half-open. Um sucesso tardio de chamada iniciada antes da abertura não fecha o circuito. Bulkheads nomeados: `db_read`, `db_write`, `hashing`, `dns`.
- P02: ordem dos middlewares (externo → interno): request-id, headers de segurança, métricas/acesso, IP real, timeout, balde global, limite de corpo, FastAPI. O timeout cobre também a leitura do corpo e a checagem global. O limite de corpo rejeita `Content-Length` acima do teto antes de ler e bufferiza corpos chunked até o teto.
- P02: IP real conta o `X-Forwarded-For` da direita para a esquerda (`parts[-TRUSTED_PROXY_COUNT]`), então entradas forjadas à esquerda não criam novos baldes. `TRUSTED_PROXY_COUNT=0` ignora o header. O balde `global` usa a chave fixa `all` (load shedding do processo inteiro), enquanto os baldes por IP (redirect/create/auth) usarão o IP resolvido.
- P02: `/metrics` exige `Authorization: Bearer <METRICS_TOKEN>` (comparação em tempo constante) e responde 401 sem token. Métricas: requisições, latência, 429, estado/transições de circuit breaker e cache hit/miss. `/health/ready` checa Postgres e Redis, ambos com timeout e circuit breaker.
- P02: `docker-compose`/Dockerfile de dev passam `--limit-concurrency 200` ao uvicorn. Nenhuma dependência nova foi adicionada.
- P03: `modules/links` e `modules/analytics` seguem domain/application/adapters/presentation. `application/ports.py` não importa FastAPI/SQLAlchemy; os adapters SQLAlchemy/Redis implementam os ports. `RecordClick` fica em `links/application` e usa o domínio de analytics.
- P03: `UrlPolicy` resolve DNS via `HostResolver` injetado; `SystemHostResolver` roda sob o bulkhead `dns`, com timeout, e o policy bloqueia se **qualquer** resposta não for global. Bloqueia localhost/hosts internos, IPs privados/loopback/link-local/metadata/multicast/reservados/CGNAT, IPv4 mapeado em IPv6, credenciais, esquemas != http/https, controles/whitespace, `%0d`/`%5c` e URLs do próprio domínio (inclui subdomínios). IDN é normalizado para punycode.
- P03: o cache do redirect usa `tl:link:{code}`, `tl:lock:{code}`, `tl:neg:{code}`. O JSON guarda `{id,u,e,s,sf}`: `sf` é o "fresh until" com jitter, necessário para SWR determinístico (o hard TTL é o TTL da chave Redis). TTLs duro, macio e negativo recebem jitter de ±15%.
- P03: anti-stampede combina single-flight **em processo** (uma task por código atende todas as requisições concorrentes) com `SET NX PX` no Redis para coordenação entre processos, além de SWR e cache negativo. Isso evita saturar o pool Redis antes do single-flight.
- P03: PATCH/DELETE (e criação de alias) invalidam `tl:link` + `tl:neg`; expiração/inatividade são checadas a cada redirect mesmo com cache. Redis indisponível/estourado/circuito aberto → `CacheUnavailable` → repositório via bulkhead `db_read`.
- P03: cotas diárias usam Redis (`INCR` + expiração até a meia-noite UTC) com fallback em memória; a chave é hash SHA-256 de escopo+IP/user, para não persistir IP em claro. `ANON_LINK_TTL_DAYS` define a expiração do link anônimo.
- P03: cliques vão para o Redis Stream `tl:clicks` via XADD; `RecordClick` agenda a publicação e nunca bloqueia o redirect. Falha de Redis incrementa `tricolink_clicks_dropped_total{reason="redis_unavailable"}`. O flusher usa consumer group, grava `click_events` em lote e incrementa `links.click_count` no mesmo commit; eventos de links deletados são descartados.
- P03: UA bruto e IP nunca são persistidos. O evento guarda apenas device/browser leve, país normalizado de `X-Vercel-IP-Country`/`CF-IPCountry` e `referrer_host` (sem path/query). Cliques são at-least-once.
- P03: `create_app()` passou a devolver a instância FastAPI (middlewares via `add_middleware`), permitindo `dependency_overrides` nos testes de autenticação enquanto P04 não existe. `get_current_user_optional` é o ponto de extensão e retorna `None` por padrão.
- P03: repositório usa somente ORM/Core com parâmetros ligados, keyset pagination por `(created_at, id)`, busca `ILIKE` com `%`/`_` escapados, cursor base64 estrito e filtro de dono no SQL (não-dono → 404). Não há relationships/selects extras (sem N+1).
- P03: `Database.read()` aplica bulkhead `db_read` + circuit breaker; `unit_of_work()` aplica `db_write` + breaker. O publicador, cache, quota e flusher usam o breaker Redis; `CacheClient` genérico também passou a aceitar breaker/timeout.
- P03: redirect responde 302 com `Cache-Control: no-store` e `X-Robots-Tag: noindex, nofollow`; 404/410 usam HTML estático sem interpolação; rotas de gestão exigem usuário e as de listagem/detalhe usam o balde `stats_list` por usuário.
- P04: `identity` também segue domain/application/adapters/presentation. O domínio tem `Email` (NFKC + lowercase + email-validator), `PasswordPolicy` (10–128, lista de senhas comuns, sem controles), `User`, `TokenFamily`/`RefreshTokenRecord` e validação pura de claims Google.
- P04: registro responde **202 genérico** (`{"status":"registered"}`) e nunca cria sessão; e-mail duplicado executa o mesmo hash e devolve a mesma resposta, reduzindo enumeração. O login responde sempre `invalid_credentials` para e-mail inexistente/senha errada/inativo.
- P04: Argon2id com parâmetros OWASP (time 3, 64 MiB, parallelismo 4) executado em threadpool sob o bulkhead `hashing`. O hash dummy é pré-aquecido no lifespan para equalizar o primeiro login inexistente.
- P04: access JWT HS256 com apenas `sub`, `jti`, `iat`, `exp`; refresh token opaco com 48 bytes aleatórios e somente SHA-256 no banco. Rotação usa `SELECT ... FOR UPDATE`; token revogado reutilizado revoga a família inteira.
- P04: cookies `httpOnly` para access/refresh, `SameSite=Lax`, `Secure` quando `COOKIE_SECURE`; `__Host-` em access/CSRF/OAuth e `__Secure-` no refresh (path `/api/v1/auth`). Tokens não aparecem no corpo das respostas.
- P04: CSRF double-submit e checagem de `Origin` (frontend/API) ou `Sec-Fetch-Site` em mutações autenticadas; login/registro validam Origin quando presente. `GET /auth/csrf` define/retorna o token.
- P04: Google OIDC via Authlib com endpoints explícitos (sem discovery no authorize), `state` + `nonce` + PKCE S256, validação explícita de `iss`, `aud`, `exp`, `nonce` e `email_verified`, vínculo por `google_sub`/e-mail verificado e redirect para `FRONTEND_ORIGIN` com `next` estritamente interno.
- P04: anti brute force combina token buckets `auth` por IP e e-mail normalizado (chaves hash) com contadores de falha/lockout no Redis e fallback em memória; mensagens não revelam existência de conta. `AUTH_LOCKOUT_THRESHOLD` e `AUTH_LOCKOUT_SECONDS` controlam o lockout.
- P04: RLS com `FORCE` em `links` e `refresh_tokens`. Contexto por transação via `set_config(..., true)` (equivalente a `SET LOCAL`, mas parametrizável): `app.current_user_id`, `app.current_link_code`, `app.refresh_token_hash`, `app.refresh_family_id`, `app.click_flusher`. A leitura pública só enxerga o código exato solicitado; leituras de dono listam apenas o próprio usuário; o flusher vê/atualiza click_count. O INSERT anônimo é permitido e o RETURNING usa o contexto do código.
- P04: o Compose agora usa `tricolink_app` (não-superuser, sem BYPASSRLS) em `DATABASE_URL`; migrations usam `MIGRATION_DATABASE_URL`. O role é criado pelo init do Postgres e pelo alvo idempotente `make db-role`, que também cobre volumes antigos.
- P04: `get_current_user_optional` foi substituído pela implementação real (JWT em cookie + consulta do usuário); `get_current_user` continua obrigatório. As rotas de links agora aplicam CSRF quando há cookies de sessão, dono e cotas de usuário logado.
- P05: no Next 16 o arquivo `middleware` foi renomeado para `proxy`; a composição next-intl + CSP vive em `src/proxy.ts`. O `matcher` está limitado a `/` e `/(pt-BR|en|es|fr|de|it|ja|ko|zh-CN|ru|ar)/:path*`, como pedido.
- P05: o rewrite de `/:code` exigido no CONTEXT §7 também está em `rewrites().fallback`, mas um rewrite `afterFiles` com o mesmo destino foi adicionado para códigos válidos: a rota dinâmica `app/[locale]` captura qualquer segmento único (inclusive `/abc1234`) antes do `fallback`, então sem esse rewrite os links curtos nunca chegariam à API. O `afterFiles` exclui locales e rotas reservadas; o `fallback` permanece como defesa extra.
- P05: CSP é gerada por requisição no proxy com nonce em `script-src`/`style-src` e `strict-dynamic`; o tema inicial é aplicado por um script inline com o mesmo nonce, evitando flash. `next.config` aplica os demais headers (HSTS só em produção, nosniff, Referrer-Policy, COOP, XFO, Permissions-Policy).
- P05: `src/lib/api.ts` usa caminhos same-origin (`/api/v1`), `credentials: "include"`, CSRF double-submit lido dos cookies `__Host-tl_csrf`/`tl_csrf` (ou `/auth/csrf` quando ausente), erro padronizado `{error:{code,message}}`, `Retry-After` em 429 e **um** refresh em 401. Tokens nunca são expostos ao JS nem guardados em storage.
- P05: `useAuthStore` carrega o usuário por `GET /auth/me` uma única vez por sessão e mapeia o DTO para camelCase; logout limpa o estado mesmo se a API falhar. Nenhum token no store.
- P05: `rewrites` do Next são resolvidos no build. O Dockerfile do web agora recebe `API_INTERNAL_URL`/`NEXT_PUBLIC_SITE_URL` como `ARG` no builder; deploy precisa definir esses valores no build (Vercel/Render) ou reconstruir a imagem.
- P05: foram adicionadas dependências de teste (`@testing-library/react`, `@testing-library/user-event`, `@testing-library/jest-dom`, `jsdom`, `@playwright/test`). O `i18n:check` importa `src/i18n/locales.ts` via type stripping do Node 22; por isso o script usa `--disable-warning=MODULE_TYPELESS_PACKAGE_JSON`.
- P05: o seletor de idiomas usa um listbox próprio (teclado, foco, `aria-selected`, nomes nativos) e preserva o pathname via `createNavigation`. O menu mobile usa `<dialog>` nativo com `showModal`, bloqueio de scroll do body e as mesmas ações do desktop.

## Validação P00
- Consultas de fumaça executadas no grafo final: fluxo de redirect; baldes de rate limit (`redirect`, `create`, `auth`, `global`, `stats/list`); rotas do frontend. Os nós e trechos retornados batem com `CONTEXT.md` e `SECURITY.md`.
- `graphify query` retorna um subgrafo (nós/arestas), não uma resposta em prosa; a interpretação foi conferida manualmente contra a spec.

## Validação P01
- `make up` saiu com código 0 e os quatro serviços ficaram `healthy` (`postgres`, `redis`, `api`, `web`).
- `GET http://localhost:8001/health/live` respondeu 200 com `{"status":"ok"}`; `http://localhost:3001` respondeu 200 com a página mínima.
- `make test-api` passou (1 teste), `make test-web` passou (1 teste), `make lint` saiu com 0, `make format` saiu com 0 e `make migrate` saiu com 0.
- Containers não-root: `postgres` uid 70, `redis` uid 999, `api` uid 999 (`app`), `web` uid 1000 (`node`).
- Imagens multi-stage de produção também foram construídas e testadas: API `runtime` (uid 999 `app`) e web `runner` (uid 1001 `nextjs`), ambas respondendo 200.

## Validação P02
- Migração do zero validada em banco descartável `tricolink_migration_test`: `alembic upgrade head`, `alembic downgrade base` e `alembic upgrade head` de novo. Conferido no Postgres: extensão `citext`, tabelas `users`, `refresh_tokens`, `links`, `click_events`, CHECKs (`ck_links_code_format`, `ck_click_events_device_allowed` etc.), índices `ix_links_user_id_created_at` com `created_at DESC` e `ix_links_expires_at` parcial. O banco descartável foi removido e `make migrate` aplicou a revisão no banco de dev.
- `make test-api`: 62 testes passando (unit, security e integration no Compose).
- `pytest --cov=tricolink.infra --cov-report=term-missing`: 92% de cobertura em `infra/` (587 stmts, 32 miss, 96 branches). Todos os módulos de infra ficaram ≥83%; a média passa do alvo de 85%.
- `alembic check` contra o banco migrado: nenhuma operação de upgrade pendente (modelos em `infra/db/models.py` e migração alinhados, incluindo tipos e índices).
- `make lint`: `ruff check`, `ruff format --check`, `mypy src` e o lint/typecheck do web passaram.
- `make up`: postgres, redis, api e web saudáveis. `GET /health/live` e `/health/ready` → 200 (`postgres: ok`, `redis: ok`), `/metrics` sem token → 401 e com token → 200, web → 200.
- Configuração de produção exercitada via `TestClient`: `/docs` e `/openapi.json` → 404.
- Logs do container mostram `request_id` nas linhas de acesso, sem query string/corpo.
- Token bucket: 100 chamadas paralelas no Redis respeitaram a capacidade; consume/esgota/recarga e fallback com Redis derrubado cobertos. Circuit breaker: transições closed → open → half_open → closed/open. Bulkhead: concorrência limitada e timeout.
- IP real: testes provam que `X-Forwarded-For` forjado à esquerda não burla o limite com `TRUSTED_PROXY_COUNT=1`; corpo chunked/acima do limite → 413.

## Validação P03
- `make test-api`: 249 testes passando (domain, application, cache, repositório, pipeline de cliques, API e segurança).
- Cobertura de `modules/links/domain`: 96% (226 stmts, 8 miss; 82 branches, 4 partial). Todos os arquivos de domínio ≥94%.
- `ruff check`, `ruff format --check` e `mypy src` limpos.
- `alembic check`: nenhuma operação pendente (P03 não alterou schema).
- Stampede HTTP: 200 GETs concorrentes no mesmo código frio → 1 consulta ao repositório e 200 respostas 302 com `Location` correto.
- Cache: 200 chamadas concorrentes → 1 loader; SWR serve stale e executa 1 refresh; 1000 códigos inexistentes → 1 loader; jitter de 2000 TTLs sempre dentro de 85–115 para base 100 ±15%; invalidação força nova leitura.
- Redirect: validado ao vivo com `curl.exe`: `HTTP/1.1 302 Found`, `location: https://93.184.216.34/p03`, `x-robots-tag`, `cache-control: no-store` e headers `RateLimit-*`.
- Clique: após o redirect, o flusher gravou `click_events` e `links.click_count=1`; evento `BR|mobile|safari|news.example.com`, sem IP/UA bruto.
- Colisão real: IntegrityError de UNIQUE(code) forçado no Postgres → retry gerou outro código.
- SQLi: payloads em `code`, `alias`, `q` e `cursor` não alteraram consultas (404/400/422/lista vazia conforme o caso).
- Redis fora no publicador: redirect continuou 302 e `clicks_dropped_total` incrementou; publisher bloqueante não impediu a resposta.
- Rate limits: redirect acima da capacidade → 429 com `Retry-After` e `RateLimit-Limit`; baldes de create cobrem IP e usuário.

## Validação P04
- `make test-api`: **325 testes passando** (identidade, Google mockado, cookies/CSRF, IDOR, RLS e regressões P02/P03).
- Cobertura de `modules/identity/domain` + `modules/identity/application`: **96%** (550 stmts, 17 miss; 108 branches, 12 partial).
- `ruff check`, `ruff format --check` e `mypy src` limpos.
- Migrations do zero em banco descartável: `0001` → `0002`, `downgrade base` e `upgrade head` novamente. O banco descartável também validou o init do role + default privileges + app role não-superuser inserindo/anonimamente lendo link com RLS.
- RLS testado com role de runtime `tricolink_app` (`rolsuper=false`, `rolbypassrls=false`): sem contexto não lê links/tokens; contexto do usuário A enxerga só A; contexto de código enxerga só aquele código; mutação cruzada retorna 0 linhas. O teste remove deliberadamente o filtro de aplicação.
- Fluxo manual ao vivo (Docker, porta 8001): register `202` → login `200` → `/auth/me` `200` → criar link logado `201` → listar `200` → refresh `200` → logout `204` → `/auth/me` `401`.
- Reuso de refresh revoga a família; somente SHA-256 do refresh fica no banco; 20 tentativas de login produzem 429; lockout progressivo com threshold baixo também produz 429; cookie access/refresh é `HttpOnly` e CSRF não é.
- Google com IdP mockado: URL contém `state`, `nonce`, `code_challenge` e `code_challenge_method=S256`; `state` inválido e nonce errado são rejeitados; `next=//evil.com` e `next=https://evil.com` retornam 400; callback válido cria/víncula usuário e redireciona para o frontend.
- `make up` saudável com o novo role; `make migrate` e `alembic check` sem operações pendentes.

## Validação P05
- `pnpm build` (Next 16.4.2, Turbopack) concluiu com sucesso; rotas geradas: `/[locale]` dinâmica, `/icon.svg`, `/robots.txt` e `/sitemap.xml`.
- `pnpm lint` (ESLint 9) e `pnpm typecheck` (`next typegen && tsc --noEmit`) limpos.
- `pnpm test`: **36 testes Vitest passando** em 9 arquivos (navbar en/ar RTL, troca de locale preservando rota, API client com CSRF/401/429, auth store, CSP, rewrites, URLs externas e `i18n:check`).
- `pnpm i18n:check`: **11 locales, 96 chaves**, sem chave faltando/sobrando, valores vazios ou placeholders divergentes.
- `pnpm test:e2e`: **6 testes Playwright passando** contra build de produção: `/` detecta `pt-BR`/fallback `en`, troca pelos 11 idiomas, `/zzzzzz9` não entra no fluxo i18n, `/ar` com `dir="rtl"` + CSP sem violações no console, e menu mobile.
- Inspeção HTTP do build: `/` → `307 /pt-BR`; `/en` e `/ar` → `200` com CSP nonce, HSTS, nosniff, Referrer-Policy, COOP, XFO e Permissions-Policy; scripts do Next e o script de tema receberam o nonce.
- Lighthouse (produção, `/en`, mobile): **Accessibility 100** (era 96 antes dos ajustes de contraste do vermelho no tema escuro e do nome acessível do seletor de idiomas).
- `GET /robots.txt` bloqueia `/account`, `/links`, `/login`, `/api/` e os equivalentes por locale; `GET /sitemap.xml` lista os 11 idiomas.
- Rewrites exercitados ao vivo: `/api/v1/auth/me` foi encaminhado ao servidor configurado em `API_INTERNAL_URL` e `/zzzzzz9` foi encaminhado a `/api/v1/r/zzzzzz9` (404 da API, sem redirect de locale).

## Bloqueios
(nenhum)

## Não validado
- O custo de tokens do Graphify ficou registrado como 0 porque o subagente de extração não retornou `usage`; não é possível afirmar o custo real desta execução.
- O diagnóstico do Graphify apontou 1 par de arestas colapsado no grafo não direcionado (`Single-Flight Lock` ↔ `Bulkhead Semaphores`, relações `references` e `semantically_similar_to`). Não é corrupção do grafo; as duas relações existem na extração bruta.
- `make logs` não foi executado porque usa `docker compose logs -f` e bloqueia; `docker compose logs` sem `-f` foi inspecionado.
- A validação de containers foi feita no Docker Desktop/Windows. Não foi executada em Linux, macOS ou CI.
- O teste da API emite um aviso de depreciação do Starlette sobre `httpx` no `TestClient`; o teste passa e o aviso não quebra o build.
- Prometheus usa o registry padrão por processo: com os 2 workers do gunicorn em produção, cada scrape vê as métricas do worker que respondeu. Não foi implementado modo multiprocess do `prometheus_client`; fica para P10 (deploy/observabilidade).
- O pool Redis padrão é 50 conexões por worker. O teste de 100 chamadas concorrentes usou pool de 120; com o pool padrão, excesso de concorrência cai no fallback em memória (seguro, mas os contadores ficam por processo).
- RLS foi criada em P04 (`links`/`refresh_tokens`), mas a validação foi local. Em Postgres gerenciado é preciso confirmar que o role de runtime não é superuser nem tem `BYPASSRLS`; o role de migração também precisa poder criar `citext` e rodar futuras migrações de dados com contexto RLS.
- Não foram executados k6/carga, `pip-audit` nem teste em Linux/macOS; o deploy real em Render/Vercel também não foi executado.
- Cliques são at-least-once: se o processo cair entre o commit do lote e o `XACK`, os eventos pendentes podem ser reprocessados e duplicar linhas em `click_events` (não há chave de idempotência). O `click_count` também pode duplicar nesse cenário.
- O flusher usa consumer name derivado do hostname; entradas pendentes de um consumer morto com hostname diferente não são reclamadas automaticamente (não foi implementado `XAUTOCLAIM`).
- Existe uma janela de corrida entre um refresh SWR em andamento e um PATCH/DELETE: o refresh pode repopular o cache com dados lidos antes da alteração. A invalidação sequencial é coberta por teste; a corrida concorrente fica para o hardening (P09).
- A política de URL resolve DNS no momento da criação, mas não fixa/pinna os IPs depois; como o servidor nunca busca a URL, o risco de SSRF em runtime é nulo, mas a checagem não protege contra mudanças posteriores de DNS.
- Google OIDC **não foi validado contra o IdP real**: os testes usam Authlib para URL/estado/PKCE e um IdP mockado para o callback. As credenciais recebidas foram gravadas em `.env.render` (ignorado pelo Git, nunca commitado); o console Google precisa ter exatamente `https://tricolink-0gzp.onrender.com/api/v1/auth/google/callback` como redirect URI. Não houve navegador/fluxo real.
- As credenciais Render (Postgres/Redis) foram guardadas apenas em `.env.render`; não foram usadas nos testes para não tocar no ambiente de produção. SSL/TLS, permissões do role `trcl` e a extensão `citext` no Render não foram verificados.
- Em produção, o role de runtime deve ser não-superuser e sem `BYPASSRLS`; se `trcl` for owner/superuser, o `FORCE` não protege contra bypass. O status do role no Render não foi consultado.
- No Compose o container da API recebe `MIGRATION_DATABASE_URL` para o alvo `make migrate`. Em produção, o job de migração deve ser separado e o processo da API não deve receber essa URL privilegiada.
- Não há verificação de posse do e-mail no cadastro local. O vínculo automático de uma conta de senha existente a um e-mail verificado do Google (conforme pedido) pode permitir pré-hijacking se alguém registrar o e-mail de outra pessoa antes; uma fase futura deve adicionar verificação de e-mail ou exigir login antes de vincular.
- O access JWT não é revogado no logout; ele continua válido até `exp` (15 min). O refresh é revogado imediatamente.
- CSRF depende de o proxy do frontend encaminhar `Origin` ou `Sec-Fetch-Site`; se remover ambos, mutações autenticadas serão rejeitadas com 403. O frontend deve usar `/api/v1/auth/csrf` e os nomes `__Host-`/`__Secure-` em produção.
- P05 consumiu `/auth/me` no client (cookie + CSRF/refresh), mas o fluxo autenticado ponta a ponta **não foi validado contra a API real**: o build usado no Playwright resolveu `API_INTERNAL_URL` para o default `http://localhost:8000`, onde não estava a API do Tricolink, e `/api/v1/auth/me` respondeu 404. Os testes do client usam `fetch` mockado.
- O build de produção do web foi validado com `next build` + `next start` local. A imagem Docker `runner` (standalone) não foi reconstruída/revalidada em P05; o Playwright emite o aviso de que `next start` não é o modo standalone.
- Lighthouse de acessibilidade foi executado apenas em `/en`; não foi rodado nos 11 idiomas nem em desktop/mobile separadamente (o preset padrão do Lighthouse é mobile).
- O menu mobile e a troca de idioma foram validados em Chromium; não foram executados em Firefox/WebKit.
- Avisos de depreciação do `httpx` no `TestClient` e do Authlib para `httpx` permanecem; não quebram os testes.

## Revisão humana pendente
- Traduções geradas por IA: `es`, `fr`, `de`, `it`, `ja`, `ko`, `zh-CN`, `ru` e `ar` (pt-BR e en são as referências).
