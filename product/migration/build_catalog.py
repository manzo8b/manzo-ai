#!/usr/bin/env python3
"""Read-only MANZO AI public educational catalog generator.

Source of truth: reviewed editorial JSON files in Git.
Output: non-sensitive catalog METADATA ONLY, not question banks or B2B users.
No network, DB connections, Supabase credentials or publishing side effects.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[2]
LOCALES = ("it", "en", "es")
SOURCES = {
    "ai-hallucinations": {
        "group": "core",
        "route": {
            "it": "it/impara/allucinazioni-ai-verificabilita/",
            "en": "en/learn/ai-hallucinations-verification/",
            "es": "es/aprende/alucinaciones-ia-verificacion/",
        },
        "file": "editorial/learning/hallucinations/{locale}.json",
        "units": 6,
        "quiz_items": 10,
        "cases": 10,
    },
    "engineering-assurance": {
        "group": "coding",
        "route": {
            "it": "it/impara/allucinazioni-ai-verificabilita/coding/",
            "en": "en/learn/ai-hallucinations-verification/coding/",
            "es": "es/aprende/alucinaciones-ia-verificacion/coding/",
        },
        "file": "editorial/learning/hallucinations/coding-{locale}.json",
        "units": 6,
        "quiz_items": 4,
        "cases": 4,
    },
}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def nonblank(value: object, where: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{where} must be nonblank text")
    return value.strip()


def read_json(root: Path, relative: str) -> tuple[dict, str]:
    file = root / relative
    require(file.is_file(), f"missing editorial source {relative}")
    raw = file.read_bytes()
    try:
        value = json.loads(raw)
    except (ValueError, UnicodeDecodeError) as error:
        raise ValueError(f"invalid JSON source {relative}") from error
    require(isinstance(value, dict), f"{relative}: JSON root must be an object")
    return value, hashlib.sha256(raw).hexdigest()


def audit_core(data: dict, where: str) -> tuple[list[dict], str]:
    require(isinstance(data.get("head"), dict), f"{where}: no head")
    title = " ".join((
        nonblank(data["head"].get("title1"), f"{where}.head.title1"),
        nonblank(data["head"].get("title2"), f"{where}.head.title2"),
    ))
    modules = data.get("modules")
    require(isinstance(modules, list) and len(modules) == 6, f"{where}: expected six modules")
    items = []
    for position, module in enumerate(modules, 1):
        require(isinstance(module, dict), f"{where}: invalid module")
        items.append({
            "key": f"core-{position:02d}",
            "position": position,
            "title": nonblank(module.get("title"), f"{where}.modules[{position}].title"),
            "duration": nonblank(module.get("duration"), f"{where}.modules[{position}].duration"),
        })
    quiz = data.get("quiz")
    require(isinstance(quiz, list) and len(quiz) == 10, f"{where}: expected ten self-assessment items")
    for idx, item in enumerate(quiz, 1):
        require(isinstance(item, list) and len(item) == 4, f"{where}.quiz[{idx}]: expected 4-part item")
        require(isinstance(item[1], list) and len(item[1]) >= 2, f"{where}.quiz[{idx}]: invalid choices")
        answers = item[2]
        require(isinstance(answers, list) and len(answers) > 0, f"{where}.quiz[{idx}]: no answer marker")
        require(all(type(x) is int and 0 <= x < len(item[1]) for x in answers), f"{where}.quiz[{idx}]: invalid answer markers")
        require(len(answers) == len(set(answers)), f"{where}.quiz[{idx}]: duplicate answer markers")
    require(isinstance(data.get("cases"), list) and len(data["cases"]) == 10, f"{where}: expected ten cases")
    return items, title


def audit_coding(data: dict, locale: str, where: str) -> tuple[list[dict], str]:
    require(data.get("locale") == locale, f"{where}: mismatched language")
    title = nonblank(data.get("title"), f"{where}.title")
    chapters = data.get("chapters")
    require(isinstance(chapters, list) and len(chapters) == 6, f"{where}: expected six chapters")
    items = []
    for position, chapter in enumerate(chapters, 1):
        require(isinstance(chapter, dict) and chapter.get("id") == f"{position:02d}", f"{where}: chapter order mismatch")
        items.append({
            "key": f"coding-{position:02d}",
            "position": position,
            "title": nonblank(chapter.get("title"), f"{where}.chapters[{position}].title"),
            "duration": None,
        })
    quiz = data.get("quiz")
    require(isinstance(quiz, list) and len(quiz) == 4, f"{where}: expected four self-assessment items")
    for idx, item in enumerate(quiz, 1):
        require(isinstance(item, dict) and isinstance(item.get("options"), list), f"{where}.quiz[{idx}]: invalid item")
        require(len(item["options"]) == 4, f"{where}.quiz[{idx}]: expected four choices")
        answer = item.get("answer")
        require(str(answer) in ("0", "1", "2", "3") and type(answer) is not bool, f"{where}.quiz[{idx}]: invalid answer marker")
    require(isinstance(data.get("cases"), list) and len(data["cases"]) == 4, f"{where}: expected four coding cases")
    return items, title


def build_catalog(root: Path = REPO) -> dict:
    courses = []
    variants = []
    for course_key, spec in SOURCES.items():
        courses.append({
            "key": course_key,
            "mode": "public_learning",
            "owner_tenant_id": None,
            "b2b_enrollment_enabled": False,
            "b2b_grading_enabled": False,
            "canonical_locale": "it",
        })
        for locale in LOCALES:
            relative = spec["file"].format(locale=locale)
            data, checksum = read_json(root, relative)
            units, title = (audit_core(data, relative) if spec["group"] == "core"
                            else audit_coding(data, locale, relative))
            require(len(units) == spec["units"], f"{relative}: invalid unit count")
            route = spec["route"][locale]
            require(route.startswith(locale + "/") and route.endswith("/"), f"{relative}: invalid route")
            variants.append({
                "key": f"{course_key}:{locale}",
                "course_key": course_key,
                "locale": locale,
                "title": title,
                "route": "/manzo-ai/" + route,
                "source_path": relative,
                "source_sha256": checksum,
                "editorial_status": "published_static",
                "units": units,
                "unit_count": len(units),
                "public_self_assessment_count": len(data["quiz"]),
                "public_case_count": len(data["cases"]),
                "private_assessment_ready": False,
                "source_contains_public_answers": True,
            })
    require(len({v["key"] for v in variants}) == len(variants), "duplicate variant key")
    require(len({v["route"] for v in variants}) == len(variants), "duplicate public route")
    return {
        "schema_version": "1.0",
        "scope": "editorial_public_metadata_only",
        "source_of_truth": "manzo8b/manzo-ai:editorial/",
        "database_target": "not_imported_pending_tenant_and_public_catalog_design",
        "content_policy": {
            "quiz_answers_exported": False,
            "user_data_exported": False,
            "progress_exported": False,
            "course_access_claimed": False,
            "score_or_certification_claimed": False,
        },
        "summary": {
            "courses": len(courses),
            "localized_variants": len(variants),
            "languages": list(LOCALES),
            "localized_units": sum(len(v["units"]) for v in variants),
            "localized_public_self_assessment_items": sum(v["public_self_assessment_count"] for v in variants),
            "localized_cases": sum(v["public_case_count"] for v in variants),
        },
        "courses": courses,
        "variants": variants,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    source_dir = (args.root / "editorial").resolve()
    require(not output.is_relative_to(source_dir), "output may not overwrite editorial source")
    require("_site" not in output.parts, "do not publish internal migration metadata as a website page")
    catalog = build_catalog(args.root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(catalog["summary"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
