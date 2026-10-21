# GRAPHIFY.md — Context Engineering com Graphify

O Graphify transforma o repositório (código + docs) em um grafo de conhecimento consultável, para o agente
navegar pela estrutura em vez de varrer arquivo por arquivo.

## Instalação (uma vez, na máquina)
```bash
pip install graphifyy          # (sim, com dois "y") — ou: uv tool install graphifyy / pipx install graphifyy
graphify install               # registra a skill /graphify no assistente
graphify opencode install      # escreve instruções always-on no AGENTS.md (OpenCode)
```
Se você usa outro agente: `graphify codex install`, `graphify cursor install`, etc.

## Uso
- No assistente: `/graphify .` mapeia o projeto e gera `graphify-out/` (`GRAPH_REPORT.md`, `graph.json`, ...).
- Leia **`graphify-out/GRAPH_REPORT.md`** antes de explorar arquivos.
- Consultas: `graphify query "como funciona o redirect?" --graph graphify-out/graph.json`
- Servidor para agentes com MCP: `python -m graphify.serve graphify-out/graph.json`

## Rotina por fase
1. Início: leia o GRAPH_REPORT e use `graphify query` antes de grepar.
2. Fim: rode `/graphify .` de novo e commite `graphify-out/` (menos `cache/`).
3. Se o grafo divergir da spec, a spec (`CONTEXT.md`) manda; corrija o código ou registre em `PROGRESS.md > Bloqueios`.
