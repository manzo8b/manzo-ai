#!/usr/bin/env python3
"""Add localized Prompt vs Skill cards to EN/ES Home.
Run after original Academy six-card curation and Build Safely Home.
Preserve identical geometry; never link translated cards to the Italian page.
"""
from __future__ import annotations
import argparse
from html import escape
from pathlib import Path
from prompt_skill_i18n import BASE, ROUTES, UI

MARKER='data-ma-home-course="prompt-vs-skill"'
SAFE='data-ma-home-course="build-safely"'

def e(x):return escape(str(x),quote=True)

def card(lang):
    t=UI[lang];url=BASE+ROUTES[lang]+"/"
    return f'''<article class="ma-course-card ps-home-course-card ps-i18n-home-course-card" {MARKER} data-ma-category="prompting" aria-labelledby="ps-i18n-home-{lang}">
  <div class="ma-course-art ps-home-art" aria-hidden="true">
    <span class="ps-home-art-label">PROMPT / {lang.upper()}</span>
    <div class="ps-home-art-diagram"><span class="ps-home-art-p">P</span><span class="ps-home-art-arrow">→</span><span class="ps-home-art-s">S</span></div>
    <strong class="ps-home-art-brand">MANZO<span>AI</span></strong>
  </div>
  <div class="ma-course-info ps-home-info">
    <p class="ps-home-kind">{e(t["catalogTag"])}</p>
    <h3 id="ps-i18n-home-{lang}">Prompt vs Skill</h3>
    <p class="ps-home-desc">{e(t["homeDesc"])}</p>
    <div class="ps-home-tags"><span>{e(t["homeTags"][0])}</span><span>{e(t["homeTags"][1])}</span></div>
    <a href="{url}" class="ma-course-link ps-home-link"><span>{e(t["catalogCTA"])}</span><span class="ps-home-link-arrow" aria-hidden="true">↗</span></a>
  </div>
</article>'''

def run(site,verify_only=False):
    for lang in ("en","es"):
        page=site/lang/"index.html"
        target=site/ROUTES[lang]/"index.html"
        if not page.is_file() or not target.is_file():raise RuntimeError(lang+": missing Home or complete translated course")
        html=page.read_text(encoding="utf-8")
        if verify_only:
            if html.count(MARKER)!=1:raise RuntimeError(lang+": course Home card missing/duplicated")
            if html.count('data-ma-course-card="1"')!=6:raise RuntimeError(lang+": original six Academy cards changed")
            if html.count('href="'+BASE+ROUTES[lang]+'/"')!=1:raise RuntimeError(lang+": course link not localized")
            if html.count(SAFE)!=1:raise RuntimeError(lang+": Build Safely card lost")
            if card(lang).count('ps-home-tags')!=1:raise RuntimeError(lang+": nonuniform Academy card")
            continue
        if MARKER in html:raise RuntimeError(lang+": translated card already inserted")
        start=html.find(SAFE)
        if start<0:raise RuntimeError(lang+": Build Safely Home card missing")
        end=html.find("</article>",start)
        if end<0:raise RuntimeError(lang+": end of Academy card not found")
        pos=end+len("</article>")
        html=html[:pos]+"\n"+card(lang)+html[pos:]
        page.write_text(html,encoding="utf-8")
    if verify_only:print("Prompt vs Skill: EN/ES Home cards uniform and link to full translated pages PASS")
    else:run(site,True)

if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("--site",required=True,type=Path);a.add_argument("--verify-only",action="store_true")
    opts=a.parse_args();run(opts.site,opts.verify_only)
