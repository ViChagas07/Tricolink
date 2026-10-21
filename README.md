# Tricolink
Encurtador de URL (projeto de portfólio). README completo é gerado na fase P11.
Veja `AGENTS.md` e `docs/agent/` para a especificação (SDD).

## Decisões técnicas
- Redirecionamento usa **302**, não 301: o navegador não guarda a resposta em cache e cada clique chega ao servidor para contabilização. A resposta leva `Cache-Control: no-store`.
- O cache de redirect (`tl:link:*`) combina TTL duro (Redis), TTL macio com jitter (SWR), single-flight em processo + `SET NX PX` no Redis e cache negativo (`tl:neg:*`). Redis indisponível cai para o Postgres via bulkhead `db_read`.
- Cliques são enviados de forma assíncrona ao Redis Stream `tl:clicks`; um flusher de consumer group grava em lote em `click_events` e incrementa `links.click_count`. O redirect nunca espera o INSERT.
- A API usa um role de runtime **não-superuser** (`tricolink_app`) para que o RLS seja aplicado. `make up` executa `make db-role` (idempotente) e as migrations usam `MIGRATION_DATABASE_URL` com o role privilegiado.
- Sessões usam access JWT de 15 min em cookie `httpOnly` + refresh opaco rotativo em cookie `httpOnly` com path `/api/v1/auth`. Access/CSRF usam prefixo `__Host-` em produção; o refresh usa `__Secure-` porque o path é restrito. Em desenvolvimento os cookies não têm `Secure`.
- CSRF é double-submit (`tl_csrf` + `X-CSRF-Token`) e também valida `Origin`/`Sec-Fetch-Site` em mutações autenticadas. `GET /api/v1/auth/csrf` disponibiliza o token para o frontend.
- RLS em `links` e `refresh_tokens` usa `set_config('app.*', ..., true)` por transação. O link público do redirect é lido apenas pelo código exato (`app.current_link_code`); o dono usa `app.current_user_id`; o flusher de cliques usa `app.click_flusher`.
- Auth usa e-mail + senha (Argon2id) e Google OIDC (Authlib). Access JWT e refresh opaco ficam em cookies `httpOnly`; mutações autenticadas exigem CSRF double-submit. Em produção, use `COOKIE_SECURE=true` e mantenha `GOOGLE_REDIRECT_URI` idêntico ao configurado no Google Cloud Console.
- Setup local: `cp .env.example .env`, `make up` (cria o role de runtime e sobe a stack) e `make migrate`. Credenciais de produção devem ficar em um env file ignorado (por exemplo `.env.render`) e nunca ser commitadas.
