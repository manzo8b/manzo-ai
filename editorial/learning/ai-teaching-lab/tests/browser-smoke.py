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
            assert page.locator(".theory-accordion").count() == 3
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
            page.screenshot(path=str(evidence / ("module-%02d-%d.png" % (i+1, width))), full_page=True)
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
