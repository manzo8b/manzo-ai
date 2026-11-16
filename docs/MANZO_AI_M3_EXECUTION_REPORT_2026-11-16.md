# MANZO AI — M3 · Schema isolato, importazione transazionale e recovery gate

**Data:** 16 novembre 2026  
**Ambiente reale:** Supabase progetto MANZO AI `bjydnaejpxwubmxpnpnv`, PostgreSQL 17.11 in `eu-west-1`, organizzazione Free.  
**Ambiente QA:** PostgreSQL 16 usa-e-getta in GitHub Actions (non contiene gli account reali).  
**Stato:** STAGING TECNICO — **nessuna modifica persistente su Supabase reale**.

## 1. Decisione di sicurezza

M3 è stato diviso in **M3a (progettazione/test isolati)** e **M3b (scrittura su Supabase reale dopo backup verificato)**.

L'account MANZO AI su piano Free non possiede backup giornalieri gestiti; Supabase indica l'esportazione tramite CLI per i progetti gratuiti (https://supabase.com/docs/guides/platform/backups). La connessione MCP disponibile non offre qui una procedura di dump completo + restore collaudato. **Questo gate non può essere saltato.**

M3a non modifica né cancella password, email, Auth, account, URL, bucket Storage, registrazioni B2B, tabelle `app`/`app_private`, pagamenti o le pagine GitHub Pages.

## 2. Modello reale proposto (DDL pronto ma NON APPLICATO)

Sorgente SQL: `product/backend/migrations/0004_public_catalog_m3.sql`.

| Schema | Tabella | Identità e scopo |
|---|---|---|
| `content_public` | `catalog_courses` | corso pubblico con `course_key` stabile; nessuna dipendenza da `app.organizations` |
| `content_public` | `catalog_localizations` | variante univoca (`course_key`, `locale`), rotta e SHA-256 dell'originale Git |
| `content_public` | `catalog_units` | unità per variante, chiave stabile e ordinamento |
| `content_internal` | `import_runs` | manifest hash e commit SHA per tracciare gli import; non esposto come endpoint |

**Scelta deliberata:** il nome `content_public` indica una futura destinazione editoriale; **non** significa che queste tabelle siano accessibili anonimamente. Prima del futuro go-live tutte e quattro saranno RLS **ENABLE + FORCE**, zero policy pubbliche, zero privilegi `anon`/`authenticated`/`service_role`, e nessuna esposizione del nuovo schema al Data API. L'eventuale lettura pubblica richiede una migration separata, in sola lettura, review di RLS e test API.

Nessuna riga viene scritta nelle già esistenti 15 tabelle applicative, né viene creato un tenant fittizio.

## 3. Generatore e transazione

Sorgente: `product/migration/prepare_m3_sql.py`.

- Ricalcola il catalogo **direttamente dai sei JSON editoriali** usando M2 e verifica JSON Schema Draft 2020-12.
- Calcola hash SHA-256 deterministico sul manifest normalizzato, per rilevare divergenze.
- Produce SQL parametrizzato tramite JSONB generato da un catalogo validato con delimitatore SQL verificato, senza dati di account o segreti.
- `BEGIN` → caricamento JSONB in tabella TEMP → controllo contratto → UPSERT corsi/localizzazioni/unità → registro import → verifica conteggi → **ROLLBACK** per default.
- Un secondo import sullo stesso database temporaneo mantiene **2 corsi, 6 varianti, 36 unità e un solo import registrato**, senza reimpostare `updated_at` se i dati sono identici.
- `--mode commit` è previsto **solo** per il database usa-e-getta della CI, richiede sia il flag `--ci-ephemeral-confirm` sia la variabile `MANZO_M3_EPHEMERAL_DATABASE=isolated-ci-only`; NON è la procedura di deploy produzione.

**Controlli attesi:** 2 corsi; 6 varianti lingua IT/EN/ES; 36 unità locali. Le 42 domande pubbliche e 42 casi restano soltanto **conteggi**, senza testi né soluzioni.

## 4. Test automatici

Workflow: `.github/workflows/m3-isolated-catalog-qa.yml`.

- Esegue tutti i test M0/M1/M2/M3 con Python 3.11 e `jsonschema==4.26.0`.
- Avvia PostgreSQL 16 temporaneo con ruoli simulati `anon`, `authenticated`, `service_role`.
- Applica **solo nello staging temporaneo** la DDL di catalogo.
- Esegue SQL in modalità rollback; verifica **zero righe persistenti**.
- Esegue due import commit **solo nell'ambiente effimero**, confronta i conteggi e gli hash logici.
- Verifica `RLS ENABLE/FORCE`, assenza di policy e impossibilità di SELECT con ruoli `anon`/`authenticated`.
- Archivia `manzo-ai-m3-isolated-import-evidence` in GitHub Actions, **non** nel sito pubblico.

Non chiamare questo test un backup di Supabase né una verifica end-to-end con identità reale.

## 5. Backup obbligatorio prima di M3b

**M3b resta bloccato fino alla verifica reale di un recovery point.**

Procedura consigliata sul Mac dell'amministratore, in ambiente locale privato, con Supabase CLI, Docker e connessione selezionata dal pannello Supabase **Connect**:

1. Controllare `supabase --version` e `supabase db dump --help`: le opzioni CLI possono variare.
2. Impostare la stringa di connessione PostgreSQL **solo nel terminale sicuro** (mai in GitHub, chat, log, screenshot o CI).
3. Esportare ruoli, schema e dati del progetto con i comandi ufficiali, per esempio:
   - `supabase db dump --db-url "$DATABASE_URL" -f roles.sql --role-only`
   - `supabase db dump --db-url "$DATABASE_URL" -f schema.sql`
   - `supabase db dump --db-url "$DATABASE_URL" -f data.sql --use-copy --data-only`
4. Archiviare i dump cifrati e fuori dal repository; verificare che siano **non vuoti**, completi per gli schemi dell'app e compatibili con un ripristino su un PostgreSQL isolato con le estensioni/ruoli necessari.
5. Verificare con un **restore reale su ambiente di test**; confrontare definizioni, funzioni, policy, conteggi e checksum applicativi. I dump CLI possono escludere schemi gestiti (per esempio Auth/Storage): pianificare separatamente il recupero completo di identità, Storage e configurazioni SMTP/redirect.
6. Registrare timestamp, versione, risultato restore e custode del backup senza salvare credenziali.

Riferimenti: [Backups Supabase](https://supabase.com/docs/guides/platform/backups) · [Backup/restore CLI](https://supabase.com/docs/guides/platform/migrating-within-supabase/backup-restore) · [CLI db dump](https://supabase.com/docs/reference/cli/supabase-db-dump).

**Non** eseguire la migration `0004` nel progetto MANZO AI finché non esistono prove del punto di ripristino. Non suggerire un backup basato sui soli conteggi SQL: non è ripristinabile.

## 6. Gate M3b e piano rollback

**Prima della scrittura reale:**
- snapshot del DB e restore provato;
- confronto delle migrazioni `0001`–`0003` in Supabase e approvazione dello script `0004`;
- controllo di privilegi di default e dell'elenco degli schemi Data API esposti;
- verifica pre-import delle cardinalità e della fonte SHA;
- import in transazione e prima lettura da backend autenticato/privilegiato;
- Security Advisor Supabase e test negativi `anon`/`authenticated`;
- nessuna modifica a Auth, e nessun servizio commerciale o a pagamento attivato.

**Fallback se la pubblicazione fallisce:** non collegare il frontend al nuovo catalogo (feature flag OFF), lasciare GitHub Pages funzionante. Se il catalogo nuovo non è stato usato da utenti reali, ripristinare mediante migrazione correttiva o backup verificato dopo controllo dipendenze; non lanciare cancellazioni sul database Auth o B2B.

## 7. Fatti verificati e limitazioni

Al momento della preparazione: tre migrazioni del progetto MANZO AI applicate; 15 tabelle applicative preesistenti, senza corsi, versioni, organizzazioni o enrollment; 0 bucket Storage e 0 Edge Functions. La registrazione Auth esistente resta disponibile.

**Non ancora fatto:** il backup recuperabile e il restore del Supabase Free reale, migration `0004` live, import effettivo su Supabase e policy di lettura pubblica. Il completamento M3a è un **gate tecnico**, non equivale a chiudere M3b.

Una segnalazione di sicurezza distinta in Supabase Auth riguarda la protezione contro password compromesse disabilitata: [configurazione ufficiale](https://supabase.com/docs/guides/auth/password-security#password-strength-and-leaked-password-protection). Non costituisce un motivo per alterare gli utenti durante M3.
