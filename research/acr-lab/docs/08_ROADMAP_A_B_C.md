# Roadmap essenziale ACR (tre programmi)

## P0 — Fondazioni già disponibili
- v0.6: engine di memoria, schema, trace store SQLite, verifica Playwright sintetica, audit, 30 test software.
- v0.7: corpus dell'utente preservato, programma A/B/C, protocolli separati, manifest, verifiche statiche di disegno.
- **Nessuna evidenza sperimentale** che memoria, scheduling o rapporto aureo migliorino un LLM.

## P1 — Esperimento A (priorità operativa)
1. Realizzare una pipeline comune di modifica di pagine web su copie isolate con due modalità C2/C3.
2. Collegare prompt/output e conteggio token/costo a ogni trace, con storage sicuro.
3. Valutazione deterministica identica per entrambi i bracci; documentare copertura test.
4. Congelare task e prompt, lanciare 2 task pilot e correggere *strumentazione*, non selezionare casi favorevoli.
5. Eseguire studio esplorativo più esteso, rilasciare tabelle, intervalli e fallimenti.
6. Decisione go/no-go B sulla base di qualità, costo e regressioni (non una scelta promozionale).

## P2 — Esperimento C (scientificamente indipendente)
1. Definire task minimi invarianti, libreria di sezioni e protocollo di equivalenza semantica.
2. Fornire tokenizzazione esatta, limiti per campo, verifiche su ordine e riempimento.
3. Eseguire un pilot per valutare fattibilità dei prompt a rapporti diversi.
4. Studio Cα (task identico, varia impalcatura e lunghezza) + Cβ (totale fisso, cambiano proporzioni con equivalenza semanticamente controllata).
5. Se un massimo vicino a 62% compare, confronto ravvicinato 60/62/65 su compiti e modello indipendenti.
6. Pubblicare anche curva di sensibilità e analisi della lunghezza.

## P3 — Esperimento B (condizionato)
1. Solo se A ha mostrato utilità, oppure come progetto separato di puro scheduling se motivato esplicitamente.
2. Usare un orizzonte di 10 revisioni; checkpoint intensivi B-FIB=1,2,3,5,8 e controlli attivi/event-driven a parità di risorse.
3. Suite di sicurezza sempre a ogni revisione, audit approfondito soltanto nei checkpoint, con budget e soglie congelate.
4. Report audit cost/regressions/task success, fallimenti e ablation dei checkpoint.

## P4 — Prodotto, soltanto dopo la ricerca
- Prima UX: coda memorie con Approva / Rifiuta / Modifica, provenienza e diff dei risultati.
- Nessuna memoria approvata da LLM senza identità umana verificabile.
- Nessuna pubblicazione su siti o repository di produzione dai workflow di sperimentazione.

## Regola di responsabilità
Le sole evidenze esistenti sono test tecnici di strumentazione, non prove di efficacia ACR. Ogni cambiamento a ipotesi, set di task e analisi successivo al congelamento deve essere riportato come deviazione.
