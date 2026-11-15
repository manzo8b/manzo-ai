-- MANZO AI Learning B2B: actual PostgreSQL workflow tests
-- Requires 000_auth_fixture.sql, 0001_foundation.sql, 0002_learning_b2b.sql,
-- and 010_rls_checks.sql. These fixtures are NEVER production data.
\set ON_ERROR_STOP on

SET ROLE service_role;

-- Approved course material is seeded by a trusted instructor/backend only.
INSERT INTO app_private.learning_modules
 (organization_id,course_id,version_id,module_key,sort_order) VALUES
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','cccccccc-cccc-4ccc-8ccc-ccccccccccca',
  'dddddddd-dddd-4ddd-8ddd-ddddddddddda','intro',1),
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','cccccccc-cccc-4ccc-8ccc-ccccccccccca',
  'dddddddd-dddd-4ddd-8ddd-ddddddddddda','verification',2);

INSERT INTO app_private.assessment_items
 (organization_id,course_id,version_id,assessment_id,question_id,allowed_options,correct_option) VALUES
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','cccccccc-cccc-4ccc-8ccc-ccccccccccca',
  'dddddddd-dddd-4ddd-8ddd-ddddddddddda','quiz','q1',ARRAY['a','b','c'],'a'),
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','cccccccc-cccc-4ccc-8ccc-ccccccccccca',
  'dddddddd-dddd-4ddd-8ddd-ddddddddddda','quiz','q2',ARRAY['a','b','c'],'c');

DO $test$
DECLARE
 a constant uuid := 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa';
 b constant uuid := 'bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb';
 admin_a constant uuid := '11111111-1111-4111-8111-111111111111';
 learner_a constant uuid := '22222222-2222-4222-8222-222222222222';
 other_a constant uuid := '44444444-4444-4444-8444-444444444444';
 learner_b constant uuid := '33333333-3333-4333-8333-333333333333';
 course_a constant uuid := 'cccccccc-cccc-4ccc-8ccc-ccccccccccca';
 version_a constant uuid := 'dddddddd-dddd-4ddd-8ddd-ddddddddddda';
 version_draft constant uuid := 'dddddddd-dddd-4ddd-8ddd-dddddddddddd';
 v_progress uuid;
 v_repeated uuid;
 v_attempt uuid;
 v_enrollment uuid;
BEGIN
 -- One seat per learner across courses; repeat request does not consume seats.
 IF app_private.assign_learning_seat(admin_a,a,learner_a)<>'already_assigned'
 THEN RAISE EXCEPTION 'Expected idempotent seat assignment'; END IF;
 IF (SELECT count(*) FROM app_private.learning_seats
     WHERE organization_id=a AND released_at IS NULL)<>1
 THEN RAISE EXCEPTION 'Duplicate seat created'; END IF;

 -- Nobody can exceed the organization's server-controlled quota.
 BEGIN
  PERFORM app_private.assign_learning_seat(admin_a,a,other_a);
  RAISE EXCEPTION 'Quota bypass' USING ERRCODE='P0002';
 EXCEPTION WHEN SQLSTATE 'P0001' THEN NULL;
 END;

 -- Invalid actor cannot grant seats for a company where they are not admin.
 BEGIN
  PERFORM app_private.assign_learning_seat(learner_b,a,other_a);
  RAISE EXCEPTION 'Cross-tenant actor privilege bypass' USING ERRCODE='P0002';
 EXCEPTION WHEN SQLSTATE 'P0001' THEN NULL;
 END;

 -- Student enrollment is repeatable, but restricted to authorized instructors.
 v_enrollment:=app_private.enroll_learning_student(admin_a,a,learner_a,course_a);
 IF v_enrollment IS NULL OR
    app_private.enroll_learning_student(admin_a,a,learner_a,course_a)<>v_enrollment
 THEN RAISE EXCEPTION 'Enrollment idempotency failed'; END IF;
 BEGIN
  PERFORM app_private.enroll_learning_student(learner_a,a,other_a,course_a);
  RAISE EXCEPTION 'Learner could enroll others' USING ERRCODE='P0002';
 EXCEPTION WHEN SQLSTATE 'P0001' THEN NULL;
 END;

 -- Learner may complete only a module from an approved published version.
 v_progress:=app_private.complete_learning_module(learner_a,a,course_a,version_a,'intro');
 v_repeated:=app_private.complete_learning_module(learner_a,a,course_a,version_a,'intro');
 IF v_progress IS NULL OR v_repeated<>v_progress OR
    (SELECT count(*) FROM app.learning_progress
      WHERE organization_id=a AND user_id=learner_a AND module_key='intro')<>1
 THEN RAISE EXCEPTION 'Progress not persisted or not idempotent'; END IF;
 BEGIN
  PERFORM app_private.complete_learning_module(learner_a,a,course_a,version_a,'invented-module');
  RAISE EXCEPTION 'Invented module accepted' USING ERRCODE='P0002';
 EXCEPTION WHEN SQLSTATE 'P0001' THEN NULL;
 END;

 -- Correct options are private. Server derives 50% from one correct answer.
 v_attempt:=app_private.record_learning_assessment(
  learner_a,a,course_a,version_a,'quiz','{"q1":"a","q2":"b"}'::jsonb
 );
 IF v_attempt IS NULL OR
    (SELECT score_percent FROM app.learning_attempts WHERE id=v_attempt)<>50
 THEN RAISE EXCEPTION 'Server scoring did not yield 50 percent'; END IF;

 -- Unauthorized, incomplete or fabricated choices never create a result.
 BEGIN
  PERFORM app_private.record_learning_assessment(
   learner_a,a,course_a,version_a,'quiz','{"q1":"a"}'::jsonb);
  RAISE EXCEPTION 'Incomplete assessment accepted' USING ERRCODE='P0002';
 EXCEPTION WHEN SQLSTATE 'P0001' THEN NULL;
 END;
 BEGIN
  PERFORM app_private.record_learning_assessment(
   learner_a,a,course_a,version_a,'quiz','{"q1":"a","q2":"invented"}'::jsonb);
  RAISE EXCEPTION 'Invented option accepted' USING ERRCODE='P0002';
 EXCEPTION WHEN SQLSTATE 'P0001' THEN NULL;
 END;
 BEGIN
  PERFORM app_private.record_learning_assessment(
   learner_a,a,course_a,version_draft,'quiz','{"q1":"a","q2":"c"}'::jsonb);
  RAISE EXCEPTION 'Draft/cross-course version accepted' USING ERRCODE='P0002';
 EXCEPTION WHEN SQLSTATE 'P0001' THEN NULL;
 END;

 IF (SELECT count(*) FROM app.learning_attempts
     WHERE organization_id=a AND user_id=learner_a)<>2
 THEN RAISE EXCEPTION 'Invalid submissions were persisted'; END IF;
 IF (SELECT count(*) FROM app_private.learning_audit_events
     WHERE organization_id=a AND event_type='assessment_recorded')<>1
 THEN RAISE EXCEPTION 'Assessment audit trail incorrect'; END IF;

 -- Revocation immediately blocks the seat and revokes active enrollments.
 IF app_private.release_learning_seat(admin_a,a,learner_a)<>'released'
 THEN RAISE EXCEPTION 'Seat release failed'; END IF;
 IF app_private.release_learning_seat(admin_a,a,learner_a)<>'not_assigned'
 THEN RAISE EXCEPTION 'Repeat release not idempotent'; END IF;
 IF (SELECT status FROM app.enrollments WHERE id=v_enrollment)<>'revoked'
 THEN RAISE EXCEPTION 'Enrollment remained active after release'; END IF;
 BEGIN
  PERFORM app_private.complete_learning_module(learner_a,a,course_a,version_a,'verification');
  RAISE EXCEPTION 'Revoked student could complete module' USING ERRCODE='P0002';
 EXCEPTION WHEN SQLSTATE 'P0001' THEN NULL;
 END;
 BEGIN
  PERFORM app_private.record_learning_assessment(
   learner_a,a,course_a,version_a,'quiz','{"q1":"a","q2":"c"}'::jsonb);
  RAISE EXCEPTION 'Revoked student could submit assessment' USING ERRCODE='P0002';
 EXCEPTION WHEN SQLSTATE 'P0001' THEN NULL;
 END;

 -- Freed seat may be reassigned but tenant ownership is immutable.
 IF app_private.assign_learning_seat(admin_a,a,other_a)<>'assigned'
 THEN RAISE EXCEPTION 'Released seat not reusable'; END IF;
 IF app_private.enroll_learning_student(admin_a,a,other_a,course_a) IS NULL
 THEN RAISE EXCEPTION 'Newly licensed student not enrollable'; END IF;
 BEGIN
  PERFORM app_private.enroll_learning_student(admin_a,a,learner_b,course_a);
  RAISE EXCEPTION 'Cross-tenant student enrollment accepted' USING ERRCODE='P0002';
 EXCEPTION WHEN SQLSTATE 'P0001' THEN NULL;
 END;
 IF (SELECT count(*) FROM app_private.learning_seats
     WHERE organization_id=a AND released_at IS NULL)<>1
 THEN RAISE EXCEPTION 'Incorrect active seat count after reassignment'; END IF;
 IF (SELECT count(*) FROM app_private.learning_audit_events
     WHERE organization_id=a AND event_type='seat_assigned')<>1
 THEN RAISE EXCEPTION 'Seat assignment auditing incorrect'; END IF;
END
$test$;

-- Never expose assessment answer keys, seat assignments or mutation routines
-- to student sessions. Historical progress can remain visible to its owner.
SET ROLE authenticated;
SET request.jwt.claim.sub='22222222-2222-4222-8222-222222222222';
DO $test$
BEGIN
 IF (SELECT count(*) FROM app.course_versions)<>0
 THEN RAISE EXCEPTION 'Released learner can still read licensed course content'; END IF;
 IF (SELECT count(*) FROM app.learning_progress)<>1
 THEN RAISE EXCEPTION 'Released learner cannot see own historical progress'; END IF;
 IF has_table_privilege(current_user,'app_private.assessment_items','SELECT')
 THEN RAISE EXCEPTION 'Answer keys exposed'; END IF;
 IF has_table_privilege(current_user,'app_private.learning_seats','SELECT')
 THEN RAISE EXCEPTION 'Seat assignments exposed'; END IF;
 IF has_table_privilege(current_user,'app.learning_progress','INSERT')
 THEN RAISE EXCEPTION 'Learner can forge progress'; END IF;
 IF has_function_privilege(current_user,'app_private.record_learning_assessment(uuid,uuid,uuid,uuid,text,jsonb)','EXECUTE')
 THEN RAISE EXCEPTION 'Learner can directly forge assessment'; END IF;
 IF has_function_privilege(current_user,'app_private.assign_learning_seat(uuid,uuid,uuid)','EXECUTE')
 THEN RAISE EXCEPTION 'Learner can directly assign seats'; END IF;
END
$test$;

SET request.jwt.claim.sub='44444444-4444-4444-8444-444444444444';
DO $test$
BEGIN
 IF (SELECT count(*) FROM app.course_versions)<>1
 THEN RAISE EXCEPTION 'Licensed replacement cannot read published course'; END IF;
 IF (SELECT count(*) FROM app.learning_attempts)<>1
 THEN RAISE EXCEPTION 'Student can read other student scores'; END IF;
END
$test$;

SET request.jwt.claim.sub='33333333-3333-4333-8333-333333333333';
DO $test$
BEGIN
 IF (SELECT count(*) FROM app.learning_progress WHERE organization_id='aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa')<>0
 THEN RAISE EXCEPTION 'Foreign tenant learning progress exposed'; END IF;
END
$test$;
RESET ROLE;

SELECT 'PASS Learning B2B: seat limits, reallocation, instructor authority, enrollments, server scoring, progress, RLS and audit' AS result;
