# PROGRESS.md

## Fases
- [x] P00 Bootstrap SDD + Graphify
- [x] P01 Monorepo, Docker e tooling
- [ ] P02 Backend: fundação + núcleo de segurança (token bucket, circuit breaker, bulkhead, middlewares)
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

## Validação P00
- Consultas de fumaça executadas no grafo final: fluxo de redirect; baldes de rate limit (`redirect`, `create`, `auth`, `global`, `stats/list`); rotas do frontend. Os nós e trechos retornados batem com `CONTEXT.md` e `SECURITY.md`.
- `graphify query` retorna um subgrafo (nós/arestas), não uma resposta em prosa; a interpretação foi conferida manualmente contra a spec.

## Validação P01
- `make up` saiu com código 0 e os quatro serviços ficaram `healthy` (`postgres`, `redis`, `api`, `web`).
- `GET http://localhost:8001/health/live` respondeu 200 com `{"status":"ok"}`; `http://localhost:3001` respondeu 200 com a página mínima.
- `make test-api` passou (1 teste), `make test-web` passou (1 teste), `make lint` saiu com 0, `make format` saiu com 0 e `make migrate` saiu com 0.
- Containers não-root: `postgres` uid 70, `redis` uid 999, `api` uid 999 (`app`), `web` uid 1000 (`node`).
- Imagens multi-stage de produção também foram construídas e testadas: API `runtime` (uid 999 `app`) e web `runner` (uid 1001 `nextjs`), ambas respondendo 200.

## Bloqueios
(nenhum)

## Não validado
- O custo de tokens do Graphify ficou registrado como 0 porque o subagente de extração não retornou `usage`; não é possível afirmar o custo real desta execução.
- O diagnóstico do Graphify apontou 1 par de arestas colapsado no grafo não direcionado (`Single-Flight Lock` ↔ `Bulkhead Semaphores`, relações `references` e `semantically_similar_to`). Não é corrupção do grafo; as duas relações existem na extração bruta.
- `make logs` não foi executado porque usa `docker compose logs -f` e bloqueia; `docker compose logs` sem `-f` foi inspecionado para api/web.
- Ainda não existe migração Alembic real: `make migrate` validou conexão e `upgrade head` com zero revisions. O schema começa em P02/P03.
- A validação de containers foi feita no Docker Desktop/Windows. Não foi executada em Linux, macOS ou CI.
- O teste da API emite um aviso de depreciação do Starlette sobre `httpx` no `TestClient`; o teste passa e o aviso não quebra o build.

## Revisão humana pendente
- Traduções geradas por IA (todos os idiomas exceto pt-BR e en)
