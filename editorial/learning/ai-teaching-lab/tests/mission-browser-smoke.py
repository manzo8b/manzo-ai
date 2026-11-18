#!/usr/bin/env python3
"""Mission brief round-trip, honest status and computed post-build contrast.

WebKit automation is not a test on a physical iPhone or Safari application.
"""
import json
import os
import re
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

BASE = os.environ.get("ATL_TOOLS_BASE", "http://127.0.0.1:8767/manzo-ai/it/formazione/ia-per-la-didattica/")
ENGINE = os.environ.get("ATL_BROWSER", "chromium")
SHOT = Path("ai-teaching-lab-screenshots")
SHOT.mkdir(exist_ok=True)


def luminance(rgb):
    channels = [v / 255 for v in rgb]
    channels = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in channels]
    return sum(v * w for v, w in zip(channels, (.2126, .7152, .0722)))


def rgb(value):
    return [int(x) for x in re.findall(r"[\d.]+", value)[:3]]


def contrast(a, b):
    light, dark = sorted([luminance(a), luminance(b)], reverse=True)
    return (light + .05) / (dark + .05)


with tempfile.TemporaryDirectory() as directory, sync_playwright() as p:
    browser = getattr(p, ENGINE).launch(headless=True)
    for width in (320, 375, 390, 430, 768, 1024, 1440):
        page = browser.new_page(viewport={"width": width, "height": 900}, reduced_motion="reduce", accept_downloads=True)
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("dialog", lambda dialog: dialog.accept())
        assert page.goto(BASE + "inizia/", wait_until="networkidle").status == 200
        assert not page.evaluate("document.documentElement.scrollWidth > innerWidth + 2"), width
        assert page.locator('link[rel="canonical"]').count() == 1
        # Inspect computed colors after the global theme has been injected.
        colors = page.locator(".mission-finish").evaluate("""node => ({
            background: getComputedStyle(node).backgroundImage,
            heading: getComputedStyle(node.querySelector('h2')).color,
            text: getComputedStyle(node.querySelector('p')).color,
            button: getComputedStyle(node.querySelector('a')).color,
            buttonBackground: getComputedStyle(node.querySelector('a')).backgroundColor
        })""")
        stops = re.findall(r"rgb\([^)]*\)", colors["background"])
        assert len(stops) >= 2, colors
        for text in (colors["heading"], colors["text"]):
            assert min(contrast(rgb(text), rgb(stop)) for stop in stops) >= 4.5, colors
        assert contrast(rgb(colors["button"]), rgb(colors["buttonBackground"])) >= 4.5, colors
        for kind, target in (("image", "studio-immagini"), ("voice", "studio-voce"), ("video", "studio-video"), ("verify", "modulo-02")):
            page.locator(f'[data-kind="{kind}"]').click()
            assert page.locator("#studio-link").get_attribute("href") == f"../{target}/"
        page.locator("#topic").fill("Triangoli ruotati — prova sintetica")
        page.locator("#objective").fill("Distinguere tre lati da quattro e motivare la scelta")
        page.locator('[data-minutes="45"]').click()
        with page.expect_download() as event:
            page.locator("#export").click()
        file = Path(directory) / f"mission-{width}.json"
        event.value.save_as(str(file))
        data = json.loads(file.read_text())
        assert data["schema"] == "ai-teaching-lab-mission-v0.1"
        assert data["approval"] is False and data["minutes"] == 45
        page.locator("#topic").fill("Una modifica provvisoria")
        page.locator(".resume > summary").click()
        page.locator("#restore").set_input_files(str(file))
        expect(page.locator("#form-status")).to_contain_text("Bozza ripristinata")
        assert page.locator("#topic").input_value() == data["topic"]
        page.locator("#restore").set_input_files({"name": "unknown.json", "mimeType": "application/json", "buffer": b'{"schema":"unknown"}'})
        expect(page.locator("#form-status")).to_contain_text("Formato non riconosciuto")
        assert page.locator("#topic").input_value() == data["topic"]
        for field in page.locator("input:not([type=file]),textarea,select").all():
            assert field.evaluate("n=>parseFloat(getComputedStyle(n).fontSize)") >= 16
        page.locator(".mission-finish").scroll_into_view_if_needed()
        page.screenshot(path=str(SHOT / f"mission-finish-{ENGINE}-{width}.png"))
        assert not errors, errors
        page.close()
    browser.close()
print(f"PASS Mission Studio {ENGINE}: 7 widths, 4 routes, JSON round-trip, negative schema, computed CTA contrast")
