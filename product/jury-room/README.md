# MANZO AI · La stanza dei giurati — Prototipo v0.5

**21 novembre 2026 · ANTEPRIMA PRIVATA · NON PUBBLICATA**

Questo pacchetto riprende e corregge la v0.4 secondo il **Brief di correzione n. 2**, conservato integralmente in `sources/MANZO_AI_Brief_Correzione_2_Prototipo.md`. È autonomo, statico, in italiano. Non serve alcuna API AI, account o pagamento.

## Aprire il prototipo

1. Estrarre l'intera cartella ZIP, mantenendo `assets/` vicino ai quattro file HTML.
2. Aprire `index.html` con un browser moderno (Chrome, Safari, Firefox).
3. Entrare nelle tre stanze: **Officina locale (Chiedi)**, **Banco di prova (Controlla)**, **Sala dei confini (Decidi)**.
4. L'animazione del palazzo è facoltativa, dispone di controlli di pausa ed è preimpostata senza caricamento automatico.

### Correzioni principali v0.5

- **Banco di prova:** i dettagli delle otto lacune del registro sono nascosti prima dell'indagine; possibile saltarla intenzionalmente. Le nove opzioni del passo 02 mostrano identificativi neutrali prima del confronto e L1–L8 / «Falso allarme» dopo. Il ripristino integrale azzera anche lo sblocco.
- **Officina locale:** il simulatore «Le regole fisse al lavoro» calcola prezzi e tre regole del forno tramite soli controlli deterministici. I sei test manuali T1–T6 hanno **3 prove per v1 e 3 per v2**: 18 caselle di esito per versione, inizialmente «Non provata». Il caso T6 segnala la presenza di errori osservati senza attribuire voti.
- **Sala dei confini:** la mappa «Prima» viene congelata al primo clic; dopo gli incidenti si possono collegare A1–A12 e cambiare livello. La mappa finale confronta Prima/Dopo, indica le modifiche e fornisce avvisi testuali di coerenza (non punteggi né verdetti legali).
- **Indice e immagini:** status delle tre stanze uniformato a «Anteprima interattiva», nessuna approvazione attribuita, titolo H1 visibile, dialogo di anteprima inutilizzato rimosso, caricamento prioritario per le immagini hero.
- **Sorgenti:** i documenti di Officina e Sala sono stati aggiornati nei soli rimandi indicati dal brief e **rigenerati** in HTML mediante `tools/regenerate_sources.py`, senza modifiche manuali alle copie integrali.

## Vincoli e privacy

Tutti i nomi, ordinativi, prezzi, casi e incidenti del laboratorio sono **fittizi**. Il sito non esegue un modello AI, non genera risultati sperimentali, non memorizza nulla nel browser, non carica dati su server, non installa cookie e non usa analytics. Le scelte sono conservate **solo nella memoria della pagina** e spariscono al reload. Le funzioni di copia richiedono permesso del browser. Le quattro pagine recano `noindex,nofollow`.

I documenti sorgenti sono leggibili anche senza JavaScript; le funzioni interattive, invece, richiedono JavaScript. Il prototipo non è un test scientifico, una certificazione di qualità o una consulenza legale.

## Collaudo

Con Python, `beautifulsoup4`, `mistune` e Playwright/Chromium installati:

```bash
python tools/check_source_content.py
python tools/check_rooms_sources.py
python tools/test_registry.py
python tools/test_experience.py
python tools/test_rooms.py
python tools/test_contrast.py
python tools/test_brief_v05.py
```

In `QA/` sono presenti screenshot di controllo. Vedi `QA_BRIEF_2_v05.md` per i risultati e per le decisioni ancora aperte. I controlli automatici non equivalgono a una certificazione WCAG né a test reali con utenti.

La build di staging si può verificare **localmente** con `python tools/build_for_manzo_ai.py --site _site` seguito da `--verify-only`. Questo script non pubblica nulla sul sito: nessun merge, nessuna modifica a `main`, alla Home del sito principale o al workflow di distribuzione.

**GitHub:** la PR #70 resta una bozza incompleta e separata; il pacchetto v0.5 non è stato caricato su GitHub. La pubblicazione richiede una decisione esplicita dell'autore.
