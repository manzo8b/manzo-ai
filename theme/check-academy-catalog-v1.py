#!/usr/bin/env python3
"""Validate MANZO AI Academy v1 canonical inventory and optionally staged links.

Read-only. Never modifies public pages or student data.
Usage:
    python3 theme/check-academy-catalog-v1.py
    python3 theme/check-academy-catalog-v1.py --site _site
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parent.parent
CATALOG=ROOT/"academy/catalog-v1.json"
KINDS={"course","foundation_module"}
PRACTICES={"interactive","guided","separate_studio","assessment","static_activity","none","external_tool"}
LANGUAGES=("it","en","es")
STATUSES={"published","route_in_build_tests","not_verified","in_preparation"}
RELATIONS={"integrated","separate_internal_studios",
           "linked_in_lesson_target_to_confirm","no_dedicated_interactive_lab"}
EXPECTED={"course":9,"foundation_module":6}
EXPECTED_CATEGORY={"foundations":6,"prompt_build":2,"reliability":3,"governance":3,"teaching":1}

def validate(site:Path|None=None):
    data=json.loads(CATALOG.read_text(encoding="utf-8"))
    if data["schema_version"]!="1.0-draft":
        raise ValueError("Unexpected catalog schema version")
    items=data["items"]
    if len(items)!=15:
        raise ValueError("Expected 15 unique core units, not all resource links")
    ids=[i["id"] for i in items]
    if len(ids)!=len(set(ids)):
        raise ValueError("Duplicate canonical course/module id")
    kinds=Counter(i["kind"] for i in items)
    cats=Counter(i["category"] for i in items)
    if dict(kinds)!=EXPECTED:
        raise ValueError(f"Expected 9 courses + 6 foundation modules: {kinds}")
    if dict(cats)!=EXPECTED_CATEGORY:
        raise ValueError(f"Incorrect learning taxonomy: {cats}")
    all_routes={}
    for item in items:
        if item["kind"] not in KINDS:
            raise ValueError("Unexpected content type "+item["id"])
        if item["category"] not in data["categories"]:
            raise ValueError("Undefined category "+item["id"])
        if not item.get("title_it") or not item.get("source"):
            raise ValueError("Missing title/source "+item["id"])
        if not item.get("outcome_it") or not item.get("audience_it"):
            raise ValueError("Missing learner outcome or audience "+item["id"])
        if item.get("copy_status")!="editorial_proposal_pending_course_review":
            raise ValueError("Unreviewed outcome copy represented as approved "+item["id"])
        if item["title_it"].strip().endswith("."):
            raise ValueError("Heading ends in a full stop "+item["id"])
        if item["duration_minutes"] is not None or item["level"] is not None:
            raise ValueError("Invented unverified duration/level "+item["id"])
        if not set(item["practice"])<=PRACTICES:
            raise ValueError("Unknown practice type "+item["id"])
        if item["lab_relation"] not in RELATIONS:
            raise ValueError("Unknown lab relation "+item["id"])
        if set(item["route"])!=set(LANGUAGES) or set(item["language_status"])!=set(LANGUAGES):
            raise ValueError("Locale fields missing "+item["id"])
        for lang in LANGUAGES:
            route=item["route"][lang]
            status=item["language_status"][lang]
            if status not in STATUSES:
                raise ValueError("Unknown status "+item["id"]+"/"+lang)
            if route is None:
                if status not in {"not_verified","in_preparation"}:
                    raise ValueError("False published status "+item["id"]+"/"+lang)
                continue
            if not route.startswith(lang+"/") or route.startswith("/") or route.endswith("/"):
                raise ValueError("Unsafe or wrong-language route "+item["id"]+"/"+lang)
            if not all(part not in ("","..",".") for part in route.split("/")):
                raise ValueError("Malformed URL "+route)
            key=(lang,route)
            if key in all_routes:
                raise ValueError(f"Duplicate route {key}: {item['id']} and {all_routes[key]}")
            all_routes[key]=item["id"]
            if site:
                target=site/route/"index.html"
                if not target.is_file():
                    raise FileNotFoundError("Catalog linked page missing: "+str(target))
                content=target.read_text(encoding="utf-8")
                if '<main' not in content.lower() or '<h1' not in content.lower():
                    raise ValueError("Linked destination lacks main/h1: "+route)
                if f'lang="{lang}"' not in content and f"lang='{lang}'" not in content:
                    raise ValueError("Linked destination locale mismatch: "+route)

    lab=next(x for x in items if x["id"]=="ai-teaching-lab")
    if lab["route"]["en"] is not None or lab["route"]["es"] is not None:
        raise ValueError("Do not claim native AI Teaching Lab EN/ES before release")
    if lab["language_status"]["en"]!="in_preparation" or lab["language_status"]["es"]!="in_preparation":
        raise ValueError("AI Teaching Lab translation status is inaccurate")
    print("PASS Academy manifest: 9 courses, 6 foundation modules, 5 categories, "
          f"{len(all_routes)} declared locale routes, no duplicate IDs or invented metadata")
    if site:
        print("PASS Staged course/module URLs and page-level lang/main/h1 inspected")
    else:
        print("NOTE URLs are source-evidenced, but a staged site was not provided for a live-path check")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--site",type=Path)
    args=p.parse_args()
    validate(args.site)
