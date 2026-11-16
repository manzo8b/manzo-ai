-- MANZO AI / M3 — catalog metadata isolation (reviewed, NOT deployed).
-- No commercial or B2B rows, student information, exam questions or solutions.
-- Running this on Supabase requires an independently verified logical backup
-- and an explicit post-test deployment gate. On CI it runs in ephemeral Postgres.
--
-- Security stance: deny-by-default. There are NO anon/authenticated policies or
-- privileges. This schema is not intended to be added to PostgREST exposed schemas
-- until a separate public-read migration has been reviewed.

CREATE SCHEMA IF NOT EXISTS content_public;
CREATE SCHEMA IF NOT EXISTS content_internal;

REVOKE ALL ON SCHEMA content_public FROM PUBLIC, anon, authenticated, service_role;
REVOKE ALL ON SCHEMA content_internal FROM PUBLIC, anon, authenticated, service_role;

CREATE TABLE IF NOT EXISTS content_public.catalog_courses (
    course_key text PRIMARY KEY
        CHECK (course_key ~ '^[a-z][a-z0-9-]{2,90}$'),
    mode text NOT NULL DEFAULT 'public_learning'
        CHECK (mode = 'public_learning'),
    canonical_locale text NOT NULL DEFAULT 'it'
        CHECK (canonical_locale IN ('it','en','es')),
    b2b_enrollment_enabled boolean NOT NULL DEFAULT false
        CHECK (b2b_enrollment_enabled IS false),
    b2b_grading_enabled boolean NOT NULL DEFAULT false
        CHECK (b2b_grading_enabled IS false),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS content_public.catalog_localizations (
    course_key text NOT NULL
        REFERENCES content_public.catalog_courses(course_key) ON DELETE RESTRICT,
    locale text NOT NULL CHECK (locale IN ('it','en','es')),
    title text NOT NULL CHECK (length(btrim(title)) > 0 AND length(title) <= 500),
    route text NOT NULL UNIQUE
        CHECK (route LIKE ('/manzo-ai/' || locale || '/%')),
    source_path text NOT NULL
        CHECK (source_path LIKE 'editorial/learning/hallucinations/%'
               AND source_path NOT LIKE '%..%'),
    source_sha256 text NOT NULL
        CHECK (source_sha256 ~ '^[a-f0-9]{64}$'),
    editorial_status text NOT NULL
        CHECK (editorial_status = 'published_static'),
    unit_count integer NOT NULL CHECK (unit_count BETWEEN 1 AND 100),
    public_self_assessment_count integer NOT NULL
        CHECK (public_self_assessment_count BETWEEN 0 AND 1000),
    public_case_count integer NOT NULL
        CHECK (public_case_count BETWEEN 0 AND 1000),
    source_contains_public_answers boolean NOT NULL DEFAULT true
        CHECK (source_contains_public_answers IS true),
    private_assessment_ready boolean NOT NULL DEFAULT false
        CHECK (private_assessment_ready IS false),
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (course_key, locale)
);

CREATE TABLE IF NOT EXISTS content_public.catalog_units (
    course_key text NOT NULL,
    locale text NOT NULL CHECK (locale IN ('it','en','es')),
    unit_key text NOT NULL CHECK (unit_key ~ '^(core|coding)-0[1-9][0-9]?$'),
    position integer NOT NULL CHECK (position BETWEEN 1 AND 100),
    title text NOT NULL CHECK (length(btrim(title)) > 0 AND length(title) <= 500),
    duration text CHECK (duration IS NULL OR length(duration) BETWEEN 1 AND 80),
    PRIMARY KEY (course_key, locale, unit_key),
    UNIQUE (course_key, locale, position),
    FOREIGN KEY (course_key, locale)
        REFERENCES content_public.catalog_localizations(course_key, locale)
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS content_internal.import_runs (
    manifest_sha256 text PRIMARY KEY
        CHECK (manifest_sha256 ~ '^[a-f0-9]{64}$'),
    source_revision text NOT NULL
        CHECK (source_revision ~ '^[a-f0-9]{40}$'),
    schema_version text NOT NULL CHECK (schema_version = '1.0'),
    course_count integer NOT NULL CHECK (course_count >= 0),
    localization_count integer NOT NULL CHECK (localization_count >= 0),
    unit_count integer NOT NULL CHECK (unit_count >= 0),
    imported_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE content_public.catalog_courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_public.catalog_courses FORCE ROW LEVEL SECURITY;
ALTER TABLE content_public.catalog_localizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_public.catalog_localizations FORCE ROW LEVEL SECURITY;
ALTER TABLE content_public.catalog_units ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_public.catalog_units FORCE ROW LEVEL SECURITY;
ALTER TABLE content_internal.import_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_internal.import_runs FORCE ROW LEVEL SECURITY;

REVOKE ALL ON ALL TABLES IN SCHEMA content_public
    FROM PUBLIC, anon, authenticated, service_role;
REVOKE ALL ON ALL TABLES IN SCHEMA content_internal
    FROM PUBLIC, anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA content_public
    REVOKE ALL ON TABLES FROM PUBLIC, anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA content_internal
    REVOKE ALL ON TABLES FROM PUBLIC, anon, authenticated, service_role;

-- No GRANT and NO policies for anon/authenticated/service_role.
-- These tables deliberately cannot be queried via public Data API today.
