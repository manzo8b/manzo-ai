-- MANZO AI SaaS database isolation smoke test.
-- Run after 000_auth_fixture.sql and 0001_foundation.sql in ephemeral PostgreSQL.
-- Every assertion raises an error, causing CI to fail.
\set ON_ERROR_STOP on

-- Server-owned seed data (simulated trusted write path).
INSERT INTO app.organizations(id,name) VALUES
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','Organization A'),
 ('bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb','Organization B');

INSERT INTO app.memberships(organization_id,user_id,role) VALUES
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','11111111-1111-4111-8111-111111111111','owner'),
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','22222222-2222-4222-8222-222222222222','learner'),
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','44444444-4444-4444-8444-444444444444','learner'),
 ('bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb','33333333-3333-4333-8333-333333333333','learner');

INSERT INTO app.courses(id,organization_id,slug,title,status) VALUES
 ('cccccccc-cccc-4ccc-8ccc-ccccccccccca','aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','hallucinations','Hallucinations and verification','published'),
 ('cccccccc-cccc-4ccc-8ccc-cccccccccccd','aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','internal-draft','Internal course','draft'),
 ('cccccccc-cccc-4ccc-8ccc-cccccccccccb','bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb','security','Tenant B private course','published');

INSERT INTO app.course_versions(id,organization_id,course_id,version_number,status,content_ref,published_at) VALUES
 ('dddddddd-dddd-4ddd-8ddd-ddddddddddda','aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','cccccccc-cccc-4ccc-8ccc-ccccccccccca',1,'published','content/course/a/1',now()),
 ('dddddddd-dddd-4ddd-8ddd-dddddddddddd','aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','cccccccc-cccc-4ccc-8ccc-cccccccccccd',1,'draft','content/course/a-draft/1',NULL),
 ('dddddddd-dddd-4ddd-8ddd-dddddddddddb','bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb','cccccccc-cccc-4ccc-8ccc-cccccccccccb',1,'published','content/course/b/1',now());

INSERT INTO app.enrollments(organization_id,course_id,user_id) VALUES
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','cccccccc-cccc-4ccc-8ccc-ccccccccccca','22222222-2222-4222-8222-222222222222'),
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','cccccccc-cccc-4ccc-8ccc-ccccccccccca','44444444-4444-4444-8444-444444444444'),
 ('bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb','cccccccc-cccc-4ccc-8ccc-cccccccccccb','33333333-3333-4333-8333-333333333333');

INSERT INTO app.learning_attempts(organization_id,course_id,user_id,version_id,assessment_id,score_percent) VALUES
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','cccccccc-cccc-4ccc-8ccc-ccccccccccca','22222222-2222-4222-8222-222222222222','dddddddd-dddd-4ddd-8ddd-ddddddddddda','quiz',82),
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','cccccccc-cccc-4ccc-8ccc-ccccccccccca','44444444-4444-4444-8444-444444444444','dddddddd-dddd-4ddd-8ddd-ddddddddddda','quiz',94),
 ('bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb','cccccccc-cccc-4ccc-8ccc-cccccccccccb','33333333-3333-4333-8333-333333333333','dddddddd-dddd-4ddd-8ddd-dddddddddddb','quiz',75);

INSERT INTO app.agent_runs(organization_id,user_id,feature,state) VALUES
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','22222222-2222-4222-8222-222222222222','verify.process','queued'),
 ('bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb','33333333-3333-4333-8333-333333333333','studio.generate','needs_review');

INSERT INTO app_private.feature_grants(organization_id,feature,status,valid_until,quota) VALUES
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','verify.process','active',now()+interval '30 days',100);
INSERT INTO app_private.feature_usage(organization_id,feature,consumed) VALUES
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','verify.process',3);

-- Licensed learners get course content; unlicensed members get catalog only.
INSERT INTO app_private.feature_grants(organization_id,feature,status,valid_until,quota) VALUES
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','learning.seats','active',now()+interval '30 days',1),
 ('bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb','learning.seats','active',now()+interval '30 days',1);
INSERT INTO app_private.learning_seats(organization_id,user_id) VALUES
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','22222222-2222-4222-8222-222222222222'),
 ('bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb','33333333-3333-4333-8333-333333333333');

-- Idempotent provider event receipt: one logical event may be retried.
INSERT INTO app_private.billing_events(provider,provider_event_id,event_type)
VALUES ('stripe','evt_test_duplicate_123','checkout.session.completed')
ON CONFLICT DO NOTHING;
INSERT INTO app_private.billing_events(provider,provider_event_id,event_type)
VALUES ('stripe','evt_test_duplicate_123','checkout.session.completed')
ON CONFLICT DO NOTHING;

DO $assert$
BEGIN
 IF (SELECT count(*) FROM app_private.billing_events WHERE provider_event_id='evt_test_duplicate_123') <> 1 THEN
   RAISE EXCEPTION 'Webhook idempotency uniqueness failed';
 END IF;
 IF NOT has_table_privilege('service_role','app_private.billing_events','INSERT') THEN
   RAISE EXCEPTION 'Trusted service cannot write billing events';
 END IF;
 IF NOT has_table_privilege('service_role','app_private.feature_grants','UPDATE') THEN
   RAISE EXCEPTION 'Trusted service cannot manage grants';
 END IF;
 -- DB integrity: a record may not refer to a course version from another course.
 BEGIN
  INSERT INTO app.learning_attempts(organization_id,course_id,user_id,version_id,assessment_id)
  VALUES (
   'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
   'cccccccc-cccc-4ccc-8ccc-ccccccccccca',
   '22222222-2222-4222-8222-222222222222',
   'dddddddd-dddd-4ddd-8ddd-dddddddddddd',
   'wrong-version'
  );
  RAISE EXCEPTION 'Cross-course version insertion wrongly allowed';
 EXCEPTION WHEN foreign_key_violation THEN NULL;
 END;
END
$assert$;

-- Simulate a verified JWT belonging to learner in tenant A.
SET ROLE authenticated;
SET request.jwt.claim.sub = '22222222-2222-4222-8222-222222222222';

DO $assert$
BEGIN
 IF (SELECT count(*) FROM app.organizations) <> 1 THEN RAISE EXCEPTION 'Learner can see foreign organization'; END IF;
 IF (SELECT count(*) FROM app.memberships) <> 1 THEN RAISE EXCEPTION 'Learner can see another membership'; END IF;
 IF (SELECT count(*) FROM app.courses) <> 1 THEN RAISE EXCEPTION 'Learner can read draft or foreign course'; END IF;
 IF (SELECT count(*) FROM app.course_versions) <> 1 THEN RAISE EXCEPTION 'Learner can read draft/foreign version'; END IF;
 IF (SELECT count(*) FROM app.enrollments) <> 1 THEN RAISE EXCEPTION 'Learner can see other enrollment'; END IF;
 IF (SELECT count(*) FROM app.learning_attempts) <> 1 THEN RAISE EXCEPTION 'Learner can see other learner scores'; END IF;
 IF (SELECT count(*) FROM app.agent_runs) <> 1 THEN RAISE EXCEPTION 'Learner can see foreign agent run'; END IF;
 IF has_table_privilege(current_user,'app.courses','INSERT') THEN RAISE EXCEPTION 'Untrusted client can add course'; END IF;
 IF has_table_privilege(current_user,'app.learning_attempts','INSERT') THEN RAISE EXCEPTION 'Untrusted client can forge attempt'; END IF;
 IF has_table_privilege(current_user,'app.memberships','UPDATE') THEN RAISE EXCEPTION 'Untrusted client can elevate role'; END IF;
 IF has_table_privilege(current_user,'app_private.feature_grants','SELECT') THEN RAISE EXCEPTION 'Private grants exposed to client'; END IF;
 IF has_table_privilege(current_user,'app_private.billing_events','INSERT') THEN RAISE EXCEPTION 'Client can forge webhook event'; END IF;
END
$assert$;

-- Impersonation to B's real member: all A records must disappear.
SET request.jwt.claim.sub = '33333333-3333-4333-8333-333333333333';
DO $assert$
BEGIN
 IF (SELECT count(*) FROM app.organizations) <> 1 THEN RAISE EXCEPTION 'Tenant B org scope'; END IF;
 IF (SELECT count(*) FROM app.courses WHERE organization_id='aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa') <> 0 THEN
    RAISE EXCEPTION 'Tenant B can see tenant A courses';
 END IF;
 IF (SELECT count(*) FROM app.learning_attempts WHERE organization_id='aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa') <> 0 THEN
    RAISE EXCEPTION 'Tenant B can see tenant A results';
 END IF;
END
$assert$;

-- Owner in A can read its draft and its student progress, but NOT tenant B.
SET request.jwt.claim.sub = '11111111-1111-4111-8111-111111111111';
DO $assert$
BEGIN
 IF (SELECT count(*) FROM app.courses) <> 2 THEN RAISE EXCEPTION 'Owner cannot see own drafts or sees tenant B'; END IF;
 IF (SELECT count(*) FROM app.course_versions) <> 2 THEN RAISE EXCEPTION 'Owner sees wrong versions'; END IF;
 IF (SELECT count(*) FROM app.learning_attempts) <> 2 THEN RAISE EXCEPTION 'Owner sees wrong attempts'; END IF;
 IF (SELECT count(*) FROM app.memberships) <> 3 THEN RAISE EXCEPTION 'Owner cannot list own tenant members'; END IF;
END
$assert$;

-- Anonymous (no JWT subject) can read no tenant data, despite authenticated role.
RESET request.jwt.claim.sub;
DO $assert$
BEGIN
 IF (SELECT count(*) FROM app.organizations) <> 0 THEN RAISE EXCEPTION 'No JWT subject: org leak'; END IF;
 IF (SELECT count(*) FROM app.courses) <> 0 THEN RAISE EXCEPTION 'No JWT subject: course leak'; END IF;
END
$assert$;

RESET ROLE;
SELECT 'PASS: 2 tenants isolated, scores private, drafts restricted, no client writes, billing private, duplicate event safe, composite FK valid' AS result;
