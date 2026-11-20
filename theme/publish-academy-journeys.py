#!/usr/bin/env python3
"""MANZO AI: goal-based, accessible learning journeys built from REAL Academy cards.

No synthetic credentials, enrolments, progress or learner analytics. Links and
lesson titles are read directly from the published Academy in IT/EN/ES.
Safe, reversible enhancement to the generated release; source ZIP untouched.
"""
from __future__ import annotations

import argparse
from html import escape, unescape
from pathlib import Path
import re
import shutil
import hashlib

ROOT = Path(__file__).resolve().parent
ASSETS = ("academy-journeys.css", "academy-journeys.js")
MARKER = 'data-ma-journeys="v1"'
BASE = "/manzo-ai/"
ROUTES = {"it":"academy", "en":"academy", "es":"academia"}

COPY = {
 "it": {
  "eyebrow":"MANZO AI / PERCORSI GUIDATI",
  "title":"Non sai da dove iniziare?",
  "subtitle":"Scegli un obiettivo e segui una sequenza ragionata di lezioni già disponibili. Nessuna iscrizione e nessun avanzamento fittizio",
  "tabs":["Capire l’AI","Verificare le risposte","AI e sviluppo"],
  "goals":[
    ("Fondamenta pratiche","Per capire come funziona un modello, scrivere un buon prompt e organizzare il lavoro"),
    ("Risposte affidabili","Per separare una risposta plausibile da una verificata e applicare la catena delle prove"),
    ("Coding con controllo","Per preparare richieste chiare, verificare gli output e valutare il rischio nel codice AI"),
  ],
  "step":"Passaggio",
  "start":"Inizia da qui",
  "open":"Apri la lezione",
  "cta":"Apri la prima tappa",
  "download":"Stampa il percorso",
  "disclaimer":"Percorsi editoriali orientativi · Studio libero · Nessuna certificazione o progresso sincronizzato",
 },
 "en": {
  "eyebrow":"MANZO AI / GUIDED LEARNING",
  "title":"Not sure where to begin?",
  "subtitle":"Choose an outcome and follow an evidence-based sequence of lessons already available. No enrollment or fictional progress",
  "tabs":["Understand AI","Verify answers","AI and coding"],
  "goals":[
    ("Practical foundations","Learn how models work, write useful prompts and organize your workflow"),
    ("Trustworthy answers","Distinguish plausible claims from verified evidence and apply a verification workflow"),
    ("Responsible coding","Write clear requests, validate outputs and evaluate risks in AI-generated software"),
  ],
  "step":"Step",
  "start":"Start here",
  "open":"Open lesson",
  "cta":"Open the first step",
  "download":"Print learning plan",
  "disclaimer":"Editorial learning suggestions · Open access · No accredited credentials or synced progress",
 },
 "es": {
  "eyebrow":"MANZO AI / ITINERARIOS GUIADOS",
  "title":"¿No sabes por dónde empezar?",
  "subtitle":"Elige un objetivo y sigue una secuencia razonada de clases ya publicadas. Sin inscripción ni progreso ficticio",
  "tabs":["Comprender la IA","Verificar respuestas","IA y desarrollo"],
  "goals":[
    ("Fundamentos prácticos","Aprende cómo funcionan los modelos, cómo escribir prompts y organizar el trabajo"),
    ("Respuestas fiables","Distingue afirmaciones plausibles de pruebas verificadas y aprende un método de contraste"),
    ("Código bajo control","Plantea instrucciones claras, comprueba resultados y evalúa riesgos en el software generado"),
  ],
  "step":"Paso",
  "start":"Empieza aquí",
  "open":"Abrir lección",
  "cta":"Abrir la primera etapa",
  "download":"Imprimir itinerario",
  "disclaimer":"Itinerarios editoriales orientativos · Acceso libre · Sin certificados ni progreso sincronizado",
 }
}

NAV_COPY = {
 "it":{
  "label":"Navigazione del percorso guidato","route":"PERCORSO GUIDATO",
  "step":"Tappa","of":"di","next":"Prossima lezione","previous":"Lezione precedente",
  "back":"Torna al percorso","last":"Ultima tappa di questo itinerario"
 },
 "en":{
  "label":"Guided learning route navigation","route":"GUIDED LEARNING",
  "step":"Step","of":"of","next":"Next lesson","previous":"Previous lesson",
  "back":"Back to learning path","last":"Final step of this learning path"
 },
 "es":{
  "label":"Navegación del itinerario guiado","route":"ITINERARIO GUIADO",
  "step":"Etapa","of":"de","next":"Siguiente lección","previous":"Lección anterior",
  "back":"Volver al itinerario","last":"Última etapa de este itinerario"
 }
}

CONTINUITY='data-ma-journey-continuity='
FOLLOW_ASSET='data-ma-journey-follow-assets='

def route_url(target,index):
 return f"{target}?journey={index}"

def lesson_continuity(lang,index,sequence,cards,position):
 """Optional next/previous navigation for users following a specific route."""
 d=NAV_COPY[lang]
 current=cards[sequence[position]][1]
 heading=COPY[lang]["goals"][index][0]
 previous=(f'<a class="ma-journey-follow-previous" href="{e(route_url(cards[sequence[position-1]][0],index))}">'
           f'{e(d["previous"])} <span aria-hidden="true">↖</span></a>') if position>0 else ''
 next_step=(f'<a class="ma-journey-follow-next" href="{e(route_url(cards[sequence[position+1]][0],index))}">'
            f'{e(d["next"])} <span aria-hidden="true">↗</span></a>') if position<len(sequence)-1 else ''
 academy=f'{BASE}{lang}/{ROUTES[lang]}/?journey={index}#ma-journey-title-{lang}'
 return (f'<nav class="ma-journey-continuation" {CONTINUITY}"{index}" hidden '
         f'aria-label="{e(d["label"])}">'
         f'<span class="ma-journey-follow-kicker">{e(d["route"])} · {e(d["step"])} '
         f'{position+1} {e(d["of"])} {len(sequence)}</span>'
         f'<h2>{e(heading)}</h2>'
         f'<p>{e(current) if position<len(sequence)-1 else e(d["last"])}</p>'
         '<div class="ma-journey-follow-links">'
         f'<a class="ma-journey-follow-back" href="{e(academy)}">{e(d["back"])}</a>'
         +previous+next_step+'</div></nav>')

def add_lesson_continuity(site,lang,cards,links,verify_only=False):
 """One small footer per active path; no modification of course lessons/content."""
 destinations={}
 for index,sequence in enumerate(SEQUENCES):
  for pos,card_index in enumerate(sequence):
   destinations.setdefault(cards[card_index][0],[]).append(
     lesson_continuity(lang,index,sequence,cards,pos))
 css_url=links[0]
 js_url=links[1]
 for target,navs in destinations.items():
  page=site/target[len(BASE):]/"index.html"
  if not page.is_file():raise RuntimeError("Guided lesson missing "+str(page))
  doc=page.read_text(encoding="utf-8")
  if verify_only:
   if doc.count(CONTINUITY)!=len(navs):
    raise RuntimeError("Guided lesson continuity missing or duplicated "+str(page))
   if doc.count(FOLLOW_ASSET)!=2:
    raise RuntimeError("Guided lesson continuity assets missing "+str(page))
   for nav in navs:
    if nav not in doc:raise RuntimeError("Incorrect guided next/prev navigation "+str(page))
   continue
  if CONTINUITY in doc or FOLLOW_ASSET in doc:
   raise RuntimeError("Guided navigation injection is not idempotent "+str(page))
  closing=list(re.finditer(r'</main\\s*>',doc,re.I))
  if len(closing)!=1:
   raise RuntimeError("One main closing tag expected in guided lesson "+str(page))
  at=closing[0].start()
  doc=doc[:at]+''.join(navs)+doc[at:]
  where=re.search(r'</head\\s*>',doc,re.I)
  if not where:raise RuntimeError("Missing document head "+str(page))
  tag=(css_url.replace('data-ma-journey-asset="css"', 'data-ma-journey-follow-assets="css"')+
       js_url.replace('data-ma-journey-asset="js"', 'data-ma-journey-follow-assets="js"'))
  doc=doc[:where.start()]+tag+doc[where.start():]
  page.write_text(doc,encoding="utf-8")

# Three deliberately curated educational sequences. Indices refer exclusively to
# the existing six Academy cards, whose destinations are verified at build time.
SEQUENCES = ((2,3,5), (2,4,0), (3,4,1))
CARD = re.compile(
 r'<article\b(?=[^>]*\bdata-ma-course-card=["\']1["\'])[^>]*>.*?</article\s*>',
 re.I | re.S)
LINK = re.compile(r'<a\b[^>]*\bhref="([^"]+)"',re.I)
H3 = re.compile(r'<h3\b[^>]*>(.*?)</h3>',re.I|re.S)
CAT = re.compile(r'data-ma-category="([^"]+)"')
SECTION_OPEN = re.compile(r'<section\b(?=[^>]*\bdata-ma-pathways=["\']v1["\'])[^>]*>',re.I|re.S)
FEATURE = re.compile(r'<section\b(?=[^>]*\bdata-atl-feature=["\']2026-11["\'])[^>]*>.*?</section\s*>',re.I|re.S)
SECTIONS = re.compile(r'</?section\b[^>]*>',re.I|re.S)

def e(text): return escape(str(text),quote=True)

def card_info(site,lang):
 p=site/lang/ROUTES[lang]/"index.html"
 if not p.exists():raise RuntimeError("Missing Academy page: "+str(p))
 doc=p.read_text(encoding="utf-8")
 cards=CARD.findall(doc)
 if len(cards)!=6:raise RuntimeError(f"Expected 6 Academy cards, got {len(cards)}: {lang}")
 result=[]
 for markup in cards:
  href=LINK.search(markup)
  title=H3.search(markup)
  cat=CAT.search(markup)
  if not href or not title or not cat:raise RuntimeError("Incomplete Academy card "+lang)
  target=unescape(href.group(1))
  if not target.startswith(f"{BASE}{lang}/") or not target.endswith("/"):
   raise RuntimeError("Unexpected Academy href "+target)
  path=site/target[len(BASE):]/"index.html"
  if not path.is_file():raise RuntimeError("Broken Academy href "+str(path))
  label=unescape(re.sub(r"<[^>]+>","",title.group(1))).strip()
  if not label:raise RuntimeError("Empty card title")
  result.append((target,label,cat.group(1)))
 expected=["verify","coding","fundamentals","prompt","verify","workflow"]
 if [item[2] for item in result]!=expected:raise RuntimeError("Academy taxonomy changed")
 if len({r[0] for r in result})!=6:raise RuntimeError("Duplicate Academy URLs")
 return result

def catalog_end(doc):
 m=SECTION_OPEN.search(doc)
 if not m:raise RuntimeError("Academy catalog not found")
 depth=1
 for t in SECTIONS.finditer(doc,m.end()):
  if t.group().startswith("</"): depth-=1
  else:depth+=1
  if depth==0:return t.end()
 raise RuntimeError("Unbalanced Academy catalog")

def render(lang,cards):
 d=COPY[lang]
 tabs="".join(
  f'<button class="ma-journey-choice" type="button" data-ma-journey-choice="{n}" '
  f'aria-controls="ma-journey-panel-{lang}-{n}" aria-pressed="{str(n==0).lower()}">'
  f'<span class="ma-journey-choice-number">0{n+1}</span>{e(label)}</button>'
  for n,label in enumerate(d["tabs"])
 )
 panels=[]
 for n,route in enumerate(SEQUENCES):
  heading,subtitle=d["goals"][n]
  steps=[]
  for i,index in enumerate(route):
   href,label,_=cards[index]
   steps.append(
    '<li class="ma-journey-step">'
    f'<span class="ma-journey-step-order">{i+1:02d}</span>'
    '<div class="ma-journey-step-body">'
    f'<span class="ma-journey-step-caption">{e(d["start"] if i==0 else d["step"])}</span>'
    f'<a href="{e(route_url(href,n))}" class="ma-journey-step-title">{e(label)}'
    '<span aria-hidden="true">↗</span></a>'
    '</div></li>'
   )
  first=cards[route[0]][0]
  panels.append(
   f'<div class="ma-journey-panel" id="ma-journey-panel-{lang}-{n}" data-ma-journey-panel="{n}">'
   '<div class="ma-journey-panel-copy">'
   f'<span class="ma-journey-panel-index">MANZO AI / 0{n+1}</span>'
   f'<h3>{e(heading)}</h3><p>{e(subtitle)}</p>'
   f'<a class="ma-journey-start" href="{e(route_url(first,n))}">{e(d["cta"])}'
   '<span aria-hidden="true">↗</span></a>'
   '</div>'
   '<ol class="ma-journey-steps">'+''.join(steps)+'</ol>'
   '</div>'
  )
 return (
  f'<section class="ma-learning-journey" {MARKER} aria-labelledby="ma-journey-title-{lang}">'
  '<div class="ma-journey-intro">'
  f'<p class="ma-journey-eyebrow">{e(d["eyebrow"])}</p>'
  f'<h2 id="ma-journey-title-{lang}">{e(d["title"])}</h2>'
  f'<p class="ma-journey-subtitle">{e(d["subtitle"])}</p>'
  '</div>'
  f'<div class="ma-journey-choices" role="group" aria-label="{e(d["title"])}">'+tabs+'</div>'
  +''.join(panels)+
  '<div class="ma-journey-footer">'
  f'<p>{e(d["disclaimer"])}</p>'
  f'<button type="button" class="ma-journey-print" data-ma-journey-print>{e(d["download"])}'
  '<span aria-hidden="true">↗</span></button>'
  '</div></section>'
 )

def apply(site,verify_only=False):
 assets=site/"assets"
 for name in ASSETS:
  src=ROOT/name
  target=assets/name
  if not src.is_file():raise RuntimeError("Missing publisher asset "+name)
  if not verify_only:
   assets.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,target)
  if not target.is_file() or src.read_bytes()!=target.read_bytes():raise RuntimeError("Asset mismatch "+name)
 version=hashlib.sha256(b"".join((ROOT/name).read_bytes() for name in ASSETS)).hexdigest()[:12]
 links=(f'<link rel="stylesheet" href="{BASE}assets/academy-journeys.css?v={version}" data-ma-journey-asset="css">'
        f'<script defer src="{BASE}assets/academy-journeys.js?v={version}" data-ma-journey-asset="js"></script>')
 for lang in COPY:
  p=site/lang/ROUTES[lang]/"index.html"
  doc=p.read_text(encoding="utf-8")
  cards=card_info(site,lang)
  if verify_only:
   if doc.count(MARKER)!=1:raise RuntimeError("Missing/duplicate journey: "+lang)
   if doc.count('data-ma-journey-choice=')!=3 or doc.count('data-ma-journey-panel=')!=3:
    raise RuntimeError("Journey controls missing: "+lang)
   if doc.count('data-ma-journey-asset=')!=2:raise RuntimeError("Journey assets missing")
   if f'academy-journeys.css?v={version}' not in doc:raise RuntimeError("Version mismatch "+lang)
   main=re.search(r'<main\b[^>]*>',doc,re.I)
   catalog=SECTION_OPEN.search(doc)
   journey=re.search(r'<section\b(?=[^>]*\bdata-ma-journeys=["\']v1["\'])',doc,re.I)
   feature=FEATURE.search(doc)
   if not (main and catalog and journey and feature and
           main.end()<=catalog.start()<journey.start()<feature.start()):
    raise RuntimeError("Academy catalog must precede guided paths and specialist feature "+lang)
   for route in SEQUENCES:
    for index in route:
     if f'href="{e(cards[index][0])}"' not in doc:raise RuntimeError("Broken journey route")
   continue
  if MARKER in doc or 'data-ma-journey-asset=' in doc:raise RuntimeError("Duplicate journey")
  features=list(FEATURE.finditer(doc))
  if len(features)!=1:raise RuntimeError("Expected exactly one Teaching Lab feature "+lang)
  feature=features[0].group(0)
  doc=doc[:features[0].start()]+doc[features[0].end():]
  offset=catalog_end(doc)
  doc=doc[:offset]+render(lang,cards)+feature+doc[offset:]
  where=re.search(r'</head\s*>',doc,re.I)
  if not where:raise RuntimeError("Head missing: "+lang)
  doc=doc[:where.start()]+links+doc[where.start():]
  p.write_text(doc,encoding="utf-8")
  add_lesson_continuity(site,lang,cards,(links[:links.index('<script')],links[links.index('<script'):]),verify_only)
 print("MANZO AI Academy guided learning: 3 paths × 3 languages, contextual next/previous lesson links; verified="+str(verify_only))

if __name__=="__main__":
 parser=argparse.ArgumentParser()
 parser.add_argument("--site",type=Path,required=True)
 parser.add_argument("--verify-only",action="store_true")
 args=parser.parse_args()
 apply(args.site,args.verify_only)
