# MANZO AI Learning B2B — MVP tecnico v0.3

**Stato:** funzioni PostgreSQL verificate soltanto nel database temporaneo della CI. **Nessun account, licenza commerciale, database Supabase o pagamento live attivato.**  
**Data:** 15 novembre 2026  
**Repository:** `manzo8b/manzo-ai`, branch `main` dopo integrazione della PR.

## Prodotto

Learning B2B è la prima verticale della piattaforma MANZO AI. Non è soltanto un elenco di lezioni: si propone di gestire imprese clienti, studenti, accessi, progressi e valutazioni verificabili, con funzionalità commerciali che saranno integrate progressivamente.

### Utenti e permessi previsti

| Ruolo | Lettura e operatività prevista |
|---|---|
| Owner / Admin aziendale | Visualizza tenant, membri, iscrizioni, progressi del team; assegna e libera posti tramite backend autorizzato |
| Instructor | Può iscrivere studenti già licenziati ai corsi pubblicati; non può modificare limiti e licenze |
| Learner | Visualizza solo i propri progressi, risultati e iscrizioni; contenuti riservati solo con licenza valida |
| Backend attendibile | Gestisce scritture, quota posti, punteggio quiz, registrazioni audit e future licenze |
| Utente anonimo | Nessun accesso ai dati aziendali |

Non sono ancora disponibili dashboard, inviti via email, account realmente autenticati, provisioning automatizzato né gestione contrattuale.

## Cosa è implementato (in SQL)

La migrazione `migrations/0002_learning_b2b.sql` introduce:

- `app_private.learning_seats`: assegnazione di una licenza per membro/azienda, non per singolo corso
- `app_private.learning_modules`: elenco versionato dei moduli ammessi
- `app_private.assessment_items`: quesiti e opzioni corrette non leggibili dal browser
- `app.learning_progress`: completamenti persistenti riferiti a utente, corso, versione e modulo
- `app_private.learning_audit_events`: registro minimo degli eventi formativi privilegiati
- `app_private.has_learning_access`: verifica di posto assegnato, membership attiva e licenza non scaduta

Le seguenti funzioni **non** sono pubbliche: possono essere eseguite solo da un backend attendibile tramite ruolo `service_role` e sono coperte da test SQL.

| Funzione | Effetto e criteri |
|---|---|
| `assign_learning_seat(actor,org,student)` | Solo owner/admin; verifica membership, stato licenza, data di scadenza e quota con lock |
| `release_learning_seat(actor,org,student)` | Solo owner/admin; libera posto, revoca iscrizioni attive, mantiene storico progressi |
| `enroll_learning_student(actor,org,student,course)` | Solo owner/admin/instructor; verifica posto valido e corso pubblicato; idempotente |
| `complete_learning_module(actor,org,course,version,module)` | Accetta soltanto progressi validi del membro autenticato e li registra una sola volta |
| `record_learning_assessment(actor,org,course,version,assessment,answers)` | Verifica tutte le scelte sul server e calcola score 0–100; mai dai parametri client |

Il database nega scritture agli utenti autenticati e impedisce che una membership priva di licenza apra le versioni pubblicate riservate. Il catalogo dei corsi può restare visibile ai membri per scoperta e acquisto, ma i riferimenti ai contenuti sono protetti da policy specifiche.

### Dimostrazione eseguibile

La CI crea un database PostgreSQL 16 temporaneo e popola due aziende inventate, studenti simulati, un catalogo e una licenza di prova. Verifica:

- impossibilità di lettura cross-tenant da browser simulato
- limiti posti e utilizzo serializzato, compresa una prova con **due connessioni concorrenti** per un solo posto
- riassegnazione, blocco dopo revoca, divieto di iscrivere persone di un'altra azienda
- iscrizione e completamento ripetibile dello stesso modulo
- quiz con punteggio calcolato dal database e quesiti corretti mantenuti privati
- rigetto di risposte parziali, inesistenti e di versioni del corso non autorizzate
- permanenza dello storico dell'utente dopo la revoca
- nessun privilegio client su chiavi quiz, posti, progressi, billing e funzioni privilegiate

Esecuzione nel runner GitHub:

```bash
psql -v ON_ERROR_STOP=1 -f product/backend/tests/000_auth_fixture.sql
psql -v ON_ERROR_STOP=1 -f product/backend/migrations/0001_foundation.sql
psql -v ON_ERROR_STOP=1 -f product/backend/migrations/0002_learning_b2b.sql
psql -v ON_ERROR_STOP=1 -f product/backend/tests/010_rls_checks.sql
psql -v ON_ERROR_STOP=1 -f product/backend/tests/020_learning_b2b_flows.sql
python3 product/backend/tests/learning_seat_concurrency_smoke.py
python3 -m unittest discover -s product/backend/tests -p 'test_*.py' -v
```

`000_auth_fixture.sql` è esclusivamente un simulatore di identity provider, MAI da distribuire su Supabase.

## Architettura UI successiva

### Pannello organizzazione (amministratore)

Posti in licenza, posti utilizzati, scadenza, membri, corsi assegnati, percentuale di completamento, registri eventi. Nei dati personali e negli export si applicano accesso per ruolo, minimizzazione e controlli di retention.

### Area studente

Corsi autorizzati, progressi per modulo, risultati dei quiz verificati lato server, fonti e materiali didattici. Nessun calcolo di punteggi affidato a dati provenienti dal browser.

### Area docente

Elenco studenti iscritti, progressi e risultati nel solo tenant autorizzato; nessuna capacità di modificare una licenza aziendale.

## Limiti attuali / prima del go-live

1. Una funzione SQL non sostituisce un API backend autenticato. **I parametri actor devono derivare da un token verificato server-side**, non da un modulo del browser.
2. Le policy RLS sono testate su PostgreSQL isolato; richiederanno nuova convalida sull'esatta versione/configurazione Supabase scelta.
3. Un controllo quota per posti è stato implementato, ma non il motore di abbonamenti, checkout Stripe, fatture, proroghe contrattuali o riallocazioni automatiche.
4. Domande e risposte ufficiali richiedono pubblicazione e versionamento controllati dall'editore; le cifre di punteggio non certificano competenze accreditate.
5. Inviti, gestione sessioni, reset password, privacy, logging operativo, backup e disaster recovery non sono ancora implementati.
6. Il **Product Lab GitHub Pages** rimane una demo non transazionale e non raccoglie dati.

## Migrazione e valore commerciale

Gli schemi SQL, il contratto API OpenAPI e la CI sono asset separati e versionati. Il progetto è quindi più trasferibile a provider diversi da GitHub Pages e dispone di una prima dimostrazione dell'isolamento dei clienti.

Per valutare la vendibilità richiederemo successivamente: casi d'uso pilota, utenti reali con consenso appropriato, dati di attivazione e retention, contratti, unit economics e un controllo esterno di sicurezza.

## Cosa serve per la prossima fase

- Selezione e approvazione del provider/backend dedicato MANZO AI, regione UE e budget massimo
- Configurazione dell'identità e API con credenziali server-side
- Test end-to-end su account reali *di prova*, non su credenziali simulate
- Prima UI amministratore e studente collegata ai nuovi endpoint
- Checkout Stripe esclusivamente in modalità test, solo dopo revisione dell'architettura

**Non si riutilizza né modifica il progetto Supabase Oiko.**
