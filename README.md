# Tricolink
Encurtador de URL (projeto de portfólio). README completo é gerado na fase P11.
Veja `AGENTS.md` e `docs/agent/` para a especificação (SDD).

## Decisões técnicas
- Redirecionamento usa **302**, não 301: o navegador não guarda a resposta em cache e cada clique chega ao servidor para contabilização. A resposta leva `Cache-Control: no-store`.
- O cache de redirect (`tl:link:*`) combina TTL duro (Redis), TTL macio com jitter (SWR), single-flight em processo + `SET NX PX` no Redis e cache negativo (`tl:neg:*`). Redis indisponível cai para o Postgres via bulkhead `db_read`.
- Cliques são enviados de forma assíncrona ao Redis Stream `tl:clicks`; um flusher de consumer group grava em lote em `click_events` e incrementa `links.click_count`. O redirect nunca espera o INSERT.
