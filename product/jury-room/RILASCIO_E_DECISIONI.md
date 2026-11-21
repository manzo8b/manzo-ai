# MANZO AI · Stanza dei giurati · Decisioni di rilascio v0.3

## Decisioni implementate

- Hero del palazzo con due stendardi MANZO, file `assets/palazzo-stendardi-manzo.webp` (~275 KB)
- Hero text-free: il testo, il logo del sito e la CTA sono elementi HTML veri. I due stendardi sono parte dell'illustrazione approvata.
- Banco di prova v0.2 preservato, con illustrazione aggiornata. Fonte integrale del preventivo e delle chiavi accessibile senza JavaScript.
- Officina locale (#03): diagnosi C1–C8, specifica della skill v1, sei test sintetici T1–T6, confronto manuale e copia del report. Gli esiti partono vuoti e non rappresentano prove eseguite dal sito.
- Sala dei confini (#02): tre domande, dodici azioni A1–A12, classificazione manuale, quattro incidenti e copia della mappa. Fonti normative da inserire: stato In preparazione.
- Ogni stanza include la scheda originaria completa, resa in HTML leggibile; i Markdown sono preservati in `sources/`.
- IT soltanto, senza API, cookies, analytics, memorizzazione o risultati precompilati.
- `noindex,nofollow` su tutte e quattro le pagine.

## Limiti e punti per approvazione

1. Niente modifica alla Home o al menu ufficiale; queste richiedono una verifica visiva della pagina principale.
2. Le due nuove stanze non sono ancora pilotate con persone reali. Nessun risultato scientifico o normativo è stato generato.
3. La pagina Officina permette una marcatura manuale per T1–T6 e v1/v2; il protocollo della fonte richiede in realtà **tre esecuzioni indipendenti per messaggio e versione**. Il log completo è specificato nel testo integrale, non viene falsificato da un singolo checkbox.
4. La Sala dei confini deve restare in preparazione finché le fonti normative ufficiali richieste non saranno integrate e datate.
5. Lo stylesheet e la testata delle stanze sono ancora componenti di anteprima: prima del rilascio pubblico occorre allinearli alla navigazione centrale del sito (senza toccare i componenti approvati).
6. Il publisher locale realizza la struttura prevista in GitHub Pages, ma non è stato aggiunto al workflow di produzione.

## Test eseguiti

- `tools/check_source_content.py`, `tools/test_experience.py`, `tools/test_registry.py` per il Banco approvato.
- `tools/test_rooms.py`: interfaccia e quattro pagine a 375, 390, 768 e 1440 pixel, senza overflow, con scelte, contenuto e report manuale.
- `tools/build_for_manzo_ai.py` eseguito su una cartella `_site` simulata: verifica percorsi assoluti, contenuti, asset e `noindex`.

## Ambito di un successivo rilascio

1. Revisionare narrativamente Officina e Sala dei confini con il brief originale
2. Collegare le quattro pagine al progetto GitHub attraverso il publisher, senza alterare altre URL
3. Valutare una singola card di ingresso nella Home italiana, *prima* di modificare la Home
4. Avviare i controlli CI di GitHub e solo in seguito effettuare il merge autorizzato

## Aggiornamento v0.5 · 21 novembre 2026

Le limitazioni indicate sopra relative a **una sola marcatura dei test Officina** e all'assenza di confronto **Prima/Dopo** nella Sala sono state risolte nella v0.5. Le due stanze sono etichettate «Anteprima interattiva» pur continuando a richiedere validazione dei contenuti e delle fonti. L'hero di riferimento ora pesa ~241 KB. Consultare `QA_BRIEF_2_v05.md` per l'elenco completo dei controlli; i precedenti riferimenti a «approvato» nei file storici di documentazione NON costituiscono approvazione del prototipo. La PR #70 resta draft e non contiene questa v0.5. Nessuna pubblicazione.
