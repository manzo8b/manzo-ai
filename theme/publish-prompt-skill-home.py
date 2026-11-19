#!/usr/bin/env python3
"""Add the published Italian Prompt vs Skill course as a real Home Academy card.

Run AFTER publish-home-curation.py verification, to keep the original
six-card curated-home contract unchanged. Does not touch English/Spanish
homes because the complete course is currently Italian only.
"""
from __future__ import annotations
import argparse
import hashlib
from html import escape
from pathlib import Path
import re
import shutil

ROOT=Path(__file__).resolve().parent
CSS=ROOT/"prompt-skill-home-card.css"
BASE="/manzo-ai/"
ROUTE="it/formazione/prompt-vs-skill"
MARKER='data-ma-home-course="prompt-vs-skill"'
GRID='<div class="ma-course-grid ma-home-course-grid">'
CARD=re.compile(r'<article\b(?=[^>]*\bdata-ma-course-card=["\']1["\'])[^>]*>.*?</article\s*>',re.I|re.S)

def home_card()->str:
    url=BASE+ROUTE+"/"
    return f'''<article class="ma-course-card ps-home-course-card" {MARKER} data-ma-category="prompt" aria-labelledby="ps-home-course-title">
  <div class="ma-course-art ps-home-art" aria-hidden="true">
    <span class="ps-home-art-label">CORSO / NUOVO</span>
    <div class="ps-home-art-diagram">
      <span class="ps-home-art-p">P</span>
      <span class="ps-home-art-arrow">→</span>
      <span class="ps-home-art-s">S</span>
    </div>
    <strong class="ps-home-art-brand">MANZO<span>AI</span></strong>
  </div>
  <div class="ma-course-info ps-home-info">
    <p class="ps-home-kind">Corso completo</p>
    <h3 id="ps-home-course-title">Prompt vs Skill</h3>
    <p class="ps-home-desc">Dalla scrittura di un prompt all’architettura di una skill. Scopri quando fare il salto, come usare gli strumenti e perché il metodo serve anche senza IA.</p>
    <div class="ps-home-tags"><span>Prompt Engineering</span><span>Agent Skills</span><span>Laboratorio e quiz</span></div>
    <a href="{escape(url,quote=True)}" class="ma-course-link ps-home-link"><span>Apri il percorso</span><span class="ps-home-link-arrow" aria-hidden="true">↗</span></a>
  </div>
</article>'''

def run(site:Path,verify_only:bool=False)->None:
    home=site/"it/index.html"
    course=site/ROUTE/"index.html"
    if not home.is_file() or not course.is_file():
        raise RuntimeError("Cannot link an unpublished course from the Home")
    html=home.read_text(encoding="utf-8")
    if html.count(GRID)!=1:
        raise RuntimeError("Expected one existing Home Academy grid")
    start=html.index(GRID)+len(GRID)
    found=list(CARD.finditer(html,start))
    if len(found)<6 or found[5].start()-start>50000:
        raise RuntimeError("Original six Academy cards not found in Home grid")
    end_original=found[5].end()
    if html.find('ma-home-showcase-footer',start,end_original)>=0:
        raise RuntimeError("Academy grid ended before six cards")
    if not CSS.is_file():
        raise RuntimeError("Home course CSS missing")
    digest=hashlib.sha256(CSS.read_bytes()).hexdigest()[:12]
    asset=site/"assets/prompt-skill-home-card.css"
    if verify_only:
        if html.count(MARKER)!=1: raise RuntimeError("New course card missing or duplicated")
        if html.count('data-ma-course-card="1"')!=6: raise RuntimeError("Original Academy cards changed")
        if html.count(f'href="{BASE}{ROUTE}/"')!=1: raise RuntimeError("Home course link missing")
        if f'prompt-skill-home-card.css?v={digest}' not in html:
            raise RuntimeError("Home CSS version missing")
        if asset.read_bytes()!=CSS.read_bytes(): raise RuntimeError("Home asset mismatch")
        print("Prompt vs Skill: one seventh Academy-style card on Italian Home; original six untouched")
        return
    if MARKER in html: raise RuntimeError("Home card already installed")
    if html.count('data-ma-home-curation="v2"')!=1:
        raise RuntimeError("Home curation gate must finish first")
    asset.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(CSS,asset)
    card=home_card()
    html=html[:end_original]+"\n"+card+html[end_original:]
    tag=f'<link rel="stylesheet" href="{BASE}assets/prompt-skill-home-card.css?v={digest}" data-ps-home-style="v1">'
    if "</head>" not in html:raise RuntimeError("Missing Home head")
    html=html.replace("</head>",tag+"</head>",1)
    home.write_text(html,encoding="utf-8")
    run(site,verify_only=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--site",type=Path,required=True)
    p.add_argument("--verify-only",action="store_true")
    a=p.parse_args()
    run(a.site,a.verify_only)
