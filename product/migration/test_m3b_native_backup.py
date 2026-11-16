import subprocess
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "product/migration/m3b_native_backup_macos.sh"


class M3bDockerlessBackupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = SCRIPT.read_text(encoding="utf-8")

    def test_shell_syntax(self):
        r = subprocess.run(["bash", "-n", str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_compatible_pg18_or_pg17_without_cli_or_docker(self):
        s = self.body
        self.assertIn("Versions/17/bin", s)
        self.assertIn("Versions/18/bin", s)
        self.assertIn('PG_DUMP="$PG_BIN/pg_dump"', s)
        self.assertIn('PG_RESTORE="$PG_BIN/pg_restore"', s)
        self.assertIn("(17|18)", s)
        self.assertNotRegex(s, r"(?m)^\s*(?:supabase|docker)\s")
        self.assertIn("--quote-all-identifiers", s)
        self.assertNotIn("supabase db push", s)
        self.assertNotIn("supabase db reset", s)

    def test_target_scoped_and_secrets_never_in_cli_arguments(self):
        s = self.body
        self.assertIn('PROJECT_REF=', s)
        self.assertIn('PGUSER="postgres.${PROJECT_REF}"', s)
        self.assertIn('PGPORT=5432', s)
        self.assertIn("pooler", s)
        self.assertIn('IFS= read -r -s PGPASSWORD', s)
        self.assertIn("export PGPASSWORD", s)
        self.assertIn("unset PGPASSWORD", s)
        self.assertNotIn('pg_dump "$PGPASSWORD"', s)

    def test_private_export_has_integrity_and_explicit_recovery_block(self):
        s = self.body
        self.assertIn('BACKUP_BASE="${HOME}/.manzo-ai/private-backups"', s)
        self.assertIn("umask 077", s)
        self.assertIn("chmod 700", s)
        self.assertIn("chmod 600", s)
        self.assertIn("shasum -a 256 -c SHA256SUMS", s)
        self.assertIn("RESTORE NOT VERIFIED", s)
        self.assertIn("full_database.dump", s)
        self.assertIn("application.dump", s)

    def test_no_mutation_of_live_database(self):
        s = self.body
        self.assertIn('--schema=app --schema=app_private', s)
        self.assertIn("pg_dump", s)
        self.assertNotIn("pg_restore --dbname", s)
        self.assertNotIn("DROP SCHEMA", s)
        self.assertNotIn("DELETE FROM", s)
        self.assertNotIn("auth.users", s)
        self.assertNotIn("CREATE ROLE", s)


if __name__ == "__main__":
    unittest.main()
