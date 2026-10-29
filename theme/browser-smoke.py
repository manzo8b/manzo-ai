#!/usr/bin/env python3
"""Real-browser smoke checks of the CSS-only release overlay (Chromium)."""
import sys
from playwright.sync_api import sync_playwright

origin = "http://127.0.0.1:8765/manzo-ai"
pages = [
    "it/", "es/", "en/",
    "it/academy/", "it/risorse/", "it/video-e-slide/",
    "it/pensiero-critico/", "it/pensiero-critico/cruciverba-affidabilita/",
    "it/prompt-mastery/laboratorio-tecnico/",
]
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    try:
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        for path in pages:
            response = page.goto(f"{origin}/{path}", wait_until="domcontentloaded")
            assert response is not None and response.status == 200, path
            assert page.locator("h1").count() == 1, path
            assert page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--cobalt').trim()") == "#244F9B", path
            assert page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--violet').trim()") == "#67439A", path
        page.goto(f"{origin}/it/")
        assert "linear-gradient" in page.locator(".home-hero").evaluate("(e)=>getComputedStyle(e).backgroundImage")
        feature_colors = page.locator(".grid-3>.feature").evaluate_all("(xs)=>xs.map(x=>getComputedStyle(x).backgroundColor)")
        assert len(set(feature_colors)) >= 4, feature_colors
        page.goto(f"{origin}/it/pensiero-critico/")
        challenge_colors = page.locator(".challenge-card").evaluate_all("(xs)=>xs.map(x=>getComputedStyle(x).backgroundColor)")
        assert len(set(challenge_colors)) >= 4, challenge_colors
        page.goto(f"{origin}/it/pensiero-critico/cruciverba-affidabilita/")
        assert page.locator(".cross-cell").count() > 0
        assert page.locator(".cross-scroll").evaluate("(e)=>getComputedStyle(e).overflowX") == "auto"
        assert not errors, errors
        mobile = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True)
        for path in pages:
            response = mobile.goto(f"{origin}/{path}", wait_until="domcontentloaded")
            assert response is not None and response.status == 200, path
            assert mobile.locator("h1").is_visible(), path
            # Crosswords may overflow inside their scrollable container but not on the body.
            assert mobile.evaluate("document.documentElement.scrollWidth <= innerWidth + 2"), "mobile overflow: "+path
        print("Chromium smoke: 9 page types, three languages, real colors and mobile layout OK.")
    finally:
        browser.close()
