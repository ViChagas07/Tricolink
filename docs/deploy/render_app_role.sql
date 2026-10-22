-- Execute no banco do Render, conectado como o usuário administrativo
-- (o mesmo usado por MIGRATION_DATABASE_URL), DEPOIS do primeiro deploy
-- que aplicou as migrations. Troque a senha antes de executar.
--
-- psql "$MIGRATION_DATABASE_URL" -f docs/deploy/render_app_role.sql
\set app_password 'TROQUE-POR-UMA-SENHA-FORTE'

CREATE ROLE tricolink_app
  LOGIN
  PASSWORD :'app_password'
  NOSUPERUSER
  NOCREATEDB
  NOCREATEROLE
  NOINHERIT
  NOBYPASSRLS;

GRANT CONNECT ON DATABASE tricolink TO tricolink_app;
GRANT USAGE ON SCHEMA public TO tricolink_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO tricolink_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO tricolink_app;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO tricolink_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT USAGE, SELECT ON SEQUENCES TO tricolink_app;

-- O role NÃO deve ser dono das tabelas nem membro de roles privilegiadas.
-- Confirme:
SELECT rolname, rolsuper, rolbypassrls
FROM pg_roles
WHERE rolname = 'tricolink_app';
