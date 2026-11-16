import os
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from prepare_m3_sql import make_sql

ROOT = Path(__file__).resolve().parents[2]
REV = "a" * 40
MIGRATION = ROOT / "product/backend/migrations/0004_public_catalog_m3.sql"


class M3ImportPreparationTests(unittest.TestCase):
    def test_rollback_is_default_and_sql_is_deterministic(self):
        a = make_sql(ROOT, REV)
        b = make_sql(ROOT, REV)
        self.assertEqual(a, b)
        self.assertTrue(a.rstrip().endswith("ROLLBACK;"))
        self.assertIn("BEGIN;", a)
        self.assertIn("ON CONFLICT (course_key, locale)", a)
        self.assertIn("m3_catalog_row_count_mismatch", a)
        self.assertIn("jsonb_array_elements", a)
        self.assertIn("36", a)

    def test_no_private_answers_user_data_or_secrets(self):
        sql = make_sql(ROOT, REV)
        for marker in [
            "correct_option", "encrypted_password", "service_role_key",
            "smtp-relay.brevo", "auth.users", "stripe_secret",
            "manzo_m3_payload$::", "password_hash",
        ]:
            self.assertNotIn(marker, sql)
        self.assertIn("quiz_answers_exported", sql)
        self.assertIn("'write_mode', 'rollback'", sql)

    def test_m3_schema_is_deny_by_default_and_tenant_independent(self):
        ddl = MIGRATION.read_text(encoding="utf-8")
        self.assertIn("CREATE SCHEMA IF NOT EXISTS content_public", ddl)
        self.assertIn("CREATE SCHEMA IF NOT EXISTS content_internal", ddl)
        for name in ("catalog_courses", "catalog_localizations", "catalog_units"):
            self.assertIn(f"content_public.{name}", ddl)
            self.assertIn(f"ALTER TABLE content_public.{name} FORCE ROW LEVEL SECURITY", ddl)
        self.assertNotIn("CREATE POLICY", ddl.upper())  # no anon read policy
        self.assertNotIn("app.organizations", ddl)
        self.assertNotIn("app.courses", ddl)
        self.assertIn("REVOKE ALL", ddl)
        self.assertNotIn("GRANT SELECT", ddl.upper())

    def test_source_sha_must_be_full_and_commit_flag_is_guarded(self):
        with self.assertRaisesRegex(ValueError, "full 40-character"):
            make_sql(ROOT, "short")
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([
                sys.executable,
                str(ROOT / "product/migration/prepare_m3_sql.py"),
                "--root", str(ROOT),
                "--source-revision", REV,
                "--mode", "commit",
                "--output", str(Path(tmp) / "unsafe.sql"),
            ], capture_output=True, text=True, env={**os.environ, "MANZO_M3_EPHEMERAL_DATABASE": ""})
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("COMMIT is forbidden", result.stderr)
            self.assertFalse((Path(tmp) / "unsafe.sql").exists())

    def test_commit_only_when_ci_isolated_flag_and_marker_both_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            sqlfile = Path(tmp) / "isolated.sql"
            result = subprocess.run([
                sys.executable,
                str(ROOT / "product/migration/prepare_m3_sql.py"),
                "--root", str(ROOT),
                "--source-revision", REV,
                "--mode", "commit",
                "--ci-ephemeral-confirm",
                "--output", str(sqlfile),
            ], capture_output=True, text=True,
               env={**os.environ, "MANZO_M3_EPHEMERAL_DATABASE": "isolated-ci-only"})
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(sqlfile.read_text().rstrip().endswith("COMMIT;"))


if __name__ == "__main__":
    unittest.main()
