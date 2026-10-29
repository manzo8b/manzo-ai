#!/usr/bin/env python3
"""Add one consistent MANZO AI identity signature to static HTML after archive extraction.
No server calls or client-side scripts are added; preserves the release archive unchanged."""
from __future__ import annotations
import argparse
from pathlib import Path
import re

URL = "https://manzo8b.github.io/manzo-ai/"
SIGNATURES = {
    "it": "Un progetto dell'ecosistema MANZO AI",
    "es": "Un proyecto del ecosistema MANZO AI",
    "en": "A project of the MANZO AI ecosystem",
}

CONTACT_LABELS = {
    "it": "Contatti e servizi",
    "es": "Contacto y servicios",
    "en": "Contact and services",
}
CONTACT_EMAIL = "marcelo2020.it@gmail.com"

def add_contact_header(html: str, language: str) -> str:
    if 'data-manzo-contact="1"' in html:
        raise ValueError("Duplicate MANZO AI contact header")
    label = CONTACT_LABELS.get(language, CONTACT_LABELS["it"])
    contact = (
        '<div class="manzo-contact-header" data-manzo-contact="1">'
        '<a href="mailto:' + CONTACT_EMAIL + '" aria-label="' + label + ': ' + CONTACT_EMAIL + '">'
        '<span>' + label + '</span><strong>' + CONTACT_EMAIL + '</strong></a></div>'
    )
    body = re.search(r"<body\b[^>]*>", html, re.I)
    if not body:
        raise ValueError("No HTML body for contact")
    return html[:body.end()] + contact + html[body.end():]

def insert_signature(html: str, language: str) -> str:
    if 'data-manzo-signature="1"' in html:
        raise ValueError("Duplicate MANZO AI signature")
    text = SIGNATURES.get(language, SIGNATURES["it"])
    element = (
        '<div class="manzo-identity-signature" data-manzo-signature="1">'
        '<a href="' + URL + '" target="_blank" rel="noopener noreferrer">'
        '<img src="/manzo-ai/assets/manzo-mark.svg" alt="" aria-hidden="true" width="34" height="33" loading="lazy">'
        '<span>' + text + '</span></a></div>'
    )
    match = re.search(r"</footer\s*>", html, re.I)
    if match:
        return html[:match.start()] + element + html[match.start():]
    match = re.search(r"</body\s*>", html, re.I)
    if not match:
        raise ValueError("No body close tag")
    return html[:match.start()] + '<footer class="manzo-identity-tail">' + element + '</footer>' + html[match.start():]

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, required=True)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    site = args.site
    css = site / "style.css"
    emblem = site / "assets/manzo-mark.svg"
    if not css.is_file() or not emblem.is_file():
        raise SystemExit("Missing shared stylesheet or original MANZO emblem")
    files = sorted(site.rglob("index.html"))
    if len(files) < 82:
        raise SystemExit("Unexpectedly small static site")
    for page in files:
        content = page.read_text(encoding="utf-8")
        lang = next((segment for segment in page.relative_to(site).parts if segment in SIGNATURES), "it")
        if args.verify_only:
            if content.count('data-manzo-signature="1"') != 1:
                raise SystemExit("Branding missing or duplicated: " + str(page))
            if "manzo-mark.svg" not in content:
                raise SystemExit("Branding image missing: " + str(page))
            if content.count('data-manzo-contact="1"') != 1 or "mailto:" + CONTACT_EMAIL not in content:
                raise SystemExit("Contact missing or duplicated: " + str(page))
        else:
            if not re.search(r"<body(?:\s|>)", content, re.I):
                raise SystemExit("Page has no body element: " + str(page))
            updated = add_contact_header(insert_signature(content, lang), lang)
            page.write_text(updated, encoding="utf-8")
    print(f"MANZO AI footer branding: {len(files)} static pages {'verified' if args.verify_only else 'updated'}")

if __name__ == "__main__":
    main()
