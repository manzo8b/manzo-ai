# MANZO AI — Audit di prodotto e piano di commercializzazione

**Data:** 16 novembre 2026  
**Base verificata:** branch `main`, GitHub Actions e database Supabase MANZO AI interrogato in sola lettura; confronto con funzionalità ufficiali di Coursera for Business, Docebo, 360Learning e LearnWorlds.  
**Direzione:** un prodotto reale, altamente dinamico, incentrato su applicazione e verifica delle competenze. Non dichiarare leadership di mercato senza test competitivi.

## 1. Visione di prodotto: tre verticali, una sola identità

- **Learning (priorità MVP):** percorsi AI per professionisti, team e formatori, con apprendimento applicato, feedback, assessment validato e dashboard aziendale.
- **Verify (modulo differenziante):** verificare output AI attraverso affermazioni, fonti, controlli e decisioni motivate, con evidenze esportabili.
- **Studio (fase successiva):** workspace di progettazione e produzione di siti e flussi digitali, con versioning, anteprima, export e agente AI controllato.

**Vantaggio proposto, da testare:** trasformare una lezione in un'azione concreta con output verificato e tracciabile. Non inseguire Coursera sul numero di corsi.

## 2. Completato — evidenze attuali

| Ambito | Evidenza | Stato |
|---|---|---|
| Portale pubblico | GitHub Pages IT/EN/ES; build/deploy QA #43944936055/#43944936022 riusciti | LIVE |
| Identità visiva | Home premium, Academy, 6 card in evidenza e 3 percorsi guidati, mobile/test Chromium | LIVE |
| Materiali pedagogici | Archivio M01–M06, corsi specialistici Allucinazioni AI e Engineering Assurance, quiz ed esercizi | PUBBLICI; non assessment enterprise |
| SEO | Sitemap 94 URL, canonical e metadati, 3 mappe HTML, audit link e ancore | TECNICAMENTE VALIDATO, non indicizzazione Google |
| Product Lab | Studio brief JSON client-side, Verify euristico e Learning configuratore locale | DEMO, no AI live |
| Identity | Supabase Auth su invito, un utente; SMTP Brevo collaudato per pilota | PILOTA |
| PostgreSQL | 15 tabelle; migrazioni 0001–0003; RLS; PostgreSQL 17.11 in UE | LIVE, senza dati B2B |
| M3b backup | dump locale applicativo + hash e restore isolato, confronti strutturali e dati; Auth presente nell'archivio | PARZIALE (non DR Auth/SMTP completo) |
| M2/M3 | Catalogo metadata-only e SQL 0004 preparata e testata isolatamente | NON DEPLOYATO |
| B2B/API | Modello grants/seats/enrollments/progressi/quiz e adapter Edge nel codice | NON OPERATIVO |

## 3. Fatti backend verificati al 16/11

- Supabase ref: `bjydnaejpxwubmxpnpnv`, `ACTIVE_HEALTHY`, regione `eu-west-1`.
- `auth.users=1`; `app.organizations=0`, `app.courses=0`, `app.memberships=0`, `app.enrollments=0`, `app.learning_attempts=0`.
- `core_tables=15`; `content_public/content_internal=0` tabelle; `storage.buckets=0`; Edge Functions distribuite **0**.
- Security Advisor: 7 INFO `rls_enabled_no_policy` in `app_private` coerenti con deny-by-default; 1 WARN password leak detection disabilitata (valutare hardening).
- Nessun pagamento, cliente B2B o metrica commerciale attestata.

## 4. Gap prioritari per poter vendere

| Priorità | Deliverable | Criterio osservabile | Dipendenza |
|---|---|---|---|
| **P0** | Decisione di mercato: target formatori/PMI che adottano AI, una promessa centrale e pacchetto pilota | 10–15 conversazioni discovery, 2 offerte concrete, obiezioni documentate | Contatto buyer e decisione titolare |
| **P0** | Chiusura recovery e security | Backup cifrato, GRANT verificati, piano Auth/SMTP e restore esercitato, login/revoca testati | Accesso privato e procedure titolare |
| **P0** | Import catalogo M3b controllato | Migration 0004, import idempotente 2 corsi/6 lingue/36 unità, rollback, RLS | P0 recovery |
| **P1** | Primo flusso Learning B2B end-to-end | Un'organizzazione autorizzata; 1 corso; iscrizioni per utenti verificati; progressi persistenti; prove server-side; report admin | Edge API autentica, tenant/ruoli |
| **P1** | Dynamic Learning UX | Dashboard My Learning (riprendi, salva, completa); obiettivi e rubriche; casi interattivi; feedback verificabile | P1 API/dati |
| **P1** | QA commerciale e WCAG/performance | Zero accessi cross-tenant; WCAG 2.2 AA su percorso vendita e studio; misure reali LCP/INP/CLS | Browser audit e test utenti |
| **P1** | Packaging/legal/operazioni | Contratti, privacy/DPA/retention, help/support, backup, rate limit, monitoraggio e policy AI | Decisione prodotto e consulenze richieste |
| **P2** | Domini e hosting commerciale | Origine propria, DNS, email autenticata, deploy/rollback e disponibilità | Budget e scelta titolare |
| **P2** | Billing in test mode, poi commerciale | Prezzi lato server, signed webhooks, revoca/expiry, test di rimborso e quote | App sicura e offerta validata |
| **P3** | Verify enterprise, poi Studio agentico | Oggetti/prove/fonti esportabili; workflow approvazioni; progetti con versioni, quota e publishing controllato | Primo Learning pilota riuscito o diversa scoperta commerciale |

L'etichetta P indica la precedenza logica: non è una promessa di data o completamento.

## 5. Funzioni dinamiche — progettate, non ancora esistenti

1. **Onboarding per obiettivo:** ruolo, livello, risultato richiesto → sequenza consigliata, non casuale.
2. **Lesson → Practice → Verify → Apply:** esercizio reale e feedback ragionato, rubriche e fonti, risultati salvati solo dopo autenticazione.
3. **My Learning reale:** ripresa cross-device, progressi verificabili, contenuti salvati e micro-ripassi in base agli errori.
4. **Skill evidence passport:** registro delle prove svolte e degli output controllati, non certificato accreditato.
5. **AI tutor con guardrail:** risposte ancorate alle fonti del corso, incertezza visibile, nessuna invenzione di risultati, limiti d'uso/costo.
6. **Tutor e manager cockpit:** iscrizioni, materiali, assegnazioni, competenze osservabili, audit trail, report esportabile.
7. **Verify integrato:** l'allievo deve motivare perché un output AI è affidabile; evidenza delle fonti e revisione umana.
8. **Studio integrato solo in una fase matura:** esercizi sul progetto digitale vero e export con codice/test/anteprima, approvazione esplicita prima della pubblicazione.

**Essenziale:** animazioni e card sono interfaccia, non un prodotto dinamico. La dinamicità si misura dal cambiamento del percorso in risposta a competenze, attività e risultati verificati, senza opacità né profilazione non necessaria.

## 6. Benchmark: non vendere come novità ciò che i concorrenti già offrono

- **Coursera for Business:** percorsi di competenza e pratica, contenuti enterprise, verifica dei risultati. https://www.coursera.org/business/skill-tracks
- **Docebo:** piattaforma learning/skills, conoscenza aziendale, tutor e agenti AI, automazioni. https://www.docebo.com/products/agents/
- **360Learning:** co-authoring di contenuti, AI support e collaborazione dei docenti. https://360learning.com/product/authoring-tool/
- **LearnWorlds:** video interattivi, domande e feedback inseriti nel filmato. https://www.learnworlds.com/product/features/interactive-video/

**Posizionamento MANZO AI:** meno catalogo massivo, più workflow professionali specifici **con output verificabili**; spiegare e misurare un beneficio concreto a un target riconoscibile.

## 7. Inizio vendita: definizione di done

Un buyer incaricato di una squadra di test deve poter:
1. vedere un'offerta e un perimetro autentici;
2. ottenere accesso autorizzato in un tenant isolato;
3. assegnare un corso a tre learner di prova;
4. far svolgere un caso pratico e una prova corretta server-side;
5. leggere i progressi effettivi e scaricare un report;
6. ricevere supporto, informazioni privacy e un accordo di servizio;
7. cessare l'accesso ed esportare i dati nei termini concordati.

**Finché manca questo scenario completo, il prodotto non è commercialmente pronto come SaaS LMS, pur con un sito pubblico professionale.**

## 8. Metriche proposte per il pilota (target interni, non risultati reali)

- **Attivazione:** percentuale di utenti invitati che iniziano il primo esercizio.
- **Time-to-first-value:** tempo fino alla prima analisi AI verificata consegnata.
- **Competenza:** risultato in un caso nuovo dopo il percorso, non solo tempo sul sito.
- **Coinvolgimento:** ripresa del percorso e completamento di almeno un caso.
- **Affidabilità:** accessi cross-tenant non autorizzati = zero nei test; errori auth e API tracciati.
- **Business:** discovery svolte, pilot offerti/accettati, costo di servizio per organizzazione, margine e rinnovi.

## 9. Decisioni prodotto

**Raccomandazione:** Learning B2B è la prima verticale vendibile; *Verify* ne diventa l'elemento distintivo; *Studio* conserva roadmap e asset, senza implementare tre SaaS contemporaneamente. Questo massimizza la probabilità di un primo flusso completo e di feedback reale.

Il Mac dell'amministratore non supporta Docker Desktop, ma Supabase consente deploy Edge Function tramite Dashboard o CLI API senza Docker; privilegiare il percorso compatibile con gli strumenti disponibili. Non introdurre costi, account o dati di prova senza una decisione.

### Sorgenti di progetto
- [Piano prodotto](MANZO_AI_PRODUCT_OPERATING_PLAN_2026-11-16.md)
- [Design/SEO audit](MANZO_AI_GLOBAL_SITE_AUDIT_2026-11-16.md)
- [Piano M3](MANZO_AI_MIGRATION_MASTER_PLAN_2026-11-16.md)
- [M3b backup](MANZO_AI_M3B_BACKUP_RECOVERY_RUNBOOK_2026-11-16.md)
- [Buyer research](MANZO_AI_BUYER_RESEARCH_2026-11-15.md)
- [Roadmap GitHub](https://github.com/manzo8b/manzo-ai/issues/35)

**Questo documento è un audit e una priorizzazione, non un'autorizzazione a modifiche di produzione.**
