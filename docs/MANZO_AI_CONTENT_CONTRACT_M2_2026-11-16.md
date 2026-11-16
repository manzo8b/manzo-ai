# MANZO AI — M2 · Contratto editoriale e preview di migrazione

**Data:** 16 novembre 2026  
**Stato:** modello e generatore READ-ONLY predisposti, in attesa di QA finale / import Supabase **non eseguito**  
**Ambito:** prima migrazione strutturale del catalogo pubblico professionale (due percorsi in IT/EN/ES), nel contesto della migrazione complessiva delle 111 pagine HTML e relativi media.

## Scopo e limite

M2 definisce la traduzione **riproducibile** da sorgente Git a metadati descrittivi, non sposta i contenuti privati né crea artificialmente organizzazioni, account, progressi o corsi a pagamento.

La build ufficiale di GitHub Pages resta la fonte di verità per esperienza visiva, link, canonical e layout. I JSON editoriali restano versionati in Git; il catalogo aggrega solo dati non sensibili e checksum. La migrazione dell'intera piattaforma richiede ancora M3–M7.

## Fonti originali verificate

| Chiave logica | Fonti | Contenuto per lingua | Rotte pubblicate |
|---|---|---|---|
| `ai-hallucinations` | `editorial/learning/hallucinations/{it,en,es}.json` | 6 moduli, 10 casi, 10 domande di autovalutazione | `it/impara/allucinazioni-ai-verificabilita/`, `en/learn/ai-hallucinations-verification/`, `es/aprende/alucinaciones-ia-verificacion/` |
| `engineering-assurance` | `editorial/learning/hallucinations/coding-{it,en,es}.json` | 6 capitoli, 4 casi, 4 domande di autovalutazione | Le tre rotte precedenti con suffisso `coding/` |

Totali **localizzati** attesi: **2 percorsi**, **6 varianti linguistiche**, **36 unità** (12 × 3), **42 domande** (14 × 3) e **42 casi** (14 × 3). Non sono 42 domande o 42 casi indipendenti: includono le tre localizzazioni.

## Output metadata-only

`product/migration/build_catalog.py` legge sei file JSON originali e genera, senza rete né scritture database:

- `course_key` e `locale`, combinati in chiave stabile `ai-hallucinations:it`, ecc.;
- titolo, rotta di pubblicazione, unità in ordine, durata se disponibile, conteggi;
- `source_path` e checksum SHA-256 calcolato dai byte originali;
- stato editoriale pubblico e indicatori espliciti `private_assessment_ready=false`, `b2b_enrollment_enabled=false`;
- policy dell'export: nessun risultato, email, credenziale o testo delle domande e delle soluzioni.

**Vietato:** trasformare le risposte già pubblicate nei JSON in una banca d'esame B2B. Le domande e le relative risposte esistono nel sito pubblico e rimangono soltanto materiale di autovalutazione. Il catalogo M2 non le duplica.

**Versionamento:** `schema_version=1.0` identifica il contratto del manifest, NON una nuova release editoriale dei corsi. I SHA-256 rilevano modifiche di contenuto e consentono un futuro aggiornamento idempotente. La chiave del corso è indipendente dal locale e dal checksum.

## Contratto e verifica

- Schema descrittivo: `product/migration/content-catalog.schema.json` (JSON Schema draft 2020-12).
- Generatore: `product/migration/build_catalog.py`.
- Test: `product/migration/test_build_catalog.py`.
- CI: `.github/workflows/migration-inventory-qa.yml`, con artefatto `manzo-ai-m2-public-catalog-preview`.

La CI esegue controlli Python sulla cardinalità, sui checksum, sulla determinazione dell'output, sui riferimenti e sulla mancanza di dati privati. Confronta inoltre versione e chiavi principali del manifest con lo schema. **Non esegue una convalida JSON Schema completa con un validatore terzo**; quel gate va aggiunto prima dell'import reale.

### Comando di prova

```bash
python3 -m unittest discover -s product/migration -p 'test_*.py' -v
python3 product/migration/build_catalog.py --root . --output /tmp/manzo-ai-m2-content-catalog.json
```

Il file di output è **fuori** dalla directory pubblica `_site` e non deve essere caricato come pagina Web. Non sono richieste credenziali Supabase o SMTP.

## Design di destinazione prima di M3

Il database attuale contiene 15 tabelle RLS, ma `app.courses` e `app.course_versions` richiedono `organization_id`. Sono **tabelle B2B tenant-scoped**, non un catalogo pubblico generale: non inserire contenuti pubblici con un tenant inventato.

Per M3 si deve deliberare e verificare una struttura distinta di metadati pubblici, ad esempio:

- `content_public.catalog_courses` per le chiavi stabili e la visibilità pubblica;
- `content_public.catalog_localizations` per locale, slug, titolo e checksum;
- `content_public.catalog_units` per unità e ordine;
- revisioni e provenienza Git legate a SHA e commit.

Questi sono **nomi di progetto, non tabelle esistenti**. Le autorizzazioni andranno definite con grant minimi, RLS dove esposto, schema API esplicitamente configurato e nessuna risposta agli esami privati nei payload. Scritture solo tramite processo di importazione autorizzato; non aggiungere una seconda sorgente editoriale manuale.

## Condizioni prima della prima importazione Supabase

1. Correzione M1 verificata sulla nuova distribuzione: eliminare il link interno rotto, snapshot delle 111 HTML/62 altri file e confronto degli hash.
2. Backup e procedura di ripristino verificabili; migrazione SQL controllata con schema pubblico separato e policy.
3. Dry-run deterministico che confronti `course_key + locale`, `SHA`, `route` e `versione` tra Git e tabelle, senza duplicati.
4. Test con accesso anonimo consentito **solo** ai metadati e alle lezioni pubbliche, negato per `app_private` e le valutazioni reali.
5. Mappa completa anche per Home, Academy, ACR, Oracle City, podcast/video, Studio e Verify; la presente fase M2 codifica **soltanto i due percorsi didattici strutturati**.

## Stato operativo e decisione

M2 prepara un contratto verificabile senza cambiare produzione. Al superamento della QA, la modifica può essere integrata in `main` senza deploy delle pagine statiche. La prima migrazione SQL/Storage richiede ancora un gate distinto; l'accesso Supabase già funzionante rimane intatto.

**Riferimenti:** [Piano maestro](MANZO_AI_MIGRATION_MASTER_PLAN_2026-11-16.md), [Audit build](MANZO_AI_RENDERED_RELEASE_AUDIT_2026-11-16.md), [Docs Supabase Database Security](https://supabase.com/docs/guides/database/secure-data), [Supabase Storage policies](https://supabase.com/docs/guides/storage/security/access-control).

## QA finale M2 — esito verificato

La [run GitHub Actions 43865791659](https://github.com/manzo8b/manzo-ai/actions/runs/43865791659) ha concluso con esito positivo le verifiche del generatore, test di regressione e produzione dell'artefatto `manzo-ai-m2-public-catalog-preview` (id `14225581355`). L'artefatto è stato ispezionato: contiene **2 percorsi, 6 varianti (IT/EN/ES), 36 unità localizzate, 42 item di autovalutazione localizzati, 42 casi localizzati**. Nessun contenuto individuale delle domande o soluzione è incluso.

**M1 risolto:** il deploy successivo alla PR #25 (run `43864931269`) contiene 0 riferimenti interni mancanti; tutti gli altri 172 file rimangono identici nei checksum, con una sola pagina video modificata.

Questo certifica il contratto di metadati **M2**; non certifica ancora la validazione JSON Schema completa con una libreria terza né l'import di dati in Supabase. Le tabelle applicative rimangono immutate.
