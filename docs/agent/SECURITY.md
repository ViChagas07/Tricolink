# SECURITY.md — Requisitos de segurança do Tricolink

Cada item abaixo vira **código + teste** (pasta `tests/security/` na API; Playwright/Vitest no web). A fase P09 audita tudo.

## 1. Token Bucket (rate limiting) — Redis + Lua atômico
- Script Lua único (`refill + consume`) retornando `allowed, remaining, retry_after_ms`. Sem race condition.
- Baldes (chave `rl:{escopo}:{id}`): `redirect` (por IP), `create` (por IP e por usuário), `auth` (por IP **e** por e-mail normalizado), `global` (load shedding), `stats/list` (por usuário).
- Parâmetros via env (`RL_*`). Respostas 429 com `Retry-After` e headers `RateLimit-Limit/Remaining/Reset`.
- Redis indisponível → **Circuit Breaker** abre e o limitador cai para token bucket **em memória** por processo (degradação segura, nunca "libera tudo" sem limite).
- Cotas diárias de criação (anônimo/logado) além do token bucket.

## 2. Resiliência / anti-DDoS (defesa em camadas)
- **Circuit Breaker** (closed/open/half-open) em Redis e Postgres; **Bulkhead** (semáforos separados) para: leituras de DB, escritas de DB, hashing argon2 (rodar em threadpool limitado) e resolução DNS.
- Timeouts em tudo (request, DB, Redis, DNS); limite de corpo (`MAX_BODY_BYTES`), limite de tamanho de campos, paginação com teto, `limit` máx 50.
- Cache negativo + SWR + single-flight protegem o banco de picos no redirect.
- Load shedding: balde `global` responde 503/429 rápido antes de tocar no banco.
- IP real: confiar em `X-Forwarded-For` apenas conforme `TRUSTED_PROXY_COUNT` (contar a partir da direita); nunca confiar cegamente no header.
- Documentar no README: em produção, colocar Cloudflare/WAF na frente (L3/L4 não se resolve na aplicação).

## 3. Anti SQL Injection
- Somente ORM/Core com parâmetros ligados; zero SQL por f-string/format/`+`. Se precisar de `text()`, usar `:param`.
- Usuário do banco da aplicação com privilégio mínimo (sem DDL em runtime; migrations com outro usuário).
- Validação Pydantic estrita (tipos, regex, tamanhos). Testes com payloads clássicos (`' OR 1=1--`, `'; DROP TABLE`, union, blind) em `code`, `alias`, `q`, `cursor`, `email`.
- **RLS (Row Level Security)** em `links` e `refresh_tokens`: política por `app.current_user_id` (`SET LOCAL`) além da checagem de dono na aplicação (defesa em profundidade; evita IDOR).

## 4. Anti XSS / injeção no front
- React escapa por padrão; **proibido** `dangerouslySetInnerHTML`. Título/alias exibidos apenas como texto.
- **CSP com nonce** por requisição (middleware Next): `default-src 'self'; script-src 'self' 'nonce-…' 'strict-dynamic'; style-src 'self' 'nonce-…'/hash; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'; object-src 'none'`.
- Headers: HSTS (preload), `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy` mínimo, `Cross-Origin-Opener-Policy: same-origin`, `X-Frame-Options: DENY`.
- `href` renderizado de URL do usuário: só se esquema `http/https` (mesma política do backend); `rel="noopener noreferrer nofollow ugc"` e `target="_blank"`.
- Páginas HTML estáticas do backend (404/410) sem interpolar entrada do usuário.
- Testes com payloads (`<script>`, `"><img onerror>`, `javascript:`, `data:`, unicode/RTL spoofing) em title/alias/url.

## 5. Autenticação, sessão e força bruta
- argon2id (parâmetros OWASP), comparação em tempo constante, mensagens genéricas ("credenciais inválidas"), sem enumeração de e-mails (cadastro e login respondem de forma indistinguível quando possível).
- Access JWT curto (15 min) + refresh opaco rotativo com **detecção de reuso** (reuso revoga a família inteira). Tokens só em **cookies httpOnly, Secure, SameSite=Lax** (prefixo `__Host-` quando possível). Nada em localStorage.
- **CSRF**: double-submit token em requisições mutáveis + checagem de `Origin`/`Sec-Fetch-Site`.
- Google OIDC: `state`, `nonce` e PKCE; validar `iss`, `aud`, `exp`, `email_verified`.
- Brute force: token bucket por IP **e** por e-mail + backoff progressivo / lockout temporário; logs de tentativas (sem senha).
- Open redirect: parâmetro `next` só aceita caminho interno.

## 6. SSRF / abuso de URL
- Política de URL do CONTEXT §6 (esquemas, credenciais, IPs privados, DNS rebinding: resolver e checar **todos** os IPs resolvidos, bloquear 169.254.169.254 e ranges internos, IPv6 incluso).
- O servidor **nunca busca** a URL do usuário (sem fetch de título/preview) → superfície de SSRF mínima. Se isso mudar, exige revisão de segurança.
- Opcional/roadmap: checagem Safe Browsing e denylist de domínios.

## 7. Credenciais e exposição
- `.env` fora do git; `.env.example` sem segredos reais; gitleaks no CI; `os.getenv()` somente em `core/config.py`.
- Nenhum segredo em bundle do cliente (auditar `NEXT_PUBLIC_*`); erros 5xx sem stack trace ao cliente; logs sem tokens/senhas/e-mails completos quando evitável.
- Respostas de erro padronizadas; `/docs` e `/openapi.json` desativados em produção; `/metrics` com token.

## 8. Buffer overflow / limites
- Python é memory-safe, mas aplicar o equivalente lógico: limites de corpo, headers, tamanhos de string, profundidade de JSON; rejeitar `Content-Length` acima do limite antes de ler; `uvicorn --limit-concurrency`.

## 9. SEO hijacking / indexação
- Links curtos: `X-Robots-Tag: noindex, nofollow` nos redirects e páginas 404/410.
- Canonical + `hreflang` corretos nas páginas públicas; `robots.txt` bloqueia `/account`, `/links`, `/login` e `/api`.

## 10. Supply chain
- Lockfiles commitados; `pip-audit` e `pnpm audit` no CI; Dependabot; imagens Docker enxutas, usuário não-root, sem segredos nas camadas.
