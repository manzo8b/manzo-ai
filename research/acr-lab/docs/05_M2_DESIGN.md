# M2 · Confronto pilota C2/C3 — specifica di implementazione

**Stato:** disegno sperimentale; nessun risultato C2/C3 acquisito.

## Esperimento minimo

Due task web indipendenti su copie di test, stesso modello/versione e stesse condizioni, ordine randomizzato e ripetizioni. Un progetto **non deve** scrivere nella directory o memoria dell'altro braccio.

### Input comuni

- Specifica utente; ultima versione corrente; feedback dell'utente; output della stessa checklist deterministica.
- Stesso numero massimo di revisioni, tetto complessivo di token, timeout e strumenti.
- Medesimo prompt di editing, oltre alla sola differenza del contesto extra.

### Braccio C2

Riceve la richiesta e la checklist; non recupera memorie persistenti.

### Braccio C3

Riceve input **identico** a C2 più dati di memoria provenienti da record `verified/approved` eleggibili per ambito, finestra di due revisioni e budget prefissato. La memoria non è mai istruzione di sistema. Il budget totale di token rimane identico a C2.

### Isolamento

Memorie e tracce C3 devono essere partizionate per `(task_id, replicate, arm)`; nessuna memoria del risultato di C2 deve essere disponibile a C3 durante l'esecuzione. Non usare memorie ricavate da altre repliche o dal set finale di validazione.

### Metriche obbligatorie

- transizioni PASS→FAIL / PASS eleggibili, test mancanti come `missing`, non `pass`;
- percentuale finale di test superati e completamento del task;
- token input/output, costi del provider, numero revisioni;
- memorie selezionate, escluse per budget e prove che ne giustificano lo stato;
- divergenze di test/catalogo e deviazioni dal protocollo.

## Gate per avviare M2

- [ ] Runner capace di applicare modifiche AI in un workspace di test isolato
- [ ] Provider LLM configurato e consumi tracciati (senza chiavi in repo)
- [ ] Catalogo Playwright + axe-core versionato
- [ ] Contenuti prompt versionati tramite hash e deposito protetto
- [ ] Policy di selezione delle memorie e autenticità delle evidenze testata
- [ ] Due task pilota definiti e congelati prima dei run
- [ ] Nessun accesso in scrittura ai siti MANZO AI pubblici o ai repository produzione

Non aggiungere Fibonacci all'Esperimento A.
