#!/usr/bin/env python3
"""Independent browser smoke for the source-only MANZO AI teacher course reader.

Run from repository root with local HTTP server on port 8766.
The CI workflow starts it automatically. Requires playwright==1.55.0 + Chromium.
This validates actual UI controls, not educational impact or full WCAG.
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8766/editorial/learning/ai-teaching-lab/preview/"
ROOT = Path(__file__).resolve().parents[1]
course = json.loads((ROOT / "it/course.json").read_text(encoding="utf-8"))
bank = json.loads((ROOT / "it/assessment-bank.json").read_text(encoding="utf-8"))
evidence = Path("ai-teaching-lab-screenshots")
evidence.mkdir(exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    for width in (1440, 390):
        page = browser.new_page(
            viewport={"width": width, "height": 900 if width == 1440 else 844},
            reduced_motion="reduce",
            device_scale_factor=1,
        )
        js_errors = []
        page.on("pageerror", lambda err: js_errors.append(str(err)))
        page.goto(BASE, wait_until="networkidle", timeout=30000)
        page.locator("#experience").wait_for(state="visible", timeout=10000)
        assert page.locator("#module-nav button").count() == 5
        assert page.locator(".atl-course-tabs a").count()==4
        assert page.locator("#competenze .atl-competencies-grid>div").count()==4
        assert page.locator(".module-outline").count()==5
        assert page.locator(".course-session-step").count()==4
        assert "CAPITOLO" not in page.locator("#atl-theory").inner_text()
        assert page.locator(".narrative-bridge").count()>=4
        page.locator(".module-outline").first.locator("summary").click()
        assert page.locator(".module-outline").first.locator(".module-outline-link").count()==4
        assert page.locator("#presentazione-corso").is_visible()
        assert page.locator(".atl-intro-media-card").count() == 2
        assert page.locator(".atl-intro-privacy").is_visible()
        page.locator('a[href="./presentazione/"]').click()
        page.wait_for_url(BASE+"presentazione/")
        page.locator(".atl-slide-page h2").wait_for(timeout=10000)
        assert page.locator("#atl-present-counter").inner_text()=="01 / 15"
        page.locator("#atl-present-next").click()
        assert page.locator("#atl-present-counter").inner_text()=="02 / 15"
        page.locator("#atl-present-select").select_option("14")
        assert "Una domanda per continuare" in page.locator(".atl-slide-page h2").inner_text()
        page.goto(BASE,wait_until="networkidle")
        page.locator("#experience").wait_for(state="visible",timeout=10000)
        assert page.locator(".atl-resource-link").count() == 19
        assert page.locator(".atl-resource-link:visible").count() == 4
        assert page.locator(".atl-resource-hub").is_visible()
        assert not page.locator("[data-atl-resource-glossary]").is_visible()
        assert page.evaluate("document.getElementById('module-nav').nextElementSibling.classList.contains('atl-resource-hub')")
        page.locator(".atl-resource-more:not(.atl-resource-specialized) summary").click()
        assert page.locator(".atl-resource-link:visible").count() == 11
        page.locator(".atl-resource-more:not(.atl-resource-specialized) summary").click()
        assert page.locator(".atl-resource-link:visible").count() == 4
        page.locator(".atl-resource-specialized summary").click()
        assert page.locator(".atl-resource-link:visible").count() == 12
        page.locator(".atl-resource-specialized summary").click()
        assert page.locator("#module-content").is_visible()
        assert page.locator(".preview-tag").is_visible()
        assert page.get_by_text("Non pubblicata", exact=False).count() >= 1
        for i in range(5):
            page.locator("#module-nav button").nth(i).click()
            page.locator(".module-hero h2").wait_for()
            assert course["modules"][i]["title"] in page.locator(".module-hero h2").inner_text()
            assert page.locator(".panel").count() >= 5
            assert page.locator(".method-step").count() == 7
            assert page.locator(".case-card").count() == 2
            assert page.locator(".lab-prompt-code").count() == 3
            assert page.locator(".competency-studio").count() == 1
            assert page.locator(".studio-check").count() >= 4
            if i == 0:
                page.locator(".competency-reason").fill("Scelgo la scheda senza IA perché rende osservabile l'argomentazione, mantiene i testi sintetici e posso controllare la fonte.")
                page.get_by_role("button", name="Verifica i miei criteri").click()
                assert "competenza osservabile" in page.locator(".option-board .result").inner_text().lower()
            if i == 1:
                page.get_by_role("button", name="Prova le quattro schede nuove").click()
                assert "2/4" in page.locator(".demo-model .result").inner_text()
                page.locator('input[name="demo-feature"][value="shape"]').check()
                page.get_by_role("button", name="Prova le quattro schede nuove").click()
                assert "4/4" in page.locator(".demo-model .result").inner_text()
            if i == 2:
                assert page.locator("#atl-model-media option").count() == 6
                assert "ChatGPT Images" in page.locator(".model-choice-detail").inner_text()
                assert "Nano Banana" in page.locator(".model-choice-detail").inner_text()
                page.locator("#atl-model-media").select_option("3")
                assert "Notebook" in page.locator(".model-choice-detail").inner_text()
                page.locator("#atl-model-media").select_option("0")
                page.locator("#atl-model-rationale").fill("Confronto due modelli di immagini sullo stesso brief, verificando accuratezza e accessibilità prima della scelta.")
                page.get_by_role("button", name="Confronta la mia scelta").click()
                assert page.locator(".model-choice-controls .result").is_visible()
                page.get_by_role("button", name="Costruisci la scaletta didattica").click()
                assert "STORYBOARD" in page.locator(".media-generated").inner_text()
                assert page.locator(".media-principle-card").count() == 6
            if i == 3:
                page.locator(".option-board .button").first.click()
                assert page.locator(".option-board .result").is_visible()
            if i == 4:
                page.locator(".practice-branch .button").first.click()
                assert "Conseguenza" in page.locator(".practice-branch .branch-feedback").inner_text()
            assert page.locator(".applied-step").count() == 5
            assert page.locator(".narrative-chapter").count() >= 5
            assert page.locator(".branch-choices button").count() == 3
            page.locator(".branch-choices button").first.click()
            assert page.locator(".branch-choices button").count() == 2
            page.locator(".branch-choices button").first.click()
            assert page.locator(".branch-outcome").is_visible()
            page.get_by_role("button", name="Esplora una scelta diversa").click()
            assert page.locator(".branch-choices button").count() == 3
            assert page.locator(".cross-cell input").count() > 0
            assert page.locator(".source-list a").count() >= 3
            assert page.locator("a.full-lesson-link").get_attribute("href") == "../it/module-%02d.md" % (i+1)
            page.screenshot(path=str(evidence / ("module-%02d-%d.png" % (i+1, width))), full_page=False)
        # Course-ending vocabulary is independently searchable and grouped.
        assert page.locator("#atl-final-glossary").is_visible()
        assert "79 voci" in page.locator("#atl-term-count").inner_text()
        page.locator("#atl-term-search").fill("pedagogia")
        assert page.locator(".term-card").count() >= 1
        page.locator("#atl-term-search").fill("")
        page.locator("#atl-term-group").select_option("Fondamenti educativi")
        assert page.locator(".term-card").count() >= 7
        page.locator("#atl-term-group").select_option("")
        page.locator("#module-nav button").first.click()
        first=page.locator("fieldset.assessment-block").filter(has=page.get_by_role("button", name="Verifica la risposta")).first
        q=course["modules"][0]["checkpoint"][0]
        first.locator('input[type="radio"]').nth(q["correct_index"]).check()
        first.get_by_role("button", name="Verifica la risposta").click()
        assert "Corretto" in first.locator(".result").inner_text()
        multi=page.locator("fieldset.assessment-block").filter(has=page.get_by_role("button", name="Controlla la selezione"))
        for idx in bank["modules"][0]["multi_select"]["correct"]:
            multi.locator('input[type="checkbox"]').nth(idx).check()
        multi.get_by_role("button", name="Controlla la selezione").click()
        assert "Corretto" in multi.locator(".result").inner_text()
        scenario=page.locator("fieldset.assessment-block").filter(has=page.get_by_role("button", name="Confronta la tua decisione"))
        scenario.locator('input[type="radio"]').nth(
            bank["modules"][0]["decision_scenario"]["correct_index"]
        ).check()
        scenario.locator("textarea").fill(
            "La decisione mantiene l'allineamento pedagogico e documenta l'evidenza."
        )
        scenario.get_by_role("button", name="Confronta la tua decisione").click()
        assert "Decisione coerente" in scenario.locator(".result").inner_text()
        match=page.locator(".assessment-block").filter(has=page.get_by_role("button",name="Controlla le associazioni"))
        assert match.count() == 1
        for idx, pair in enumerate(bank["modules"][0]["matching"]["pairs"]):
            match.locator("select").nth(idx).select_option(label=pair["description"])
        match.get_by_role("button",name="Controlla le associazioni").click()
        assert "4 associazioni corrette su 4" in match.locator(".result").inner_text()
        puzzle=page.locator(".assessment-block").filter(has=page.get_by_role("button",name="Verifica il cruciverba"))
        assert puzzle.count() == 1
        puzzle.get_by_role("button",name="Elenco accessibile").click()
        for entry, input_el in zip(bank["modules"][0]["crossword"]["entries"],
                                   puzzle.locator(".accessible-words input").all()):
            input_el.fill(entry["answer"])
        puzzle.get_by_role("button", name="Verifica il cruciverba").click()
        assert "7 parole corrette su 7" in puzzle.locator(".result").inner_text()
        puzzle.get_by_role("button",name="Griglia",exact=True).click()
        assert puzzle.locator(".crossword-wrap").is_visible()
        assert not puzzle.locator(".accessible-words").is_visible()
        assert not page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 2"), (
            "horizontal overflow at %s px" % width
        )
        assert not js_errors, js_errors
        page.close()
    browser.close()
print("AI Teaching Lab browser smoke: desktop+mobile, 5 modules, quizzes, matching, crossword PASS")
