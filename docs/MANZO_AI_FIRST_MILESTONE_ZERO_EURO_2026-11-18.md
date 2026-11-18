# MANZO AI / Mission Studio — Primo traguardo · Budget 0 €

**Data:** 18 novembre 2026  
**Obiettivo concordato:** 1) stabilizzare il deploy GitHub Pages e i controlli di AI Teaching Lab; 2) preparare un prototipo tecnico IA per Mission Studio, senza attivazione pubblica né costi.

## Esito verificato

### Pubblicazione MANZO AI — PASS

- `Deploy MANZO AI` run **44281580560** (`ba03bc0`): `completed / success`, dopo le correzioni ai test che bloccavano il sito.
- `Deploy MANZO AI` run **44287800914** (`6b31b58`): `completed / success`, **dopo** l'introduzione del prototipo Mission Copilot e del relativo test gate.
- `AI Teaching Lab — editorial and preview QA` run **44287800740**: `completed / success`.
- Log `44287800914`: `node --test product/mission-copilot/worker.test.mjs` ⇒ **8 test, 8 PASS, 0 FAIL**.
- Gli stessi log riportano: publisher AI Teaching Lab PASS, controlli sui quattro Studi/Workspace PASS, verifiche home IT/EN/ES PASS, audit di integrità sito PASS e configurazione GitHub Pages completata.
- **Non verificato:** rendering nel browser Safari iPhone dell'ultimo commit e qualità pedagogica sperimentale; non dedurre usabilità da un workflow verde.

Run GitHub verificati:
- https://github.com/manzo8b/manzo-ai/actions/runs/44287800914
- https://github.com/manzo8b/manzo-ai/actions/runs/44287800740
- https://github.com/manzo8b/manzo-ai/actions/runs/44281580560

### Prototipo IA privato — PREPARATO, NON ATTIVATO

Source:
- `product/mission-copilot/worker.mjs`: Cloudflare Worker, schema `mission-copilot-v0.1`, proposta didattica generativa con output JSON strettamente controllato.
- `product/mission-copilot/worker.test.mjs`: otto test unitari su risposte fittizie; nessuna inferenza reale.
- `product/mission-copilot/wrangler.toml`: `COPILOT_ENABLED="false"`, `workers_dev=false`, nessuna route pubblica.
- `product/mission-copilot/README.md`: limitazioni tecniche, budget, accesso privato e documentazione.

Controlli previsti:
- Rifiuta ogni richiesta di generazione se disattivato, senza secret valido o senza binding IA.
- Richiede token per anteprima privata; non è previsto alcun token nel frontend.
- Accetta solo JSON di dimensione limitata e categorie di pubblico/durata/risorsa previste.
- Blocca alcuni pattern di dati personali (contatti), ma **non certifica** l'assenza di dati identificabili.
- Verifica la forma del JSON restituito dal modello; l'output resta **non approvato** fino al controllo docente.
- Non conserva dati, non offre CORS pubblica e non inserisce alcuna API nella pagina GitHub Pages.
- Un modello non disponibile, un output invalido o quota esaurita causano errore, non un'approvazione fittizia.

**Nessun modello IA è stato invocato durante questo traguardo.** Cloudflare non è stato collegato o configurato sull'account utente e nessun deployment Worker è stato eseguito.

## Budget autorizzato
- Massimo **€0**. Cloudflare Workers AI Free dichiara 10.000 Neurons/giorno, non IA illimitata. Superata la quota Free, le richieste falliscono; non occorre usare Workers Paid.
- Modello candidato da riconfermare prima dell'uso reale: `@cf/google/gemma-4-26b-a4b-it`. Il catalogo cloud e il prezzo sono soggetti a modifiche.
- Non attivare billing, piano Workers Paid, crediti prepagati, account a pagamento, upgrade automatici, video IA o infrastruttura di archiviazione a pagamento.
- `max_completion_tokens` è un limite per richiesta, **non** un tetto giornaliero globale: prima di aprire l'endpoint al pubblico servono un meccanismo distribuito di rate limiting, protezioni antiabuso e monitoraggio dell'uso.

Riferimenti:
- https://developers.cloudflare.com/workers-ai/platform/pricing/
- https://developers.cloudflare.com/workers-ai/models/gemma-4-26b-a4b-it/

## Gate successivo — non eseguito
1. Audit visuale reale iPhone Safari + desktop della HOME, Mission Studio e dei laboratori, con screenshot prima/dopo.
2. Valutare con il titolare soltanto **l'eventuale connessione a Cloudflare Free**; non creare account o collegare strumenti senza suo intervento esplicito.
3. Aggiungere autenticazione adeguata e contatore globale distribuito prima di qualunque chat pubblica; il token privato non deve essere condiviso nei browser.
4. Collegare il brief di Mission Studio all'output IA con consenso esplicito e avviso privacy, **senza** inviare dati al backend finché non sono presenti tutte le protezioni.
5. Misurare qualità delle proposte su casi sintetici e la percentuale di correzioni necessarie, senza simulare risultati di test con docenti.

**Verdetto:** infrastruttura di pubblicazione verificata, prototipo IA privato predisposto e testato con mock a costo zero. IA pubblica **non disponibile né pubblicizzata**.
