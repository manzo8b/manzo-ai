#!/usr/bin/env python3
"""Browser QA for the real six-card Academy showcase on trilingual homepages.

Run against the same static release served at 127.0.0.1:8765/manzo-ai/.
No login, database connection, analytics, trackers or invented course data.
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8765/manzo-ai"
DEST = Path("design-review-screenshots")
LOCALES = {"it": "academy", "en": "academy", "es": "academia"}


def assert_home(page, locale, academy_route, width):
    url = f"{BASE}/{locale}/"
    response = page.goto(url, wait_until="domcontentloaded")
    assert response and response.status == 200, url
    root = page.locator('[data-ma-home-showcase="v1"]')
    assert root.count() == 1, f"Missing home showcase {locale}"
    assert root.locator("h2").count() == 1
    assert not root.locator("h2").inner_text().rstrip().endswith("."), "Title ends with punctuation"
    cards = root.locator("[data-ma-course-card='1']")
    assert cards.count() == 6, f"{locale}: expected six Academy cards"
    assert page.locator(".home-hero").count() == 1
    assert page.locator(".home-hero input").count() >= 1, "Existing search lost"
    assert page.locator(".ma-product-scene").count() == 0, "Obsolete technical scene still present"
    assert page.locator(".ma-home-showcase .ma-course-card.ma-tone-blue").count() == 1
    assert page.locator(".ma-home-showcase .ma-course-card.ma-tone-navy").count() == 1
    assert page.locator(".ma-home-showcase .ma-course-art").count() == 6
    assert root.locator(f'a[href="/manzo-ai/{locale}/{academy_route}/"]').count() == 1

    for card in cards.all():
        heading = card.locator("h3")
        assert heading.count() == 1 and heading.inner_text().strip()
        link = card.locator("a.ma-course-link")
        href = link.get_attribute("href")
        assert href and href.startswith(f"/manzo-ai/{locale}/"), href
        assert link.is_visible()
        assert card.locator(".ma-course-facts").count() == 1, f"Missing course facts: {href}"

    first_art = root.locator(".ma-course-card").first.locator(".ma-course-art")
    background = first_art.evaluate("(el)=>getComputedStyle(el).backgroundColor")
    assert background == "rgb(33, 88, 237)", f"Academy palette not reused {background}"
    over = page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 2")
    assert not over, f"Horizontal overflow {locale}/{width}"
    assert root.bounding_box() and root.bounding_box()["width"] > 280

    if width == 1440:
        first = root.locator(".ma-course-card").first
        first.hover()
        page.wait_for_timeout(460)
        transform = first.evaluate("(el)=>getComputedStyle(el).transform")
        assert transform != "none", f"Hover effect lost {locale}"
        first.locator("a").focus()
        assert first.locator("a").evaluate("(el)=>el===document.activeElement")
    DEST.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(DEST / f"home-academy-{locale}-{width}.png"), full_page=True)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for locale, academy_route in LOCALES.items():
            for width, height in [(1440, 900), (390, 844)]:
                page = browser.new_page(viewport={"width": width, "height": height})
                assert_home(page, locale, academy_route, width)
                page.close()
        page = browser.new_page(viewport={"width": 1440, "height": 900},
                                reduced_motion="reduce")
        page.goto(f"{BASE}/it/", wait_until="domcontentloaded")
        first = page.locator(".ma-home-showcase .ma-course-card").first
        first.hover()
        page.wait_for_timeout(100)
        assert first.evaluate("(el)=>getComputedStyle(el).transform") == "none"
        page.close()
        browser.close()
    print("PASS: home Academy showcase IT/EN/ES, six real cards, mobile, motion, links")


if __name__ == "__main__":
    main()
