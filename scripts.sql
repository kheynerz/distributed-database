DO $$ <<create_extension>> DECLARE installed BOOL := false; BEGIN SELECT (COUNT(*) = 1) into installed FROM pg_extension WHERE extname = 'postgres_fdw'; IF NOT installed THEN CREATE EXTENSION postgres_fdw; END IF; END create_extension $$;