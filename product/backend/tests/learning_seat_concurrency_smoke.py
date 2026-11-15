#!/usr/bin/env python3
"""Race test for an organization's last Learning seat.

Runs only inside the ephemeral PostgreSQL GitHub Actions database, AFTER
migrations and SQL assertions. Not for deployment on production databases.
Uses external psql processes so transactions genuinely overlap.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import os
import subprocess
import threading

ORG="eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee"
ADMIN="11111111-1111-4111-8111-111111111111"
MEMBERS=(
 "22222222-2222-4222-8222-222222222222",
 "44444444-4444-4444-8444-444444444444"
)


def psql(sql: str, *, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["psql","-X","-v","ON_ERROR_STOP=1","-A","-t","-c",sql],
        text=True,capture_output=True,check=check,timeout=20,
        env=os.environ.copy()
    )


psql(f"""
INSERT INTO app.organizations(id,name)
VALUES ('{ORG}','Concurrency Test Company');
INSERT INTO app.memberships(organization_id,user_id,role)
VALUES ('{ORG}','{ADMIN}','owner'),
       ('{ORG}','{MEMBERS[0]}','learner'),
       ('{ORG}','{MEMBERS[1]}','learner');
INSERT INTO app_private.feature_grants(organization_id,feature,status,valid_until,quota)
VALUES ('{ORG}','learning.seats','active',now()+interval '2 days',1);
""")

barrier=threading.Barrier(2)


def competing_request(member: str) -> subprocess.CompletedProcess:
    barrier.wait(timeout=10)
    return psql(
      f"SET ROLE service_role; SELECT app_private.assign_learning_seat("
      f"'{ADMIN}'::uuid,'{ORG}'::uuid,'{member}'::uuid);",
      check=False
    )

with ThreadPoolExecutor(max_workers=2) as pool:
    futures=[pool.submit(competing_request,user) for user in MEMBERS]
    results=[future.result(timeout=30) for future in futures]

success=[x for x in results if x.returncode==0 and "assigned" in x.stdout]
denied=[x for x in results if x.returncode!=0 and "LEARNING_NO_SEATS" in x.stderr]
if len(success)!=1 or len(denied)!=1:
    raise AssertionError("Seat race permitted wrong results: "+repr([
       {"returncode":x.returncode,"out":x.stdout[-300:],"error":x.stderr[-300:]}
       for x in results
    ]))

counts=psql(f"""SELECT count(*) FROM app_private.learning_seats
WHERE organization_id='{ORG}' AND released_at IS NULL;""").stdout.strip()
audits=psql(f"""SELECT count(*) FROM app_private.learning_audit_events
WHERE organization_id='{ORG}' AND event_type='seat_assigned';""").stdout.strip()
if counts!="1" or audits!="1":
    raise AssertionError(f"Race outcomes inconsistent: seats={counts},audit={audits}")
print("PASS: 2 truly concurrent seat requests -> exactly 1 assignment and 1 quota rejection")
