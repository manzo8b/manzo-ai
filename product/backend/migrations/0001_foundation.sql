-- MANZO AI · Database foundation v0.1
-- Target: Supabase Postgres (auth.users + auth.uid())
-- Migrations are NOT automatically applied to any connected project.
-- Create a NEW dedicated MANZO AI project when region, DPA and costs are approved.
-- Public clients receive read-only access to strictly RLS-scoped resources.
-- All writes, billing events, attempts and AI runs require a separately secured backend.
BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS app;
CREATE SCHEMA IF NOT EXISTS app_private;
REVOKE ALL ON SCHEMA app_private FROM PUBLIC;
REVOKE ALL ON SCHEMA app FROM PUBLIC;

CREATE TABLE app.organizations (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text NOT NULL CHECK (length(trim(name)) BETWEEN 2 AND 140),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE app.memberships (
    organization_id uuid NOT NULL REFERENCES app.organizations(id) ON DELETE CASCADE,
    user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    role text NOT NULL CHECK (role IN ('owner','admin','instructor','learner')),
    status text NOT NULL DEFAULT 'active' CHECK (status IN ('active','suspended')),
    created_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (organization_id, user_id)
);

CREATE TABLE app.courses (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL REFERENCES app.organizations(id) ON DELETE CASCADE,
    slug text NOT NULL CHECK (slug ~ '^[a-z0-9]+(-[a-z0-9]+)*$'),
    title text NOT NULL CHECK (length(trim(title)) BETWEEN 3 AND 180),
    status text NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','published','archived')),
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (organization_id, id),
    UNIQUE (organization_id, slug)
);

CREATE TABLE app.course_versions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL,
    course_id uuid NOT NULL,
    version_number integer NOT NULL CHECK (version_number > 0),
    status text NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','published','retired')),
    content_ref text NOT NULL CHECK (length(trim(content_ref)) BETWEEN 3 AND 350),
    published_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (organization_id, course_id)
        REFERENCES app.courses(organization_id,id) ON DELETE CASCADE,
    UNIQUE (organization_id,id),
    UNIQUE (organization_id,course_id,version_number),
    CHECK (status <> 'published' OR published_at IS NOT NULL)
);

CREATE TABLE app.enrollments (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL,
    course_id uuid NOT NULL,
    user_id uuid NOT NULL,
    status text NOT NULL DEFAULT 'active'
        CHECK (status IN ('active','completed','revoked')),
    created_at timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (organization_id,course_id)
        REFERENCES app.courses(organization_id,id) ON DELETE CASCADE,
    FOREIGN KEY (organization_id,user_id)
        REFERENCES app.memberships(organization_id,user_id) ON DELETE CASCADE,
    UNIQUE (organization_id,course_id,user_id)
);

CREATE TABLE app.learning_attempts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL,
    course_id uuid NOT NULL,
    user_id uuid NOT NULL,
    version_id uuid NOT NULL,
    assessment_id text NOT NULL CHECK (length(trim(assessment_id)) BETWEEN 1 AND 160),
    score_percent integer CHECK (score_percent BETWEEN 0 AND 100),
    recorded_at timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (organization_id,course_id,user_id)
        REFERENCES app.enrollments(organization_id,course_id,user_id) ON DELETE CASCADE,
    FOREIGN KEY (organization_id,version_id)
        REFERENCES app.course_versions(organization_id,id),
    -- Backend must additionally ensure version_id belongs to course_id;
    -- this is enforced below by a composite FK.
    UNIQUE (id,organization_id)
);

-- Strengthen version/course/tenant integrity: it must be impossible for a
-- backend mistake to record an attempt against another course's version.
ALTER TABLE app.course_versions
    ADD CONSTRAINT course_versions_org_course_id_unique UNIQUE (organization_id,course_id,id);
ALTER TABLE app.learning_attempts
    ADD CONSTRAINT learning_attempts_version_course_fk
    FOREIGN KEY (organization_id,course_id,version_id)
    REFERENCES app.course_versions(organization_id,course_id,id);

CREATE TABLE app.agent_runs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id uuid NOT NULL,
    user_id uuid NOT NULL,
    feature text NOT NULL CHECK (feature ~ '^[a-z][a-z0-9_.-]{2,100}$'),
    state text NOT NULL DEFAULT 'queued'
        CHECK (state IN ('queued','running','needs_review','completed','failed','cancelled')),
    provider text,
    input_tokens bigint NOT NULL DEFAULT 0 CHECK (input_tokens >= 0),
    output_tokens bigint NOT NULL DEFAULT 0 CHECK (output_tokens >= 0),
    estimated_cost_microunits bigint NOT NULL DEFAULT 0
        CHECK (estimated_cost_microunits >= 0),
    created_at timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (organization_id,user_id)
        REFERENCES app.memberships(organization_id,user_id) ON DELETE CASCADE
);

-- Never expose financial control tables through PostgREST.
-- These are updated only by trusted, signed webhook or quota transactions.
CREATE TABLE app_private.feature_grants (
    organization_id uuid NOT NULL REFERENCES app.organizations(id) ON DELETE CASCADE,
    feature text NOT NULL CHECK (feature ~ '^[a-z][a-z0-9_.-]{2,100}$'),
    status text NOT NULL DEFAULT 'inactive'
        CHECK (status IN ('inactive','active','suspended','revoked')),
    valid_until timestamptz NOT NULL,
    quota bigint NOT NULL CHECK (quota >= 0),
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (organization_id,feature)
);

CREATE TABLE app_private.feature_usage (
    organization_id uuid NOT NULL,
    feature text NOT NULL,
    consumed bigint NOT NULL DEFAULT 0 CHECK (consumed >= 0),
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (organization_id,feature),
    FOREIGN KEY (organization_id,feature)
        REFERENCES app_private.feature_grants(organization_id,feature) ON DELETE CASCADE
);

CREATE TABLE app_private.billing_events (
    provider text NOT NULL CHECK (provider IN ('stripe')),
    provider_event_id text NOT NULL CHECK (length(provider_event_id) BETWEEN 5 AND 250),
    event_type text NOT NULL CHECK (length(event_type) BETWEEN 2 AND 250),
    received_at timestamptz NOT NULL DEFAULT now(),
    processed_at timestamptz,
    status text NOT NULL DEFAULT 'received'
        CHECK (status IN ('received','processed','failed')),
    PRIMARY KEY (provider,provider_event_id)
);
COMMENT ON TABLE app_private.billing_events IS
    'Idempotency ledger only. NEVER use redirect parameters to grant licenses.';

CREATE INDEX idx_memberships_user ON app.memberships(user_id,status);
CREATE INDEX idx_courses_tenant_status ON app.courses(organization_id,status);
CREATE INDEX idx_versions_by_course ON app.course_versions(organization_id,course_id,version_number DESC);
CREATE INDEX idx_enrollments_user ON app.enrollments(user_id,organization_id);
CREATE INDEX idx_attempts_user_course ON app.learning_attempts(user_id,organization_id,course_id,recorded_at DESC);
CREATE INDEX idx_agent_runs_by_user ON app.agent_runs(user_id,organization_id,created_at DESC);

-- These helpers bypass RLS ONLY to check membership safely.
-- auth.uid() gets the identity from a verified session in Supabase.
-- Never accept an arbitrary organization/user ID as proof of identity.
CREATE FUNCTION app_private.is_member(p_organization_id uuid)
RETURNS boolean
LANGUAGE sql STABLE SECURITY DEFINER SET search_path = ''
AS $$
    SELECT EXISTS (
        SELECT 1 FROM app.memberships m
        WHERE m.organization_id=p_organization_id
          AND m.user_id=(SELECT auth.uid())
          AND m.status='active'
    )
$$;

CREATE FUNCTION app_private.is_admin(p_organization_id uuid)
RETURNS boolean
LANGUAGE sql STABLE SECURITY DEFINER SET search_path = ''
AS $$
    SELECT EXISTS (
        SELECT 1 FROM app.memberships m
        WHERE m.organization_id=p_organization_id
          AND m.user_id=(SELECT auth.uid())
          AND m.status='active'
          AND m.role IN ('owner','admin')
    )
$$;

REVOKE ALL ON ALL FUNCTIONS IN SCHEMA app_private FROM PUBLIC;
GRANT USAGE ON SCHEMA app_private TO authenticated;
GRANT EXECUTE ON FUNCTION app_private.is_member(uuid) TO authenticated;
GRANT EXECUTE ON FUNCTION app_private.is_admin(uuid) TO authenticated;

-- Default deny: all tables have row-level security ON and FORCE.
ALTER TABLE app.organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.organizations FORCE ROW LEVEL SECURITY;
ALTER TABLE app.memberships ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.memberships FORCE ROW LEVEL SECURITY;
ALTER TABLE app.courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.courses FORCE ROW LEVEL SECURITY;
ALTER TABLE app.course_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.course_versions FORCE ROW LEVEL SECURITY;
ALTER TABLE app.enrollments ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.enrollments FORCE ROW LEVEL SECURITY;
ALTER TABLE app.learning_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.learning_attempts FORCE ROW LEVEL SECURITY;
ALTER TABLE app.agent_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.agent_runs FORCE ROW LEVEL SECURITY;
ALTER TABLE app_private.feature_grants ENABLE ROW LEVEL SECURITY;
ALTER TABLE app_private.feature_grants FORCE ROW LEVEL SECURITY;
ALTER TABLE app_private.feature_usage ENABLE ROW LEVEL SECURITY;
ALTER TABLE app_private.feature_usage FORCE ROW LEVEL SECURITY;
ALTER TABLE app_private.billing_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE app_private.billing_events FORCE ROW LEVEL SECURITY;

-- Service access is for trusted backend processes ONLY.
-- Supabase's service_role has BYPASSRLS, but still requires object privileges.
-- NEVER expose this role's key or a database connection string to the browser.
GRANT USAGE ON SCHEMA app,app_private TO service_role;
GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA app,app_private TO service_role;

-- Clients can read ONLY. All mutations must be server-authorized.
GRANT USAGE ON SCHEMA app TO authenticated;
GRANT SELECT ON
    app.organizations,app.memberships,app.courses,
    app.course_versions,app.enrollments,app.learning_attempts,app.agent_runs
TO authenticated;

CREATE POLICY organization_member_read ON app.organizations FOR SELECT TO authenticated
    USING (app_private.is_member(id));

CREATE POLICY membership_self_or_admin_read ON app.memberships FOR SELECT TO authenticated
    USING (user_id=(SELECT auth.uid()) OR app_private.is_admin(organization_id));

CREATE POLICY published_or_admin_course_read ON app.courses FOR SELECT TO authenticated
    USING (
        app_private.is_member(organization_id)
        AND (status='published' OR app_private.is_admin(organization_id))
    );

CREATE POLICY published_or_admin_version_read ON app.course_versions FOR SELECT TO authenticated
    USING (
        app_private.is_member(organization_id)
        AND (
            app_private.is_admin(organization_id)
            OR (
                status='published'
                AND EXISTS (
                    SELECT 1 FROM app.courses c
                    WHERE c.organization_id=course_versions.organization_id
                      AND c.id=course_versions.course_id
                      AND c.status='published'
                )
            )
        )
    );

CREATE POLICY enrollment_self_or_admin_read ON app.enrollments FOR SELECT TO authenticated
    USING (
        app_private.is_member(organization_id)
        AND (user_id=(SELECT auth.uid()) OR app_private.is_admin(organization_id))
    );

CREATE POLICY attempt_self_or_admin_read ON app.learning_attempts FOR SELECT TO authenticated
    USING (
        app_private.is_member(organization_id)
        AND (user_id=(SELECT auth.uid()) OR app_private.is_admin(organization_id))
    );

CREATE POLICY agent_run_self_or_admin_read ON app.agent_runs FOR SELECT TO authenticated
    USING (
        app_private.is_member(organization_id)
        AND (user_id=(SELECT auth.uid()) OR app_private.is_admin(organization_id))
    );

-- No authenticated DML grants. No financial RLS read policies.
-- A backend service role must be restricted and its privileges audited.
COMMIT;
