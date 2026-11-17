# AI Teaching Lab · Corso docenti MANZO AI

**Stato:** cinque moduli redatti in italiano e integrati nel publisher della **versione pubblica beta non accreditata**. I file JSON sorgenti conservano lo stato di bozza editoriale; il publisher produce copie pubbliche con metadati diversi. La presenza del codice sul branch principale non dimostra, da sola, l'esito dell'ultimo deploy GitHub Pages.  
**Sviluppo:** contenuti inizialmente preparati su `feat/ai-teaching-lab-curriculum-20261117`; integrazioni successive e quattro studi audiovisivi presenti sul branch `main`.  
**Revisione:** 17 novembre 2026  
**Licenze e diritti:** documenti didattici originali per revisione del titolare; fonti esterne solo con link, senza riproduzioni integrali.

## Contenuti

- it/course.json — cinque moduli, teoria e fonti, pedagogisti citati come parafrasi, metodo MANZO AI sempre presente, due scenari autentici sintetici per modulo.
- it/module-01.md ... module-05.md — **cinque lezioni integrali**, di lunghezza diversa (circa 2.900–5.000 parole nei sorgenti al 17 novembre 2026), con una durata didattica stimata di 240 minuti per modulo, due laboratori principali per modulo, prompt, casi sintetici, verifiche, rubriche e guida del formatore. Il progetto finale del modulo 05 è un'attività aggiuntiva distinta dai dieci laboratori principali.
- it/lesson-01.md — prima lezione pilota, conservata come risorsa storica complementare.
- it/assessment-bank.json — 5 set con scelta multipla, scenari, associazioni, 5 cruciverba realmente incrociati (35 termini), compiti autentici ed exit ticket.
- it/scenarios.json — cinque decision lab, 3 scelte iniziali × 2 sviluppi per modulo: **30 percorsi possibili** con feedback specifico, revisione e trasferimento al lavoro docente.
- theme/publish-ai-teaching-lab.py — publisher pubblico per il corso in italiano: landing, cinque lezioni HTML complete, CSS/JS, metadati, JSON-LD e card dedicate nelle tre Academy con lingua originale dichiarata.
- preview/index.html, preview/assets.css, preview/app.js — **anteprima interattiva source-only**, senza backend, che visualizza teoria, pedagogisti, casi, quiz, matching e cruciverba in griglia + modalità accessibile.
- tests/test_course.py — test di integrità, coerenza didattica e sicurezza editoriale.
- ../../../../docs/AI_TEACHING_LAB_CURRICULUM_2026-11-17.md — curriculum di progettazione generale.

## Avvio anteprima su Mac o PC

Clonare o scaricare il repository; dalla **radice del progetto**:

    python3 -m http.server 8766

Aprire:

    http://localhost:8766/editorial/learning/ai-teaching-lab/preview/

**Importante:** non aprire index.html con file:// perché l'anteprima carica due JSON relativi usando fetch e alcuni browser bloccano queste richieste. Non è un servizio Supabase: è una UI locale di prova.

### QA automatica

    python3 -m unittest discover -s editorial/learning/ai-teaching-lab/tests -p 'test_*.py' -v
    node --check editorial/learning/ai-teaching-lab/preview/app.js

Workflow di sola verifica: .github/workflows/ai-teaching-lab-qa.yml.

I test comprendono controlli unitari, pubblicazione su staging statico con sitemap, browser Chromium alle larghezze 390/1440 px e interazioni di tutti i moduli. **Non** equivalgono a validazione pedagogica, audit WCAG completo, lettore schermo reale, Safari/iOS o verifica delle 20 ore con docenti.

## Versione pubblica beta

Il publisher predispone il percorso a questo indirizzo, da considerare operativo soltanto dopo una verifica del deploy GitHub Pages:

    https://manzo8b.github.io/manzo-ai/it/formazione/ia-per-la-didattica/

Il percorso è progettato per essere **ad accesso aperto**, senza account, progressi persistenti, certificati, voti o raccolta dei lavori degli studenti. Le cinque lezioni hanno URL predisposti sotto `modulo-01/` … `modulo-05/`; il publisher integra anche i collegamenti all'Academy e alla sitemap. Le traduzioni non sono ancora disponibili: i collegamenti EN/ES identificano la lingua italiana del corso, senza fingere una localizzazione.

## Metodo MANZO AI

**Ascolto → Classificazione → Valutazione del rischio → Domande mirate → Progettazione → Verifica → Consegna**, integrato con la progressione **Comprendere → Applicare → Valutare → Creare**. È un metodo operativo MANZO AI, non uno standard accreditato.

## Temi

1. Carico di lavoro, attenzione e valore di una scelta IA/non IA
2. Compiti generati, fake news, affidabilità documentale e integrità
3. Materiali multimediali corretti, accessibili e non sovraccarichi
4. Differenziazione, UDL, valutazione formativa e feedback
5. Tutor socratico, prova di sicurezza, governance e cyberbullismo

## Regole di sicurezza

- Tutti gli studenti, documenti, chat, dati e casi devono essere **fittizi**; vietato usare dati identificabili di minori in sistemi non autorizzati.
- Soluzioni nel JSON pubblico sono formative; non sono idonee a esami privati o certificazioni.
- Tutti i controlli, punteggi e cruciverba girano **esclusivamente nel browser**. Nessun progresso reale viene registrato o inviato. L'anteprima non dispone di login, database o analytics.
- Non dichiarare badge, attestati, accreditamento MIUR/MIM o soddisfacimento dell'articolo 4 dell'AI Act come automatismi del percorso.
- Prima di un impiego in scuole reali verificare contratto, ruolo titolare/responsabile, policy, finalità, anonimizzazione, sicurezza, AI Act e GDPR con personale responsabile. Il parere Garante del 20/10/2026 riguarda **uno schema di decreto**: verificare prima di citare come definitivo.
- Gli aggiornamenti sono effettuati nel codice del sito e nei suoi workflow di pubblicazione; non implicano modifiche alle tabelle Supabase, all'autenticazione, al catalogo commerciale o ai pagamenti.

## Definizione di completamento editoriale vs product release

**Sviluppo contenuti:** cinque moduli, banca di verifiche e trenta percorsi decisionali redatti; publisher e laboratori integrati nel codice sorgente. La funzionalità nel browser e la pubblicazione devono essere verificate con test eseguiti e controlli sul sito reale.  
**Resta per una versione pienamente validata:** revisione disciplinare, controllo periodico delle fonti, prove con docenti principianti, audit UX e accessibilità, test su dispositivi reali e, se necessari, traduzioni EN/ES, progressi persistenti e integrazioni commerciali. La durata complessiva di 20 ore è **una stima progettuale, non una misurazione con utenti**. L'effettiva pubblicazione dipende dall'esito di GitHub Pages.


## Mission Studio — micro-web-app didattica

**Codice:** `tools/ai-teaching-launchpad/index.html`  
**Rotta prevista:** `/it/formazione/ia-per-la-didattica/inizia/`  
**Stato:** micro-app interattiva v0.1 in sorgente, collegata al publisher e ai controlli GitHub Pages. La disponibilità del sito pubblico va confermata dopo il deploy.

Permette al docente di selezionare una missione fra immagini, voce, video e verifica delle fonti; personalizzare argomento, destinatari, tempo e obiettivo; vedere un piano didattico sintetico; scaricare o ripristinare un brief JSON. È una guida **basata su regole locali**, senza inferenza IA, accesso a dati degli studenti, registrazione dei progressi o invio del brief a server. Non sostituisce i laboratori: vi si collega, ma il JSON del brief non viene importato automaticamente dagli Studi.

## Laboratori multimediali e Workspace

Oltre al corso e al laboratorio multimediale iniziale, il publisher collega gli Studi **immagini**, **voce** e **video** e il **Workspace multimediale**, nei rispettivi percorsi `studio-immagini/`, `studio-voce/`, `studio-video/` e `workspace-multimediale/`.

Gli Studi lavorano sui materiali importati localmente e producono schede JSON di lavoro; non attivano modelli generativi remoti. Lo Studio video, sui browser compatibili, esporta soltanto una sequenza WebM silenziosa: la traccia audio di riferimento e i sottotitoli restano separati. Il Workspace aggrega **metadati** e approvazioni autodichiarate, non ingloba file audiovisivi e non certifica in modo indipendente la revisione del docente.

L'audit automatico del codice si avvia con `node theme/check-ai-teaching-lab-contracts.cjs`; dopo un build si può indicare `--site _site` per verificare anche la struttura pubblicata. L'esito dello script non sostituisce test reali con browser o docenti.
