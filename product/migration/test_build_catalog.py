import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from build_catalog import build_catalog, SOURCES, LOCALES

ROOT = Path(__file__).resolve().parents[2]


class EditorialCatalogContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = build_catalog(ROOT)

    def test_expected_courses_locales_units_and_assessments(self):
        d = self.catalog
        self.assertEqual(d["summary"]["courses"], 2)
        self.assertEqual(d["summary"]["localized_variants"], 6)
        self.assertEqual(d["summary"]["languages"], ["it", "en", "es"])
        self.assertEqual(d["summary"]["localized_units"], 36)
        self.assertEqual(d["summary"]["localized_public_self_assessment_items"], 42)
        self.assertEqual(d["summary"]["localized_cases"], 42)
        self.assertEqual(len({v["route"] for v in d["variants"]}), 6)
        self.assertEqual(
            set(v["key"] for v in d["variants"]),
            {f"{key}:{loc}" for key in SOURCES for loc in LOCALES},
        )

    def test_manifest_is_metadata_only_no_answers_or_private_data(self):
        d = self.catalog
        self.assertEqual(d["scope"], "editorial_public_metadata_only")
        self.assertFalse(d["content_policy"]["quiz_answers_exported"])
        self.assertFalse(d["content_policy"]["progress_exported"])
        self.assertFalse(d["content_policy"]["course_access_claimed"])
        forbidden = {"quiz", "questions", "answer", "correct_option", "correct_answer", "solution",
                     "explanation", "rationale", "student_id", "email", "password", "user_id"}
        def walk(obj):
            if isinstance(obj, dict):
                self.assertFalse(forbidden.intersection(obj), f"sensitive output keys: {forbidden.intersection(obj)}")
                for value in obj.values():
                    walk(value)
            elif isinstance(obj, list):
                for item in obj:
                    walk(item)
        walk(d)
        self.assertTrue(all(not v["private_assessment_ready"] for v in d["variants"]))
        self.assertTrue(all(c["owner_tenant_id"] is None for c in d["courses"]))

    def test_content_addresses_match_exact_original_bytes(self):
        for v in self.catalog["variants"]:
            raw = (ROOT / v["source_path"]).read_bytes()
            self.assertEqual(v["source_sha256"], hashlib.sha256(raw).hexdigest())
            self.assertEqual(len(v["source_sha256"]), 64)
            self.assertEqual(v["unit_count"], len(v["units"]))
            self.assertEqual([x["position"] for x in v["units"]], list(range(1, 7)))

    def test_rebuild_is_deterministic(self):
        self.assertEqual(
            json.dumps(build_catalog(ROOT), ensure_ascii=False, sort_keys=True),
            json.dumps(build_catalog(ROOT), ensure_ascii=False, sort_keys=True),
        )

    def test_missing_locale_and_invalid_quiz_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            dst = Path(tmp)
            for spec in SOURCES.values():
                for lang in LOCALES:
                    name = spec["file"].format(locale=lang)
                    (dst / name).parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(ROOT / name, dst / name)
            source = dst / SOURCES["ai-hallucinations"]["file"].format(locale="it")
            original = json.loads(source.read_text(encoding="utf-8"))
            original["quiz"][0][2] = [999]
            source.write_text(json.dumps(original, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "answer markers"):
                build_catalog(dst)
            source.unlink()
            with self.assertRaisesRegex(ValueError, "missing editorial source"):
                build_catalog(dst)


if __name__ == "__main__":
    unittest.main()
