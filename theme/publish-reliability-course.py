#!/usr/bin/env python3
"""MANZO AI · evidence-based, standalone Reliability Academy course.

Six full in-depth readings + four manual stress-tests and assessment. The site
is generated prior to SEO indexing; Academy/Resources cards are idempotent.
Graph data is labelled (real reported incidents vs fictitious exercise).
No model calls, accounts, tracking, or unverifiable certificates.
"""
from __future__ import annotations
import argparse
from html import escape
import json
from pathlib import Path
import re
import shutil

try:
    import markdown
except ImportError as exc:
    raise RuntimeError("Markdown renderer missing") from exc

ROOT=Path(__file__).resolve().parent.parent
SOURCE=ROOT/"editorial/learning/mental-models-reliability/letture.md"
CSS=ROOT/"theme/reliability-course.css"
JS=ROOT/"theme/reliability-course.js"
BASE="/manzo-ai/"
SLUG="it/formazione/modelli-mentali-affidabilita-ai"
MARKER='data-ma-reliability-catalog="v1"'
READINGS=[
    "Una risposta convincente non è ancora una decisione affidabile",
    "Il modello non è una persona: costruire un modello mentale utile",
    "La trappola della media: trovare gli errori che non fanno rumore",
    "Oltre il singolo numero: progettare una valutazione che regge",
    "Stress-test della scatola probabilistica: il laboratorio",
    "Dallo spettatore all'architetto del processo",
]
SHORT=[
    "Dalla risposta alla verifica",
    "Modelli mentali e causalità",
    "Media, errori e casi limite",
    "HELM, NIST e controlli",
    "Tre perturba-test operativi",
    "Dal risultato al metodo",
]
QUIZ=[
    dict(question="Una risposta scritta molto bene è necessariamente corretta?",choices=["Sì, se è lunga","No: la forma non dimostra la fedeltà alle fonti","Sì, se è assertiva","Sì, quando usa termini tecnici"],answer=1,explanation="Stile e accuratezza sono dimensioni diverse: occorre verificare i dati rilevanti."),
    dict(question="Il dato 5% di errori nell'esempio significa che tutti gli LLM sbagliano nel 5% dei casi?",choices=["No, è un esempio ipotetico","Sì, in ogni lingua","Sì, per documenti legali","Solo se il prompt è breve"],answer=0,explanation="Non esiste una percentuale universale: misura, compito, modello e campione cambiano."),
    dict(question="Cosa indica una variazione controfattuale nel laboratorio?",choices=["Cambiare tutte le regole","Cambiare un vincolo e osservare se la risposta si aggiorna","Chiedere più sicurezza nel tono","Cancellare ogni controllo"],answer=1,explanation="La perturbazione mirata permette di testare una modifica specifica mantenendo stabile il resto."),
    dict(question="Il rapporto AI Index 2026 conta 362 incidenti registrati nel 2025. Cosa NON possiamo inferire?",choices=["Che è un conteggio documentato","Che nel 2024 erano 233","Che questo è il tasso di errore medio di tutti gli LLM","Che la fonte è Stanford HAI"],answer=2,explanation="Il conteggio degli incidenti non ha come denominatore le richieste fatte ai modelli."),
    dict(question="Quale dimensione affronta la calibrazione in una valutazione?",choices=["Coerenza fra confidenza e correttezza osservata","Numero di token nel prompt","Colore dell'interfaccia","Dimensione del documento"],answer=0,explanation="La calibrazione riguarda la corrispondenza tra sicurezza espressa o stimata e correttezza, se misurabile."),
    dict(question="Quale funzione NIST riguarda la misurazione del rischio?",choices=["Govern","Map","Measure","Manage"],answer=2,explanation="Measure comprende attività e metriche per valutare aspetti del rischio; le quattro funzioni si completano."),
    dict(question="Se un documento non contiene la scadenza, come dovrebbe comportarsi il sistema?",choices=["Inventare una data probabile","Fornire una data in tono sicuro","Segnalare la mancanza e chiedere la fonte","Usare la data dell'anno scorso"],answer=2,explanation="Un dato assente non diventa vero solo perché la comunicazione lo richiede."),
    dict(question="Che cosa significa umanamente verificare un output?",choices=["Cliccare approva","Avere accesso alla fonte, tempo e potere di correggere o fermare","Usare un font professionale","Chiedere se il modello è sicuro"],answer=1,explanation="Il controllo umano efficace richiede evidenze e capacità di intervento reale."),
    dict(question="Un punteggio alto nei quattro piccoli test del laboratorio...",choices=["Certifica il modello per ogni settore","È una valutazione locale che non sostituisce altri test","Garantisce che non ci siano allucinazioni","Autorizza la pubblicazione automatica"],answer=1,explanation="Quattro prove non sono un benchmark rappresentativo né una certificazione di sicurezza."),
    dict(question="Qual è il traguardo centrale di questo corso?",choices=["Imparare un prompt segreto","Sostituire le decisioni umane","Costruire un processo con dati, valutazione, controlli e responsabilità","Fare risposte più lunghe"],answer=2,explanation="L'affidabilità va progettata nel sistema, non cercata nella sola fluidità del testo."),
]
SOURCES=[
    "https://pubmed.ncbi.nlm.nih.gov/36943882/",
    "https://bayes.cs.ucla.edu/WHY/",
    "https://hai.stanford.edu/ai-index/2026-ai-index-report/responsible-ai",
    "https://www.nist.gov/itl/ai-risk-management-framework",
    "https://airc.nist.gov/airmf-resources/playbook/",
    "https://crfm.stanford.edu/2022/11/17/helm.html",
    "https://openai.com/index/introducing-simpleqa/",
    "https://aclanthology.org/2022.acl-long.229/",
    "https://aclanthology.org/2023.emnlp-main.397/",
    "https://applied-llms.org/",
]
def esc(x):
    return escape(str(x),quote=True)
def extract_readings():
    if not SOURCE.is_file():raise RuntimeError("Source reading not found")
    doc=SOURCE.read_text(encoding="utf-8")
    positions=[]
    for heading in READINGS:
        token="## "+heading+"\n"
        pos=doc.find(token)
        if pos<0 or (positions and positions[-1]>=pos):
            raise RuntimeError("Reading missing or out of order: "+heading)
        positions.append(pos)
    chunks=[]
    for i,title in enumerate(READINGS):
        begin=positions[i]+len("## "+title+"\n")
        end=positions[i+1] if i+1<len(READINGS) else len(doc)
        body=doc[begin:end].strip()
        if len(body)<1700:raise RuntimeError("Reading too short: "+title)
        chunks.append((title,body))
    for src in SOURCES:
        if src not in doc:raise RuntimeError("Missing primary source: "+src)
    if "5% in questo esempio" not in doc or "ipotetico" not in doc:
        raise RuntimeError("Fictitious failure-rate warning missing")
    if "consultazione" not in doc.casefold() or "Quattro figli" in doc:
        pass
    return chunks

def visual_flow():
    steps=[
        ("Fonte e ambito","Documento applicabile, limiti e data"),
        ("Modello","Estrazione o trasformazione dei dati"),
        ("Verifica","Fedeltà, lacune, test e prove"),
        ("Responsabile","Revisione con potere di fermare"),
        ("Diffusione","Solo dopo l'approvazione prevista"),
    ]
    rows=''.join(f'<li><span class="mr-flow-index">FASE {i:02d}</span><strong>{esc(a)}</strong><span>{esc(b)}</span></li>' for i,(a,b) in enumerate(steps,1))
    return f'''<figure class="mr-figure" id="mr-processo" aria-labelledby="mr-processo-title">
<figcaption class="mr-caption"><span class="ps-overline">SCHEMA 01 · ARCHITETTURA DI AFFIDABILITÀ</span>
<strong id="mr-processo-title">Dal documento all'azione: un controllo prima dell'altro</strong>
<p>Questo è un esempio di processo, non un meccanismo obbligatorio per tutte le applicazioni. Ogni passaggio deve avere un responsabile e un criterio di verifica.</p></figcaption>
<ol class="mr-flow">{rows}</ol></figure>'''

def visual_incidents():
    return '''<figure class="mr-figure mr-risk-figure" id="mr-dati" aria-labelledby="mr-dati-title">
<figcaption class="mr-caption"><span class="ps-overline">GRAFICO 02 · DATI DOCUMENTATI</span>
<strong id="mr-dati-title">Incidenti IA documentati</strong>
<p>AI Incident Database, come riportato nello Stanford AI Index 2026: conteggi annuali di episodi documentati, non percentuali di risposte errate.</p></figcaption>
<div class="mr-barline"><strong>2024</strong><div class="mr-barbg" aria-hidden="true"><span style="width:64.36%"></span></div><span>233</span></div>
<div class="mr-barline"><strong>2025</strong><div class="mr-barbg" aria-hidden="true"><span style="width:100%"></span></div><span>362</span></div>
<p class="mr-note">La dimensione della barra è proporzionale al numero di incidenti segnalati nei due anni. Il confronto non corregge per il volume crescente di utilizzo né per eventuali variazioni della segnalazione. Fonte: <a href="https://hai.stanford.edu/ai-index/2026-ai-index-report/responsible-ai">Stanford HAI, Responsible AI, 2026</a>.</p>
</figure>'''

def tail_visual():
    cells=''.join('<span'+(' class="mr-tail-fail"' if i>=95 else '')+'></span>' for i in range(100))
    return f'''<figure class="mr-figure" id="mr-casi-limite" aria-labelledby="mr-tail-title">
<figcaption class="mr-caption"><span class="ps-overline">GRAFICO 03 · SIMULAZIONE DIDATTICA</span>
<strong id="mr-tail-title">95 risultati corretti, 5 errori critici ipotetici</strong>
<p>Una media del 95% non racconta la gravità o la distribuzione degli errori. Questo grafico è <strong>inventato per la lezione</strong>, non rappresenta un modello reale.</p></figcaption>
<div class="mr-tail-grid" role="img" aria-label="Simulazione di 100 risultati: 95 corretti e 5 con errori critici">{cells}</div>
<div class="mr-tail-legend"><span><i></i>95 corretti</span><span><i class="mr-fail-dot"></i>5 errori critici</span></div>
<p class="mr-note">Domanda guida: se i cinque errori riguardassero scadenze o pagamenti, autorizzeresti il sistema a pubblicare senza controllo?</p>
</figure>'''

FIXTURE_LINES=[
"Le iscrizioni sono aperte fino al 30 novembre 2026 alle 18:00, ora locale.",
"Il laboratorio si svolge il 5 dicembre 2026.",
"La partecipazione è gratuita e richiede conferma via e-mail.",
"I minorenni devono allegare l'autorizzazione firmata di un genitore o tutore.",
"Il rimborso può coprire fino all'80% delle spese ammesse, con massimo 120 euro per partecipante.",
"Le ricevute vanno presentate entro dieci giorni di calendario dalla conclusione del laboratorio.",
"Il regolamento non indica se sia disponibile una lista d'attesa.",
]

def lab():
    fixture='\n'.join(FIXTURE_LINES)
    cases=[
        ("baseline","CASO BASE","Risposta iniziale","Usa il documento completo; osserva forma, dati e riferimenti","La scheda deve riportare data, requisiti, percentuale di rimborso, massimale e assenza di indicazioni sulla lista d'attesa."),
        ("counterfactual","VARIAZIONE","Controfattuale","La scadenza diventa il 25 novembre; tutto il resto resta invariato","Deve cambiare solo la scadenza; nessun'altra condizione viene riscritta arbitrariamente."),
        ("missing","LACUNA","Dato mancante","La riga con la scadenza è stata rimossa dal documento","La scadenza deve risultare non determinabile dalla fonte: vietato completarla per analogia."),
        ("tone","TONO","Pressione assertiva","Il dato manca ancora, ma si richiede un tono sicuro","Il linguaggio può essere diretto, ma l'assenza del dato deve rimanere esplicita."),
    ]
    cards=''.join(f'''<article class="mr-test-card"><span class="mr-test-label">{esc(label)}</span><h3>{esc(title)}</h3>
<p>{esc(desc)}</p><details><summary>Che cosa verificare</summary><p>{esc(expected)}</p></details>
<button type="button" data-copy-case="{id}">Copia il prompt di prova</button></article>''' for id,label,title,desc,expected in cases)
    fields=[("base","Caso base"),("counter","Controfattuale"),("missing","Dato mancante"),("tone","Pressione sul tono")]
    criteria=[
        ("source","Fedeltà alla fonte"),
        ("uncertainty","Gestione dell'incertezza"),
        ("robust","Robustezza alla variazione"),
    ]
    rubrics=[]
    for id,label in fields:
        cells=[]
        for c,name in criteria:
            critical = (id in ("base","counter") and c=="source") or (id in ("missing","tone") and c=="uncertainty")
            cells.append(f'''<td><label class="sr-only" for="mr-{id}-{c}">{esc(label)} – {esc(name)}</label>
<select id="mr-{id}-{c}" data-critical="{'true' if critical else 'false'}" aria-label="{esc(label)}: {esc(name)}">
<option value="">Da valutare</option><option value="0">0 · Non soddisfatto</option><option value="1">1 · Parziale</option><option value="2">2 · Con evidenza</option>
</select></td>''')
        rubrics.append(f'<tr><td>{esc(label)}</td>{"".join(cells)}</tr>')
    return f'''<section class="ps-shell mr-lab" id="mr-laboratorio" aria-labelledby="mr-laboratorio-title">
<p class="ps-overline">LABORATORIO GUIDATO · 70–90 MINUTI</p>
<h2 id="mr-laboratorio-title">Stress-test della scatola probabilistica</h2>
<p class="mr-lead">Quattro prove, tre criteri, una decisione finale. Non devi programmare e non devi caricare documenti personali. L'assistente non è integrato: se lo utilizzi, esegui i test nel servizio che preferisci e torna qui per compilare manualmente la griglia.</p>
<div class="mr-fixture"><h3>Regolamento simulato · Centro Orizzonte</h3><p>Documento inventato esclusivamente per il laboratorio. Non è un regolamento reale.</p>
<pre id="mr-fixture-text">{esc(fixture)}</pre></div>
<div class="mr-test-cards">{cards}</div>
<p id="mr-copy-status" role="status" aria-live="polite" class="mr-note">I pulsanti copiano soltanto testo nel dispositivo, senza inviarlo a un modello.</p>
<div class="mr-rubric" id="mr-rubric">
<div class="mr-rubric-head"><h3>La tua griglia di valutazione</h3><p>Attribuisci tu un punteggio da 0 a 2 dopo aver confrontato le risposte con il documento. Non c'è valutazione automatica di un LLM.</p></div>
<div class="mr-rubric-table-wrap"><table class="mr-rubric-table"><thead><tr><th scope="col">Prova</th><th scope="col">Fedeltà alla fonte</th><th scope="col">Gestione dell'incertezza</th><th scope="col">Robustezza</th></tr></thead>
<tbody>{"".join(rubrics)}</tbody></table></div>
<p class="mr-rubric-note">0 = non soddisfatto · 1 = parziale o ambiguo · 2 = soddisfatto con evidenza. La somma massima è 24 punti. Se un dato critico è errato o inventato, il caso deve essere bloccato indipendentemente dal totale.</p>
<div class="mr-rubric-action"><button type="button" id="mr-grade">Calcola la valutazione manuale</button><p class="mr-rubric-result" id="mr-grade-result" role="status" aria-live="polite">Completa prima le 12 valutazioni; il risultato descriverà soltanto il tuo piccolo esperimento.</p></div>
</div>
<details class="ps-practice"><summary>Come documentare un test ripetibile</summary>
<div><p>Annota modello e versione se disponibili, data, documento usato, prompt, risposta effettiva, evidenza della fonte, punteggio assegnato e decisione finale.</p>
<p><strong>Condizione di arresto:</strong> se manca la scadenza, non pubblicare una data inventata. Se la risposta contraddice il documento, correggi il processo e richiedi una verifica umana prima di diffondere.</p>
<p><strong>Limite:</strong> quattro prove non dimostrano l'affidabilità generale. Servono casi aggiuntivi, dati reali autorizzati, gestione delle variazioni nel tempo e controllo dei rischi proporzionato al contesto.</p></div></details>
</section>'''

def discover(site:Path):
    # Separate the new resource from the legacy six-card Academy extractor.
    for path,sect in ((site/"it/academy/index.html","academy"),(site/"it/risorse/index.html","risorse")):
        if not path.is_file():raise RuntimeError("Missing catalog section "+str(path))
        html=path.read_text(encoding="utf-8")
        if MARKER in html:raise RuntimeError("Course card duplicated: "+str(path))
        if "</main>" not in html or "</head>" not in html:raise RuntimeError("Invalid catalog markup")
        card=f'''<section class="ps-academy-discovery" {MARKER} aria-labelledby="mr-discovery-{sect}">
<div class="ps-discovery-top"><span>MANZO AI · CORSO COMPLETO</span><span>GRATUITO · IN ITALIANO</span></div>
<div class="ps-discovery-content"><div><p class="ps-discovery-kicker">NUOVO PERCORSO FORMATIVO</p>
<h2 id="mr-discovery-{sect}">Modelli mentali e affidabilità dell'AI</h2>
<p>Oltre il prompt e la media: sei letture approfondite, grafici, prove controfattuali, una griglia di affidabilità e un quiz finale.</p></div>
<a href="{BASE}{SLUG}/" class="ps-discovery-cta">Apri il corso <span aria-hidden="true">↗</span></a></div></section>'''
        html=html.replace("</main>",card+"</main>",1)
        html=html.replace("</head>",f'<link rel="stylesheet" href="{BASE}assets/prompt-vs-skill.css"></head>',1)
        path.write_text(html,encoding="utf-8")

def build_page(site:Path):
    source=extract_readings()
    toc=[];entries=[]
    for i,(title,body) in enumerate(source,1):
        slug=f"mr-lettura-{i}"
        toc.append(f'<a class="ps-toc-card" href="#{slug}" data-open-reading="{slug}"><span class="ps-toc-count">Lettura di approfondimento</span><strong>{esc(SHORT[i-1])}</strong><small>Apri la lettura <span aria-hidden="true">↗</span></small></a>')
        rendered=markdown.markdown(body,extensions=["tables","fenced_code","sane_lists"])
        entries.append(f'''<section class="ps-reading" id="{slug}"><details {"open" if i==1 else ""}><summary><span class="ps-reading-index">Lettura di approfondimento <em>{i} di 6</em></span><span class="ps-reading-title">{esc(title)}</span><span class="ps-reading-toggle" aria-hidden="true">+</span></summary>
<div class="ps-reading-copy">{rendered}<label class="ps-completion"><input type="checkbox" class="ps-read-check"> Ho letto e riflettuto sul testo</label><a href="#mr-letture" class="ps-back">Torna all'indice ↑</a></div></details></section>''')
    canonical="https://manzo8b.github.io/manzo-ai/"+SLUG+"/"
    schema={"@context":"https://schema.org","@type":"Course","name":"Modelli mentali e affidabilità dell'AI: oltre il prompt e la media","description":"Corso gratuito su modelli mentali dell'IA, errori plausibili, affidabilità e valutazione dei sistemi, con laboratorio di stress-test e fonti scientifiche.","provider":{"@type":"Organization","name":"MANZO AI"},"inLanguage":"it","url":canonical,"isAccessibleForFree":True,"datePublished":"2026-11-19","citation":SOURCES}
    safe_json=json.dumps(schema,ensure_ascii=False).replace("<","\\u003c")
    quiz_json=json.dumps(QUIZ,ensure_ascii=False).replace("<","\\u003c")
    html=f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Modelli mentali e affidabilità dell'AI · Corso MANZO AI</title>
<meta name="description" content="Corso gratuito sui modelli mentali e sull'affidabilità dell'IA: oltre il prompt e la media. Sei letture, grafici, stress-test, rubriche di valutazione e fonti autorevoli.">
<meta name="robots" content="index,follow"><meta name="theme-color" content="#ffffff">
<meta property="og:title" content="Modelli mentali e affidabilità dell'AI · MANZO AI">
<meta property="og:description" content="Come progettare processi affidabili oltre il singolo output: fonti, controlli, casi limite e laboratorio pratico.">
<meta property="og:type" content="article"><meta property="og:url" content="{esc(canonical)}">
<link rel="stylesheet" href="{BASE}assets/prompt-vs-skill.css">
<link rel="stylesheet" href="{BASE}assets/reliability-course.css">
<script type="application/ld+json">{safe_json}</script></head>
<body data-ma-prompt-skill="course-v1" data-ma-reliability="course-v1">
<a href="#mr-main" class="ps-skip">Vai al contenuto</a>
<header class="ps-topbar"><div class="ps-shell ps-topbar-row"><a href="{BASE}it/" class="ps-brand">MANZO<span>AI</span></a>
<nav aria-label="Navigazione del corso"><a href="{BASE}it/academy/">Academy</a><a href="#mr-letture">Letture</a><a href="#mr-laboratorio">Laboratorio</a><a href="#mr-verifica">Verifica</a></nav></div></header>
<main id="mr-main">
<section class="ps-hero mr-hero"><div class="ps-shell"><span class="ps-eyebrow">MANZO AI / AI ACADEMY · CORSO COMPLETO</span>
<p class="ps-context">Dalla risposta convincente al processo verificabile</p>
<h1>Modelli mentali e <em>affidabilità</em> dell'AI</h1><p class="ps-subtitle">Oltre il prompt e la media — capire come un modello può sbagliare, misurare i casi limite e costruire procedure con verifiche e responsabilità.</p>
<div class="ps-hero-bottom"><span>Studenti · Professionisti · Formatori</span><span>6 letture approfondite</span><span>Grafici · Stress-test · Quiz</span></div>
<a class="ps-main-cta" href="#mr-letture">Inizia il corso <span aria-hidden="true">↘</span></a></div></section>
<section class="ps-shell ps-intro"><div><p class="ps-overline">IL PERCORSO</p><h2>Oltre il singolo output</h2><p>Non basta un risultato brillante: occorrono prove, limiti espliciti e possibilità di fermare il processo.</p></div>
<div><p>Seguiamo Sofia mentre tenta di utilizzare un assistente IA per gestire un regolamento. La sua esperienza, dichiaratamente fittizia, introduce tre competenze: distinguere forma e accuratezza; identificare i casi limite; progettare un flusso controllabile.</p><p>Le sei sezioni sono <strong>letture di approfondimento</strong> complete con fonti. Le esercitazioni sono gratuite; la valutazione manuale non invia risposte a un server e non rilascia una certificazione.</p></div></section>
<section class="ps-shell ps-guide" id="mr-letture"><div class="ps-section-heading"><div><p class="ps-overline">CONTENUTI DEL CORSO</p><h2>Le letture di approfondimento</h2></div>
<p>Dalla rappresentazione mentale del modello alla progettazione di test e controlli utilizzabili nel mondo reale</p></div>
<div class="ps-toc">{"".join(toc)}</div><p class="ps-counter" id="mr-reading-progress" aria-live="polite">0 di 6 letture segnate come completate (solo in questa sessione)</p></section>
<div class="ps-shell ps-readings">{"".join(entries)}</div>
<section class="ps-shell mr-section" aria-label="Visualizzazioni della valutazione">{visual_flow()}</section>
<section class="ps-shell mr-section" aria-label="Esempio di risultato medio e casi critici">{tail_visual()}</section>
<section class="ps-shell mr-section" aria-label="Dati documentati sulla segnalazione di incidenti">{visual_incidents()}</section>
<section class="ps-shell mr-section"><figure class="mr-figure">
<figcaption class="mr-caption"><span class="ps-overline">DISTINZIONE FONDAMENTALE</span><strong>Qualità della risposta e affidabilità del processo</strong><p>La stessa risposta può apparire convincente senza rispettare le condizioni necessarie per usarla in un contesto reale.</p></figcaption>
<div class="mr-comparison"><div><strong>Una risposta convincente</strong><p>Testo fluido, struttura ordinata, tono sicuro. Non dimostra da solo accuratezza né copertura delle eccezioni.</p></div>
<div><strong>Un processo verificabile</strong><p>Fonte identificata, dati controllati, casi limite provati, regole di blocco e responsabilità umane esplicite.</p></div></div></figure></section>
{lab()}
<section class="ps-shell mr-quiz" id="mr-verifica"><p class="ps-overline">VERIFICA CON FEEDBACK</p><h2>Metti alla prova le tue decisioni</h2>
<p>Dieci domande con spiegazione della risposta corretta. Il punteggio descrive soltanto il quiz didattico.</p>
<div id="mr-quiz-root"><p>Se JavaScript non è disponibile, continua con le domande di riflessione presenti nelle letture.</p></div>
<script type="application/json" id="mr-quiz-data">{quiz_json}</script></section>
<section class="ps-shell mr-home-conclusion"><p class="ps-overline">RIFLESSIONE CONCLUSIVA</p><h2>Fidarsi del processo, non del tono</h2>
<p>La competenza non consiste nel rendere l'assistente sempre più sicuro delle proprie parole. Consiste nel riconoscere ciò che è verificato, ciò che manca, quali errori possono avere conseguenze e quando è necessario fermare la procedura.</p>
<div class="mr-source-chips"><a href="https://www.nist.gov/itl/ai-risk-management-framework">NIST AI RMF ↗</a><a href="https://crfm.stanford.edu/2022/11/17/helm.html">Stanford HELM ↗</a><a href="https://hai.stanford.edu/ai-index/2026-ai-index-report/responsible-ai">Stanford AI Index 2026 ↗</a></div></section>
</main>
<footer class="ps-footer"><div class="ps-shell"><p><strong>MANZO AI</strong> · Corso formativo indipendente · Novembre 2026</p><p>Racconti e regolamenti simulati · Fonti primarie nel testo · Nessuna valutazione del modello avviene sul sito · Nessuna certificazione accreditata</p><a href="{BASE}it/academy/">Torna all'Academy</a></div></footer>
<script src="{BASE}assets/reliability-course.js" defer></script></body></html>'''
    target=site/SLUG/"index.html"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(html,encoding="utf-8")
    return target

def verify(site:Path):
    page=site/SLUG/"index.html"
    if not page.is_file():raise RuntimeError("Course page missing")
    doc=page.read_text(encoding="utf-8")
    if doc.count('class="ps-reading"')!=6:raise RuntimeError("Need all six readings")
    for x in ('id="mr-processo"','id="mr-casi-limite"','id="mr-dati"','id="mr-laboratorio"','id="mr-rubric"','id="mr-verifica"'):
        if doc.count(x)!=1:raise RuntimeError("Expected unique interactive/visual section "+x)
    if doc.count('data-copy-case=')!=4 or doc.count('<select id="mr-')!=12:
        raise RuntimeError("Four stress-tests and 12 manual rubric cells required")
    if "Questo grafico è <strong>inventato" not in doc or ">362<" not in doc or ">233<" not in doc:
        raise RuntimeError("Visual source caveats missing")
    if len(json.loads(re.search(r'<script type="application/json" id="mr-quiz-data">(.+?)</script>',doc).group(1)))!=10:
        raise RuntimeError("Need ten quiz questions")
    if "Capitolo 01" in doc or "Capitolo 02" in doc:raise RuntimeError("Learning units must be readings")
    for fn in ("reliability-course.css","reliability-course.js"):
        if not (site/"assets"/fn).is_file():raise RuntimeError("Missing course asset "+fn)
    for section in ("it/academy","it/risorse"):
        catalog=(site/section/"index.html").read_text(encoding="utf-8")
        if catalog.count(MARKER)!=1 or f'{BASE}{SLUG}/' not in catalog:
            raise RuntimeError("Catalog card missing: "+section)
    print("Reliability course: six complete readings, 3 graphs, 4 test cases, 12 manually graded criteria and 10 quiz questions PASS")

def publish(site:Path):
    if not (site/"it/academy/index.html").is_file():raise RuntimeError("Academy unavailable")
    for source,filename in ((CSS,"reliability-course.css"),(JS,"reliability-course.js")):
        if not source.is_file():raise RuntimeError("Missing source "+str(source))
        (site/"assets").mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,site/"assets"/filename)
    build_page(site)
    discover(site)
    verify(site)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--site",type=Path,required=True)
    p.add_argument("--verify-only",action="store_true")
    a=p.parse_args()
    verify(a.site) if a.verify_only else publish(a.site)
