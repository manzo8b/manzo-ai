# MANZO AI — Home redesign · Fase 0 · Ispezione e decisioni

**Data:** 20 novembre 2026  
**Base:** brief «Brief di redesign – Home MANZO AI», v1.0, consegnato dall'autore  
**Stato:** sola ispezione e definizione del perimetro. **Nessuna modifica al codice, nessuna nuova Home distribuita, nessun cambio di URL.**  
**Ambito immediato:** solo Home italiana. EN/ES dopo validazione dell'italiano.

## 1 · Intenzione della revisione

Passare dalla Home-catalogo a una Home che **incuriosisce con una domanda riconoscibile e offre un primo passo verificabile**. La promessa editoriale proposta dal brief è:

- H1: **L’IA ti ha risposto con sicurezza. Ma è vero?**
- Sottotitolo: «Impara a fare le domande giuste, a controllare le risposte e a decidere tu.»
- CTA: **Inizia dalle basi** e **Prova una sfida di pensiero critico**

La narrazione ha priorità rispetto agli effetti grafici. Non inserire livelli, durate, risultati, certificazioni, metriche o endorsement non documentati.

## 2 · Inventario tecnico verificato sul repository

| Elemento | Origine / situazione verificata | Implicazione |
| --- | --- | --- |
| Build pubblica | `.github/workflows/deploy-pages.yml`: estrazione dell'archivio storico `site-v0.7.zip` e publisher successivi | Conservarne l'ordine fino a una migrazione distinta |
| Hero e ricerca | `theme/publish-home-conversational.py`, `theme/publish-home-curation.py` e `theme/publish-sprint1-home.py` | La modifica finale deve evitare quattro testi introduttivi concorrenti e mantenere la ricerca dove utile |
| Card storiche | `theme/publish-home-showcase.py`: **6 card prelevate dalle pagine Academy** e riutilizzate in Home | Riusare la loro anatomia; non ricreare sei schede con nuovi contenuti non verificati |
| Card aggiuntive | `publish-prompt-skill-home.py`, `publish-build-safely-home.py`, `publish-prompt-skill-translated-home.py`, `publish-govern-autonomy-home.py`, `publish-final-two-home.py`, `publish-legacy-course-home.py` | **7 card extra** sono aggiunte nella Home dopo le prime sei |
| Academy | `theme/publish-academy-journeys.py` verifica che la pagina `/it/academy/` esponga **6 card canoniche**, con tassonomia `verify, coding, fundamentals, prompt, verify, workflow` | Il catalogo esteso dei sette corsi non può essere assunto già presente in Academy |
| Sprint 1 esistente | `theme/publish-sprint1-home.py` + CSS/JS relativi: 4 passi «Comprendi/Sperimenta/Verifica/Costruisci» e anteprima 4→13 card | Il brief sostituisce questo approccio: la nuova Home non deve restare un catalogo espandibile di 13 card |
| Design | `theme/ACADEMY_CARD_STANDARD.md`, `home-showcase.css` e card originarie: struttura condivisa e scala responsive | Preservare il linguaggio delle copertine, ma uniformare effettivamente anatomia, codice, metadati e interazione |
| Menù lingua | Pagina radice e componenti della sidebar già esistenti | **Congelati**: nessuna modifica a layout, collegamenti, effetti e animazioni |
| QA | `theme/home-showcase-browser-smoke.py`, `theme/sprint1-home-browser-smoke.py`, `theme/site-integrity-audit.py` e pipeline | I controlli che richiedono 13 card devono essere aggiornati solo in concomitanza con il nuovo layout approvato |

### Dipendenze della nuova Home

Il brief propone sei blocchi: **Hero → quattro domande → sei card → docenti/professionisti → Brain Challenge → chiusura**. Il footer legale/editoriale resta immutato.

Nuovi layout, icone e testi **non** devono cambiare: corsi, quiz, esercizi, pagine di ricerca, Product Lab, login, footer legale, sitemap o URL. Una pulizia delle sezioni della Home non autorizza a cancellare le pagine di destinazione.

## 3 · URL della proposta italiana

| Area | Route prevista |
| --- | --- |
| Basi e prima domanda | `/manzo-ai/it/impara/come-funziona-un-modello-linguistico/` |
| Prompt e seconda domanda | `/manzo-ai/it/impara/come-costruire-un-prompt-efficace/` |
| Verifica e terza domanda | `/manzo-ai/it/impara/allucinazioni-ai-verificabilita/` |
| Coding e quarta domanda | `/manzo-ai/it/impara/allucinazioni-ai-verificabilita/coding/` |
| Quinta card: verifica | `/manzo-ai/it/impara/come-verificare-le-risposte-ai/` |
| Sesta card: workflow | `/manzo-ai/it/impara/progettare-un-workflow-ai/` |
| Academy | `/manzo-ai/it/academy/` |
| AI Teaching Lab | `/manzo-ai/it/formazione/ia-per-la-didattica/inizia/` |
| Costruire in sicurezza | `/manzo-ai/it/formazione/costruire-in-sicurezza/` |
| AI Brain Challenge | `/manzo-ai/it/pensiero-critico/` |
| Chi siamo | `/manzo-ai/it/chi-siamo/` |

**Stato:** rotte ricavate dal brief e confrontate con i percorsi usati dai generatori; la verifica di ogni file di destinazione sull'artefatto finale appartiene alla Fase 4, non è dichiarata completata qui.

## 4 · Decisioni e contraddizioni da risolvere PRIMA di scrivere la nuova Home

**D1 — Unica destinazione oppure mappa richiesta.**  
La norma «ogni destinazione compare una sola volta nella Home» è incompatibile con la stessa mappa del brief: l'URL delle basi compare nell'hero, nella prima domanda e nella card 03; il Brain Challenge compare nell'hero e nel banner; gli URL per allucinazioni, coding e prompt ricorrono sia nelle domande sia nelle card. Due opzioni coerenti:
- **A (raccomandata):** mantenere i quattro ingressi in forma di domande cliccabili e sei card come richiesto, autorizzando duplicazioni soltanto quando chiariscono una diversa intenzione (hero vs catalogo) e non ripetendo altri caroselli; oppure
- **B:** imporre unicità assoluta degli URL nella Home, **modificando** esplicitamente la mappa di domande e card approvata dal brief.

**D2 — Sette corsi extra e Academy.**  
I generatori attuali inseriscono le sette card aggiuntive nella **Home**. L'Academy corrente è verificata con sei card originali; per spostare davvero gli altri percorsi nell'Academy, bisogna **estendere l'indice dei contenuti di Academy**, senza cambiarne il design, oppure garantire una lista di accesso coerente da altre pagine. È una manutenzione editoriale di Academy, pur essendo escluso il redesign dell'Academy. Richiede un sì esplicito sul minimo adeguamento necessario.

**D3 — «Tre schermate» come soglia orientativa.**  
Hero, quattro porte, sei card (2 righe), doppio blocco, banner e chiusura potrebbero richiedere più di tre viewport a seconda dell'altezza disponibile. Usare la soglia per limitare il rumore e la densità, non tagliare testi o nascondere controlli per raggiungere un valore artificiale.

**D4 — Metadati.**  
Livello e durata rimangono **null** finché non esiste un dato validato; non sostituirli con stime o badge generici spacciati per misurazioni. Titoli senza punto; un'unica anatomia.

**D5 — Verifica Brain Challenge.**  
La formula «Otto sfide» è nel brief ma va confrontata con il contenuto effettivamente pubblicato prima di inserirla nella Home. In caso di disallineamento, non mostrare il numero.

**D6 — Studio / Lavoro / Vita quotidiana.**  
Il brief rileva che raggiungono la stessa destinazione. **Segnalare e non correggere** queste voci: la modifica del menù è fuori ambito.

**D7 — IT prima di EN/ES.**  
Anche se l'attuale Sprint 1 ha già pubblicato una Home trilingue, questa **nuova revisione** viene validata prima sull'italiano. Le versioni EN ed ES non saranno riscritte né pubblicate prima di un'approvazione espressa.

## 5 · Piano di esecuzione dopo approvazione

1. **Fase 1 / Struttura e copy IT:** realizzare esattamente i sei blocchi nell'ordine richiesto, sostituendo i blocchi duplicati e le frasi di servizio; preservare menu, ricerca dove non duplicata e footer.
2. **Fase 2 / Card:** componente unico con sei card originali, griglia 3/2/1, header colorati, icone distinte, un solo link per card, codice 01–06; campi livello e durata disponibili ma vuoti.
3. **Fase 3 / Pulizia e reperibilità:** escludere dalla Home ACR, Product Lab, slide e card aggiuntive; controllare che i sette corsi e le pagine spostate restino raggiungibili nei percorsi autorizzati.
4. **Fase 4 / QA italiano:** 375/768/1440 px, tastiera, reduced motion, contrasto, overflow, 6 card simmetriche, 1 H1, 6 blocchi, nessuna destinazione spezzata, asset e test di SEO/metadati. Lighthouse se eseguibile: **misurare**, non dichiarare anticipatamente 90/100.
5. **Fase 5 / EN e ES:** traduzione dei contenuti della Home e stessa architettura **solo dopo validazione italiana**, senza intervenire sul componente delle lingue.

**Gate di pubblicazione:** nessun commit che attivi deploy di una Home diversa prima della convalida. Fase 0 è terminata; qualsiasi file di implementazione deve essere preparato senza promuovere la modifica su `main`/GitHub Pages fino all'approvazione. Lo Sprint 0 di localizzazione di AI Teaching Lab resta indipendente.

## 6 · Esclusioni ferme

- Menù lingue, animazioni, sidebar e navigazione a sezioni
- Nuovi sistemi di pagamento, login, API o database
- Modifica delle lezioni, corsi e quiz
- Nuovi font o dipendenze esterne
- Promesse di titoli, livelli, durata o efficacia formativa non verificati

**Raccomandazione:** confermare **D1 opzione A** (duplicazioni editoriali motivate soltanto fra hero, domande e sei card) e **D2 estensione minima dell'indice Academy** prima di scrivere il codice; altrimenti il brief non è implementabile integralmente senza contraddirne almeno una regola.
