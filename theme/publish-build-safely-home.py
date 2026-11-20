#!/usr/bin/env python3
"""Present Build Safely as a single, uniform Academy course card on IT EN ES Home.

Runs only AFTER legacy Academy Home generation. It uses the exact shared
.ma-course-card/.ps-home-course-card structure, cover height, two tags
and horizontal CTA. No fake translations or links to Italian fallbacks.
"""
from __future__ import annotations
import argparse
import hashlib
from html import escape
from pathlib import Path
import re
import shutil
from build_safely_i18n import I18N,ROUTES,BASE
ROOT=Path(__file__).resolve().parent
CSS=ROOT/"prompt-skill-home-card.css"
MARKER='data-ma-home-course="build-safely"'
GRID='<div class="ma-course-grid ma-home-course-grid">'
ORIGINAL=re.compile(r'<article\b(?=[^>]*\bdata-ma-course-card=["\']1["\'])[^>]*>.*?</article\s*>',re.I|re.S)

def e(x):return escape(str(x),quote=True)

def card(locale):
    t=I18N[locale]
    return f'''<article class="ma-course-card ps-home-course-card safe-home-course-card" {MARKER} data-ma-category="safety" aria-labelledby="safe-home-title-{locale}">
  <div class="ma-course-art ps-home-art" aria-hidden="true">
    <span class="ps-home-art-label">SAFE / {locale.upper()}</span>
    <div class="ps-home-art-diagram"><span class="ps-home-art-p">S</span><span class="ps-home-art-arrow">→</span><span class="ps-home-art-s">✓</span></div>
    <strong class="ps-home-art-brand">MANZO<span>AI</span></strong>
  </div>
  <div class="ma-course-info ps-home-info">
    <p class="ps-home-kind">{e(t["catalogType"])}</p>
    <h3 id="safe-home-title-{locale}">{e(t["catalogHeading"])}</h3>
    <p class="ps-home-desc">{e(t["homeDescription"])}</p>
    <div class="ps-home-tags"><span>{e(t["homeTags"][0])}</span><span>{e(t["homeTags"][1])}</span></div>
    <a href="{BASE}{ROUTES[locale]}/" class="ma-course-link ps-home-link"><span>{e(t["catalogCTA"])}</span><span class="ps-home-link-arrow" aria-hidden="true">↗</span></a>
  </div>
</article>'''

def run(site:Path,verify_only:bool=False):
    if not CSS.is_file():raise RuntimeError("Shared Academy card stylesheet missing")
    digest=hashlib.sha256(CSS.read_bytes()).hexdigest()[:12]
    asset=site/"assets/prompt-skill-home-card.css"
    if not verify_only:
        asset.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(CSS,asset)
    for locale in I18N:
        home=site/locale/"index.html"
        page=site/ROUTES[locale]/"index.html"
        if not home.is_file() or not page.is_file():raise RuntimeError(locale+": missing translated home or full course")
        html=home.read_text(encoding="utf-8")
        if html.count(GRID)!=1:raise RuntimeError(locale+": expected one Academy grid")
        if verify_only:
            if html.count(MARKER)!=1 or html.count('data-ma-course-card="1"')!=6:
                raise RuntimeError(locale+": missing new card or changed legacy six")
            if html.count('href="'+BASE+ROUTES[locale]+'/"')!=1:
                raise RuntimeError(locale+": translated course destination missing")
            if "prompt-skill-home-card.css?v="+digest not in html:
                raise RuntimeError(locale+": shared style version mismatch")
            if card(locale).count("ps-home-tags")!=1 or card(locale).count("ps-home-link-arrow")!=1:
                raise RuntimeError(locale+": card geometry invalid")
            continue
        if MARKER in html:raise RuntimeError(locale+": duplicate Home safety card")
        start=html.index(GRID)+len(GRID)
        section_end=html.find("ma-home-showcase-footer",start)
        if section_end<0:raise RuntimeError(locale+": missing Academy grid footer")
        original=list(ORIGINAL.finditer(html,start,section_end))
        if len(original)!=6:raise RuntimeError(locale+": original six Academy cards missing")
        last=html.rfind("</article>",original[-1].end(),section_end)
        insert=(last+len("</article>")) if last!=-1 else original[-1].end()
        # Italian pages already have three further custom cards; translate the new
        # safety course only and never invent translations for those legacy cards.
        html=html[:insert]+"\n"+card(locale)+html[insert:]
        href=f'{BASE}assets/prompt-skill-home-card.css?v={digest}'
        if "prompt-skill-home-card.css" not in html:
            html=html.replace("</head>",f'<link rel="stylesheet" href="{href}"></head>',1)
        elif href not in html:
            html=re.sub(r'/manzo-ai/assets/prompt-skill-home-card\.css\?v=[a-f0-9]{12}',href,html,count=1)
        home.write_text(html,encoding="utf-8")
    if not verify_only:run(site,True)
    else:
        if asset.read_bytes()!=CSS.read_bytes():raise RuntimeError("Shared Academy card CSS not copied")
        print("Build Safely: identical eighth/next Academy card geometry and translated Home destinations in IT EN ES PASS")

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--site",required=True,type=Path);p.add_argument("--verify-only",action="store_true")
    args=p.parse_args()
    run(args.site,args.verify_only)
