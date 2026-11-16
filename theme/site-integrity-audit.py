#!/usr/bin/env python3
"""MANZO AI static release integrity audit: routes, fragments, IDs and language.

Read-only; scans final generated HTML (never production database or external URLs).
No third-party Python dependencies. Intended to catch broken learning navigation
across home, Academy, courses, research and product demo.
"""
from __future__ import annotations

import argparse
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT_PREFIX="/manzo-ai/"

class Markup(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[]
        self.hrefs=[]
        self.language=None
        self.h1=0
    def handle_starttag(self,tag,attrs):
        data=dict(attrs)
        if tag=="html":self.language=data.get("lang")
        if tag=="h1":self.h1+=1
        if "id" in data:self.ids.append(data["id"])
        if tag=="a" and data.get("href") is not None:self.hrefs.append(data["href"])

def destination(root,page,href):
    parts=urlsplit(href)
    if parts.scheme or parts.netloc:return None
    if href.startswith("//"):return None
    if not parts.path:return (page,unquote(parts.fragment)) if parts.fragment else None
    if parts.path.startswith(ROOT_PREFIX):
        local=root/unquote(parts.path[len(ROOT_PREFIX):])
    elif parts.path.startswith("/"):
        # The shared github.io origin also hosts projects outside MANZO AI.
        return None
    else:
        local=page.parent/unquote(parts.path)
    if local.is_dir():local=local/"index.html"
    return (local,unquote(parts.fragment))

def audit(site:Path):
    site=site.resolve()
    pages=sorted(site.rglob("index.html"))
    if len(pages)<100:raise RuntimeError(f"Suspiciously incomplete site: {len(pages)} pages")
    parsed={}
    issues=[]
    for page in pages:
        markup=Markup()
        markup.feed(page.read_text(encoding="utf-8"))
        parsed[page]=markup
        label=str(page.relative_to(site))
        if not markup.language:issues.append(label+": html lang is missing")
        if markup.h1<1:issues.append(label+": no H1")
        duplicate=[name for name,count in Counter(markup.ids).items() if count>1]
        if duplicate:issues.append(label+": duplicate DOM IDs: "+", ".join(duplicate[:5]))
    checked=0;anchors=0
    supplemental={}
    for page,markup in parsed.items():
        for href in markup.hrefs:
            dest=destination(site,page,href)
            if dest is None:continue
            target,fragment=dest
            checked+=1
            label=str(page.relative_to(site))
            if not target.is_file():
                issues.append(label+" -> missing route: "+href)
                continue
            if fragment:
                anchors+=1
                if target not in parsed and target not in supplemental:
                    sub=Markup()
                    sub.feed(target.read_text(encoding="utf-8"))
                    supplemental[target]=sub
                matched=parsed.get(target) or supplemental.get(target)
                if fragment not in matched.ids:
                    issues.append(label+" -> missing fragment: "+href)
    if issues:
        for item in issues[:35]:print("ISSUE: "+item)
        raise RuntimeError(f"Integrity issues: {len(issues)}")
    print(f"PASS MANZO AI release integrity: {len(pages)} pages; "
          f"{checked} in-site links; {anchors} fragment targets; "
          "unique DOM IDs and language tags")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--site",type=Path,required=True)
    args=parser.parse_args()
    audit(args.site)
