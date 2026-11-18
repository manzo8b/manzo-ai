#!/usr/bin/env python3
"""Teacher-first MANZO AI home curation after the existing Academy publishers.

Remove the technical Product Lab scene, foreground actual training, introduce
an identifiable curator and a concise side navigation. Existing Academy pages,
other audiences and language gateway are preserved.
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
  "hero":"Impara a insegnare con l'IA",
  "lead":"Formazione pratica per docenti e formatori: progetta attività didattiche, scrivi prompt più efficaci e verifica le risposte con metodo.",
  "persona":"Per docenti e formatori",
  "curator":"Progetto indipendente curato da",
  "learn":"Scopri il metodo e l'autore",
  "nav":"Percorsi principali",
  "labels":("Home","Percorsi formativi","AI Teaching Lab","Prompt Engineering","Verifica le risposte","Chi cura MANZO AI"),
 },
 "en":{
  "hero":"Learn to teach with AI",
  "lead":"Practical learning for educators and trainers: design activities, write better prompts and evaluate AI-generated answers critically.",
  "persona":"For educators and trainers",
  "curator":"An independent project curated by",
  "learn":"About the project and its creator",
  "nav":"Main learning paths",
  "labels":("Home","Learning paths","AI Teaching Lab (Italian)","Prompt Engineering","Check AI answers","About MANZO AI"),
 },
 "es":{
  "hero":"Aprende a enseñar con IA",
  "lead":"Formación práctica para docentes y formadores: diseña actividades, redacta mejores prompts y verifica las respuestas de IA con criterio.",
  "persona":"Para docentes y formadores",
  "curator":"Proyecto independiente dirigido por",
  "learn":"Conoce el método y a su creador",
  "nav":"Itinerarios principales",
  "labels":("Inicio","Formación","AI Teaching Lab (italiano)","Prompt Engineering","Verificar respuestas","Quiénes somos"),
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
 # Exactly three real routes were already rendered by the first publisher.
 pairs=DISCOVERY_LINK.findall(doc)
 links={int(index):href for href,index in pairs}
 if set(links)!={0,1,2}:raise RuntimeError("Home must have exactly three learning goals "+lang)
 for href in links.values():
  if not href.startswith(BASE) or not href.endswith("/"):raise RuntimeError("Invalid learning route")
 academy=BASE+lang+("/academia/" if lang=="es" else "/academy/")
 about=BASE+lang+"/"+ABOUT[lang]+"/"
 return (BASE+lang+"/",academy,links[0],links[1],links[2],about)

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
 # Editorial remnants in the generated homepage, not a rewrite of course content.
 pairs=(
  ("Lezione Lezione","Lezione"),("Cerca Cerca","Cerca"),
  ("Lesson Lesson","Lesson"),("Search Search","Search"),
  ("Lección Lección","Lección"),("Buscar Buscar","Buscar"),
 )
 for old,new in pairs:h=h.replace(old,new)
 return h

def curated(site,lang,html):
 copy=COPY[lang]
 links=content_links(html,lang)
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
 html=html[:begin]+hero+html[end:]
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
   for invariant in (MARKER,'data-ma-home-primary-nav="v2"',
       "ma-home-curator",esc(COPY[lang]["hero"]),f'home-curation.css?v={digest}'):
    if invariant not in html:raise RuntimeError("Curation missing "+invariant+" "+lang)
   if 'data-ma-home-scene="1"' in html:raise RuntimeError("Removed technical scene is still present")
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
 print("MANZO AI homepage: teacher-first / 3 goals / curated navigation / localized portal; verified="+str(verify_only))

if __name__=="__main__":
 parser=argparse.ArgumentParser()
 parser.add_argument("--site",required=True,type=Path)
 parser.add_argument("--verify-only",action="store_true")
 args=parser.parse_args()
 run(args.site,args.verify_only)
