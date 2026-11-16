#!/usr/bin/env python3
"""Add MANZO AI's *existing* six Academy cards to the trilingual homepages.

All titles, destinations, teaching formats and lesson facts are extracted from
the published Academy, not duplicated editorial data or synthetic SaaS records.
This is a static, reversible presentation layer; Supabase Auth is unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
from html import escape
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parent
STYLE = ROOT / "home-showcase.css"
ACADEMY_STYLE = "assets/learning-experience/guide.css"
MARKER = 'data-ma-home-showcase="v1"'
PREFIX = "/manzo-ai/"

LOCALES = {
    "it": {
        "academy": "it/academy",
        "eyebrow": "MANZO AI / ACADEMY",
        "heading": "Dalla curiosità alla competenza",
        "description": "Percorsi completi, lezioni pratiche e strumenti di verifica. Le stesse risorse dell'Academy, disponibili subito e senza registrazione",
        "count": "6 risorse pubblicate",
        "language": "IT / EN / ES",
        "cta": "Esplora tutta l'Academy",
        "note": "Corsi e lezioni aperti · Learning B2B su invito, separato dal catalogo pubblico",
    },
    "en": {
        "academy": "en/academy",
        "eyebrow": "MANZO AI / ACADEMY",
        "heading": "Turn curiosity into capability",
        "description": "Complete learning paths, practical lessons and verification skills. The same Academy resources, available immediately without signing up",
        "count": "6 published resources",
        "language": "IT / EN / ES",
        "cta": "Explore the full Academy",
        "note": "Open courses and lessons · Invite-only Learning B2B is separate from the public catalog",
    },
    "es": {
        "academy": "es/academia",
        "eyebrow": "MANZO AI / ACADEMY",
        "heading": "De la curiosidad a la competencia",
        "description": "Recorridos completos, lecciones prácticas y herramientas de verificación. Los mismos recursos de la Academia, sin necesidad de registrarte",
        "count": "6 recursos publicados",
        "language": "IT / EN / ES",
        "cta": "Explorar toda la Academia",
        "note": "Cursos y lecciones abiertos · Learning B2B por invitación es independiente del catálogo público",
    },
}

CARD = re.compile(
    r"<article\b(?=[^>]*\bdata-ma-course-card=[\"']1[\"'])[^>]*>.*?</article\s*>",
    re.IGNORECASE | re.DOTALL,
)
COURSE_LINK = re.compile(r'<a\b[^>]*\bhref="([^"]+)"', re.IGNORECASE)
HOME_HERO = re.compile(
    r'<section\b[^>]*\bclass=["\'][^"\']*\bhome-hero\b[^"\']*["\'][^>]*>',
    re.IGNORECASE | re.DOTALL,
)
CLOSE_SECTION = re.compile(r"</?section\b[^>]*>", re.IGNORECASE | re.DOTALL)


def home_hero_end(html: str) -> int:
    match = HOME_HERO.search(html)
    if not match:
        raise RuntimeError("The existing home hero was not found")
    depth = 1
    for token in CLOSE_SECTION.finditer(html, match.end()):
        if token.group().startswith("</"):
            depth -= 1
        else:
            depth += 1
        if depth == 0:
            return token.end()
    raise RuntimeError("Unbalanced home hero section")


def cards_from_academy(site: Path, locale: str) -> list[str]:
    path = site / LOCALES[locale]["academy"] / "index.html"
    if not path.is_file():
        raise RuntimeError(f"Missing Academy source: {path}")
    html = path.read_text(encoding="utf-8")
    cards = CARD.findall(html)
    if len(cards) != 6:
        raise RuntimeError(f"Expected 6 reviewed Academy cards for {locale}, got {len(cards)}")
    seen = set()
    for card in cards:
        links = COURSE_LINK.findall(card)
        if len(links) != 1:
            raise RuntimeError(f"Card should have exactly one primary link: {locale}")
        href = escape(links[0], quote=False)
        if not href.startswith(f"{PREFIX}{locale}/") or not href.endswith("/"):
            raise RuntimeError(f"Unexpected card destination: {href}")
        if href in seen:
            raise RuntimeError(f"Duplicate course link for {locale}: {href}")
        seen.add(href)
        target = site / href.removeprefix(PREFIX) / "index.html"
        if not target.is_file():
            raise RuntimeError(f"Academy card links to missing page: {href}")
        if len(re.findall(r"<h3\b", card, re.IGNORECASE)) != 1:
            raise RuntimeError(f"Academy card has no unique heading: {href}")
    return cards


def section(locale: str, cards: list[str]) -> str:
    d = LOCALES[locale]
    def e(x: str) -> str:
        return escape(x, quote=True)
    return (
        f'<section {MARKER} class="ma-home-showcase" aria-labelledby="ma-home-showcase-title-{locale}">'
        '<div class="ma-home-showcase-intro">'
        '<div class="ma-home-showcase-heading">'
        f'<p class="ma-home-showcase-eyebrow">{e(d["eyebrow"])}</p>'
        f'<h2 id="ma-home-showcase-title-{locale}">{e(d["heading"])}</h2>'
        f'<p class="ma-home-showcase-description">{e(d["description"])}</p>'
        '</div>'
        '<div class="ma-home-showcase-aside" aria-label="Academy">'
        f'<span class="ma-home-showcase-number">{e(d["count"])}</span>'
        f'<span class="ma-home-showcase-language">{e(d["language"])}</span>'
        '</div></div>'
        '<div class="ma-course-grid ma-home-course-grid">'
        + "\n".join(cards)
        + '</div>'
        '<div class="ma-home-showcase-footer">'
        f'<p>{e(d["note"])}</p>'
        f'<a href="{PREFIX}{d["academy"]}/" class="ma-home-showcase-all">{e(d["cta"])}'
        '<span aria-hidden="true">↗</span></a>'
        '</div></section>'
    )


def publish(site: Path, verify_only: bool = False) -> None:
    if not (site / ACADEMY_STYLE).is_file():
        raise RuntimeError("Academy card stylesheet missing")
    if not STYLE.is_file():
        raise RuntimeError("Home showcase source CSS missing")
    asset = site / "assets" / STYLE.name
    if not verify_only:
        asset.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(STYLE, asset)
    if not asset.is_file() or asset.read_bytes() != STYLE.read_bytes():
        raise RuntimeError("Home showcase CSS mismatch")
    version = hashlib.sha256(STYLE.read_bytes()).hexdigest()[:12]
    guide = f'{PREFIX}{ACADEMY_STYLE}'
    home_css = f'{PREFIX}assets/{STYLE.name}?v={version}'
    link = (
        f'<link rel="stylesheet" href="{guide}" data-ma-home-style="academy">'
        f'<link rel="stylesheet" href="{home_css}" data-ma-home-style="showcase">'
    )

    for locale, d in LOCALES.items():
        home = site / locale / "index.html"
        if not home.is_file():
            raise RuntimeError(f"Homepage missing: {home}")
        html = home.read_text(encoding="utf-8")
        cards = cards_from_academy(site, locale)
        if verify_only:
            if html.count(MARKER) != 1:
                raise RuntimeError(f"Home showcase marker missing or duplicated: {locale}")
            if html.count('data-ma-home-style="academy"') != 1:
                raise RuntimeError(f"Academy stylesheet missing or duplicated: {locale}")
            if html.count('data-ma-home-style="showcase"') != 1:
                raise RuntimeError(f"Home CSS missing or duplicated: {locale}")
            if home_css not in html:
                raise RuntimeError(f"Home CSS revision mismatch: {locale}")
            main = html.split(MARKER, 1)[1].split("</section>", 1)[0]
            if len(CARD.findall(main)) != 6:
                raise RuntimeError(f"Home card count mismatch: {locale}")
            if f'href="{PREFIX}{d["academy"]}/"' not in main:
                raise RuntimeError(f"Home Academy CTA missing: {locale}")
            for card in cards:
                href = COURSE_LINK.findall(card)[0]
                if html.count(f'href="{href}"') < 1:
                    raise RuntimeError(f"Missing homepage card: {href}")
            continue
        if MARKER in html or 'data-ma-home-style=' in html:
            raise RuntimeError(f"Home showcase already present: {locale}")
        where = home_hero_end(html)
        html = html[:where] + section(locale, cards) + html[where:]
        head = re.search(r"</head\s*>", html, flags=re.IGNORECASE)
        if not head:
            raise RuntimeError(f"Homepage head missing: {locale}")
        html = html[:head.start()] + link + html[head.start():]
        home.write_text(html, encoding="utf-8")
    print(f"MANZO AI home showcase: 6 genuine cards × 3 languages; verify={verify_only}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, required=True)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    publish(args.site, args.verify_only)
