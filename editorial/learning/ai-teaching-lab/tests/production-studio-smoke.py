#!/usr/bin/env python3
"""Exercise production studio and its actual exported artifacts in Chromium.
This validates a local authoring path, not educational outcomes or full WCAG.
"""
import base64
import json
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE="http://127.0.0.1:8766/editorial/learning/ai-teaching-lab/preview/laboratorio-multimediale/"
PNG=base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9f8agPkAAAAASUVORK5CYII=")

with tempfile.TemporaryDirectory() as directory:
    tmp=Path(directory)
    image=tmp/"didattica.png"
    image.write_bytes(PNG)
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(headless=True,args=["--use-fake-ui-for-media-stream","--use-fake-device-for-media-stream"])
        for width in (390,1440):
            page=browser.new_page(viewport={"width":width,"height":900},accept_downloads=True,reduced_motion="reduce")
            errors=[]
            page.on("pageerror",lambda error:errors.append(str(error)))
            page.goto(BASE,wait_until="networkidle")
            assert "Laboratorio di produzione" in page.title() or "Studio multimediale" in page.title()
            assert page.locator(".studio-phase").count()==5
            assert page.locator("#studio-progress-text").inner_text()=="Fase 1 di 5"
            assert page.locator("#studio-form").count()==1
            assert page.locator(".studio-phase-switcher").count()==1
            if width<=760:
                assert not page.locator(".studio-phase-switcher").evaluate("(node)=>node.open")
                page.locator(".studio-phase-switcher > summary").click()
                assert page.locator("#studio-steps button").first.is_visible()
                page.locator(".studio-phase-switcher > summary").click()
            else:
                assert page.locator(".studio-phase-switcher").evaluate("(node)=>node.open")
            assert page.locator('input[name="title"]').input_value()=="Una giornata fredda cambia il clima?"
            assert not page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 2"), page.evaluate("""() => ({
                inner:innerWidth,
                scroll:document.documentElement.scrollWidth,
                overflow:[...document.querySelectorAll('body *')].filter(e=>{
                    const r=e.getBoundingClientRect();
                    return r.right>innerWidth+2 && getComputedStyle(e).position!=='absolute';
                }).slice(0,12).map(e=>({tag:e.tagName,class:e.className,id:e.id,scroll:e.scrollWidth,right:e.getBoundingClientRect().right}))
            })""")

            # Brief to model selection
            page.locator("#studio-next").click()
            assert page.locator("#studio-progress-text").inner_text()=="Fase 2 di 5"
            assert page.locator(".studio-model-card").count()>=2
            assert "ChatGPT" in page.locator(".studio-models").inner_text()
            assert "Nano Banana" in page.locator(".studio-models").inner_text()
            page.locator("#studio-medium").select_option("audio")
            assert "NotebookLM" in page.locator(".studio-models").inner_text()
            page.locator("#studio-medium").select_option("slides")
            page.locator("#studio-next").click()

            # Scene editing and a real local image import
            assert page.locator(".studio-scene-editor").count()==3
            page.locator('[data-scene="0"] [data-field="title"]').fill("Da una domanda a un metodo")
            page.locator('[data-scene="0"] input[type="file"]').set_input_files(str(image))
            page.locator('[data-scene="0"] div.studio-file-state').get_by_text("Immagine pronta",exact=False).wait_for(timeout=10000)
            # Prompt that can be copied into an authorized external AI model.
            page.locator('[data-scene="0"] .studio-scene-tools button').nth(1).click()
            assert "16:9" in page.locator('[data-scene="0"] .studio-prompt-output').input_value()
            assert "niente dati o grafici inventati" in page.locator('[data-scene="0"] .studio-prompt-output').input_value()
            # Produce a real PNG with the text of scene 2; it is attached to the kit.
            page.locator(".studio-scene-disclosure").nth(1).locator("summary").click()
            page.locator('[data-scene="1"] .studio-scene-tools button').first.click()
            assert page.locator('[data-scene="1"] .studio-generated-image').is_visible()
            assert page.locator('[data-scene="1"] .studio-generated-image').get_attribute("src").startswith("data:image/png;base64,")
            with page.expect_download() as generated:
                page.locator('[data-scene="1"] .studio-scene-tools button').nth(2).click()
            graphic=tmp/f"generated-{width}.png"
            generated.value.save_as(str(graphic))
            assert graphic.read_bytes()[:8]==bytes.fromhex("89504e470d0a1a0a")
            assert graphic.stat().st_size>2000
            page.locator("#studio-next").click()

            # Script, quiz, all six formats are recognized and separate.
            assert page.locator('textarea[name="script"]').count()==1
            assert page.locator('textarea[name="quiz_question"]').count()==1
            page.locator('textarea[name="script"]').fill("")
            page.locator("#studio-script-draft").click()
            assert "Marta:" in page.locator('textarea[name="script"]').input_value()
            assert "Davide:" in page.locator('textarea[name="script"]').input_value()
            # The microphone is optional and explicitly controlled by the user.
            assert page.locator("#studio-record-start").count()==1
            assert page.locator("#studio-record-stop").count()==1
            if page.locator("#studio-record-start").is_enabled():
                page.locator("#studio-record-start").click()
                page.locator("#studio-record-stop").wait_for(state="visible")
                if page.locator("#studio-record-stop").is_enabled():
                    page.wait_for_timeout(900)
                    page.locator("#studio-record-stop").click()
                    page.locator("#studio-record-download").wait_for(state="enabled",timeout=8000)
                    assert page.locator("#studio-record-preview").is_visible()
                    with page.expect_download() as audio_export:
                        page.locator("#studio-record-download").click()
                    audio_file=tmp/f"narration-{width}"
                    audio_export.value.save_as(str(audio_file))
                    assert audio_file.stat().st_size>1000
            # Produce a silent video from the storyboard only where the browser supports it.
            assert page.locator("#studio-video-create").count()==1
            if page.locator("#studio-video-create").is_enabled():
                page.locator("#studio-video-seconds").select_option("2")
                page.locator("#studio-video-create").click()
                page.locator("#studio-video-download").wait_for(state="enabled",timeout=24000)
                assert page.locator("#studio-video-preview").is_visible()
                with page.expect_download() as video_export:
                    page.locator("#studio-video-download").click()
                video_file=tmp/f"clip-{width}"
                video_export.value.save_as(str(video_file))
                assert video_file.stat().st_size>3000
            page.locator("#studio-next").click()
            assert page.locator("#studio-progress-text").inner_text()=="Fase 5 di 5"
            assert page.locator(".studio-preview-card").count()==3
            assert page.locator(".studio-preview-card img").count()==2
            assert "Da una domanda a un metodo" in page.locator(".studio-preview").inner_text()
            assert not page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 2"), page.evaluate("""() => ({
                inner:innerWidth,
                scroll:document.documentElement.scrollWidth,
                overflow:[...document.querySelectorAll('body *')].filter(e=>{
                    const r=e.getBoundingClientRect();
                    return r.right>innerWidth+2 && getComputedStyle(e).position!=='absolute';
                }).slice(0,12).map(e=>({tag:e.tagName,class:e.className,id:e.id,scroll:e.scrollWidth,right:e.getBoundingClientRect().right}))
            })""")

            # Quality gate prevents falsely claiming readiness.
            page.locator("#studio-download-html").click()
            assert "checklist" in page.locator("#studio-status").inner_text().lower()
            for box in page.locator('input[name="quality"]').all():
                box.check()

            # Export an editable JSON project with media embedded.
            with page.expect_download() as event:
                page.locator("#studio-download-json").click()
            project_path=tmp/f"project-{width}.json"
            event.value.save_as(str(project_path))
            data=json.loads(project_path.read_text(encoding="utf-8"))
            assert data["schema"]=="manzo-ai-multimedia-studio-v1"
            assert len(data["scenes"])==3
            assert data["scenes"][0]["title"]=="Da una domanda a un metodo"
            assert data["scenes"][0]["image"].startswith("data:image/png;base64,")
            assert data["scenes"][1]["image"].startswith("data:image/png;base64,")

            # Export and *run* a standalone learning object offline.
            with page.expect_download() as event:
                page.locator("#studio-download-html").click()
            lesson=tmp/f"microlezione-{width}.html"
            event.value.save_as(str(lesson))
            html=lesson.read_text(encoding="utf-8")
            assert '<div id="slides"' in html
            assert "quiz-answers" in html
            assert "data:image/png;base64," in html
            offline=browser.new_page(viewport={"width":width,"height":900})
            offline_errors=[]
            offline.on("pageerror",lambda error:offline_errors.append(str(error)))
            offline.goto(lesson.as_uri(),wait_until="load")
            assert offline.locator(".slide").count()==3
            assert offline.locator(".slide:visible").count()==1
            offline.locator("#next").click()
            assert "2 / 3" in offline.locator("#slide-counter").inner_text()
            offline.locator('#quiz-answers input[value="1"]').check()
            offline.locator("#evaluate").click()
            assert "Esatto" in offline.locator("#result").inner_text()
            assert not offline_errors,offline_errors
            assert not offline.evaluate("document.documentElement.scrollWidth > window.innerWidth + 2")
            offline.close()

            # Imported file really restores the changed slide and embedded image.
            page.goto(BASE,wait_until="networkidle")
            page.locator("#studio-import").set_input_files(str(project_path))
            assert "Progetto importato" in page.locator("#studio-status").inner_text()
            if width<=760: page.locator(".studio-phase-switcher > summary").click()
            page.locator('#studio-steps button[data-go="2"]').click()
            assert page.locator('[data-scene="0"] [data-field="title"]').input_value()=="Da una domanda a un metodo"
            assert "Immagine caricata" in page.locator('[data-scene="0"] div.studio-file-state').inner_text()
            assert not errors,errors
            page.close()
        browser.close()
print("PASS production studio: 5 phases, real PNG creation, prompts, local recording/video if available, HTML/JSON, offline quiz, mobile and desktop")
