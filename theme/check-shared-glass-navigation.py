#!/usr/bin/env python3
"""Release gate for the shared glass-pill navigation skin.

Checks asset parity and link injection across public Academy, course and research
pages without changing page content, sidebar routes, or account-only surfaces.
"""
from __future__ import annotations
import argparse
from pathlib import Path

ROOT=Path(__file__).resolve().parent
MARKER="MANZO AI · universal glass-pill sidebar navigation"
MOBILE="MANZO AI · mobile drawer glass-pill companion"
ROUTES=(
    "it/academy",
    "en/academy",
    "es/academia",
    "it/impara/allucinazioni-ai-verificabilita",
    "it/ricerca/acr",
)
SELECTORS=(
    '.rail .nav-link[aria-current="page"]',
    '.rail .nav-link:is(:hover,:focus-visible)',
)
SAFE=(
    "@media(prefers-reduced-motion:reduce)",
    "@media(prefers-reduced-transparency:reduce)",
    "@media(prefers-contrast:more)",
)
def run(site:Path)->None:
    assets=site/"assets"
    desktop=(assets/"design-system.css").read_text(encoding="utf-8")
    mobile=(assets/"mobile-nav.css").read_text(encoding="utf-8")
    if desktop!=(ROOT/"design-system.css").read_text(encoding="utf-8"):
        raise AssertionError("Shared design stylesheet not staged from source")
    if mobile!=(ROOT/"mobile-nav.css").read_text(encoding="utf-8"):
        raise AssertionError("Mobile stylesheet not staged from source")
    if MARKER not in desktop or MOBILE not in mobile:
        raise AssertionError("Shared glass navigation tokens missing")
    if any(x not in desktop for x in SELECTORS+SAFE):
        raise AssertionError("Desktop state or accessibility fallback missing")
    if any(x not in mobile for x in SAFE):
        raise AssertionError("Mobile accessibility fallback missing")
    if "not([data-product-preview]):not([data-learning-console])" not in desktop:
        raise AssertionError("Product Lab privacy scope not preserved")
    seen=0
    for rel in ROUTES:
        page=site/rel/"index.html"
        if not page.is_file():
            raise AssertionError("Missing public learning/research route: "+rel)
        html=page.read_text(encoding="utf-8")
        if html.count('data-manzo-design="precision-motion-v1"')!=1:
            raise AssertionError("Shared design link missing or duplicated: "+rel)
        if 'design-system.css?v=' not in html:
            raise AssertionError("Shared CSS cache revision missing: "+rel)
        if 'data-ma-surface=' not in html:
            raise AssertionError("Page missing surface classification: "+rel)
        seen+=1
    print(f"PASS Glass navigation: shared source, both active/hover states, "
          f"keyboard focus, motion/transparency/contrast fallbacks, {seen} public routes. "
          "Product and private console UI excluded.")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--site",required=True,type=Path)
    opts=p.parse_args()
    run(opts.site)
