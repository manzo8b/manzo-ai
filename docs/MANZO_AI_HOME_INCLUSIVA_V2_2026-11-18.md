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
