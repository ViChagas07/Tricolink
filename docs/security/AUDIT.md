# Auditoria de segurança — P09

**Data:** 2026-10-22
**Escopo:** SECURITY.md §1–§10 contra o código real do monorepo, suíte ofensiva, headers/CSP do build de produção, segredos/bundle, supply chain, RLS e configuração de produção.
**Ambiente:** Windows 11 + Docker Desktop; API em container de desenvolvimento (FastAPI/Uvicorn, Python 3.11), Postgres 16 e Redis 7 em containers; web em build de produção (`next build` + `next start`, Next 16.4.2) na porta 3100; API real em 127.0.0.1:8001.
**Regra de severidade:** crítica/alta = exploração remota com impacto relevante sem pré-requisito incomum; média = impacto limitado ou pré-requisito; baixa/informativa = defesa em profundidade, configuração ou achado de scanner sem exploração prática demonstrada.

## Resumo executivo

| Severidade | Abertos | Corrigidos nesta fase |
|---|---:|---:|
| Crítica | 0 | 0 |
| Alta | 0 | 2 |
| Média | 0 | 3 |
| Baixa / informativa | 8 (aceitos ou residuais) | 3 |

**Resultado:** zero achados críticos ou altos em aberto. Riscos médios remanescentes são de produto/arquitetura (verificação de e-mail e revogação do access JWT no logout) e estão registrados abaixo com mitigações e recomendações.

### Achados corrigidos

| ID | Severidade | Achado | Correção | Evidência |
|---|---|---|---|---|
| F-01 | Alta | `GoogleOIDCClient.exchange` decodificava o `id_token` com `verify_signature: False` quando o `userinfo` vinha sem claims; um token não verificado poderia influenciar identidade/e-mail. | Removido o fallback; só claims validadas pelo Authlib (`userinfo`) são aceitas. | `apps/api/src/tricolink/modules/identity/adapters/google.py:59`; `tests/unit/test_identity_adapters.py::test_google_exchange_never_decodes_an_unverified_id_token` |
| F-02 | Alta | Pré-hijacking: login Google vinculava automaticamente um e-mail verificado a uma conta de senha já existente; quem registrou o e-mail antes mantinha a senha e o acesso. | Vínculo automático só é permitido para conta sem `password_hash`; conta com senha é rejeitada e exige fluxo explícito de vínculo. | `apps/api/src/tricolink/modules/identity/application/google_login.py:45`; `tests/unit/test_identity_application.py::test_google_login_creates_links_and_rejects_unverified` |
| F-03 | Média | Cache de estatísticas usava `tl:stats:{code}:{range}`; após excluir um link e outro usuário reutilizar o alias, estatísticas antigas podiam ser servidas por até 30 s (vazamento entre donos). | Chave passou a usar o `link_id` imutável (`tl:stats:{link_id}:{range}`) e o flusher invalida as três janelas ao persistir cliques. | `apps/api/src/tricolink/modules/analytics/adapters/stats_cache.py:24`; `apps/api/src/tricolink/modules/analytics/adapters/flusher.py:97`; `tests/security/test_cache_security.py::test_stats_cache_is_scoped_by_link_id_and_does_not_leak_after_code_reuse` |
| F-04 | Média | Corrida do SWR: um refresh iniciado antes de PATCH/DELETE podia repopular `tl:link:{code}` com a URL antiga depois da invalidação, mantendo um redirect revogado no cache. | Geração por código (`tl:link:gen:{code}`) incrementada atomicamente na invalidação; stores de link/negativo usam Lua condicional e são descartados se a geração mudou. | `apps/api/src/tricolink/modules/links/adapters/cache.py:30`, `:37`, `:191`, `:348`; `tests/integration/test_link_cache.py::test_invalidation_during_a_stale_refresh_cannot_repopulate_the_cache`; `tests/security/test_cache_security.py::test_invalidation_generation_blocks_a_stale_cache_refresh` |
| F-05 | Média | Flusher de cliques não recriava o consumer group após `FLUSHDB`/failover (`NOGROUP`): os cliques paravam de ser gravados até reiniciar o processo. Além disso, estatísticas em cache não eram invalidadas ao persistir um lote, exibindo 0 cliques por até 30 s. | `NOGROUP` reseta `_group_ready` e recria o grupo; `_invalidate_stats` apaga as chaves das três janelas após o commit do lote. | `apps/api/src/tricolink/modules/analytics/adapters/flusher.py:163`; `tests/integration/test_click_pipeline.py::test_flusher_recreates_the_group_after_the_stream_is_lost` e `::test_flusher_persists_batch_and_increments_click_count` |
| F-06 | Baixa | Caminhos sem locale (`/links`, `/login`, `/account`) e locales desconhecidos (`/xx/links`) podiam servir HTML sem CSP porque o matcher do proxy só cobria `/` e locales conhecidos. | Matcher inclui os prefixos reservados e qualquer locale de 2 letras; o next-intl redireciona para o locale conhecido, aplicando CSP no redirect e na página final. | `apps/web/src/proxy.ts:62`; `apps/web/e2e/security.spec.ts`; verificação manual `/links`/`/xx/links` → 307 com CSP |
| F-07 | Baixa | Páginas HTML de erro da API e respostas de `/auth/*`/`/metrics` não tinham CSP nem `Cache-Control: no-store` em produção. | CSP deny-by-default no middleware de produção e `no-store` para auth/métricas. | `apps/api/src/tricolink/core/middleware/security_headers.py:24`, `:29`; `tests/security/test_production_hardening.py` |
| F-08 | Baixa | `shadcn` estava em `dependencies` apesar de ser CLI/build-time (o `globals.css` importa `shadcn/tailwind.css`), arrastando `braces` (advisory de DoS por padrão profundamente aninhado, sem versão corrigida) para o escopo de produção. | Movido para `devDependencies`; o build (Docker/CI) instala dev deps, mas o runtime/produção não recebe o pacote. `pnpm audit --prod` ficou limpo. | `apps/web/package.json`; `pnpm audit --prod --audit-level high` |

### Achados residuais aceitos (com justificativa)

| ID | Severidade | Risco | Por que não foi corrigido agora | Recomendação |
|---|---|---|---|---|
| R-01 | Média | Não há verificação de posse do e-mail no cadastro. Um atacante pode registrar `vitima@exemplo.com` com senha; a vítima não consegue usar login Google nesse e-mail (o auto-vínculo foi bloqueado na F-02), mas o atacante continua com uma conta com o e-mail dela. | Exige infraestrutura de e-mail/verificação, fora do escopo P09. | Adicionar verificação de e-mail (token de uso único, expiração curta) e exigir vínculo explícito para contas existentes. |
| R-02 | Média | Logout revoga o refresh, mas o access JWT continua válido até `exp` (15 min). Um token roubado funciona por até 15 min após o logout. | Revogação por `jti` exige denylist/consulta por request no Redis; a arquitetura atual prioriza latência do caminho quente. | Considerar denylist de `jti` com TTL igual ao access TTL; até lá, manter access curto e cookies `HttpOnly`/`Secure`. |
| R-03 | Baixa | Se a invalidação de cache falhar durante uma indisponibilidade de Redis, um redirect pode continuar no cache até o TTL duro (24 h por padrão) e estatísticas até o TTL de 30 s. | A falha de Redis já é degradada com fallback; implementar versão no banco/read-through invalidation adicionaria acoplamento. | Encurtar `CACHE_HARD_TTL_SECONDS` em produção ou invalidar por `updated_at` em uma fila durável. |
| R-04 | Baixa | `click_events` não tem RLS (só `links`/`refresh_tokens`). O role de runtime poderia ler cliques de todos os links se houvesse SQL injection ou comprometimento do processo. | Não há SQL dinâmico nem injection conhecida; RLS em cliques exigiria join/contexto extra no caminho de estatísticas. | Avaliar RLS em `click_events` por `link_id` em uma migração futura. |
| R-05 | Baixa | `/health/ready` é isento do balde global e faz `SELECT 1` + ping Redis por chamada; um atacante pode amplificar carga no banco/Redis. | Health checks de plataforma precisam responder mesmo sob load shedding; o request timeout e os pools limitam o dano. | Adicionar cache curto (1–5 s) no readiness ou um balde por IP para o endpoint. |
| R-06 | Baixa | `TRUSTED_PROXY_COUNT` confia no `X-Forwarded-For` a partir da direita. Se a API for exposta diretamente, o header pode ser forjado para criar novos baldes. | É uma decisão de topologia; a aplicação não consegue distinguir um proxy confiável sem configuração de IPs. | Em produção, manter a API atrás de Cloudflare/WAF/proxy e definir `TRUSTED_PROXY_COUNT` exatamente; nunca expor a porta da API. |
| R-07 | Baixa | Páginas 404 arbitrárias (`/nonexistent`, `/*/links` em fuzzing) e assets inexistentes não recebem CSP, pois o proxy não as cobre. | São páginas estáticas de erro, sem interpolação de entrada; a aplicação real e os prefixos reservados têm CSP. | Se necessário, um `not-found` global com CSP estática sem scripts, ou um proxy catch-all cuidadoso. |
| R-08 | Baixa | `Cross-Origin-Embedder-Policy`/`Cross-Origin-Resource-Policy` não são enviados (ZAP WARN). | COEP `require-corp` exigiria CORP em todos os assets e pode quebrar imagens/fontes; não há recurso cross-origin na app. | Avaliar `COEP: credentialless` + `CORP: same-origin` após validar imagens OG/fontes. |
| R-09 | Informativo | Cliques são at-least-once: queda entre commit e `XACK` pode duplicar `click_events`/`click_count`. | Comportamento conhecido do desenho assíncrono. | Adicionar chave de idempotência/`XAUTOCLAIM` em uma fase de observabilidade. |
| R-10 | Informativo | `style-src-attr 'unsafe-inline'` permanece na CSP. | Recharts e barras de participação usam atributos `style`; não é possível aplicar nonce a atributo. `script-src` não contém `unsafe-inline` nem `unsafe-eval`. | Reavaliar `unsafe-hashes`/remoção de estilos inline; não há ganho de script execution. |
| R-11 | Informativo | Cookies `NEXT_LOCALE` e `tl_session_hint` não são `HttpOnly`. | Contêm apenas locale e “1”/vazio; não autenticam nem autorizam. | Manter sem segredos; não usar para decisões de autorização no backend. |
| R-12 | Informativo | Dependência transitiva de desenvolvimento `braces@3.0.3` (via `eslint-config-next`) tem advisory de DoS sem versão corrigida. O `shadcn` também é dev/build-time. | Não são usadas em runtime nem no bundle; `pnpm audit --prod` está limpo. | Acompanhar atualização do ESLint/Next; não executar lint sobre padrões não confiáveis. |

## Auditoria item a item — SECURITY.md

### §1 Token Bucket

| Item | Status | Evidência | Risco residual |
|---|---|---|---|
| Lua único atômico (`refill + consume`) | OK | `infra/ratelimit/redis_backend.py` (script Lua com `TIME`); `tests/unit/test_token_bucket.py`, `tests/unit/test_redis_ratelimit.py` | Nenhum identificado. |
| Baldes `redirect`, `create` (IP/usuário), `auth` (IP/e-mail), `global`, `stats/list` | OK | `infra/ratelimit/policies.py`, `dependencies.py`; `tests/unit/test_rate_limit_dependency.py`, `tests/unit/test_global_rate_limit.py` | Nenhum. |
| `RL_*` por env, 429 com `Retry-After` e `RateLimit-*` | OK | `core/config.py`; `tests/unit/test_rate_limit_dependency.py`; k6 | Nenhum. |
| Redis indisponível → breaker aberto + fallback em memória | OK | `infra/ratelimit/service.py`, `memory.py`; `tests/unit/test_token_bucket.py` | Fallback é por processo; contadores não são globais (aceito). |
| Cotas diárias de criação | OK | `infra/ratelimit/daily_quota.py`; `tests/integration/test_links_api.py` | IP é hasheado; sem IP em claro. |

Carga (k6, `apps/api/tests/load/token_bucket.js`): 12.270 requisições, **11.610 respostas 429**, 224 respostas 404 e 100/100 redirects frios em 302; p95 de latência **35,24 ms**. O `http_req_failed` alto é esperado (429 é a prova do bucket), não uma falha de threshold.

### §2 Resiliência / anti-DDoS

| Item | Status | Evidência | Risco residual |
|---|---|---|---|
| Circuit breaker Redis/Postgres | OK | `infra/resilience`; `tests/unit/test_circuit_breaker.py` | Nenhum. |
| Bulkheads DB read/write, hashing, DNS | OK | `tests/unit/test_bulkhead.py`; `core/services.py` | Nenhum. |
| Timeouts request/DB/Redis/DNS | OK | `core/middleware/timeout.py`; `Settings`; testes de config/middlewares | Nenhum. |
| Body/field/page limits | OK | `core/middleware/body_limit.py`; `tests/security/test_limits_offensive.py`; `tests/security/test_body_limit.py` | Header size depende do default do Uvicorn (16 KB), não testado ponta a ponta. |
| Cache negativo + SWR + single-flight | OK | `links/adapters/cache.py`; `tests/integration/test_link_cache.py`, `test_redirect_stampede.py` (200 concorrentes → 1 consulta; 1000 códigos inexistentes → 1 loader) | Nenhum. |
| Load shedding global | OK | `core/middleware/global_rate_limit.py`; `tests/security/test_global_rate_limit.py` | Health/readiness isento (R-05). |
| IP real conforme `TRUSTED_PROXY_COUNT` | OK | `core/middleware/real_ip.py`; `tests/security/test_real_ip.py` | Spoof se a API for exposta diretamente (R-06). |
| WAF/L3-L4 documentado | Corrigido | `README.md` (seção de produção) | Documentação, não código. |

### §3 Anti SQL Injection

| Item | Status | Evidência | Risco residual |
|---|---|---|---|
| Somente ORM/Core com parâmetros ligados | OK | Revisão de `modules/**/adapters/repository.py`, `stats_repository.py`, `flusher.py`; único `text()` dinâmico é `SET LOCAL` com binds em `infra/db/rls.py:8`. | Nenhum. |
| Role de runtime sem DDL e sem superuser/BYPASSRLS | OK | `tests/security/test_rls_security.py::test_runtime_role_has_rls_enforced` (`rolsuper=false`, `rolbypassrls=false`) | No Render, o role `trcl` ainda precisa ser verificado (P10). |
| Pydantic estrito (regex/tamanho) | OK | `tests/security/test_sqli_offensive.py` (clássico/union/blind/time-based em code, alias, q, cursor, email); `test_limits_offensive.py` | Nenhum. |
| RLS em `links` e `refresh_tokens` | OK | `alembic/versions/0002_row_level_security.py`; `tests/security/test_rls_security.py` (sem contexto = 0 linhas; contexto de A não vê B; update/delete cruzado = 0) | `click_events` sem RLS (R-04). |

Time-based payload `'; SELECT pg_sleep(2);--` respondeu em < 1,5 s (sem execução); union/drop não alteraram as tabelas semeadas.

### §4 Anti XSS / injeção no front

| Item | Status | Evidência | Risco residual |
|---|---|---|---|
| React escapa; sem `dangerouslySetInnerHTML` | OK | `apps/web/src/lib/bundle-safety.test.ts`; `links-view.test.tsx` (título `<img onerror>` vira texto, sem `<img>`/`<script>`); `apps/web/e2e/auth-links.spec.ts` (título malicioso no card e na página de detalhe) | Nenhum. |
| CSP com nonce por requisição + `strict-dynamic` | OK | `src/lib/security.ts`, `src/proxy.ts`; `apps/web/e2e/security.spec.ts`; ZAP `CSP` PASS | Nenhum. |
| `script-src` sem `unsafe-inline`/`unsafe-eval` | OK | `security.test.ts`; header do build verificado no E2E | `style-src-attr 'unsafe-inline'` é exceção documentada (R-10), fora de `script-src`. |
| HSTS, nosniff, Referrer-Policy, Permissions-Policy, COOP, XFO | OK | `securityHeaders`; `apps/web/e2e/security.spec.ts`; ZAP passa nesses itens | COEP/CORP ausentes (R-08). |
| `href` de URL do usuário só http/https + `rel` seguro | OK | `lib/url.ts`; `url.test.ts`; E2E verifica `a[target=_blank]` | Nenhum. |
| HTML 404/410 do backend sem interpolação | OK | `test_xss_offensive.py::test_html_error_pages_do_not_reflect_the_requested_code`; CSP da API em produção | Nenhum. |
| Payloads `<script>`, `"><img onerror>`, `javascript:`, `data:`, SVG, RTL/unicode em title/alias/url | OK | `tests/security/test_xss_offensive.py`; título aceito só como texto; alias/url perigosos → 422/400; `\u202e` e `\x00` rejeitados | Nenhum. |

### §5 Autenticação, sessão e força bruta

| Item | Status | Evidência | Risco residual |
|---|---|---|---|
| Argon2id OWASP, comparação, mensagens genéricas | OK | `adapters/password.py`; `tests/unit/test_identity_application.py` (hash dummy, mesmo 401) | Nenhum. |
| Access 15 min, refresh rotativo, detecção de reuso/família | OK | `application/session.py`, `refresh_session.py`; `tests/security/test_auth_offensive.py::test_refresh_reuse...` | Access não revogado no logout (R-02). |
| Cookies `HttpOnly`, `Secure`, `SameSite=Lax`, prefixos | OK | `presentation/cookies.py`; `tests/unit/test_identity_adapters.py`; `test_production_hardening.py`; E2E | `NEXT_LOCALE`/`tl_session_hint` não-HttpOnly (R-11). |
| Nada em localStorage/sessionStorage | OK | `bundle-safety.test.ts`; E2E lê storages e não encontra JWT/tokens; cookies de sessão `HttpOnly` | Nenhum. |
| CSRF double-submit + Origin/Sec-Fetch-Site | OK | `presentation/security.py`; `tests/security/test_auth_offensive.py::test_csrf...`; `test_production_surface.py` | Depende do proxy encaminhar Origin/Sec-Fetch-Site (documentado). |
| Google OIDC: state/nonce/PKCE/iss/aud/exp/email_verified | Corrigido | `adapters/google.py`, `application/google_login.py`; testes com IdP mockado; F-01 | IdP real não foi exercitado (limitação). |
| Brute force por IP e e-mail + lockout + logs sem senha | OK | `adapters/throttle.py`; `tests/security/test_auth_offensive.py::test_login_and_register_brute_force...`, `::test_progressive_lockout...` | Bucket `auth` é agressivo (5 tokens) por design; NAT pode sofrer 429. |
| Sem enumeração por resposta/timing | OK | `test_auth_offensive.py::test_login_and_register_do_not_enumerate_emails_by_response`, `::test_login_timing_does_not_reveal...` (mediana < 50 ms) | Medição local; jitter de rede pode variar em CI (teste usa limite folgado). |
| Open redirect no `next` | OK | `test_auth_offensive.py::test_google_next_rejects_open_redirect_variants`; `test_identity_adapters.py` (caminhos); `apps/web/e2e/auth-links.spec.ts` | Nenhum. |

### §6 SSRF / abuso de URL

| Item | Status | Evidência | Risco residual |
|---|---|---|---|
| Esquemas, credenciais, IPs privados/loopback/link-local/metadata/CGNAT, IPv6, IDN | OK | `domain/url_policy.py`; `tests/security/test_ssrf_offensive.py`; `tests/unit/test_url_policy.py` | Nenhum. |
| DNS rebinding: resolver e checar todos os IPs | OK | `test_ssrf_offensive.py::test_dns_rebinding_mixed_answers_are_all_checked` (ordens públicas/privadas) | DNS não é pinado após criação; servidor nunca busca a URL (abaixo). |
| Bloqueio do próprio domínio/subdomínios | OK | `test_ssrf_offensive.py::test_own_domain...`; `test_url_policy.py` | Nenhum. |
| URLs obfuscadas (decimal/octal/hex, `0.0.0.0`, `[::ffff:127.0.0.1]`, nip.io, localtest.me) | OK | `test_ssrf_offensive.py::test_obfuscated_or_internal_hostnames_are_blocked` | Depende do resolver interpretar formas exóticas; respostas privadas são bloqueadas e falhas são rejeitadas. |
| Servidor nunca busca a URL | OK | Revisão: não há `httpx`/`requests` para URL do usuário; redirect devolve `Location` | Nenhum. |
| Safe Browsing/denylist | N/A | Roadmap opcional do SECURITY.md | Não implementado; aceito. |

### §7 Credenciais e exposição

| Item | Status | Evidência | Risco residual |
|---|---|---|---|
| `.env` fora do git; `.env.example` sem segredos reais | OK | `.gitignore`; gitleaks | Nenhum. |
| gitleaks no histórico | OK | `docker run ... gitleaks detect`: 13 commits, 35,89 MB, **no leaks found**; workflow `security.yml` | Workflow não foi executado no GitHub Actions nesta rodada. |
| `os.getenv` só em `core/config.py` | OK | `tests/unit/test_config.py::test_only_config_module_reads_process_environment`; busca manual | Nenhum. |
| Nenhum segredo no bundle cliente | OK | `pnpm scan:bundle` (env carregado) em `.next/static` e `.next/server`: limpo; `bundle-safety.test.ts` | Build local; deploy precisa repetir o scan. |
| `NEXT_PUBLIC_*` sem nomes sensíveis | OK | `bundle-safety.test.ts`; `scan-bundle.mjs` | Nenhum. |
| Erros 5xx sem stack; logs sem tokens/e-mails | OK | `tests/security/test_production_hardening.py::test_unexpected_errors...`; `core/error_handlers.py`; logging | Nenhum. |
| `/docs`/`/openapi.json` off em produção | OK | `test_production_hardening.py` → 404 | Nenhum. |
| `/metrics` com token | OK | `test_production_hardening.py` (401 sem/errado, 200 com token); `test_metrics_auth.py` | Token deve ser rotacionado e mantido só no ambiente. |
| CORS inexistente (same-origin) | OK | `test_production_hardening.py::test_no_cors_headers_are_emitted` | Nenhum. |

### §8 Buffer overflow / limites

| Item | Status | Evidência | Risco residual |
|---|---|---|---|
| Limite de corpo antes de ler / chunked | OK | `core/middleware/body_limit.py`; `test_body_limit.py`; `test_limits_offensive.py` (20 KB → 413) | Nenhum. |
| Limites de campos, paginação e `limit` 50 | OK | `test_limits_offensive.py`; `test_xss_offensive.py` (título 121) | Nenhum. |
| Profundidade de JSON | OK | JSON com 2.000 níveis → **400** `bad_request`, sem 500 (`test_limits_offensive.py`) | Nenhum. |
| Headers e concorrência | Parcial | Uvicorn default de headers (~16 KB); dev `--limit-concurrency 200`; produção Gunicorn/UvicornWorker sem `limit-concurrency` explícito | Header size não testado ponta a ponta; concurrency de produção depende do balde global/WAF (aceito, documentado). |

### §9 SEO hijacking / indexação

| Item | Status | Evidência | Risco residual |
|---|---|---|---|
| `X-Robots-Tag: noindex, nofollow` em redirect/404/410 | OK | `links/presentation/router.py`; testes de redirect; E2E |
| `robots.txt` bloqueia `/account`, `/links`, `/login`, `/api` | OK | `src/app/robots.txt`; E2E/P05 |
| Canonical + hreflang + sitemap | OK | `src/lib/seo.ts`; E2E P06/P07 |
| Open redirect não usado para SEO hijacking | OK | `next` interno; ZAP `Off-site Redirect` PASS |

### §10 Supply chain

| Item | Status | Evidência | Risco residual |
|---|---|---|---|
| Lockfiles commitados | OK | `poetry.lock`, `pnpm-lock.yaml` |
| `pip-audit` | OK | `No known vulnerabilities found` (pacote local `tricolink-api` não auditável, esperado) |
| `pnpm audit --prod` | OK | `No known vulnerabilities found` |
| `pnpm audit` completo | Exceção documentada | 1 high dev-only `braces@3.0.3` via `eslint-config-next`; sem versão corrigida; não entra no bundle/runtime | R-12 |
| Dependabot | OK | `.github/dependabot.yml` (pip, npm, Docker API/web, GitHub Actions) |
| Imagens não-root/enxutas, sem segredos em camadas | OK (herdado P01) | Dockerfiles multi-stage; `USER app`/`node`; gitleaks/bundle | Imagem standalone do web não foi reconstruída nesta rodada. |

## RLS — prova independente

`tests/security/test_rls_security.py` executa com o role de runtime:

- `pg_roles`: `rolsuper=false`, `rolbypassrls=false`.
- Sem `app.current_user_id`: `SELECT * FROM links` e `SELECT * FROM refresh_tokens` retornam **0 linhas**, mesmo havendo linhas semeadas.
- Contexto do usuário A: vê somente o link/token de A; contexto de B não vê A.
- Contexto de um UUID aleatório: 0 linhas.
- `UPDATE`/`DELETE` no link de A com contexto de B: `rowcount = 0`.
- Link anônimo: invisível sem contexto; visível apenas com `app.current_link_code` exato.
- `session.get` sem contexto retorna `None`.

## Cabeçalhos/CSP e ZAP baseline

Build de produção em 3100. Verificações:

- `script-src 'self' 'nonce-…' 'strict-dynamic'` — **sem** `'unsafe-inline'`/`'unsafe-eval'`.
- `style-src-attr 'unsafe-inline'` presente (exceção R-10); `style-src` com nonce.
- HSTS `max-age=63072000; includeSubDomains; preload`; `X-Content-Type-Options: nosniff`; `X-Frame-Options: DENY`; `Referrer-Policy: strict-origin-when-cross-origin`; `Permissions-Policy` mínimo; `COOP: same-origin`.
- `X-Powered-By` ausente; `/docs`/`/openapi.json` 404 na API de produção.
- Redirects de short link com `Cache-Control: no-store` e `X-Robots-Tag: noindex, nofollow`.

ZAP baseline (`ghcr.io/zaproxy/zaproxy:stable`, alvo `/en`): **0 FAIL, 8 WARN, 59 PASS**. Os WARN são:

1. `Cookie No HttpOnly` — `NEXT_LOCALE` e `tl_session_hint`; não sensíveis (R-11).
2. `Content-Type Header Missing` — respostas 307/308 sem corpo.
3. `User Controllable HTML Element Attribute (Potential XSS)` — `next` no login; sanitizado por `sanitizeNextPath`/`toNavigationTarget` e `encodeURIComponent`; E2E prova que `javascript:`/`https://evil` não executam.
4. `CSP Header Not Set` — 404/fuzz paths e assets inexistentes; páginas estáticas sem entrada do usuário (R-07).
5. `Big Redirect Detected` — redirects 307 de autenticação; sem dado sensível no corpo.
6. `Non-Storable Content` — `no-store` intencional em páginas dinâmicas.
7. `Modern Web Application` — informativo (Next.js).
8. `Cross-Origin-Embedder-Policy Missing` — R-08.

## Segredos e DevTools

- `gitleaks` no histórico: limpo.
- `scan-bundle.mjs` com env carregado: `.next/static` e `.next/server` sem `postgresql+asyncpg://`, `redis://`, chaves privadas, `sk_live_`, `AKIA` ou valores de `JWT_SECRET`/`CSRF_SECRET`/`SESSION_SECRET`/`METRICS_TOKEN`/`GOOGLE_CLIENT_SECRET`/`DATABASE_URL`/`REDIS_URL`.
- E2E autenticado: `localStorage`/`sessionStorage` sem `eyJ`/`access_token`/`refresh_token`; `tl_access`/`tl_refresh` são `HttpOnly`; `tl_session_hint` é apenas “1”/vazio; `NEXT_LOCALE` é o locale.
- `os.getenv`/`os.environ` só em `core/config.py` (teste automatizado).

## Configuração de produção

Testes com `APP_ENV=production`:

- `/docs` e `/openapi.json` → 404.
- `/metrics` sem token/errado → 401; token correto → 200 e `Cache-Control: no-store`.
- Cookies de sessão: `__Host-tl_access`, `__Secure-tl_refresh`, `Secure`, `HttpOnly`, `SameSite=Lax`.
- Nenhum header CORS (`Access-Control-Allow-*`).
- Erro inesperado → `500 {"error":{"code":"internal_error","message":"Internal server error"}}`, sem stack/segredo.
- CSP deny-by-default e HSTS na API; `no-store` em auth.
- `TRUSTED_PROXY_COUNT`, `/docs` e cookies são validados na inicialização (`Settings`).

## Suíte ofensiva

| Área | Arquivo | Cobertura |
|---|---|---|
| SQLi | `apps/api/tests/security/test_sqli_offensive.py` | clássico, union, drop, blind/time-based em code, alias, q, cursor, email; wildcard `%`/`_` escapado; tabelas intactas |
| XSS API | `test_xss_offensive.py` | `<script>`, `<img onerror>`, `javascript:`, `data:`, SVG, RTL/unicode, título como texto, URL/alias rejeitados, HTML de erro sem reflexão |
| SSRF/URL | `test_ssrf_offensive.py` | IPv4/IPv6 privados, metadata, mapped, obfuscados, rebinding, own domain, esquemas, credenciais, CRLF/backslash |
| Auth/CSRF/IDOR/JWT | `test_auth_offensive.py` | alg none, assinatura/segredo/exp, cookie adulterado, CSRF/Origin/Sec-Fetch-Site, IDOR de links/stats, troca de sessão, reuso de refresh, logout, brute force, lockout, enumeração/timing, open redirect, cookie flags |
| RLS | `test_rls_security.py` | role, sem contexto, contexto cruzado, update/delete, link anônimo |
| Cache | `test_cache_security.py` + `tests/integration/test_link_cache.py` | reuso de código não vaza stats, corrida de invalidação, geração |
| Limites | `test_limits_offensive.py` | JSON profundo, corpo 20 KB, título/q/limit/URL |
| Headers/produção | `test_production_hardening.py` | docs/metrics, HSTS/CSP/COOP/Permissions, CORS, cookies, no-store, erros |
| Web unit | `apps/web/src/lib/bundle-safety.test.ts`, `security.test.ts`, `url.test.ts`, `links-view.test.tsx` | sem `dangerouslySetInnerHTML`/eval/Function, CSP, href seguro, título inerte |
| Web E2E | `apps/web/e2e/security.spec.ts`, `auth-links.spec.ts` | CSP/HSTS/COOP, XSS em query/título, `javascript:`/`data:` inline, href/rel, cookies/storage |

Resultados: **423 testes de API** (103 só em `tests/security`), **91 testes Vitest**, **20 testes Playwright**, todos passando. k6: thresholds verdes (429 > 0, 404 > 0, p95 < 1,5 s, 100/100 cold stampede 302).

## O que não foi possível testar / limitações honestas

- **CI real:** o workflow `.github/workflows/security.yml` foi criado e os comandos foram executados localmente, mas **não foi executado no GitHub Actions** nesta máquina. O P10 deve validar o workflow, os services Postgres/Redis e o job E2E no runner Linux.
- **k6 e ZAP** foram executados localmente em Docker Desktop/Windows; não há execução periódica em CI nem em hardware de produção.
- **Google OIDC real** não foi exercitado: os testes usam IdP mockado/Authlib. `state`, `nonce`, PKCE e claims são testados, mas o fluxo de navegador com o Google real e o redirect URI do Render não.
- **Role do Render/Postgres gerenciado** não foi consultado; o teste de RLS prova o role local `tricolink_app`. Em produção é preciso confirmar `rolsuper=false`/`rolbypassrls=false` para o role usado pela API.
- **Imagem standalone do web** não foi reconstruída/revalidada; o E2E usa `next build` + `next start` (o Next avisa que `next start` não é o modo standalone). O bundle foi escaneado localmente.
- **Firefox/WebKit** não foram executados; Playwright roda só Chromium.
- **Header size limit** não foi testado ponta a ponta (depende do Uvicorn/h11, default ~16 KB); **concurrency limit** de produção depende do Gunicorn/WAF (o dev usa `--limit-concurrency 200`).
- **Timing de enumeração** é uma medição local (5 amostras, mediana < 50 ms); não é um teste estatístico rigoroso e pode variar em CI barulhento.
- **`style-src-attr 'unsafe-inline'`** não foi removido; a justificativa está em R-10. Não há `unsafe-inline`/`unsafe-eval` em `script-src`.
- **ZAP** fez fuzzing de paths (`/*/links`, assets inexistentes) que não são rotas reais; os WARN de CSP nesses caminhos são R-07.
- **Access JWT pós-logout** e **verificação de e-mail** continuam como riscos de produto (R-01/R-02), não como falhas ocultas.

## Como reproduzir

```bash
# API (com Postgres/Redis no Compose)
docker compose exec -T api pytest -q
docker compose exec -T api pytest -q tests/security
docker compose exec -T api ruff check src tests
docker compose exec -T api mypy src

# Web
cd apps/web
pnpm test
pnpm lint
pnpm typecheck
pnpm build
pnpm scan:bundle
pnpm test:e2e

# Segredos / supply chain
docker run --rm -v "$PWD:/repo" zricethezav/gitleaks:latest detect --source=/repo --config=/repo/.gitleaks.toml --redact --verbose
docker compose exec -T api pip-audit --desc
cd apps/web && pnpm audit --prod --audit-level high

# Carga (API no network do Compose)
Get-Content -Raw apps/api/tests/load/token_bucket.js | docker run --rm -i --network tricolink_app -e BASE_URL=http://api:8000 grafana/k6 run -

# ZAP baseline (web em 3100)
docker run --rm -v "$OUT:/zap/wrk:rw" ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://host.docker.internal:3100/en -r zap-report.html
```

## Conclusão

O código resistiu à suíte ofensiva e aos scanners sem achados críticos/altos em aberto. As correções F-01/F-02 eliminam as duas falhas altas encontradas (JWT não verificado no OIDC e pré-hijacking por auto-vínculo). F-03/F-04/F-05 eliminam vazamentos/race conditions no cache e a parada do flusher. As pendências são de produto (verificação de e-mail, revogação de access JWT), de topologia (proxy/WAF, role do Render) e de validação em CI/Linux, todas registradas acima sem maquiagem.
