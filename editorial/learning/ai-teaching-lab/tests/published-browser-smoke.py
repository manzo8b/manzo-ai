#!/usr/bin/env python3
"""Published-pages Chromium smoke on isolated staging (not real production)."""
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE="http://127.0.0.1:8767/manzo-ai/"
COURSE=BASE+"it/formazione/ia-per-la-didattica/"
SHOT=Path("ai-teaching-lab-screenshots")
SHOT.mkdir(exist_ok=True)
with sync_playwright() as playwright:
    browser=playwright.chromium.launch(headless=True)
    for width in [390,1440]:
        page=browser.new_page(viewport={"width":width,"height":880},reduced_motion="reduce")
        errors=[]
        page.on("pageerror",lambda ex:errors.append(str(ex)))
        page.goto(COURSE,wait_until="networkidle")
        page.locator("#experience").wait_for(state="visible",timeout=10000)
        assert "Formazione docenti" in page.title()
        assert page.locator("header.module-hero").count()==1
        assert page.locator("#module-nav button").count()==5
        assert page.locator(".atl-course-tabs a").count()==4
        assert page.locator("#competenze .atl-competencies-grid>div").count()==4
        assert page.locator(".module-outline").count()==5
        assert page.locator(".course-session-step").count()==4
        assert "CAPITOLO" not in page.locator("#atl-theory").inner_text()
        assert page.locator(".narrative-bridge").count()>=4
        assert page.locator(".course-next-section").count()==1
        assert page.locator("#presentazione-corso").is_visible()
        assert page.locator(".atl-intro-media-card").count()==2
        assert "20 h" in page.locator(".atl-intro-facts").inner_text()
        assert page.locator("a.atl-intro-primary-action").count()==1
        assert page.locator("[data-atl-video-media] video").count() in (0,1)
        # No broken media links are generated before files are staged.
        if not page.locator("[data-atl-video-media] video").count():
            assert page.locator("[data-atl-video-media] .atl-intro-missing").is_visible()
        page.locator("a.atl-intro-primary-action").click()
        page.wait_for_url(COURSE+"presentazione/")
        assert page.locator("#atl-present-counter").inner_text()=="01 / 15"
        page.locator("#atl-present-next").click()
        assert page.locator("#atl-present-counter").inner_text()=="02 / 15"
        page.locator("#atl-present-select").select_option("11")
        assert "La prospettiva pedagogica" in page.locator(".atl-slide-page h2").inner_text()
        assert "parafrasi" in page.locator(".atl-present-side-note").inner_text()
        assert not page.evaluate("document.documentElement.scrollWidth>window.innerWidth+2")
        page.goto(COURSE,wait_until="networkidle")
        page.locator("#experience").wait_for(state="visible",timeout=10000)
        assert page.locator(".atl-resource-hub").is_visible()
        assert page.locator(".atl-resource-link").count()==19
        assert page.locator(".atl-resource-link:visible").count()==4
        assert page.locator("[data-atl-resource-glossary]").is_visible()
        assert page.locator('.atl-resource-link[href*="mim.gov.it"]').count()==1
        assert page.locator('.atl-resource-link[href*="unesco.org"]').count()==2
        assert page.locator(".atl-resource-link").first.get_attribute("target")=="_blank"
        page.locator(".atl-resource-more:not(.atl-resource-specialized) summary").click()
        assert page.locator(".atl-resource-link:visible").count()==11
        page.locator(".atl-resource-more:not(.atl-resource-specialized) summary").click()
        page.locator(".atl-resource-specialized summary").click()
        assert page.locator(".atl-resource-link:visible").count()==12
        page.locator(".atl-resource-specialized summary").click()
        assert page.locator(".branch-choices button").count()==3
        assert page.locator(".lab-prompt-code").count()==3
        probe=page.locator("fieldset.assessment-block").filter(has=page.get_by_role("button",name="Confronta la mia ipotesi"))
        assert probe.count()==1
        probe.locator("input").nth(1).check()
        probe.get_by_role("button",name="Confronta la mia ipotesi").click()
        assert "Hai individuato" in probe.locator(".result").inner_text()
        for index in range(5):
            page.locator("#module-nav button").nth(index).click()
            assert page.locator(".branch-choices button").count()==3
            page.locator(".branch-choices button").first.click()
            assert page.locator(".branch-choices button").count()==2
            page.locator(".branch-choices button").first.click()
            assert page.locator(".branch-outcome").is_visible()
            assert page.locator(".narrative-chapter").count()>=5
            assert page.locator(".competency-studio").count()==1
            assert page.locator(".studio-check").count()>=4
            if index==1:
                page.get_by_role("button",name="Prova le quattro schede nuove").click()
                assert "2/4" in page.locator(".demo-model .result").inner_text()
            if index==2:
                assert page.locator(".media-principle-card").count()==6
                assert page.locator("#atl-model-media option").count()==6
                assert "Nano Banana" in page.locator(".model-choice-detail").inner_text()
                page.locator("#atl-model-media").select_option("4")
                assert "Veo" in page.locator(".model-choice-detail").inner_text()
                page.get_by_role("button",name="Costruisci la scaletta didattica").click()
                assert "STORYBOARD" in page.locator(".media-generated").inner_text()
            if index==4:
                page.locator(".practice-branch .button").first.click()
                assert "Conseguenza" in page.locator(".branch-feedback").inner_text()
            assert page.locator(".source-list a").count()>=3
            page.screenshot(path=str(SHOT/f"published-module-{index+1:02d}-{width}.png"),full_page=False)
        # A complete lesson must be a semantic HTML page on the same site.
        link=page.locator("a.full-lesson-link")
        assert link.get_attribute("href")=="./modulo-05/"
        assert page.locator("#atl-final-glossary").is_visible()
        assert "79 voci" in page.locator("#atl-term-count").inner_text()
        assert page.locator('a[data-atl-glossary-page]').is_visible()
        link.click()
        page.wait_for_url(COURSE+"modulo-05/")
        assert page.locator("h1").count()==1
        assert page.locator(".atl-reading").is_visible()
        assert page.locator(".atl-reading h2").count()>=5
        assert page.locator(".atl-reading pre code").count()>=2
        assert page.locator('link[rel="canonical"]').count()==1
        assert page.get_by_text("Per chi facilita un gruppo",exact=False).count()>=1
        assert page.locator("a.atl-next").count()==1
        glossary_link=page.locator("a.atl-side-glossary-link")
        assert glossary_link.count()==1
        glossary_link.click()
        page.wait_for_url(COURSE+"glossario/")
        assert page.locator("h1").count()==1
        assert page.locator(".term-card").count()==79
        assert "Pedagogia" in page.locator("main").inner_text()
        assert "Metodo MANZO AI" in page.locator("main").inner_text()
        assert not page.evaluate("document.documentElement.scrollWidth>window.innerWidth+2")
        assert not errors,errors
        page.close()
    page=browser.new_page()
    for locale,academy in [("it","academy"),("en","academy"),("es","academia")]:
        page.goto(BASE+locale+"/"+academy+"/",wait_until="domcontentloaded")
        feature=page.locator('section[data-atl-feature="2026-11"]')
        assert feature.count()==1
        href=feature.locator("a.atl-feature-cta").get_attribute("href")
        assert href=="/manzo-ai/it/formazione/ia-per-la-didattica/"
        assert page.locator('article[data-ma-course-card="1"]').count()==0 or page.locator('article[data-ma-course-card="1"]').count()==6
    page.close()
    browser.close()
print("PASS public teaching course: 5 decision trees, theory probes, 5 lesson routes, Academy IT/EN/ES, 390/1440px")
