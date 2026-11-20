#!/usr/bin/env python3
"""Place the same MANZO AI Academy card on IT/EN/ES Home.

The autonomy course follows Build Safely immediately; the geometry, cover,
two tags, body and CTA are identical to the existing reviewed card standard.
Runs AFTER build-safely and prompt-skill translated Home publishers.
"""
from __future__ import annotations
import argparse
from html import escape
from pathlib import Path
from govern_autonomy_i18n import BASE, ROUTES, UI
MARKER='data-ma-home-course="governare-autonomia"'
SAFETY='data-ma-home-course="build-safely"'
GRID='<div class="ma-course-grid ma-home-course-grid">'

def e(x):return escape(str(x),quote=True)

def card(lang):
    t=UI[lang]
    return f'''<article class="ma-course-card ps-home-course-card ga-home-course-card" {MARKER}
 data-ma-category="agent-governance" aria-labelledby="ga-home-title-{lang}">
 <div class="ma-course-art ps-home-art" aria-hidden="true">
 <span class="ps-home-art-label">AGENT / {lang.upper()}</span>
 <div class="ps-home-art-diagram"><span class="ps-home-art-p">A</span>
 <span class="ps-home-art-arrow">→</span><span class="ps-home-art-s">✓</span></div>
 <strong class="ps-home-art-brand">MANZO<span>AI</span></strong>
 </div>
 <div class="ma-course-info ps-home-info">
 <p class="ps-home-kind">{e(t["catalogStatus"])}</p>
 <h3 id="ga-home-title-{lang}">{e(t["catalogTitle"])}</h3>
 <p class="ps-home-desc">{e(t["homeDescription"])}</p>
 <div class="ps-home-tags"><span>{e(t["homeTags"][0])}</span><span>{e(t["homeTags"][1])}</span></div>
 <a href="{BASE}{ROUTES[lang]}/" class="ma-course-link ps-home-link">
 <span>{e(t["catalogOpen"])}</span><span class="ps-home-link-arrow" aria-hidden="true">↗</span></a>
 </div></article>'''

def run(site,verify_only=False):
    for lang in ("it","en","es"):
        home=site/lang/"index.html"
        target=site/ROUTES[lang]/"index.html"
        if not home.is_file() or not target.is_file():
            raise RuntimeError(lang+": cannot add card without a complete native-language course")
        html=home.read_text(encoding="utf-8")
        if verify_only:
            if html.count(MARKER)!=1 or html.count(SAFETY)!=1:
                raise RuntimeError(lang+": missing or duplicated sequential courses")
            if html.count('data-ma-course-card="1"')!=6:
                raise RuntimeError(lang+": legacy six-card geometry changed")
            if html.count('href="'+BASE+ROUTES[lang]+'/"')!=1:
                raise RuntimeError(lang+": autonomy card links to wrong language")
            if card(lang).count('ps-home-tags')!=1 or card(lang).count('ps-home-link-arrow')!=1:
                raise RuntimeError(lang+": non-uniform Academy card")
            if html.index(SAFETY)>html.index(MARKER):
                raise RuntimeError(lang+": autonomy must follow Build Safely")
            continue
        if MARKER in html:raise RuntimeError(lang+": course card already present")
        if html.count(GRID)!=1:raise RuntimeError(lang+": missing uniform Academy card grid")
        start=html.find(SAFETY,html.index(GRID))
        if start<0:raise RuntimeError(lang+": prerequisite safety card absent")
        end=html.find("</article>",start)
        if end<0:raise RuntimeError(lang+": prerequisite card invalid")
        pos=end+len("</article>")
        html=html[:pos]+"\n"+card(lang)+html[pos:]
        home.write_text(html,encoding="utf-8")
    if verify_only:
        print("Governing Autonomy Home: three translated and geometrically uniform cards follow Build Safely PASS")
    else:run(site,True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--site",required=True,type=Path)
    p.add_argument("--verify-only",action="store_true")
    args=p.parse_args();run(args.site,args.verify_only)
