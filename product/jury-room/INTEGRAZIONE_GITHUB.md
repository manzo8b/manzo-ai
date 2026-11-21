# Piano d'integrazione GitHub Pages — v0.4

**Stato**: `READY FOR REVIEW`, non ancora in `main` e non pubblicato.

## Architettura del publisher

Sorgente da collocare in `product/jury-room/` (cartelle `assets/`, `tools/`, le quattro HTML, documenti `sources/` e README). La script `tools/build_for_manzo_ai.py` genera:

- `/it/laboratorio/stanza-dei-giurati/`
- `/it/laboratorio/stanza-dei-giurati/banco-di-prova/`
- `/it/laboratorio/stanza-dei-giurati/officina-locale/`
- `/it/laboratorio/stanza-dei-giurati/sala-dei-confini/`

Gli asset sono versionati sotto `/manzo-ai/assets/jury-room/`. Tutte le pagine conservano `noindex,nofollow` e sono dichiarate prototipi privati; non sono aggiunte automaticamente al menu ES/EN. L'integrazione della Home è **separata e facoltativa**, con `--home-preview`: aggiunge soltanto un collegamento discreto nel blocco esistente della sfida, non cambia il numero di sezioni.

## Come integrarlo nel workflow di build (solo quando autorizzato)

Dopo la generazione della Home v2 e prima dei gate finali:

```bash
python3 -m py_compile product/jury-room/tools/build_for_manzo_ai.py
python3 product/jury-room/tools/build_for_manzo_ai.py --site _site
python3 product/jury-room/tools/build_for_manzo_ai.py --site _site --verify-only
python3 product/jury-room/tools/test_contrast.py
```

Non aggiungere `--home-preview` alla pipeline pubblica prima della revisione visiva. Aggiornare il controllo finale di integrità dei link dopo l'iniezione e confermare la nav condivisa del sito. Inserire la nuova voce del menu solo quando validata dall'autore. Lo script fallisce se un URL di destinazione esiste già, evitando sovrascritture accidentali.

## Gate

- Conservare le immagini, in particolare `palazzo-stendardi-manzo.webp`, e i 4 documenti sorgente
- Ripetere fedeltà editoriale, simulazione di 8 lacune, Prima/Dopo/Chiave, controlli Officina/Confini, mobile, contrasto e noindex
- Rivedere i testi visualizzati su sfondo fotografico e sui gradienti con browser dopo l'effettiva pubblicazione in ambiente di staging
- Completare le fonti ufficiali per Sala dei confini prima di dichiarare la scheda completa
- Non simulare l'AI né riempire i risultati dei test effettivi
- Non pubblicare su `main` prima di un'approvazione esplicita
