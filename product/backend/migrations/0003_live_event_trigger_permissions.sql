-- MANZO AI · Live security hardening 0003 (2026-11-16)
-- New, separately linked MANZO AI Supabase project only.
-- The Supabase-managed event-trigger helper is SECURITY DEFINER.
-- It should remain available for Postgres DDL events, but must not
-- expose EXECUTE grants to unauthenticated or ordinary users.
--
-- No tables, customer records, policies, triggers or schema objects
-- are deleted or replaced by this migration.
REVOKE EXECUTE ON FUNCTION public.rls_auto_enable()
  FROM PUBLIC, anon, authenticated;
