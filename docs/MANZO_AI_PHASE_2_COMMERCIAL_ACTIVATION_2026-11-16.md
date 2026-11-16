# MANZO AI · Fase 2 — Attivazione controllata Learning B2B

**Data:** 16 novembre 2026  
**Stato:** proposta tecnica con primo adapter API implementato in codice, **non pubblicato né collegato ad account**  
**Vincolo:** preservare il restyling v1.3 approvato. Nessun cambiamento ai corsi, nessun pagamento o risorsa cloud creata.  
**Prima verticale:** Learning B2B. Studio e Verify restano distinti e non vengono anticipati con funzioni inesistenti.

## 1. Decisione architetturale raccomandata

| Strato | Scelta iniziale | Alternativa successiva |
|---|---|---|
| Marketing, Academy, dossier | GitHub Pages per l'attuale fase dimostrativa | Hosting statico commerciale dedicato |
| Accesso studenti e organizzazioni | Supabase Auth (account realmente verificati) | IdP esterno con standard aperti |
| Dati aziendali e progressi | Un **nuovo** progetto PostgreSQL Supabase in una precisa regione UE | PostgreSQL gestito indipendente |
| API privilegiata | Supabase Edge Functions / Deno, protetta da verifica JWT e controlli DB | Backend dedicato FastAPI o altro |
| Iscrizioni, quiz e posti | Le migration MANZO AI 0001 + 0002 già testate | Schema portabile PostgreSQL |
| Pagamenti futuri | Stripe Checkout + Billing, modalità test iniziale | Provider alternativo in base al mercato |
| Agenti AI | Fuori dall'MVP Learning v1, abilitazione successiva con quote e approvazione | Modello/provider intercambiabile |

**Non creare MANZO AI nel database Oiko.** È presente un solo progetto Supabase esistente, chiamato Oiko, inattivo nella regione Irlanda. Per separazione dell'asset e futura acquisibilità, è preferibile creare anche una **organizzazione Supabase separata** denominata MANZO AI e collocare lì il progetto dedicato. L'organizzazione condivisa crea dipendenze di fatturazione e governance.

### Regione

Preferire una regione AWS specifica dell'UE, come **eu-central-1 (Francoforte)** o **eu-west-1 (Irlanda)**. Evitare di presumere che una generica scelta «Europe» garantisca la permanenza nell'UE. La regione non è di per sé prova di conformità al GDPR.

Fonte: https://supabase.com/docs/guides/platform/regions

## 2. Tariffe verificate sui listini ufficiali

| Voce | Prova/staging | Produzione leggera | Note |
|---|---:|---:|---|
| Supabase Auth + DB + Edge Functions | **0 USD/mese** sul piano Free, entro le quote | **da 25 USD/mese** Pro, primo progetto Micro incluso | Importi in USD, escludono imposte e extras |
| Database Supabase | Free 500 MB | Pro 8 GB inclusi | Free sospende progetti dopo una settimana di inattività |
| Auth attivo mensile | Free 50.000 MAU | Pro 100.000 MAU inclusi | Non usare le quote come obiettivi o previsioni |
| Edge Functions | Free 500.000 invocazioni | Pro 2 milioni incluse | Oltre soglia Pro: 2 USD per milione di invocazioni, per pacchetti |
| Backup gestiti | Non inclusi sul Free | Backup giornalieri, retention 7 giorni Pro | Testare ripristino e disaster recovery |
| Stripe Payments | Nessun pagamento in test mode | 1,5% + 0,25 EUR per carta standard SEE | Altre carte/metodi hanno costi diversi |
| Stripe Billing (se si usano abbonamenti) | Nessun incasso in test mode | +0,7% del volume Billing | In aggiunta ai costi Payments |
| Dominio, email transazionale, API AI | Non ancora richiesti | Prezzi da stimare sul consumo/fornitore | Non sono inclusi nei 25 USD/mese |

Fonti ufficiali, controllate il 16/11/2026:
- https://supabase.com/pricing
- https://supabase.com/docs/guides/functions/pricing
- https://supabase.com/docs/guides/platform/manage-your-usage/edge-function-invocations
- https://stripe.com/it/pricing
- https://stripe.com/it/billing/pricing

**Stima prudenziale:** la prima piattaforma di autenticazione + DB + funzioni può essere sperimentata sul Free (0 USD/mese). Per un pilota aziendale con obblighi di disponibilità e backup, prevedere **almeno 25 USD/mese di piano Supabase**, più possibili domini, email, commissioni, fiscalità, sicurezza e supporto. Il prezzo mensile finale deve essere validato prima dell'attivazione.

Non usare Vercel Hobby come backend SaaS commerciale: i termini del relativo piano gratuito sono per progetti personali/non commerciali. In questa fase non è necessario alcun secondo host applicativo: le Supabase Edge Functions coprono la prima API Learning. Alternative Cloudflare Workers a 5 USD/mese e Vercel Pro da 20 USD/mese, se motivate tecnicamente, aumentano la base dei costi senza risolvere il bisogno principale (identità e database).

Fonti alternative: https://developers.cloudflare.com/workers/platform/pricing/ · https://vercel.com/pricing

## 3. Ciò che è già sviluppato

### Database PostgreSQL

La CI crea Postgres 16 temporaneo e applica:
- \`product/backend/migrations/0001_foundation.sql\`
- \`product/backend/migrations/0002_learning_b2b.sql\`

Le routine private proteggono licenze, quote, iscrizioni e valutazioni. I test coprono isolamento tenant e assegnazione concorrente dell'ultimo posto. Il superamento di quei test non prova ancora la sicurezza di un deployment Supabase reale.

### Primo API adapter (questo sprint)

\`product/backend/edge/learning-api/router.mjs\` è una policy HTTP **provider-neutral**: valida rigorosamente UUID, contenuto JSON e campi ammessi, non accetta punteggi né identità di sessione provenienti dalla richiesta, e rende gli errori senza esporre segreti.

\`product/backend/edge/learning-api/index.ts\` è un adapter **Supabase Edge Functions NON DEPLOYED**. Propone:
- autenticazione reale con \`withSupabase({auth:'user'})\` e identità derivata da \`ctx.userClaims.id\`;
- query di lettura sotto ruolo PostgreSQL \`authenticated\` e \`request.jwt.claim.sub\` impostato soltanto nel contesto transazionale;
- comandi di scrittura attraverso le funzioni SQL private già verificate su due tenant;
- CORS con singolo origin esplicito, nessun \`*\`, payload limitato, query SQL parametrizzate, credenziali PostgreSQL solo in variabili segrete dell'ambiente backend;
- nessun collegamento ai pagamenti o agli agenti AI.

La sola presenza del file Deno **non rende attivo un endpoint reale**. Non è ancora stato testato con JWT, rete e ruoli di un progetto Supabase appena creato.

### API v0.4 (scope limitato)

Operazioni previste dalla prima versione: elenco corsi, elenco progressi, assegnazione/rilascio posto, iscrizione, completamento modulo, invio risposte quiz con score computato dal database. Il contratto in \`product/backend/contracts/openapi.json\` identifica espressamente ciò che è implementato in source e ciò che rimane solo progettato.

## 4. Blocco prima di creare account realmente utilizzabili

- [ ] Esiste un'organizzazione Supabase MANZO AI distinta da Oiko
- [ ] Regione UE specifica e piano Free/Pro scelti con costo noto
- [ ] Proprietario conferma eventuali addebiti: **nessuna spesa autorizzata in questo sprint**
- [ ] Progetto creato e ambiente di staging separato dalla Home pubblica
- [ ] Firma JWT, inviti/email, rotazione e revoca sessioni verificati end-to-end
- [ ] RLS esercitata con utenti reali di due organizzazioni, compreso tentativo cross-tenant
- [ ] Prove di pagamento esclusivamente in **Stripe test mode**, dopo accordo esplicito
- [ ] Audit provider su DB secrets, default privileges, accesso \`app_private\`, query CORS e limiti
- [ ] Policy privacy, durata dati, richieste di accesso/cancellazione, DPA, registro trattamento e backup completati
- [ ] Monitoraggio, rate limit server-side e test di restore verificati
- [ ] Test Android/iOS, tastiera, focus, accessibilità e regressione del design approvato

## 5. Mercato e ricavi: ipotesi da validare (non clienti acquisiti)

**Prima buyer persona:** responsabile formazione di PMI/agenzia digitale che impiega AI nel lavoro quotidiano e vuole documentare formazione e verifiche, senza comprare una piattaforma didattica enterprise sovradimensionata.

**Seconda:** società di consulenza formazione e compliance che richiedono corsi versionati, assegnazione a team e report ripetibili.

**Terza:** software house che intendono addestrare sviluppatori a non consegnare codice AI senza test e revisione; offrire il percorso Engineering Assurance come prodotto verticale.

Per iniziare: 10–15 interviste esplorative con buyer reali, due proposte di pilota B2B ben delimitate, nessuna promessa di certificazione accreditata, un solo prezzo sperimentale validato sul mercato. Non confondere traffico GitHub con clienti, fatturato o product-market fit.

## 6. Release gate e decisione successiva

Il completamento del presente sprint significa **codice sorgente del primo adapter + CI e preventivo ragionato**, NON attivazione del SaaS.

La scelta necessaria prima della fase successiva è: autorizzare un **nuovo spazio MANZO AI** in Supabase, in una regione UE specifica, inizialmente con un budget **0 USD/mese (Free)** salvo limiti e conferme del provider. Nessun sistema già esistente sarà modificato.

Il successivo sprint tecnico configurerà auth, migrazioni e test con **account di prova reali**, poi collegherà l'area studente senza intaccare homepage e corsi pubblici approvati.
