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
RELIABILITY_ROUTE="it/formazione/modelli-mentali-affidabilita-ai"
RELIABILITY_MARKER='data-ma-home-course="modelli-mentali-affidabilita"'
CENTRONI_ROUTE="it/formazione/ai-product-builder-centroni-city"
CENTRONI_MARKER='data-ma-home-course="ai-product-builder-centroni-city"'
MARKER='data-ma-home-course="prompt-vs-skill"'
GRID='<div class="ma-course-grid ma-home-course-grid">'
CARD=re.compile(r'<article\b(?=[^>]*\bdata-ma-course-card=["\']1["\'])[^>]*>.*?</article\s*>',re.I|re.S)

def home_card()->str:
    url=BASE+ROUTE+"/"
    return f'''<article class="ma-course-card ps-home-course-card" {MARKER} data-ma-category="prompt" aria-labelledby="ps-home-course-title">
  <div class="ma-course-art ps-home-art" aria-hidden="true">
    <span class="ps-home-art-label">SKILL / 07</span>
    <div class="ps-home-art-diagram">
      <span class="ps-home-art-p">P</span>
      <span class="ps-home-art-arrow">→</span>
      <span class="ps-home-art-s">S</span>
    </div>
    <strong class="ps-home-art-brand">MANZO<span>AI</span></strong>
  </div>
  <div class="ma-course-info ps-home-info">
    <p class="ps-home-kind">Corso</p>
    <h3 id="ps-home-course-title">Prompt vs Skill</h3>
    <p class="ps-home-desc">Impara a progettare prompt e skill, scegliere il metodo più adatto e verificarne i risultati.</p>
    <div class="ps-home-tags"><span>Prompting</span><span>Agent Skills</span></div>
    <a href="{escape(url,quote=True)}" class="ma-course-link ps-home-link"><span>Apri il percorso</span><span class="ps-home-link-arrow" aria-hidden="true">↗</span></a>
  </div>
</article>'''

def reliability_card()->str:
    """Reuse exactly the reviewed Prompt vs Skill card geometry and CTA."""
    url=BASE+RELIABILITY_ROUTE+"/"
    return f'''<article class="ma-course-card ps-home-course-card mr-home-course-card" {RELIABILITY_MARKER} data-ma-category="affidabilita" aria-labelledby="mr-home-course-title">
  <div class="ma-course-art ps-home-art" aria-hidden="true">
    <span class="ps-home-art-label">RISK / 08</span>
    <div class="ps-home-art-diagram">
      <span class="ps-home-art-p">AI</span>
      <span class="ps-home-art-arrow">→</span>
      <span class="ps-home-art-s">✓</span>
    </div>
    <strong class="ps-home-art-brand">MANZO<span>AI</span></strong>
  </div>
  <div class="ma-course-info ps-home-info">
    <p class="ps-home-kind">Corso</p>
    <h3 id="mr-home-course-title">Affidabilità dell'AI</h3>
    <p class="ps-home-desc">Oltre il prompt e la media: riconosci errori plausibili, valuta i casi limite e costruisci processi verificabili.</p>
    <div class="ps-home-tags"><span>Affidabilità</span><span>Valutazione AI</span></div>
    <a href="{escape(url,quote=True)}" class="ma-course-link ps-home-link"><span>Apri il percorso</span><span class="ps-home-link-arrow" aria-hidden="true">↗</span></a>
  </div>
</article>'''

def centroni_card()->str:
    """One shared Academy card structure: artwork, concise copy, two badges, CTA."""
    url=BASE+CENTRONI_ROUTE+"/"
    return f'''<article class="ma-course-card ps-home-course-card cc-home-course-card" {CENTRONI_MARKER} data-ma-category="product-building" aria-labelledby="cc-home-course-title">
  <div class="ma-course-art ps-home-art" aria-hidden="true">
    <span class="ps-home-art-label">CIVIC / 09</span>
    <div class="ps-home-art-diagram">
      <span class="ps-home-art-p">F</span>
      <span class="ps-home-art-arrow">→</span>
      <span class="ps-home-art-s">C</span>
    </div>
    <strong class="ps-home-art-brand">MANZO<span>AI</span></strong>
  </div>
  <div class="ma-course-info ps-home-info">
    <p class="ps-home-kind">Corso</p>
    <h3 id="cc-home-course-title">Centroni City</h3>
    <p class="ps-home-desc">Da Facebook a un prodotto civico: progetta servizi utili, costruisci un prototipo e verifica i risultati.</p>
    <div class="ps-home-tags"><span>Product Design</span><span>Civic Tech</span></div>
    <a href="{escape(url,quote=True)}" class="ma-course-link ps-home-link"><span>Apri il percorso</span><span class="ps-home-link-arrow" aria-hidden="true">↗</span></a>
  </div>
</article>'''

def run(site:Path,verify_only:bool=False)->None:
    home=site/"it/index.html"
    course=site/ROUTE/"index.html"
    reliability_course=site/RELIABILITY_ROUTE/"index.html"
    centroni_course=site/CENTRONI_ROUTE/"index.html"
    if not home.is_file() or not course.is_file() or not reliability_course.is_file() or not centroni_course.is_file():
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
    # Academy card design standard: 1 shared cover, 1 title, concise copy,
    # at most two chips, and a single horizontal CTA row on all viewports.
    if home_card().count('class="ps-home-tags"') != 1 or home_card().count('<span>Prompting</span><span>Agent Skills</span>') != 1:
        raise RuntimeError("New course card does not follow the two-tag catalog standard")
    if reliability_card().count('class="ps-home-tags"') != 1 or "Apri il percorso" not in reliability_card():
        raise RuntimeError("Reliability card must reuse Academy card structure")
    if centroni_card().count('class="ps-home-tags"') != 1 or "Apri il percorso" not in centroni_card():
        raise RuntimeError("Centroni card must reuse Academy card structure")
    digest=hashlib.sha256(CSS.read_bytes()).hexdigest()[:12]
    asset=site/"assets/prompt-skill-home-card.css"
    if verify_only:
        if html.count(MARKER)!=1: raise RuntimeError("New course card missing or duplicated")
        if html.count(RELIABILITY_MARKER)!=1: raise RuntimeError("Reliability course card missing or duplicated")
        if html.count(CENTRONI_MARKER)!=1: raise RuntimeError("Centroni City card missing or duplicated")
        new=html.split(MARKER,1)[1].split("</article>",1)[0]
        if "SKILL / 07" not in new or "Corso</p>" not in new:
            raise RuntimeError("Academy cover or teaching format inconsistent")
        if new.count('class="ps-home-link-arrow"') != 1 or new.count("ps-home-tags") != 1:
            raise RuntimeError("Academy CTA and tag structure inconsistent")
        if html.count('data-ma-course-card="1"')!=6: raise RuntimeError("Original Academy cards changed")
        if html.count(f'href="{BASE}{ROUTE}/"')!=1: raise RuntimeError("Home course link missing")
        if html.count(f'href="{BASE}{RELIABILITY_ROUTE}/"')!=1: raise RuntimeError("Reliability link missing")
        if html.count(f'href="{BASE}{CENTRONI_ROUTE}/"')!=1: raise RuntimeError("Centroni City link missing")
        if html.count('class="ma-course-card ps-home-course-card') != 3: raise RuntimeError("All three new cards must share visual geometry")
        if f'prompt-skill-home-card.css?v={digest}' not in html:
            raise RuntimeError("Home CSS version missing")
        if asset.read_bytes()!=CSS.read_bytes(): raise RuntimeError("Home asset mismatch")
        print("Home Academy: six existing cards + three uniform courses, no duplicate destinations")
        return
    if MARKER in html or RELIABILITY_MARKER in html or CENTRONI_MARKER in html: raise RuntimeError("Home card already installed")
    if html.count('data-ma-home-curation="v2"')!=1:
        raise RuntimeError("Home curation gate must finish first")
    asset.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(CSS,asset)
    card=home_card()+"\n"+reliability_card()+"\n"+centroni_card()
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
