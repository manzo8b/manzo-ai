# MANZO AI — M3b · Backup locale controllato e verifica del ripristino

**Progetto Supabase:** `bjydnaejpxwubmxpnpnv` (Free, eu-west-1, PostgreSQL 17.11).  
**Data:** 16 novembre 2026.  
**Stato:** PREPARAZIONE E PREFLIGHT: nessun backup remoto materializzato dall'assistente; nessuna migrazione `0004` applicata.  
**Ambiente previsto:** Mac personale dell'amministratore, fuori dal repository e dai workflow GitHub Actions.

## Perché questo passaggio è obbligatorio

Il piano Free non fornisce backup giornalieri gestiti (Supabase: https://supabase.com/docs/guides/platform/backups). M3a è stata collaudata su PostgreSQL usa-e-getta; M3b richiede dati **reali** protetti e prova di ripristino. L'azione di esportazione via Supabase CLI è in sola lettura, ma il dump può contenere dati di utenti o metadati riservati e non va caricato in cloud pubblici.

**Attenzione alla versione:** dalla CLI v3 (novembre 2026), `supabase db dump` senza `--remote` sceglie il database locale. Il nostro script verifica CLI v3 e imposta `--remote=<URL>` verso il progetto previsto. Non usare guide basate su `--db-url` o `--linked` senza controllare il cambiamento: https://supabase.com/changelog/supabase-cli-v3 .

## 1. Preparazione sul Mac (nessuna credenziale in chat)

Sono necessari: Python 3, Node.js >=20 se si installa la CLI tramite npm, Supabase CLI v3 e Docker Desktop avviato.

- Supabase CLI: https://supabase.com/docs/guides/local-development/cli/getting-started
- Docker Desktop: https://docs.docker.com/desktop/setup/install/mac-install/
- Verificare nel Terminale `supabase --version`, `supabase db dump --help` e `docker info`.
- La CLI installata localmente via npm è invocata da `npx supabase`: per usare lo script senza modificarlo aggiungere la cartella `node_modules/.bin` al `PATH` del Terminale; non forzare un'installazione Homebrew se non è compatibile con il Mac.
- Aprire nel Dashboard MANZO AI `Project → Connect → Session pooler`: https://supabase.com/dashboard/project/bjydnaejpxwubmxpnpnv .
- Copiare la stringa PostgreSQL con password già impostata; se contiene caratteri riservati, occorre la codifica URL corretta. **Mai incollare questa stringa in chat, issue, repository o screenshot.**

## 2. Esecuzione esportazione

Scaricare il file dal repository e conservarlo **fuori** da cartelle GitHub, siti Web o iCloud sincronizzato:

`product/migration/m3b_private_backup_macos.sh`

Dal Terminale, con la CLI v3 disponibile sul PATH:

```bash
bash /percorso-privato/m3b_private_backup_macos.sh
```

Lo script rifiuta CI, sistema operativo diverso da macOS, CLI non v3, Docker inattivo e URL che non indicano **il progetto Supabase MANZO AI** (host di progetto oppure session pooler con username `postgres.bjydnaejpxwubmxpnpnv`).

L'URL viene richiesto in modo interattivo e nascosto. La password può comunque comparire brevemente negli argomenti di processo della CLI locale: **eseguire esclusivamente su Mac personale non condiviso**. Lo script non scrive la stringa in file, log o shell history.

Gli export vengono salvati in `~/.manzo-ai/private-backups/MANZO_AI_<UTC>_<random>/` con permessi privati:

- `roles.sql` — ruoli custom applicativi
- `schema.sql` — struttura, policy e funzioni dell'app
- `data.sql` — dati degli schemi inclusi nel dump CLI
- `SHA256SUMS` — integrità dei tre file
- `STATUS.txt` — **EXPORTED, CHECKSUMS PASSED — RESTORE NOT VERIFIED**

L'operazione usa il dump ufficiale CLI e rifiuta file vuoti e check SHA non validi. Non esegue SQL DDL, `db push` o `db reset` nel progetto remoto.

**Limite fondamentale:** il dump CLI standard esclude gli schemi gestiti `auth`/`storage`. Questi file **non rappresentano da soli** una copia ripristinabile dell'account Auth e delle impostazioni SMTP, redirect, API key, provider. Poiché il progetto ha un account Auth attivo, questo punto va trattato separatamente.

## 3. Verifica checksum locale

Nel Terminale, dentro la directory del backup appena creato:

```bash
cd "$HOME/.manzo-ai/private-backups/NOME_DIRECTORY_DUMP"
shasum -a 256 -c SHA256SUMS
cat STATUS.txt
```

L'output deve riportare tre `OK`. **Questo dimostra l'integrità dei file, non un restore riuscito.**

Tenere una seconda copia cifrata in archivio privato fuori dal repository. Non allegare file `.sql`, connection URL, QR, email, token, SHA contenenti nomi o dati di utenti.

## 4. Prova di ripristino (ambiente separato)

La prova reale deve usare **un ambiente Supabase locale o un altro progetto temporaneo isolato**, non l'istanza MANZO AI online. La documentazione Supabase descrive l'esportazione di ruoli/schema/dati e il ripristino tramite `psql --single-transaction --variable ON_ERROR_STOP=1`: https://supabase.com/docs/guides/platform/migrating-within-supabase/backup-restore .

Preparazione obbligatoria: istanza test vuota, estensioni e ruoli richiesti presenti, connessione test verificata; nessun comando di restore puntato al database online. **Non** automatizzare `DROP SCHEMA`, `db reset` o ricreazione utenti sul progetto MANZO AI.

Il restore dei soli dump CLI deve verificare:
1. Struttura delle **15 tabelle applicative** (`app`: 8; `app_private`: 7) e funzioni/trigger/migrazioni equivalenti;
2. RLS forzata sulle 15 tabelle e permessi senza aperture involontarie;
3. Conteggi delle tabelle applicative, schema e checksum confrontati con il progetto sorgente, in modo privato;
4. Eventuale differenza tra PostgreSQL 17 (produzione) e ambiente QA locale;
5. Separatamente, **continuità dell'account Auth**, credenziali, SMTP Brevo, redirect e segreti tramite una procedura di disaster recovery specifica. Il backup CLI standard non è sufficiente.

Il risultato finale dell'operazione deve riportare un verbale con data, CLI version, destinazione ISOLATA, esito restore, check RLS e dichiarazione esplicita sulle esclusioni. Non inserire in GitHub né in chat dati utenti o backup.

## 5. Gate Go/No-Go prima dell'importazione live

| Gate | Condizione | Stato 16/11/2026 |
|---|---|---|
| L1 | Progetto sano, 15 tabelle protette e 3 migrazioni verificate | PASS |
| L2 | Script export CLI v3 conservato su GitHub (nessun segreto) | PREPARATO |
| L3 | Dump locale di `roles.sql`, `schema.sql`, `data.sql` verificato | **DA ESEGUIRE SUL MAC** |
| L4 | Restore applicativo effettuato e confrontato in ambiente ISOLATO | **NON ESEGUITO** |
| L5 | Piano documentato di recupero Auth/SMTP e configurazioni | **INCOMPLETO** |
| L6 | Applicazione migration `0004` e import live metadata-only | **BLOCCATO** |

**Divieto operativo:** non modificare in alcun modo `auth.users`, non lanciare `apply_migration` sul progetto live, non attivare il Data API per le nuove tabelle e non inviare backup a GitHub prima del PASS dei gate L3–L5.

## 6. Ulteriore segnalazione

Il Security Advisor Supabase segnala la funzionalità di protezione dalle password note compromesse disattivata; è un'attività di hardening distinta. Non cambiare gli account durante M3b.

## Riferimenti

- [Piano M3](MANZO_AI_M3_EXECUTION_REPORT_2026-11-16.md)
- [Migrazione SQL pronta ma non deployata](../product/backend/migrations/0004_public_catalog_m3.sql)
- [Supabase — Database Backups](https://supabase.com/docs/guides/platform/backups)
- [Supabase — CLI v3 breaking changes](https://supabase.com/changelog/supabase-cli-v3)
- [Supabase — Backup/restore CLI](https://supabase.com/docs/guides/platform/migrating-within-supabase/backup-restore)
