import os
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "product/migration/m3b_private_backup_macos.sh"
REF = "bjydnaejpxwubmxpnpnv"


class MacPrivateBackupKitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SCRIPT.read_text(encoding="utf-8")
        match = re.search(r"python3 - <<'PY' \|\|\n(.*?)\nPY\n", cls.source, re.S)
        assert match, "script must validate remote target before exporting"
        cls.validator = match.group(1)

    def validate(self, url, expected):
        r = subprocess.run(["python3", "-c", self.validator], capture_output=True, text=True,
                           env={**os.environ, "MANZO_DB_URL": url,
                                "MANZO_PROJECT_REF": REF})
        self.assertEqual(r.returncode == 0, expected)
        self.assertNotIn("password123", r.stdout + r.stderr)

    def test_shell_syntax(self):
        p = subprocess.run(["bash", "-n", str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)

    def test_accept_only_this_supabase_project(self):
        self.validate(f"postgresql://postgres:password123@db.{REF}.supabase.co:5432/postgres", True)
        self.validate(f"postgresql://postgres.{REF}:password123@aws-0-eu-west-1.pooler.supabase.com:5432/postgres", True)
        self.validate(f"postgresql://postgres.{REF}:password123@aws-0-eu-west-1.pooler.supabase.com:6543/postgres", True)

    def test_refuse_unrelated_local_or_malicious_hosts(self):
        self.validate("postgresql://postgres:password123@127.0.0.1:54322/postgres", False)
        self.validate("postgresql://postgres:password123@db.other.supabase.co:5432/postgres", False)
        self.validate("postgresql://postgres.bad:password123@aws-0-eu-west-1.pooler.supabase.com:5432/postgres", False)
        self.validate(f"postgresql://postgres.{REF}:password123@pooler.supabase.com.evil.com:5432/postgres", False)
        self.validate(f"postgresql://postgres.{REF}:password123@aws-0-eu-west-1.pooler.supabase.com:5432/other", False)
        self.validate(f"postgresql://postgres.{REF}@aws-0-eu-west-1.pooler.supabase.com:5432/postgres", False)

    def test_cli_v3_remote_is_explicit_and_no_mutation_commands(self):
        source = self.source
        self.assertIn('supabase db dump "$@" "--remote=${MANZO_DB_URL}"', source)
        self.assertIn("dump_to_file roles.sql --role-only", source)
        self.assertIn("dump_to_file schema.sql", source)
        self.assertIn("dump_to_file data.sql --data-only --use-copy", source)
        self.assertNotIn("supabase db push", source)
        self.assertNotIn("supabase db reset", source)
        self.assertNotIn("supabase db dump --local", source)
        self.assertIn('[[ -z "${GITHUB_ACTIONS:-}" && -z "${CI:-}" ]]', source)

    def test_private_storage_and_restore_not_verified(self):
        source = self.source
        self.assertIn('BACKUP_BASE="${HOME}/.manzo-ai/private-backups"', source)
        self.assertIn("umask 077", source)
        self.assertIn("chmod 700", source)
        self.assertIn("chmod 600", source)
        self.assertIn("shasum -a 256 -c SHA256SUMS", source)
        self.assertIn("RESTORE NOT VERIFIED", source)
        self.assertIn("CLI dumps exclude Supabase-managed schemas such as Auth and Storage.", source)


if __name__ == "__main__":
    unittest.main()
