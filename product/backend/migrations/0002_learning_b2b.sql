-- MANZO AI · Learning B2B, migration 0002
-- NOT applied to any real project. PostgreSQL 16 tests are ephemeral.
-- All mutations require trusted service_role; authenticated users have SELECT only.
BEGIN;

-- Seats are per tenant/member, not per enrolled course.
CREATE TABLE app_private.learning_seats (
  organization_id uuid NOT NULL,
  user_id uuid NOT NULL,
  assigned_at timestamptz NOT NULL DEFAULT now(),
  released_at timestamptz,
  PRIMARY KEY (organization_id,user_id),
  FOREIGN KEY (organization_id,user_id)
    REFERENCES app.memberships(organization_id,user_id) ON DELETE CASCADE,
  CHECK (released_at IS NULL OR released_at >= assigned_at)
);

CREATE TABLE app_private.learning_modules (
  organization_id uuid NOT NULL,
  course_id uuid NOT NULL,
  version_id uuid NOT NULL,
  module_key text NOT NULL CHECK (module_key ~ '^[a-zA-Z0-9_.-]{1,100}$'),
  sort_order int NOT NULL CHECK (sort_order > 0),
  PRIMARY KEY (organization_id,course_id,version_id,module_key),
  FOREIGN KEY (organization_id,course_id,version_id)
    REFERENCES app.course_versions(organization_id,course_id,id) ON DELETE CASCADE,
  UNIQUE (organization_id,course_id,version_id,sort_order)
);

-- Correct answers never enter public learning/course_version records.
CREATE TABLE app_private.assessment_items (
  organization_id uuid NOT NULL,
  course_id uuid NOT NULL,
  version_id uuid NOT NULL,
  assessment_id text NOT NULL CHECK (length(trim(assessment_id)) BETWEEN 1 AND 160),
  question_id text NOT NULL CHECK (length(trim(question_id)) BETWEEN 1 AND 160),
  allowed_options text[] NOT NULL CHECK (cardinality(allowed_options) BETWEEN 2 AND 20),
  correct_option text NOT NULL,
  PRIMARY KEY (organization_id,course_id,version_id,assessment_id,question_id),
  FOREIGN KEY (organization_id,course_id,version_id)
    REFERENCES app.course_versions(organization_id,course_id,id) ON DELETE CASCADE,
  CHECK (correct_option=ANY(allowed_options))
);

CREATE TABLE app.learning_progress (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL,
  course_id uuid NOT NULL,
  version_id uuid NOT NULL,
  user_id uuid NOT NULL,
  module_key text NOT NULL,
  completed_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (organization_id,course_id,version_id,user_id,module_key),
  FOREIGN KEY (organization_id,course_id,user_id)
    REFERENCES app.enrollments(organization_id,course_id,user_id) ON DELETE CASCADE,
  FOREIGN KEY (organization_id,course_id,version_id,module_key)
    REFERENCES app_private.learning_modules(organization_id,course_id,version_id,module_key)
);

-- Minimal append-only evidence for privileged learning changes.
CREATE TABLE app_private.learning_audit_events (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  organization_id uuid NOT NULL REFERENCES app.organizations(id),
  actor_user_id uuid NOT NULL REFERENCES auth.users(id),
  subject_user_id uuid NOT NULL REFERENCES auth.users(id),
  event_type text NOT NULL CHECK (event_type IN (
    'seat_assigned','seat_released','student_enrolled','module_completed','assessment_recorded'
  )),
  related_id uuid,
  occurred_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_learning_progress_user
  ON app.learning_progress(organization_id,user_id,course_id,completed_at DESC);
CREATE INDEX idx_learning_seats_active
  ON app_private.learning_seats(organization_id) WHERE released_at IS NULL;
CREATE INDEX idx_learning_audit_org
  ON app_private.learning_audit_events(organization_id,occurred_at DESC);

ALTER TABLE app_private.learning_seats ENABLE ROW LEVEL SECURITY;
ALTER TABLE app_private.learning_seats FORCE ROW LEVEL SECURITY;
ALTER TABLE app_private.learning_modules ENABLE ROW LEVEL SECURITY;
ALTER TABLE app_private.learning_modules FORCE ROW LEVEL SECURITY;
ALTER TABLE app_private.assessment_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE app_private.assessment_items FORCE ROW LEVEL SECURITY;
ALTER TABLE app_private.learning_audit_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE app_private.learning_audit_events FORCE ROW LEVEL SECURITY;
ALTER TABLE app.learning_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE app.learning_progress FORCE ROW LEVEL SECURITY;

GRANT SELECT,INSERT,UPDATE,DELETE ON
 app_private.learning_seats,app_private.learning_modules,
 app_private.assessment_items,app.learning_progress
TO service_role;
GRANT SELECT,INSERT ON app_private.learning_audit_events TO service_role;
GRANT USAGE,SELECT ON SEQUENCE app_private.learning_audit_events_id_seq TO service_role;
GRANT SELECT ON app.learning_progress TO authenticated;
CREATE POLICY progress_self_or_admin_read ON app.learning_progress FOR SELECT TO authenticated
 USING (
   app_private.is_member(organization_id)
   AND (user_id=(SELECT auth.uid()) OR app_private.is_admin(organization_id))
 );

-- Security definer: may only answer whether the VERIFIED session's member
-- has a currently valid seat. Does not return grant details or other users.
CREATE FUNCTION app_private.has_learning_access(p_organization_id uuid)
RETURNS boolean
LANGUAGE sql STABLE SECURITY DEFINER SET search_path=''
AS $fn$
 SELECT EXISTS (
  SELECT 1
  FROM app.memberships m
  JOIN app_private.learning_seats s
    ON s.organization_id=m.organization_id AND s.user_id=m.user_id
  JOIN app_private.feature_grants g
    ON g.organization_id=m.organization_id
   AND g.feature='learning.seats'
  WHERE m.organization_id=p_organization_id
    AND m.user_id=(SELECT auth.uid())
    AND m.status='active'
    AND s.released_at IS NULL
    AND g.status='active'
    AND g.valid_until > now()
 )
$fn$;
REVOKE ALL ON FUNCTION app_private.has_learning_access(uuid) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION app_private.has_learning_access(uuid) TO authenticated;

-- Harden course material visibility: membership alone is NOT a paid license.
-- Admins can maintain drafts; learners only access published versions
-- when an active seat AND the organization's grant are both valid.
DROP POLICY published_or_admin_version_read ON app.course_versions;
CREATE POLICY published_or_admin_version_read ON app.course_versions
 FOR SELECT TO authenticated
 USING (
  app_private.is_member(organization_id)
  AND (
    app_private.is_admin(organization_id)
    OR (
      status='published'
      AND app_private.has_learning_access(organization_id)
      AND EXISTS (
        SELECT 1 FROM app.courses c
        WHERE c.organization_id=course_versions.organization_id
          AND c.id=course_versions.course_id
          AND c.status='published'
      )
    )
  )
 );

-- Mutations are SECURITY INVOKER, NOT SECURITY DEFINER.
-- They require service_role's private-table privileges and a verified
-- actor identity supplied by the trusted backend (never user-controlled).
CREATE FUNCTION app_private.assign_learning_seat(
 p_actor uuid, p_org uuid, p_student uuid
) RETURNS text LANGUAGE plpgsql VOLATILE SECURITY INVOKER SET search_path=''
AS $fn$
DECLARE
 v_grant app_private.feature_grants%ROWTYPE;
 v_existing boolean;
 v_active bigint;
BEGIN
 IF NOT EXISTS (
  SELECT 1 FROM app.memberships
  WHERE organization_id=p_org AND user_id=p_actor
    AND role IN ('owner','admin') AND status='active'
 ) THEN RAISE EXCEPTION 'LEARNING_NOT_ADMIN' USING ERRCODE='P0001'; END IF;
 IF NOT EXISTS (
  SELECT 1 FROM app.memberships
  WHERE organization_id=p_org AND user_id=p_student AND status='active'
 ) THEN RAISE EXCEPTION 'LEARNING_STUDENT_NOT_MEMBER' USING ERRCODE='P0001'; END IF;

 -- Row lock serializes seat assignment for a given organization, ensuring
 -- concurrent requests cannot exceed the grant's seat count.
 SELECT * INTO v_grant FROM app_private.feature_grants
 WHERE organization_id=p_org AND feature='learning.seats' FOR UPDATE;
 IF NOT FOUND OR v_grant.status<>'active' OR v_grant.valid_until<=now()
 THEN RAISE EXCEPTION 'LEARNING_LICENSE_INACTIVE' USING ERRCODE='P0001'; END IF;

 SELECT EXISTS(
   SELECT 1 FROM app_private.learning_seats
    WHERE organization_id=p_org AND user_id=p_student AND released_at IS NULL
 ) INTO v_existing;
 IF v_existing THEN RETURN 'already_assigned'; END IF;

 SELECT count(*) INTO v_active FROM app_private.learning_seats
 WHERE organization_id=p_org AND released_at IS NULL;
 IF v_active>=v_grant.quota
 THEN RAISE EXCEPTION 'LEARNING_NO_SEATS' USING ERRCODE='P0001'; END IF;

 INSERT INTO app_private.learning_seats (organization_id,user_id)
 VALUES (p_org,p_student)
 ON CONFLICT (organization_id,user_id)
 DO UPDATE SET assigned_at=now(),released_at=NULL;

 INSERT INTO app_private.learning_audit_events
 (organization_id,actor_user_id,subject_user_id,event_type)
 VALUES (p_org,p_actor,p_student,'seat_assigned');
 RETURN 'assigned';
END;
$fn$;

CREATE FUNCTION app_private.release_learning_seat(
 p_actor uuid,p_org uuid,p_student uuid
) RETURNS text LANGUAGE plpgsql VOLATILE SECURITY INVOKER SET search_path=''
AS $fn$
DECLARE v_grant app_private.feature_grants%ROWTYPE;
BEGIN
 IF NOT EXISTS (
  SELECT 1 FROM app.memberships WHERE organization_id=p_org
  AND user_id=p_actor AND role IN ('owner','admin') AND status='active'
 ) THEN RAISE EXCEPTION 'LEARNING_NOT_ADMIN' USING ERRCODE='P0001'; END IF;
 -- Lock serializes release with any concurrent assignment.
 SELECT * INTO v_grant FROM app_private.feature_grants
 WHERE organization_id=p_org AND feature='learning.seats' FOR UPDATE;
 IF NOT FOUND THEN RAISE EXCEPTION 'LEARNING_LICENSE_MISSING' USING ERRCODE='P0001'; END IF;

 UPDATE app_private.learning_seats SET released_at=now()
 WHERE organization_id=p_org AND user_id=p_student AND released_at IS NULL;
 IF NOT FOUND THEN RETURN 'not_assigned'; END IF;
 UPDATE app.enrollments SET status='revoked'
 WHERE organization_id=p_org AND user_id=p_student AND status='active';
 INSERT INTO app_private.learning_audit_events
 (organization_id,actor_user_id,subject_user_id,event_type)
 VALUES (p_org,p_actor,p_student,'seat_released');
 RETURN 'released';
END;
$fn$;

CREATE FUNCTION app_private.enroll_learning_student(
 p_actor uuid,p_org uuid,p_student uuid,p_course uuid
) RETURNS uuid LANGUAGE plpgsql VOLATILE SECURITY INVOKER SET search_path=''
AS $fn$
DECLARE v_id uuid;
BEGIN
 IF NOT EXISTS (
   SELECT 1 FROM app.memberships WHERE organization_id=p_org AND user_id=p_actor
     AND role IN ('owner','admin','instructor') AND status='active'
 ) THEN RAISE EXCEPTION 'LEARNING_NOT_INSTRUCTOR' USING ERRCODE='P0001'; END IF;
 IF NOT EXISTS (
   SELECT 1 FROM app_private.learning_seats s
   JOIN app_private.feature_grants g ON g.organization_id=s.organization_id
     AND g.feature='learning.seats'
   JOIN app.memberships m ON m.organization_id=s.organization_id AND m.user_id=s.user_id
   WHERE s.organization_id=p_org AND s.user_id=p_student
     AND s.released_at IS NULL AND m.status='active'
     AND g.status='active' AND g.valid_until>now()
 ) THEN RAISE EXCEPTION 'LEARNING_STUDENT_UNLICENSED' USING ERRCODE='P0001'; END IF;
 IF NOT EXISTS (
   SELECT 1 FROM app.courses WHERE organization_id=p_org
     AND id=p_course AND status='published'
 ) THEN RAISE EXCEPTION 'LEARNING_COURSE_UNAVAILABLE' USING ERRCODE='P0001'; END IF;
 INSERT INTO app.enrollments(organization_id,course_id,user_id,status)
 VALUES(p_org,p_course,p_student,'active')
 ON CONFLICT(organization_id,course_id,user_id)
 DO UPDATE SET status='active' RETURNING id INTO v_id;
 INSERT INTO app_private.learning_audit_events
 (organization_id,actor_user_id,subject_user_id,event_type,related_id)
 VALUES(p_org,p_actor,p_student,'student_enrolled',p_course);
 RETURN v_id;
END;
$fn$;

-- Student identity is always the verified actor. Course, version and module
-- must belong to the same org and be published; no arbitrary progress claims.
CREATE FUNCTION app_private.complete_learning_module(
 p_actor uuid,p_org uuid,p_course uuid,p_version uuid,p_module text
) RETURNS uuid LANGUAGE plpgsql VOLATILE SECURITY INVOKER SET search_path=''
AS $fn$
DECLARE v_id uuid;
BEGIN
 IF NOT EXISTS (
   SELECT 1 FROM app.memberships m
   JOIN app_private.learning_seats s ON s.organization_id=m.organization_id AND s.user_id=m.user_id
   JOIN app_private.feature_grants g ON g.organization_id=m.organization_id AND g.feature='learning.seats'
   JOIN app.enrollments e ON e.organization_id=m.organization_id
     AND e.user_id=m.user_id AND e.course_id=p_course
   JOIN app.course_versions v ON v.organization_id=m.organization_id
     AND v.course_id=p_course AND v.id=p_version
   JOIN app.courses c ON c.organization_id=m.organization_id AND c.id=p_course
   JOIN app_private.learning_modules lm ON lm.organization_id=m.organization_id
     AND lm.course_id=p_course AND lm.version_id=p_version AND lm.module_key=p_module
   WHERE m.organization_id=p_org AND m.user_id=p_actor AND m.status='active'
     AND s.released_at IS NULL AND g.status='active' AND g.valid_until>now()
     AND e.status='active' AND v.status='published' AND c.status='published'
 ) THEN RAISE EXCEPTION 'LEARNING_MODULE_UNAVAILABLE' USING ERRCODE='P0001'; END IF;

 INSERT INTO app.learning_progress
 (organization_id,course_id,version_id,user_id,module_key)
 VALUES(p_org,p_course,p_version,p_actor,p_module)
 ON CONFLICT (organization_id,course_id,version_id,user_id,module_key)
 DO NOTHING RETURNING id INTO v_id;
 IF v_id IS NULL THEN
   SELECT id INTO v_id FROM app.learning_progress
   WHERE organization_id=p_org AND course_id=p_course AND version_id=p_version
     AND user_id=p_actor AND module_key=p_module;
 ELSE
   INSERT INTO app_private.learning_audit_events
   (organization_id,actor_user_id,subject_user_id,event_type,related_id)
   VALUES(p_org,p_actor,p_actor,'module_completed',v_id);
 END IF;
 RETURN v_id;
END;
$fn$;

-- Answer key is accessible to service_role only. Payload contains option IDs,
-- never client-provided score, and must provide exactly one allowed selection
-- per approved question in this assessment/version.
CREATE FUNCTION app_private.record_learning_assessment(
 p_actor uuid,p_org uuid,p_course uuid,p_version uuid,
 p_assessment text,p_answers jsonb
) RETURNS uuid LANGUAGE plpgsql VOLATILE SECURITY INVOKER SET search_path=''
AS $fn$
DECLARE v_id uuid; v_count bigint; v_supplied bigint; v_correct bigint; v_valid boolean;
BEGIN
 IF jsonb_typeof(p_answers) IS DISTINCT FROM 'object'
 THEN RAISE EXCEPTION 'LEARNING_INVALID_ANSWERS' USING ERRCODE='P0001'; END IF;
 IF NOT EXISTS (
   SELECT 1 FROM app.memberships m
   JOIN app_private.learning_seats s ON s.organization_id=m.organization_id AND s.user_id=m.user_id
   JOIN app_private.feature_grants g ON g.organization_id=m.organization_id AND g.feature='learning.seats'
   JOIN app.enrollments e ON e.organization_id=m.organization_id
     AND e.user_id=m.user_id AND e.course_id=p_course
   JOIN app.course_versions v ON v.organization_id=m.organization_id
     AND v.course_id=p_course AND v.id=p_version
   JOIN app.courses c ON c.organization_id=m.organization_id AND c.id=p_course
   WHERE m.organization_id=p_org AND m.user_id=p_actor AND m.status='active'
     AND s.released_at IS NULL AND g.status='active' AND g.valid_until>now()
     AND e.status='active' AND v.status='published' AND c.status='published'
 ) THEN RAISE EXCEPTION 'LEARNING_NOT_ENROLLED' USING ERRCODE='P0001'; END IF;

 SELECT count(*),
        count(*) FILTER (WHERE
          (p_answers->>question_id)=correct_option),
        coalesce(bool_and(
          p_answers ? question_id
          AND jsonb_typeof(p_answers->question_id)='string'
          AND (p_answers->>question_id)=ANY(allowed_options)
        ),false)
 INTO v_count,v_correct,v_valid
 FROM app_private.assessment_items
 WHERE organization_id=p_org AND course_id=p_course AND version_id=p_version
   AND assessment_id=p_assessment;
 SELECT count(*) INTO v_supplied FROM jsonb_object_keys(p_answers);
 IF v_count=0 OR v_count<>v_supplied OR NOT v_valid
 THEN RAISE EXCEPTION 'LEARNING_INVALID_ANSWERS' USING ERRCODE='P0001'; END IF;

 INSERT INTO app.learning_attempts
 (organization_id,course_id,user_id,version_id,assessment_id,score_percent)
 VALUES(p_org,p_course,p_actor,p_version,p_assessment,
        round((v_correct::numeric/v_count::numeric)*100)::integer)
 RETURNING id INTO v_id;
 INSERT INTO app_private.learning_audit_events
 (organization_id,actor_user_id,subject_user_id,event_type,related_id)
 VALUES(p_org,p_actor,p_actor,'assessment_recorded',v_id);
 RETURN v_id;
END;
$fn$;

-- PostgreSQL gives PUBLIC EXECUTE by default on new functions unless revoked.
-- Only the backend's trusted service_role may invoke mutation routines.
REVOKE ALL ON FUNCTION app_private.assign_learning_seat(uuid,uuid,uuid) FROM PUBLIC;
REVOKE ALL ON FUNCTION app_private.release_learning_seat(uuid,uuid,uuid) FROM PUBLIC;
REVOKE ALL ON FUNCTION app_private.enroll_learning_student(uuid,uuid,uuid,uuid) FROM PUBLIC;
REVOKE ALL ON FUNCTION app_private.complete_learning_module(uuid,uuid,uuid,uuid,text) FROM PUBLIC;
REVOKE ALL ON FUNCTION app_private.record_learning_assessment(uuid,uuid,uuid,uuid,text,jsonb) FROM PUBLIC;

GRANT EXECUTE ON FUNCTION app_private.assign_learning_seat(uuid,uuid,uuid) TO service_role;
GRANT EXECUTE ON FUNCTION app_private.release_learning_seat(uuid,uuid,uuid) TO service_role;
GRANT EXECUTE ON FUNCTION app_private.enroll_learning_student(uuid,uuid,uuid,uuid) TO service_role;
GRANT EXECUTE ON FUNCTION app_private.complete_learning_module(uuid,uuid,uuid,uuid,text) TO service_role;
GRANT EXECUTE ON FUNCTION app_private.record_learning_assessment(uuid,uuid,uuid,uuid,text,jsonb) TO service_role;

-- Default privileges should be reviewed independently on a real deployment.
-- No authenticated inserts/updates, no access to assessment keys or seat quotas.
COMMIT;
