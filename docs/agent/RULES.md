# RULES.md — Regras de trabalho dos agentes

## Fluxo
1. Leia `AGENTS.md` → RULES → PROGRESS → CONTEXT (seções da fase) → `GRAPH_REPORT.md`.
2. Execute **uma fase por vez**, na ordem de `PROGRESS.md`. Não adiante fases nem faça "extras".
3. **TDD:** escreva o teste que falha, implemente, refatore. Cada fase termina com testes passando.
4. Commits pequenos e semânticos (`feat(links): ...`, `fix(auth): ...`, `test: ...`), **sem push**.
5. Ao terminar: rode lint + tipos + testes, atualize `PROGRESS.md`, rode o graphify de novo (`docs/agent/GRAPHIFY.md`).

## Código
- Clean Architecture por módulo; dependências apontam para dentro (domain não importa framework).
- SOLID, funções curtas, nomes em inglês, tipagem estrita (mypy strict / TS strict), sem `any`.
- SQL só via SQLAlchemy com parâmetros. **Proibido** concatenar/formatar string em SQL.
- Segredos: apenas `os.getenv()` em `core/config.py` (API) e `process.env` no servidor Next. Nunca `NEXT_PUBLIC_` para segredo. Nunca commitar `.env`.
- Frontend: proibido `dangerouslySetInnerHTML`, `eval`, `new Function`; tokens nunca em localStorage/sessionStorage.
- Todo endpoint novo: schema Pydantic de entrada/saída com limites de tamanho, rate limit (token bucket), autorização explícita e teste de acesso negado.
- Mensagens ao usuário sempre via i18n (nada de string fixa na UI).
- Acessibilidade (POUR): foco visível, labels, contraste AA, navegação por teclado, `aria-*` corretos, respeitar `prefers-reduced-motion`.

## Honestidade nos relatos (importante)
- Só marque algo como validado se **você realmente executou**. Se Docker, banco ou rede não estiverem disponíveis, escreva em `PROGRESS.md > Não validado` exatamente o que ficou sem verificação.
- Não invente resultados de teste, cobertura ou benchmark.

## Proibido
- Comandos destrutivos fora do projeto; `git push`; `git reset --hard` sem pedido explícito.
- Adicionar dependências sem necessidade (justifique em `PROGRESS.md > Decisões`).
- Alterar a stack, o modelo de dados ou a API sem atualizar `CONTEXT.md` na mesma mudança.
