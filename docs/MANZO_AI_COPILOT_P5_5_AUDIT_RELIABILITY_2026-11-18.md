# Mission Copilot — Audit P5.5 · Affidabilità prima del collegamento reale

**18 novembre 2026 · Branch di audit · Nessun deploy né inferenza dall'account · Budget massimo 0 €**

## Obiettivo

Preparare il Worker P4 a una futura singola inferenza privata con Gemma 4, senza attivare servizi e senza sostituire le protezioni già presenti. Questo documento descrive soltanto evidenze da codice, documentazione Cloudflare e schermate condivise dal titolare. Non è un verbale di collaudo live.

## Riscontri sul modello

- Identificativo: `@cf/google/gemma-4-26b-a4b-it`
- La guida Cloudflare per Workers AI mostra esplicitamente `chat_template_kwargs: { enable_thinking: false }` per questo modello. Il nostro limite applicativo rimane `max_completion_tokens: 650`.
- Cloudflare documenta una risposta `choices[0].message.content` con `finish_reason`, oltre alla forma legacy `response`.
- La pagina generale JSON Mode elenca modelli compatibili, **ma non include Gemma 4 nell'elenco esplicito** aggiornato nella pagina consultata. Perciò in P5.5 **non aggiungiamo `response_format`**: si conserva il vincolo testuale JSON e la validazione stretta; la compatibilità del JSON Mode con Gemma 4 va provata separatamente solo quando possibile.
- Un errore del Playground (`3045`) non dimostra né esclude un errore nella chiamata reale del Worker. La risposta `FUNZIONA` nel Playground prova la generazione di base del modello, non l'integrazione nel nostro account.

## Correzioni sul branch

1. **Controllo dell'output**: il Worker richiede esplicitamente `enable_thinking: false`; nessun aumento dei token massimi o della quota giornaliera.
2. **Controllo dell'esito**: per le risposte chat, rifiuta `finish_reason` diversi da `stop`, messaggi di rifiuto e contenuto assente; restano attivi i validatori per JSON malformato o incoerente.
3. **Regressioni**: test per risposta chat valida, risposta troncata, filtrata, rifiutata e formato errato.
4. **Preflight**: verifica statica che disattivare il ragionamento non venga accidentalmente annullato in futuro.
5. **CI isolata**: workflow GitHub Actions solo su branch audit/pull request o esecuzione manuale, senza deploy né contatto Cloudflare.

## Sicurezza invariata

- `COPILOT_ENABLED=false`
- `FREE_PLAN_CONFIRMED=false`
- `MODEL_FREE_CONFIRMED=false`
- `DATA_PROTECTION_CONFIRMED=false`
- `BETA_SYNTHETIC_ONLY=true`
- `workers_dev=false`, nessuna route pubblica e nessuna CORS pubblica
- Quattro `scenarioId` fittizi definiti sul server, nessun testo arbitrario di studenti
- Cloudflare Access tramite `ctx.access` e audience, HMAC server-only, quota globale atomica e cancellazione best-effort mediante alarm
- 20 richieste globali/giorno UTC, massimo 3 per tester, intervallo minimo 60 secondi
- Il risultato è sempre una bozza con `teacherApproval=false`; il docente conserva la responsabilità della revisione

## Evidenze dell'account

Dalle schermate del titolare, Workers Free è il piano corrente da $0 e il modello appare nel catalogo Cloudflare. Il Playground ha restituito almeno una risposta testuale valida. Non sono invece verificati l'utilizzo effettivo dei Neurons **nell'account**, la configurazione Zero Trust, né l'esecuzione `env.AI.run` dal Worker di Mission Copilot.

La configurazione reale di Zero Trust Free, secondo Cloudflare, richiede un controllo preliminare delle condizioni di onboarding e dei dati di pagamento. Nessun inserimento dati, upgrade o servizio a pagamento è autorizzato.

## Gate esterni prima di una sola inferenza privata

1. Confermare il piano Workers Free e l'assenza di servizi a consumo attivi
2. Decidere consapevolmente come configurare Cloudflare Access; nessuna disattivazione dell'autenticazione per aggirare l'onboarding
3. Verificare condizioni privacy, DPA, conservazione e log account/provider
4. Configurare segreti solo lato Cloudflare e protezione reale prima dell'eventuale endpoint
5. Misurare i Neurons consumati nella prima inferenza con uno dei quattro casi fittizi
6. Valutare pedagogicamente il risultato; nessuna pubblicazione pubblica o invio di dati degli studenti

## Fonti Cloudflare

- https://developers.cloudflare.com/workers-ai/get-started/workers-wrangler/
- https://developers.cloudflare.com/workers-ai/models/gemma-4-26b-a4b-it/
- https://developers.cloudflare.com/workers-ai/features/json-mode/
- https://developers.cloudflare.com/workers/configuration/cloudflare-access/
- https://developers.cloudflare.com/cloudflare-one/setup/
- https://developers.cloudflare.com/workers-ai/platform/pricing/

**Verdetto P5.5**: pronto per revisione delle patch e QA offline; **non pronto all'attivazione reale** senza risoluzione dei gate esterni.
