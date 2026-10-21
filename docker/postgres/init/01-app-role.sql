-- Local development role for the API runtime.
-- It is intentionally NOT a superuser so RLS policies are enforced.
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'tricolink_app') THEN
    CREATE ROLE tricolink_app LOGIN PASSWORD 'tricolink_app'
      NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT;
  END IF;
END
$$;

DO $$
BEGIN
  EXECUTE format('GRANT CONNECT ON DATABASE %I TO tricolink_app', current_database());
END
$$;

GRANT USAGE ON SCHEMA public TO tricolink_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO tricolink_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO tricolink_app;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO tricolink_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT USAGE, SELECT ON SEQUENCES TO tricolink_app;
