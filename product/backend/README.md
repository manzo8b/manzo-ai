# MANZO AI · Backend Foundation v0.1

**Stato:** migrazione SQL e test automatici pronti, nessun database MANZO AI attivato.  
**Destinazione prevista:** progetto PostgreSQL/Supabase esclusivo, nella regione da scegliere.  
**Non eseguire su Oiko o su altri database esistenti.**

## Principio di sicurezza

L'organizzazione (tenant) non è una stringa affidabile inviata dal browser. Nel runtime Supabase l'identità arriva da una sessione autenticata e `auth.uid()`. Le autorizzazioni sono controllate da PostgreSQL mediante RLS e una tabella server-managed di membership. Non si usano valori scrivibili dall'utente nei JWT come prova del ruolo.

**Attenzione:** il fixture CI usa deliberatamente `SET request.jwt.claim.sub` per simulare utenti. Questo non è un modello di autenticazione per un'app che permetta connessioni SQL dirette. Solo uno strato affidabile deve tradurre JWT verificati in sessioni database.

## Schemi e dati

- `app.organizations` — tenant/organizzazioni clienti.
- `app.memberships` — utenti e ruoli aziendali; solo i responsabili possono leggere l'elenco della propria organizzazione.
- `app.courses` — catalogo; bozze visibili solo a owner/admin.
- `app.course_versions` — versione pubblicata o bozza (con riferimenti al contenuto esterno); studenti vedono solo versioni pubblicate.
- `app.enrollments` — assegnazione studenti; l'utente vede le proprie iscrizioni.
- `app.learning_attempts` — risultati verificati in backend, riferiti a corso, versione e utente corretti.
- `app.agent_runs` — soli metadati minimi relativi alle esecuzioni future, non il testo dei prompt.
- `app_private.feature_grants` — stato e limiti delle licenze; non esposto al browser.
- `app_private.feature_usage` — consumi per organizzazione; incremento atomico da implementare lato backend.
- `app_private.billing_events` — registro eventi provider con chiave unica, per idempotenza.

Tutte le tabelle usano RLS con politica di accesso restrittiva; `app_private` NON è uno schema da esporre via PostgREST. I client ricevono soltanto i grant SELECT alle risorse autorizzate, nessuna scrittura diretta.

## Contratto API portabile (solo progettazione)

Il file [`contracts/openapi.json`](contracts/openapi.json) definisce le future API per consultazione corsi e iscrizioni, invio risposte con **valutazione server-side**, licenze derivate dal backend, avvio controllato dell'agente e Checkout con prezzo determinato **soltanto dal server**. L'endpoint webhook dovrà validare la firma su raw body e l'idempotenza.

**Non esiste oggi nessun endpoint HTTP attivo.** Il contratto OpenAPI serve a verificare ora le superfici di autorizzazione e a mantenere la migrazione indipendente dal provider. I test automatici rifiutano campi di prezzo/punteggio/budget inseriti dal browser.

## Importante prima della migrazione in Supabase

1. Creare **un progetto MANZO AI nuovo**, con regione, piano e policy di trattamento dati approvati.
2. Fare backup e rileggere la migration; non eseguire sul progetto Oiko.
3. Verificare la presenza e il significato dei ruoli Supabase `authenticated`, `anon`, `service_role` e della funzione `auth.uid()`.
4. Non esporre `app_private` nei Data API schemas. Anche `app` può rimanere non esposto finché non sono completati test end-to-end con sessioni vere.
5. Verificare grants, default privileges, funzioni `SECURITY DEFINER`, eventuali limiti specifici della versione Postgres e comportamento con RLS.
6. Imporre che server/Edge Functions autorizzino ogni scrittura, calcolino punteggi, registrino ruoli e verifichino licenze. Non usare direttamente client per creare tentativi o entitlement.
7. Verificare policy con utenti autentici in due organizzazioni e con ruoli differenti; testare per abuso dei service role e revoca immediata.
8. Svolgere verifiche su retention, cancellazione dati, privacy, costi, audit, backup, osservabilità e test di ripristino.

### Sicurezza del billing

Il modulo `product/core/webhook_security.py` verifica localmente la firma HMAC SHA-256 dell'header Stripe, il timestamp e la struttura dell'input. **Non** attiva checkout, non riceve webhook via HTTP e non abilita abbonamenti. Quando implementato, l'endpoint dovrà usare i **byte originali** del body, verificare la firma server-side, registrare eventi in transazione con chiave unica, reagire a disdette/rimborsi e aggiornare i diritti in modo atomico.

La sicurezza dell'uso AI richiederà un ulteriore livello di quote con incremento atomico, budget e tool permissions. Il contratto Python `product/core/entitlements.py` è un modulo deterministico di riferimento, NON ancora collegato al database.

## Verifiche locali

Con PostgreSQL 16 locale (o runner CI isolato):

```bash
psql -v ON_ERROR_STOP=1 -f product/backend/tests/000_auth_fixture.sql
psql -v ON_ERROR_STOP=1 -f product/backend/migrations/0001_foundation.sql
psql -v ON_ERROR_STOP=1 -f product/backend/tests/010_rls_checks.sql
python3 -m unittest discover -s product/core/tests -v
```

Il fixture `000_auth_fixture.sql` crea un finto `auth.users` SOLO per test e non deve essere distribuito in produzione.

I test coprono isolamento delle organizzazioni, visibilità dei corsi, privacy dei risultati, permessi read-only, enforcement di versioni e idempotenza dell'identificativo evento. La suite Python copre anche policy degli accessi e integrità delle firme webhook.

Il superamento dei test è una condizione necessaria ma **non sufficiente** per dichiarare il SaaS sicuro, conforme o pronto alla vendita.

## Fonti tecniche

- Supabase Row Level Security: https://supabase.com/docs/guides/database/postgres/row-level-security
- Supabase database functions e SECURITY DEFINER: https://supabase.com/docs/guides/database/functions
- Stripe webhook signature verification: https://docs.stripe.com/webhooks/signature
- NIST Secure Software Development Framework: https://csrc.nist.gov/pubs/sp/800/218/final

## Passaggi successivi

1. Confermare budget/hosting/dominio di prova.
2. Eseguire migrazioni nel nuovo backend dedicato, non nel repository Oiko.
3. Collegare autenticazione con sessioni reali e politiche RLS verificate end-to-end.
4. Scegliere una verticale: Learning con accesso team e progressi, oppure Verify con claim e fonti; implementare operazioni server-side.
5. Collegare Stripe in **test mode** senza pagamenti reali; revisionare legal e fiscalità prima del live.
