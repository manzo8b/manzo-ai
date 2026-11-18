#!/usr/bin/env python3
"""MANZO AI — language-preserving conversational discovery for the three homepages.

Preserves the existing home hero search and Academy showcase. The four goals are
grounded in REAL published Academy/Product/Mission routes, never in fake AI replies.
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
  "eyebrow":"MANZO AI / PERCORSI FORMATIVI",
  "heading":"Da dove vuoi iniziare?",
  "tag":"Percorsi disponibili",
  "open":"Apri il percorso",
  "group":"Scegli un obiettivo",
  "note":"Puoi cercare una lezione oppure scegliere un obiettivo. I suggerimenti utilizzano contenuti disponibili, senza generare risposte IA.",
  "goals":[
   ("Progettare una lezione","AI Teaching Lab · Mission Studio","Crea un brief didattico e prosegui nei laboratori multimediali per docenti e formatori."),
   ("Scrivere prompt efficaci","Prompt Engineering","Esercitati a scrivere istruzioni chiare e a verificare i risultati ottenuti."),
   ("Verificare una risposta IA","Verifica e pensiero critico","Impara a confrontare affermazioni, evidenze e fonti originali."),
     ],
 },
 "en":{
  "eyebrow":"MANZO AI / LEARNING PATHS",
  "heading":"Where would you like to begin?",
  "tag":"Available learning resources",
  "open":"Open this path",
  "group":"Choose a goal",
  "note":"Search the catalog or select a goal. Suggestions are based on available resources, not generated AI replies.",
  "goals":[
   ("Plan a teaching activity","AI Teaching Lab · Mission Studio (Italian)","Prepare an educational brief with the Italian teacher-training micro-app; English translation is not available yet."),
   ("Improve my prompts","Prompt Engineering lessons","Learn practical prompting from an existing Academy resource."),
   ("Check an AI response","Evidence and critical thinking","Examine claims and sources using real published educational resources."),
     ],
 },
 "es":{
  "eyebrow":"MANZO AI / ITINERARIOS DE APRENDIZAJE",
  "heading":"¿Por dónde quieres empezar?",
  "tag":"Recursos disponibles",
  "open":"Abrir este recorrido",
  "group":"Elige un objetivo",
  "note":"Busca una lección o elige un objetivo. Las sugerencias proceden de contenidos disponibles, no de respuestas generadas por IA.",
  "goals":[
   ("Preparar una actividad didáctica","AI Teaching Lab · Mission Studio (italiano)","Diseña una actividad con la micro-app italiana. La traducción al español aún no está disponible."),
   ("Mejorar mis prompts","Lecciones de Prompt Engineering","Aprende a escribir instrucciones útiles mediante lecciones ya publicadas."),
   ("Verificar respuestas de IA","Evidencias y pensamiento crítico","Contrasta afirmaciones con fuentes en los recursos disponibles de la Academia."),
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
 teacher=BASE+"it/formazione/ia-per-la-didattica/inizia/"
 product=BASE+locale+"/"+PRODUCT[locale]+"/"
 hrefs=(teacher,catalog["prompt"][0],catalog["verify"][0])
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
