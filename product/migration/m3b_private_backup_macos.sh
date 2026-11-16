#!/usr/bin/env bash
# MANZO AI M3b — private read-only Supabase CLI v3 backup on macOS.
# No credentials, SQL dumps or personal information in GitHub/ChatGPT.
# This is NOT a full restore of managed Supabase Auth/Storage/config.
set -euo pipefail
umask 077

PROJECT_REF="bjydnaejpxwubmxpnpnv"
BACKUP_BASE="${HOME}/.manzo-ai/private-backups"

fail() { printf '\nERRORE: %s\n' "$*" >&2; exit 1; }
msg() { printf '%s\n' "$*"; }
command -v python3 >/dev/null 2>&1 || fail "Python 3 non disponibile."
command -v supabase >/dev/null 2>&1 || fail "Installa Supabase CLI v3 prima di proseguire."
command -v docker >/dev/null 2>&1 || fail "Installa Docker Desktop."
command -v shasum >/dev/null 2>&1 || fail "shasum non disponibile."
[[ "$(uname -s)" == "Darwin" ]] || fail "Questa procedura interattiva è destinata al Mac."
[[ -z "${GITHUB_ACTIONS:-}" && -z "${CI:-}" ]] || fail "Nessun backup con credenziali in CI o GitHub Actions."

version="$(supabase --version 2>/dev/null || true)"
[[ "$version" =~ (^|[^0-9])v?3\. ]] || fail "Richiesta CLI v3. Versione rilevata: ${version:-sconosciuta}."
supabase db dump --help 2>/dev/null | grep -Fq -- '--remote' ||
  fail "La CLI non espone --remote: controlla supabase db dump --help."
docker info >/dev/null 2>&1 || fail "Avvia Docker Desktop prima dell'esportazione."

msg "MANZO AI | M3b | Solo backup locale, nessuna modifica al database online."
msg "Apri https://supabase.com/dashboard/project/${PROJECT_REF} e scegli Connect → Session pooler."
msg "Inserisci nel Mac l'URL PostgreSQL COMPLETO; non condividerlo via chat, Git o screenshot."
printf 'Connection string (inserimento nascosto): '
IFS= read -r -s MANZO_DB_URL
printf '\n'

# A username bound to the project is required, or project-specific direct host.
# Reject localhost and unrelated projects.
MANZO_DB_URL="$MANZO_DB_URL" MANZO_PROJECT_REF="$PROJECT_REF" python3 - <<'PY' ||
import os, sys
from urllib.parse import urlsplit
u = urlsplit(os.environ["MANZO_DB_URL"])
ref = os.environ["MANZO_PROJECT_REF"]
host, user = (u.hostname or "").lower(), (u.username or "")
db = u.path.strip("/")
direct = host == f"db.{ref}.supabase.co" and user == "postgres"
pooler = host.endswith(".pooler.supabase.com") and user == f"postgres.{ref}"
valid = (u.scheme in ("postgres", "postgresql")
         and (direct or pooler) and bool(u.password)
         and db == "postgres" and u.port in (5432, 6543))
if not valid:
    print("ERRORE: connection string non corrispondente al progetto MANZO AI.", file=sys.stderr)
    sys.exit(1)
PY
  fail "URL PostgreSQL non valido o destinazione non verificata."

# Keep backup outside Git, iCloud Documents and published _site.
mkdir -p "$BACKUP_BASE"
chmod 700 "$BACKUP_BASE"
timestamp="$(date -u '+%Y%m%dT%H%M%SZ')"
dest="$(mktemp -d "${BACKUP_BASE}/MANZO_AI_${timestamp}_XXXXXX")" ||
  fail "Impossibile creare directory backup privata."
chmod 700 "$dest"
printf 'INCOMPLETE — do not use for recovery\n' > "$dest/STATUS.txt"

msg "Esportazione verso cartella privata locale: $dest"
# Supabase CLI v3: without --remote it would dump LOCAL.
dump_to_file() {
  local filename="$1"
  shift
  if ! supabase db dump "$@" "--remote=${MANZO_DB_URL}" -f "$dest/$filename" >/dev/null 2>/dev/null; then
    fail "Esportazione $filename non riuscita. Il backup è INCOMPLETO; non usare per ripristino."
  fi
  [[ -s "$dest/$filename" ]] || fail "$filename risulta vuoto (backup INCOMPLETO)."
  chmod 600 "$dest/$filename"
}

dump_to_file roles.sql --role-only
dump_to_file schema.sql
dump_to_file data.sql --data-only --use-copy

(
  cd "$dest"
  shasum -a 256 roles.sql schema.sql data.sql > SHA256SUMS
  chmod 600 SHA256SUMS
  shasum -a 256 -c SHA256SUMS >/dev/null
)
cat > "$dest/STATUS.txt" <<'EOF'
EXPORTED, CHECKSUMS PASSED — RESTORE NOT VERIFIED
CLI dumps exclude Supabase-managed schemas such as Auth and Storage.
Separate recovery for identity, SMTP, redirects and config is still required.
Do not execute M3b migration/import based on this file alone.
EOF
chmod 600 "$dest/STATUS.txt"
unset MANZO_DB_URL
msg "Esportazione locale completata. Integrità file: PASS."
msg "Cartella: $dest"
msg "Stato: RESTORE NON ANCORA VERIFICATO. Mantieni l'archivio cifrato fuori da GitHub."
