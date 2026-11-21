# La stanza dei giurati — staging v0.5

**Stato:** staging tecnico non pubblicato; **non effettuare merge** prima di aggiungere gli asset approvati e verificare il contrasto dopo il deploy.

## Architettura

Prototipo revisionato visivamente (v0.5): tre esperienze all'interno di Laboratorio, nell'ordine didattico Chiedi → Controlla → Decidi. L'immagine del palazzo conserva due stendardi MANZO. Il Banco di prova ha la narrazione Prima / Dopo / Chiave, un documento fittizio, prompt A/B ed errori verificabili. Officina locale dispone di sei casi sintetici, mini simulatore deterministico e 18 esiti manuali per versione (v1/v2). Sala dei confini comprende dodici azioni, quattro incidenti, confronto Prima/Dopo e avvisi informativi. Le tre stanze restano anteprime interattive: le fonti normative della Sala richiedono ancora una validazione specifica.

### Percorsi già previsti

- /it/laboratorio/stanza-dei-giurati/
- /it/laboratorio/stanza-dei-giurati/banco-di-prova/
- /it/laboratorio/stanza-dei-giurati/officina-locale/
- /it/laboratorio/stanza-dei-giurati/sala-dei-confini/

## Sorgenti necessari prima di attivare il publisher

Collocare **senza riscriverli** in `product/jury-room/` i file approvati nel pacchetto v0.5, cioè i quattro HTML, `assets/` (CSS, JavaScript, immagini compresa `palazzo-stendardi-manzo.webp`, SVG e video compresso), e `sources/` con i quattro documenti originali. Inserire anche i test `tools/test_contrast.py`, `tools/test_experience.py`, `tools/test_rooms.py`, `tools/check_source_content.py` e `tools/check_rooms_sources.py`.

Il pacchetto integrale è stato consegnato come ZIP nella conversazione; GitHub non è la fonte definitiva finché questi file non sono stati trasferiti. Non si usa un segnaposto o una versione precedente delle immagini approvate.

## Regole di rilascio

- Nessuna modifica al menu lingue o ai blocchi Home approvati senza anteprima specifica
- Le pagine mantengono `noindex,nofollow`, non sono disponibili in EN/ES e non devono comparire nella sitemap
- Dati e identità degli scenari sono fittizi; niente API AI, cookie o risultati precompilati
- I componenti devono essere operabili da tastiera, con etichette testuali oltre ai colori e `prefers-reduced-motion`
- Almeno 4,5:1 sul testo ordinario a sfondo solido; controlli supplementari sugli sfondi fotografici e gli stati disabilitati
- In questa tranche l'accesso dalla Home è una **preview opzionale**, non un nuovo blocco pubblico
- Il publisher non va aggiunto al workflow di Pages prima del collaudo dei file nel branch

## Comandi di staging dopo l'aggiunta delle sorgenti

```bash
python3 theme/publish-jury-room.py --site _site
python3 theme/publish-jury-room.py --site _site --verify-only
python3 product/jury-room/tools/test_contrast.py
```

La modifica alla Home, una volta approvata, si esegue **dopo** `publish-home-magic-v2.py` e **prima** degli ultimi controlli di integrità. Conservare sempre il numero dei cinque blocchi, le sei card esistenti e la navigazione condivisa.

Questo documento e il publisher sono lo **scheletro di integrazione**, non la pubblicazione del prodotto.


## Aggiornamento del 21 novembre 2026 — approvazione visiva della v0.5

La revisione visiva della **v0.5** è stata approvata dall'autore. Questa approvazione **non autorizza la pubblicazione su GitHub Pages, il merge o modifiche alla Home principale**.

Il pacchetto sorgente completo v0.5 è stato collaudato localmente: 38 file runtime/documentali (senza screenshot QA), 4 rotte generate, verifica `--verify-only` positiva; test della fedeltà ai sorgenti, delle interazioni e degli stati senza JavaScript superati a 375/768/1440 px. 122 campioni testuali a sfondo solido soddisfano 4,5:1. Questi controlli non equivalgono a certificazione WCAG.

**Il ramo GitHub è ancora incompleto** finché i 38 file della v0.5, compresi asset binari, non sono materialmente presenti in `product/jury-room/`.

### Importazione sicura dal pacchetto esatto

Su un clone locale pulito del ramo `feat/jury-room-v04-staging`:

```bash
python3 theme/install-jury-v05.py --zip /percorso/MANZO_AI_Stanza_dei_Giurati_v05_Brief_2_Corretto.zip --dry-run
python3 theme/install-jury-v05.py --zip /percorso/MANZO_AI_Stanza_dei_Giurati_v05_Brief_2_Corretto.zip
python3 product/jury-room/tools/build_for_manzo_ai.py --site /percorso/staging/_site
python3 product/jury-room/tools/build_for_manzo_ai.py --site /percorso/staging/_site --verify-only
python3 product/jury-room/tools/test_brief_v05.py
```

L'installatore convalida lo SHA-256 esatto `0d74c2832cb296a22d15aaa6aef0791d7f60536bfefc3b7d37d47a427e52ace7`, impedisce sovrascritture e rifiuta i rami di produzione. Non effettua push o deploy.

La preview della Home è facoltativa ed esclusa dalla prima integrazione. `deploy-pages.yml` resta invariato; mantenere questa PR in stato draft e non unirla a `main` senza autorizzazione esplicita al rilascio.
