#!/usr/bin/env python3
"""Inclusive MANZO AI home curation after the existing Academy publishers.

Remove the technical Product Lab scene, showcase real AI learning topics for
all audiences, and introduce a concise navigation. Preserve all existing
Academy cards, creator attribution and the language gateway.
"""
from __future__ import annotations
import argparse
import hashlib
from html import escape
from pathlib import Path
import re
import shutil

ROOT=Path(__file__).resolve().parent
CSS=ROOT/"home-curation.css"
BASE="/manzo-ai/"
MARKER='data-ma-home-curation="v2"'
SCENE=re.compile(r'<aside\b(?=[^>]*\bdata-ma-home-scene=["\']1["\'])[^>]*>.*?</aside\s*>',re.I|re.S)
HERO=re.compile(r'<section\b[^>]*\bclass=["\'][^"\']*\bhome-hero\b[^"\']*["\'][^>]*>',re.I|re.S)
SECTIONS=re.compile(r'</?section\b[^>]*>',re.I|re.S)
H1=re.compile(r'(<h1\b[^>]*>)(.*?)(</h1>)',re.I|re.S)
P=re.compile(r'<p\b[^>]*>.*?</p\s*>',re.I|re.S)
DISCOVERY_LINK=re.compile(r'<a class="ma-discovery-choice" href="([^"]+)" data-ma-intent="([0-9]+)"',re.I)
ABOUT={"it":"chi-siamo","en":"about","es":"quienes-somos"}
COPY={
 "it":{
  "hero":"Esplora il mondo dell'intelligenza artificiale",
  "lead":"Dalle prime domande ai prompt, dalle allucinazioni ai progetti digitali: scopri l'IA, sperimenta e impara a valutare i risultati.",
  "persona":"Per chi è curioso, studia, lavora o insegna",
  "curator":"Un progetto indipendente curato da",
  "learn":"Scopri chi siamo",
  "nav":"Esplora MANZO AI",
  "labels":("Home","AI Academy","Prompt Engineering","Allucinazioni dell'IA","AI Teaching Lab","Chi siamo"),
  "featured":"Scegli un tema e comincia",
  "featured_lead":"Quattro porte d'ingresso concrete. Nell'Academy trovi il catalogo completo dei percorsi.",
  "featured_cards":[
   ("Le basi dell'IA","Comprendi come funzionano i modelli e cosa possono — e non possono — fare","Esplora le basi"),
   ("Prompt Engineering","Impara a scrivere istruzioni efficaci, migliorare le risposte e verificarle","Scopri i prompt"),
   ("Allucinazioni dell'IA","Riconosci informazioni inventate, controlla fonti e misura l'incertezza","Impara a verificare"),
   ("AI Teaching Lab","Dalla progettazione delle attività ai laboratori multimediali per docenti","Apri il laboratorio"),
  ],
  "academy":"Esplora tutta l'Academy",
 },
 "en":{
  "hero":"Explore the world of artificial intelligence",
  "lead":"From the basics to prompts, from hallucinations to digital projects: explore AI, experiment and learn how to evaluate results.",
  "persona":"For curious people, learners, professionals and educators",
  "curator":"An independent project curated by",
  "learn":"About the project",
  "nav":"Explore MANZO AI",
  "labels":("Home","AI Academy","Prompt Engineering","AI hallucinations","AI Teaching Lab","About"),
  "featured":"Find a topic to explore",
  "featured_lead":"Four concrete starting points. The complete learning catalog is available in the Academy.",
  "featured_cards":[
   ("AI fundamentals","Understand how models work and what they can and cannot do","Explore the basics"),
   ("Prompt Engineering","Write clearer instructions, improve responses and check their quality","Explore prompts"),
   ("AI hallucinations","Spot fabricated information, check sources and consider uncertainty","Learn to verify"),
   ("AI Teaching Lab","From lesson design to multimedia workshops for educators","Open the lab (Italian)"),
  ],
  "academy":"Explore the full Academy",
 },
 "es":{
  "hero":"Explora el mundo de la inteligencia artificial",
  "lead":"Desde los fundamentos hasta los prompts, de las alucinaciones a los proyectos digitales: descubre la IA, experimenta y aprende a evaluar resultados.",
  "persona":"Para quienes sienten curiosidad, estudian, trabajan o enseñan",
  "curator":"Proyecto independiente dirigido por",
  "learn":"Conoce el proyecto",
  "nav":"Explora MANZO AI",
  "labels":("Inicio","Academia de IA","Prompt Engineering","Alucinaciones de la IA","AI Teaching Lab","Quiénes somos"),
  "featured":"Elige un tema y empieza",
  "featured_lead":"Cuatro puntos de entrada concretos. El catálogo completo está en la Academia.",
  "featured_cards":[
   ("Fundamentos de IA","Comprende cómo funcionan los modelos y qué pueden o no pueden hacer","Explora los fundamentos"),
   ("Prompt Engineering","Aprende a formular instrucciones claras y a comprobar los resultados","Descubre los prompts"),
   ("Alucinaciones de la IA","Reconoce información inventada, comprueba fuentes y evalúa incertidumbres","Aprende a verificar"),
   ("AI Teaching Lab","Del diseño de clases a los laboratorios multimedia para docentes","Abre el laboratorio (italiano)"),
  ],
  "academy":"Explora toda la Academia",
 },
}

def esc(x):return escape(str(x),quote=True)

def hero_bounds(doc):
 m=HERO.search(doc)
 if not m:raise RuntimeError("Home hero missing")
 depth=1
 for token in SECTIONS.finditer(doc,m.end()):
  depth+= -1 if token.group().startswith("</") else 1
  if depth==0:return m.start(),token.end()
 raise RuntimeError("Unbalanced home hero")

def content_links(doc,lang):
 # Four public goal paths: foundations, prompts, hallucinations and creation.
 pairs=DISCOVERY_LINK.findall(doc)
 intents={int(index):href for href,index in pairs}
 if set(intents)!={0,1,2,3}:raise RuntimeError("Expected four real homepage topics "+lang)
 academy=BASE+lang+("/academia/" if lang=="es" else "/academy/")
 about=BASE+lang+"/"+ABOUT[lang]+"/"
 teacher=BASE+"it/formazione/ia-per-la-didattica/inizia/"
 menu=(BASE+lang+"/",academy,intents[1],intents[2],teacher,about)
 if len(set(menu))!=len(menu):raise RuntimeError("Homepage menu has duplicate destinations "+lang)
 return menu,intents

def portal_copy(root):
 # Preserve visual layout; fix multilingual title and repeated unlocalized CTAs.
 root=re.sub(r'(<title\b[^>]*>).*?(</title\s*>)',
             r'\1MANZO AI | Scegli la lingua · Choose a language · Elige idioma\2',
             root,count=1,flags=re.I|re.S)
 root=re.sub(r'(<html\b[^>]*\blang=["\'])it_IT(["\'])',r'\1it\2',root,count=1,flags=re.I)
 anchor=re.compile(r'(<a\b[^>]*\bhref=["\'](?P<href>[^"\']+)["\'][^>]*>)(?P<body>.*?)(</a\s*>)',re.I|re.S)
 labels={"it":"Esplora","en":"Explore","es":"Explorar"}
 def translate(m):
  href=m.group("href").strip().rstrip("/")
  target=None
  for locale in labels:
   if href in (BASE+locale,BASE+locale+"/index.html",
               locale,locale+"/index.html","./"+locale,"./"+locale+"/index.html"):
    target=locale
    break
  if not target:return m.group(0)
  body=re.sub(r'\bExplore\b',labels[target],m.group("body"),flags=re.I)
  return m.group(1)+body+m.group(4)
 return anchor.sub(translate,root)

def remove_old_duplicates(h):
 """Polish only rendered HOME language; original Academy and lessons untouched.

 A duplicate 'Lezione' often exists as two separate adjacent badge elements,
 rather than the literal string 'Lezione Lezione'. Only collapse adjacent
 short, repeated badges inside copied HOME article cards.
 """
 pairs=(
  ("Lezione Lezione","Lezione"),("Cerca Cerca","Cerca"),
  ("Lesson Lesson","Lesson"),("Search Search","Search"),
  ("Lección Lección","Lección"),("Buscar Buscar","Buscar"),
  ("i video didattici che selezioneremo insieme","i video didattici disponibili"),
  ("Nuovi materiali scaricabili saranno aggiunti dopo revisione.",""),
  ("Un laboratorio di conoscenza, non un chatbot","Impara, sperimenta e verifica"),
  ("Esplora lezioni, concetti ed esercizi verificati. Nessun chatbot: la ricerca mostra solo contenuti disponibili",
   "Cerca lezioni, attività e risorse disponibili"),
  ("MANZO AI · v0.6","MANZO AI"),
 )
 for old,new in pairs:h=h.replace(old,new)
 card=re.compile(r'<article\b(?=[^>]*\bdata-ma-course-card=["\x27]1["\x27])[^>]*>.*?</article\s*>',re.I|re.S)
 badge=re.compile(r'<(?P<tag>span|small|strong|b)\b(?P<attrs>[^>]*)>\s*(?P<label>Lezione|Lesson|Lección)\s*</(?P=tag)\s*>',re.I)
 def clean_card(match):
  seen=set()
  def clean_badge(m):
   key=m.group("label").casefold()
   if key in seen:return ""
   seen.add(key)
   return m.group(0)
  return badge.sub(clean_badge,match.group(0))
 return card.sub(clean_card,h)

def curated(site,lang,html):
 copy=COPY[lang]
 links,intents=content_links(html,lang)
 for link in links:
  target=site/link.removeprefix(BASE)/"index.html"
  if not target.is_file():raise RuntimeError("Unpublished destination "+link)
 if html.count('data-ma-home-scene="1"')!=1:
  raise RuntimeError("Legacy scene changed; do not silently remove unrelated content "+lang)
 html,num=SCENE.subn("",html,count=1)
 if num!=1:raise RuntimeError("Unable to remove technical scene "+lang)
 begin,end=hero_bounds(html)
 hero=html[begin:end]
 h1=H1.search(hero)
 if not h1:raise RuntimeError("Homepage headline missing "+lang)
 hero=hero[:h1.start(2)]+esc(copy["hero"])+hero[h1.end(2):]
 h1=H1.search(hero)
 first_p=P.search(hero,h1.end())
 # Replace an introductory paragraph, leaving the original search and its form intact.
 if first_p and first_p.start()<hero.find('data-ma-home-discovery="v1"'):
  hero=hero[:first_p.start()]+f'<p class="ma-home-positioning">{esc(copy["lead"])}</p>'+hero[first_p.end():]
 else:
  hero=hero[:h1.end()]+f'<p class="ma-home-positioning">{esc(copy["lead"])}</p>'+hero[h1.end():]
 persona=f'<p class="ma-home-persona">{esc(copy["persona"])}</p>'
 hero=hero.replace(h1.group(1),persona+h1.group(1),1)
 # Remove the redundant explicit "no chatbot" from the older hero paragraph.
 hero=re.sub(r'\s*Nessun chatbot:\s*la ricerca mostra solo contenuti disponibili', "",hero,flags=re.I)
 hero=re.sub(r'\s*No chatbot:\s*search only shows available content', "",hero,flags=re.I)
 if hero.count('data-ma-home-discovery="v1"')!=1:raise RuntimeError("Missing discovery block")
 labels=copy["labels"]
 nav='<nav class="ma-home-primary-nav" data-ma-home-primary-nav="v2" aria-label="'+esc(copy["nav"])+'">'
 for i,(label,href) in enumerate(zip(labels,links)):
  nav+=f'<a href="{esc(href)}"'+(' aria-current="page"' if i==0 else '')+f'>{esc(label)}</a>'
 nav+='</nav>'
 about=links[5]
 curator=(f'<div class="ma-home-curator"><span>{esc(copy["curator"])} '
          f'<strong>Marcelo Javier Fernandez Caballero</strong></span>'
          f'<a href="{esc(about)}">{esc(copy["learn"])} ↗</a></div>')
 marker='<p data-ma-discovery-live class="sr-only" role="status" aria-live="polite"></p>'
 if hero.count(marker)!=1:raise RuntimeError("Discovery live note changed")
 hero=hero.replace(marker,marker+curator+nav,1)
 featured_links=(intents[0],intents[1],intents[2],links[4])
 for href in featured_links:
  target=site/href.removeprefix(BASE)/"index.html"
  if not target.is_file():raise RuntimeError("Unpublished featured learning card "+href)
 feature_cards=[]
 for idx,((title,summary,action),href) in enumerate(zip(copy["featured_cards"],featured_links),1):
  feature_cards.append(
   f'<a class="ma-topic-card ma-topic-{idx}" href="{esc(href)}">'
   f'<span class="ma-topic-num">{idx:02d} / 04</span>'
   f'<strong>{esc(title)}</strong><span class="ma-topic-summary">{esc(summary)}</span>'
   f'<span class="ma-topic-action">{esc(action)} <span aria-hidden="true">↗</span></span></a>'
  )
 feature_section=(
  f'<section class="ma-topic-features" data-ma-home-featured="v1" aria-labelledby="ma-featured-{lang}">'
  '<div class="ma-topic-heading">'
  f'<div><p class="ma-topic-eyebrow">MANZO AI / ACADEMY</p>'
  f'<h2 id="ma-featured-{lang}">{esc(copy["featured"])}</h2>'
  f'<p>{esc(copy["featured_lead"])}</p></div>'
  f'<a class="ma-topic-all" href="{esc(links[1])}">{esc(copy["academy"])} ↗</a>'
  '</div><div class="ma-topic-grid">'+''.join(feature_cards)+'</div></section>'
 )
 html=html[:begin]+hero+feature_section+html[end:]
 html=remove_old_duplicates(html)
 if 'data-ma-home-scene="1"' in html:raise RuntimeError("Legacy technical scene survived")
 return html

def run(site,verify_only=False):
 if not CSS.is_file():raise RuntimeError("Missing curated homepage stylesheet")
 assets=site/"assets"
 digest=hashlib.sha256(CSS.read_bytes()).hexdigest()[:12]
 if not verify_only:
  assets.mkdir(parents=True,exist_ok=True)
  shutil.copyfile(CSS,assets/CSS.name)
 if not (assets/CSS.name).is_file() or (assets/CSS.name).read_bytes()!=CSS.read_bytes():
  raise RuntimeError("Curation stylesheet mismatch")
 tag=(f'<link {MARKER} rel="stylesheet" '
      f'href="{BASE}assets/home-curation.css?v={digest}">')
 for lang in COPY:
  path=site/lang/"index.html"
  if not path.is_file():raise RuntimeError("Home missing "+lang)
  html=path.read_text(encoding="utf-8")
  if verify_only:
   for invariant in (MARKER,'data-ma-home-primary-nav="v2"','data-ma-home-featured="v1"',
       "ma-home-curator",esc(COPY[lang]["hero"]),f'home-curation.css?v={digest}'):
    if invariant not in html:raise RuntimeError("Curation missing "+invariant+" "+lang)
   if 'data-ma-home-scene="1"' in html:raise RuntimeError("Removed technical scene is still present")
   # Release gates: the homepage must genuinely offer four topics while retaining
   # all six original Academy cards; neither source intent nor a CSS mock is enough.
   if html.count('data-ma-intent="')!=4:raise RuntimeError("Home should offer exactly four goals "+lang)
   if html.count('data-ma-course-card="1"')!=6:raise RuntimeError("Original six Academy cards were lost "+lang)
   featured=re.findall(r'<a class="ma-topic-card ma-topic-[1-4]" href="([^"]+)"',html)
   if len(featured)!=4 or len(set(featured))!=4:raise RuntimeError("Four distinct topic cards required "+lang)
   menu=re.search(r'<nav class="ma-home-primary-nav"[^>]*>(.*?)</nav>',html,re.S)
   if not menu:raise RuntimeError("Curated navigation is missing "+lang)
   menu_links=re.findall(r'<a href="([^"]+)"',menu.group(1))
   if len(menu_links)!=6 or len(set(menu_links))!=6:raise RuntimeError("Six unique homepage menu routes required "+lang)
   for href in featured+menu_links:
    if not href.startswith(BASE) or not href.endswith("/"):
     raise RuntimeError("Unsafe internal link "+href)
    target=site/href.removeprefix(BASE)/"index.html"
    if not target.is_file():raise RuntimeError("Broken internal homepage link "+href)
   stale=("Nuovi materiali scaricabili saranno aggiunti dopo revisione.","i video didattici che selezioneremo insieme","MANZO AI · v0.6")
   if any(s in html for s in stale):raise RuntimeError("Outdated placeholder copy on homepage "+lang)
   continue
  if MARKER in html:raise RuntimeError("Repeated home curation "+lang)
  html=curated(site,lang,html)
  head=re.search(r'</head\s*>',html,re.I)
  if not head:raise RuntimeError("Missing HTML head "+lang)
  html=html[:head.start()]+tag+html[head.start():]
  path.write_text(html,encoding="utf-8")
 portal=site/"index.html"
 if not portal.is_file():raise RuntimeError("Missing language gateway")
 html=portal.read_text(encoding="utf-8")
 if verify_only:
  if "Scegli la lingua · Choose a language · Elige idioma" not in html:
   raise RuntimeError("Multilingual language portal title missing")
 else:
  portal.write_text(portal_copy(html),encoding="utf-8")
 print("MANZO AI homepage: all audiences / 4 goals / 4 topic cards / 6 Academy cards preserved; verified="+str(verify_only))

if __name__=="__main__":
 parser=argparse.ArgumentParser()
 parser.add_argument("--site",required=True,type=Path)
 parser.add_argument("--verify-only",action="store_true")
 args=parser.parse_args()
 run(args.site,args.verify_only)
