#!/usr/bin/env bash
# MANZO AI M3b: Docker-free PostgreSQL 17/18 client for Supabase PG17.
# READ-ONLY. No Supabase CLI/Docker. Never share resulting files.
set -euo pipefail
umask 077
PROJECT_REF='bjydnaejpxwubmxpnpnv'
BACKUP_BASE="${HOME}/.manzo-ai/private-backups"
fail() { printf '\nERRORE: %s\n' "$*" >&2; exit 1; }
info() { printf '%s\n' "$*"; }

[[ "$(uname -s)" = Darwin ]] || fail 'Questo script è per macOS.'
[[ -z "${CI:-}" && -z "${GITHUB_ACTIONS:-}" ]] || fail 'Backup remoto vietato in CI.'
command -v shasum >/dev/null || fail 'shasum non disponibile.'

# PostgreSQL 18 pg_dump supports older server 17.11. Restore target should be >=18.
PG_BIN=''
for candidate in \
  '/Applications/Postgres.app/Contents/Versions/18/bin' \
  "${HOME}/Applications/Postgres.app/Contents/Versions/18/bin" \
  '/Applications/Postgres.app/Contents/Versions/17/bin' \
  "${HOME}/Applications/Postgres.app/Contents/Versions/17/bin"
do
  if [[ -x "$candidate/pg_dump" && -x "$candidate/pg_restore" && -x "$candidate/psql" ]]; then
    PG_BIN="$candidate"
    break
  fi
done
if [[ -z "$PG_BIN" ]]; then
  command -v pg_dump >/dev/null || fail 'pg_dump non trovato: controlla Postgres.app 18 o 17.'
  command -v pg_restore >/dev/null || fail 'pg_restore non trovato.'
  command -v psql >/dev/null || fail 'psql non trovato.'
  PG_BIN="$(dirname "$(command -v pg_dump)")"
fi
PG_DUMP="$PG_BIN/pg_dump"
PG_RESTORE="$PG_BIN/pg_restore"
PSQL="$PG_BIN/psql"
version="$("$PG_DUMP" --version)"
[[ "$version" =~ PostgreSQL\)\ (17|18)\. ]] ||
  fail "Serve pg_dump 17 o 18 per Supabase 17.11. Versione: $version"

info 'MANZO AI — Backup PostgreSQL nativo, senza Docker.'
info 'Apri Supabase MANZO AI > Connect > Session pooler.'
info 'Inserisci soltanto il server/hostname del pooler.'
IFS= read -r -p 'Host session pooler: ' PGHOST
[[ "$PGHOST" =~ ^[a-z0-9-]+\.pooler\.supabase\.com$ ]] ||
  fail 'Host non riconosciuto come pooler Supabase.'
export PGHOST
export PGPORT=5432
export PGUSER="postgres.${PROJECT_REF}"
export PGDATABASE=postgres
export PGSSLMODE=require
export PGCONNECT_TIMEOUT=10

info 'Inserisci la PASSWORD DEL DATABASE Supabase (non la chiave Brevo).'
printf 'Password database (nascosta): '
IFS= read -r -s PGPASSWORD
printf '\n'
[[ -n "$PGPASSWORD" ]] || fail 'Password mancante.'
export PGPASSWORD

if ! "$PSQL" -X -qAt -c "select current_database()" 2>/dev/null | grep -Fxq 'postgres'; then
  unset PGPASSWORD
  fail 'Connessione non riuscita; nulla esportato.'
fi

mkdir -p "$BACKUP_BASE"
chmod 700 "$BACKUP_BASE"
timestamp="$(date -u '+%Y%m%dT%H%M%SZ')"
dest="$(mktemp -d "${BACKUP_BASE}/MANZO_AI_${timestamp}_XXXXXX")" ||
  fail 'Impossibile creare cartella privata.'
chmod 700 "$dest"
printf 'INCOMPLETE; RESTORE NOT VERIFIED\n' > "$dest/STATUS.txt"
info "Salvataggio esclusivamente sul Mac: $dest"

if ! "$PG_DUMP" -Fc --no-owner --quote-all-identifiers \
  --schema=app --schema=app_private \
  --file="$dest/application.dump" 2>/dev/null; then
  unset PGPASSWORD
  fail 'Dump applicativo fallito; backup incompleto.'
fi
[[ -s "$dest/application.dump" ]] || fail 'Dump applicativo vuoto.'
"$PG_RESTORE" --list "$dest/application.dump" >/dev/null ||
  fail 'Archivio applicativo non leggibile.'
chmod 600 "$dest/application.dump"

full='NOT_AVAILABLE'
if "$PG_DUMP" -Fc --no-owner --quote-all-identifiers --file="$dest/full_database.dump" 2>/dev/null &&
   [[ -s "$dest/full_database.dump" ]] &&
   "$PG_RESTORE" --list "$dest/full_database.dump" >/dev/null 2>&1; then
  full='ARCHIVE_VALID'
  chmod 600 "$dest/full_database.dump"
else
  rm -f "$dest/full_database.dump"
fi
unset PGPASSWORD

(
  cd "$dest"
  shasum -a 256 application.dump > SHA256SUMS
  if [[ "$full" = ARCHIVE_VALID ]]; then
    shasum -a 256 full_database.dump >> SHA256SUMS
  fi
  shasum -a 256 -c SHA256SUMS >/dev/null
  chmod 600 SHA256SUMS
)
cat > "$dest/STATUS.txt" <<EOF
EXPORTED; SHA256 PASSED; RESTORE NOT VERIFIED
PROJECT_REF: ${PROJECT_REF}
APP_DUMP: application.dump
FULL_DATABASE_DUMP: ${full}
PG_DUMP_VERSION: ${version}
UTC: ${timestamp}
REMINDER: Auth, SMTP, Storage object bytes and API settings need separate
recovery verification. Never restore onto MANZO AI production.
EOF
chmod 600 "$dest/STATUS.txt"

info 'Esportazione locale completata. Integrità file: PASS.'
info "Full database archive: $full"
info 'Restore: NON ANCORA VERIFICATO.'
info "File privati: $dest"
info 'Non pubblicare o inviare questi file: potrebbero contenere dati riservati.'
