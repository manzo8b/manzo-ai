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
SCENES = json.loads((ROOT / "scenarios.json").read_text(encoding="utf-8"))


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
        by_id = {m["module_id"]: m for m in BANK["modules"]}
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
        self.assertEqual(len(ids), 5)
        for i, module_id in enumerate(ids, start=1):
            with self.subTest(module=module_id):
                p = ROOT / ("module-%02d.md" % i)
                self.assertTrue(p.is_file(), str(p))
                body = p.read_text(encoding="utf-8")
                self.assertGreater(len(body), 14000)
                for marker in [
                    "Come seguire questo modulo in autonomia",
                    "Questo corso è un esempio di didattica applicata",
                    "Il metodo MANZO AI: una proposta",
                    "Laboratorio 1", "Laboratorio 2",
                    "Parole utili", "Prompt pronto da copiare",
                    "Verifica ciò che hai imparato",
                    "Per chi facilita un gruppo",
                    "Fonti da esplorare",
                ]:
                    self.assertIn(marker, body)
                self.assertIn(COURSE["modules"][i - 1]["title"], body)
                self.assertNotIn("Sequenza guidata da 240 minuti", body)
                self.assertNotIn("applicazione obbligatoria", body)
                for quote in COURSE["modules"][i - 1]["theory"]["sources"]:
                    self.assertIn(quote["url"], body)
                for item in COURSE["modules"][i - 1]["checkpoint"]:
                    self.assertIn(item["question"], body)
                self.assertNotIn("Voto finale automatico", body)

    def test_narrative_and_teacher_glossary(self):
        narrative = json.loads((ROOT / "narrative.json").read_text(encoding="utf-8"))
        glossary = json.loads((ROOT / "glossary.json").read_text(encoding="utf-8"))
        self.assertEqual([m["id"] for m in narrative["modules"]], [m["id"] for m in COURSE["modules"]])
        self.assertGreaterEqual(len(glossary["entries"]), 40)
        self.assertEqual(len(glossary["entries"]), len(set(x["term"].casefold() for x in glossary["entries"])))
        words = {x["term"] for x in glossary["entries"]}
        for required in ("Metodo MANZO AI", "Didattica", "Pedagogia", "Pedagogico / pedagogica",
                         "Educazione", "Metodo", "Tecnica", "Prompt", "IA generativa"):
            self.assertIn(required, words)
        for row in glossary["entries"]:
            self.assertGreater(len(row["definition"]), 55)
            self.assertGreater(len(row["classroom_example"]), 35)
            self.assertIn(row["category"], glossary["categories"])
        for m in narrative["modules"]:
            self.assertGreaterEqual(len(m["chapters"]), 5)
            self.assertEqual(len(m["labs"]), 2)
            for lab in m["labs"]:
                self.assertGreaterEqual(len(lab["steps"]), 5)
                for label in ["prompt", "sample", "check", "deliverable", "goal"]:
                    self.assertGreater(len(lab[label]), 28)
                self.assertIn("OBIETTIVO", lab["prompt"])
            self.assertGreaterEqual(len(m["glossary"]), 6)
        self.assertIn("Che cos’è l’IA", " ".join(x["heading"] for x in narrative["modules"][0]["chapters"]))
        self.assertIn("applicata", COURSE["course_title"].lower())
        self.assertEqual(len(COURSE["course_as_demonstration"]["sequence"]), 7)

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


    def test_branching_simulations_and_transfer(self):
        self.assertFalse(SCENES["published"])
        self.assertEqual(len(SCENES["modules"]), 5)
        for scene, course_module in zip(SCENES["modules"], COURSE["modules"]):
            with self.subTest(module=scene["module_id"]):
                self.assertEqual(scene["module_id"], course_module["id"])
                self.assertEqual(scene["path_count"], 6)
                self.assertEqual(len(scene["first"]), 3)
                self.assertEqual(len({choice["label"] for choice in scene["first"]}), 3)
                self.assertGreater(len(scene["setting"]), 100)
                self.assertGreater(len(scene["reflection"]), 50)
                theory = scene["mini_theory"]
                self.assertEqual(len(theory["options"]), 3)
                self.assertIn(theory["source"], [s["url"] for s in course_module["theory"]["sources"]]
                              + [course_module["theory"]["pedagogical_reference"]["source"]])
                self.assertIn(theory["correct"], [0,1,2])
                for option in scene["first"]:
                    self.assertEqual(len(option["routes"]), 2)
                    self.assertTrue(any(route["good"] for route in option["routes"]))
                    self.assertTrue(any(not route["good"] for route in option["routes"]))
                    for route in option["routes"]:
                        self.assertGreater(len(route["why"]), 35)
                        self.assertGreater(len(route["transfer"]), 20)
                        self.assertGreater(len(route["result"]), 40)


    def test_official_teacher_document_hub_and_podcast(self):
        preview = (ROOT.parent / "preview" / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="atl-resource-heading"', preview)
        self.assertIn('<nav id="module-nav"', preview)
        self.assertLess(preview.index('id="module-nav"'), preview.index('class="atl-resource-hub"'))
        self.assertEqual(preview.count('class="atl-resource-link"'), 19)
        self.assertEqual(preview.count('rel="noopener noreferrer" title="Apri'), 19)
        for authority in ["mim.gov.it", "unesco.org", "education.ec.europa.eu",
                          "garanteprivacy.it", "oecd.org", "udlguidelines.cast.org",
                          "ai-act-service-desk.ec.europa.eu"]:
            self.assertIn(authority, preview)
        self.assertIn("schema MIM, ottobre 2026", preview)
        self.assertIn("altre 7 risorse", preview.lower())
        media = (ROOT.parent / "media" / "PODCAST_NOTEBOOKLM_ITALIANO_8_MIN.md").read_text(encoding="utf-8")
        self.assertIn("La classe delle 7:43", media)
        self.assertIn("MARTA", media)
        self.assertIn("DAVIDE", media)
        self.assertIn("### Prompt da incollare", media)
        self.assertIn("Formato APPROFONDIMENTO", media)
        self.assertIn("sistema scientificamente validato", media)
        dialogue = media.split("# Copione originale — due voci", 1)[1].split("## Fonti da caricare", 1)[0]
        utterances = [line for line in dialogue.splitlines()
                      if line.startswith("**MARTA:**") or line.startswith("**DAVIDE:**")]
        self.assertGreaterEqual(len(utterances), 45)
        self.assertGreater(sum(len(u.split()) for u in utterances), 1120)
        self.assertLess(sum(len(u.split()) for u in utterances), 1450)
        self.assertFalse(any("**TERZA VOCE:**" in x for x in utterances))


    def test_course_presentation_and_uploaded_deck_source(self):
        page=(ROOT.parent/"preview"/"index.html").read_text(encoding="utf-8")
        self.assertIn('id="presentazione-corso"',page)
        self.assertIn('data-atl-video-media',page)
        self.assertIn('data-atl-deck-downloads',page)
        self.assertIn('href="./presentazione/"',page)
        self.assertLess(page.index('id="presentazione-corso"'),page.index('id="experience"'))
        self.assertIn("20 h",page)
        self.assertIn("Non occorre creare un account",page)
        self.assertIn("non equivale a certificare",page)
        self.assertEqual(page.count("Domande per discutere con i colleghi"),1)
        data=json.loads((ROOT/"presentation.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["slides"]),15)
        self.assertEqual(data["duration_podcast_seconds"]//60,7)
        for slide in data["slides"]:
            self.assertTrue(slide["title"])
            self.assertTrue(slide["lead"])
            self.assertTrue(slide["takeaway"])
            self.assertGreaterEqual(len(slide["points"]),2)
        self.assertIn("parafrasi",data["slides"][11]["points"][-1])
        self.assertIn("GDPR",data["slides"][7]["takeaway"])
        slide_page=(ROOT.parent/"preview"/"presentazione"/"index.html").read_text(encoding="utf-8")
        self.assertIn('id="atl-present-slide"',slide_page)
        self.assertIn('id="atl-present-next"',slide_page)
        self.assertIn('data-slides-base="../../it/"',slide_page)


    def test_continuous_narrative_and_learning_activities(self):
        narrative = json.loads((ROOT / "narrative.json").read_text(encoding="utf-8"))
        self.assertEqual(len(narrative["modules"]), 5)
        for idx, m in enumerate(narrative["modules"],1):
            with self.subTest(module=m["id"]):
                self.assertEqual(m["reading_label"],"Lettura di approfondimento")
                self.assertEqual(len(m["learning_rhythm"]), 4)
                self.assertEqual(sum(x["estimated_min"] for x in m["learning_rhythm"]),240)
                self.assertEqual(len([c for c in m["chapters"] if c.get("transition")]),len(m["chapters"])-1)
                for c in m["chapters"][:-1]:
                    self.assertGreater(len(c["transition"]), 120)
                self.assertGreater(len(m["bridge_to_next"]["back"]), 140)
                full=(ROOT / f"module-{idx:02d}.md").read_text(encoding="utf-8")
                self.assertIn("## Lettura di approfondimento",full)
                self.assertIn("## Per continuare il percorso",full)
                self.assertIn(m["bridge_to_next"]["back"],full)
                self.assertIn(m["chapters"][0]["transition"],full)
        script=(ROOT.parent/"preview"/"app.js").read_text(encoding="utf-8")
        self.assertNotIn('"CAPITOLO "+String(',script)
        # One clear study journey; long readings and labs are retained in the data.
        self.assertIn('title:"Orientati"',script)
        self.assertIn('title:"Comprendi"',script)
        self.assertIn('title:"Sperimenta"',script)
        self.assertIn('title:"Verifica"',script)
        self.assertIn("atl-journey-panel",script)
        self.assertIn("atl-journey-nav",script)
        self.assertIn("atl-module-select",script)
        self.assertIn('theory.id="atl-theory"',script)
        self.assertIn('assess.id="atl-quiz"',script)
        self.assertNotIn("course-session-map",script)
        self.assertNotIn("module-outline",script)
        self.assertIn("course-next-section",script)

    def test_authentic_slide_mode_and_media_bundle_contract(self):
        preview=ROOT.parent/"preview"
        script=(preview/"presentation.js").read_text(encoding="utf-8")
        css=(preview/"presentation.css").read_text(encoding="utf-8")
        publisher=(ROOT.parents[3] / "theme" / "publish-ai-teaching-lab.py").read_text(encoding="utf-8")
        self.assertIn("data-original-slide-base",publisher)
        self.assertIn("slide-{i:02d}.webp",publisher)
        self.assertIn("AI_Teaching_Lab_Originali_Per_GitHub_e_Anteprima.zip",publisher)
        self.assertIn("AI_per_Docenti.web.mp4",publisher)
        self.assertIn("authentic_slides",publisher)
        self.assertIn("atl-original-slide",script)
        self.assertIn("atl-slide-transcription",script)
        self.assertIn("document.body.dataset.originalSlideBase",script)
        self.assertIn("color:#fff!important",css)
        self.assertIn("atl-slide-reading h2",css)


    def test_five_integrated_professional_experiences(self):
        narrative=json.loads((ROOT/"narrative.json").read_text(encoding="utf-8"))
        expected=["decision_matrix","model_test","multimedia_design","inclusive_feedback","branching_path"]
        self.assertEqual(sum(m["hours"] for m in COURSE["modules"]),20)
        self.assertFalse(COURSE["hours_validated_by_pilot"])
        self.assertEqual(len(COURSE["cross_module_competences"]),5)
        for i,m in enumerate(narrative["modules"]):
            with self.subTest(module=m["id"]):
                f=m["focus_experience"]
                self.assertEqual(f["type"],expected[i])
                self.assertGreaterEqual(len(f["steps"]),5)
                self.assertIn("OBIETTIVO",f["prompt"])
                self.assertGreater(len(f["example"]),160)
                self.assertGreaterEqual(len(f["criteria"]),4)
                self.assertGreaterEqual(len(f["references"]),1)
                self.assertTrue(all(x["url"].startswith("https://") for x in f["references"]))
                self.assertTrue(0<=f["quiz"]["correct_index"]<len(f["quiz"]["options"]))
                self.assertEqual(BANK["modules"][i]["competency_check"]["question"],f["quiz"]["question"])
                self.assertEqual(BANK["modules"][i]["competency_check"]["format"],expected[i])
                self.assertEqual(COURSE["modules"][i]["competence_focus"]["kind"],expected[i])
                lesson=(ROOT/f"module-{i+1:02d}.md").read_text(encoding="utf-8")
                self.assertIn("## Esercitazione integrata",lesson)
                self.assertIn(f["prompt"],lesson)
                self.assertIn(f["deliverable"],lesson)
        demo=narrative["modules"][1]["focus_experience"]["demo"]
        self.assertEqual(len(demo["training"]),8)
        self.assertEqual(len(demo["test"]),4)
        self.assertEqual(sum(x["label"]==("triangolo" if x["color"]=="blu" else "cerchio") for x in demo["test"]),2)
        self.assertEqual(sum(x["label"]==x["shape"] for x in demo["test"]),4)

    def test_multimedia_model_guide_studio_and_glossary(self):
        story=json.loads((ROOT/"narrative.json").read_text(encoding="utf-8"))["modules"][2]
        guide=story["generative_model_guide"]
        self.assertEqual(len(guide["rows"]),6)
        for needle in ("ChatGPT Images","Nano Banana"):
            self.assertIn(needle,str(guide["rows"][0]))
        self.assertIn("Veo",str(guide["rows"][4]))
        self.assertIn("NotebookLM",str(guide["rows"][3]))
        self.assertIn("H5P",str(guide["rows"][5]))
        self.assertEqual(guide["as_of"],"2026-11-17")
        self.assertGreaterEqual(len(guide["decision_criteria"]),6)
        self.assertTrue(all(row["source"].startswith("https://") for row in guide["rows"]))
        self.assertEqual(len(story["multimedia_design_principles"]),6)
        self.assertEqual(len(story["media_blueprints"]),4)
        lesson=(ROOT/"module-03.md").read_text(encoding="utf-8")
        self.assertIn("ChatGPT Images",lesson)
        self.assertIn("Nano Banana",lesson)
        self.assertEqual(len(COURSE["modules"][2]["generative_model_selection"]["examples"]),6)
        gloss=json.loads((ROOT/"glossary.json").read_text(encoding="utf-8"))
        self.assertEqual(len(gloss["entries"]),79)
        words={x["term"] for x in gloss["entries"]}
        for term in ("Apprendimento automatico (machine learning)","Multimodalità",
                     "Storyboard didattico","ChatGPT Images / GPT Image",
                     "Nano Banana / Gemini Image","Scenario ramificato (branching)"):
            self.assertIn(term,words)
        html=(ROOT.parent/"preview"/"index.html").read_text(encoding="utf-8")
        self.assertEqual(html.count('class="atl-resource-link"'),19)
        self.assertIn("Strumenti per i laboratori · 8 risorse",html)
        script=(ROOT.parent/"preview"/"app.js").read_text(encoding="utf-8")
        for word in ("professionalStudio","model-selection-guide","media-creator",
                     "model-test-grid","practice-branch"):
            self.assertIn(word,script)


    def test_real_multimedia_production_studio_contract(self):
        preview=ROOT.parent/"preview"
        source=(preview/"laboratorio-multimediale"/"index.html").read_text(encoding="utf-8")
        script=(preview/"production-studio.js").read_text(encoding="utf-8")
        css=(preview/"production-studio.css").read_text(encoding="utf-8")
        course=(preview/"index.html").read_text(encoding="utf-8")
        self.assertEqual(source.count('class="studio-phase"'),5)
        for field in ('title','audience','goal','source','script','quiz_question',
                      'feedback_correct','feedback_wrong'):
            self.assertIn(f'name="{field}"',source)
        for token in ("studio-download-html","studio-download-json","studio-import",
                      "studio-scenes","studio-audio","studio-preview","studio-medium"):
            self.assertIn(token,source)
        self.assertIn("studio-entry-action",course)
        self.assertIn('href="./laboratorio-multimediale/"',course)
        self.assertIn("String.raw",script)
        self.assertIn("fileDownload",script)
        self.assertIn("exportedHTML",script)
        self.assertIn("readAsDataURL",script)
        self.assertIn("new FileReader",script)
        self.assertIn("microlezione",script)
        self.assertIn("quiz-answers",script)
        self.assertIn("studio-workspace",css)
        self.assertIn("max-width:700px",css)
        publisher=(ROOT.parents[3]/"theme"/"publish-ai-teaching-lab.py").read_text(encoding="utf-8")
        self.assertIn('"laboratorio-multimediale"/"index.html"',publisher)
        self.assertIn('"production-studio.js"',publisher)
        self.assertIn('"production-studio.css"',publisher)
        module=(ROOT/"module-03.md").read_text(encoding="utf-8")
        self.assertIn("Laboratorio di produzione · costruisci e scarica il tuo kit",module)

if __name__ == "__main__":
    unittest.main()
