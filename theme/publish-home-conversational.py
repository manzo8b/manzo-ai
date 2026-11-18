#!/usr/bin/env python3
"""MANZO AI — language-preserving conversational discovery for the three homepages.

Preserves the existing home hero search and six Academy cards. Four general-purpose goals
lead to REAL published lessons and labs, never simulated AI replies.
This publisher runs after the three Academies and the Italian Mission Studio exist.
"""
from __future__ import annotations
import argparse
import hashlib
from html import escape, unescape
from pathlib import Path
import re
import shutil

ROOT=Path(__file__).resolve().parent
BASE="/manzo-ai/"
MARKER='data-ma-home-discovery="v1"'
ASSETS=("home-conversational.css","home-conversational.js")
ACADEMY={"it":"academy","en":"academy","es":"academia"}
PRODUCT={"it":"prodotto","en":"product","es":"producto"}
HERO=re.compile(r'<section\b[^>]*\bclass=["\'][^"\']*\bhome-hero\b[^"\']*["\'][^>]*>',re.I|re.S)
CLOSE=re.compile(r'</?section\b[^>]*>',re.I|re.S)
CARD=re.compile(r'<article\b(?=[^>]*\bdata-ma-course-card=["\']1["\'])[^>]*>.*?</article\s*>',re.I|re.S)
LINK=re.compile(r'<a\b[^>]*\bhref="([^"]+)"',re.I)
CAT=re.compile(r'data-ma-category="([^"]+)"')
TITLE=re.compile(r'<h3\b[^>]*>(.*?)</h3>',re.I|re.S)
COPY={
 "it":{
  "eyebrow":"MANZO AI / ESPLORA L'INTELLIGENZA ARTIFICIALE",
  "heading":"Cosa vorresti scoprire oggi?",
  "tag":"Scegli il tuo percorso",
  "open":"Esplora",
  "group":"Obiettivi di apprendimento",
  "note":"Scegli ciò che ti interessa oppure cerca una lezione. Tutti i percorsi rimandano a contenuti realmente disponibili.",
  "goals":[
   ("Capire l'IA","Parti dalle basi","Scopri come funzionano i modelli, cosa possono fare e dove serve il giudizio umano."),
   ("Scrivere prompt migliori","Prompt Engineering","Impara a dare istruzioni chiare, confrontare risposte e ottenere risultati controllabili."),
   ("Riconoscere le allucinazioni","Allucinazioni dell'IA","Capisci perché l'IA può inventare informazioni e come verificare risposte e fonti."),
   ("Creare e sperimentare","IA per progetti digitali","Passa dalla teoria alla pratica con esempi di coding e produzione responsabile."),
  ],
 },
 "en":{
  "eyebrow":"MANZO AI / EXPLORE ARTIFICIAL INTELLIGENCE",
  "heading":"What would you like to explore today?",
  "tag":"Find your learning path",
  "open":"Explore",
  "group":"Learning goals",
  "note":"Choose a topic or search for a lesson. Every path links to an existing learning resource.",
  "goals":[
   ("Understand AI","Start with the foundations","Learn what models do, how they work and when human judgment is essential."),
   ("Write better prompts","Prompt Engineering","Practice clear instructions, compare responses and check results."),
   ("Spot AI hallucinations","AI hallucinations","Understand why AI can invent details and learn how to check claims and sources."),
   ("Build and experiment","AI for digital projects","Move from theory to practice with coding and responsible production."),
  ],
 },
 "es":{
  "eyebrow":"MANZO AI / EXPLORA LA INTELIGENCIA ARTIFICIAL",
  "heading":"¿Qué te gustaría descubrir hoy?",
  "tag":"Encuentra tu recorrido",
  "open":"Explorar",
  "group":"Objetivos de aprendizaje",
  "note":"Elige lo que te interesa o busca una lección. Todos los enlaces llevan a recursos realmente disponibles.",
  "goals":[
   ("Comprender la IA","Empieza por lo esencial","Descubre qué hacen los modelos, cómo funcionan y cuándo importa el criterio humano."),
   ("Escribir mejores prompts","Prompt Engineering","Practica instrucciones claras, compara respuestas y comprueba resultados."),
   ("Detectar alucinaciones","Alucinaciones de la IA","Comprende por qué la IA puede inventar datos y aprende a verificar afirmaciones y fuentes."),
   ("Crear y experimentar","IA para proyectos digitales","Pasa de la teoría a la práctica mediante ejemplos de código y producción responsable."),
  ],
 },
}

def e(s): return escape(str(s),quote=True)

def hero_end(html):
 match=HERO.search(html)
 if not match:raise RuntimeError("Missing home-hero: homepage structure changed")
 depth=1
 for m in CLOSE.finditer(html,match.end()):
  if m.group(0).startswith("</"):depth-=1
  else:depth+=1
  if depth==0:return m.start()
 raise RuntimeError("Unbalanced home hero")

def discovery_position(html):
 """Place the interactive gateway before the decorative product scene.

 On mobile the product scene becomes a tall block; novice actions must precede it.
 """
 end=hero_end(html)
 start=HERO.search(html)
 if not start:raise RuntimeError("Missing home hero")
 match=re.search(r'<aside\b[^>]*\bclass=["\'][^"\']*\bma-product-scene\b[^"\']*["\'][^>]*>',html[start.end():end],re.I|re.S)
 return start.end()+match.start() if match else end

def cards_from_academy(site,locale):
 path=site/locale/ACADEMY[locale]/"index.html"
 if not path.is_file():raise RuntimeError("Academy unavailable: "+str(path))
 cards=CARD.findall(path.read_text(encoding="utf-8"))
 if len(cards)!=6:raise RuntimeError(f"Expected six real Academy cards: {locale}, got {len(cards)}")
 result={}
 for card in cards:
  link=LINK.search(card);category=CAT.search(card);title=TITLE.search(card)
  if not link or not category or not title:raise RuntimeError("Incomplete Academy card "+locale)
  href=unescape(link.group(1))
  if not href.startswith(BASE+locale+"/"):raise RuntimeError("Unexpected Academy route "+href)
  target=site/href[len(BASE):].strip("/")/"index.html"
  if not target.is_file():raise RuntimeError("Broken Academy route "+href)
  result.setdefault(category.group(1),[]).append(href)
 if "prompt" not in result or "verify" not in result:raise RuntimeError("Learning taxonomy missing "+locale)
 return result

def destination(site,href):
 if not href.startswith(BASE) or not href.endswith("/"):raise RuntimeError("Invalid destination "+href)
 target=site/href[len(BASE):]/"index.html"
 if not target.is_file():raise RuntimeError("Missing published destination "+str(target))
 return href

def render(site,locale):
 copy=COPY[locale]
 catalog=cards_from_academy(site,locale)
 hallucination=BASE+{"it":"it/impara/allucinazioni-ai-verificabilita/","en":"en/learn/ai-hallucinations-verification/","es":"es/aprende/alucinaciones-ia-verificacion/"}[locale]
 hrefs=(catalog["fundamentals"][0],catalog["prompt"][0],hallucination,catalog["coding"][0])
 for href in hrefs:destination(site,href)
 choices=[]
 for n,(label,title,description) in enumerate(copy["goals"]):
  href=hrefs[n]
  choices.append(
   f'<a class="ma-discovery-choice" href="{e(href)}" data-ma-intent="{n}" '
   f'data-ma-title="{e(title)}" data-ma-description="{e(description)}" '
   f'data-ma-action="{e(copy["open"])}" aria-current="{"true" if n==0 else "false"}">'
   f'<span>{e(label)}</span><span class="ma-arrow" aria-hidden="true">↗</span></a>'
  )
 first=copy["goals"][0]
 return (
  f'<div {MARKER} class="ma-discovery" data-locale="{locale}" aria-labelledby="ma-discovery-title-{locale}">'
  '<div class="ma-discovery-top">'
  f'<p class="ma-discovery-label">{e(copy["eyebrow"])}</p>'
  f'<span class="ma-discovery-honesty">{e(copy["tag"])}</span></div>'
  f'<h2 id="ma-discovery-title-{locale}">{e(copy["heading"])}</h2>'
  f'<div class="ma-discovery-goals" role="group" aria-label="{e(copy["group"])}">'
  +''.join(choices)+'</div>'
  '<div class="ma-discovery-result">'
  f'<div><strong data-ma-discovery-title>{e(first[1])}</strong>'
  f'<p data-ma-discovery-summary>{e(first[2])}</p></div>'
  f'<a data-ma-discovery-action href="{e(teacher)}">{e(copy["open"])}</a>'
  '</div>'
  f'<p class="ma-discovery-foot">{e(copy["note"])}</p>'
  '<p data-ma-discovery-live class="sr-only" role="status" aria-live="polite"></p></div>'
 )

def apply(site,verify_only=False):
 if not (site/"index.html").is_file():raise RuntimeError("Missing preserved root language gateway")
 assets=site/"assets"
 digest=hashlib.sha256(b"".join((ROOT/f).read_bytes() for f in ASSETS)).hexdigest()[:12]
 if not verify_only:
  assets.mkdir(parents=True,exist_ok=True)
  for f in ASSETS:shutil.copyfile(ROOT/f,assets/f)
 for f in ASSETS:
  if not (assets/f).is_file() or (assets/f).read_bytes()!=(ROOT/f).read_bytes():
   raise RuntimeError("Home discovery asset mismatch "+f)
 tags=(
  f'<link data-ma-home-discovery-asset="v1" rel="stylesheet" href="{BASE}assets/home-conversational.css?v={digest}">'
  f'<script data-ma-home-discovery-asset="v1" src="{BASE}assets/home-conversational.js?v={digest}" defer></script>'
 )
 for locale in COPY:
  page=site/locale/"index.html"
  if not page.is_file():raise RuntimeError("Missing localized homepage "+locale)
  html=page.read_text(encoding="utf-8")
  if not HERO.search(html) or not re.search(r'class=["\'][^"\']*\bsearchbox\b',html,re.I):
   raise RuntimeError("Existing homepage hero/search not found "+locale)
  if verify_only:
   if html.count(MARKER)!=1 or html.count('data-ma-home-discovery-asset="v1"')!=2:
    raise RuntimeError("Missing or duplicated conversational gateway "+locale)
   if f"home-conversational.js?v={digest}" not in html or f"home-conversational.css?v={digest}" not in html:
    raise RuntimeError("Stale conversational gateway assets "+locale)
   for href in (BASE+"it/formazione/ia-per-la-didattica/inizia/",BASE+locale+"/"+PRODUCT[locale]+"/"):
    if f'href="{href}"' not in html:raise RuntimeError("Missing goal destination "+href)
   continue
  if MARKER in html or 'data-ma-home-discovery-asset=' in html:
   raise RuntimeError("Duplicate homepage gateway "+locale)
  insert_at=discovery_position(html)
  html=html[:insert_at]+render(site,locale)+html[insert_at:]
  head=re.search(r"</head\s*>",html,re.I)
  if not head:raise RuntimeError("Missing head close "+locale)
  html=html[:head.start()]+tags+html[head.start():]
  page.write_text(html,encoding="utf-8")
 print(f"MANZO AI conversational gateway: IT/EN/ES · truthful recommendations · verified={verify_only}")

if __name__=="__main__":
 parser=argparse.ArgumentParser()
 parser.add_argument("--site",required=True,type=Path)
 parser.add_argument("--verify-only",action="store_true")
 args=parser.parse_args()
 apply(args.site,args.verify_only)
