#!/usr/bin/env python3
"""Publish MANZO AI Prompt vs Skill as a FULL Italian course with six detailed readings.
Single-source editorial Markdown, accessible reading navigation, quiz, crossword,
academy/resource discovery, and a reversible idempotent build step.
"""
from __future__ import annotations
import argparse
from html import escape
import json
from pathlib import Path
import re
import shutil
from prompt_skill_visuals import decorate_reading, family_map

try:
    import markdown
except ImportError as exc:
    raise RuntimeError("Markdown 3.10 is required by deploy-pages.yml") from exc

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "editorial/learning/prompt-vs-skill/letture.md"
SCRIPT = ROOT / "editorial/learning/prompt-vs-skill/course.js"
STYLE = ROOT / "editorial/learning/prompt-vs-skill/course.css"
BASE = "/manzo-ai/"
SLUG = "it/formazione/prompt-vs-skill"
MARKER = 'data-ma-prompt-skill="course-v1"'
READINGS = [
    "Quando una richiesta diventa un problema da comprendere",
    "L'architettura di un prompt che possiamo verificare",
    "Dalla ripetizione al metodo riutilizzabile",
    "Dentro una skill: Markdown, metadati e controlli",
    "Skill, plugin, connettori, tool e agenti: dare un nome alle funzioni",
    "Se domani l'intelligenza artificiale si spegnesse",
]
SHORT = [
    "Dalla domanda alla comprensione",
    "Progettare un prompt verificabile",
    "Quando emerge un metodo",
    "Come si costruisce SKILL.md",
    "Orientarsi nell'ecosistema IA",
    "Ragionare anche senza IA",
]
QUIZ = [
    dict(q="Quale parte di un prompt indica perché serve un risultato?",o=["Il formato","L'obiettivo","L'estensione del file","Il nome del plugin"],a=1,e="L'obiettivo esplicita il bisogno da soddisfare; il formato stabilisce soltanto come presentare l'output."),
    dict(q="Quale frase rappresenta soprattutto un vincolo?",o=["Sono al primo anno universitario","Ti allego due dispense","Non inventare fonti","Prepara una scheda"],a=2,e="Un vincolo delimita il comportamento atteso. La sua presenza non elimina la necessità della verifica."),
    dict(q="Un prompt più lungo è sempre migliore?",o=["Sì, in qualsiasi compito","Solo con ChatGPT","No: la struttura deve essere proporzionata al compito","Sì, se contiene un ruolo"],a=2,e="Un prompt deve essere chiaro e adeguato; lunghezza e ruolo non sono garanzie di qualità."),
    dict(q="Qual è la prima soluzione da valutare per una richiesta ricorrente con poche variabili?",o=["Prompt template","Un agente complesso","Una nuova API","Un plugin a pagamento"],a=0,e="Un template spesso permette già di ridurre la riscrittura senza aumentare inutilmente la complessità."),
    dict(q="Quale caratteristica distingue una skill Agent Skills da un semplice prompt?",o=["È sempre più lunga","Contiene per definizione un modello diverso","Garantisce risposte esatte","Organizza istruzioni e risorse riutilizzabili in un formato riconoscibile"],a=3,e="La skill codifica un procedimento riutilizzabile. La correttezza dell'output va ancora verificata."),
    dict(q="Nel formato Agent Skills quale file è centrale?",o=["prompt.exe","config.csv","SKILL.md","readme.pdf"],a=2,e="SKILL.md contiene i metadati e le istruzioni della skill secondo la specifica Agent Skills."),
    dict(q="A cosa servono name e description nel frontmatter YAML?",o=["A indicare identità e pertinenza della skill","A collegare automaticamente tutti i cloud","A certificare l'autore","A criptare i dati"],a=0,e="Nome e descrizione costituiscono metadati importanti; la descrizione aiuta a determinare quando utilizzare la skill."),
    dict(q="Che cosa fa tipicamente un connettore?",o=["Trasforma un prompt in markdown","Collega un sistema a dati o azioni di un servizio autorizzato","Garantisce che una skill sia sicura","Sostituisce il giudizio umano"],a=1,e="Un connettore fornisce accesso a capacità esterne, soggetto alle autorizzazioni. Non decide da solo il metodo."),
    dict(q="Una frase nascosta in un documento esterno che ordina di ignorare le istruzioni è...",o=["Sempre una richiesta prioritaria","Un file di configurazione","Un esempio di output","Un possibile tentativo di prompt injection"],a=3,e="I dati esterni non devono automaticamente essere trattati come istruzioni di maggiore autorità."),
    dict(q="Qual è il senso dell'esercizio finale senza IA?",o=["Provare che ogni prompt aumenta l'intelligenza","Eliminare la tecnologia","Mettere alla prova il trasferimento di un metodo in un altro contesto","Sostituire i professionisti"],a=2,e="Il trasferimento è un obiettivo formativo da esercitare e verificare, non un effetto automatico."),
]
CROSS = [
    ("MARKDOWN",6,6,"h","Formato testuale leggero per strutturare SKILL.md"),
    ("PROMPT",3,6,"v","Input con cui si orienta il modello generativo"),
    ("SKILL",5,9,"v","Metodo riutilizzabile in un agente compatibile"),
    ("VINCOLO",2,11,"v","Limite o condizione che la richiesta deve rispettare"),
    ("OUTPUT",3,3,"h","Risultato generato dal sistema"),
    ("PLUGIN",1,13,"v","Pacchetto di funzionalità installabili"),
    ("AGENTE",8,2,"h","Sistema che coordina modello e strumenti"),
    ("METODO",5,1,"h","Procedura ragionata, documentabile e verificabile"),
]
SOURCE_URLS = [
    "https://developers.openai.com/api/docs/guides/prompt-engineering",
    "https://agentskills.io/specification",
    "https://help.openai.com/it-it/articles/20001256-plugins-in-chatgpt",
    "https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax",
    "https://www.unesco.org/en/articles/ai-competency-framework-students",
]
def e(value):
    return escape(str(value),quote=True)

def get_readings():
    if not SOURCE.is_file():
        raise RuntimeError("Missing complete editorial reading source: "+str(SOURCE))
    data = SOURCE.read_text(encoding="utf-8")
    positions = []
    for title in READINGS:
        marker = "## "+title+"\n"
        pos = data.find(marker)
        if pos < 0 or (positions and pos <= positions[-1]):
            raise RuntimeError("Reading missing or out of order: "+title)
        positions.append(pos)
    pieces=[]
    for i,title in enumerate(READINGS):
        start=positions[i]+len("## "+title+"\n")
        end=positions[i+1] if i+1 < len(READINGS) else len(data)
        body=data[start:end].strip()
        if len(body)<1900:
            raise RuntimeError("Reading needs depth: "+title)
        pieces.append((title,body))
    if data.count("https://") < 10:
        raise RuntimeError("Insufficient linked primary citations")
    for u in SOURCE_URLS:
        if u not in data: raise RuntimeError("Required source absent: "+u)
    if any("Capitolo 0" in x[1] for x in pieces):
        raise RuntimeError("Use Lettura di approfondimento, never Capitolo")
    return pieces

def crossword():
    occupied={}
    start_numbers={}
    for idx,(word,y,x,d,clue) in enumerate(CROSS,1):
        start_numbers[(y,x)]=idx
        for i,char in enumerate(word):
            point=(y+(i if d=="v" else 0),x+(i if d=="h" else 0))
            if point in occupied and occupied[point] != char:
                raise RuntimeError("Crossword collision "+word)
            occupied[point]=char
    miny=min(y for y,x in occupied); maxy=max(y for y,x in occupied)
    minx=min(x for y,x in occupied); maxx=max(x for y,x in occupied)
    cols=maxx-minx+1
    cells=[]
    for y in range(miny,maxy+1):
        for x in range(minx,maxx+1):
            if (y,x) in occupied:
                num=start_numbers.get((y,x))
                indicator=f'<span aria-hidden="true">{num}</span>' if num else ""
                cells.append(f'<label class="ps-cross-square">{indicator}<input type="text" inputmode="text" maxlength="1" autocomplete="off" spellcheck="false" data-answer="{occupied[y,x]}" aria-label="Riga {y-miny+1}, colonna {x-minx+1}"></label>')
            else:
                cells.append('<span class="ps-cross-blank" aria-hidden="true"></span>')
    clues=[]
    for i,(word,y,x,d,clue) in enumerate(CROSS,1):
        clues.append(f'<li><strong>{i} {"Verticale" if d=="v" else "Orizzontale"}</strong> · {e(clue)} <span class="ps-lettercount">({len(word)} lettere)</span></li>')
    return f'<div class="ps-crossboard" style="--ps-cols:{cols}" role="group" aria-label="Cruciverba di {len(CROSS)} parole">'+"".join(cells)+"</div>", "<ol class=\"ps-clues\">"+"".join(clues)+"</ol>"

def build_page(site):
    readings=get_readings()
    path=site/SLUG/"index.html"
    path.parent.mkdir(parents=True,exist_ok=True)
    toc=[]
    blocks=[]
    for i,(title,body) in enumerate(readings,1):
        slug="lettura-"+str(i)
        toc.append(f'<a class="ps-toc-card" href="#{slug}" data-open-reading="{slug}"><span class="ps-toc-count">Lettura di approfondimento</span><strong>{e(SHORT[i-1])}</strong><small>Apri la lettura <span aria-hidden="true">↗</span></small></a>')
        rendered=markdown.markdown(body,extensions=["fenced_code","tables","sane_lists"])
        rendered=decorate_reading(i, rendered)
        blocks.append(f'<section class="ps-reading" id="{slug}"><details {"open" if i==1 else ""}><summary><span class="ps-reading-index">Lettura di approfondimento <em>{i} di 6</em></span><span class="ps-reading-title">{e(title)}</span><span class="ps-reading-toggle" aria-hidden="true">+</span></summary><div class="ps-reading-copy">{rendered}<label class="ps-completion"><input type="checkbox" class="ps-read-check"> Ho letto e riflettuto sul testo</label><a href="#indice-letture" class="ps-back">Torna all’indice delle letture ↑</a></div></details></section>')
    board,clues=crossword()
    canonical="https://manzo8b.github.io/"+SLUG+"/"
    schema={"@context":"https://schema.org","@type":"Course","name":"Prompt vs Skill — Dalla richiesta al metodo","description":"Corso completo di prompt engineering, architettura Agent Skills, plugin e connettori con letture, laboratori, cruciverba e quiz.","inLanguage":"it","isAccessibleForFree":True,"url":canonical,"provider":{"@type":"Organization","name":"MANZO AI"},"author":{"@type":"Person","name":"Marcelo Fernandez"},"datePublished":"2026-11-19","dateModified":"2026-11-19","citation":SOURCE_URLS}
    safe_json=json.dumps(schema,ensure_ascii=False).replace("<","\\u003c")
    quiz_json=json.dumps(QUIZ,ensure_ascii=False).replace("<","\\u003c")
    page=f"""<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Prompt vs Skill · Corso completo | MANZO AI</title>
<meta name="description" content="Corso gratuito e approfondito: dal prompt a SKILL.md, plugin, connettori e ragionamento autonomo. Sei letture narrative, laboratorio, cruciverba e quiz.">
<meta name="robots" content="index,follow"><meta name="theme-color" content="#ffffff">
<meta property="og:type" content="article"><meta property="og:title" content="Prompt vs Skill — Dalla richiesta al metodo">
<meta property="og:description" content="Un corso accessibile con letture approfondite, attività pratiche e riferimenti ufficiali.">
<meta property="og:url" content="{e(canonical)}">
<link rel="stylesheet" href="{BASE}assets/prompt-vs-skill.css">
<script type="application/ld+json">{safe_json}</script></head>
<body data-ma-prompt-skill="course-v1">
<a class="ps-skip" href="#ps-main">Vai al contenuto</a>
<header class="ps-topbar"><div class="ps-shell ps-topbar-row">
<a class="ps-brand" href="{BASE}it/">MANZO<span>AI</span></a>
<nav aria-label="Navigazione del corso"><a href="{BASE}it/academy/">Academy</a><a href="#indice-letture">Letture</a><a href="#laboratorio">Laboratorio</a><a href="#verifica">Verifica</a></nav>
</div></header>
<main id="ps-main">
<section class="ps-hero"><div class="ps-shell">
<span class="ps-eyebrow">MANZO AI / ACADEMY · CORSO COMPLETO</span>
<p class="ps-context">Dal prompt alla skill, dall'istruzione al ragionamento</p>
<h1>Prompt <span class="ps-vs">vs</span> Skill</h1>
<p class="ps-subtitle">Come si passa da una richiesta occasionale a un metodo riutilizzabile? E che cosa possiamo imparare anche quando l'intelligenza artificiale non è disponibile?</p>
<div class="ps-hero-bottom"><span>Per studenti, professionisti, freelance e persone curiose</span><span>6 letture approfondite</span><span>Laboratorio + cruciverba + quiz</span></div>
<a class="ps-main-cta" href="#indice-letture">Inizia il corso <span aria-hidden="true">↘</span></a>
</div></section>
<section class="ps-shell ps-intro" aria-label="Presentazione del corso">
<div><p class="ps-overline">IL PERCORSO</p><h2>Non imparare soltanto a chiedere<br>Impara a progettare il lavoro</h2></div>
<div><p>Partiamo da una studentessa universitaria e seguiamo le sue decisioni: dalla prima richiesta generica alla costruzione di un metodo affidabile. Le storie sono esempi didattici; le definizioni tecniche sono documentate con fonti primarie.</p>
<p>Ogni parte del corso è una <strong>lettura di approfondimento</strong>, non un capitolo numerato. Apri una lettura alla volta, sperimenta e torna all'indice quando desideri. Il percorso è gratuito, senza iscrizione e senza progressi salvati sul server.</p></div>
</section>
<section class="ps-shell ps-guide" id="indice-letture"><div class="ps-section-heading"><div><p class="ps-overline">CONTENUTI DEL CORSO</p><h2>Le letture di approfondimento</h2></div><p>Sei percorsi narrativi, dal primo prompt al metodo applicato nella vita quotidiana</p></div>
<div class="ps-toc">{"".join(toc)}</div>
<nav class="ps-viz-jumps" aria-label="Apri le mappe visive">
<strong>Mappe visive del corso</strong>
<a href="#lettura-2" data-open-reading="lettura-2">Architettura del prompt ↗</a>
<a href="#lettura-3" data-open-reading="lettura-3">Il salto di qualità ↗</a>
<a href="#lettura-4" data-open-reading="lettura-4">Struttura della skill ↗</a>
<a href="#mappa-famiglia">Famiglia con quattro figli ↗</a>
</nav>
<p class="ps-counter" id="ps-progress" aria-live="polite">0 di 6 letture segnate come completate in questa sessione</p>
</section>
<div class="ps-shell ps-readings">{"".join(blocks)}</div>
{family_map()}
<section class="ps-shell ps-lab" id="laboratorio">
<p class="ps-overline">LABORATORIO DI PROGETTAZIONE</p><h2>Un problema, tre architetture</h2>
<p>Giulia ripete il ripasso ogni settimana. Confronta un prompt scritto una volta, un prompt template e una skill Agent Skills. La tua sfida non è costruire la soluzione più complessa, ma giustificare quando un metodo riutilizzabile produce un vantaggio concreto.</p>
<div class="ps-step-grid"><article><span>FASE A</span><h3>Prompt strutturato</h3><p>Definisci obiettivo, materiali, compito, vincoli, output e verifica per un singolo incarico.</p></article>
<article><span>FASE B</span><h3>Prompt template</h3><p>Identifica i dati che cambiano. Mantieni stabili le istruzioni che funzionano e sostituisci le variabili.</p></article>
<article><span>FASE C</span><h3>Skill documentata</h3><p>Se il contesto lo giustifica, descrivi attivazione, procedura, input necessari, eccezioni, controllo e casi di test.</p></article></div>
<details class="ps-practice"><summary>Apri la consegna pratica e il criterio di valutazione <span>+</span></summary><div><p><strong>Consegna.</strong> Usa un incarico reale ma non sensibile: organizzare una scheda di studio, preparare un breve report o sintetizzare un dossier. Scrivi tre versioni equivalenti, poi confronta numero di passaggi manuali, errori, facilità di aggiornamento e tempo di verifica.</p><p><strong>Criterio.</strong> La skill è giustificata solo se il metodo ricorre, ha istruzioni stabili e l'ambiente è compatibile. Se il template è più semplice e offre risultati equivalenti, puoi sceglierlo.</p><p><strong>Test.</strong> Prova con dati completi, incompleti e con una richiesta non pertinente. Registra che cosa succede anziché limitarti a un'impressione.</p></div></details>
</section>
<section class="ps-shell ps-cross" id="cruciverba">
<div class="ps-section-heading"><div><p class="ps-overline">ESERCIZIO INTERATTIVO</p><h2>Cruciverba del lessico IA</h2></div><p>Otto termini da riconoscere. Le definizioni riprendono le parole incontrate nelle letture</p></div>
<div class="ps-cross-layout"><div>{board}<div class="ps-cross-actions"><button id="ps-check-cross" type="button">Controlla le risposte</button><button id="ps-clear-cross" type="button" class="ps-outline">Ricomincia</button></div><p id="ps-cross-result" role="status" aria-live="polite">Scrivi una lettera per casella</p></div><div><h3>Definizioni</h3>{clues}</div></div>
</section>
<section class="ps-shell ps-quiz" id="verifica">
<p class="ps-overline">VERIFICA DELL'APPRENDIMENTO</p><h2>Quiz finale con spiegazioni</h2>
<p>Dieci domande sul funzionamento dei prompt, sulla struttura delle skill e sulla scelta della soluzione proporzionata. Le risposte commentate aiutano a comprendere anche gli errori.</p>
<div id="ps-quiz-form"><p>Attiva JavaScript per svolgere il quiz interattivo. Puoi comunque leggere tutte le spiegazioni e gli esempi nelle letture.</p></div>
<script type="application/json" id="ps-quiz-data">{quiz_json}</script>
</section>
<section class="ps-shell ps-outro"><p class="ps-overline">RIFLESSIONE CONCLUSIVA</p><h2>E se domani l'IA si spegnesse?</h2><p>Il valore di questo percorso non è possedere il prompt più lungo o la skill più complessa. È riuscire a riconoscere un problema, distinguere dati e ipotesi, progettare un metodo, verificare gli errori e modificare le decisioni quando la realtà cambia.</p><a href="#lettura-6" data-open-reading="lettura-6">Rileggi la riflessione sulla famiglia <span aria-hidden="true">↗</span></a></section>
</main>
<footer class="ps-footer"><div class="ps-shell"><p><strong>MANZO AI</strong> · Corso divulgativo indipendente · 19 novembre 2026</p><p>Testi con riferimenti documentali nelle letture · Nessuna certificazione accreditata · Esercizi svolti localmente nel browser, senza invio di risposte al server</p><a href="{BASE}it/academy/">Torna all'Academy</a></div></footer>
<script src="{BASE}assets/prompt-vs-skill.js" defer></script></body></html>"""
    path.write_text(page,encoding="utf-8")
    return path

def add_academy_card(site):
    academy=site/"it/academy/index.html"
    resources=site/"it/risorse/index.html"
    if not academy.is_file() or not resources.is_file():
        raise RuntimeError("Academy and resources pages are necessary for a real course card")
    for target,source in ((academy,"academy"),(resources,"resources")):
        doc=target.read_text(encoding="utf-8")
        if MARKER in doc: continue
        if "</main>" not in doc: raise RuntimeError("Missing main in "+str(target))
        card=f'''<section class="ps-academy-discovery" {MARKER} aria-labelledby="ps-card-{source}">
<div class="ps-discovery-top"><span>MANZO AI · CORSO COMPLETO</span><span>GRATUITO · IN ITALIANO</span></div>
<div class="ps-discovery-content"><div><p class="ps-discovery-kicker">NUOVO PERCORSO FORMATIVO</p><h2 id="ps-card-{source}">Prompt <em>vs</em> Skill</h2><p>Dalla prima richiesta all’architettura di una skill: sei letture di approfondimento, laboratorio, cruciverba e quiz. Per studenti, professionisti e chiunque voglia usare l'IA con metodo.</p></div><a href="{BASE}{SLUG}/" class="ps-discovery-cta">Apri il corso <span aria-hidden="true">↗</span></a></div></section>'''
        doc=doc.replace("</main>",card+"</main>",1)
        doc=doc.replace("</head>",f'<link rel="stylesheet" href="{BASE}assets/prompt-vs-skill.css"></head>',1)
        target.write_text(doc,encoding="utf-8")

def verify(site):
    target=site/SLUG/"index.html"
    if not target.is_file(): raise RuntimeError("Published course page is missing")
    doc=target.read_text(encoding="utf-8")
    if doc.count("class=\"ps-reading\"") != 6: raise RuntimeError("Expected six complete readings")
    if doc.count("Lettura di approfondimento") < 7: raise RuntimeError("Reading label missing")
    if "Capitolo 01" in doc or "Capitolo 02" in doc: raise RuntimeError("Incorrect chapter labels")
    # All four teaching diagrams must render in the final HTML (not just the source).
    for key in ('id="mappa-prompt"','id="mappa-salto"','id="mappa-skill"','id="mappa-famiglia"'):
        if doc.count(key) != 1: raise RuntimeError("Missing or duplicated learning flowchart: "+key)
    if "Uno dei figli si ammala" not in doc or "famiglia composta da due genitori e quattro figli" not in doc:
        raise RuntimeError("Family scenario or its complete narrative is missing")
    for key in ("id=\"laboratorio\"","id=\"cruciverba\"","id=\"verifica\"","id=\"ps-quiz-data\""):
        if key not in doc: raise RuntimeError("Course activity missing: "+key)
    if len(json.loads(re.search(r'<script type="application/json" id="ps-quiz-data">(.+?)</script>',doc).group(1))) != 10:
        raise RuntimeError("Expected ten quiz questions")
    for fname in ("prompt-vs-skill.css","prompt-vs-skill.js"):
        if not (site/"assets"/fname).is_file(): raise RuntimeError("Missing course asset "+fname)
    for p in ("it/academy/index.html","it/risorse/index.html"):
        page=(site/p).read_text(encoding="utf-8")
        if page.count(MARKER)!=1 or f'{BASE}{SLUG}/' not in page: raise RuntimeError("Missing or duplicate course card "+p)
    print("Prompt vs Skill: six deep readings, four visual flows, family narrative, 10 quiz items, 8 crossword words, Academy and resources cards verified")

def publish(site):
    if not (site/"it/academy/index.html").is_file(): raise RuntimeError("Academy not found")
    for file,asset in ((STYLE,"prompt-vs-skill.css"),(SCRIPT,"prompt-vs-skill.js")):
        if not file.is_file(): raise RuntimeError("Source asset missing: "+str(file))
        (site/"assets").mkdir(parents=True,exist_ok=True)
        shutil.copy2(file,site/"assets"/asset)
    build_page(site)
    add_academy_card(site)
    verify(site)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--site",type=Path,required=True)
    parser.add_argument("--verify-only",action="store_true")
    args=parser.parse_args()
    verify(args.site) if args.verify_only else publish(args.site)
