# PROGRESS.md

## Fases
- [x] P00 Bootstrap SDD + Graphify
- [x] P01 Monorepo, Docker e tooling
- [x] P02 Backend: fundação + núcleo de segurança (token bucket, circuit breaker, bulkhead, middlewares)
- [x] P03 Links: encurtar, redirecionar, cache anti-stampede, cliques
- [ ] P04 Identity: cadastro/login, Google OIDC, sessões, anti brute force
- [ ] P05 Frontend: fundação, next-intl (11 idiomas), navbar, API client, CSP
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
- RLS em `links`/`refresh_tokens` (SECURITY §3) não foi criada em P02; fica para as fases de identidade/hardening.
- Não foram executados k6/carga, `pip-audit`, deploy real em Render/Vercel nem teste em Linux/macOS.
- No Compose o usuário do Postgres é superuser do container. Não foi validado em Postgres gerenciado se o usuário de migração tem permissão para `CREATE EXTENSION citext`; o plano é rodar migrations com um usuário/procedimento privilegiado separado do runtime.
- Cliques são at-least-once: se o processo cair entre o commit do lote e o `XACK`, os eventos pendentes podem ser reprocessados e duplicar linhas em `click_events` (não há chave de idempotência). O `click_count` também pode duplicar nesse cenário.
- O flusher usa consumer name derivado do hostname; entradas pendentes de um consumer morto com hostname diferente não são reclamadas automaticamente (não foi implementado `XAUTOCLAIM`).
- Existe uma janela de corrida entre um refresh SWR em andamento e um PATCH/DELETE: o refresh pode repopular o cache com dados lidos antes da alteração. A invalidação sequencial é coberta por teste; a corrida concorrente fica para o hardening (P09).
- A política de URL resolve DNS no momento da criação, mas não fixa/pinna os IPs depois; como o servidor nunca busca a URL, o risco de SSRF em runtime é nulo, mas a checagem não protege contra mudanças posteriores de DNS.
- Não foram executados k6/carga, `pip-audit`, deploy real em Render/Vercel nem teste em Linux/macOS.

## Revisão humana pendente
- Traduções geradas por IA (todos os idiomas exceto pt-BR e en)
