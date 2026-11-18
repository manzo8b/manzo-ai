# MANZO AI — HOME inclusiva · Architettura v2

**Data:** 18 novembre 2026  
**Decisione:** MANZO AI è una piattaforma divulgativa, educativa e operativa **aperta a tutte le persone interessate all'intelligenza artificiale**, non una homepage rivolta prevalentemente a docenti o ad aziende.  
**Stato:** modifiche ai sorgenti su `main`; deploy e prova visiva finale non ancora confermati.

## Direzione di prodotto

1. **Gateway lingua** autonomo: mantenere la selezione IT/EN/ES, aggiornarne la microcopy senza demolire il design già approvato.
2. **Homepage localizzate** per utenti di diversi livelli e professioni, con messaggio semplice e non tecnico.
3. **Quattro obiettivi** iniziali: capire l'IA, migliorare i prompt, riconoscere le allucinazioni, creare e sperimentare.
4. **Quattro card in evidenza**: fondamenti, Prompt Engineering, Allucinazioni dell'IA, AI Teaching Lab. Ognuna ha una destinazione reale, verificata nella build; il Teaching Lab resta attualmente in italiano.
5. **Conservare integralmente le sei card Academy** e il catalogo nei rispettivi URL. L'Academy è il punto di accesso all'intera offerta, comprese le risorse più tecniche.
6. **Menu della home essenziale**: Home, Academy, Prompt, Allucinazioni, AI Teaching Lab, Chi siamo. Sei URL distinti, non sei etichette per la stessa pagina. Le pagine tecniche e di ricerca rimangono disponibili nel catalogo e nella struttura del sito.
7. **Togliere la scena tecnica blu Product Lab** soltanto dalle homepage locali: non eliminare il Product Lab né riscrivere i laboratori.
8. **Credibilità**: nominare il curatore e aprire una pagina Chi siamo / About / Quiénes somos in tre lingue, senza dichiarare accreditamenti o certificazioni inesistenti.

## Cosa resta operativo

La ricerca originaria non viene sostituita. I suggerimenti hanno destinazioni reali e non simulano risposte generative. La scelta di una card porta a un corso o laboratorio pubblicato; non si sostituisce un catalogo con un chatbot fittizio.

## Implementazione

- `theme/publish-home-conversational.py` + `theme/home-conversational.js`: quattro obiettivi inclusivi e destinazioni verificate
- `theme/publish-home-curation.py`: rimozione della scena tecnica, nuovo messaggio globale, card tematiche, menu breve, attributi locale
- `theme/home-curation.css`: card editoriali moderne e responsive, palette bianca con blu/arancione/rosso/giallo e focus visibile
- `theme/mobile-nav.js`: navigazione a sei destinazioni sulle home, navigazione completa intatta nelle altre pagine
- `theme/publish-about.py`: pagine autoriali IT/EN/ES
- `theme/tests/test_home_conversational.py`, `theme/tests/test_home_curation.py`, test JS e smoke browser: protezione regressioni
- `.github/workflows/deploy-pages.yml`: build/verification gate; i risultati di esecuzione non sono ancora stati controllati

## Accettazione e limiti

- Le pagine devono mostrare tutti e quattro gli obiettivi e tutte e quattro le card tematiche con URL validi.
- Le sei card dell'Academy preesistenti devono restare visibili, senza alterazione dei loro contenuti.
- Il menu non deve duplicare destinazioni e non deve occupare metà viewport mobile.
- L'inglese e lo spagnolo descrivono onestamente la lingua italiana del Teaching Lab.
- Nessuna etichetta deve fingere un chatbot, attestati, iscrizioni o funzionalità SaaS non distribuite.
- Rimangono da verificare GitHub Actions, rendering Chrome/Safari, tastiera/VoiceOver, overlay globali, ricerca e sitemap effettiva.

**Nota:** non confondere "home aperta a tutti" con "tutti i contenuti per tutti". Ogni card ha livello, destinatari e limiti propri, ma la home non seleziona né esclude categorie di visitatori.

## Consolidamento della pubblicazione — 18 novembre 2026

### Controlli di build aggiornati
- `publish-home-curation.py --verify-only` ora verifica i **quattro obiettivi**, la presenza delle **sei card originali Academy**, i **quattro collegamenti delle card tematiche**, i **sei collegamenti unici del menu**, l'assenza della scena tecnica blu e l'esistenza delle pagine di destinazione.
- Nessuna modifica ai contenuti delle lezioni, ai corsi originali, al backend, ai dati o ai pagamenti.
- Eliminati sulla homepage alcuni testi non più adatti a una pagina pubblica, tra cui il richiamo ripetuto a «non essere un chatbot», riferimenti a materiali «che selezioneremo insieme» e la versione editoriale `v0.6`. Gli stessi testi nelle eventuali lezioni originali non sono stati alterati.
- Aggiunta pulizia delle etichette duplicate `Lezione / Lesson / Lección` **solo sulle copie delle card in homepage**.
- Corretto il confronto delle vecchie scorciatoie con icone decorative: `◈ Studio`, `◈ Lavoro`, `◈ Vita quotidiana`. Il menu breve non dipende più dal confronto testuale letterale prima della normalizzazione.
- Test JS isolato eseguito sul controller per menu e scorciatoie: **PASS**. Test di regressione `theme/tests/test_home_legacy_cleanup.cjs` incluso nel workflow GitHub Pages.
- Test Python/Node dell'intera pipeline e ultimo deploy: **esito non osservabile dal controllo commit**, perché il connettore disponibile non espone l'elenco completo delle esecuzioni push su `main`. Controllare le Actions direttamente prima di presentare la versione come definitivamente pubblicata.

### Controlli finali richiesti
Confrontare i tre URL pubblici `/it/`, `/en/`, `/es/` e il gateway `/manzo-ai/`, preferibilmente con browser ricaricato senza cache. Verificare anche 320, 390 e 1440 px, che il menu non duplichi destinazioni, che le quattro card in evidenza e le sei dell'Academy siano tutte presenti, che la ricerca preesistente funzioni e che la pagina About abbia contenuti reali ma senza accreditamenti inventati.

## Diagnosi GitHub Pages — 18 novembre 2026 (verificata sui log Actions)

**Problema reale:** più workflow `Deploy MANZO AI` sul branch `main` sono falliti prima del deploy GitHub Pages.

- Esecuzione di riferimento: `https://github.com/manzo8b/manzo-ai/actions/runs/44277738505` (commit `115b347`).
- Job `deploy`, step `Extract and inspect static site`: `NameError: name 'PRODUCT' is not defined` in `theme/tests/test_home_conversational.py:36`.
- I quattro test in quel modulo fallivano nel `setUp`, prima di poter produrre e distribuire la nuova HOME.
- **Correzione su `main`:** commit `197d709d7d9bc095322e469bcd4fb0a92fa58af8`, eliminato il vecchio fixture Product Lab non più necessario. La pipeline è configurata per attivarsi alle modifiche di quel file.
- **Stato non ancora attestato:** esito della prima esecuzione GitHub Actions **successiva** al fix. Non dichiarare il sito aggiornato in produzione finché quel run non conclude `success` e i contenuti pubblici non siano verificati.

**Lezione per il processo:** non sostituire i test di pubblicazione con un check visivo dei file su GitHub. Fare sempre triage dei log effettivi dei workflow falliti e correggere prima il primo errore bloccante.
