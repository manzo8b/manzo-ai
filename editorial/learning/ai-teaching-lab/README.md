# AI Teaching Lab · Corso docenti MANZO AI

**Stato:** cinque moduli completi in italiano, con **publisher predisposto per la versione pubblica beta**, non accreditata. I file sorgenti restano bozze editoriali non transazionali; il sito diventa pubblico soltanto dopo un deploy GitHub Pages concluso con successo.  
**Ramo dedicato:** feat/ai-teaching-lab-curriculum-20261117  
**Revisione:** 17 novembre 2026  
**Licenze e diritti:** documenti didattici originali per revisione del titolare; fonti esterne solo con link, senza riproduzioni integrali.

## Contenuti

- it/course.json — cinque moduli, teoria e fonti, pedagogisti citati come parafrasi, metodo MANZO AI sempre presente, due scenari autentici sintetici per modulo.
- it/module-01.md ... module-05.md — **cinque lezioni integrali** di circa 2.000 parole ciascuna, con sequenza da 240 minuti, laboratori da 72+72 minuti, prompt, esempi ragionati, quiz, matching, cruciverba, rubrica, guida del formatore e schede di consegna.
- it/lesson-01.md — prima lezione pilota, conservata come risorsa storica complementare.
- it/assessment-bank.json — 5 set con scelta multipla, scenari, associazioni, 5 cruciverba realmente incrociati (35 termini), compiti autentici ed exit ticket.
- it/scenarios.json — cinque decision lab, 3 scelte iniziali × 2 sviluppi per modulo: **30 percorsi possibili** con feedback specifico, revisione e trasferimento al lavoro docente.
- theme/publish-ai-teaching-lab.py — publisher pubblico per il corso in italiano: landing, cinque lezioni HTML complete, CSS/JS, metadati, JSON-LD e card dedicate nelle tre Academy con lingua originale dichiarata.
- preview/index.html, preview/assets.css, preview/app.js — **anteprima interattiva source-only**, senza backend, che visualizza teoria, pedagogisti, casi, quiz, matching e cruciverba in griglia + modalità accessibile.
- tests/test_course.py — test di integrità, coerenza didattica e sicurezza editoriale.
- ../../../../docs/AI_TEACHING_LAB_CURRICULUM_2026-11-17.md — curriculum di progettazione generale.

## Avvio anteprima su Mac o PC

Clonare o scaricare il ramo; dalla **radice del repository**:

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

Quando il ramo verrà integrato e il deploy GitHub Pages terminerà con esito positivo, il percorso sarà disponibile su:

    https://manzo8b.github.io/manzo-ai/it/formazione/ia-per-la-didattica/

Il corso sarà **ad accesso aperto**, senza account, progressi persistenti, certificati, voti o raccolta di lavori degli studenti. Le cinque lezioni integrali avranno propri URL sotto `modulo-01/` … `modulo-05/` e il percorso sarà collegato all'Academy e alle sitemap. Le traduzioni non sono ancora disponibili: i collegamenti EN/ES identificano la lingua italiana del corso, senza fingere una localizzazione.

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
- Nessuna modifica al sito pubblico, alle tabelle Supabase esistenti, Auth, catalogo M2, deploy o pagamenti.

## Definizione di completamento editoriale vs product release

**Sviluppo contenuti:** cinque moduli, banca di verifiche e trenta percorsi decisionali scritti, prototipo funzionante in sorgente. Nuovo publisher pronto per l'integrazione e la verifica su staging.  
**Resta prima di una release:** validazione teorica con esperto disciplinare, controllo delle fonti, prove di comprensione con docenti campione, revisione UX, test su dispositivi reali, traduzioni EN/ES se richieste, eventuale integrazione nel catalogo e progressi sicuri server-side. La durata 20h è **stimata**. Nessuna pubblicazione automatica per il solo merge.

