#!/usr/bin/env python3
"""Final MANZO AI SEO polish, applied after all public editorial publishers.

Uses real course metadata and approved lessons. No search-rank promises, new
pages, fake ratings, user tracking, or changes to Auth / private pages.
The generated project-site sitemap and canonical URLs remain authoritative.
"""
from __future__ import annotations

import argparse
from collections import Counter
from html import escape, unescape
from pathlib import Path
import re
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

BASE = "https://manzo8b.github.io/manzo-ai/"
SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
META = re.compile(r"<meta\b[^>]*>", re.I | re.S)
ATTR = re.compile(r'([:\w-]+)\s*=\s*(["\'])(.*?)\2', re.I | re.S)
HEAD_END = re.compile(r"</head\s*>", re.I)
TITLE = re.compile(r"(<title\b[^>]*>)(.*?)(</title\s*>)", re.I | re.S)

MAPS = {"it":"mappa-del-sito", "en":"site-map", "es":"mapa-del-sitio"}
LOCALES = {"it":"it_IT","en":"en_US","es":"es_ES"}

# Each expansion describes content already published in these exact sections.
# Never invent lesson time, qualifications, results, enrollment or user metrics.
EXTENSIONS = {
 "it": {
  "lesson": "Approfondisci i concetti con spiegazioni, esempi e attività di autoverifica nel percorso didattico di MANZO AI.",
  "method": "Scopri come organizziamo gli obiettivi formativi, controlliamo le evidenze e rendiamo espliciti i limiti dei materiali.",
  "sources": "Consulta riferimenti e documenti utilizzati per spiegazioni, esercizi e approfondimenti pubblicati nel laboratorio.",
  "lab": "Esplora esercizi e casi pratici per sviluppare capacità di analisi, confronto delle fonti e verifica.",
  "map": "Sfoglia Academy, Prompt Mastery, ricerca, pensiero critico, laboratori e risorse pubbliche.",
 },
 "en": {
  "lesson": "Explore the lesson with explanations, examples and practical self-check activities from the MANZO AI learning catalog.",
  "method": "See how the learning objectives are organized, evidence is checked and editorial limitations are made explicit.",
  "sources": "Consult the references and original sources behind the lessons, exercises and published research materials.",
  "lab": "Try practical exercises and scenarios focused on critical analysis, verification and responsible AI use.",
  "map": "Browse the Academy, Prompt Mastery, critical thinking, research, labs and public learning resources.",
  "crossword": "Review clues, compare evidence and practice evaluating claims through an original interactive learning activity.",
 },
 "es": {
  "lesson": "Profundiza con explicaciones, ejemplos y actividades de autoevaluación del catálogo educativo MANZO AI.",
  "method": "Conoce cómo organizamos objetivos educativos, revisamos evidencias y explicamos los límites de cada material.",
  "sources": "Consulta las referencias y los documentos originales que sustentan las clases, ejercicios e investigaciones.",
  "lab": "Explora actividades y casos prácticos sobre análisis crítico, contraste de fuentes y verificación.",
  "map": "Descubre la Academia, Prompt Mastery, pensamiento crítico, investigación, laboratorios y recursos públicos.",
 },
}

def attrs(tag: str) -> dict[str, str]:
    return {name.lower(): unescape(value) for name, _quote, value in ATTR.findall(tag)}

def get_tag(html: str, attr: str, key: str) -> str | None:
    for tag in META.findall(html):
        if attrs(tag).get(attr, "").lower() == key.lower():
            return tag
    return None

def get(html: str, attr: str, key: str) -> str:
    tag = get_tag(html, attr, key)
    return attrs(tag).get("content","") if tag else ""

def put(html: str, attr: str, key: str, value: str, replace: bool = False) -> str:
    tag = get_tag(html, attr, key)
    if tag and not replace:
        return html
    new = '<meta '+attr+'="'+escape(key, quote=True)+'" content="'+escape(value, quote=True)+'">'
    if tag:
        return html.replace(tag,new,1)
    m = HEAD_END.search(html)
    if m is None:
        raise RuntimeError("Missing HEAD")
    return html[:m.start()] + new + html[m.start():]

def is_noindex(html: str) -> bool:
    return "noindex" in get(html,"name","robots").lower()

def suffix_for(rel: str, lang: str) -> str | None:
    if any(part in rel for part in ("/learn/","/impara/","/aprende/")):
        return EXTENSIONS[lang]["lesson"]
    if rel.endswith("/"+MAPS[lang]+"/index.html"):
        return EXTENSIONS[lang]["map"]
    if any(part in rel for part in ("/method/", "/metodo/")):
        return EXTENSIONS[lang]["method"]
    if any(part in rel for part in ("/sources/", "/fonti/", "/fuentes/")):
        return EXTENSIONS[lang]["sources"]
    if any(part in rel for part in ("/lab/","/laboratorio/")):
        return EXTENSIONS[lang]["lab"]
    if "crossword-sources/" in rel and lang=="en":
        return EXTENSIONS[lang]["crossword"]
    return None

def squeeze(s: str, limit: int = 170) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= limit:
        return s
    return s[:limit+1].rsplit(" ", 1)[0].rstrip(" ,;:") + "."

def title_without_terminal_period(html: str, rel: str) -> str:
    # Only three preview page browser titles end in an unnecessary full stop.
    if rel not in {"it/prodotto/index.html","en/product/index.html","es/producto/index.html"}:
        return html
    def change(m: re.Match) -> str:
        body=m.group(2)
        return m.group(1)+re.sub(r"\.(\s*)$", r"\1", body)+m.group(3)
    return TITLE.sub(change,html,count=1)

def canonical_for(site:Path, path:Path) -> str:
    rel=path.parent.relative_to(site).as_posix()
    return BASE+(rel+"/" if rel!="." else "")

def polish(page:Path, site:Path) -> str:
    rel=page.relative_to(site).as_posix()
    html=title_without_terminal_period(page.read_text(encoding="utf-8"), rel)
    if is_noindex(html):
        # Auth and product preview stay noindex, with no new social indexing.
        return html
    lang=rel.split("/",1)[0] if "/" in rel else "it"
    if lang not in LOCALES:
        raise RuntimeError("Unexpected public locale: "+rel)
    original_desc=get(html,"name","description")
    if not original_desc:
        raise RuntimeError("Public page is missing description: "+rel)
    if len(original_desc)<75:
        suffix=suffix_for(rel,lang)
        if suffix is None:
            raise RuntimeError("Short description requires editorial review: "+rel)
        separator=" " if original_desc.endswith((".", "!", "?")) else ". "
        desc=squeeze(original_desc.strip()+separator+suffix)
        if len(desc)<75:
            raise RuntimeError("Description remains too short: "+rel)
        html=put(html,"name","description",desc,replace=True)
        if get(html,"property","og:description")==original_desc:
            html=put(html,"property","og:description",desc,replace=True)
        if get(html,"name","twitter:description")==original_desc:
            html=put(html,"name","twitter:description",desc,replace=True)

    desc=get(html,"name","description")
    title=TITLE.search(html)
    if not title:
        raise RuntimeError("Public HTML has no title: "+rel)
    title=unescape(re.sub(r"<[^>]*>","",title.group(2))).strip()
    canonical=canonical_for(site,page)
    if '<link rel="canonical" href="'+canonical+'">' not in html:
        # canonical generated by the authoritative existing SEO step
        raise RuntimeError("Unexpected canonical: "+rel)
    image=BASE+"og-"+lang+".png"
    if not (site/("og-"+lang+".png")).is_file():
        raise RuntimeError("Missing branded Open Graph image: "+lang)

    hub=(rel=="index.html" or rel in [l+"/index.html" for l in LOCALES]
         or rel in [l+"/"+route+"/index.html" for l,route in
                     [("it","academy"),("en","academy"),("es","academia")]]
         or rel in [l+"/"+route+"/index.html" for l,route in MAPS.items()])
    if hub and get_tag(html,"property","og:type"):
        html=put(html,"property","og:type","website",replace=True)
    else:
        html=put(html,"property","og:type","website" if hub else "article")

    tags=[
        ("property","og:site_name","MANZO AI"),
        ("property","og:title",title),
        ("property","og:description",desc),
        ("property","og:url",canonical),
        ("property","og:image",image),
        ("property","og:locale",LOCALES[lang]),
        ("name","twitter:card","summary_large_image"),
        ("name","twitter:title",get(html,"property","og:title") or title),
        ("name","twitter:description",get(html,"property","og:description") or desc),
        ("name","twitter:image",get(html,"property","og:image") or image),
    ]
    for kind,key,value in tags:
        html=put(html,kind,key,value)

    if get_tag(html,"name","theme-color"):
        html=put(html,"name","theme-color","#ffffff",replace=True)

    # Three reciprocal human-readable site maps. URLs and indexing unchanged.
    if rel in {l+"/"+route+"/index.html" for l,route in MAPS.items()}:
        for locale,route in MAPS.items():
            href=BASE+locale+"/"+route+"/"
            if not re.search(r'<link\b(?=[^>]*\bhreflang=["\']'+locale+r'["\'])',html,re.I):
                m=HEAD_END.search(html)
                html=html[:m.start()] + '<link rel="alternate" hreflang="'+locale+'" href="'+href+'">' + html[m.start():]
    return html

def run(site:Path, verify_only:bool=False) -> None:
    pages=sorted(site.rglob("index.html"))
    if len(pages)<100:
        raise RuntimeError("Unexpectedly incomplete release")
    changed=0
    indexable=0
    for page in pages:
        original=page.read_text(encoding="utf-8")
        updated=polish(page,site)
        if not is_noindex(updated):
            indexable+=1
        if updated!=original:
            if verify_only:
                raise RuntimeError("SEO polish missing: "+str(page.relative_to(site)))
            page.write_text(updated,encoding="utf-8")
            changed+=1

    xml=ET.parse(site/"sitemap.xml")
    locs=[el.text for el in xml.findall(".//"+SITEMAP_NS+"loc")]
    expected=[canonical_for(site,p) for p in pages if not is_noindex(p.read_text(encoding="utf-8"))]
    if set(locs)!=set(expected) or len(locs)!=len(expected):
        raise RuntimeError("Sitemap must match exactly the public, indexable URL inventory")
    if len(set(locs))!=len(locs):
        raise RuntimeError("Sitemap has duplicate URLs")

    titles=[]
    for page in pages:
        html=page.read_text(encoding="utf-8")
        if is_noindex(html):
            continue
        title=TITLE.search(html)
        if not title:
            raise RuntimeError("Missing SEO title")
        titles.append(unescape(title.group(2)).strip())
        if len(get(html,"name","description"))<75:
            raise RuntimeError("Short description: "+str(page))
        for kind,key in (("property","og:title"),("property","og:description"),
                         ("property","og:image"),("name","twitter:card"),
                         ("name","twitter:image"),("name","twitter:description")):
            if not get(html,kind,key):
                raise RuntimeError("Missing "+key+": "+str(page))
    if len(set(titles))!=len(titles):
        raise RuntimeError("Duplicate public page titles")
    print(f"PASS MANZO AI SEO polish: {len(pages)} pages, {indexable} public/sitemap URLs, "
          f"{len(pages)-indexable} noindex preserved, {changed} files amended, "
          f"canonical/OG/Twitter/description/lang and sitemap coverage validated; verify={verify_only}")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--site",type=Path,required=True)
    p.add_argument("--verify-only",action="store_true")
    args=p.parse_args()
    run(args.site,args.verify_only)
