#!/usr/bin/env python3
"""Publish the Italian MANZO AI AI Teaching Lab within existing Pages build.
No database, auth, grades, certificates or commercial entitlements are added.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import json
import re
import shutil
from zipfile import ZipFile
from markdown import markdown

ROOT=Path(__file__).resolve().parent.parent
SRC=ROOT/"editorial"/"learning"/"ai-teaching-lab"
DATA=SRC/"it"
PREVIEW=SRC/"preview"
MEDIA=SRC/"media"
IMAGE_STUDIO=ROOT/"tools"/"ai-teaching-image-studio"/"index.html"
VOICE_STUDIO=ROOT/"tools"/"ai-teaching-voice-studio"/"index.html"
VIDEO_STUDIO=ROOT/"tools"/"ai-teaching-video-studio"/"index.html"
MULTIMEDIA_WORKSPACE=ROOT/"tools"/"ai-teaching-workspace"/"index.html"
LAUNCHPAD=ROOT/"tools"/"ai-teaching-launchpad"/"index.html"
ROUTE="it/formazione/ia-per-la-didattica"
BASE="/manzo-ai/"
MARKER='data-atl-feature="2026-11"'

def e(s):return escape(str(s),quote=True)

def accessible_studio(html,tool):
    """Attach the shared, scoped tool styles and an activity skip link."""
    class Landmarks(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=False)
            self.positions={"head":[],"body":[],"main":[]}
            self.lines=html.splitlines(keepends=True)
        def absolute_offset(self):
            line,column=self.getpos()
            return sum(map(len,self.lines[:line-1]))+column
        def handle_starttag(self,tag,attrs):
            if tag in ("body","main"):
                self.positions[tag].append((self.absolute_offset(),self.get_starttag_text(),dict(attrs)))
        def handle_endtag(self,tag):
            if tag=="head":self.positions[tag].append((self.absolute_offset(),"</head>",{}))
    landmarks=Landmarks()
    landmarks.feed(html)
    if any(len(landmarks.positions[tag])!=1 for tag in ("head","body","main")):
        raise RuntimeError("Unexpected standalone studio structure: "+tool)
    head_at,_,_=landmarks.positions["head"][0]
    body_at,body_tag,_=landmarks.positions["body"][0]
    main_at,main_tag,main_attrs=landmarks.positions["main"][0]
    target=main_attrs.get("id") or "atl-studio-main"
    if not main_attrs.get("id"):main_tag=main_tag[:-1]+' id="'+target+'">'
    if "tabindex" not in main_attrs:main_tag=main_tag[:-1]+' tabindex="-1">'
    body_tag=body_tag[:-1]+' data-atl-tool="'+e(tool)+'">'
    body_tag+='<a class="atl-studio-skip" href="#'+e(target)+'">Vai all’attività</a>'
    replacements=[(head_at,0,'<link rel="stylesheet" href="../studio-accessibility.css">'),
                  (body_at,len(landmarks.positions["body"][0][1]),body_tag),
                  (main_at,len(landmarks.positions["main"][0][1]),main_tag)]
    for start,length,replacement in sorted(replacements,reverse=True):
        html=html[:start]+replacement+html[start+length:]
    return html

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
<a class="atl-side-glossary-link" href="{BASE}{ROUTE}/glossario/">Vocabolario IA e didattica</a>
<p>Accesso aperto in italiano. Nessuna iscrizione o certificazione richiesta.</p></aside>
<article class="atl-reading" aria-label="Testo integrale">
<p class="atl-alert">Materiale formativo aperto e non accreditato. Le attività simulano casi e dati: non usare informazioni personali di studenti. Le 20 ore sono una stima da validare.</p>
{html}
<nav class="atl-bottom-nav" aria-label="Continua il percorso">
<a href="{BASE}{ROUTE}/">Laboratori interattivi</a>
<a href="{BASE}{ROUTE}/glossario/">Consulta il vocabolario</a>
<a class="atl-next" href="{next_url}">{next_label} <span aria-hidden="true">→</span></a>
</nav></article></div></main><footer class="footer"><div class="wrap">
<strong>MANZO AI · AI Teaching Lab</strong><p>Progettazione e verifica professionale con supervisione umana</p>
</div></footer></body></html>'''


def glossary_page(g):
    """Static, indexable and keyboard-readable vocabulary for independent teachers."""
    title="Vocabolario IA e didattica applicata per docenti"
    url=BASE+ROUTE+"/glossario/"
    meta=seo(title+" | MANZO AI",
             "Le parole fondamentali della didattica e dell'intelligenza artificiale spiegate con esempi scolastici, da pedagogia e metodo a prompt e privacy.",
             "DefinedTermSet",url)
    chunks=[]
    for category in g["categories"]:
        items=[x for x in g["entries"] if x["category"]==category]
        blocks=[]
        for item in items:
            refs=('<a href="'+e(item["source"])+'" rel="noopener noreferrer" target="_blank">Fonte di approfondimento</a>'
                  if item.get("source") else "")
            blocks.append('<article class="term-card" id="'+e(item["id"])+'">'
              '<div class="term-group">'+e(category)+'</div>'
              '<h3>'+e(item["term"])+'</h3>'
              '<p>'+e(item["definition"])+'</p>'
              '<div class="term-example"><b>Nella pratica scolastica</b><p>'+e(item["classroom_example"])+'</p></div>'
              +refs+'</article>')
        chunks.append('<section class="glossary-category" aria-label="'+e(category)+'">'
          '<h2>'+e(category)+'</h2><div class="glossary-results">'+''.join(blocks)+'</div></section>')
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | MANZO AI</title>{meta}
<link rel="stylesheet" href="../assets.css"><link rel="stylesheet" href="../lesson.css">
</head><body><a class="skip-link" href="#contenuto">Vai al vocabolario</a>
<header class="site-head"><div class="wrap head-inner"><a class="brand" href="{BASE}it/">
<img class="brand-icon" src="{BASE}assets/manzo-mark.svg" alt="" width="38" height="38"><span>MANZO <b>AI</b></span></a>
<a href="{BASE}{ROUTE}/">Torna al corso</a></div></header>
<main id="contenuto" class="wrap final-glossary">
<div class="glossary-banner"><span class="eyebrow">AI TEACHING LAB / RIFERIMENTO FINALE</span>
<h1>{e(title)}</h1>
<p>{e(g["subtitle"])}. Differenze, significati ed esempi per orientarsi nella professione.</p>
<a class="glossary-page-link" href="{BASE}{ROUTE}/">Riprendi la formazione</a></div>
<p class="glossary-standalone-intro">Questo vocabolario è una risorsa didattica, non un dizionario normativo. Le definizioni semplificano termini professionali e illustrano un uso concreto. Il metodo MANZO AI è una proposta progettuale interna, non un metodo pedagogico validato sperimentalmente.</p>
{''.join(chunks)}
<section class="glossary-refs"><h2>Fonti per approfondire</h2><ul>
{''.join('<li><a href="'+e(x["url"])+'" target="_blank" rel="noopener noreferrer">'+e(x["title"])+'</a></li>' for x in g["sources"])}
</ul></section></main><footer class="footer"><div class="wrap"><b>MANZO AI · AI Teaching Lab</b>
<p>Approccio centrato sul docente e sull'apprendimento, con verifica umana dei materiali generati</p></div></footer>
</body></html>'''

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
    narrative=json.loads((DATA/"narrative.json").read_text(encoding="utf-8"))
    glossary=json.loads((DATA/"glossary.json").read_text(encoding="utf-8"))
    if len(course["modules"])!=5 or len(scenes["modules"])!=5 or len(assessments["modules"])!=5 or len(narrative["modules"])!=5:raise RuntimeError("Course incomplete")
    if [m["id"] for m in course["modules"]] != [m["id"] for m in narrative["modules"]]:raise RuntimeError("Narrative module order mismatch")
    if len(glossary["entries"])<40:raise RuntimeError("Teacher glossary incomplete")
    for name in ["course.json","assessment-bank.json","scenarios.json","narrative.json","glossary.json","presentation.json"]:
        dst=target/"data"/name
        if name=="course.json":
            public_course=dict(course)
            public_course["published"]=True
            public_course["status"]="public_beta"
            public_course["publication_status"]="open_educational_beta"
            public_course["public_access_free"]=True
            public_course["locale_coverage"]=dict(course["locale_coverage"],it="public_beta")
            expected=(json.dumps(public_course,ensure_ascii=False,indent=2)+chr(10)).encode("utf-8")
        else:
            expected=(DATA/name).read_bytes()
        if not verify:
            dst.parent.mkdir(parents=True,exist_ok=True)
            dst.write_bytes(expected)
        if not dst.is_file() or dst.read_bytes()!=expected:raise RuntimeError("Data mismatch "+name)
    if not verify:
        target.mkdir(parents=True,exist_ok=True)
        for name in ["assets.css","app.js","lesson.css","feature.css","presentation.css","presentation.js","production-studio.css","production-studio.js","studio-accessibility.css"]:
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
            "Corso aperto in italiano, non accreditato. Le verifiche sono locali al browser; non serve un account, non si salvano progressi né si rilasciano attestati. Le 20 ore sono stimate e saranno validate con docenti.")
        home=home.replace('<span class="brand-symbol" aria-hidden="true">M</span>',
            '<img class="brand-icon" src="/manzo-ai/assets/manzo-mark.svg" width="38" height="38" alt="">')
        # Media are optional: never publish dead links while the binary originals
        # have not yet been added to the repository.
        media_paths=("AI_per_Docenti.web.mp4","IA_e_Progettazione_Didattica.pdf","IA_e_Progettazione_Didattica.pptx")
        media_available={}
        for name in media_paths:
            src=MEDIA/name
            if src.is_file():
                (target/"media").mkdir(parents=True,exist_ok=True)
                shutil.copyfile(src,target/"media"/name)
                media_available[name]=True
        # A single small ZIP stores unaltered slide artwork and the original podcast video.
        bundle=MEDIA/"AI_Teaching_Lab_Originali_Per_GitHub_e_Anteprima.zip"
        expected_slides=[f"slide-{i:02d}.webp" for i in range(1,16)]
        authentic_slides=False
        if bundle.is_file():
            with ZipFile(bundle) as z:
                if not set(expected_slides+["AI_per_Docenti.web.mp4"]).issubset(z.namelist()):
                    raise RuntimeError("Incomplete original slide/video bundle")
                if not verify:
                    (target/"media"/"slides").mkdir(parents=True,exist_ok=True)
                    for filename in expected_slides:
                        (target/"media"/"slides"/filename).write_bytes(z.read(filename))
                    (target/"media"/"AI_per_Docenti.web.mp4").write_bytes(z.read("AI_per_Docenti.web.mp4"))
                authentic_slides=True
                media_available["AI_per_Docenti.web.mp4"]=True
        if media_available.get("AI_per_Docenti.web.mp4"):
            home=home.replace('<span class="atl-intro-duration">Video non caricato</span>','<span class="atl-intro-duration">Video disponibile</span>',1)
            home=re.sub(r'<div data-atl-video-media>.*?</div>',
                '<div data-atl-video-media><video class="atl-intro-video-player" controls preload="metadata" playsinline aria-label="Video podcast AI per docenti">'
                '<source src="./media/AI_per_Docenti.web.mp4" type="video/mp4">Il browser non supporta il video HTML5</video>'
                '<p class="atl-intro-video-a11y">Video con elementi grafici: consulta la presentazione web per una sintesi testuale. Non sono ancora disponibili sottotitoli verificati.</p></div>',
                home, count=1,flags=re.S)
        available_docs=[(n,label) for n,label in [
            ("IA_e_Progettazione_Didattica.pdf","Apri PDF originale"),
            ("IA_e_Progettazione_Didattica.pptx","Scarica PowerPoint originale")
        ] if media_available.get(n)]
        if available_docs:
            links='<div data-atl-deck-downloads class="atl-intro-media-downloads">'+''.join(
                '<a href="./media/'+n+'" download>'+label+' ↗</a>' for n,label in available_docs
            )+'</div>'
            home=re.sub(r'<div data-atl-deck-downloads>.*?</div>',links,home,count=1,flags=re.S)
        entry='<a href="./studio-immagini/" data-atl-image-studio="v0.1" style="display:inline-flex;margin:12px 0 0;padding:12px 18px;border-radius:14px;background:#205beb;color:white;font-weight:750;text-decoration:none">Apri lo Studio immagini · progettazione e verifica ↗</a>'
        anchor='<a class="studio-entry-action" href="./laboratorio-multimediale/">'
        if home.count(anchor)!=1:raise RuntimeError("Image Studio landing anchor missing or repeated")
        home=home.replace(anchor,entry+"\\n"+anchor,1)
        voice_entry='<a href="./studio-voce/" data-atl-voice-studio="v0.1" style="display:inline-flex;margin:12px 0 0 10px;padding:12px 18px;border-radius:14px;background:#174c7b;color:white;font-weight:750;text-decoration:none">Apri lo Studio voce · registrazione e verifica ↗</a>'
        if home.count('data-atl-image-studio="v0.1"')!=1:raise RuntimeError("Missing image studio link before voice insertion")
        home=home.replace(entry,entry+voice_entry,1)
        video_entry='<a href="./studio-video/" data-atl-video-studio="v0.1" style="display:inline-flex;margin:12px 0 0 10px;padding:12px 18px;border-radius:14px;background:#6048b9;color:white;font-weight:750;text-decoration:none">Apri lo Studio video · storyboard e verifica ↗</a>'
        home=home.replace(voice_entry,voice_entry+video_entry,1)
        workspace_entry='<a href="./workspace-multimediale/" data-atl-workspace="v0.1" style="display:inline-flex;margin:12px 0 0 10px;padding:12px 18px;border-radius:14px;background:#1b6559;color:white;font-weight:750;text-decoration:none">Apri il Workspace · unisci i tre studi ↗</a>'
        home=home.replace(video_entry,video_entry+workspace_entry,1)
        # An actionable micro-app above the course catalogue, not a fake AI chatbot.
        launch_entry=('<a href="./inizia/" data-atl-launchpad="v0.1" '
            'style="display:inline-flex;align-items:center;gap:10px;margin:10px 0 16px;'
            'padding:13px 19px;background:#111827;color:#fff;border:2px solid #111827;'
            'border-radius:15px;text-decoration:none;font-weight:850;'
            'box-shadow:0 9px 24px #12224324">'
            '✦ Avvia Mission Studio · progetta una microlezione ↗</a>')
        if home.count('<div class="hero-stat"')!=1:
            raise RuntimeError("Missing landing hero insertion point for Mission Studio")
        home=home.replace('<div class="hero-stat"',launch_entry+'<div class="hero-stat"',1)
        (target/"index.html").write_text(home,encoding="utf-8")
        presentation=(PREVIEW/"presentazione"/"index.html").read_text(encoding="utf-8")
        presentation=presentation.replace('<meta name="robots" content="noindex,nofollow">',"")
        presentation=presentation.replace(
            '<title>Presentazione del corso · IA e didattica applicata | MANZO AI</title>',
            '<title>Presentazione del corso · IA e didattica applicata | MANZO AI</title>'+
            seo("Presentazione del corso · IA e didattica applicata | MANZO AI",
                "Quindici slide didattiche sulla progettazione con l'intelligenza artificiale, in una versione web accessibile.",
                "LearningResource",BASE+ROUTE+"/presentazione/"))
        presentation=presentation.replace('data-slides-base="../../it/"','data-slides-base="../data/"')
        if authentic_slides:
            presentation=presentation.replace('data-slides-base="../data/"',
                'data-slides-base="../data/" data-original-slide-base="../media/slides/"')
            presentation=presentation.replace(
               "15 slide · versione web testuale e accessibile dei materiali originali, con possibilità di consultare ogni passaggio.",
               "15 slide originali realizzate con NotebookLM, preservate come immagini e accompagnate da un approfondimento testuale accessibile.")
            presentation=presentation.replace(
                "Le grafiche originali sono state realizzate in una presentazione illustrata. Qui il loro significato è proposto in formato testuale per una lettura più accessibile.",
                "Queste sono le immagini originali delle slide di NotebookLM. L'approfondimento testuale è una risorsa distinta.")
            home=home.replace("I file originali PDF e PowerPoint saranno scaricabili qui appena ospitati sul sito.",
               "Le 15 slide originali sono nel lettore. Le versioni PDF e PowerPoint potranno essere aggiunte separatamente.")
            (target/"index.html").write_text(home,encoding="utf-8")
        if available_docs:
            links='<div class="atl-present-files" data-atl-slide-files><strong>Materiali originali</strong>'+''.join(
               '<a href="../media/'+n+'" download>'+label+' ↗</a>' for n,label in available_docs
            )+'</div>'
            presentation=re.sub(r'<div class="atl-present-files" data-atl-slide-files>.*?</div>',
                                links,presentation,count=1,flags=re.S)
        slidepath=target/"presentazione"/"index.html"
        slidepath.parent.mkdir(parents=True,exist_ok=True)
        slidepath.write_text(presentation,encoding="utf-8")
        # Authoring studio is a separate, public, standalone learning activity:
        # all project data and media stay on the user's device until export.
        studio_source=PREVIEW/"laboratorio-multimediale"/"index.html"
        studio_html=studio_source.read_text(encoding="utf-8")
        studio_html=studio_html.replace('<meta name="robots" content="noindex,nofollow">',"")
        studio_title="Laboratorio di produzione multimediale · AI Teaching Lab | MANZO AI"
        original_studio_title="<title>Studio multimediale · AI Teaching Lab | MANZO AI</title>"
        if original_studio_title not in studio_html:
            raise RuntimeError("Production studio title changed; check SEO injection")
        studio_html=studio_html.replace(
            original_studio_title,
            "<title>"+studio_title+"</title>"+
            seo(studio_title,
                "Studio didattico autonomo per progettare, verificare ed esportare slide, script audio e attività interattive.",
                "LearningResource",BASE+ROUTE+"/laboratorio-multimediale/"))
        if '<meta name="description"' not in studio_html:
            raise RuntimeError("Production studio is missing a description")
        studio_path=target/"laboratorio-multimediale"/"index.html"
        studio_path.parent.mkdir(parents=True,exist_ok=True)
        if studio_html.count("</body>")!=1:raise RuntimeError("Unexpected production studio body")
        studio_html=studio_html.replace("</body>",'<div style="max-width:1100px;margin:1rem auto 2rem;padding:1.25rem;border:1px solid #cbd9f0;border-radius:20px;background:#f1f6ff;color:#193454"><strong>Studio immagini · nuovo laboratorio dedicato</strong><p>Progetta l’immagine, prepara il prompt, importa il risultato e verifica il materiale prima dell’approvazione docente. La generazione IA rimane esterna.</p><a href="../studio-immagini/" style="display:inline-block;padding:.8rem 1rem;border-radius:11px;background:#205beb;color:#fff;font-weight:700">Apri Studio immagini ↗</a></div></body>',1)
        studio_html=studio_html.replace("</body>",'<div style="max-width:1100px;margin:1rem auto 2rem;padding:1.25rem;border:1px solid #cbd9f0;border-radius:20px;background:#f1f6ff;color:#193454"><strong>Studio voce · narrazione didattica</strong><p>Scrivi il copione, registra dal microfono o importa una voce esterna, controlla la trascrizione e approva il materiale. Nessuna voce IA integrata.</p><a href="../studio-voce/" style="display:inline-block;padding:.8rem 1rem;border-radius:11px;background:#174c7b;color:#fff;font-weight:700">Apri Studio voce ↗</a></div></body>',1)
        studio_html=studio_html.replace("</body>",'<div style="max-width:1100px;margin:1rem auto 2rem;padding:1.25rem;border:1px solid #cbd9f0;border-radius:20px;background:#f1f6ff;color:#193454"><strong>Studio video · storyboard didattico</strong><p>Progetta scene, prepara l’anteprima, esporta un video locale silenzioso dove supportato, aggiungi sottotitoli e approva il progetto. La generazione IA resta esterna.</p><a href="../studio-video/" style="display:inline-block;padding:.8rem 1rem;border-radius:11px;background:#6048b9;color:#fff;font-weight:700">Apri Studio video ↗</a></div></body>',1)
        studio_html=studio_html.replace("</body>",'<div style="max-width:1100px;margin:1rem auto 2rem;padding:1.25rem;border:1px solid #cbd9f0;border-radius:20px;background:#f1f6ff;color:#193454"><strong>Workspace multimediale · collega i tre studi</strong><p>Importa le schede di immagini, voce e video, verifica la coerenza pedagogica e prepara un manifest locale di consegna. Nessuna approvazione automatica.</p><a href="../workspace-multimediale/" style="display:inline-block;padding:.8rem 1rem;border-radius:11px;background:#1b6559;color:#fff;font-weight:700">Apri Workspace ↗</a></div></body>',1)
        studio_path.write_text(studio_html,encoding="utf-8")
        if not IMAGE_STUDIO.is_file():raise RuntimeError("Missing standalone image studio source")
        image_html=IMAGE_STUDIO.read_text(encoding="utf-8")
        if image_html.count("</header>")!=1:raise RuntimeError("Unexpected image studio header")
        image_html=image_html.replace("</header>",'<a href="../laboratorio-multimediale/" style="display:inline-block;margin-top:12px;font-weight:700">← Torna al laboratorio multimediale</a></header>',1)
        image_html=image_html.replace('<meta name="theme-color" content="#ffffff">','<meta name="theme-color" content="#ffffff">'+seo("Studio immagini didattiche | AI Teaching Lab | MANZO AI","Progetta immagini formative, prepara prompt e verifica la qualità prima della decisione docente.","LearningResource",BASE+ROUTE+"/studio-immagini/"),1)
        image_dest=target/"studio-immagini"/"index.html"
        image_dest.parent.mkdir(parents=True,exist_ok=True)
        image_dest.write_text(accessible_studio(image_html,"image"),encoding="utf-8")
        if not VOICE_STUDIO.is_file():raise RuntimeError("Missing standalone voice studio source")
        voice_html=VOICE_STUDIO.read_text(encoding="utf-8")
        if '<meta name="robots" content="noindex,follow">' not in voice_html:
            raise RuntimeError("Voice studio prototype status not declared")
        voice_html=voice_html.replace('<meta name="robots" content="noindex,follow">',seo("Studio voce didattica | AI Teaching Lab | MANZO AI","Copione, registrazione locale, importazione, trascrizione e verifica della voce sotto controllo del docente.","LearningResource",BASE+ROUTE+"/studio-voce/"),1)
        voice_dest=target/"studio-voce"/"index.html"
        voice_dest.parent.mkdir(parents=True,exist_ok=True)
        voice_dest.write_text(accessible_studio(voice_html,"voice"),encoding="utf-8")
        if not VIDEO_STUDIO.is_file():raise RuntimeError("Missing standalone video studio source")
        video_html=VIDEO_STUDIO.read_text(encoding="utf-8")
        if '<meta name="robots" content="noindex,follow">' not in video_html:raise RuntimeError("Video studio prototype status missing")
        video_html=video_html.replace('<meta name="robots" content="noindex,follow">',seo("Studio video didattico | AI Teaching Lab | MANZO AI","Storyboard educativo, anteprima sequenziale, video silenzioso locale, sottotitoli e approvazione docente.","LearningResource",BASE+ROUTE+"/studio-video/"),1)
        video_dest=target/"studio-video"/"index.html"
        video_dest.parent.mkdir(parents=True,exist_ok=True)
        video_dest.write_text(accessible_studio(video_html,"video"),encoding="utf-8")
        if not MULTIMEDIA_WORKSPACE.is_file():raise RuntimeError("Missing multimedia workspace source")
        workspace_html=MULTIMEDIA_WORKSPACE.read_text(encoding="utf-8")
        if '<meta name="robots" content="noindex,follow">' not in workspace_html:
            raise RuntimeError("Workspace source must disclose prototype status")
        workspace_html=workspace_html.replace('<meta name="robots" content="noindex,follow">',seo("Workspace multimediale docenti | AI Teaching Lab | MANZO AI","Importa progetti degli Studi immagini, voce e video, verifica provenienza e prepara un kit didattico approvato dal docente.","LearningResource",BASE+ROUTE+"/workspace-multimediale/"),1)
        workspace_dest=target/"workspace-multimediale"/"index.html"
        workspace_dest.parent.mkdir(parents=True,exist_ok=True)
        workspace_dest.write_text(accessible_studio(workspace_html,"workspace"),encoding="utf-8")
        # Publish Mission Studio as a standalone, browser-only teaching micro-app.
        if not LAUNCHPAD.is_file():raise RuntimeError("Missing Mission Studio source")
        launch_html=LAUNCHPAD.read_text(encoding="utf-8")
        marker='<meta name="robots" content="noindex,follow">'
        if launch_html.count(marker)!=1:raise RuntimeError("Mission Studio source must declare prototype status")
        launch_html=launch_html.replace(marker,seo(
            "Mission Studio | AI Teaching Lab | MANZO AI",
            "Micro-app formativa per docenti: progetta un brief didattico, seleziona risorse e verifica obiettivi prima di usare l'IA.",
            "LearningResource",BASE+ROUTE+"/inizia/")+'<link rel="canonical" href="https://manzo8b.github.io'+BASE+ROUTE+'/inizia/">',1)
        launch_dest=target/"inizia"/"index.html"
        launch_dest.parent.mkdir(parents=True,exist_ok=True)
        launch_dest.write_text(launch_html,encoding="utf-8")
        for i,m in enumerate(course["modules"],1):
            text=(DATA/f"module-{i:02d}.md").read_text(encoding="utf-8")
            dest=target/f"modulo-{i:02d}"/"index.html"
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_text(lesson_page(i,m,course,text),encoding="utf-8")
        vocab=target/"glossario"/"index.html"
        vocab.parent.mkdir(parents=True,exist_ok=True)
        vocab.write_text(glossary_page(glossary),encoding="utf-8")
    for i in range(1,6):
        page=target/f"modulo-{i:02d}"/"index.html"
        if not page.is_file():raise RuntimeError("Missing module "+str(page))
        html=page.read_text(encoding="utf-8")
        if html.count("<h1")!=1 or "Metodo MANZO AI" not in html or "Laboratorio" not in html:raise RuntimeError("Semantic module missing")
        if 'content="noindex' in html or 'Non pubblicato' in html:raise RuntimeError("Incorrect public lesson status")
    vocab=target/"glossario"/"index.html"
    if not vocab.is_file() or "Pedagogia" not in vocab.read_text(encoding="utf-8"):raise RuntimeError("Public glossary missing")
    studio=(target/"laboratorio-multimediale"/"index.html")
    if not studio.is_file():raise RuntimeError("Missing multimedia production studio")
    studio_html=studio.read_text(encoding="utf-8")
    if 'id="studio-form"' not in studio_html or 'id="studio-download-html"' not in studio_html:
        raise RuntimeError("Incomplete multimedia production studio")
    image_studio=(target/"studio-immagini"/"index.html")
    if not image_studio.is_file():raise RuntimeError("Missing published image studio")
    image_content=image_studio.read_text(encoding="utf-8")
    if 'id="approve"' not in image_content or 'id="upload"' not in image_content or "Non genera immagini con IA" not in image_content:
        raise RuntimeError("Image Studio review/provenance flow incomplete")
    if '../studio-immagini/' not in studio_html:raise RuntimeError("No link from production studio to image studio")
    voice_studio=(target/"studio-voce"/"index.html")
    if not voice_studio.is_file():raise RuntimeError("Missing published voice studio")
    voice_content=voice_studio.read_text(encoding="utf-8")
    if any(x not in voice_content for x in ('id="record"','id="stop"','id="transcript"','id="approve"','getUserMedia','MediaRecorder')):
        raise RuntimeError("Voice studio recording/transcript/approval incomplete")
    if '../studio-voce/' not in studio_html:raise RuntimeError("No link from production studio to voice studio")
    video_studio=(target/"studio-video"/"index.html")
    if not video_studio.is_file():raise RuntimeError("Missing published video studio")
    video_content=video_studio.read_text(encoding="utf-8")
    if any(marker not in video_content for marker in ('id="scenes"','id="render"','id="captions"','id="approve"','captureStream','MediaRecorder')):
        raise RuntimeError("Video studio storyboard/captions/review incomplete")
    if '../studio-video/' not in studio_html:raise RuntimeError("No link from production studio to video studio")
    workspace_page=target/"workspace-multimediale"/"index.html"
    if not workspace_page.is_file():raise RuntimeError("Missing published multimedia workspace")
    workspace_content=workspace_page.read_text(encoding="utf-8")
    if any(marker not in workspace_content for marker in ('id="jsonfile"','id="approve"','id="exportJSON"','ai-teaching-lab-multimedia-kit-v0.1')):
        raise RuntimeError("Incomplete multimedia workspace import/review/export")
    if '../workspace-multimediale/' not in studio_html:
        raise RuntimeError("Missing multimedia workspace navigation")
    launchpad_page=target/"inizia"/"index.html"
    if not launchpad_page.is_file():raise RuntimeError("Missing Mission Studio micro-app")
    launchpad_html=launchpad_page.read_text(encoding="utf-8")
    if any(key not in launchpad_html for key in ('id="generate"','id="export"','id="copy"','data-kind="image"','ai-teaching-lab-mission-v0.1')):
        raise RuntimeError("Incomplete Mission Studio actions or schema")
    if 'content="noindex,follow"' in launchpad_html:raise RuntimeError("Mission Studio published noindex")
    slides=(target/"presentazione"/"index.html")
    if not slides.is_file() or "15 slide" not in slides.read_text(encoding="utf-8"):raise RuntimeError("Slide reader missing")
    if (MEDIA/"AI_Teaching_Lab_Originali_Per_GitHub_e_Anteprima.zip").is_file():
        slide_files=list((target/"media"/"slides").glob("slide-*.webp"))
        if len(slide_files)!=15:raise RuntimeError("Missing all original NotebookLM slide images")
        if not (target/"media"/"AI_per_Docenti.web.mp4").is_file():raise RuntimeError("Original video missing")
    for tool,path in [("image","studio-immagini"),("voice","studio-voce"),("video","studio-video"),("workspace","workspace-multimediale")]:
        html=(target/path/"index.html").read_text(encoding="utf-8")
        if 'data-atl-tool="'+tool+'"' not in html or 'href="../studio-accessibility.css"' not in html or 'href="#atl-studio-main"' not in html:
            raise RuntimeError("Shared studio accessibility missing: "+tool)
    for asset in ["index.html","app.js","assets.css","lesson.css","feature.css","presentation.css","presentation.js","production-studio.css","production-studio.js","studio-accessibility.css"]:
        if not (target/asset).is_file():raise RuntimeError("Missing asset "+asset)
    home=(target/"index.html").read_text(encoding="utf-8")
    if 'data-course-data-base="./data/"' not in home or 'content="noindex' in home:raise RuntimeError("Home not public")
    if 'data-atl-image-studio="v0.1"' not in home:raise RuntimeError("Home image studio link missing")
    if 'data-atl-voice-studio="v0.1"' not in home:raise RuntimeError("Home voice studio link missing")
    if 'data-atl-video-studio="v0.1"' not in home:raise RuntimeError("Home video studio link missing")
    if 'data-atl-workspace="v0.1"' not in home:raise RuntimeError("Home workspace link missing")
    if 'data-atl-launchpad="v0.1"' not in home:raise RuntimeError("Home Mission Studio entry missing")
    if not (target/"data"/"narrative.json").is_file():raise RuntimeError("Missing full narrative")
    presentation=json.loads((target/"data"/"presentation.json").read_text(encoding="utf-8"))
    if len(presentation["slides"])!=15:raise RuntimeError("Expected 15 presentation slides")
    for name in ("AI_per_Docenti.web.mp4","IA_e_Progettazione_Didattica.pdf","IA_e_Progettazione_Didattica.pptx"):
        if (MEDIA/name).is_file() and not (target/"media"/name).is_file():raise RuntimeError("Missing staged media "+name)
    feature(site,verify)
    print("PASS AI Teaching Lab publisher: 5 complete lessons, public course, 3 Academy features, verified="+str(verify))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--site",type=Path,required=True)
    ap.add_argument("--verify-only",action="store_true")
    a=ap.parse_args()
    publish(a.site,a.verify_only)
