-- Test-only Supabase auth fixture: NEVER deploy to a real project.
-- Replaces the auth.users table and auth.uid() function in an ephemeral
-- PostgreSQL CI container with verified-session-like test inputs.
CREATE ROLE authenticated NOLOGIN;
CREATE SCHEMA auth;
CREATE TABLE auth.users (id uuid PRIMARY KEY);
CREATE FUNCTION auth.uid()
RETURNS uuid
LANGUAGE sql STABLE
AS $fixture$
  SELECT NULLIF(current_setting('request.jwt.claim.sub',true),'')::uuid
$fixture$;
GRANT USAGE ON SCHEMA auth TO authenticated;
GRANT EXECUTE ON FUNCTION auth.uid() TO authenticated;
INSERT INTO auth.users(id) VALUES
 ('11111111-1111-4111-8111-111111111111'), -- tenant A owner
 ('22222222-2222-4222-8222-222222222222'), -- tenant A learner
 ('44444444-4444-4444-8444-444444444444'), -- tenant A other learner
 ('33333333-3333-4333-8333-333333333333'); -- tenant B learner
