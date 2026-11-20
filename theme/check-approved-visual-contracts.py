#!/usr/bin/env python3
"""Sprint 2 MANZO AI release gate: protect approved visual/editorial components.

Read-only QA on the FINAL GitHub Pages bundle, after all course and Home
publishers. Does not impose a new design or rewrite content.
"""
from __future__ import annotations

import argparse
from html import unescape
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
LOCALES = {"it": "academy", "en": "academy", "es": "academia"}
ACADEMY_CARD = re.compile(
    r'<article\b(?=[^>]*\bdata-ma-course-card=["\']1["\'])[^>]*>.*?</article\s*>',
    re.I | re.S,
)
HOME_CARD = re.compile(
    r'<article\b(?=[^>]*\bdata-ma-v2-card=["\'][1-6]["\'])[^>]*>.*?</article\s*>',
    re.I | re.S,
)
TITLE = re.compile(r'<h([1-6])\b[^>]*>(.*?)</h\1>', re.I | re.S)
TEXT = re.compile(r'<[^>]+>')
SHEETS = (
    ("assets/design-system.css", "theme/design-system.css"),
    ("assets/mobile-nav.css", "theme/mobile-nav.css"),
    ("assets/home-magic-v2.css", "theme/home-magic-v2.css"),
    ("assets/academy-journeys.css", "theme/academy-journeys.css"),
    ("assets/learning-experience/guide.css", "product/learning-experience/guide.css"),
)


def check(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def text(html: str) -> str:
    return unescape(TEXT.sub("", html)).strip()


def inspect(site: Path) -> None:
    # Protect one common interaction system and its keyboard/motion alternatives.
    for staged, original in SHEETS:
        target, source = site / staged, BASE.parent / original
        check(target.is_file() and source.is_file(),
              "Missing approved stylesheet: " + staged)
        check(target.read_bytes() == source.read_bytes(),
              "Visual source drift: " + staged)
        css = target.read_text(encoding="utf-8")
        check(":focus-visible" in css and "prefers-reduced-motion:reduce" in css,
              "Missing accessible interaction fallback: " + staged)

    checked = 0
    for locale, segment in LOCALES.items():
        home = (site / locale / "index.html").read_text(encoding="utf-8")
        academy = (site / locale / segment / "index.html").read_text(encoding="utf-8")
        check('data-ma-surface="landing"' in home,
              "Missing branded Home surface: " + locale)
        check('data-ma-surface="learning"' in academy,
              "Missing Academy design surface: " + locale)
        check("assets/learning-experience/guide.css" in home and
              "assets/learning-experience/guide.css" in academy,
              "Home/Academy must share the approved course card CSS: " + locale)

        original = ACADEMY_CARD.findall(academy)
        featured = HOME_CARD.findall(home)
        check(len(original) == len(featured) == 6,
              "Exactly six native Academy cards expected: " + locale)
        for number, (src, displayed) in enumerate(zip(original, featured), 1):
            expected = re.sub(
                r"<article\b", f'<article data-ma-v2-card="{number}"',
                src, count=1, flags=re.I,
            )
            check(displayed == expected,
                  f"{locale}: Home card {number} differs from the Academy source")
            headings = TITLE.findall(src)
            check(len(headings) == 1 and headings[0][0] == "3" and
                  text(headings[0][1]) and not text(headings[0][1]).endswith("."),
                  f"{locale}: invalid Academy card title {number}")
            check(src.count('class="ma-course-cta"') == 1 and
                  src.count('class="ma-course-link"') == 1,
                  f"{locale}: approved single-link card/CTA contract lost {number}")
            checked += 1

        for title in TITLE.findall(home) + TITLE.findall(academy):
            check(not text(title[1]).endswith("."),
                  f"{locale}: terminal full stop reintroduced in a heading")
        title_tag = re.search(r"<title\b[^>]*>(.*?)</title\s*>", home, re.I | re.S)
        check(title_tag is not None and
              not text(title_tag.group(1).partition("|")[0]).endswith("."),
              "Home SEO headline ends with a forbidden full stop: " + locale)

        # The mobile entry point is the course catalog, not the teaching promotion.
        positions = [academy.find(value) for value in (
            'data-ma-pathways="v1"',
            'data-ma-journeys="v1"',
            'data-atl-feature="2026-11"',
        )]
        check(-1 not in positions and positions == sorted(positions) and
              len(set(positions)) == 3,
              "Academy catalog/paths/specialist order changed: " + locale)

    print("PASS Sprint 2 visual contract: 3 Home + 3 Academy, "
          f"{checked} canonical card instances, original CSS parity, "
          "keyboard focus, reduced motion, editorial punctuation and catalog-first UX")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--site", required=True, type=Path)
    inspect(p.parse_args().site)
