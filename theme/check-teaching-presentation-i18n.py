#!/usr/bin/env python3
"""Parità delle 15 slide testuali accessibili IT/EN/ES per AI Teaching Lab.

Controllo dei sorgenti: non certifica la pubblicazione delle slide tradotte,
la localizzazione dei video originali, la qualità linguistica o WCAG.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "editorial/learning/ai-teaching-lab"
LOCALES = ("it", "en", "es")
FIELDS = ("title", "eyebrow", "lead", "takeaway")


def check() -> None:
    content = {}
    for locale in LOCALES:
        path = BASE / locale / "presentation.json"
        if not path.is_file():
            raise RuntimeError(f"Missing translated slide content {path}")
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("locale") != locale:
            raise RuntimeError(f"{locale}: wrong presentation language metadata")
        if data.get("version") != "1.0":
            raise RuntimeError(f"{locale}: unexpected slide schema version")
        if data.get("slides_count") != 15 or len(data.get("slides", [])) != 15:
            raise RuntimeError(f"{locale}: exactly 15 slides required")
        if not isinstance(data.get("duration_podcast_seconds"), (int, float)):
            raise RuntimeError(f"{locale}: original podcast duration must remain numeric")
        if not all(isinstance(data.get(k), str) and data[k].strip()
                   for k in ("course", "source", "editorial_policy")):
            raise RuntimeError(f"{locale}: missing essential presentation metadata")
        for i, slide in enumerate(data["slides"], 1):
            if not isinstance(slide, dict):
                raise RuntimeError(f"{locale}: slide {i} must be an object")
            for field in FIELDS:
                if not isinstance(slide.get(field), str) or len(slide[field].strip()) < 5:
                    raise RuntimeError(f"{locale}: missing {field} on slide {i}")
            points = slide.get("points")
            if not isinstance(points, list) or not points or not all(
                isinstance(p, str) and len(p.strip()) >= 8 for p in points
            ):
                raise RuntimeError(f"{locale}: incomplete points on slide {i}")
        content[locale] = data

    it = content["it"]
    for locale in ("en", "es"):
        translated = content[locale]
        if translated["duration_podcast_seconds"] != it["duration_podcast_seconds"]:
            raise RuntimeError(f"{locale}: original podcast timing must be preserved")
        for i, (base, other) in enumerate(zip(it["slides"], translated["slides"]), 1):
            if len(base["points"]) != len(other["points"]):
                raise RuntimeError(f"{locale}: slide {i} lost or added a teaching point")
            if all(base[field] == other[field] for field in FIELDS):
                raise RuntimeError(f"{locale}: slide {i} left entirely in Italian")
    print(
        "PASS AI Teaching Lab presentation IT/EN/ES: "
        "15 slides x 3 locales, equal point counts, localized metadata, "
        "podcast duration preserved; educational source parity only, "
        "native publication and complete UI translation NOT certified."
    )


if __name__ == "__main__":
    check()
