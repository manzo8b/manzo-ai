# MANZO AI · SaaS commercial architecture — ADR-001

**Data:** 2026-11-15  
**Stato:** PROPOSTA / NON DEPLOYED / Nessun costo attivato  
**Scopo:** rendere MANZO AI tecnicamente vendibile e trasferibile, evitando la falsa impressione che una demo GitHub Pages sia già un SaaS funzionante.

## 0. Decisione e limiti

GitHub resta fonte versionata, sistema CI e vetrina dimostrativa. Le funzionalità che elaborano dati degli utenti, utilizzano modelli AI, verificano licenze o accettano pagamenti **non** saranno implementate come codice client-only sulla pagina pubblica GitHub.

Un progetto Supabase connesso all'account è denominato **Oiko** ed è in stato inattivo; NON riutilizzarlo per MANZO AI. Prima di creare backend o ambienti fatturabili verificare le tariffe e ottenere consenso esplicito per i relativi costi. Nessun sistema di pagamento verrà attivato senza dati del titolare e configurazione fiscale/legale.

**Nota GitHub Pages:** controllare regole d'uso per siti principalmente commerciali; la piattaforma di vendita verrà ospitata su provider appropriato quando si passerà al lancio.

## 1. Architettura bersaglio

```text
GitHub (source, CI, editorial assets)
       |
       +--> Public marketing / demos (static hosting)
       |
       +--> SaaS app frontend (future managed hosting; exact provider TBD)
                  |
              Auth session
                  |
              Backend API / Edge Functions  <-----> AI model API (server-only secret)
                  |                   |
                  |                   +--> rate limits / token cost budgets
                  v
              Dedicated EU Postgres/Supabase project
                  | profiles
                  | organizations & memberships
                  | course catalog & enrollments
                  | learning_attempts & progress
                  | projects, agent_runs & output_artifacts
                  | plan entitlements & usage ledger
                  |
              Stripe Checkout (test mode initially)
                  |
              Signed, idempotent webhook -> server entitlements
```

Il frontend **non** conserva chiavi Stripe segrete, chiavi di servizio Supabase, credenziali di provider AI, o verifica abbonamenti mediante semplici parametri di URL.

## 2. Tre percorsi di prodotto da non confondere

**A — MANZO AI Learning.** Acquisto corso, accesso autenticato, quiz e progressi persistenti, attestato interno con significato dichiarato, gestione utenti team e report aziendali. Prima verticale per enti di formazione e aziende.

**B — MANZO AI Verify.** Registro di claim, fonti, verifiche e revisione; prove esportabili; possibile uso B2B per compliance, legal e quality assurance, senza automatizzare decisioni professionali riservate.

**C — MANZO AI Studio.** Workspace per progetto di sito, brief, template, output versionati, anteprima e pubblicazione controllata; agente AI che agisce solo dietro autorizzazioni definite. Rilascio successivo, perché è più complesso e ha costo di inferenza.

L'infrastruttura di identità e billing deve poter sostenere tutti e tre, ma il primo MVP vendibile deve avere **un solo workflow prioritario**, scelto sulla base della discovery commerciale.

## 3. Identità e multi-tenancy

- **auth.users**: identità gestite da provider dedicato; verifica email e strumenti anti-abuso.
- **organizations**: organizzazioni clienti e tenant isolati.
- **organization_members**: ruoli espliciti (owner, admin, instructor, learner); i ruoli non devono essere controllabili dalla richiesta del browser.
- **courses**, **course_versions**, **enrollments**, **learning_attempts**: contenuti versionati e progressi, con proprietà di organizzazione e utente.
- **projects**, **agent_runs**, **artifacts**: workspace e risultati, ogni record vincolato a un tenant.
- **billing_accounts**, **subscriptions**, **entitlements**: letture autorizzate, scritture unicamente lato backend dopo verifica provider.
- **usage_ledger**, **security_events**: costi, limiti, eventi di sicurezza, retention.
- **webhook_events**: eventi di pagamento con identificativo univoco e idempotenza.

I tenant devono essere separati anche per ricerche, letture, upload e log. **RLS deny-by-default su ogni tabella esposta**, query con tenant ID derivato dalla sessione verificata e test con due tenant isolati.

## 4. Pagamenti: regola fail-closed

1. Checkout avviato da endpoint backend con piano/prezzo deciso server-side.
2. Stripe Checkout in **test mode** nel primo sprint.
3. Il redirect di successo non sblocca accessi da solo.
4. Webhook firmato, evento univoco, gestione dei retry; subscription state da provider.
5. Entitlement aggiornato nel backend con log e controlli idempotenti.
6. Revoche, mancati pagamenti, rimborsi e dispute devono aggiornare gli accessi in modo coerente.
7. Billing e fatture devono passare verifica commerciale/fiscale prima di qualsiasi pagamento reale.

## 5. Agente AI operativo: controlli minimi

**Verticale proposta per il primo test:** assistente di verifica delle risposte con fonti utente, non agente autonomo di pubblicazione web.

- Input limitato per lunghezza, tipo file e contenuto; scansione upload.
- Nessuna chiave modello esposta nel browser.
- Allowlist di strumenti consentiti e nessun accesso indiscriminato a repository/segreti.
- Limite di spesa per utente/azienda, rate limiting, budget di token.
- Etichette chiare per claim e prove; una fonte citata non è prova automatica.
- Revisione umana prima di azioni permanenti o ad alto impatto.
- Prompt injection threat model, output sanitization, controlli autorizzativi e audit trail.
- Logging minimizzato; nessuna conservazione indiscriminata di dati sensibili; cancellazione ed export da progettare.
- Artefatti con stato e versione, non promesse di risultato di sistema mai eseguite.

## 6. Data protection e governance

Prima di registrare studenti o clienti: privacy notice, ruoli del trattamento, dati necessari, finalità, basi giuridiche, retention, cancellazione/export, subprocessor list e documenti contrattuali appropriati. L'hosting UE non garantisce da solo conformità GDPR: controllare regioni, trasferimenti eventuali e provider AI.

Se il sistema viene offerto come servizio su misura ai clienti, definire SLA, assistenza, responsabilità, sicurezza, limiti di garanzia e disaster recovery. Attestati corsi MANZO AI restano **interni**, mai descritti come certificazioni accreditate senza titolo valido.

## 7. Milestone di implementazione

**M0 · Decisioni e ricerca mercato** — buyer persona, 10 interviste, 2 demo, no pagamenti.

**M1 · Fondazioni tecniche** — nuovo progetto Supabase dedicato, schema migrazioni, RLS, test multi-tenant, autenticazione/staging, deploy non pubblico. Richiede approvazione delle eventuali spese.

**M2 · Learning MVP** — 1 corso, account studenti, enrollments, progressi salvati, console amministratore; nessun checkout live.

**M3 · Billing test** — Stripe Checkout test mode, webhook firmato, entitlements, test di cancellazione/rimborsi/retry, policy ed error handling.

**M4 · Agent MVP** — una sola capacità reale, limiti consumo, processore asincrono dove necessario, audit delle fonti e un flusso di approvazione.

**M5 · Lancio controllato** — hosting e dominio appropriati, documentazione legale, monitoraggio, backup, test di sicurezza, pagamenti live SOLO dopo configurazione e approvazione.

## 8. Criteri di accettazione verificabili

- Un account A **non** può leggere, aggiornare o creare dati nell'organizzazione B anche alterando richieste manualmente.
- Un utente senza entitlement valido **non** può consumare API o risorse a pagamento.
- Un redirect Checkout forgiato **non** concede accesso.
- Un webhook ripetuto **non** duplica iscrizioni o crediti.
- Nessuna chiave privata è inclusa nell'HTML o negli asset JavaScript pubblici.
- Tutti i task AI hanno limiti di costo, rate-limit e codice di errore esplicito.
- Pagamenti, cancellazioni e privacy workflows sono collaudati in test prima del go-live.
- Un deploy riuscito non è presentato come prova di sicurezza o di vendite.

## 9. Decisioni sospese e non attivate

- Dominio commerciale: non acquistato né verificato.
- Provider frontend managed: da scegliere tra soluzioni compatibili con SSR/serverless.
- Backend Supabase MANZO AI: **non creato** (progetto Oiko esistente mantenuto separato).
- Stripe account: **non collegato** e nessun pagamento attivato.
- API AI: provider e budget da definire.
- Mercato e prezzo: da validare con buyer reali.

## Riferimenti di lavoro
- EU AI Act Art. 4: https://digital-strategy.ec.europa.eu/en/faqs/ai-literacy-questions-answers
- NIST SSDF: https://csrc.nist.gov/pubs/sp/800/218/final
- Supabase RLS: https://supabase.com/docs/guides/database/postgres/row-level-security
- Stripe checkout/webhooks: https://docs.stripe.com/payments/checkout and https://docs.stripe.com/webhooks
- GitHub Pages service limitations: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
