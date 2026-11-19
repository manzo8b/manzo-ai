#!/usr/bin/env python3
"""Build MANZO AI / AI Product Builder — Centroni City.
Complete narrative course, safe civic-service prototype, editable local-only
blueprint, six readings, schematic diagrams, quiz and learning quality gates.
This is NOT a production civic reporting application.
"""
from __future__ import annotations
import argparse
from html import escape
from pathlib import Path
import json
import re
import shutil

try:
    import markdown
except ImportError as err:
    raise RuntimeError("GitHub Pages must install markdown==3.10") from err

ROOT=Path(__file__).resolve().parent.parent
SOURCE=ROOT/"editorial/learning/centroni-city-builder/letture.md"
STYLE=ROOT/"theme/centroni-city-course.css"
SCRIPT=ROOT/"theme/centroni-city-course.js"
BASE="/manzo-ai/"
ROUTE="it/formazione/ai-product-builder-centroni-city"
MARKER='data-ma-centroni-catalog="v1"'
READINGS=[
    "Dalla conversazione al problema reale",
    "Prima la persona, poi la funzione",
    "Dall'idea al blueprint: input, processo, output",
    "Prototipare con metodo, anche a budget zero",
    "Qualità, responsabilità e sicurezza dei contenuti civici",
    "Misurare il valore, preparare la versione successiva",
]
SHORT=[
    "Da Facebook al bisogno reale",
    "Progettare per le persone",
    "Prima la logica, poi il prompt",
    "Costruire Centroni City V1",
    "Testare rischi e informazioni",
    "Misurare l'utilità civica",
]
PHASES=[
    ("Bisogno","Problemi reali e criteri di successo"),
    ("Persone","Scenari e percorsi d'uso"),
    ("Blueprint","Input, processo, output"),
    ("Prototipo","Interfaccia e dati sintetici"),
    ("Verifica","Errori e condizioni di blocco"),
    ("Valore","Risultati e manutenzione"),
]
QUIZ=[
    dict(q="Qual è il problema iniziale più rilevante di Centroni City?",options=["Il colore di Facebook","L'informazione sparsa, poco verificabile o difficile da recuperare","L'assenza di un chatbot obbligatorio","La mancanza di servizi a pagamento"],answer=1,why="Il progetto nasce dall'esigenza informativa dei cittadini, non dalla scelta di una tecnologia."),
    dict(q="Un post Facebook pubblico può essere importato automaticamente nel portale?",options=["Sì, sempre","Solo se contiene una fotografia","No: vanno considerate fonti, diritti, privacy e autorizzazioni","Sì, se è molto condiviso"],answer=2,why="L'accessibilità di un contenuto sui social non equivale a un'autorizzazione indiscriminata al riuso."),
    dict(q="Da dove comincia la progettazione prima di usare l'IA?",options=["Dalla lista di funzionalità","Da una scheda del problema, persone coinvolte e risultato atteso","Dal prompt più lungo disponibile","Dalla scelta della palette"],answer=1,why="Il problem framing distingue il bisogno dalla soluzione, evitando prototipi vistosi ma poco utili."),
    dict(q="Quale sequenza rappresenta l'architettura IPO?",options=["Input → Processo → Output","Internet → Prompt → Opinione","Immagine → Pubblicità → Offerta","IA → Plugin → Organizzazione"],answer=0,why="IPO aiuta a distinguere dati in ingresso, regole e risultato prima di generare codice."),
    dict(q="Nella V1 Centroni City può dichiarare di ricevere denunce formali?",options=["Sì, se usa un form gratuito","No: deve indirizzare alle autorità competenti","Sì, con un badge istituzionale","Solo con una grafica professionale"],answer=1,why="Una demo indipendente non è uno sportello ufficiale e non deve archiviare accuse o simulare protocolli."),
    dict(q="Che cosa fare di una notizia senza fonte attendibile?",options=["Pubblicarla come confermata","Inventare una data di verifica","Non presentarla come fatto verificato; chiedere una fonte","Aggiungere un testo più lungo"],answer=2,why="La catena editoriale richiede provenienza, revisione e gestione delle lacune."),
    dict(q="Quale funzione non appartiene automaticamente a una demo statica senza backend?",options=["Mostrare guide e link","Visualizzare schede con informazioni","Gestire in modo sicuro ticket personali, account e notifiche","Organizzare un menu leggibile"],answer=2,why="Ricevere e gestire contributi richiede infrastruttura, autorizzazioni, sicurezza e responsabili reali."),
    dict(q="Come misuri un miglioramento utile per un cittadino?",options=["Con il numero di emoji","Verificando se trova un canale appropriato con meno difficoltà","Con il numero di schermate generate","Con la lunghezza del prompt"],answer=1,why="La riuscita di una persona su compiti reali è più significativa della sola quantità di funzioni."),
    dict(q="Una persona pubblica un'accusa identificativa contro un vicino: cosa deve fare il prototipo?",options=["Pubblicarla per trasparenza","Metterla in evidenza","Non pubblicare accuse o dati personali e indirizzare alle autorità appropriate","Chiedere più condivisioni"],answer=2,why="Il prototipo non è un canale legittimo per accuse non verificate e deve prevenire danni alle persone."),
    dict(q="Qual è il traguardo del corso?",options=["Scrivere più prompt possibili","Construire una landing page senza verifiche","Progettare, collaudare e valutare un prodotto utile, anche senza programmazione iniziale","Sostituire gli uffici pubblici"],answer=2,why="Il progetto didattico si misura su bisogni, coerenza della logica, sicurezza e utilità verificabile."),
]
SOURCES=[
    "https://www.comune.roma.it/web/it/i-quartieri-di-roma-mun7.page",
    "https://www.comune.roma.it/web/it/attivita-progetto.page?contentId=PRG1506858",
    "https://www.comune.roma.it/web/it/suggerimenti-segnalazioni-e-reclami-urp-uffici-relazioni-con-il-pubblico.page",
    "https://designers.italia.it/risorse-per-progettare/comprendere/",
    "https://designers.italia.it/normativa/linee-guida-di-design/requisito-4-1/",
    "https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/10071261",
    "https://pubmed.ncbi.nlm.nih.gov/932126/",
]
def e(x):return escape(str(x),quote=True)

def read():
    if not SOURCE.is_file():raise RuntimeError("Missing Centroni City editorial source")
    doc=SOURCE.read_text(encoding="utf-8")
    offsets=[]
    for h in READINGS:
        token="## "+h+"\n"
        i=doc.find(token)
        if i<0 or (offsets and i<=offsets[-1]):
            raise RuntimeError("Reading missing or out of order: "+h)
        offsets.append(i)
    parts=[]
    for i,title in enumerate(READINGS):
        start=offsets[i]+len("## "+title+"\n")
        end=offsets[i+1] if i+1<len(READINGS) else len(doc)
        body=doc[start:end].strip()
        if len(body)<2200:raise RuntimeError("Reading is too shallow: "+title)
        parts.append((title,body))
    for url in SOURCES:
        if url not in doc:raise RuntimeError("Authoritative source missing: "+url)
    for term in ("non riceve né conserva segnalazioni personali","nessun dato del segnalante","indipendente"):
        if term.lower() not in doc.lower():raise RuntimeError("Safety boundary absent: "+term)
    return parts

def phases():
    cards=[]
    for i,(title,desc) in enumerate(PHASES,1):
        cards.append(f'<li><span>FASE {i:02d}</span><strong>{e(title)}</strong><small>{e(desc)}</small></li>')
    return f'<ol class="cc-mast" aria-label="Sei fasi della progettazione AI Product Builder">{"".join(cards)}</ol>'

def ipo():
    defs=[
      ("INPUT","Informazioni in ingresso","Esigenza dei residenti, fonti istituzionali e avvisi da verificare"),
      ("PROCESSO","Regole e controlli","Classificare, verificare, aggiornare, scegliere i canali appropriati"),
      ("OUTPUT","Risultato per il cittadino","Notizia con fonte e data, guida, collegamento ufficiale, avviso di limite"),
    ]
    return '<div class="cc-ipo" aria-label="Architettura logica input, processo e output">'+''.join(
        f'<article><span>{e(name)}</span><h3>{e(title)}</h3><p>{e(desc)}</p></article>' for name,title,desc in defs)+'</div>'

def lab():
    fields=[
      ("project","Progetto","Centroni City","Nome del tuo prodotto"),
      ("problem","Problema da risolvere","Le informazioni di quartiere sono disperse, difficili da aggiornare e verificare.","Che cosa impedisce a una persona di completare un compito?"),
      ("target","Per chi","Residenti di Centroni e zone limitrofe, anche con poca esperienza digitale.","Descrivi persone e bisogni senza inserire dati identificativi"),
      ("input","Input","Fonti ufficiali, informazioni editoriali autorizzate, bisogni generali.","Che cosa entra nel sistema?"),
      ("process","Processo e regole","Controllare fonti e date, classificare, bloccare contenuti incerti, indirizzare ai canali corretti.","Quali regole determinano il risultato?"),
      ("output","Output atteso","Schede aggiornabili, guide di servizio, percorsi ufficiali.","Che cosa vedrà o otterrà il cittadino?"),
      ("limits","Vincoli e limiti","Prototipo indipendente; nessuna denuncia, nessuna raccolta di dati personali; link esterni verificabili.","Quali azioni non deve compiere la V1?"),
      ("measure","Come misurare l'utilità","Tempo necessario per trovare un canale ufficiale e successo del compito in un test.","Come capirai se il prodotto aiuta davvero?"),
    ]
    cards=[]
    for i,(id,label,default,hint) in enumerate(fields):
        full=" cc-field--full" if id in ("problem","limits") else ""
        safe=e(default)
        control=f'<input id="cc-{id}" type="text" value="{safe}" maxlength="400" autocomplete="off">' if id=="project" else f'<textarea id="cc-{id}" rows="3" maxlength="900">{e(default)}</textarea>'
        cards.append(f'<div class="cc-field{full}"><label for="cc-{id}">{e(label)}</label>{control}<small>{e(hint)}</small></div>')
    return f'''<section class="ps-shell cc-studio" id="cc-blueprint" aria-labelledby="cc-studio-title">
<div class="cc-studio-inner"><div class="cc-studio-top"><p class="cc-kicker">LABORATORIO 01 · PROGETTA PRIMA DI GENERARE</p><span class="cc-status-pill">Funziona senza account</span></div>
<h2 id="cc-studio-title">Il tuo Blueprint operativo</h2><p>Il progetto nasce dalle decisioni del partecipante. Puoi modificare il caso Centroni City o adattarlo a un altro quartiere. <strong>Non inserire dati personali, accuse o segnalazioni reali.</strong> Il contenuto resta in questa pagina e viene perso se la ricarichi.</p>
<div class="cc-form">{"".join(cards)}</div><div class="cc-actions"><button class="cc-btn" id="cc-copy-blueprint" type="button">Copia il blueprint</button><button class="cc-btn cc-btn--light" id="cc-copy-coach" type="button">Copia il Tutor socratico</button></div>
<p id="cc-studio-status" role="status" aria-live="polite" class="cc-rule">La copia usa gli appunti compilati qui; nessuna informazione viene trasmessa al server.</p>
<details class="cc-coach"><summary>Come utilizzare il tutor socratico senza delegare il progetto</summary><p>Copia il prompt in un modello IA a tua scelta e rispondi alle sue domande una per volta. Non permettere al modello di generare direttamente il prodotto finché non hai definito bisogni, input, regole e criteri di verifica. Controlla gli output: il tutor può sbagliare.</p></details>
</div></section>'''

def prototype():
    return f'''<section class="ps-shell cc-sim" id="cc-prototipo" aria-labelledby="cc-proto-title">
<p class="ps-overline">LABORATORIO 02 · PROTOTIPO NAVIGABILE</p>
<h2 id="cc-proto-title">Centroni City · Anteprima V1</h2>
<p>Non è un servizio già operativo: è una dimostrazione di progettazione civica. Tocca le sezioni, valuta quanto sono chiare e osserva come funzionano i percorsi di orientamento alle segnalazioni.</p>
<div class="cc-sim-wrap"><div class="cc-sim-head"><strong class="cc-sim-brand">CENTRONI<span>CITY</span></strong><span class="cc-sim-badge">PROTOTIPO · DATI DIMOSTRATIVI</span></div>
<div class="cc-sim-tabs" role="tablist" aria-label="Anteprima di Centroni City">
<button type="button" role="tab" aria-selected="true" tabindex="0" data-tab="info">Informazioni</button>
<button type="button" role="tab" aria-selected="false" tabindex="-1" data-tab="servizi">Servizi</button>
<button type="button" role="tab" aria-selected="false" tabindex="-1" data-tab="segnalazioni">Segnalazioni</button>
</div><div id="cc-sim-content" class="cc-sim-content" role="tabpanel" aria-live="polite"><h3>Informazioni e fonti</h3><p>L'anteprima si avvia qui. Attiva JavaScript per esplorare le tre aree dimostrative.</p></div>
</div></section>'''

def quality():
    checks=[
      "Il problema civico è concreto e definito prima della scelta degli strumenti",
      "Ogni avviso pubblicabile ha una fonte controllabile e una data",
      "La V1 non raccoglie né trasmette denunce, accuse o dati personali",
      "I percorsi di segnalazione portano a canali istituzionali appropriati",
      "Almeno cinque casi limite sono stati provati e documentati",
      "La demo è leggibile e navigabile su smartphone e con tastiera",
    ]
    html=''.join(f'<label><input type="checkbox"><span>{e(item)}</span></label>' for item in checks)
    return f'''<section class="ps-shell cc-check" id="cc-verifiche">
<p class="ps-overline">LABORATORIO 03 · SICUREZZA E CONTROLLO</p><h2>La checklist di rilascio</h2>
<p>Segna i controlli completati solo se puoi dimostrarli. La spunta è un promemoria di apprendimento, non una certificazione di conformità né un'autorizzazione a raccogliere segnalazioni reali.</p>
<div class="cc-check-list">{html}</div><p class="cc-check-meter" id="cc-check-status" role="status" aria-live="polite">0 di 6 verifiche completate</p>
</section>'''

def build_page(site:Path):
    readings=read()
    cards=[]; sections=[]
    for i,(title,text) in enumerate(readings,1):
        slug=f"cc-lettura-{i}"
        cards.append(f'<a class="ps-toc-card" href="#{slug}" data-open-reading="{slug}"><span class="ps-toc-count">Lettura di approfondimento</span><strong>{e(SHORT[i-1])}</strong><small>Apri la lettura <span aria-hidden="true">↗</span></small></a>')
        rendered=markdown.markdown(text,extensions=["tables","fenced_code","sane_lists"])
        sections.append(f'<section class="ps-reading" id="{slug}"><details {"open" if i==1 else ""}><summary><span class="ps-reading-index">Lettura di approfondimento <em>{i} di 6</em></span><span class="ps-reading-title">{e(title)}</span><span class="ps-reading-toggle" aria-hidden="true">+</span></summary><div class="ps-reading-copy">{rendered}<label class="ps-completion"><input type="checkbox" class="ps-read-check"> Ho letto e riflettuto sul contenuto</label><a class="ps-back" href="#cc-letture">Torna all'indice delle letture ↑</a></div></details></section>')
    url="https://manzo8b.github.io/manzo-ai/"+ROUTE+"/"
    schema={"@context":"https://schema.org","@type":"Course","name":"AI Product Builder — Dal problema al prodotto: Centroni City","description":"Corso aperto di progettazione digitale con caso Centroni City: bisogni dei cittadini, blueprint IPO, prototipo, sicurezza, verifica e misurazione del valore.","inLanguage":"it","isAccessibleForFree":True,"url":url,"provider":{"@type":"Organization","name":"MANZO AI"},"datePublished":"2026-11-19","citation":SOURCES}
    json_schema=json.dumps(schema,ensure_ascii=False).replace("<","\\u003c")
    quiz=json.dumps(QUIZ,ensure_ascii=False).replace("<","\\u003c")
    body=f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Product Builder · Costruire Centroni City | MANZO AI</title>
<meta name="description" content="Corso gratuito MANZO AI: dal gruppo Facebook al prototipo civico Centroni City. Sei letture, architettura Input Processo Output, blueprint interattivo, demo e quiz con fonti ufficiali.">
<meta name="robots" content="index,follow"><meta name="theme-color" content="#ffffff">
<meta property="og:title" content="AI Product Builder — Costruire Centroni City"><meta property="og:type" content="article">
<meta property="og:description" content="Dalla community a un servizio civico: progettazione, fonti, prototipo e controllo qualità.">
<meta property="og:url" content="{e(url)}">
<link rel="stylesheet" href="{BASE}assets/prompt-vs-skill.css">
<link rel="stylesheet" href="{BASE}assets/centroni-city-course.css">
<script type="application/ld+json">{json_schema}</script></head>
<body data-ma-centroni="course-v1" data-ma-prompt-skill="course-v1">
<a class="ps-skip" href="#cc-main">Vai al contenuto</a>
<header class="ps-topbar"><div class="ps-shell ps-topbar-row"><a class="ps-brand" href="{BASE}it/">MANZO<span>AI</span></a><nav aria-label="Navigazione del corso"><a href="{BASE}it/academy/">Academy</a><a href="#cc-letture">Letture</a><a href="#cc-blueprint">Blueprint</a><a href="#cc-prototipo">Demo</a><a href="#cc-quiz">Quiz</a></nav></div></header>
<main id="cc-main">
<section class="ps-hero cc-hero"><div class="ps-shell"><span class="ps-eyebrow">MANZO AI · AI PRODUCT BUILDER · CORSO COMPLETO</span>
<p class="ps-context">Dal problema reale al prodotto digitale</p><h1>Costruire <em>Centroni City</em></h1>
<p class="ps-subtitle">Come trasformare una community Facebook in un progetto civico utile: sei letture narrative, logica prima del prompt, demo, controlli e un metodo riutilizzabile.</p>
<div class="ps-hero-bottom"><span>Studenti e professionisti</span><span>6 letture approfondite</span><span>Blueprint + demo + quiz</span><span>Budget base 0 €</span></div>
<a class="ps-main-cta" href="#cc-letture">Inizia il corso <span aria-hidden="true">↘</span></a></div></section>
<div class="ps-shell"><p class="cc-rule"><strong>Un progetto indipendente, non istituzionale.</strong> Centroni City è un caso di studio. La demo non raccoglie segnalazioni né sostituisce gli uffici pubblici. Per denunce e situazioni urgenti occorre rivolgersi alle autorità competenti.</p></div>
<section class="ps-shell ps-intro"><div><p class="ps-overline">PROGETTAZIONE ATTIVA</p><h2>Una sola idea, sei decisioni importanti</h2><p>Il corso forma persone capaci di progettare strumenti utili, non soltanto generare interfacce con un prompt.</p></div>
<div><p>Partiamo da un problema di quartiere. Impareremo ad ascoltare gli utenti, disegnare il processo Input → Processo → Output, impostare una V1 e testare errori di pubblicazione, moderazione, privacy e accessibilità.</p>
<p>Ogni tappa produce un artefatto. I personaggi e le situazioni narrative sono immaginari; i dati istituzionali rimandano alle rispettive fonti.</p></div></section>
<section class="ps-shell cc-visual" id="cc-percorso"><p class="ps-overline">MAPPA INTERATTIVA DEL METODO</p><h2>Il percorso dal problema al valore</h2>
<p>Prima la ricerca di un bisogno, poi il disegno del servizio e la verifica dell'utilità. L'IA entra come supporto, non come sostituto della progettazione.</p>{phases()}
<p class="cc-visual-note">Le sei fasi sono una proposta formativa MANZO AI: non un protocollo istituzionale né una garanzia automatica di qualità.</p></section>
<section class="ps-shell ps-guide" id="cc-letture"><div class="ps-section-heading"><div><p class="ps-overline">CONTENUTI DEL CORSO</p><h2>Le letture di approfondimento</h2></div>
<p>Una storia continua e sei tappe progressive: dal bisogno del cittadino alla valutazione della V1.</p></div>
<div class="ps-toc">{"".join(cards)}</div><p class="ps-counter" id="cc-progress" aria-live="polite">0 di 6 letture completate (solo durante questa visita)</p></section>
<div class="ps-shell ps-readings">{"".join(sections)}</div>
<section class="ps-shell cc-visual" id="cc-ipo"><p class="ps-overline">MAPPA OPERATIVA · CENTRONI CITY</p><h2>Input → Processo → Output</h2>
<p>Una scheda del cittadino nasce da dati verificabili, regole editoriali e un output comprensibile. Il processo non dovrebbe trasformare voci non confermate in fatti.</p>{ipo()}</section>
{lab()}
{prototype()}
{quality()}
<section class="ps-shell cc-quiz" id="cc-quiz"><p class="ps-overline">VERIFICA FINALE</p><h2>Dieci scelte da progettista</h2>
<p>Le risposte sono commentate. L'obiettivo è spiegare perché una scelta di prodotto migliora oppure mette a rischio l'esperienza del cittadino.</p>
<div id="cc-quiz-root"><p>Attiva JavaScript per svolgere il quiz; le domande riflessive restano disponibili nelle letture.</p></div><script type="application/json" id="cc-quiz-data">{quiz}</script></section>
<section class="ps-shell cc-bottom"><p class="ps-overline">IL TRAGUARDO</p><h2>Un prodotto utile comincia da una responsabilità chiara</h2>
<p>Un prototipo non diventa un servizio civico solo perché è pubblicato. Deve essere aggiornabile, accessibile, documentato e gestito da persone responsabili. Questa capacità di valutare il prodotto è il cuore del metodo AI Product Builder.</p>
<a href="#cc-blueprint">Rivedi il Blueprint del tuo progetto ↗</a></section>
</main><footer class="ps-footer"><div class="ps-shell"><p><strong>MANZO AI</strong> · Formazione indipendente · Novembre 2026</p>
<p>Centroni City è una simulazione progettuale; nessun servizio pubblico è gestito o imitato · Nessuna raccolta dati nella demo</p><a href="{BASE}it/academy/">Torna all'Academy</a></div></footer>
<script src="{BASE}assets/centroni-city-course.js" defer></script></body></html>'''
    target=site/ROUTE/"index.html"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(body,encoding="utf-8")

def add_discovery(site:Path):
    for p,section in ((site/"it/academy/index.html","academy"),(site/"it/risorse/index.html","resources")):
        if not p.is_file():raise RuntimeError("Missing catalog "+str(p))
        html=p.read_text(encoding="utf-8")
        if MARKER in html:raise RuntimeError("Duplicate course card "+str(p))
        if "</main>" not in html:raise RuntimeError("Catalog invalid")
        card=f'''<section class="ps-academy-discovery" {MARKER} aria-labelledby="cc-discovery-{section}">
<div class="ps-discovery-top"><span>MANZO AI · AI PRODUCT BUILDER</span><span>GRATUITO · IN ITALIANO</span></div>
<div class="ps-discovery-content"><div><p class="ps-discovery-kicker">NUOVO PERCORSO FORMATIVO</p>
<h2 id="cc-discovery-{section}">Costruire Centroni City</h2>
<p>Un solo progetto, sei letture: dal bisogno di quartiere a un prodotto civico verificabile. Blueprint, anteprima interattiva, QA e quiz.</p></div>
<a href="{BASE}{ROUTE}/" class="ps-discovery-cta">Apri il corso <span aria-hidden="true">↗</span></a></div></section>'''
        html=html.replace("</main>",card+"</main>",1)
        html=html.replace("</head>",f'<link rel="stylesheet" href="{BASE}assets/prompt-vs-skill.css"></head>',1)
        p.write_text(html,encoding="utf-8")

def verify(site:Path):
    page=site/ROUTE/"index.html"
    if not page.is_file():raise RuntimeError("Course not published")
    doc=page.read_text(encoding="utf-8")
    if doc.count('class="ps-reading"')!=6:raise RuntimeError("Missing six readings")
    for fragment in ('id="cc-percorso"','id="cc-ipo"','id="cc-blueprint"','id="cc-prototipo"','id="cc-verifiche"','id="cc-quiz"'):
        if doc.count(fragment)!=1:raise RuntimeError("Missing or duplicated learning module "+fragment)
    if doc.count('class="cc-field')!=8:raise RuntimeError("Blueprint must have eight fields")
    if doc.count('class="cc-mast"')!=1:raise RuntimeError("Missing six-step visual")
    if len(json.loads(re.search(r'<script type="application/json" id="cc-quiz-data">(.+?)</script>',doc).group(1)))!=10:
        raise RuntimeError("Quiz must have ten questions")
    if 'Capitolo 01' in doc or 'Capitolo 02' in doc:raise RuntimeError("Unit labels must be Lettura di approfondimento")
    for fn in ("centroni-city-course.css","centroni-city-course.js"):
        if not (site/"assets"/fn).is_file():raise RuntimeError("Course asset missing "+fn)
    if 'non raccoglie segnalazioni' not in doc.lower():raise RuntimeError("Civic privacy disclaimer absent")
    for path in ("it/academy","it/risorse"):
        html=(site/path/"index.html").read_text(encoding="utf-8")
        if html.count(MARKER)!=1 or f"{BASE}{ROUTE}/" not in html:raise RuntimeError("Academy or resources discovery absent")
    print("AI Product Builder: 6 deep readings, 6 steps, 8-field blueprint, simulated civic UI, QA checklist and 10 quiz questions PASS")

def publish(site:Path):
    if not (site/"it/academy/index.html").is_file():raise RuntimeError("Academy missing")
    for src,fn in ((STYLE,"centroni-city-course.css"),(SCRIPT,"centroni-city-course.js")):
        if not src.is_file():raise RuntimeError("Course source missing "+str(src))
        (site/"assets").mkdir(parents=True,exist_ok=True)
        shutil.copy2(src,site/"assets"/fn)
    build_page(site)
    add_discovery(site)
    verify(site)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--site",required=True,type=Path)
    p.add_argument("--verify-only",action="store_true")
    a=p.parse_args()
    verify(a.site) if a.verify_only else publish(a.site)
