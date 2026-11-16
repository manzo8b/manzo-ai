# MANZO AI — Piano maestro di migrazione GitHub → Supabase

**Decisione:** preparare la migrazione dell'intera piattaforma prima di attivare membership, corsi B2B e progressi persistenti.  
**Baseline:** 16 novembre 2026 · **Stato:** audit e preparazione, nessun import runtime effettuato.  
**Repo:** `manzo8b/manzo-ai` · **Supabase:** `bjydnaejpxwubmxpnpnv` (Irlanda, eu-west-1, Free).  
**Git baseline pre-audit:** `76656f6aba305204128bdea776c8debc95c0a1f6`.

## 1. Architettura e principi

GitHub resta il **sistema autorevole per i sorgenti e l'editoria versionata** (contenuti, layout, CSS, asset originali, build, test). Supabase è il **backend** per Auth, PostgreSQL, Storage e API/Edge Functions. GitHub Pages rimane il frontend pubblico durante l'audit e il pilota: non è una piattaforma di hosting commerciale SaaS definitiva. La futura distribuzione frontend richiede un provider, un dominio e un budget decisi separatamente.

Le verticali sono Learning, Verify e Studio. Il catalogo pubblico deve restare accessibile e indicizzabile senza login; le funzionalità riservate devono essere protette da verifica server-side. Non usare lo schema privato per generare pagine pubbliche, e non convertire ogni HTML in una riga PostgreSQL.

## 2. Stato misurato il 16/11/2026

| Componente | Evidenza | Limite |
|---|---|---|
| Sorgenti GitHub | **154 file blob** completi nella baseline di `main`, 7 ZIP storici; `site-v0.7.zip` è il package di base usato nel deploy | Non sono il censimento del sito pubblicato |
| Sito | Il workflow verifica 82 pagine `index.html` nel package v0.7 prima dei publisher successivi | Il numero di HTML **finali** va contato dopo la build |
| PostgreSQL | 15 tabelle: 8 in `app`, 7 in `app_private` | 0 righe in **tutte** le 15 tabelle applicative |
| RLS | Abilitata e forzata per tutte le 15 tabelle | Manca prova end-to-end con due tenant reali |
| Migrazioni | `manzo_ai_0001_foundation`, `manzo_ai_0002_learning_b2b`, `manzo_ai_0003_harden_event_trigger` applicate | Non applicare nuovamente |
| Edge Functions | 0 deployate | L'adapter Learning API è soltanto sorgente |
| Storage | 0 bucket | Nessun trasferimento file avviato |
| Auth | Primo account verificato con recupero via Brevo/Supabase | Autenticazione NON equivale ad autorizzazione aziendale |
| Prodotti | Demo Learning, Verify e Studio; fonti e materiali editoriali pubblicati | Nessun SaaS commerciale o pagamento attivo |

L'inventario sorgente firmato da SHA Git e dimensioni è in `product/migration/github-source-inventory-2026-11-16.json`. Si tratta di una baseline storica e riproducibile. I nuovi file per l'audit non devono alterarla.

## 3. Matrice di destinazione

| Componente | Sorgente | Migrazione proposta | Vincoli |
|---|---|---|---|
| Home, Academy, pagine IT/EN/ES e corsi statici | `site-v0.7.zip` + `theme/*` | Frontend versionato, poi hosting dedicato quando giustificato | Mantenere URL, design, SEO, locale, accessibilità |
| Corso Allucinazioni AI e autovalutazione | `editorial/learning/hallucinations/{it,en,es}.json` e `course.js` | Sorgente Git immutabile, catalogo/versioni metadati DB; contenuti privati solo quando necessario | L'attuale autovalutazione espone già le risposte |
| Engineering Assurance / coding | `coding-{it,en,es}.json` + `coding.js` | Come sopra, con modulo privato e scoring separati | Nessuna valutazione ufficiale basata su risposte nel browser |
| Percorsi/UX didattica | `product/learning-experience/*` | Frontend; progressi reali successivamente in `app.learning_progress` | Non importare progressi demo |
| Learning B2B | `product/learning-console/*` e SQL backend | `app.courses`, `app.course_versions`, `app.enrollments`, `app.learning_progress`, `app_private.learning_modules` e `app_private.assessment_items` | Tabelle vuote; prima un modello tenant e API verificate |
| Identità | `product/auth-staging/*` | Auth Supabase esistente + frontend corrente | Non ricreare utenti, copiare password o cambiare redirect |
| Studio / Product Lab | `product/preview/*`, `product/core/*` | Demo attuale sul sito; API e schema Studio futuri | La demo non usa modelli AI né salva progetti server-side |
| Verify | Product Lab + materiale ricerca | Frontend e ricerca pubblica; futura API con prove, citazioni e audit | Nessuna pretesa di verifiche AI realmente automatizzate |
| Dossier ACR e contenuti editoriali | `editorial/research/acr/*` | Git quale fonte di verità, asset statici o Storage selettivo | Conservare metodo, fonti, metadati |
| Oracle City | `editorial/oracle-city/numero-01/*` | Media pubblici; Storage facoltativo se dimostrato vantaggio | Ordine pagine, URL e diritti invariati |
| Podcast, video, sottotitoli, slide e documenti | `editorial/podcast/*`, `editorial/video/*`, media in ZIP | Asset statici esistenti; valutare Storage pubblico o privato | NON importare come pubblicati file scartati/non approvati |
| SEO, navigazione, titoli, legal, sitemap | `theme/*`, workflow deploy e verifica Google | Restano nella pipeline frontend | Nessun 404, canonical rotto o indicizzazione di aree private |
| Billing e agenti futuri | `product/backend/*`, `product/core/*` | Edge Functions + schemi privati dopo gate sicurezza/costi | Segreti server-only, nessun pagamento o agente live ora |

### Separazione obbligatoria dei dati

**Pubblico:** materiale didattico/editoriale, titoli, slug, locale, fonti, metadati SEO, storia delle revisioni. L'origine resta Git: un futuro catalogo DB deve essere una *proiezione versionata*, non una seconda redazione manuale.

**Riservato B2B:** corsi assegnati, versioni immutabili con `content_ref`, contenuti soggetti a licenza, iscrizioni, progressi, quiz non pubblici, risultati e organizzazioni. Tenant e autorizzazione sempre lato server.

**Privato di sistema:** grants, quote, audit, billing, costi di inferenza, segreti; mai esposto con politiche generiche in `app_private`.

**Gate esami:** le soluzioni già presenti nei JSON pubblici possono servire per autovalutazione, **non** per una valutazione B2B attendibile. Occorre una banca item privata e un correttore server-side.

## 4. Sequenza di lavoro e criterio di uscita

| Fase | Attività | Gate di accettazione | Stato |
|---|---|---|---|
| M0 | Audit di sorgenti Git e struttura database | Inventario con SHA + schema reale letto in sicurezza | **Completato** |
| M1 | Audit della **build finale** (ZIP + publisher + auth + SEO) | 111 HTML, 62 altri file, 0 link locali mancanti, 172/173 SHA invariati dopo correzione | **PASS — deploy 43864931269** |
| M2 | Progettare contratto editoriale e mappa IT/EN/ES | Generator metadata-only di 2 percorsi/6 varianti, SHA stabili, test e CI; nessun quiz privato esportato | **PASS tecnico — import non eseguito** |
| M3 | Backup verificato e import controllato di prova | Dati di prova isolati, checksum corrispondenti, ripristino e idempotenza | Da eseguire |
| M4 | Valutare Storage e migrare solo media appropriati | File approvati, SHA verificato, accesso pubblico/privato corretto | Da eseguire |
| M5 | Hardening Edge API e collegamento frontend con feature flag | JWT, RLS tenant A/B, CORS, 401/403, rate limit, fallback | Da eseguire |
| M6 | Attivazione organizzazioni, ruoli, corsi e progressi B2B | Test E2E, revoca, privacy/export e studio UX su desktop/mobile | Da eseguire |
| M7 | Hosting applicativo e commerciale | Nuovo budget/dominio approvati, DNS, rollback e monitoraggio | Non autorizzato |

### Audit automatico del prodotto costruito

Eseguire **solo dopo l'ultimo publisher** della pipeline, quando `_site` rappresenta ciò che verrà pubblicato:

```bash
python3 -m unittest discover -s product/migration -p 'test_*.py' -v
python3 product/migration/audit_release.py \
  --site _site \
  --output /tmp/manzo-ai-final-release-inventory.json \
  --minimum-pages 82 --strict
```

Il report in JSON contiene URL/percorsi locali, locale, titolo, canonical, hreflang, robots, hash e dimensioni dei file, link interni mancanti e check di noindex privati. Il programma è di sola lettura e rifiuta di scrivere il report nel sito pubblico. Se il gate `--strict` fallisce, diagnosticare e correggere senza sopprimere il controllo. **Le 82 pagine sono il minimo dell'archivio, non il totale finale certificato.**

## 5. Sicurezza, backup e rollback

- Prima di **scrivere** in Supabase: esportazione/backup verificati di schema/dati, piano di ripristino ed evidenza di eseguibilità. Il piano Free non garantisce backup gestiti equivalenti al Pro.
- Prima di caricare media: verifica diritti, MIME, dimensione, identificatore sorgente, SHA-256. I file approvati restano versionati su Git.
- In ogni import: chiavi naturali stabili e idempotenza; evitare doppie righe per lingua/versione; transazioni o staging isolato e conteggio prima/dopo.
- Frontend: mantenere la versione Pages attuale senza cambi DNS; feature flag backend inizialmente disabilitata, rollback immediato alla UI statica in caso di errore.
- Database: evitare `DROP`, cancellazioni Auth o rollback ciechi su un sistema in uso; preferire migrazioni forward e backup testato per interventi strutturali.
- Privacy: nessuna password, token Auth, chiave SMTP, service-role, provider AI o segreto in GitHub, Storage pubblico o report.
- Regolazione commerciale: hosting/dominio e pagamenti dopo nuovo gate costi/legal. Non considerare la regione UE garanzia automatica GDPR.

## 6. Definizione di "migrazione completa"

Non dichiarare completata la migrazione se manca anche solo uno dei seguenti controlli:

1. Inventario **effettivo** del sito compilato, inclusi itinerari IT/EN/ES, asset, download, header SEO, pagine private.
2. Parità di contenuto, media e comportamento per Home, Academy, dossier, video, Oracle City, Learning, Verify e Studio, o cambi approvati esplicitamente.
3. Catalogo/moduli/versioni coerenti e privi di doppioni; distinzione pubblico/B2B mantenuta.
4. RLS e API server-side provate con account di due organizzazioni, inclusi tentativi cross-tenant e revoche.
5. Test accessibilità, performance, mobile, SEO, privacy, backup/restore e rollback completati.
6. Nessuna promessa non implementata (AI generator, pagamenti, certificazioni, licenze attive).

## 7. Consegnato ora e prossimo gate

**Eseguiti:** audit GitHub e Supabase in sola lettura; manifest dei 154 file sorgente; scanner post-build, test automatici e CI separata dalla pubblicazione; questo piano.

**Non eseguiti:** import contenuti, nuove tabelle o bucket, API deployate, hosting, utenti/ruoli aggiunti, password modificate, pagamenti. Successivamente è stato recuperato l'artefatto completo del deploy GitHub Actions `43852683965`: **111 HTML (109 `index.html`), 62 asset/file tecnici, 15 pagine `noindex`, 6/6 pagine Auth/privacy marcate `noindex`**. È emerso **un collegamento mancante** in `it/video-e-slide/prompt-engineering/index.html` verso `/manzo-ai/it/prompt-mastery/`. Il gate M1 rimane aperto fino alla correzione e alla nuova build QA. Vedere `docs/MANZO_AI_RENDERED_RELEASE_AUDIT_2026-11-16.md`.

**Prossima attività:** correggere l'unico collegamento locale mancante, generare una build QA e acquisire nuovamente il manifest finale. Dopo il PASS di M1 si prepara lo schema contenuti e il dry-run di import.

## 8. Sorgenti e riferimenti

- `product/migration/github-source-inventory-2026-11-16.json`
- `product/migration/audit_release.py` e `product/migration/test_audit_release.py`
- `.github/workflows/migration-inventory-qa.yml`
- `.github/workflows/deploy-pages.yml`
- `docs/MANZO_AI_SUPABASE_LIVE_FOUNDATION_2026-11-16.md`
- `docs/MANZO_AI_SAAS_ARCHITECTURE_ADR001_2026-11-15.md`
- `product/backend/migrations/0001_foundation.sql`, `0002_learning_b2b.sql`, `0003_live_event_trigger_permissions.sql`
- Documentazione ufficiale: https://supabase.com/docs/guides/deployment · https://supabase.com/docs/guides/storage · https://supabase.com/docs/guides/database/postgres/row-level-security

### Aggiornamento verificato del 16/11/2026

L'inventario dell'artefatto GitHub Pages successivo al fix della PR #25 registra **0 collegamenti interni mancanti**, mantenendo **111 HTML e 62 altri file**. I checksum indicano un solo file HTML modificato su 173: `it/video-e-slide/prompt-engineering/index.html`. Gate **M1 PASS**; si conserva il rapporto storico del difetto in `docs/MANZO_AI_RENDERED_RELEASE_AUDIT_2026-11-16.md`.

Il generatore M2 è stato testato su tutti e sei i JSON editoriali originali. Produce 2 corsi, 6 varianti IT/EN/ES, 36 unità, 42 autovalutazioni localizzate e 42 casi localizzati, esportando soltanto metadati. Gate **M2 PASS tecnico** per il contratto editoriale, **nessuna importazione DB**. Dettagli: `docs/MANZO_AI_CONTENT_CONTRACT_M2_2026-11-16.md`.

**Passo seguente M3:** pianificazione e verifica backup, schema pubblico isolato dai tenant, import idempotente in dry-run e test negativi di autorizzazione prima di qualsivoglia scrittura a Supabase.
