#!/usr/bin/env python3
"""Exercise the four published tools with synthetic files and real downloads.

Approval clicks simulate declarations for software QA; they are not evidence of
a teacher's review, educational efficacy, Safari/iPhone or WCAG conformance.
"""
import base64
import copy
import io
import json
import os
import tempfile
import wave
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

BASE = os.environ.get("ATL_TOOLS_BASE", "http://127.0.0.1:8767/manzo-ai/it/formazione/ia-per-la-didattica/")
ENGINE = os.environ.get("ATL_BROWSER", "chromium")
PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9f8agPkAAAAASUVORK5CYII=")
REVIEWER = "Revisore sintetico QA"


def synthetic_audio():
    # A silent PCM fixture, not a person's voice or a narrated lesson.
    out = io.BytesIO()
    with wave.open(out, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(8000)
        wav.writeframes(b"\x00\x00" * 8000)
    return out.getvalue()


def upload_json(page, selector, value, name="fixture.json"):
    page.locator(selector).set_input_files({"name": name, "mimeType": "application/json", "buffer": json.dumps(value).encode()})


def download(page, selector, destination):
    with page.expect_download() as event:
        page.locator(selector).click()
    event.value.save_as(str(destination))
    assert destination.stat().st_size > 0
    return destination


def export_json(page, destination, selector="#export"):
    return json.loads(download(page, selector, destination).read_text())


def fill(page, values):
    for name, value in values.items():
        page.locator("#" + name).fill(value)


def review(page, prefix="c", reviewer="reviewer"):
    page.locator("#" + reviewer).fill(REVIEWER)
    for index in range(1, 5):
        page.locator(f"#{prefix}{index}").check()


def approved(page):
    page.locator("#approve").click()
    expect(page.locator("#decision")).to_contain_text("pprovato")


with tempfile.TemporaryDirectory() as directory, sync_playwright() as playwright:
    tmp = Path(directory)
    browser = getattr(playwright, ENGINE).launch(headless=True)
    for width in (390, 1440):
        context = browser.new_context(viewport={"width": width, "height": 900}, accept_downloads=True, reduced_motion="reduce")
        errors = []
        dialogs = []
        pages = []
        responses = {"accept": True}

        def open_tool(route):
            page = context.new_page()
            pages.append(page)
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("dialog", lambda dialog: (dialogs.append(dialog.message), dialog.accept() if responses["accept"] else dialog.dismiss()))
            response = page.goto(BASE + route + "/", wait_until="networkidle")
            assert response.status == 200
            return page

        # Image: valid local file -> declaration -> JSON -> invalidation.
        image = open_tool("studio-immagini")
        image.locator("#guided-demo").click()
        image.locator("#t4").click()
        image.locator("#upload").set_input_files({"name": "synthetic.png", "mimeType": "image/png", "buffer": PNG})
        image.wait_for_function("document.querySelector('#preview img')?.naturalWidth > 0")
        image.locator("#origin").select_option("local")
        image.locator("#alt").fill("Pixel sintetico per verificare il caricamento, non una risorsa didattica")
        image.locator("#t5").click()
        review(image, "r", "teacher")
        approved(image)
        image_json = export_json(image, tmp / f"image-{width}.json")
        assert image_json["approval"]["approved"] is True
        assert image_json["image"]["name"] == "synthetic.png"
        image.locator("#t1").click()
        image.locator("#title").fill("Revisione sintetica")
        image.locator("#t5").click()
        assert export_json(image, tmp / "changed-image.json")["approval"]["approved"] is False

        # Voice: PCM fixture with no speech, explicitly documented as such.
        voice = open_tool("studio-voce")
        voice.locator("#guided-demo").click()
        voice.locator("#t2").click()
        voice.locator("#script").fill("Fixture audio sintetica senza parole, usata solo per QA")
        voice.locator("#t3").click()
        voice.locator("#file").set_input_files({"name": "synthetic.wav", "mimeType": "audio/wav", "buffer": synthetic_audio()})
        expect(voice.locator("#audioinfo")).to_contain_text("synthetic.wav")
        voice.locator("#origin").select_option("external_other")
        voice.locator("#source").fill("PCM generato dal test; nessuna registrazione umana")
        voice.locator("#t4").click()
        voice.locator("#transcript").fill("[Silenzio sintetico, nessuna parola pronunciata]")
        voice.locator("#t5").click()
        review(voice)
        approved(voice)
        voice_json = export_json(voice, tmp / f"voice-{width}.json")
        assert voice_json["audio"]["name"] == "synthetic.wav"
        voice.locator("#t4").click()
        voice.locator("#transcript").fill("Trascrizione modificata: controllo da ripetere")
        voice.locator("#t5").click()
        assert export_json(voice, tmp / "changed-voice.json")["approval"]["approved"] is False

        # Video: real scene image imports, provenance, separate WebVTT and JSON.
        video = open_tool("studio-video")
        video.locator("#guided-demo").click()
        video.locator("#t2").click()
        video.locator("#example").click()
        assert video.locator("#scenes .scene").count() == 3
        for index in range(3):
            scene = video.locator("#scenes .scene").nth(index)
            scene.locator("input[type=file]").set_input_files({"name": f"scene-{index}.png", "mimeType": "image/png", "buffer": PNG})
            expect(video.locator("#scenes .scene").nth(index).locator("img")).to_be_visible()
            scene = video.locator("#scenes .scene").nth(index)
            scene.locator("select").select_option("local")
            scene.locator("input[type=number]").fill("2")
            scene.locator("input[type=number]").dispatch_event("change")
        video.locator("#t4").click()
        video.locator("#captionDraft").click()
        video.locator("#access").fill("Tre immagini fixture; alternativa testuale completa nelle didascalie")
        vtt = download(video, "#vtt", tmp / f"captions-{width}.vtt").read_text()
        assert vtt.startswith("WEBVTT") and vtt.count(" --> ") == 3
        assert "00:00:06.000" in vtt
        video.locator("#t5").click()
        review(video)
        approved(video)
        video_json = export_json(video, tmp / f"video-{width}.json")
        assert len(video_json["scenes"]) == 3
        assert all(s["imageName"] == f"scene-{i}.png" for i, s in enumerate(video_json["scenes"]))

        # WebM where available; explicit fallback is also a legitimate result.
        video.locator("#t3").click()
        if video.locator("#render").is_enabled():
            supported = video.evaluate("typeof MediaRecorder !== 'undefined' && ['video/webm;codecs=vp8','video/webm'].some(t=>MediaRecorder.isTypeSupported(t)) && !!HTMLCanvasElement.prototype.captureStream")
            if supported:
                clip = download(video, "#render", tmp / f"silent-{width}.webm")
                assert clip.stat().st_size > 1000
                expect(video.locator("#renderStatus")).to_contain_text("silenzioso")
            else:
                video.locator("#render").click()
                expect(video.locator("#renderStatus")).to_contain_text("supportat")
        video.locator("#t1").click()
        video.locator("#objective").fill("Obiettivo aggiornato dopo la verifica")
        video.locator("#t5").click()
        assert export_json(video, tmp / "changed-video.json")["approval"]["approved"] is False

        workspace = open_tool("workspace-multimediale")
        workspace.locator("#sample-brief").click()
        workspace.locator("#wk-all").click()
        for data in (image_json, voice_json, video_json):
            upload_json(workspace, "#jsonfile", data)
            expect(workspace.locator("#importstatus")).to_contain_text("importata localmente")
        assert workspace.locator("#modules .module").count() == 3
        replacement = copy.deepcopy(image_json)
        replacement["fields"]["title"] = "Sostituzione da annullare"
        responses["accept"] = False
        upload_json(workspace, "#jsonfile", replacement)
        workspace.wait_for_timeout(100)
        assert "Sostituzione da annullare" not in workspace.locator("#modules").inner_text()
        responses["accept"] = True
        review(workspace)
        workspace.locator("#date").fill("2026-11-18")
        approved(workspace)
        manifest = export_json(workspace, tmp / f"kit-{width}.json", "#exportJSON")
        assert manifest["approval"]["approved"] is True
        assert manifest["assets"]["video"]["media"]["scenes"][2]["imageName"] == "scene-2.png"
        html_file = download(workspace, "#exportHTML", tmp / f"kit-{width}.html")
        html = html_file.read_text()
        assert "Provenienza e file" in html and "scene-2.png" in html
        offline = context.new_page()
        offline.goto(html_file.as_uri())
        assert offline.locator("h1").count() == 1
        offline.close()

        # Reopen exported v0.1: metadata survive, final decision must be new.
        upload_json(workspace, "#kitfile", manifest)
        expect(workspace.locator("#restorestatus")).to_contain_text("Bozza ripristinata")
        restored = export_json(workspace, tmp / "restored.json", "#exportJSON")
        assert restored["approval"]["approved"] is False
        assert not any(restored["review"]["checks"].values())
        assert restored["assets"]["video"]["media"] == manifest["assets"]["video"]["media"]

        # Negative imports are atomic and do not remove the current project.
        for invalid in ({"schema": "unknown"}, {"schema": manifest["schema"], "assets": []}):
            upload_json(workspace, "#kitfile", invalid)
            expect(workspace.locator("#restorestatus")).to_contain_text("non riuscito")
            assert workspace.locator("#title").input_value() == manifest["title"]
        broken = copy.deepcopy(image_json)
        broken["review"] = {"r1": False, "r2": False, "r3": False, "r4": False}
        upload_json(workspace, "#jsonfile", broken)
        expect(workspace.locator("#importstatus")).to_contain_text("non riuscita")
        missing = copy.deepcopy(image_json)
        missing["image"] = None
        upload_json(workspace, "#jsonfile", missing)
        expect(workspace.locator("#importstatus")).to_contain_text("non riuscita")
        forged = copy.deepcopy(manifest)
        forged["assets"]["image"]["review"] = 0
        upload_json(workspace, "#kitfile", forged)
        expect(workspace.locator("#restorestatus")).to_contain_text("non riuscito")
        workspace.locator("#jsonfile").set_input_files({"name": "broken.json", "mimeType": "application/json", "buffer": b"{malformed"})
        expect(workspace.locator("#importstatus")).to_contain_text("non riuscita")
        workspace.locator("#jsonfile").set_input_files({"name": "large.json", "mimeType": "application/json", "buffer": b" " * (2 * 1024 * 1024 + 1)})
        expect(workspace.locator("#importstatus")).to_contain_text("superiore a 2 MB")
        assert workspace.locator("#modules .module").count() == 3
        # Browser leave warning: editing after export must not be silently lost.
        image.locator("#t1").click()
        image.locator("#title").fill("Modifica non esportata")
        before = len(dialogs)
        image.goto(BASE, wait_until="domcontentloaded")
        assert len(dialogs) > before, "Missing beforeunload warning for unsaved work"
        assert not errors, errors
        print(f"PASS {ENGINE} {width}px: 3 media schemas, approval invalidation, VTT/WebM fallback, workspace JSON/HTML, v0.1 restore, negative imports")
        context.close()
    browser.close()
