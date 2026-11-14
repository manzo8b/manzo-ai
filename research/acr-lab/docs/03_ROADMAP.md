# 03 · Roadmap e criteri di avanzamento

Non procedere per settimane arbitrarie: ogni fase si conclude soltanto dopo aver verificato una *exit condition*.

## M1 · Osservabilità (v0.6: browser smoke completato su fixture, fase di integrazione reale parziale)

**Esistente:** schema di memoria, controller di prova, SQLite per run/eventi/test, metrica elementare di regressione, suite test software, esempio sintetico.

**Eseguito in v0.6:** Chromium/Playwright esegue sei test su quattro revisioni HTML sintetiche; eventi, hash SHA-256, versione browser, DB SQLite, screenshot e audit indipendente salvati.

**Da completare:** hashing reale dei prompt/output di LLM, monitoraggio di run incompleti, esportazione anonimizzata e verifiche su una copia di un sito reale.

**Exit condition:** tre revisioni di una copia reale di una UI dell’utente registrate senza perdita di eventi, con test identificabili e metriche riproducibili da un secondo esecutore. **Non ancora soddisfatta**: le fixture v0.6 sono sintetiche.

## M2 · Confronto C2/C3 (Esperimento A, fase pilota)

Implementare una checklist Playwright + axe-core; collegare il runner all'archivio. Aggiungere il retrieval del controller, memorie verificate da registro indipendente e stesso tetto di token per i due bracci. Eseguire almeno due task pilota **non conteggiati** nei risultati finali.

**Exit condition:** C2 e C3 eseguono gli stessi test sugli stessi task con tutti i costi tracciati e senza contaminazione delle memorie tra bracci.

## M3 · Valutazione e decisione

Congelare il protocollo, eseguire il dataset esplorativo e analizzare regressioni, successo finale, costi, errori di recupero e limiti. Pubblicare dati aggregati senza segreti e senza identificativi.

**Exit condition:** rapporto con differenze, intervalli, fallimenti, riproducibilità e decisione motivata: **proseguire**, **semplificare**, oppure **interrompere** la linea ACR.

## Dopo M3, solo se giustificato

Coda di approvazione `approva / rifiuta / modifica`, autenticazione e database transazionale delle memorie; poi eventuale esperimento B sui checkpoint Fibonacci. Non investire subito in UI complessa, multi-agent o promessa di un nuovo algoritmo di ragionamento.

## Caso d'uso scelto

Revisione iterativa delle interfacce web di MANZO AI e progetti dimostrativi derivati, **su copie di test**, non sui siti pubblici o repository di produzione. Test centrati su navigazione mobile, responsività, accessibilità e funzionalità dei form.


## Integrazione v0.7

Questo documento è la roadmap operativa originaria dell’Esperimento A. Per il programma scientifico **A, B e C** (incluso l’Esperimento C indipendente sulla quota impalcatura/compito), consultare `08_ROADMAP_A_B_C.md`. B è condizionato; C non richiede che A abbia esito positivo.
