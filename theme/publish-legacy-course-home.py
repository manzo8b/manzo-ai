#!/usr/bin/env python3
"""Two translated, symmetrical Academy Home cards. Original IT cards preserved."""
from __future__ import annotations
import argparse
from html import escape
from pathlib import Path
from legacy_learning_i18n import BASE, COURSES, UI, SHARED
MARKERS={"reliability":'data-ma-home-course="reliability-i18n"',
         "centroni":'data-ma-home-course="centroni-i18n"'}
ANCHOR='data-ma-home-course="augmented-intelligence"'
def e(v):return escape(str(v),quote=True)
def make_card(kind,locale):
    t=UI[kind][locale];s=SHARED[locale]
    route=BASE+COURSES[kind]["routes"][locale]+"/"
    letters=("R","✓") if kind=="reliability" else ("C","C")
    return f'''<article class="ma-course-card ps-home-course-card lgi-home-card lgi-home-{kind}" {MARKERS[kind]}
 data-ma-category="{kind}" aria-labelledby="lgi-home-{kind}-{locale}">
<div class="ma-course-art ps-home-art" aria-hidden="true">
 <span class="ps-home-art-label">{"RELIABILITY" if kind=="reliability" else "CIVIC PRODUCT"} / {locale.upper()}</span>
 <div class="ps-home-art-diagram"><span class="ps-home-art-p">{letters[0]}</span>
 <span class="ps-home-art-arrow">→</span><span class="ps-home-art-s">{letters[1]}</span></div>
 <strong class="ps-home-art-brand">MANZO<span>AI</span></strong>
</div><div class="ma-course-info ps-home-info">
<p class="ps-home-kind">{e(s["tag"])}</p><h3 id="lgi-home-{kind}-{locale}">{e(t["title"])}</h3>
<p class="ps-home-desc">{e(t["home"])}</p>
<div class="ps-home-tags"><span>{e(t["chips"][0])}</span><span>{e(t["chips"][1])}</span></div>
<a href="{route}" class="ma-course-link ps-home-link"><span>{e(s["homeOpen"])}</span>
<span class="ps-home-link-arrow" aria-hidden="true">↗</span></a></div></article>'''

def run(site,verify_only=False):
    for locale in ("en","es"):
        page=site/locale/"index.html"
        if not page.is_file():raise RuntimeError(locale+": Home missing")
        for kind in MARKERS:
            if not (site/COURSES[kind]["routes"][locale]/"index.html").is_file():
                raise RuntimeError("No translated course page: "+kind+" "+locale)
        html=page.read_text(encoding="utf-8")
        if verify_only:
            for kind,marker in MARKERS.items():
                if html.count(marker)!=1:raise RuntimeError(locale+": duplicated or missing Home card "+kind)
                if html.count('href="'+BASE+COURSES[kind]["routes"][locale]+'/"')!=1:
                    raise RuntimeError(locale+": broken localized course link "+kind)
            if html.count('data-ma-course-card="1"')!=6:
                raise RuntimeError(locale+": six curated original cards altered")
            idx=[html.index(ANCHOR),html.index(MARKERS["reliability"]),html.index(MARKERS["centroni"])]
            if idx!=sorted(idx):raise RuntimeError(locale+": course cards out of order")
            continue
        if any(marker in html for marker in MARKERS.values()):
            raise RuntimeError(locale+": duplicate translated cards")
        start=html.find(ANCHOR)
        if start<0:raise RuntimeError("Prior Academy card missing")
        end=html.find("</article>",start)
        if end<0:raise RuntimeError("Prior Academy card malformed")
        pos=end+len("</article>")
        html=html[:pos]+"\n"+make_card("reliability",locale)+"\n"+make_card("centroni",locale)+html[pos:]
        page.write_text(html,encoding="utf-8")
    if verify_only:
        print("Legacy Academy Home: four uniform EN/ES cards, fully translated destinations; original curated six preserved PASS")
    else:run(site,True)
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--site",type=Path,required=True)
    p.add_argument("--verify-only",action="store_true")
    args=p.parse_args();run(args.site,args.verify_only)
