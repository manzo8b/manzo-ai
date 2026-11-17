#!/usr/bin/env python3
"""Publish the Italian MANZO AI AI Teaching Lab within existing Pages build.
No database, auth, grades, certificates or commercial entitlements are added.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from html import escape
import json
import re
import shutil
from markdown import markdown

ROOT=Path(__file__).resolve().parent.parent
SRC=ROOT/"editorial"/"learning"/"ai-teaching-lab"
DATA=SRC/"it"
PREVIEW=SRC/"preview"
ROUTE="it/formazione/ia-per-la-didattica"
BASE="/manzo-ai/"
MARKER='data-atl-feature="2026-11"'

def e(s):return escape(str(s),quote=True)

def seo(title,desc,kind,url):
    ld={"@context":"https://schema.org","@type":kind,"name":title,
        "description":desc,"inLanguage":"it",
        "url":"https://manzo8b.github.io"+url,
        "provider":{"@type":"Organization","name":"MANZO AI"}}
    if kind=="Course":
        ld["timeRequired"]="PT20H"
        ld["educationalLevel"]="Formazione docenti"
    return ('<meta name="description" content="'+e(desc)+'">'
            '<meta name="robots" content="index,follow">'
            '<meta property="og:title" content="'+e(title)+'">'
            '<meta property="og:description" content="'+e(desc)+'">'
            '<meta name="twitter:card" content="summary">'
            '<meta name="twitter:title" content="'+e(title)+'">'
            '<meta name="twitter:description" content="'+e(desc)+'">'
            '<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False).replace("<","\\u003c")+'</script>')

def lesson_page(i,m,course,text):
    if re.search(r'<\s*(?:script|iframe|style)\b|javascript:',text,re.I):
        raise RuntimeError("Unsafe raw HTML or link in lesson source")
    lines=text.splitlines()
    if not lines or not lines[0].startswith("# "):raise RuntimeError("Lesson lacks source heading")
    # The page supplies the only H1, so remove the source-level H1.
    html=markdown("\n".join(lines[1:]),extensions=["tables","fenced_code","sane_lists","toc"])
    html=html.replace("Non pubblicato","Materiale formativo aperto, non accreditato")
    html=html.replace("né pubblicazione web","e pubblicato come materiale aperto")
    title=m["title"].rstrip(".")
    url=BASE+ROUTE+"/modulo-%02d/"%i
    desc="AI Teaching Lab: teoria documentata, metodo MANZO AI, laboratori autentici, verifiche, fonti e guida per il docente."
    siblings="".join(f'<a href="{BASE}{ROUTE}/modulo-{j:02d}/" '+('aria-current="page"' if i==j else '')+'>'+f"{j:02d} · "+e(course["modules"][j-1]["title"])+'</a>' for j in range(1,6))
    next_url=(BASE+ROUTE+"/modulo-%02d/"%(i+1)) if i<5 else BASE+ROUTE+"/"
    next_label="Modulo successivo" if i<5 else "Torna al percorso"
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} · AI Teaching Lab | MANZO AI</title>
{seo(title+" · AI Teaching Lab | MANZO AI",desc,"LearningResource",url)}
<link rel="stylesheet" href="../assets.css"><link rel="stylesheet" href="../lesson.css"></head>
<body class="atl-lesson"><a class="skip-link" href="#contenuto">Vai alla lezione</a>
<header class="site-head"><div class="wrap head-inner"><a class="brand" href="{BASE}it/">
<img class="brand-icon" src="{BASE}assets/manzo-mark.svg" width="38" height="38" alt=""><span>MANZO <b>AI</b></span></a>
<a href="{BASE}{ROUTE}/">Tutti i moduli</a></div></header>
<main id="contenuto" class="wrap atl-lesson-wrap">
<div class="atl-lesson-hero"><span class="eyebrow">AI TEACHING LAB / MODULO {i:02d} DI 05</span>
<h1>{e(title)}</h1><p>{e(m["question"])}</p><div class="atl-lesson-facts">
<span>4 ore progettate</span><span>2 laboratori</span><span>Metodo MANZO AI</span></div></div>
<div class="atl-learn-shell"><aside class="atl-side-index" aria-label="Indice del corso">
<strong>Programma</strong><nav aria-label="Altri moduli">{siblings}</nav>
<p>Accesso aperto in italiano. Nessuna iscrizione o certificazione richiesta.</p></aside>
<article class="atl-reading" aria-label="Testo integrale">
<p class="atl-alert">Materiale formativo aperto e non accreditato. Le attività simulano casi e dati: non usare informazioni personali di studenti. Le 20 ore sono una stima da validare.</p>
{html}
<nav class="atl-bottom-nav" aria-label="Continua il percorso">
<a href="{BASE}{ROUTE}/">Laboratori interattivi</a>
<a class="atl-next" href="{next_url}">{next_label} <span aria-hidden="true">→</span></a>
</nav></article></div></main><footer class="footer"><div class="wrap">
<strong>MANZO AI · AI Teaching Lab</strong><p>Progettazione e verifica professionale con supervisione umana</p>
</div></footer></body></html>'''

def feature(site,verify=False):
    titles={
    "it":("FORMAZIONE DOCENTI · NUOVO","AI Teaching Lab","Cinque moduli, teoria documentata, decisioni ramificate e laboratori. Corso disponibile in italiano.","Scopri il laboratorio"),
    "en":("TEACHER TRAINING · IN ITALIAN","AI Teaching Lab","Five modules and classroom decision simulations, currently available in Italian.","View Italian course"),
    "es":("FORMACIÓN DOCENTE · EN ITALIANO","AI Teaching Lab","Cinco módulos y simulaciones de decisiones, disponibles actualmente en italiano.","Ver curso en italiano")}
    for loc,(k,title,desc,cta) in titles.items():
        academy="academia" if loc=="es" else "academy"
        page=site/loc/academy/"index.html"
        if not page.is_file():raise RuntimeError("Missing Academy "+str(page))
        doc=page.read_text(encoding="utf-8")
        if verify:
            if doc.count(MARKER)!=1:raise RuntimeError("Academy course feature missing "+loc)
            continue
        if MARKER in doc:raise RuntimeError("Duplicate Academy feature "+loc)
        block=f'''<section {MARKER} class="atl-academy-feature" aria-label="AI Teaching Lab">
<div class="atl-feature-art" aria-hidden="true"><span>MANZO AI / EDUCATION</span>
<strong>AI<br>TEACHING<br>LAB</strong><i></i></div>
<div class="atl-feature-copy"><span class="atl-feature-eyebrow">{e(k)}</span><h2>{e(title)}</h2>
<p>{e(desc)}</p><div class="atl-feature-chips"><span>05 MODULES</span><span>10 LABS</span><span>IT</span></div>
<a class="atl-feature-cta" href="{BASE}{ROUTE}/">{e(cta)} <span aria-hidden="true">↗</span></a></div></section>'''
        main=re.search(r"<main\b[^>]*>",doc,re.I)
        head=re.search(r"</head\s*>",doc,re.I)
        if not main or not head:raise RuntimeError("Missing Academy main/head")
        doc=doc[:main.end()]+block+doc[main.end():]
        head=re.search(r"</head\s*>",doc,re.I)
        doc=doc[:head.start()]+f'<link rel="stylesheet" href="{BASE}{ROUTE}/feature.css" data-atl-asset="1">'+doc[head.start():]
        page.write_text(doc,encoding="utf-8")

def publish(site,verify=False):
    target=site/ROUTE
    course=json.loads((DATA/"course.json").read_text(encoding="utf-8"))
    scenes=json.loads((DATA/"scenarios.json").read_text(encoding="utf-8"))
    assessments=json.loads((DATA/"assessment-bank.json").read_text(encoding="utf-8"))
    if len(course["modules"])!=5 or len(scenes["modules"])!=5 or len(assessments["modules"])!=5:raise RuntimeError("Course incomplete")
    for name in ["course.json","assessment-bank.json","scenarios.json"]:
        dst=target/"data"/name
        if not verify:
            dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(DATA/name,dst)
        if not dst.is_file() or dst.read_bytes()!=(DATA/name).read_bytes():raise RuntimeError("Data mismatch "+name)
    if not verify:
        target.mkdir(parents=True,exist_ok=True)
        for name in ["assets.css","app.js","lesson.css","feature.css"]:
            shutil.copyfile(PREVIEW/name,target/name)
        home=(PREVIEW/"index.html").read_text(encoding="utf-8")
        home=home.replace('<meta name="robots" content="noindex,nofollow">',"")
        home=home.replace("<title>AI Teaching Lab · Anteprima MANZO AI</title>",
            "<title>AI Teaching Lab — Formazione docenti | MANZO AI</title>"+
            seo("AI Teaching Lab — Formazione docenti | MANZO AI",
                "Corso aperto per docenti: cinque moduli, casi attuali, teoria pedagogica e simulazioni decisionali.",
                "Course",BASE+ROUTE+"/"))
        home=home.replace("<body>",'<body data-course-data-base="./data/" data-module-base="./modulo-">')
        home=home.replace('ANTEPRIMA DIDATTICA · NON PUBBLICATA','FORMAZIONE DOCENTI · ACCESSO APERTO')
        home=home.replace("Questo è un prototipo editoriale isolato: non salva risposte, non prevede login, non valuta studenti reali e non rilascia attestati. La durata non è stata ancora validata con un gruppo pilota.",
            "Corso aperto in italiano, non accreditato. Le risposte restano solo nel browser: nessun account, dato personale o certificato. Le 20 ore sono stimate e saranno validate con docenti.")
        home=home.replace('<span class="brand-symbol" aria-hidden="true">M</span>',
            '<img class="brand-icon" src="/manzo-ai/assets/manzo-mark.svg" width="38" height="38" alt="">')
        (target/"index.html").write_text(home,encoding="utf-8")
        for i,m in enumerate(course["modules"],1):
            text=(DATA/f"module-{i:02d}.md").read_text(encoding="utf-8")
            dest=target/f"modulo-{i:02d}"/"index.html"
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_text(lesson_page(i,m,course,text),encoding="utf-8")
    for i in range(1,6):
        page=target/f"modulo-{i:02d}"/"index.html"
        if not page.is_file():raise RuntimeError("Missing module "+str(page))
        html=page.read_text(encoding="utf-8")
        if html.count("<h1")!=1 or "Metodo MANZO AI" not in html or "Laboratorio" not in html:raise RuntimeError("Semantic module missing")
        if 'content="noindex' in html or 'Non pubblicato' in html:raise RuntimeError("Incorrect public lesson status")
    for asset in ["index.html","app.js","assets.css","lesson.css","feature.css"]:
        if not (target/asset).is_file():raise RuntimeError("Missing asset "+asset)
    home=(target/"index.html").read_text(encoding="utf-8")
    if 'data-course-data-base="./data/"' not in home or 'content="noindex' in home:raise RuntimeError("Home not public")
    feature(site,verify)
    print("PASS AI Teaching Lab publisher: 5 complete lessons, public course, 3 Academy features, verified="+str(verify))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--site",type=Path,required=True)
    ap.add_argument("--verify-only",action="store_true")
    a=ap.parse_args()
    publish(a.site,a.verify_only)
