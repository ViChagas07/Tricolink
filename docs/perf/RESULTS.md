# Resultados de carga — P10

**Data:** 2026-10-22
**Máquina:** AMD Ryzen 7 5800X (8C/16T), 16 GB RAM, Windows 11 25H2 (build 26200).
**Docker Desktop:** 29.4.3; VM com **16 CPUs e 8,29 GB** de RAM.
**API:** container `tricolink-api` (imagem dev), Uvicorn 0.38 com `--reload --limit-concurrency 200`, 1 processo.
**Banco/cache:** PostgreSQL 16.15 e Redis 7.4.11 em containers Alpine na mesma rede Docker.
**Gerador:** k6 v2.3.0 em container `grafana/k6`, na mesma rede Docker (`tricolink_app`); o gerador compartilha CPU/RAM com a API.
**Não é um benchmark de produção:** os números abaixo são do ambiente local, com o gerador no mesmo host e limites de dev. Não foram feitos ajustes de CPU pinning, `ulimit`, TCP tuning ou réplicas.

## Metodologia

1. `docker compose exec -T redis redis-cli FLUSHDB` antes de cada execução.
2. `loadtest/redirect.js` cria um link no `setup` (warm/ratelimit) ou usa 500 códigos
   pré-semeados em `loadtest/seed_cold.sql` (cold), com a cache fria.
3. `loadtest/create.js` cria links via API; no modo `throughput` cada iteração usa um
   `X-Forwarded-For` sintético diferente (só para o teste; em produção o header é
   confiável apenas atrás do proxy), e no modo `ratelimit` usa um IP fixo.
4. Os códigos de link usam `https://93.184.216.34/loadtest/...` (IP literal, sem DNS).
5. Depois das execuções: `loadtest/cleanup.sql`.

Os números de p50/p95/p99 vêm do `handleSummary` do k6 (Trend dedicado
`redirect_duration`/`create_duration`); RPS vem do `redirect_ok`/`created` dividido pela
duração do teste. `http_reqs` inclui requests do `setup` quando ele existe; por isso as
tabelas usam os contadores do cenário, não o total bruto.

## Resultados

### Redirect — cache quente (rampa 50→150 RPS, 65 s)

| Métrica | Valor |
|---|---:|
| Requisições de redirect | 6.581 |
| RPS médio | 101,1 |
| p50 | 4,84 ms |
| p95 | 941,92 ms |
| p99 | 1.593,63 ms |
| 302 | 6.538 |
| 429 | 0 |
| 5xx | 42 (0,64%) |

O p50 de 4,8 ms confirma o cache quente; o p95/p99 sobem no topo da rampa de 150 RPS,
quando 150 VUs encostam no `--limit-concurrency 200` e na contenção do host. O número
reportado é o da execução final; o Docker Desktop variou entre execuções (em uma
rodada intermediária sem o Trend dedicado houve 6.749/6.750 respostas 302 e nenhum 5xx,
mas os percentis dessa rodada não foram preservados).

### Redirect — cache frio (500 códigos, 50 VUs)

| Métrica | Valor |
|---|---:|
| Requisições | 500 |
| RPS | 88,5 |
| p50 | 342,12 ms |
| p95 | 1.517,99 ms |
| p99 | 1.534,59 ms |
| máx | 1.562,77 ms |
| 302 | 500 (100%) |
| 429 / 5xx | 0 / 0 |

Cada código foi consultado uma vez com `tl:link`/`tl:neg` vazios; o single-flight
impede stampede dentro do mesmo processo, mas 500 códigos distintos exigem 500 idas ao
Postgres. O p50 de ~342 ms é o custo de banco + serialização do primeiro hit.

### Redirect — prova do token bucket (IP fixo, rampa 20→300 RPS, 65 s)

| Métrica | Valor |
|---|---:|
| Requisições | 10.258 |
| RPS médio | 157,4 |
| p50 | 2,45 ms |
| p95 | 176,94 ms |
| p99 | 2.201,64 ms |
| 302 | 1.515 |
| **429** | **8.531 (83,2%)** |
| 5xx | 211 (2,1%) |

O 429 aparece já na subida; o p50 de 2,4 ms é a resposta barata do bucket. Os 5xx
ocorrem no topo da rampa, quando o `--limit-concurrency 200` do servidor de dev é
atingido; são erros de sobrecarga, não de lógica de negócio. O teste prova que o
bucket responde 429 e que a API não fica processando a carga inteira.

### Create — throughput (rampa 10→100 RPS, 55 s, IPs sintéticos por iteração)

| Métrica | Valor |
|---|---:|
| Requisições | 3.997 |
| RPS médio | 72,7 |
| p50 | 69,76 ms |
| p95 | 880,59 ms |
| p99 | 1.056,24 ms |
| 201 | 3.991 (99,85%) |
| 429 | 0 |
| 5xx | 6 (0,15%) |

O gargalo é o insert + resolução DNS/validação; a mediana de 69,8 ms é dominada pelo
trabalho de criação, não pelo cache. Os 6 erros são a cauda de contenção do host.

### Create — prova do token bucket (IP fixo, rampa 5→100 RPS, 55 s)

| Métrica | Valor |
|---|---:|
| Requisições | 2.535 |
| RPS médio | 46,1 |
| p50 | 3,21 ms |
| p95 | 21,41 ms |
| p99 | 157,63 ms |
| 201 | 5 |
| **429** | **2.530 (99,8%)** |
| 5xx | 0 |

Só 5 criações passam: é a **cota diária anônima** (`ANON_DAILY_LINK_LIMIT=5`) por IP,
que dispara antes do bucket de create esgotar. O restante é 429, como esperado para um
IP fixo. Para medir throughput de create use o cenário com IPs distintos.

## Leitura dos resultados

- **Cache quente** atende na casa de 100 RPS com p50 de poucos ms neste host; a cauda
  p95/p99 cresce perto de 150 RPS por limite de concorrência e disputa de CPU do
  Docker Desktop, não por query ao Postgres.
- **Cache frio** custa ~340 ms de mediana por código novo; 500 códigos distintos em
  50 VUs terminaram em ~5,7 s (88,5 req/s), sem 429/5xx.
- **Token bucket**: 8.531 429 no redirect e 2.530 429 no create; o caminho 429 é
  barato (p50 de 2–3 ms) e alivia o banco.
- **Criação**: ~73 RPS de throughput com IPs distintos; a cota diária e o bucket por
  IP são o limite quando o IP é fixo.
- O host é o gargalo: o `--limit-concurrency 200` do Uvicorn dev gera 5xx na cauda
  das rampas mais altas. Em produção, o Render/Gunicorn e o WAF mudam esse teto; os
  números não devem ser extrapolados para o Render.

## Reprodução

```bash
# API, Postgres e Redis
docker compose up -d --build --wait postgres redis api
docker compose exec -T api alembic upgrade head

# Warm redirect
docker compose exec -T redis redis-cli FLUSHDB
Get-Content -Raw loadtest/redirect.js |
  docker run --rm -i --network tricolink_app -e BASE_URL=http://api:8000 -e MODE=warm \
  grafana/k6 run -

# Cold redirect (500 códigos)
Get-Content -Raw loadtest/cleanup.sql | docker compose exec -T postgres psql -U tricolink -d tricolink
Get-Content -Raw loadtest/seed_cold.sql | docker compose exec -T postgres psql -U tricolink -d tricolink
$codes = @(docker compose exec -T postgres psql -U tricolink -d tricolink -At \
  -c "SELECT code FROM links WHERE original_url LIKE 'https://93.184.216.34/loadtest/redirect-%' ORDER BY id") |
  Where-Object { $_ -match '^ld' }
$codes | ConvertTo-Json -Compress | Set-Content -LiteralPath .secrets/codes.json -Encoding utf8
docker compose exec -T redis redis-cli FLUSHDB
Get-Content -Raw loadtest/redirect.js |
  docker run --rm -i --network tricolink_app -v "$((Get-Location).Path)/.secrets:/loadtest:ro" \
  -e BASE_URL=http://api:8000 -e MODE=cold -e CODES_FILE=/loadtest/codes.json grafana/k6 run -

# Rate limit do redirect
docker compose exec -T redis redis-cli FLUSHDB
Get-Content -Raw loadtest/redirect.js |
  docker run --rm -i --network tricolink_app -e BASE_URL=http://api:8000 -e MODE=ratelimit \
  grafana/k6 run -

# Create throughput / rate limit
Get-Content -Raw loadtest/create.js |
  docker run --rm -i --network tricolink_app -e BASE_URL=http://api:8000 -e MODE=throughput \
  grafana/k6 run -
Get-Content -Raw loadtest/create.js |
  docker run --rm -i --network tricolink_app -e BASE_URL=http://api:8000 -e MODE=ratelimit \
  grafana/k6 run -

# Limpeza
Get-Content -Raw loadtest/cleanup.sql | docker compose exec -T postgres psql -U tricolink -d tricolink
```

> No PowerShell, o JSON de códigos precisa ser gravado sem BOM (`UTF8Encoding(false)`);
> o `open()` do k6 rejeita BOM. No CI/Linux, use `jq -c`/`printf` para o mesmo efeito.
