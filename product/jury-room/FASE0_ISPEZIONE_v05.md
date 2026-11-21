# Fase 0 · Ispezione del pacchetto v0.4 prima delle correzioni v0.5

**Data:** 21 novembre 2026 · **Ambito:** 4 HTML, 5 asset JS/CSS, immagini/video, documenti di origine.

| Verifica | Risultato dell'ispezione v0.4 |
|---|---|
| Titolo HTML dell'indice | H1 unico; una regola CSS più avanti nel file lo rendeva visibile, nonostante una precedente regola contraddittoria che lo nascondeva. La v0.5 elimina la regola superata. |
| Dialogo inutilizzato | `#room-dialog` e relativi handler di `app.js` ancora presenti nell'indice, mentre le card sono link diretti. Rimossi nella v0.5. |
| Registro Banco | La lista L1–L8 era leggibile dal registro prima della prima diagnosi; ora protetta da stato in memoria della pagina. |
| Selezione Banco | L'etichetta «FA» rendeva identificabile il falso allarme. Ora etichette neutre 1–9, svelate dopo il confronto. |
| Calcolo del confronto Banco | `app.js` compara le scelte dell'utente con `window.MANZO_EVAL_01`, costruisce la rete solo dalle selezioni reali e conserva una fotografia `before` per la revisione R1–R8; nessun modello è chiamato. |
| Stato Banco | Array `runs[]` e oggetto `before` in memoria JS. Nessun `localStorage`, `sessionStorage` o cookie. |
| Officina | Diagnosi C1–C8 funzionante; prima mancavano il simulatore e le tre ripetizioni per versione. |
| Sala | Dodici classificazioni e quattro note per incidenti, ma nessun prima/dopo o collegamento azione-incidente; introdotti nella v0.5. |
| Fallback senza JavaScript | Fascicolo e schede integrali già nell'HTML; mantenuti. |
| Tabelle | Contenitori con overflow orizzontale locale; nessun overflow dell'intera pagina ai viewport verificati. |
| Video | `filmato-concept.mp4`: **212.027 byte**, video facoltativo con `preload=none` e controlli di pausa nativi. |

## Pesi delle immagini (prima → dopo)

| Asset | v0.4 | v0.5 | Nota |
|---|---:|---:|---|
| `palazzo-stendardi-manzo.webp` | 281.184 B | 241.120 B | Immagine hero effettivamente usata in tutte e quattro le pagine, ricompressa senza rigenerazione del soggetto |
| `palazzo-senza-testo.webp` | 255.610 B | 241.288 B | Archivio storico, non referenziato dalle pagine attuali |
| `hero-palazzo-futuristico.webp` | 207.178 B | 207.178 B | Poster del video, già sotto 250 KB |
| `stanza-dei-giurati.webp` | 378.942 B | 378.942 B | Archivio storico NON referenziato, conservato senza alterazioni |
| `filmato-concept.mp4` | 212.027 B | 212.027 B | Video invariato |

**Riferimento editoriale:** gli originali Markdown recuperati dalla Library contenevano ancora i vecchi rimandi nonostante il brief li dichiarasse aggiornati. Le copie in `sources/` sono state allineate **solo** alle sostituzioni esplicite del brief e poi usate per rigenerare le schede integrali. Gli originali esterni al pacchetto sono rimasti immutati.
