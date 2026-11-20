#!/usr/bin/env python3
"""MANZO AI · read-only pedagogical contract for the first two Academy pathways.

Checks SOURCE evidence for objectives, six ordered units, practical cases,
answer keys, explanations and source references in IT/EN/ES.
Optionally checks the published course guides and Academy entry points.
This is structural QA, not an automatic judgment of instructional quality.
No pages, quiz answers, grades or teaching materials are modified.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "editorial/learning/hallucinations"
LABELS = ROOT / "product/learning-experience/labels.json"
CORE_MAP = ROOT / "product/learning-experience/core-unit-evidence.json"
CODING_MAP = ROOT / "product/learning-experience/coding-unit-evidence.json"
PATHS = {
    "it": ("it/academy", "it/impara/allucinazioni-ai-verificabilita",
           "it/impara/allucinazioni-ai-verificabilita/coding"),
    "en": ("en/academy", "en/learn/ai-hallucinations-verification",
           "en/learn/ai-hallucinations-verification/coding"),
    "es": ("es/academia", "es/aprende/alucinaciones-ia-verificacion",
           "es/aprende/alucinaciones-ia-verificacion/coding"),
}


def ensure(value: bool, description: str) -> None:
    if not value:
        raise RuntimeError("Pedagogy gate: " + description)


def words(value: object, description: str) -> None:
    ensure(isinstance(value, str) and len(value.strip()) >= 8, description)


def check_core(data: dict, locale: str) -> None:
    modules = data.get("modules", [])
    ensure(len(modules) == 6, f"{locale} core: six learning units")
    titles = []
    for index, module in enumerate(modules, 1):
        title = module.get("title")
        words(title, f"{locale} core unit {index}: missing title")
        titles.append(title)
        ensure(isinstance(module.get("p"), list) and len(module["p"]) >= 2 and
               all(isinstance(p, str) and p.strip() for p in module["p"]),
               f"{locale} core unit {index}: missing explanatory reading")
        words(module.get("evidence"), f"{locale} core unit {index}: missing evidence note")
        ensure(bool(module.get("sources")), f"{locale} core unit {index}: missing source citations")
    ensure(len(set(titles)) == 6, f"{locale} core: duplicate unit title")
    cases = data.get("cases", [])
    ensure(len(cases) == 10, f"{locale} core: 10 practice cases required")
    for index, case in enumerate(cases, 1):
        ensure(isinstance(case, list) and len(case) == 5 and
               all(isinstance(part, str) and part.strip() for part in case),
               f"{locale} core case {index}: requires task and suggested resolution")
    quiz = data.get("quiz", [])
    ensure(len(quiz) == 10, f"{locale} core: 10 quiz items required")
    for index, item in enumerate(quiz, 1):
        ensure(isinstance(item, list) and len(item) == 4,
               f"{locale} core quiz {index}: malformed question")
        question, choices, correct, feedback = item
        words(question, f"{locale} core quiz {index}: missing question")
        ensure(isinstance(choices, list) and len(choices) >= 2 and
               all(isinstance(x, str) and x.strip() for x in choices),
               f"{locale} core quiz {index}: missing alternatives")
        ensure(isinstance(correct, list) and bool(correct) and
               all(isinstance(x, int) and 0 <= x < len(choices) for x in correct),
               f"{locale} core quiz {index}: invalid answer key")
        words(feedback, f"{locale} core quiz {index}: missing explanatory feedback")


def check_coding(data: dict, locale: str) -> None:
    chapters = data.get("chapters", [])
    ensure(len(chapters) == 6, f"{locale} coding: six ordered chapters")
    ids = []
    for index, chapter in enumerate(chapters, 1):
        words(chapter.get("title"), f"{locale} coding chapter {index}: missing title")
        ids.append(chapter.get("id"))
        ensure(isinstance(chapter.get("paragraphs"), list) and
               len(chapter["paragraphs"]) >= 1 and
               all(isinstance(p, str) and p.strip() for p in chapter["paragraphs"]),
               f"{locale} coding chapter {index}: missing reading")
        ensure(bool(chapter.get("refs")), f"{locale} coding chapter {index}: missing references")
    ensure(len(set(ids)) == 6, f"{locale} coding: duplicate chapter IDs")
    cases = data.get("cases", [])
    ensure(len(cases) == 4, f"{locale} coding: four real practice scenarios")
    for index, case in enumerate(cases, 1):
        ensure(isinstance(case, dict), f"{locale} coding case {index}: malformed")
        for key in ("sector", "title", "scenario", "task", "solution"):
            words(case.get(key), f"{locale} coding case {index}: missing {key}")
    quiz = data.get("quiz", [])
    ensure(len(quiz) == 4, f"{locale} coding: four questions")
    for index, item in enumerate(quiz, 1):
        ensure(isinstance(item, dict), f"{locale} coding quiz {index}: malformed")
        words(item.get("question"), f"{locale} coding quiz {index}: missing question")
        choices = item.get("options")
        ensure(isinstance(choices, list) and len(choices) >= 2 and
               all(isinstance(x, str) and x.strip() for x in choices),
               f"{locale} coding quiz {index}: missing alternatives")
        key = item.get("answer")
        ensure(isinstance(key, int) and 0 <= key < len(choices),
               f"{locale} coding quiz {index}: invalid answer key")
        words(item.get("why"), f"{locale} coding quiz {index}: missing explanation")


def validate(site: Path | None = None) -> None:
    labels = json.loads(LABELS.read_text(encoding="utf-8"))
    maps = json.loads(CORE_MAP.read_text(encoding="utf-8"))
    coding_maps = json.loads(CODING_MAP.read_text(encoding="utf-8"))
    ensure(set(maps) == set(PATHS) and set(coding_maps) == set(PATHS),
           "Competency maps require IT/EN/ES")
    expected_links = None
    expected_coding_links = None
    ensure(set(labels) == set(PATHS), "Academy requires all 3 languages")
    catalog_ids = None
    for loc, paths in PATHS.items():
        d = labels[loc]
        for name in ("coreOutcomes", "codingOutcomes"):
            outcomes = d.get(name, [])
            ensure(len(outcomes) == 3 and all(isinstance(x, str) and
                   len(x.strip()) >= 12 for x in outcomes),
                   f"{loc}: three explicit {name} outcomes")
        catalog = d["hub"].get("catalog", [])
        ensure(len(catalog) == 6, f"{loc}: six distinct Academy entries")
        ids = [item.get("id") for item in catalog]
        ensure(len(set(ids)) == 6, f"{loc}: duplicate Academy entries")
        if catalog_ids is None:
            catalog_ids = ids
        else:
            ensure(ids == catalog_ids, f"{loc}: course taxonomy differs across languages")
        ensure(all(item.get("route", "").startswith(loc + "/") for item in catalog),
               f"{loc}: Academy card links cross language boundaries")
        ensure(isinstance(d["hub"].get("orientationLabel"), str) and
               bool(d["hub"]["orientationLabel"].strip()),
               f"{loc}: missing positioning label")
        ensure(all(isinstance(item.get("pathHint"), str) and
                   len(item["pathHint"].strip()) >= 12 and
                   not item["pathHint"].strip().endswith(".") for item in catalog),
               f"{loc}: missing or period-terminated learning sequence hints")

        core = json.loads((CONTENT / f"{loc}.json").read_text(encoding="utf-8"))
        coding = json.loads((CONTENT / f"coding-{loc}.json").read_text(encoding="utf-8"))
        check_core(core, loc)
        check_coding(coding, loc)
        mapping = maps[loc]
        units = mapping.get("units", [])
        ensure(len(units) == len(core["modules"]) == 6,
               f"{loc}: one observable competency per core unit")
        for key in ("expand", "ability", "case", "quiz", "openCases", "openQuiz", "note"):
            ensure(isinstance(mapping.get(key), str) and bool(mapping[key].strip()),
                   f"{loc}: missing learner-facing evidence label {key}")
        links = []
        for i, entry in enumerate(units, 1):
            words(entry.get("outcome"), f"{loc}: unit {i} missing observable skill")
            ensure(not entry["outcome"].strip().endswith("."),
                   f"{loc}: unit {i} contains a terminal title period")
            case, quiz = entry.get("case"), entry.get("quiz")
            ensure(type(case) is int and 1 <= case <= len(core["cases"]) and
                   type(quiz) is int and 1 <= quiz <= len(core["quiz"]),
                   f"{loc}: unit {i} references a nonexistent case or question")
            links.append((case, quiz))
        if expected_links is None:
            expected_links = links
        else:
            ensure(links == expected_links,
                   f"{loc}: evidence numbering must be identical across languages")
        coding_mapping = coding_maps[loc]
        coding_units = coding_mapping.get("units", [])
        ensure(len(coding_units) == len(coding["chapters"]) == 6,
               f"{loc}: one observable skill per Engineering Assurance chapter")
        for key in ("expand", "ability", "case", "quiz", "openCases", "openQuiz", "note"):
            ensure(isinstance(coding_mapping.get(key), str) and
                   bool(coding_mapping[key].strip()),
                   f"{loc}: missing coding learner-facing label {key}")
        coding_links = []
        for index, entry in enumerate(coding_units, 1):
            words(entry.get("outcome"),
                  f"{loc}: coding chapter {index} missing observable skill")
            ensure(not entry["outcome"].strip().endswith("."),
                   f"{loc}: coding chapter {index} has terminal heading period")
            case, question = entry.get("case"), entry.get("quiz")
            ensure(type(case) is int and 1 <= case <= len(coding["cases"]) and
                   type(question) is int and 1 <= question <= len(coding["quiz"]),
                   f"{loc}: coding chapter {index} links to nonexistent evidence")
            coding_links.append((case, question))
        ensure(isinstance(coding_units[5].get("limitation"), str) and
               bool(coding_units[5]["limitation"].strip()),
               f"{loc}: business-value outcome must disclose evidence limitation")
        if expected_coding_links is None:
            expected_coding_links = coding_links
        else:
            ensure(coding_links == expected_coding_links,
                   f"{loc}: coding evidence numbering differs across languages")
        if site is None:
            continue
        academy, core_route, coding_route = paths
        academy_page = site / academy / "index.html"
        ensure(academy_page.is_file(), f"{loc}: Academy page absent")
        academy_html = academy_page.read_text(encoding="utf-8")
        ensure('data-ma-pathways="v1"' in academy_html and
               'data-ma-journeys="v1"' in academy_html,
               f"{loc}: course catalog or guided journeys absent")
        for name, route in (("core", core_route), ("coding", coding_route)):
            page = site / route / "index.html"
            ensure(page.is_file(), f"{loc}: {name} page absent")
            html = page.read_text(encoding="utf-8")
            if name == "core":
                ensure(html.count('data-ma-core-evidence=') == 6,
                       f"{loc}: rendered core unit map missing")
                for index, item in enumerate(units, 1):
                    ensure(f'data-ma-core-evidence="{index}"' in html and
                           f'data-ma-core-case="{item["case"]}"' in html and
                           f'data-ma-core-quiz="{item["quiz"]}"' in html,
                           f"{loc}: rendered mapping for unit {index} inconsistent")
            else:
                ensure(html.count('data-ma-coding-evidence=') == 6,
                       f"{loc}: six Engineering Assurance competency panels missing")
                for index, entry in enumerate(coding_units, 1):
                    ensure(f'data-ma-coding-evidence="{index}"' in html and
                           f'data-ma-coding-case="{entry["case"]}"' in html and
                           f'data-ma-coding-quiz="{entry["quiz"]}"' in html,
                           f"{loc}: coding evidence mapping for chapter {index} inconsistent")
                ensure('data-ma-core-evidence=' not in html,
                       f"{loc}: core evidence leaked into specialist coding course")
                ensure(coding_units[5]["limitation"] in html,
                       f"{loc}: evidence limitation not disclosed to learners")
            ensure(html.count('data-ma-learning-guide="v1"') == 1,
                   f"{loc}: {name} learning guide missing/duplicated")
            ensure(len(re.findall(r'data-ma-unit="[1-6]"', html)) == 6,
                   f"{loc}: {name} learning sequence not fully rendered")
            for anchor in (("hx-lab", "hx-quiz", "hx-crossword") if name == "core"
                           else ("hc-lab", "hc-quiz", "hc-gate")):
                ensure(f'id="{anchor}"' in html,
                       f"{loc}: {name} missing practical/assessment anchor {anchor}")

    print("PASS Academy pedagogical contract: 2 verified pathways × 3 locales, "
          "36 sourced units, 42 practice cases, 42 explained quiz items, "
          "explicit outcomes, 12 observable skills per locale, real-case/quiz evidence, consistent course taxonomy"
          + (", rendered guides and activities" if site else " (source only)"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path)
    validate(parser.parse_args().site)
