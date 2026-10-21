# PROGRESS.md

## Fases
- [x] P00 Bootstrap SDD + Graphify
- [ ] P01 Monorepo, Docker e tooling
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

## Validação P00
- Consultas de fumaça executadas no grafo final: fluxo de redirect; baldes de rate limit (`redirect`, `create`, `auth`, `global`, `stats/list`); rotas do frontend. Os nós e trechos retornados batem com `CONTEXT.md` e `SECURITY.md`.
- `graphify query` retorna um subgrafo (nós/arestas), não uma resposta em prosa; a interpretação foi conferida manualmente contra a spec.

## Bloqueios
(nenhum)

## Não validado
- O custo de tokens do Graphify ficou registrado como 0 porque o subagente de extração não retornou `usage`; não é possível afirmar o custo real desta execução.
- O diagnóstico do Graphify apontou 1 par de arestas colapsado no grafo não direcionado (`Single-Flight Lock` ↔ `Bulkhead Semaphores`, relações `references` e `semantically_similar_to`). Não é corrupção do grafo; as duas relações existem na extração bruta.

## Revisão humana pendente
- Traduções geradas por IA (todos os idiomas exceto pt-BR e en)
