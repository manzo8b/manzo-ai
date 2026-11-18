# MANZO AI · Mission Copilot · P5.12 — Protezione preliminare contro abusi

**18 novembre 2026 — sviluppo offline, branch di audit, costo effettivo di deployment/inferenze 0 € (nessuna distribuzione o invocazione remota).**

## Risultato

È stato predisposto un filtro *prima* della verifica del bearer token da parte di Supabase Auth nel Worker di Mission Copilot. Questo evita che ogni tentativo anonimo, contraffatto o eccessivo determini necessariamente una richiesta verso `/auth/v1/user`.

L'identità Supabase (P5.7) è ancora **disabilitata** nei file di configurazione. Cloudflare Access resta il provider di default, il Worker è `workers_dev=false` e non possiede route pubbliche. Le autorizzazioni `COPILOT_ENABLED`, `FREE_PLAN_CONFIRMED`, `MODEL_FREE_CONFIRMED`, `DATA_PROTECTION_CONFIRMED` e `SUPABASE_AUTH_CONFIRMED` rimangono `false`. È proibita qualsiasi inferenza con contenuti reali degli studenti.

## Scelta tecnica

**Workers Rate Limiting binding (Cloudflare)**, fissato nel `wrangler.toml`:

- Nome: `PRE_AUTH_LIMITER`
- Configurazione: **12 richieste / 60 secondi / sede Cloudflare**
- Identificativo namespace: `51218` (da verificare come univoco nell'account prima di un deploy)
- Chiave interna: `mission-copilot:preview:supabase:preauth:v1`
- Nessun indirizzo IP, email, identificativo studente o bearer token viene inserito nel contatore

Poiché la prima beta è destinata a un solo tester, il limiter usa una chiave condivisa per tutte le richieste `/api/plan` con provider Supabase. È intenzionale: una moltitudine di IP non deve ottenere quote per-IP separate sul medesimo PoP. **Compromesso:** anche un utente autorizzato può essere temporaneamente bloccato se altri utenti hanno consumato il limite locale (rischio di denial of service). La scelta sarà rivalutata prima di scalare oltre il primo tester.

Il servizio Cloudflare documenta che i limiti di questo binding sono **approssimativi e locali ai data center**: non garantiscono una quota esatta su scala mondiale né protezione totale da attacchi distribuiti. **Non** vengono usati per contabilizzare le inferenze, che sono ancora limitate dal Durable Object `GLOBAL_QUOTA` con una transazione atomica (20 al giorno globali, 3 al giorno per tester, minimo 60 s).

## Risposte applicative

| Condizione | HTTP | Risposta | Invocazione Supabase / AI |
| --- | --- | --- | --- |
| Limite disponibile | continua | Verifica sessione Supabase sul server | Solo se i gate di sicurezza lo consentono |
| Limite superato | 429 | `PRE_AUTH_RATE_LIMIT` | Nessuna |
| Binding assente, errore o risposta invalida | 503 | `PRE_AUTH_RATE_LIMIT_UNAVAILABLE` | Nessuna |
| Flag beta/piano/privacy spento | 503 | Codice di blocco già presente | Nessuna |
| Auth Supabase fallita, limitazione superata non presente | 401 | `SUPABASE_AUTH_REQUIRED` | Nessuna AI |

Il client riceve sempre JSON senza stack trace, credenziali o dati personali, con `Cache-Control: no-store`. Le risposte 429/503 non possono aggirare né prenotazione della quota AI né verifiche dell'identità.

## Modifiche su GitHub

1. `product/mission-copilot/preauth-rate-limit.mjs`: singola chiave, controllo fail-closed `env.PRE_AUTH_LIMITER.limit()`.
2. `product/mission-copilot/worker.mjs`: filtro applicato esclusivamente al percorso Supabase, **prima** di `authenticatedSupabasePrincipal()`.
3. `product/mission-copilot/wrangler.toml`: binding con `limit=12`, `period=60`. Gli altri flag restano disattivati.
4. `product/mission-copilot/preauth-rate-limit.test.mjs`: controlli di disponibilità, rifiuto, valore inatteso, errore e assenza del binding.
5. `product/mission-copilot/worker.test.mjs`: fixture offline che provano il rifiuto 429/503 **prima** di chiamate esterne e la sequenza `limiter → Supabase mock → quota Durable Object mock → Gemma 4 mock`.
6. `product/mission-copilot/zero-euro-preflight.mjs` e test: assert statici su presenza del limiter e ordine dei controlli.
7. Workflow GitHub Actions QA locale: include nuovi test Node, **nessun deploy, token o chiamata AI remota**.

## Rischi non ancora risolti

- Questo limite non è una WAF, non sostituisce CAPTCHA o un controllo anti-bot specifico e non impedisce a un attaccante distribuito di esaurire la quota Workers Free (100.000 richieste al giorno).
- La disponibilità del Rate Limiting binding e l'identificativo namespace nell'**account personale** devono essere confermati prima di distribuirlo. Non è stata effettuata una prova live di funzionalità, tempi o tariffazione.
- Mancano il controllo dell'origine CORS esatta, la scelta definitiva dell'endpoint protetto e un test browser end-to-end; si valuterà una protezione ulteriore se necessaria.
- La verifica Supabase `/auth/v1/user` non è stata eseguita dal Worker in produzione. Gli access token e le sessioni possono essere rinnovati; solo la verifica del server e l'allowlist sono utilizzabili per l'autorizzazione.
- La privacy (informativa, DPA, log, data retention, segreti), l'approvazione dei flag Free, e la misura reale dei Neurons restano gate separati.
- La presenza di un binding non autorizza un Worker pubblico; le PR rimangono in bozza senza merge.

## Fonti ufficiali

- https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/
- https://developers.cloudflare.com/workers/platform/limits/
- https://developers.cloudflare.com/workers/platform/pricing/
- https://supabase.com/docs/guides/auth/rate-limits
- https://supabase.com/docs/guides/auth/sessions

**Verdetto P5.12:** implementazione del controllo pre-auth e QA offline completabili senza Codex; non equivale a deploy, protezione live o prima inferenza reale. Ulteriori autorizzazioni necessarie prima dell'attivazione.
