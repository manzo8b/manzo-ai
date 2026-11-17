# AI Teaching Lab · Audit di copertura delle cinque competenze

**Data:** 17 novembre 2026  
**Ambito:** repository \`manzo8b/manzo-ai\`, ramo \`main\` (verificato prima della stesura)  
**Tipo:** audit pedagogico-editoriale e strategia di integrazione; **non** attestato di qualità scientifica, conformità normativa, certificazione o prova sul campo  
**Stato:** proposta di miglioramento, **senza modifiche al corso pubblico** in questa PR

## 1 · Quesito di audit

Verificare se il corso «Intelligenza artificiale e didattica applicata» sviluppi davvero, nelle **letture**, nei **laboratori**, nella **valutazione**, nel **kit di risorse** e nel **vocabolario**, le cinque competenze professionali:

1. Intelligenza Artificiale per la didattica: conoscere, valutare e scegliere gli strumenti più efficaci
2. Dentro l’Intelligenza Artificiale: comprendere i meccanismi dell’apprendimento automatico
3. Creatività digitale e Intelligenza Artificiale: progettare contenuti multimediali per l’apprendimento
4. Didattica personalizzata e Intelligenza Artificiale: strategie innovative per la valutazione e l’inclusione
5. Ambienti digitali intelligenti: progettare esperienze di apprendimento interattive e coinvolgenti

**Criteri applicati.** Una competenza è «trattata in modo solido» quando esistono simultaneamente: (A) spiegazione accessibile e accurata; (B) almeno un esempio svolto e corretto; (C) un laboratorio con obiettivo, consegna, materiali sintetici, output e controlli; (D) verifica osservabile; (E) voce/e nel vocabolario e (F) una fonte esterna pertinente. La mera menzione di una parola **non** vale come competenza insegnata.

## 2 · Materiali effettivamente esaminati

- \`editorial/learning/ai-teaching-lab/it/course.json\` — obiettivi dichiarati, struttura e fonti dei 5 moduli
- \`editorial/learning/ai-teaching-lab/it/narrative.json\` — narrazioni e **10 laboratori** con passi, prompt, esempi, controlli
- \`editorial/learning/ai-teaching-lab/it/module-01.md\` … \`module-05.md\` — testo delle 5 lezioni integrali
- \`editorial/learning/ai-teaching-lab/it/glossary.json\` — **47 termini**
- \`editorial/learning/ai-teaching-lab/it/assessment-bank.json\` — cinque banche di verifiche e 5 cruciverba
- \`editorial/learning/ai-teaching-lab/it/scenarios.json\` — scelte simulate ramificate
- \`editorial/learning/ai-teaching-lab/preview/index.html\` — 11 risorse esterne nel «Kit professionale»
- \`editorial/learning/ai-teaching-lab/README.md\` — vincoli di pubblicazione, privacy e stima di durata

Questo è un audit dei **contenuti presenti nel repository**, non una misurazione dell'apprendimento o un collaudo in classe. Il corso è pubblico, libero, non accreditato; nessun risultato sul campo è implicato.

## 3 · Matrice di copertura

| Area professionale | Letture | Laboratori | Verifiche | Risorse dedicate | Vocabolario | Giudizio |
| --- | --- | --- | --- | --- | --- | --- |
| 1. Valutazione e scelta degli strumenti IA | Parziale · obiettivi prima dello strumento | Parziale · confronto IA/no IA | Presente · go/no-go | Presente DigCompEdu, ma nessuna guida comparativa | Parziale · prompt, output, rischio | **Da completare** |
| 2. Apprendimento automatico, meccanismi e limiti | Minimo · LLM, regolarità apprese, token | Assente · nessuna prova train/test | Obiettivo nel \`course.json\`, prova specifica debole | Assenti ML Crash Course e dimostrazione pratica | Mancano dataset, etichette, training, test, overfitting, generalizzazione | **Lacuna prioritaria** |
| 3. Creatività e prodotti multimediali | Buona introduzione a carico cognitivo e accessibilità | Presenti micro-kit clima + script podcast, ma artefatti dimostrativi limitati | Presente revisione e portfolio | Presenti CAST e DigCompEdu; manca guida specifica alla produzione | Presenti licenza, alt text, trascrizione, micro-kit | **Buona base, da rendere più operativa** |
| 4. Valutazione, inclusione e personalizzazione | Solida base UDL e formativa | Presenti prove equivalenti e feedback su esempi sintetici | Presente rubrica e revisione | CAST, EEF, DigCompEdu | UDL, accessibilità, feedback, rubrica, metacognizione | **Area più matura** |
| 5. Esperienze interattive e ambienti intelligenti | Tutor socratico, supervisione e sicurezza | Presente progetto di tutor e test critici, assente costruzione completa di percorso ramificato | Scenari e quiz interattivi locali presenti | Mancano authoring e specifiche learning design (es. H5P) | Tutor socratico, fallback, test; mancano LMS, branching, adattività | **Da completare** |

### 3.1 · Prova forte per la lacuna sul machine learning

Nelle cinque lezioni Markdown pubblicate non compaiono le espressioni \`apprendimento automatico\`, \`machine learning\`, \`dataset\`, \`overfitting\`, \`set di test\` o \`apprendimento supervisionato\`. Il modulo 01 accenna all’«addestramento» del modello linguistico; il modulo 02 spiega bene allucinazioni, attendibilità e fonti, ma **non insegna una sequenza dati → training → inferenza → valutazione di esempi nuovi**.

**Disallineamento interno:** \`course.json\`, negli esiti del modulo 02, promette di descrivere generazione di token e ruolo del contesto, ma non segue una lezione/laboratorio che dimostri esplicitamente come funziona l'apprendimento automatico. La classificazione con un piccolo modello supervisionato e la generazione di testo con un LLM vanno spiegate **come due esperienze diverse**; non è corretto far credere che «addestrare un classificatore in classe» riproduca il funzionamento completo di ChatGPT.

### 3.2 · Distinzione da preservare nell'area 5

MANZO AI usa **scenari ramificati con scelte e feedback locali**. Questa è **interattività pedagogica deterministica**. Non equivale di per sé a una piattaforma che adatta il percorso a dati del discente tramite modelli IA. Il corso deve **insegnare** questa distinzione e non applicare etichette come «tutor intelligente» a qualsiasi quiz.

## 4 · Piano di integrazione senza creare altri cinque moduli

Rimangono **cinque moduli** con i titoli già approvati e un filo narrativo continuo. Le cinque aree professionali diventano **competenze trasversali visibili**, non cinque nuovi corsi scollegati.

### Modulo 01 · Insegnare nell'era dell'intelligenza artificiale
**Area 1: conoscere, valutare e scegliere gli strumenti più efficaci**

**Aggiunta teorica:** differenza fra assistente generativo generalista, assistente centrato sui documenti, creatore multimediale e autore di attività interattive. La categoria è più importante del marchio.

**Nuovo laboratorio nel percorso esistente:** «Quale strumento serve davvero?». Il docente riceve 3 problemi scolastici sintetici e confronta **tre categorie** di strumenti più un'alternativa senza IA. Compila una **scheda decisionale** su: obiettivo formativo, correttezza delle bozze, trasparenza e controllo, accessibilità, dati/privacy/autorizzazioni, licenze, costi e tempo completo comprensivo di revisione. Le limitazioni su dati di minori e policy scolastiche sono **condizioni eliminatorie**, non punti negoziabili a compensazione.

**Evidenza/valutazione:** tabella argomentata con scelta, motivazioni, almeno un motivo per rifiutare la tecnologia e un test sulla qualità di due output fittizi.

**Risorsa:** approfondimento DigCompEdu 2.1 (selezione delle risorse digitali) e quadro UNESCO sulle competenze IA per docenti, già presenti nel kit.

### Modulo 02 · Pensiero critico e informazioni affidabili
**Area 2: come un modello può apprendere, generalizzare e sbagliare**

**Aggiunta teorica imprescindibile:** apprendimento automatico vs IA generativa; dati, esempi, etichette, modello, addestramento, dati mai visti, test, classificazione, previsione, generalizzazione, overfitting e bias. Distinguere in seguito l'inferenza di un classificatore dalla generazione testuale di un modello linguistico; spiegare token e contesto con linguaggio semplice, senza algebra avanzata.

**Nuovo laboratorio**, anche senza software: «Insegniamo a una macchina a distinguere due categorie». Usare 10 immagini/descrizioni **inventate** di oggetti (non foto di alunni), definire etichette, conservare 4 casi nuovi per la prova, annotare false classificazioni e cambiare il campione. Variante facoltativa con [Teachable Machine di Google](https://teachablemachine.withgoogle.com/) usando soltanto esempi e immagini non identificabili. **Mai chiedere foto, audio, pose o altre informazioni personali di minori.**

**Evidenza/valutazione:** schema «quello che il modello ha visto / quello che non ha visto», tabella con successi ed errori, spiegazione dei limiti; domanda su come una classificazione superficiale differisca da un LLM che produce testi.

**Risorse da aggiungere:**
- [Google Machine Learning Crash Course, in italiano](https://developers.google.com/machine-learning/crash-course?hl=it)
- [Set di dati, generalizzazione e overfitting](https://developers.google.com/machine-learning/crash-course/overfitting?hl=it)
- [Google Teachable Machine](https://teachablemachine.withgoogle.com/)

### Modulo 03 · Progettare materiali che fanno imparare
**Area 3: creatività digitale e contenuti multimediali**

**Aggiunta teorica:** progettazione dell'esperienza multimediale prima del prompt; storyboard, narrazione, sovraccarico cognitivo, principi di accessibilità e diritti/licenze. Chiarire che la fedeltà all'obiettivo didattico conta più degli effetti grafici.

**Laboratorio:** ricavare **uno stesso concetto** da una fonte controllata in tre formati diversi: breve serie di slide, script audio + trascrizione, piccola attività interattiva. Confrontare cosa si comprende meglio con ciascuno e creare una nota «cosa ho controllato e modificato».

**Evidenza/valutazione:** micro-kit riutilizzabile con storyboard e traccia di revisione. Usare come **caso di studio autentico** il podcast e le slide originali già ospitati nel corso, distinguendo l'artefatto dell'autore dall'analisi didattica.

**Risorsa da aggiungere:** [Commissione europea — Digital education content: guidelines for teachers](https://education.ec.europa.eu/focus-topics/digital-education/actions/plan/digital-education-content-guidelines-and-framework) e manuale di [H5P Interactive Video](https://h5p.org/interactive-video).

### Modulo 04 · Una scuola che include e fa progredire
**Area 4: inclusione, differenziazione e valutazione formativa**

**Preservare la struttura esistente**, già forte sul piano degli esempi: tre modalità di mostrare la stessa competenza, una rubrica coerente, feedback specifico e nuova prova.

**Miglioramento mirato:** progettare **tre itinerari di supporto** per differenti esigenze didattiche senza trasformare descrizioni di performance in diagnosi; un esercizio di *feedback che cambia il prossimo passo* e un confronto tra raccomandazioni automatiche e scelta umana.

**Evidenza/valutazione:** scheda obiettivo comune → barriere → opzioni → rubrica → evidenza → feedback → prossima attività. Se si propone un percorso «adattivo», dichiarare se usa **regole didattiche esplicite** oppure una IA vera, e quali dati richiederebbe. Nessun trattamento reale di dati individuali degli studenti nel prototipo.

**Risorse:** CAST UDL 3.0, EEF feedback e DigCompEdu sono già nel kit. Non duplicarle.

### Modulo 05 · Tutor intelligenti, persone responsabili
**Area 5: ambienti digitali interattivi e apprendimento coinvolgente**

**Aggiunta teorica:** anatomia essenziale di un'esperienza formativa: obiettivi, orientamento, risorsa, interazione, decisione, feedback, ripasso, verifica, uscita e piano alternativo. Distinzione fra sito di contenuti, LMS, quiz, scenario ramificato, tutor IA e personalizzazione realmente data-driven.

**Nuovo laboratorio:** «Progetta un percorso interattivo di 10 minuti». Disegnare uno storyboard con **tre scelte**, feedback e un'attività di recupero, usando i dati fittizi del corso. Variante **no-code** con [H5P Branching Scenario](https://h5p.org/branching-scenario) o simulazione locale MANZO AI. Il prototipo deve poter funzionare senza servizi esterni e senza registrare dati.

**Evidenza/valutazione:** mappa del percorso, criteri di feedback, alternativa accessibile, sei test di sicurezza del tutor, distinzione tecnica fra *branching regolato* e *adattività IA*.

**Risorsa da aggiungere:** [H5P — Branching Scenario](https://h5p.org/branching-scenario) e [tutorial ufficiale H5P](https://h5p.org/documentation/for-authors/tutorials).

## 5 · Nuove voci consigliate per il vocabolario

Il vocabolario attuale ha **47 voci**, ben costruite per pedagogia, prompt, fonti, UDL, privacy e supervisione. **Non contiene** le parole tecniche indispensabili per l'area 2 e alcune per l'area 5. Aggiungere **15 definizioni concise, con esempio scolastico**, senza gergo superfluo:

| Nuova voce | Collocazione proposta |
| --- | --- |
| Apprendimento automatico / machine learning | Fondamenti IA |
| Modello IA | Fondamenti IA |
| Set di dati / dataset | Fondamenti IA |
| Dato di addestramento | Fondamenti IA |
| Etichetta (classificazione) | Fondamenti IA |
| Apprendimento supervisionato | Fondamenti IA |
| Addestramento e inferenza | Fondamenti IA |
| Set di test | Fondamenti IA |
| Generalizzazione | Fondamenti IA |
| Overfitting / sovradattamento | Fondamenti IA |
| Classificazione vs generazione | Fondamenti IA |
| Multimodalità | Prompt e produzione |
| Storyboard didattico | Didattica e valutazione |
| Scenario ramificato / branching | Didattica e valutazione |
| LMS e apprendimento adattivo | Didattica e valutazione |

**Criterio terminologico:** ogni voce presenta definizione, differenza dal termine vicino, esempio con dati sintetici e fonte consultabile. «LMS e apprendimento adattivo» possono successivamente essere separati se la sezione cresce. Non usare *adattivo* come sinonimo di *interattivo*.

## 6 · Centro risorse: esistente vs integrazione

**Già presenti nel «Kit professionale» (11 collegamenti):** linee guida MIM 2025, etica IA UE, UNESCO competenze IA per docenti e studenti, Garante scuola e parere 2026, DigCompEdu, AI Act alfabetizzazione, CAST UDL 3.0, TALIS Italia 2024, EEF feedback.

**Lacune del repertorio:** mancano una fonte progressiva sui meccanismi del machine learning, una dimostrazione accessibile dell'addestramento di un classificatore, una fonte dedicata alla produzione multimediale verificabile, un authoring per interazioni ramificate.

**Strategia UX:** mantenere **quattro risorse essenziali** in vista. Aggiungere soltanto 5–6 schede pertinenti nella parte espandibile, etichettate «Fondamenti IA», «Strumenti e progettazione», «Multimedia e interattività». Ogni collegamento avrà **perché aprirlo**, **cosa si impara** e **lingua**; evitare di presentare un prodotto privato come obbligatorio o approvato dal Ministero. Verificare condizioni d'uso e protezione dati alla data di utilizzo.

## 7 · Ricaduta sui materiali di verifica e sull'esperienza Coursera-style

Per ogni nuova competenza aggiunta:

- **Lettura di approfondimento:** motivazione narrativa e spiegazione rigorosa ma accessibile
- **Un esempio commentato:** la prova del perché un risultato è corretto, parziale o errato
- **Laboratorio:** istruzione esplicita «che cosa fai», input fittizi, prompt completo o alternativa senza IA, output atteso e revisione
- **Autoverifica:** una domanda diagnostica, una prova applicativa, una motivazione della scelta; non solo memorizzazione
- **Portfolio:** un artefatto concreto utilizzabile nel proprio lavoro, senza richieste di caricamento sul sito
- **Collegamento al modulo seguente:** domanda che trasferisce la competenza acquisita
- **Glossario e fonte:** parola tecnica spiegata dove serve, con rimando finale

Non inserire «lezione video da 60 minuti» o «test adattivo» se non esiste davvero. Non inventare progressi, LMS, tutoring in tempo reale, certificazioni o punteggi professionali.

## 8 · Roadmap ordinata

| Priorità | Intervento | File / aree candidate | Verifica di accettazione |
| --- | --- | --- | --- |
| P0 | Fondamenti ML + prova train/test nel Modulo 02 | narrative.json, module-02.md, course.json, assessment-bank.json | Il docente sa distinguere training, test, classificazione e LLM in una prova pratica |
| P0 | Matrice di selezione degli strumenti nel Modulo 01 | narrative.json, module-01.md, course.json, assessment-bank.json | Una scelta IA/no IA motivata con criteri espliciti e condizioni di esclusione |
| P1 | Percorso interattivo completo nel Modulo 05 | narrative.json, module-05.md, preview/app.js e relativi CSS/test | Percorso di 3 diramazioni, feedback e fallback, dichiarato rule-based se lo è |
| P1 | Multimedialità originale e storyboard nel Modulo 03 | narrative.json, module-03.md, preview, fonti media | Tre formati coerenti e accessibili dello stesso concetto, con revisione tracciata |
| P1 | Differenziazione e feedback per itinerari nel Modulo 04 | narrative.json, module-04.md, assessment-bank.json | Stessi obiettivi e criteri, opzioni diverse, nessuna diagnosi IA |
| P1 | Glossario tecnico 15 voci | it/glossary.json, preview/app.js | Definizioni chiare, esempi, ricerca, filtri, test su mobile |
| P1 | Kit risorse 5–6 nuove fonti | preview/index.html, relativi CSS/test | URL verificati, raggruppamento, link sicuri e fonti coerenti |
| P2 | Audit finale trasversale e pilota | tests, docs, traccia per docente | Tutti i 5 esiti dichiarati hanno lettura, prova, rubrica, fonte e voce di glossario |

### Quantità di lavoro e correttezza delle 20 ore

Il corso attuale stima **5 × 4 ore = 20 ore**, senza validazione in una prova reale. Non sommare semplicemente cinque nuovi laboratori alla durata mantenendo il valore «20 ore»: sostituire parte delle attività esistenti o **ricalcolare apertamente** il carico dopo un pilota. Possibile scelta: mantenere 20h per la versione di base e proporre approfondimenti **facoltativi**, etichettati come tali, senza manipolare la promessa formativa.

### Stato della pubblicazione

Questo audit non è un rilascio delle attività proposte. Per il momento non modifica nessuna pagina pubblica, le cinque lezioni, i voti, le identità, i dati, il backend Supabase o la formazione a pagamento. Il lavoro di sviluppo dovrà seguire il ramo di progetto e superare i test già usati per la versione pubblica.

### Osservazione di coerenza editoriale

Nel `course.json` il corso risulta ancora contrassegnato con `status: editorial_draft` e `published: false`, mentre il publisher GitHub Pages lo distribuisce pubblicamente. **Non correggere automaticamente tali campi**: potrebbero indicare lo stato della validazione pedagogica e sono richiamati nei test. Occorre separare e documentare chiaramente *disponibilità pubblica della beta*, *maturità editoriale* e *validazione con docenti* prima di modificare lo schema.

## 9 · Riferimenti esterni suggeriti per l'espansione

1. UNESCO (2024), *AI competency framework for teachers*: https://www.unesco.org/en/articles/ai-competency-framework-teachers
2. Commissione europea / JRC, *DigCompEdu*: https://joint-research-centre.ec.europa.eu/scientific-activities/key-competences-lifelong-learning/digcompedu_en
3. Google Developers, *Machine Learning Crash Course* (IT): https://developers.google.com/machine-learning/crash-course?hl=it
4. Google, *Teachable Machine*: https://teachablemachine.withgoogle.com/
5. Commissione europea, *Digital education content guidelines*: https://education.ec.europa.eu/focus-topics/digital-education/actions/plan/digital-education-content-guidelines-and-framework
6. H5P, *Branching Scenario*: https://h5p.org/branching-scenario
7. H5P, *Interactive Video*: https://h5p.org/interactive-video
8. CAST, *UDL Guidelines 3.0*: https://udlguidelines.cast.org/

Le fonti esterne sono **riferimenti da citare e consultare**, non materiale da riprodurre integralmente dentro MANZO AI senza licenza. L'eventuale uso di servizi e strumenti con studenti richiederà valutazione istituzionale e protezione dei dati personali.
