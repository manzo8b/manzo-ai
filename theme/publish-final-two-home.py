#!/usr/bin/env python3
"""Add the final two complete, uniform Academy Home cards in IT EN ES.

Publish only after each native-language learning page and the previously
approved Governing Autonomy Home card exist. Keep the reviewed card geometry:
same article, art, info, two chips and horizontal CTA.
"""
from __future__ import annotations
import argparse
from html import escape
from pathlib import Path
from final_two_i18n_base import BASE,LOCALES,COURSES,CONTENT_UI
import final_two_i18n_aug  # side-effect: registers augmented course

MARKERS={"compliance":'data-ma-home-course="dynamic-compliance"',
         "augmented":'data-ma-home-course="augmented-intelligence"'}
ANCHOR='data-ma-home-course="governare-autonomia"'

def e(value):return escape(str(value),quote=True)
def card(kind,lang):
    t=CONTENT_UI[kind][lang]
    route=BASE+COURSES[kind]["routes"][lang]+"/"
    marker=MARKERS[kind]
    letters=("R","✓") if kind=="compliance" else ("H","A")
    visual=f'''<span class="ps-home-art-p">{letters[0]}</span>
<span class="ps-home-art-arrow" aria-hidden="true">→</span><span class="ps-home-art-s">{letters[1]}</span>'''
    return f'''<article class="ma-course-card ps-home-course-card ft-home-course-card ft-home-{kind}" {marker}
 data-ma-category="{kind}" aria-labelledby="ft-home-{kind}-{lang}">
  <div class="ma-course-art ps-home-art" aria-hidden="true">
    <span class="ps-home-art-label">{"AI ACT / GOVERNANCE" if kind=="compliance" else "HUMAN / AI"} · {lang.upper()}</span>
    <div class="ps-home-art-diagram">{visual}</div><strong class="ps-home-art-brand">MANZO<span>AI</span></strong>
  </div>
  <div class="ma-course-info ps-home-info">
    <p class="ps-home-kind">{e({"it":"CORSO PROFESSIONALE","en":"PROFESSIONAL COURSE","es":"CURSO PROFESIONAL"}[lang])}</p>
    <h3 id="ft-home-{kind}-{lang}">{e(t["title"])}</h3>
    <p class="ps-home-desc">{e(t["homeDescription"])}</p>
    <div class="ps-home-tags"><span>{e(t["homeTags"][0])}</span><span>{e(t["homeTags"][1])}</span></div>
    <a href="{route}" class="ma-course-link ps-home-link">
      <span>{e({"it":"Apri il corso","en":"Open course","es":"Abrir curso"}[lang])}</span>
      <span class="ps-home-link-arrow" aria-hidden="true">↗</span></a>
  </div>
</article>'''

def run(site,verify_only=False):
    for lang in LOCALES:
        home=site/lang/"index.html"
        if not home.is_file():raise RuntimeError(lang+": Home missing")
        for kind,conf in COURSES.items():
            if not (site/conf["routes"][lang]/"index.html").is_file():
                raise RuntimeError(lang+": no full translated page for "+kind)
        html=home.read_text(encoding="utf-8")
        if verify_only:
            for kind,marker in MARKERS.items():
                if html.count(marker)!=1:raise RuntimeError(lang+": course card missing or repeated "+kind)
                route=BASE+COURSES[kind]["routes"][lang]+"/"
                if html.count('href="'+route+'"')!=1:raise RuntimeError(lang+": wrong language for "+kind)
                if card(kind,lang).count('ps-home-tags')!=1 or card(kind,lang).count('ps-home-link-arrow')!=1:
                    raise RuntimeError(lang+": broken visual card geometry "+kind)
            if html.count('data-ma-course-card="1"')!=6:
                raise RuntimeError(lang+": original six curated cards changed")
            positions=[html.index(ANCHOR),html.index(MARKERS["compliance"]),html.index(MARKERS["augmented"])]
            if positions!=sorted(positions):raise RuntimeError(lang+": expected sequential course order")
            continue
        if any(marker in html for marker in MARKERS.values()):
            raise RuntimeError(lang+": duplicate final course Home cards")
        start=html.find(ANCHOR)
        if start<0:raise RuntimeError(lang+": preceding autonomy course card missing")
        end=html.find("</article>",start)
        if end<0:raise RuntimeError(lang+": invalid existing Academy card")
        pos=end+len("</article>")
        cards="\n"+card("compliance",lang)+"\n"+card("augmented",lang)
        html=html[:pos]+cards+html[pos:]
        home.write_text(html,encoding="utf-8")
    if verify_only:
        print("Final Academy Home: 6 uniform and translated additional cards, original curated 6 preserved PASS")
    else:run(site,True)

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--site",type=Path,required=True)
    p.add_argument("--verify-only",action="store_true")
    args=p.parse_args();run(args.site,args.verify_only)
