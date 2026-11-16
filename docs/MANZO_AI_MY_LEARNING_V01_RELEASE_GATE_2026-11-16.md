# MANZO AI — My Learning v0.1 · Incremento verso dati reali

**16 novembre 2026 · Stato:** sorgenti e contratti implementati, test CI, pagina pubblica pilota con lettura API **disabilitata**. Non è ancora un LMS commerciale o un endpoint distribuito.

## Obiettivo

Una vera area My Learning per account invitati e confermati, progettata per leggere soltanto **dati già registrati in Supabase**. Non crea iscrizioni, risultati, percentuali, certificati, contenuti o studenti fittizi. L'Academy pubblica resta invariata.

## Architettura

- Frontend editoriale: GitHub Pages IT/EN/ES.
- Supabase Auth: progetto `bjydnaejpxwubmxpnpnv`, account verificato; sessione dalla stessa chiave `sessionStorage` del login.
- Pagine private `noindex,nofollow,noarchive`: IT `/it/prodotto/learning-b2b/mio-percorso/`, EN `/en/product/learning-b2b/my-learning/`, ES `/es/producto/learning-b2b/mi-aprendizaje/`.
- La pagina invoca `auth.getUser()` prima di consultare il JWT della sessione; non permette di forzare un organization ID via query string.
- Nuove API solo in codice: `GET /v1/learning/organizations` (membership attive del soggetto autenticato) e `GET /v1/organizations/{id}/learning/enrollments` (solo iscrizioni proprie). API corsi e progressi già presenti, progressi ora ulteriormente filtrati per l'utente autenticato.
- Le schede mostrano soltanto iscrizioni a corsi pubblicati e il **numero di unità completate**, non percentuali o certificati. Titoli inseriti con `textContent`; vietato l'HTML da dati non affidabili.

## Interruttore go-live

Il publisher `theme/publish-my-learning.py` genera `workspaceApiEnabled=false` in GitHub Pages. Le chiamate effettive al backend sono **impossibili** nel pilota pubblico finché il flag non viene modificato dopo la validazione di produzione. In QA si verifica separatamente la futura modalità dati reali tramite API simulata e utente fake **solo per test**; quelle credenziali e risposte non vengono distribuite.

La Edge Function Learning non è ancora pubblicata: non chiamare il codice un servizio live.

## Supabase: fatti verificati in sola lettura

- PostgreSQL 17.11, eu-west-1, progetto healthy; 15 tabelle applicative, migrazioni 0001–0003.
- 1 utente Auth; **0** organizzazioni, membership, corsi B2B, iscrizioni, tentativi valutati, bucket Storage e Edge Functions.
- SQL catalogo `0004` non applicata; zero tabelle catalogo M3.
- Dump applicativo e restore locale verificati; ripristino integrale Auth/SMTP e privilegi ancora da chiudere.
- Security Advisor: 7 INFO su RLS privato senza policy (deny-by-default) e WARN sulla leaked-password protection disabilitata.

## Prove di qualità

- Unit test Node: identità tenant, ruoli, payload non affidabili, nessun progresso inventato, revoche.
- Router API: identity scoped organization discovery, enrollments, progress, errori senza divulgazione.
- Browser Chromium IT/EN/ES e mobile/desktop: mock Auth e API completamente isolati, due organizzazioni QA, cambio tenant, protezione XSS, flag OFF senza chiamate e nessuna metrica artificiale.
- Test Deno dell'Edge adapter e PostgreSQL 16 temporaneo con RLS/seat-concurrency.
- Questi test **non sostituiscono** il test con token reali su due organizzazioni prima della commercializzazione.

## Gate prima dell'attivazione vera

1. Recupero e verifica di Auth, SMTP Brevo, privilegi GRANT, backup cifrato e restore integrale.
2. Applicazione catalogo M3 in versione metadata-only con rollback e audit dopo chiusura gate.
3. Edge Function staging con JWT verificato, rate limit, segreti solo server-side, CORS origin esplicito e test su due tenant reali.
4. Creazione autorizzata di una organizzazione pilota e utenti test; assegnazioni, completamenti e risultati persistenti verificati direttamente.
5. Navigazione ai contenuti versionati e scoring quiz dal backend; dashboard amministratore e report.
6. Hosting frontend su origine propria, privacy/GDPR, supporto, monitoraggio e pricing dopo discovery cliente.

## Invarianti

Mai inserire password, chiavi SMTP, URL del pooler, service-role o dati utenti su GitHub. Non esporre `app_private` via Data API. Non modificare account e database esistenti prima del recovery gate. Nessun checkout, AI inference o registrazione libera attivati da questa fase.

## Riferimenti

- [Piano commerciale](MANZO_AI_SAAS_COMMERCIAL_PRODUCT_REVIEW_2026-11-16.md)
- [Publisher My Learning](../theme/publish-my-learning.py)
- [Adapter Learning API](../product/backend/edge/learning-api/index.ts)
- [Modello dati del workspace](../product/auth-staging/src/workspace-model.mjs)
- [Runbook M3b](MANZO_AI_M3B_BACKUP_RECOVERY_RUNBOOK_2026-11-16.md)
