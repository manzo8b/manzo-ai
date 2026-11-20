#!/usr/bin/env python3
"""MANZO AI Sprint 1: editorial-first, pedagogical trilingual Home.

This is a reversible, final Home presentation overlay. It preserves:
- the root language gateway and its motion/behaviour UNMODIFIED
- all six existing Academy cards and seven appended courses
- the original home search, four intent links and sidebar/navigation
- existing live routes and source content.

Transforms the four redundant 'topic' cards into a meaningful learning method:
Understand -> Experiment -> Verify -> Build. Adds an honest, accessible
show-more control for the long course grid (without JS, all cards remain visible).
"""
from __future__ import annotations
import argparse
import hashlib
from html import escape
from pathlib import Path
import re
import shutil

ROOT=Path(__file__).resolve().parent
BASE="/manzo-ai/"
CSS=ROOT/"sprint1-home.css"
JS=ROOT/"sprint1-home.js"
MARKER='data-ma-sprint1-home="v1"'
DATA={
"it":{
 "hero":"L'AI si impara facendo",
 "lead":"Comprendi le idee, sperimenta con metodo e verifica i risultati. Poi trasformali in un progetto utile.",
 "heroMicro":"DALLA DOMANDA ALLA SOLUZIONE",
 "heroSteps":["Capire","Provare","Verificare","Costruire"],
 "start":"Scegli come iniziare",
 "academy":"Vai all'Academy",
 "stage":"MANZO AI / IL METODO DI APPRENDIMENTO",
 "section":"Quattro passi. Una competenza reale",
 "intro":"Niente percorsi impersonali: scegli un passo, prova un'attività e porta con te qualcosa che sai spiegare e usare.",
 "cta":"Esplora il passo",
 "steps":[
  ("Comprendi","Una mappa mentale chiara di ciò che l'AI può e non può fare","La base"),
  ("Sperimenta","Scrivi un prompt, confronta gli esiti e migliora le istruzioni","Il laboratorio"),
  ("Verifica","Metti alla prova un'affermazione: fonti, limiti e incertezza","Il controllo"),
  ("Costruisci","Progetta Centroni City: da un problema reale a un prototipo civico","Il prodotto")
 ],
 "deckTitle":"Esplora i percorsi",
 "deckLead":"Dal primo concetto ai laboratori avanzati: corsi e lezioni pubblicati, con esercizi, fonti e verifiche.",
 "more":"Mostra tutti i",
 "less":"Mostra la selezione",
 "unit":"percorsi",
 "count":"percorsi visualizzati",
 "footnote":"Tutti i percorsi restano disponibili anche nel catalogo Academy"
},
"en":{
 "hero":"Learn AI by building understanding",
 "lead":"Understand ideas, experiment with purpose and verify the result. Then turn your learning into something useful.",
 "heroMicro":"FROM THE QUESTION TO THE SOLUTION",
 "heroSteps":["Understand","Try","Verify","Build"],
 "start":"Choose your first step",
 "academy":"Explore the Academy",
 "stage":"MANZO AI / LEARNING METHOD",
 "section":"Four steps. A real capability",
 "intro":"No one-size-fits-all learning: choose a step, try an activity, and leave with something you can explain and use.",
 "cta":"Explore step",
 "steps":[
  ("Understand","A clear mental model of what AI can and cannot do","The foundation"),
  ("Experiment","Write a prompt, compare outcomes and refine your instructions","The workshop"),
  ("Verify","Test a claim against sources, limitations and uncertainty","The safeguard"),
  ("Build","Design Centroni City: from a real problem to a civic prototype","The product")
 ],
 "deckTitle":"Explore learning paths",
 "deckLead":"From your first concept to advanced workshops: published courses and lessons with exercises, sources and checks.",
 "more":"Show all",
 "less":"Show the selection",
 "unit":"paths",
 "count":"paths visible",
 "footnote":"All paths remain available in the full Academy catalogue"
},
"es":{
 "hero":"Aprende IA construyendo criterio",
 "lead":"Comprende las ideas, experimenta con método y verifica los resultados. Después construye algo útil.",
 "heroMicro":"DE LA PREGUNTA A LA SOLUCIÓN",
 "heroSteps":["Comprender","Probar","Verificar","Construir"],
 "start":"Elige por dónde empezar",
 "academy":"Explora la Academia",
 "stage":"MANZO AI / MÉTODO DE APRENDIZAJE",
 "section":"Cuatro pasos. Una capacidad real",
 "intro":"Sin recorridos genéricos: elige un paso, prueba una actividad y llévate algo que puedas explicar y utilizar.",
 "cta":"Explorar paso",
 "steps":[
  ("Comprender","Un modelo mental claro de lo que la IA puede y no puede hacer","Los fundamentos"),
  ("Experimentar","Escribe un prompt, compara resultados y mejora las instrucciones","El laboratorio"),
  ("Verificar","Contrasta una afirmación: fuentes, límites e incertidumbre","El control"),
  ("Construir","Diseña Centroni City: de un problema real al prototipo cívico","El producto")
 ],
 "deckTitle":"Explora los itinerarios",
 "deckLead":"Desde el primer concepto hasta los talleres avanzados: cursos y lecciones con ejercicios, fuentes y verificaciones.",
 "more":"Mostrar todos los",
 "less":"Mostrar la selección",
 "unit":"itinerarios",
 "count":"itinerarios visibles",
 "footnote":"Todos los itinerarios siguen disponibles en el catálogo de la Academia"
}
}
HERO=re.compile(r'<section\b[^>]*\bclass=["\'][^"\']*\bhome-hero\b[^"\']*["\'][^>]*>',re.I|re.S)
SEC=re.compile(r'</?section\b[^>]*>',re.I|re.S)
TOPIC=re.compile(r'<section\s+class="ma-topic-features"[^>]*>.*?</section\s*>',re.I|re.S)
INTENT=re.compile(r'<a\s+class="ma-discovery-choice"\s+href="([^"]+)"\s+data-ma-intent="([0-3])"',re.I)
CARD=re.compile(r'<article\b(?=[^>]*\bdata-ma-course-card=["\']1["\'])[^>]*>.*?</article\s*>',re.I|re.S)
EXTRA='data-ma-home-course='

def e(text):return escape(str(text),quote=True)

def hero_bounds(doc):
 m=HERO.search(doc)
 if not m:raise RuntimeError("Home hero missing")
 depth=1
 for token in SEC.finditer(doc,m.end()):
  depth+=-1 if token.group().startswith("</") else 1
  if depth==0:return m.start(),token.end()
 raise RuntimeError("Home hero unbalanced")

def academy(loc):
 return BASE+loc+("/academia/" if loc=="es" else "/academy/")

def centroni(loc):
 return {
  "it":BASE+"it/formazione/ai-product-builder-centroni-city/",
  "en":BASE+"en/learning/ai-product-builder-centroni-city/",
  "es":BASE+"es/formacion/ai-product-builder-centroni-city/",
 }[loc]

def links(site,loc,doc):
 pairs=INTENT.findall(doc)
 routes={int(i):href for href,i in pairs}
 if set(routes)!={0,1,2,3}:raise RuntimeError("Four actual home intentions missing: "+loc)
 destinations=[routes[0],routes[1],routes[2],centroni(loc)]
 if len(set(destinations))!=4:raise RuntimeError("Learning routes not distinct")
 for dest in destinations+[academy(loc)]:
  if not dest.startswith(BASE) or not dest.endswith("/") or not (site/dest.removeprefix(BASE)/"index.html").is_file():
   raise RuntimeError("Unpublished learning route "+dest)
 return destinations

def steps_section(loc,dests):
 d=DATA[loc];steps=[]
 for index,((title,description,meta),href) in enumerate(zip(d["steps"],dests),1):
  steps.append(
   f'<a class="ma-topic-card ma-topic-{index} ma-s1-step" href="{e(href)}" '
   f'data-ma-s1-step="{index}">'
   f'<span class="ma-topic-num">{index:02d} / 04 <small>{e(meta)}</small></span>'
   f'<strong>{e(title)}</strong><span class="ma-topic-summary">{e(description)}</span>'
   f'<span class="ma-topic-action">{e(d["cta"])} <span aria-hidden="true">↗</span></span></a>')
 return (
  '<section class="ma-topic-features ma-s1-steps" data-ma-home-featured="v1" '
  f'aria-labelledby="ma-featured-{loc}">'
  '<div class="ma-topic-heading ma-s1-steps-heading"><div>'
  f'<p class="ma-topic-eyebrow">{e(d["stage"])}</p>'
  f'<h2 id="ma-featured-{loc}">{e(d["section"])}</h2>'
  f'<p>{e(d["intro"])}</p></div>'
  f'<a class="ma-topic-all" href="{e(academy(loc))}">{e(d["academy"])} <span aria-hidden="true">↗</span></a>'
  '</div><div class="ma-topic-grid ma-s1-steps-grid">'
  +''.join(steps)+'</div></section>'
 )

def redesign(site,loc,doc,cssver,jsver):
 if MARKER in doc:raise RuntimeError("Second Sprint 1 pass on "+loc)
 if doc.count('data-ma-home-showcase="v1"')!=1:
  raise RuntimeError("Home Academy section absent: "+loc)
 if doc.count('data-ma-course-card="1"')!=6 or doc.count(EXTRA)!=7:
  raise RuntimeError("Expected 6 original + 7 published extra cards: "+loc)
 routes=links(site,loc,doc)
 d=DATA[loc]
 start,end=hero_bounds(doc)
 hero=doc[start:end]
 h1=re.search(r'(<h1\b[^>]*>).*?(</h1>)',hero,re.S|re.I)
 if not h1:raise RuntimeError("Hero heading missing")
 hero=hero[:h1.start()]+h1.group(1)+e(d["hero"])+h1.group(2)+hero[h1.end():]
 pattern=r'<p\s+class="ma-home-positioning">.*?</p\s*>'
 if len(re.findall(pattern,hero,flags=re.I|re.S))!=1:
  raise RuntimeError("Intro paragraph not unique "+loc)
 micro='<div class="ma-s1-micro" aria-label="'+e(d["heroMicro"])+'">'
 micro+='<span>'+e(d["heroMicro"])+'</span><ol>'
 micro+=''.join('<li>'+e(t)+'</li>' for t in d["heroSteps"])
 micro+='</ol></div>'
 actions='<div class="ma-s1-hero-actions"><a class="ma-s1-hero-primary" href="#ma-featured-'+loc+'">'+e(d["start"])+' <span aria-hidden="true">↘</span></a>'
 actions+='<a class="ma-s1-hero-secondary" href="'+e(academy(loc))+'">'+e(d["academy"])+' <span aria-hidden="true">↗</span></a></div>'
 hero=re.sub(pattern,lambda _:'<p class="ma-home-positioning">'+e(d["lead"])+'</p>'+actions+micro,hero,count=1,flags=re.I|re.S)
 doc=doc[:start]+hero+doc[end:]
 if len(TOPIC.findall(doc))!=1:raise RuntimeError("Topics section missing/duplicate "+loc)
 doc=TOPIC.sub(lambda _:steps_section(loc,routes),doc,count=1)
 heading=re.compile(r'(<h2\s+id="ma-home-showcase-title-'+loc+r'">).*?(</h2>)',re.I|re.S)
 if len(heading.findall(doc))!=1:raise RuntimeError("Academy home title missing")
 doc=heading.sub(lambda m:m.group(1)+e(d["deckTitle"])+m.group(2),doc,count=1)
 desc=re.compile(r'(<p\s+class="ma-home-showcase-description">).*?(</p>)',re.I|re.S)
 if len(desc.findall(doc))!=1:raise RuntimeError("Academy deck lead missing")
 doc=desc.sub(lambda m:m.group(1)+e(d["deckLead"])+m.group(2),doc,count=1)
 grid='<div class="ma-course-grid ma-home-course-grid">'
 if doc.count(grid)!=1:raise RuntimeError("Academy grid not unique "+loc)
 doc=doc.replace(grid,'<div class="ma-course-grid ma-home-course-grid" id="ma-s1-grid-'+loc+'">',1)
 footer='<div class="ma-home-showcase-footer">'
 if doc.count(footer)!=1:raise RuntimeError("Academy footer not unique "+loc)
 button=(
  '<div class="ma-s1-catalog-controller">'
  '<button type="button" class="ma-s1-catalog-toggle" hidden '
  'data-ma-s1-toggle="v1" aria-expanded="true" '
  f'aria-controls="ma-s1-grid-{loc}" '
  f'data-more="{e(d["more"])}" data-less="{e(d["less"])}" '
  f'data-unit="{e(d["unit"])}">'
  f'{e(d["more"])}</button>'
  '<p class="ma-s1-catalog-feedback" role="status" aria-live="polite" '
  f'data-ma-s1-status data-count="{e(d["count"])}"></p>'
  f'<p class="ma-s1-catalog-note">{e(d["footnote"])}</p></div>')
 doc=doc.replace(footer,button+footer,1)
 doc=doc.replace('</head>',
  f'<link {MARKER} rel="stylesheet" href="{BASE}assets/{CSS.name}?v={cssver}">'
  f'<script defer data-ma-sprint1-script="v1" src="{BASE}assets/{JS.name}?v={jsver}"></script>'
  '</head>',1)
 return doc

def check(site,cssver,jsver):
 for loc,d in DATA.items():
  page=site/loc/"index.html"
  if not page.is_file():raise RuntimeError("Home missing "+loc)
  html=page.read_text(encoding="utf-8")
  for marker in (MARKER,'data-ma-sprint1-script="v1"','data-ma-s1-toggle="v1"',
                 'data-ma-home-featured="v1"','data-ma-home-showcase="v1"',
                 f'id="ma-featured-{loc}"',f'id="ma-s1-grid-{loc}"',
                 f'{CSS.name}?v={cssver}',f'{JS.name}?v={jsver}'):
   if html.count(marker)!=1:raise RuntimeError("Missing or duplicate Sprint 1 marker "+loc+" "+marker)
  if html.count('data-ma-course-card="1"')!=6 or html.count(EXTRA)!=7:
   raise RuntimeError("Course covers altered "+loc)
  if len(re.findall(r'data-ma-s1-step="[1-4]"',html))!=4:
   raise RuntimeError("Incomplete 4 step educational method "+loc)
  if e(d["hero"]) not in html or e(d["lead"]) not in html:
   raise RuntimeError("New intro absent "+loc)
  for dest in links(site,loc,html):
   if f'href="{e(dest)}"' not in html:raise RuntimeError("Learning destination missing "+dest)
  for invariant in ('data-ma-home-primary-nav="v2"','data-ma-intent="0"',
                    'data-ma-intent="1"','data-ma-intent="2"','data-ma-intent="3"'):
   if invariant not in html:raise RuntimeError("Existing functionality lost "+invariant)
 for name in (CSS.name,JS.name):
  if not (site/"assets"/name).is_file():raise RuntimeError("Missing "+name)
 if not (site/"assets"/CSS.name).read_bytes()==CSS.read_bytes():
  raise RuntimeError("Sprint 1 visual styling mismatch")
 if not (site/"assets"/JS.name).read_bytes()==JS.read_bytes():
  raise RuntimeError("Sprint 1 interaction mismatch")
 print("PASS Sprint 1 Home: 3-language pedagogical 4-step method, course disclosure, six original + seven extra Academy cards, search and home navigation preserved. ROOT LANGUAGE MENU UNCHANGED.")

def publish(site,verify_only=False):
 if not CSS.is_file() or not JS.is_file():raise RuntimeError("Sprint 1 assets missing")
 cssver=hashlib.sha256(CSS.read_bytes()).hexdigest()[:12]
 jsver=hashlib.sha256(JS.read_bytes()).hexdigest()[:12]
 if not verify_only:
  (site/"assets").mkdir(parents=True,exist_ok=True)
  shutil.copy2(CSS,site/"assets"/CSS.name)
  shutil.copy2(JS,site/"assets"/JS.name)
  for loc in DATA:
   file=site/loc/"index.html"
   if not file.is_file():raise RuntimeError("Home missing "+loc)
   html=file.read_text(encoding="utf-8")
   file.write_text(redesign(site,loc,html,cssver,jsver),encoding="utf-8")
 check(site,cssver,jsver)

if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("--site",type=Path,required=True)
 p.add_argument("--verify-only",action="store_true")
 arg=p.parse_args()
 publish(arg.site,arg.verify_only)
