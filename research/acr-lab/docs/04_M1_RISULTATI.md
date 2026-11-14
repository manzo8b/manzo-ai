# M1 · Verifica strumentale v0.6 — risultato locale

**Data:** 14 novembre 2026  
**Tipologia:** smoke test di integrazione browser + trace store, **non** studio scientifico ACR.  
**Ambiente:** Chromium headless con Playwright Python, emulazione viewport 390 × 844, dati HTML interamente locali, nessuna API AI.

## Obiettivo

Validare che un unico catalogo di test riproducibile registri correttamente quattro versioni di un'interfaccia e riconosca regressioni introdotte intenzionalmente.

## Sequenza

| Versione | Cambio predefinito | Test superati / totale | Atteso |
|---|---|---:|---|
| V0 | baseline | 6/6 | tutto funzionante |
| V1 | il pulsante menu non apre il nav | 5/6 | nuova regressione mobile |
| V2 | menu corretto, contrasto testo peggiorato | 5/6 | nuova regressione contrasto |
| V3 | contrasto ripristinato | 6/6 | nessuna nuova regressione |

Catalogo fisso `mobile-web-smoke-v1`: menu mobile e aria-expanded; rapporto cromatico mirato 4,5:1 su un paragrafo; validazione email; assenza scroll orizzontale; punteggiatura titoli; landmark semantici. La verifica del contrasto è un test **mirato** e **non** sostituisce un audit WCAG/axe-core completo.

## Misure osservate

- **2 regressioni** rilevate su **16 transizioni eleggibili**, tasso 12,5% nella sequenza sintetica.
- **30/30 test del codice** superati nel runtime di sviluppo con Chromium disponibile; la suite del codice include verifiche dell'engine precedente.
- Il registro SQLite archivia le sei misure per ogni versione, gli eventi e gli hash SHA-256 dei file HTML.
- È presente uno script indipendente di audit: confronta database, riepilogo JSON, file originali e ricalcola le metriche.

Questi risultati verificano la **strumentazione**, non la superiorità di C3 su C2. I bug sono stati introdotti intenzionalmente e l'agente AI non è stato coinvolto.

## Come riprodurre

```bash
python -m pip install -e '.[test,browser]'
python -m pytest -q
python examples/run_browser_smoke.py --out experiments/experiment_a/results/browser_smoke_local_2
python examples/audit_browser_smoke.py --dir experiments/experiment_a/results/browser_smoke_local_2
```

Se non si dispone di Chromium di sistema, impostare `ACR_CHROMIUM_BIN=/percorso/chromium` o installare il browser Playwright per la piattaforma. I test browser vengono saltati quando il browser non è disponibile, mentre lo smoke test standalone termina con errore: nessun PASS simulato.

## Cosa manca per M2

1. Il catalogo deve essere ampliato con axe-core e controlli di interazione su due compiti reali, su copie di test (non produzione).
2. Implementare un medesimo controller di revisione C2/C3 con il solo retrieval come trattamento differenziale.
3. Integrare provider LLM, contatori token/costo, hash e riferimenti protetti ai prompt, e isolamento delle memorie tra i bracci.
4. Congelare protocollo e versione dei tool. Il pilot serve a validare il metodo di misura; non deve produrre affermazioni di efficacia.

**Decisione:** si può passare alla preparazione tecnica di M2. Non è corretto dichiarare M2 eseguito.
