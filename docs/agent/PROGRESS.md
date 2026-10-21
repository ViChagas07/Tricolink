# PROGRESS.md

## Fases
- [x] P00 Bootstrap SDD + Graphify
- [x] P01 Monorepo, Docker e tooling
- [x] P02 Backend: fundação + núcleo de segurança (token bucket, circuit breaker, bulkhead, middlewares)
- [ ] P03 Links: encurtar, redirecionar, cache anti-stampede, cliques
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

## Revisão humana pendente
- Traduções geradas por IA (todos os idiomas exceto pt-BR e en)
