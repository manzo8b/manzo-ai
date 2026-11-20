#!/usr/bin/env python3
"""Sprint 0 release gate: honest homepage catalogue labels and translation provenance.

Read-only checks. This does not certify translation quality, WCAG, or the live
site: it compares the generated static bundle with the indexed editorial sources
and current-facing project status documentation.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "theme"))
from importlib.machinery import SourceFileLoader

i18n = SourceFileLoader(
    "academy_i18n_audit", str(ROOT / "theme/audit-academy-i18n.py")
).load_module()

LABELS = {
    "it": "Corsi e lezioni aperti",
    "en": "Open courses and lessons",
    "es": "Cursos y lecciones abiertos",
}
STALE_LABELS = (
    "6 risorse pubblicate",
    "6 published resources",
    "6 recursos publicados",
)


def audit(site: Path) -> None:
    for locale, label in LABELS.items():
        page = site / locale / "index.html"
        if not page.is_file():
            raise RuntimeError(f"Missing {locale.upper()} homepage: {page}")
        html = page.read_text(encoding="utf-8")
        marker = 'data-ma-home-showcase="v1"'
        if html.count(marker) != 1:
            raise RuntimeError(f"{locale}: Academy Home showcase marker not unique")
        # The same live DOM string must appear once in the showcase number/label.
        match = re.search(
            r'<span class="ma-home-showcase-number">([^<]+)</span>',
            html,
            re.I,
        )
        if not match or match.group(1) != label:
            raise RuntimeError(f"{locale}: static catalogue quantity is not honest/localized")
        for stale in STALE_LABELS:
            if stale in html:
                raise RuntimeError(f"{locale}: obsolete six-resource badge visible")
        # The initial six Academy cards were never re-authored. Additional
        # courses use a separate marker: these may be pedagogically distinct
        # from the six legacy lessons, which is why we never invent a count.
        curated = len(re.findall(r'data-ma-course-card="1"', html))
        expanded = len(re.findall(r'data-ma-home-course=', html))
        if curated != 6 or expanded < 7:
            raise RuntimeError(
                f"{locale}: home inventory unexpectedly changed "
                f"(curated={curated}, extended={expanded})"
            )
    courses = i18n.evaluate()
    complete = sum(c["source_complete"] for c in courses.values())
    total = len(courses)
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    policy = (ROOT / "theme/ACADEMY_I18N_STANDARD.md").read_text(encoding="utf-8")
    if f"**{complete} percorsi su {total}**" not in readme:
        raise RuntimeError(
            f"README Academy source state differs from current audit ({complete}/{total})"
        )
    if f"**Copertura fonti editoriali Academy aggiornata: {complete}/{total} corsi**" not in policy:
        raise RuntimeError(
            f"Editorial language policy is stale (actual {complete}/{total})"
        )
    teaching = courses["ai-teaching-lab"]
    if teaching["source_complete"] is False:
        # This is an acknowledged work item, not a reason to remove or reroute
        # the existing full Italian course.
        for locale in ("en", "es"):
            missing = teaching["languages"][locale]["missing"]
            if not missing:
                raise RuntimeError(f"{locale}: Teaching Lab incomplete without a listed gap")
        if "AI Teaching Lab" not in readme or "incompleto" not in readme:
            raise RuntimeError("README does not disclose incomplete Teaching Lab translation")
        print(
            "SPRINT0 PARTIAL: AI Teaching Lab EN/ES translations not yet complete; "
            "native English/Spanish course must not be advertised as finished"
        )
    print(
        f"PASS Sprint 0 Home and status consistency: "
        f"IT/EN/ES truthful Academy labels, 6 curated + 7 extended cards per locale; "
        f"editorial parity {complete}/{total}, documentation consistent. "
        "Full site translation and human review NOT certified."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True, type=Path)
    opts = parser.parse_args()
    audit(opts.site)
