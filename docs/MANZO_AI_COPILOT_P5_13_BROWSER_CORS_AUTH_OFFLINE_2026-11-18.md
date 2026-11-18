# Mission Studio — P5.13 · Collegamento browser protetto (solo sorgente)

**18 novembre 2026 · Audit MANZO AI / Mission Copilot · Decisione: NON DISTRIBUIRE**

## Sintesi verificabile

Questa fase prepara un percorso `Mission Studio → Supabase session → Worker → Supabase Auth → quota globale → Workers AI Gemma 4`. È una **integrazione solo nel codice**, con fixture di test; **non** è installata in GitHub Pages, non esiste un endpoint reale configurato e non sono state effettuate chiamate al modello dall'account Cloudflare.

Piano Workers Free e progetto Supabase Free sono stati mostrati o verificati nelle sessioni precedenti. La schermata Cloudflare Zero Trust Free ha richiesto un metodo di pagamento: tale opzione **non** è stata sottoscritta. La selezione Supabase è quindi una proposta tecnica alternativa, non una autorizzazione a pubblicare.

## Confini tecnici

### 1. Autenticazione e autorizzazione non sono CORS

- `Origin` viene verificato **esattamente** contro `https://manzo8b.github.io`; nessun `*`, origine null, sottodominio simile, schema HTTP o porta alternativa.
- Un'origine è `schema + host + porta`, **NON** include il percorso `/manzo-ai/`. Tutti i siti serviti dalla stessa origine GitHub Pages sono indistinguibili per CORS. In particolare CORS non autorizza l'utente, non blocca chiamate server-to-server e non garantisce la privacy.
- Il controllo principale resta la verifica del token con il **servizio remoto Supabase Auth** sul solo progetto MANZO AI e la piccola allowlist server-side di UUID dei tester. Non ci si fida dell'ID utente, email o ruolo riportati dal browser.
- L'HMAC dell'UUID verificato alimenta il contatore del Durable Object e non è inviato al modello.

### 2. Nuovo gate browser, disattivato

`wrangler.toml` ora contiene `BROWSER_CONNECTION_CONFIRMED = "false"`. L'accesso browser richiede `true` **insieme** a consenso privacy, piano Free, modello Free, beta sintetica, provider Supabase e conferma Auth.

`OPTIONS /api/plan` viene servito soltanto quando tutti i gate sono veri, con intestazioni limitate a `authorization, content-type` e metodo `POST`; gli altri metodi/origini/intestazioni non sono autorizzati. Non chiama Auth, Durable Object né Workers AI.

`POST /api/plan` con origine approvata riceve risposte JSON leggibili dal browser anche in caso di 401, 429, 502 e 503. Le altre origini non ottengono `Access-Control-Allow-Origin`.

### 3. Client browser di prova, NON importato

`product/mission-copilot/private-browser-client.mjs` è uno **scheletro disattivato**. `PRIVATE_BROWSER_CONFIG` include `enabled:false` e `endpoint:null`. La pagina pubblica non lo carica.

Nelle prove offline con un finto Supabase SDK:
- Legge un token di sessione temporaneo con `getSession()` ma **non si fida della session.user presente nel browser**.
- Invia solo `{ "scenarioId": "water_cycle" }` (o un altro ID dei quattro casi fittizi).
- Non invia testo libero, obiettivi di studenti, email, cookies, credenziali permanenti o URL da query.
- Rifiuta endpoint HTTP, con query, hash, password in URL o host non appropriati.
- Gestisce 401 (autenticazione), 403 (origine), 429 (quota), 503 (servizio), JSON non valido e risposte che pretendono `teacherApproval=true` attraverso codici applicativi privi di stack trace.
- La risposta resta **una bozza non approvata**: il docente deve sempre correggerla e approvarne l'utilizzo.

Non è stata aggiunta alcuna interfaccia che consenta al visitatore di abilitare la modalità reale. Il client non possiede una route o un hostname del Worker: **nessuna chiamata di rete operativa è possibile nella configurazione del repository**.

## Sicurezza e limiti residui

1. **Endpoint reale:** `workers_dev=false` e nessuna route; per funzionare nel browser servirà una futura decisione esplicita di pubblicare un URL tecnicamente raggiungibile, protetto da autenticazione applicativa e limitazioni. Il dominio `workers.dev` può essere gratuito ma, se abilitato, è pubblicamente indirizzabile e suscettibile di abuso.
2. **Protezione abuso pre-auth:** il Rate Limiting Cloudflare è approssimativo e locale per PoP, non globale né immunità agli attacchi DDoS. Serve verifica del binding e namespace reali prima del deploy.
3. **Origini condivise:** `manzo8b.github.io` contiene altri progetti; non esiste isolamento per percorso in CORS. Valutare un dominio dedicato in futuro **solo se compatibile con €0**, senza acquisti.
4. **Sessioni:** il token breve (1 ora secondo dashboard) non impone la fine di sessioni rinnovabili; durata massima, revoca, browser storage e interfaccia di logout devono essere esaminati prima dell'utilizzo reale.
5. **Privacy:** una futura beta dovrà documentare controlli contrattuali, logging, ruoli di trattamento, data retention, cookie e le informative. Quattro casi sintetici non autorizzano dati effettivi di studenti.
6. **Sicurezza del contenuto:** output AI va validato scientificamente da un docente. Il controllo dei dati identificabili è euristico, NON un filtro affidabile per contenuti di minori.
7. **Costi:** piano Workers Free, Neurons, eventuale limite CPU e Durable Objects Free devono essere controllati nella dashboard prima dell'eventuale primo test. Nessuna attivazione di Paid o carte.

## Testing

- `browser-origin.test.mjs`: preflight consentito solo per l'origine autorizzata; blocco di origini simili, nulle, con metodo errato o header extra; gestione errori e default OFF.
- `private-browser-client.test.mjs`: client spento, input sintetico, sessione mancante, endpoint invalido, chiamate simulate, errori e verifica bozza.
- `worker.test.mjs`: esecuzione `OPTIONS` senza auth/AI e blocco delle richieste `POST` provenienti da origini non approvate.
- `zero-euro-preflight.test.mjs`: assicura che il gate browser resti `false` e che il controllo origine avvenga prima del filtro e dell'autenticazione.

**Tutte le prove sono offline con `node --test` in GitHub Actions. Non includono un browser reale, una login session reale, chiamate a Supabase, inferenze Gemma o deploy.**

## Checklist per il confronto con il proprietario (P5.14 / rilascio futuro)

- [ ] Conferma esplicita che il primo accesso reale userà un **solo tester** già verificato.
- [ ] Valutazione informativa e condizioni di servizio per Supabase/Cloudflare, nessun dato di studenti.
- [ ] Controllo dei limiti reali, dei costi a consumo, delle quote DO e del namespace Rate Limiting.
- [ ] Scelta di hostname Worker / routing che consenta revoca immediata e non richieda servizi a pagamento.
- [ ] Configurazione sul provider dei segreti e dell'allowlist, **mai** nel repository.
- [ ] Prova privata di `OPTIONS`, errore 401 con origine autorizzata, 429, 503 e differenza fra origini ammesse/non ammesse.
- [ ] Una sola inferenza sintetica autenticata, Neurons misurati e output validato.
- [ ] Solo dopo, valutazione dell'eventuale UI di Mission Studio: mai attivare il client nel sito per semplice modifica di query.

## Fonti ufficiali

- https://developers.cloudflare.com/workers/examples/cors-header-proxy/
- https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/
- https://developers.cloudflare.com/workers/configuration/routing/workers-dev/
- https://supabase.com/docs/reference/javascript/auth-getuser
- https://supabase.com/docs/guides/auth/sessions
- https://supabase.com/docs/guides/auth/redirect-urls

**Verdetto:** P5.13 source-only verificabile, P5.14 e rilascio reale NON autorizzati. `main` e il sito GitHub Pages rimangono invariati.
