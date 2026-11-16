#!/usr/bin/env python3
"""MANZO AI M3 — deterministic, SQL-only catalog importer.

Build a PostgreSQL transaction from the M2 SOURCE files (never from user input).
Default mode is ROLLBACK: the test leaves no persistent rows.
Commit mode is *only* for an isolated disposable CI database and requires an
explicit environment marker plus an acknowledgement CLI flag.

Never connects to Supabase, applies DDL, modifies Auth, or uploads assets.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re

from jsonschema import Draft202012Validator
from build_catalog import build_catalog

REPO = Path(__file__).resolve().parents[2]
M2_SCHEMA = Path(__file__).with_name("content-catalog.schema.json")
DDL = REPO / "product/backend/migrations/0004_public_catalog_m3.sql"


def make_sql(root: Path, revision: str, mode: str = "rollback") -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("source_revision must be a full 40-character git SHA")
    if mode not in ("rollback", "commit"):
        raise ValueError("invalid mode")
    catalog = build_catalog(root)
    schema = json.loads((root / "product/migration/content-catalog.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(catalog)
    payload = json.dumps(catalog, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    manifest_sha = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    # Safe dollar quotes: input is validated against a strict whitelist of keys,
    # but we also guarantee the chosen SQL delimiter cannot occur in the payload.
    delim = "$manzo_m3_payload$"
    if delim in payload:
        raise ValueError("unsafe delimiter in metadata payload")
    doc = f"{delim}{payload}{delim}::jsonb"
    return f"""-- GENERATED M3 IMPORT; never edit by hand; metadata-only.
-- Revision: {revision}
-- Canonical JSON SHA-256: {manifest_sha}
-- Mode: {mode.upper()}; Git source of truth; no quiz answers or private users.
\\set ON_ERROR_STOP on
BEGIN;
SET LOCAL lock_timeout = '3s';
SET LOCAL statement_timeout = '30s';

CREATE TEMP TABLE _manzo_m3_doc(doc jsonb NOT NULL) ON COMMIT DROP;
INSERT INTO _manzo_m3_doc(doc) VALUES ({doc});

-- Reject payloads that are not the intentionally limited M2 contract.
DO $manzo_validation$
DECLARE payload jsonb;
BEGIN
  SELECT doc INTO STRICT payload FROM _manzo_m3_doc;
  IF payload->>'scope' IS DISTINCT FROM 'editorial_public_metadata_only'
     OR payload->>'schema_version' IS DISTINCT FROM '1.0'
     OR (payload->'content_policy'->>'quiz_answers_exported')::boolean IS DISTINCT FROM false
     OR (payload->'content_policy'->>'progress_exported')::boolean IS DISTINCT FROM false
     OR (payload->'summary'->>'courses')::integer IS DISTINCT FROM 2
     OR (payload->'summary'->>'localized_variants')::integer IS DISTINCT FROM 6
     OR (payload->'summary'->>'localized_units')::integer IS DISTINCT FROM 36
  THEN RAISE EXCEPTION 'm3_catalog_contract_rejected'; END IF;
END
$manzo_validation$;

INSERT INTO content_public.catalog_courses
  (course_key, mode, canonical_locale, b2b_enrollment_enabled, b2b_grading_enabled)
SELECT c->>'key', c->>'mode', c->>'canonical_locale',
       (c->>'b2b_enrollment_enabled')::boolean,
       (c->>'b2b_grading_enabled')::boolean
FROM _manzo_m3_doc p CROSS JOIN LATERAL jsonb_array_elements(p.doc->'courses') AS c
ON CONFLICT (course_key) DO UPDATE
SET mode = EXCLUDED.mode, canonical_locale = EXCLUDED.canonical_locale,
    b2b_enrollment_enabled = EXCLUDED.b2b_enrollment_enabled,
    b2b_grading_enabled = EXCLUDED.b2b_grading_enabled,
    updated_at = now()
WHERE (catalog_courses.mode, catalog_courses.canonical_locale,
       catalog_courses.b2b_enrollment_enabled, catalog_courses.b2b_grading_enabled)
IS DISTINCT FROM
      (EXCLUDED.mode, EXCLUDED.canonical_locale,
       EXCLUDED.b2b_enrollment_enabled, EXCLUDED.b2b_grading_enabled);

INSERT INTO content_public.catalog_localizations
  (course_key, locale, title, route, source_path, source_sha256,
   editorial_status, unit_count, public_self_assessment_count,
   public_case_count, source_contains_public_answers, private_assessment_ready)
SELECT v->>'course_key', v->>'locale', v->>'title', v->>'route',
       v->>'source_path', v->>'source_sha256', v->>'editorial_status',
       (v->>'unit_count')::integer,
       (v->>'public_self_assessment_count')::integer,
       (v->>'public_case_count')::integer,
       (v->>'source_contains_public_answers')::boolean,
       (v->>'private_assessment_ready')::boolean
FROM _manzo_m3_doc p CROSS JOIN LATERAL jsonb_array_elements(p.doc->'variants') AS v
ON CONFLICT (course_key, locale) DO UPDATE
SET title=EXCLUDED.title, route=EXCLUDED.route,
    source_path=EXCLUDED.source_path, source_sha256=EXCLUDED.source_sha256,
    editorial_status=EXCLUDED.editorial_status,
    unit_count=EXCLUDED.unit_count,
    public_self_assessment_count=EXCLUDED.public_self_assessment_count,
    public_case_count=EXCLUDED.public_case_count,
    source_contains_public_answers=EXCLUDED.source_contains_public_answers,
    private_assessment_ready=EXCLUDED.private_assessment_ready,
    updated_at=now()
WHERE (catalog_localizations.title, catalog_localizations.route,
       catalog_localizations.source_path, catalog_localizations.source_sha256,
       catalog_localizations.editorial_status, catalog_localizations.unit_count,
       catalog_localizations.public_self_assessment_count,
       catalog_localizations.public_case_count,
       catalog_localizations.source_contains_public_answers,
       catalog_localizations.private_assessment_ready)
IS DISTINCT FROM
      (EXCLUDED.title, EXCLUDED.route,
       EXCLUDED.source_path, EXCLUDED.source_sha256,
       EXCLUDED.editorial_status, EXCLUDED.unit_count,
       EXCLUDED.public_self_assessment_count, EXCLUDED.public_case_count,
       EXCLUDED.source_contains_public_answers, EXCLUDED.private_assessment_ready);

INSERT INTO content_public.catalog_units
    (course_key, locale, unit_key, position, title, duration)
SELECT v->>'course_key', v->>'locale', u->>'key',
       (u->>'position')::integer, u->>'title', u->>'duration'
FROM _manzo_m3_doc p
CROSS JOIN LATERAL jsonb_array_elements(p.doc->'variants') AS v
CROSS JOIN LATERAL jsonb_array_elements(v->'units') AS u
ON CONFLICT (course_key, locale, unit_key) DO UPDATE
SET position=EXCLUDED.position, title=EXCLUDED.title, duration=EXCLUDED.duration
WHERE (catalog_units.position, catalog_units.title, catalog_units.duration)
IS DISTINCT FROM (EXCLUDED.position, EXCLUDED.title, EXCLUDED.duration);

INSERT INTO content_internal.import_runs
    (manifest_sha256, source_revision, schema_version, course_count,
     localization_count, unit_count)
VALUES ('{manifest_sha}', '{revision}', '1.0', 2, 6, 36)
ON CONFLICT (manifest_sha256) DO NOTHING;

-- Do not silently leave stale units if editorial content changes in the future.
DO $manzo_counts$
BEGIN
  IF (SELECT count(*) FROM content_public.catalog_courses
      WHERE course_key IN ('ai-hallucinations','engineering-assurance')) <> 2
     OR (SELECT count(*) FROM content_public.catalog_localizations
         WHERE course_key IN ('ai-hallucinations','engineering-assurance')) <> 6
     OR (SELECT count(*) FROM content_public.catalog_units
         WHERE course_key IN ('ai-hallucinations','engineering-assurance')) <> 36
  THEN RAISE EXCEPTION 'm3_catalog_row_count_mismatch'; END IF;
END
$manzo_counts$;

SELECT jsonb_build_object(
  'courses', (SELECT count(*) FROM content_public.catalog_courses
       WHERE course_key IN ('ai-hallucinations','engineering-assurance')),
  'localized_variants', (SELECT count(*) FROM content_public.catalog_localizations
       WHERE course_key IN ('ai-hallucinations','engineering-assurance')),
  'localized_units', (SELECT count(*) FROM content_public.catalog_units
       WHERE course_key IN ('ai-hallucinations','engineering-assurance')),
  'manifest_sha256', '{manifest_sha}',
  'write_mode', '{mode}'
) AS manzo_m3_verification;

{'COMMIT' if mode == 'commit' else 'ROLLBACK'};
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO)
    parser.add_argument("--source-revision", required=True, help="full 40-character Git commit SHA")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mode", choices=["rollback", "commit"], default="rollback")
    parser.add_argument("--ci-ephemeral-confirm", action="store_true",
                        help="test-only, no production use")
    args = parser.parse_args()
    if args.mode == "commit" and not (
        args.ci_ephemeral_confirm and os.environ.get("MANZO_M3_EPHEMERAL_DATABASE") == "isolated-ci-only"
    ):
        parser.error("COMMIT is forbidden outside an explicitly acknowledged isolated CI database")
    path = args.output.resolve()
    if path.is_relative_to((args.root / "_site").resolve()):
        parser.error("refusing to publish a database import script in the public site")
    content = make_sql(args.root, args.source_revision, args.mode)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"M3 SQL prepared ({args.mode}); source and metadata only; no database connection")


if __name__ == "__main__":
    main()
