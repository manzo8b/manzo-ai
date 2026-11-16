# MANZO AI — Primo deploy reale del database Supabase

**Data verifica:** 16 novembre 2026  
**Progetto:** MANZO AI  
**Project ref:** `bjydnaejpxwubmxpnpnv`  
**Organizzazione:** MANZO AI, distinta da Oiko  
**Regione:** `eu-west-1` — Irlanda  
**Database:** PostgreSQL 17.11, stato ACTIVE_HEALTHY  
**Ambiente:** primo progetto Free utilizzato per sviluppo e prove, NON produzione commerciale

## Migrazioni realmente applicate

| Versione Supabase | Nome migrazione | Esito |
|---|---|---|
| 20261116083851 | `manzo_ai_0001_foundation` | applicata |
| 20261116083913 | `manzo_ai_0002_learning_b2b` | applicata |
| 20261116084108 | `manzo_ai_0003_harden_event_trigger` | applicata |

Le prime due migrazioni derivano dai file esistenti `product/backend/migrations/0001_foundation.sql` e `0002_learning_b2b.sql`. Il terzo file, `0003_live_event_trigger_permissions.sql`, documenta una correzione dei permessi rilevata dall'advisor del nuovo progetto.

## Stato verificato direttamente

- 15 tabelle applicative in `app` e `app_private`, tutte con RLS **abilitata e forzata**
- Tabelle applicative senza righe; **nessun utente reale, corso, licenza o contenuto è stato importato durante le migrazioni**
- Funzioni mutative `app_private.assign_learning_seat`, `release_learning_seat`, `enroll_learning_student`, `complete_learning_module` e `record_learning_assessment`: invocabili da `service_role`, non da `anon` o `authenticated`
- `public.rls_auto_enable()`: conservata come event trigger, ma revocato `EXECUTE` ai ruoli pubblici e agli utenti autenticati
- Il nuovo advisor sicurezza non mostra più gli avvisi sulla funzione pubblica `SECURITY DEFINER`
- **Sette avvisi INFO** `rls_enabled_no_policy` rimangono sulle tabelle `app_private` e sono coerenti con il modello fail-closed: non aggiungere policy SELECT generiche per far scomparire questi avvisi
- Nessuna Edge Function distribuita. L'adapter API esiste nel repository, ma **non ha un endpoint attivo**
- Non sono stati attivati Stripe, email commerciali, agenti AI né hosting a pagamento
- Il design pubblico approvato in GitHub Pages è invariato

## Gate prima di account studenti reali

1. Controllare nel pannello Supabase Auth i provider abilitati, le regole di conferma indirizzo e i limiti email
2. Definire `Site URL` e redirect esatti per l'ambiente di test, senza link permissivi o domini fittizi
3. Verificare i permessi del nuovo progetto e predisporre almeno due identità di prova con indirizzi autorizzati dal proprietario
4. Configurare un'organizzazione applicativa `app.organizations` (diversa dall'organizzazione di fatturazione Supabase) e le membership solo dopo che gli account sono stati creati e verificati
5. Caricare un corso di test versionato, i moduli e un grant di licenza gratuito e circoscritto: non usare dati personali reali né fingere un acquisto
6. Testare l'isolamento tenant con login autenticati, assegnazione/rilascio posti, enrollment, progressi e quiz direttamente sul progetto
7. Preparare con attenzione i segreti backend e la configurazione delle Edge Functions. Una funzione pubblica senza controlli e rate limit **non** va deployata prematuramente
8. Completare documentazione privacy, consenso operativo, export/cancellazione e backup prima del primo cliente esterno

## Avvisi performance

Il linter Supabase segnala diverse chiavi esterne che beneficerebbero di indici aggiuntivi e alcuni indici attualmente non usati. Con tutte le tabelle vuote, non è corretto dedurre un problema reale di performance dall'uso zero degli indici. Valutare gli indici con test e workload rappresentativi prima della produzione.

## Link operativi

- Dashboard: https://supabase.com/dashboard/project/bjydnaejpxwubmxpnpnv
- Migrazioni: https://supabase.com/dashboard/project/bjydnaejpxwubmxpnpnv/database/migrations
- Autenticazione: https://supabase.com/dashboard/project/bjydnaejpxwubmxpnpnv/auth/users
- Security Advisor: https://supabase.com/dashboard/project/bjydnaejpxwubmxpnpnv/advisors/security
- Documentazione SQL sorgente: `product/backend/migrations/`

**Importante:** `production` nell'intestazione di un progetto Supabase gratuito non implica che MANZO AI sia pronta per clienti o in produzione commerciale. La configurazione rimane da considerarsi **staging non validato**.
