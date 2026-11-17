"""Offline integrity checks for the unpublished MANZO AI Teaching Lab editorial package.

Run: python3 -m unittest discover -s editorial/learning/ai-teaching-lab/tests -p 'test_*.py' -v
Uses stdlib only. Verifies content contracts, not educational efficacy or legal compliance.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "it"
COURSE = json.loads((ROOT / "course.json").read_text(encoding="utf-8"))
BANK = json.loads((ROOT / "assessment-bank.json").read_text(encoding="utf-8"))


class CourseQuality(unittest.TestCase):
    def test_unpublished_synthetic(self):
        self.assertEqual(COURSE["status"], "editorial_draft")
        self.assertFalse(COURSE["published"])
        self.assertFalse(COURSE["ai_and_data_policy"]["real_student_data_allowed"])
        self.assertFalse(COURSE["assessment"]["certificate_available"])
        self.assertFalse(BANK["implementation_status"]["persistent_progress"])
        self.assertFalse(BANK["implementation_status"]["server_side_grading"])
        self.assertTrue(BANK["policy"]["formative_only"])

    def test_methodology_in_every_module(self):
        method = COURSE["methodology"]
        steps = [s["id"] for s in method["seven_steps"]]
        self.assertEqual(len(steps), 7)
        self.assertEqual(len(set(steps)), 7)
        self.assertEqual(method["learning_progression"], ["Comprendere", "Applicare", "Valutare", "Creare"])
        for module in COURSE["modules"]:
            with self.subTest(module=module["id"]):
                self.assertEqual(module["methodology_steps"], steps)

    def test_theory_cases_sources(self):
        modules = COURSE["modules"]
        self.assertEqual(len(modules), 5)
        self.assertEqual(sum(m["hours"] for m in modules), 20)
        self.assertEqual(sum(len(m["professional_cases"]) for m in modules), 10)
        for m in modules:
            with self.subTest(module=m["id"]):
                th = m["theory"]
                self.assertGreaterEqual(len(th["paragraphs"]), 3)
                self.assertGreaterEqual(len(th["sources"]), 3)
                self.assertTrue(th["pedagogical_reference"]["name"])
                self.assertIn("parafrasi", th["pedagogical_reference"]["type"])
                self.assertTrue(th["pedagogical_reference"]["source"].startswith("https://"))
                self.assertTrue(all(s["url"].startswith("https://") for s in th["sources"]))
                self.assertGreaterEqual(len(m["professional_cases"]), 2)
                for case in m["professional_cases"]:
                    for field in ["title", "situation", "task", "artifact", "redline"]:
                        self.assertTrue(case[field])

    def test_assessments_and_answers(self):
        by_id = {m["id"]: m for m in BANK["modules"]}
        self.assertEqual(set(by_id), {m["id"] for m in COURSE["modules"]})
        for mod in COURSE["modules"]:
            m = by_id[mod["id"]]
            with self.subTest(module=mod["id"]):
                self.assertGreaterEqual(len(mod["checkpoint"]), 2)
                for item in mod["checkpoint"]:
                    self.assertTrue(0 <= item["correct_index"] < len(item["options"]))
                    self.assertTrue(item["feedback"])
                required = {"single_choice", "multi_select", "decision_scenario",
                            "matching", "crossword", "authentic_task", "exit_ticket"}
                self.assertTrue(required.issubset(set(m["types"])))
                ms = m["multi_select"]
                self.assertGreaterEqual(len(ms["choices"]), 4)
                self.assertGreaterEqual(len(ms["correct"]), 2)
                self.assertTrue(all(0 <= x < len(ms["choices"]) for x in ms["correct"]))
                self.assertEqual(len(ms["correct"]), len(set(ms["correct"])))
                decision = m["decision_scenario"]
                self.assertTrue(0 <= decision["correct_index"] < len(decision["options"]))
                self.assertEqual(len(decision["options"]), len(decision["feedback"]))
                self.assertGreaterEqual(len(m["matching"]["pairs"]), 4)

    def test_crosswords_are_real_intersections(self):
        for module in BANK["modules"]:
            puzzle = module["crossword"]
            with self.subTest(module=module["module_id"]):
                h, w = puzzle["height"], puzzle["width"]
                rows = puzzle["pattern"]
                self.assertEqual(len(rows), h)
                self.assertTrue(all(len(row) == w for row in rows))
                self.assertEqual(len(puzzle["entries"]), 7)
                all_cells = {}
                for entry in puzzle["entries"]:
                    answer = entry["answer"]
                    self.assertTrue(answer.isascii() and answer.isalpha() and answer.isupper())
                    self.assertGreaterEqual(len(entry["clue"]), 15)
                    self.assertIn(entry["direction"], ["across", "down"])
                    for i, letter in enumerate(answer):
                        y = entry["row"] + (i if entry["direction"] == "down" else 0)
                        x = entry["col"] + (i if entry["direction"] == "across" else 0)
                        self.assertTrue(0 <= y < h and 0 <= x < w)
                        self.assertEqual(rows[y][x], ".")
                        all_cells.setdefault((y, x), []).append(letter)
                self.assertTrue(all(len(set(letters)) == 1 for letters in all_cells.values()))
                self.assertGreaterEqual(sum(len(v) > 1 for v in all_cells.values()), 3)
                self.assertEqual(sum(ch == "." for row in rows for ch in row), len(all_cells))
                self.assertTrue(puzzle["accessible_alternative"])



    def test_five_full_module_readers(self):
        ids = [m["id"] for m in COURSE["modules"]]
        for i, module_id in enumerate(ids, start=1):
            with self.subTest(module=module_id):
                p = ROOT / ("module-%02d.md" % i)
                self.assertTrue(p.is_file(), str(p))
                body = p.read_text(encoding="utf-8")
                self.assertGreater(len(body), 10000)
                for marker in [
                    "Teoria documentata", "Metodo MANZO AI", "Laboratorio A",
                    "Laboratorio B", "Verifica differenziata", "Cruciverba professionale",
                    "Insegnamento pedagogico", "Guida del formatore",
                    "Bibliografia specifica", "Exit ticket",
                ]:
                    self.assertIn(marker, body)
                self.assertIn(COURSE["modules"][i - 1]["title"], body)
                self.assertIn("48 |", body)
                self.assertIn("72 |", body)
                self.assertIn("15 |", body)
                for quote in COURSE["modules"][i - 1]["theory"]["sources"]:
                    self.assertIn(quote["url"], body)
                for item in COURSE["modules"][i - 1]["checkpoint"]:
                    self.assertIn(item["question"], body)
                self.assertNotIn("Voto finale automatico", body)

    def test_preview_files_and_privacy(self):
        preview = ROOT.parent / "preview"
        html = (preview / "index.html").read_text(encoding="utf-8")
        css = (preview / "assets.css").read_text(encoding="utf-8")
        js = (preview / "app.js").read_text(encoding="utf-8")
        self.assertIn('name="robots" content="noindex,nofollow"', html)
        self.assertIn("[hidden]{display:none!important}", css)
        for marker in ["assessment-bank.json", "crossword", "matching", "singleChoice",
                       "multiChoice", "scenario", "fetch("]:
            self.assertIn(marker, js)
        for bad in ["localStorage.setItem", "sessionStorage.setItem", "service_role",
                    "analytics.track(", "eval("]:
            self.assertNotIn(bad, js)
        self.assertIn("course.json", js)
        self.assertIn("aria-label", js)

    def test_crossword_numbers_and_recovery(self):
        for module in BANK["modules"]:
            with self.subTest(module=module["module_id"]):
                puzzle = module["crossword"]
                for entry in puzzle["entries"]:
                    self.assertTrue(1 <= entry["number"] <= 7)
                    self.assertTrue(entry["row"] >= 0 and entry["col"] >= 0)
                    self.assertTrue(entry["clue"])

if __name__ == "__main__":
    unittest.main()
