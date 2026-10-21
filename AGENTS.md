# AGENTS.md — Tricolink

Você é um agente de engenharia trabalhando no **Tricolink** (encurtador de URL, projeto de portfólio).

## Ordem de leitura obrigatória (toda sessão)
1. `docs/agent/RULES.md` — regras de trabalho (inegociáveis)
2. `docs/agent/PROGRESS.md` — onde o projeto está; atualize ao terminar
3. `docs/agent/CONTEXT.md` — fonte única da verdade (produto, stack, dados, API, rotas)
4. `docs/agent/SECURITY.md` e `docs/agent/UI_SPEC.md` — quando a fase tocar segurança ou interface
5. `graphify-out/GRAPH_REPORT.md` — mapa do código (veja `docs/agent/GRAPHIFY.md`)

Nunca implemente algo que contradiga o CONTEXT.md. Se a spec estiver errada ou ambígua, registre em
`PROGRESS.md > Bloqueios` e siga com a opção mais segura e simples.
