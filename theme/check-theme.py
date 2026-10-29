#!/usr/bin/env python3
"""Check that MANZO AI's CSS-only educational refresh changes no v0.7 content."""
import argparse
from pathlib import Path
import re
import zipfile

p = argparse.ArgumentParser()
p.add_argument("--site", required=True, type=Path)
p.add_argument("--archive", required=True, type=Path)
p.add_argument("--theme", required=True, type=Path)
args = p.parse_args()

theme = args.theme.read_bytes()
with zipfile.ZipFile(args.archive) as archive:
    originals = archive.namelist()
    assert "style.css" in originals, "Missing original stylesheet"
    original_style = archive.read("style.css")
    deployed_style = (args.site / "style.css").read_bytes()
    assert deployed_style == original_style + b"\n" + theme, "Style overlay mismatch"
    # Preserve byte-for-byte ALL other original resources: HTML, JS, PDFs and slides.
    for name in originals:
        if name.endswith("/") or name == "style.css":
            continue
        assert (args.site / name).read_bytes() == archive.read(name), f"Unexpected content change: {name}"
    total_html = sum(name.endswith("index.html") for name in originals)
    assert total_html == 82, f"Unexpected site inventory: {total_html}"
    for locale in ("it", "es", "en"):
        assert (args.site / locale / "index.html").is_file(), locale

for page in args.site.rglob("index.html"):
    content = page.read_text(encoding="utf-8")
    assert 'href="/manzo-ai/style.css"' in content, f"Stylesheet missing: {page}"

css = theme.decode("utf-8")
assert len(css) > 5000
assert css.count("{") == css.count("}"), "Unbalanced CSS block count"
for required in (".rail", ".nav-link[aria-current=page]", ".home-hero",
                 ".grid-3>.feature", ".challenge-card", ".cross-scroll",
                 ".dilemma-option", ".technical-article", "@media print",
                 "prefers-reduced-motion", ":focus-visible"):
    assert required in css, f"Missing design target: {required}"

# WCAG AA contrast for dark palette on the white cards and ivory canvas.
def luminance(value):
    v = [int(value[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    v = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in v]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]

def ratio(a, b):
    x, y = luminance(a), luminance(b)
    return (max(x, y) + .05) / (min(x, y) + .05)

for swatch in ("#0C615D", "#244F9B", "#B13F28", "#67439A", "#7B4B10"):
    for surface in ("#FFFFFF", "#FCFBF8"):
        assert ratio(swatch, surface) >= 4.5, f"Insufficient contrast: {swatch} on {surface}"

print("MANZO AI v0.7.1: 82 pages; original HTML, JS and downloads untouched; CSS overlay and contrast verified.")
