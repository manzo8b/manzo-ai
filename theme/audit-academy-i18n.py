#!/usr/bin/env python3
"""Evidence-based editorial translation coverage inventory for MANZO AI.

Do not count a language as translated because a home page, card or heading is
localised. Inspect each course's editorial source and interactive components.
A source audit is not a human editorial-review certification.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from datetime import date

ROOT=Path(__file__).resolve().parent.parent
ED=ROOT/"editorial/learning"
LOCALES=("it","en","es")
CATALOGUE={
 "hallucinations":{
   "display":"AI Hallucinations",
   "files":{"it":["hallucinations/it.json","hallucinations/coding-it.json"],
            "en":["hallucinations/en.json","hallucinations/coding-en.json"],
            "es":["hallucinations/es.json","hallucinations/coding-es.json"]},
   "minimum_bytes":11000,
 },
 "ai-teaching-lab":{
   "display":"AI Teaching Lab",
   "files":{locale:[
       f"ai-teaching-lab/{locale}/course.json",
       f"ai-teaching-lab/{locale}/narrative.json",
       f"ai-teaching-lab/{locale}/glossary.json",
       f"ai-teaching-lab/{locale}/assessment-bank.json",
       f"ai-teaching-lab/{locale}/scenarios.json",
       f"ai-teaching-lab/{locale}/presentation.json",
       *[f"ai-teaching-lab/{locale}/module-{i:02}.md" for i in range(1,6)],
   ] for locale in LOCALES},
   "minimum_bytes":1500,
 },
 "prompt-vs-skill":{
   "display":"Prompt vs Skill",
   "files":{"it":["prompt-vs-skill/letture.md"],
            "en":["prompt-vs-skill/en.md"],
            "es":["prompt-vs-skill/es.md"]},
   "minimum_bytes":17000,
 },
 "mental-models-reliability":{
   "display":"Mental Models and AI Reliability",
   "files":{"it":["mental-models-reliability/letture.md"],
            "en":["mental-models-reliability/en.md"],
            "es":["mental-models-reliability/es.md"]},
   "minimum_bytes":16000,
 },
 "centroni-city":{
   "display":"AI Product Builder — Centroni City",
   "files":{"it":["centroni-city-builder/letture.md"],
            "en":["centroni-city-builder/en.md"],
            "es":["centroni-city-builder/es.md"]},
   "minimum_bytes":16000,
 },
 "build-safely":{
   "display":"Build Safely — Shadow AI and Human Oversight",
   "files":{locale:[f"build-safely/{locale}.md"] for locale in LOCALES},
   "minimum_bytes":18000,
 },
 "governing-autonomy":{
   "display":"Governing Autonomy — AI Agents and Human Oversight",
   "files":{locale:[f"governare-autonomia/{locale}.md"] for locale in LOCALES},
   "minimum_bytes":19000,
 },
 "dynamic-compliance":{
   "display":"Dynamic Compliance and Continuous Governance",
   "files":{locale:[f"compliance-dinamica-governance-continua/{locale}.md"] for locale in LOCALES},
   "minimum_bytes":29000,
 },
 "augmented-intelligence":{
   "display":"Augmented, Not Replaced — AI Literacy and Critical Thinking",
   "files":{locale:[f"intelligenza-aumentata-non-sostituita/{locale}.md"] for locale in LOCALES},
   "minimum_bytes":29000,
 },
}
INTERACTIONS={
 "hallucinations":{loc:[f"hallucinations/{loc}.json",f"hallucinations/coding-{loc}.json"] for loc in LOCALES},
 "build-safely":{loc:["build-safely/"+loc+".md"] for loc in LOCALES},
}
def evaluate():
    result={}
    for key,data in CATALOGUE.items():
        statuses={}
        for locale in LOCALES:
            paths=data["files"][locale]
            missing=[];too_short=[]
            for relative in paths:
                source=ED/relative
                if not source.is_file():missing.append(relative)
                elif source.stat().st_size < data["minimum_bytes"] and source.suffix==".md":
                    too_short.append(relative)
            if missing or too_short:
                statuses[locale]={"source_present":False,"missing":missing,"too_short":too_short,
                    "interpretation":"Missing full source material; do not claim this course is translated."}
            else:
                statuses[locale]={"source_present":True,"missing":[],"too_short":[],
                    "interpretation":"Source exists; requires page and human quality review."}
        result[key]={"title":data["display"],"languages":statuses,
                     "source_complete":all(statuses[loc]["source_present"] for loc in LOCALES)}
    return result
def run(output:Path|None,fail_on_missing:bool):
    courses=evaluate()
    complete=sum(item["source_complete"] for item in courses.values())
    total=len(courses)
    summary={"audit_date":"2026-11-20","policy":"theme/ACADEMY_I18N_STANDARD.md",
             "source_complete_courses":complete,"total_indexed_courses":total,
             "full_site_certified":False,
             "note":"This covers indexed Academy source sets only; a sitewide content-language and QA audit is still required.",
             "courses":courses}
    for key,data in courses.items():
        langs=", ".join(f"{loc.upper()}={'source' if data['languages'][loc]['source_present'] else 'MISSING'}" for loc in LOCALES)
        print(f"[{'SOURCES COMPLETE' if data['source_complete'] else 'NEEDS TRANSLATION'}] {key}: {langs}")
    print(f"Academy editorial source parity: {complete}/{total} indexed courses. Full MANZO AI coverage NOT certified.")
    if output:
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if fail_on_missing and complete<total:raise SystemExit(1)
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    parser.add_argument("--fail-on-missing",action="store_true")
    args=parser.parse_args()
    run(args.output,args.fail_on_missing)
