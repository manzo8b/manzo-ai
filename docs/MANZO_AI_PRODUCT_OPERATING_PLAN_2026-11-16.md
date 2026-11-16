# MANZO AI — Stato prodotto e priorità operative

**Data:** 16 novembre 2026  
**Architettura:** frontend pubblico su GitHub Pages, identità/dati su Supabase MANZO AI, email Auth tramite Brevo.  
**Linea creativa:** home, Academy e laboratori come un prodotto editoriale professionale; design delle sei card Academy approvato come riferimento.  
**Obiettivo:** piattaforma reale progressiva, senza funzionalità fittizie o certificazioni non implementate.

## 1. Cosa è già funzionante

| Area | Stato tecnico verificato | Esperienza disponibile |
|---|---|---|
| Home pubblica | **ONLINE** GitHub Pages, IT/EN/ES | Ricerca, orientamento, scene Studio/Verify/Learning, percorsi aperti |
| Card Academy in home | **Rilasciate nel sorgente e QA Playwright superata** | 2 card grandi + 4 secondarie identiche al catalogo, con link ai corsi pubblicati; il deploy va verificato separatamente |
| Academy | **CONTENUTI VERI** e filtrabili su Pages | Sei schede, lezioni/pratiche; nessuna iscrizione richiesta |
| Supabase Auth | **ATTIVO, PILOTA RISERVATO** | Accesso, email verificata e recupero credenziali; 1 account presente |
| PostgreSQL | **LIVE** | 15 tabelle applicative protette da RLS, migrazioni 0001–0003 applicate |
| SMTP Brevo | **COLLAUDATO PER AUTH** | Invio email; mancano le premesse per il servizio commerciale su dominio autenticato |
| M2–M3 | **PROTOTIPO TECNICO VERIFICATO** | Catalogo trilingue con SHA e SQL preparata/testata in DB isolato |
| M3b backup | **BACKUP E RIPRISTINO APPLICATIVO VERIFICATI** | Dump privato sul Mac e restore delle 15 tabelle, 8 policy e 20 FK; 0 record applicativi; backup di 1 utente, 1 identità, 1 sessione; manca recupero end-to-end Auth |
| Learning B2B | **STRUTTURA DB ESISTENTE, DEMO UI** | Nessuna azienda, licenza, iscrizione, corso B2B o avanzamento live |
| Edge Functions / Storage | **NON ATTIVI** | 0 funzioni distribuite, 0 bucket |

## 2. Scelta architetturale corretta

**Supabase NON sostituisce direttamente un hosting frontend per l'intero sito.** Per il pilota la soluzione concreta è:

- Frontend statico, Academy e risorse editoriali su `https://manzo8b.github.io/manzo-ai/`.
- Auth Supabase reale, con area riservata per gli account invitati e URL tenuti fuori dalla navigazione pubblica.
- Tabelle PostgreSQL con RLS per future organizzazioni, assegnazioni, iscrizioni e progressi: oggi sono vuote.
- Edge Functions come API protetta futura, non inventata dal frontend.
- Una sola fonte Git per il catalogo editoriale; Supabase conterrà metadati e stato applicativo al termine di M3b.

**Non** indicare come “SaaS già operativo” una console con dati simulati. Il prodotto deve essere veritiero anche quando la sua veste grafica è di livello premium.

## 3. Home Academy premium — definizione dell'intervento

Publisher: `theme/publish-home-showcase.py`. CSS: `theme/home-showcase.css`. QA: `theme/home-showcase-browser-smoke.py`.

- Legge i sei articoli **dalla build dell'Academy**, non da copie manuali o da JSON fittizi.
- Valida esistenza di tutti i link IT/EN/ES (2 percorsi, 4 lezioni per lingua).
- Riproduce microcopy, colori, badge e titoli originali; 2 card hero e 4 card secondarie.
- Aggiunge un'introduzione editoriale, CTA verso l'Academy e precisazione che Learning B2B è su invito.
- Non modifica il pacchetto statico v0.7 né login, privacy, SEO o percorsi.
- Test browser: 1440/390 px, hover, focus, reduced motion, link locali e assenza di overflow; screenshot allegati alla workflow QA.
- La home non invia dati del lettore a Supabase, perché i corsi pubblici non richiedono un account.

## 4. Sequenza per trasformare il pilota in piattaforma operativa

**A. Completamento M3b in sicurezza**
- Conservare backup cifrato fuori da Git; documentare recupero dei GRANT e ricostruzione Auth/SMTP/redirect.
- Solo dopo il gate recovery, applicare migration `0004_public_catalog_m3.sql` e importare i metadati M2, verificandone la corrispondenza hash.
- Public Data API soltanto quando esistono policy di lettura limitate; mai esporre `app_private`, service-role o quiz valutativi.

**B. Learning B2B**
- Creare due tenant di prova con inviti e autorizzazioni appropriate, test di isolamento incrociato e revoca.
- Collegare la prima Edge Function con JWT verificato server-side e CORS limitato.
- Rendere reali soltanto i flussi con persistenza confermata: corsi assegnati, moduli completati, progressi, quiz corretti sul server.
- Conservare Studio e Verify come demo chiaramente etichettate finché non esistono API vere.

**C. Qualità di prodotto**
- Sistema unico delle card, tipografia, stati, componenti di navigazione e CTA su Home, Academy, lezioni e dashboard.
- Nessun punto finale nelle intestazioni H1–H6; niente sfondi neri o avorio; bianco editoriale, colori di categoria saturi, contrasti accessibili.
- Verifiche di accessibilità, mobile, SEO, performance e protezione delle pagine private. Preview non è garanzia di certificazione WCAG.

## 5. Decisioni riservate al titolare

1. Approvazione visiva definitiva della home pubblicata sui tre idiomi.
2. Scelta dominio e hosting frontend dedicato per clienti esterni e isolamento della sessione (origine comune `github.io` da superare prima dell'uso commerciale).
3. Modello di accesso: Academy pubblica oggi; valutare eventuali nuovi corsi su invito con licenze reali.
4. Priorità commerciale tra Learning, Studio e Verify; raccomandazione tecnica: Learning come prima verticale.
5. Trattamento dati, termini, DPA, supporto, retention, prezzi e possibili pagamenti: non attivare senza scelta esplicita.
6. Gestione SMTP/URL Auth e segreti durante il recupero: configurazioni a cura del titolare, senza condividere credenziali.

## 6. Quadro sicurezza Supabase letto in sola lettura

- Auth: 1 utente; organizzazioni: 0; corsi aziendali: 0; iscrizioni: 0.
- Migrazioni: 3; tabelle M3 catalogo live: 0; Storage: 0 bucket; Edge Functions: 0.
- Security Advisor: 7 INFO su RLS senza policy per tabelle `app_private` volutamente inaccessibili; non aprirle per eliminare il warning.
- Security Advisor: password compromesse non bloccate (WARN); rimane una decisione di hardening Auth, non impedisce il lavoro sulla Home.

## 7. Evidenze

- PR Home: https://github.com/manzo8b/manzo-ai/pull/32
- Pipeline design: `.github/workflows/theme-qa.yml`
- Pipeline deploy: `.github/workflows/deploy-pages.yml`
- Piano architettura: `docs/MANZO_AI_MIGRATION_MASTER_PLAN_2026-11-16.md`
- Recupero M3b: `docs/MANZO_AI_M3B_BACKUP_RECOVERY_RUNBOOK_2026-11-16.md`

Questo rapporto descrive **funzioni realmente disponibili** e passaggi bloccati. Non autorizza da solo nuove credenziali, pagamenti o modifiche all'autenticazione.
