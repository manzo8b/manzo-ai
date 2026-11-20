# MANZO AI — Studio · Verify · Learning

**Progetto digitale in sviluppo** · IT / EN / ES · [Sito pubblico](https://manzo8b.github.io/manzo-ai/it/) · [Product Lab](https://manzo8b.github.io/manzo-ai/it/prodotto/)

MANZO AI combina progettazione di workflow digitali, verificabilità degli output AI e formazione professionale. Il codice e gli strumenti editoriali sono versionati su GitHub; la strategia prevede licenze B2B e un'eventuale acquisizione futura soltanto sulla base di asset e risultati verificabili.

### Stato verificato — 16 novembre 2026

| Area | Stato verificabile | Limite |
|---|---|---|
| Sito e corsi | Portale multilingue, Academy, sei risorse evidenziate, tre percorsi guidati e test QA | Nessun LMS commerciale attivo con progressi persistentemente collegati |
| Product Lab | Studio brief JSON, Verify euristico e demo Learning, separati dal pilota Auth reale | Nessun modello AI produttivo, scoring B2B o checkout attivo |
| Backend SaaS | Progetto Supabase MANZO AI attivo: 15 tabelle, 3 migrazioni applicate, Auth verificata, SMTP di prova | Nessuna Edge Function distribuita; zero organizzazioni, iscrizioni o dati Learning B2B |
| Billing | Contratti locali di autorizzazione e verifica della firma dei webhook | Nessun incasso o abbonamento attivato |
| My Learning | Nuovo workspace autenticato IT/EN/ES e letture API utente in codice, testati con mock isolati | Pagina pilota pubblicata con API disattivata; nessun corso o avanzamento inventato |\n| Clienti | Ricerca dei segmenti commerciali documentata | Nessun cliente, incasso o fatturato attestato |


**Piano del prossimo salto:** [My Learning v0.1 e gate di attivazione](docs/MANZO_AI_MY_LEARNING_V01_RELEASE_GATE_2026-11-16.md) · [Audit commerciale](docs/MANZO_AI_SAAS_COMMERCIAL_PRODUCT_REVIEW_2026-11-16.md). Le note successive sono storiche e non sostituiscono lo stato verificato qui sopra.

**Architettura e roadmap:** [Product Lab](product/README.md) · [Database e security QA](product/backend/README.md) · [Architettura SaaS](docs/MANZO_AI_SAAS_ARCHITECTURE_ADR001_2026-11-15.md) · [Mercati potenziali](docs/MANZO_AI_BUYER_RESEARCH_2026-11-15.md) · [Release gates](docs/MANZO_AI_PRODUCT_RELEASE_GATE_2026-11-15.md).

> La sezione seguente contiene il registro editoriale e le note storiche del sito: versioni e stati precedenti non rappresentano la piattaforma SaaS attuale.

---


## Tre lingue obbligatorie · 20 novembre 2026

Tutti i contenuti MANZO AI devono essere disponibili **integralmente in italiano, inglese e spagnolo**: lezioni, glossari, grafici, laboratori, quiz e feedback compresi, non soltanto titoli e navigazione. Consultare lo **[standard i18n Academy](theme/ACADEMY_I18N_STANDARD.md)** e l'[audit della copertura effettiva](theme/audit-academy-i18n.py).

I corsi **Costruire in sicurezza / Build Safely / Construir con seguridad**, **Prompt vs Skill**, **Governare l'autonomia / Governing Autonomy / Gobernar la autonomía**, **Compliance dinamica e governance continua / Dynamic Compliance and Continuous Governance / Compliance dinámica y gobernanza continua** e **Intelligenza aumentata, non sostituita / Augmented, Not Replaced / Inteligencia aumentada, no sustituida** sono pubblicati con lezioni e attività native IT/EN/ES. L'audit dei sorgenti editoriali del 20 novembre 2026 registra **6 corsi su 9 completi nelle tre lingue** (incluso Allucinazioni dell'IA). Rimangono non completamente localizzati **Modelli mentali e affidabilità**, **AI Product Builder — Centroni City** e **AI Teaching Lab**. Il dato 6/9 misura solo il catalogo censito, non certifica l'intera piattaforma. **Fase di sviluppo di nuovi corsi chiusa dopo questi due moduli; il passo successivo concordato è l'audit globale MANZO AI con il metodo AI Web Production, seguito da ricerca di un prodotto originale.**

## Standard delle card Academy · 19 novembre 2026

**Regola permanente di UI/UX per i nuovi corsi:** tutte le card nella Home devono essere uniformi per dimensioni, proporzioni delle copertine, padding, lunghezza dei testi, badge e CTA «Apri il percorso» su una sola riga. Colori e illustrazioni possono variare; struttura e comportamento responsivo devono rimanere coerenti. Prima della pubblicazione confrontare visivamente la nuova card con quelle esistenti su desktop e smartphone. **[Specifiche vincolanti](theme/ACADEMY_CARD_STANDARD.md).**

## HOME inclusiva + AI Academy · 18 novembre 2026

MANZO AI mantiene la selezione centrale delle lingue e propone un ingresso **per tutti**: persone curiose, studenti, professionisti, creatori e docenti. Le homepage IT/EN/ES presentano quattro obiettivi generali (fondamenti IA, prompt, allucinazioni, creazione), quattro card tematiche aggiuntive e **tutte le sei card Academy preesistenti**. AI Teaching Lab è un percorso specifico, non il pubblico principale del portale.

Il menu della homepage è sintetico e contiene sei destinazioni non duplicate. Le altre pagine tecniche e il Product Lab restano pubblicati senza essere la prima cosa proposta a ogni visitatore. [Decisione di prodotto](docs/MANZO_AI_HOME_INCLUSIVA_V2_2026-11-18.md).

**Stato:** modifiche ai sorgenti e pipeline GitHub Pages predisposte; risultato dell'ultima esecuzione, pubblicazione effettiva e QA Safari/iPhone ancora da verificare. Non è una chat IA generativa.


## Ricerca ACR · Dossier scientifico

Il nuovo dossier di ricerca applicata sull'**Adaptive Cognitive Recursion** è disponibile in [italiano](https://manzo8b.github.io/manzo-ai/it/ricerca/acr/), [inglese](https://manzo8b.github.io/manzo-ai/en/research/acr/) e [spagnolo](https://manzo8b.github.io/manzo-ai/es/investigacion/acr/). Presenta ipotesi A/B/C, memoria verificata, pilota offline, metodi e fonti. **Nessuna superiorità ACR o Fibonacci è stata dimostrata tramite esperimenti LLM.** [Note di pubblicazione](docs/ACR_DOSSIER_RELEASE.md).


**[Apri MANZO AI](https://manzo8b.github.io/manzo-ai/it/)** · **[Laboratorio tecnico](https://manzo8b.github.io/manzo-ai/it/prompt-mastery/laboratorio-tecnico/)** · [GitHub Actions](https://github.com/manzo8b/manzo-ai/actions)

**Stato operativo verificato l'8 novembre 2026:** il workflow di deploy del ramo `main` è terminato con successo dopo la correzione dei tag XML e del contrasto dei blocchi di codice. L'archivio `site-v0.7.zip` è presente nel repository; gli appunti sulle versioni 0.4–0.7 qui sotto restano **cronologia storica**, non istruzioni sullo stato attuale di pubblicazione. Il collaudo visivo su dispositivi reali resta separato dal successo del workflow.

## Revisione visiva · 3 novembre 2026

Interfaccia professionale con struttura conversazionale conservata: tipografia di sistema, superfici neutre, tinte leggere, ricerca e sidebar più sobrie. Overlay CSS su tutte le 82 pagine originali; nessun cambiamento ai contenuti o alle funzioni. [Intervento e verifiche](docs/MANZO_AI_PROFESSIONAL_REFINEMENT.md). Le note di rilascio seguenti sono il registro storico del progetto.

Portale educativo trilingue (IT, ES, EN), parte dell'ecosistema MARCELUS AI LAB.

**Sito pubblico:** https://manzo8b.github.io/manzo-ai/

## v0.7 — Technical Prompt Engineering Lab (ready for binary upload)

Approved scope: an original technical lab in IT / ES / EN inspired by Anthropic's `Prompting 101` video, used as an **optional reference** rather than embedded or reproduced course material. Includes prompt architecture, XML boundaries, JSON Schema, structured output, test fixtures and an offline Python checker. **82 static HTML pages in the v0.7 build**. No LLM benchmarks were performed. The existing v0.6 site stays live until `site-v0.7.zip` is uploaded and the publishing workflow succeeds. [Full release notes](docs/MANZO_AI_V07_TECHNICAL_COURSE.md).

## Current project milestone · 27 October 2026

- **Live release (verified): v0.5**, six complete approved lessons M01–M06 in IT/ES/EN. GitHub Pages deploy 27 October 2026 succeeded.
- **Next release (binary upload pending): v0.6 — Critical Thinking Edition.** Eight new resources per language (three crosswords, three dated news analyses and two decision dilemmas), plus localized hub: 79 HTML pages total. [Scope and QA](docs/MANZO_AI_V06_RELEASE.md).
- The GitHub Actions workflow is ready to prioritize `site-v0.6.zip` once uploaded to main. Its successful workflow completion must be checked before declaring the new pages public.

## Release

- **v0.4 (pubblicata il 27 ottobre 2026)** — otto slide 16:9 M01, visualizzatore localizzato, PDF/PowerPoint italiano e guida docente. Collegamenti da Home, Academy, M01, Risorse e Video. [Dettagli della release](docs/SLIDE_M01_V04_RELEASE.md).

- **v0.1** — Home conversazionale, M01 approvato, glossario, laboratorio e fonti.
- **v0.2 (pubblicata)** — catalogo M01–M06 con stati editoriali, area Risorse, area Video e slide, un video ufficiale Anthropic collegato senza incorporamento YouTube.
- **v0.3 (versione storica, incorporata nel percorso v0.4)** — percorso introduttivo «Che cos'è un prompt e come si scrive?» (IT/ES/EN), collegamento alla Biblioteca Prometeus dalla sezione Risorse e quattro video tutorial esterni selezionati. M01 rimane invariato; M03 resta in revisione.

**Decisione editoriale del 27 ottobre 2026:** il Product Owner ha approvato i contenuti didattici completi di **M02–M06**, preparati in IT/ES/EN. La pubblicazione online delle lezioni complete è **ancora da effettuare**: nel pacchetto v0.4 il catalogo mostra tuttora i titoli, gli obiettivi e lo stato precedente «In revisione editoriale». La lezione integrale pubblicata e già verificata editorialmente resta M01. [Registro dell'approvazione M02–M06](docs/APPROVAZIONE_M02_M06_2026-10-27.md).

## Release v0.4 — deployment completato, collaudo umano residuo

**`site-v0.4.zip`** è presente nel repository e il workflow [Deploy MANZO AI](https://github.com/manzo8b/manzo-ai/actions) ha completato con successo il deployment del 27 ottobre 2026 (commit `20d72370`). Restano da verificare a mano navigazione delle otto slide M01, schermo intero e download su desktop e smartphone. Non considerare le slide grafiche definitivamente approvate prima della revisione visuale. L'approvazione dei moduli testuali M02–M06 non cambia questo vincolo.

## Procedura storica v0.3

Carica **`site-v0.3.zip`** nella radice del repository tramite [Upload files](https://github.com/manzo8b/manzo-ai/upload/main), senza estrarlo. Il workflow pubblica automaticamente la versione più recente disponibile. Attendere un run riuscito prima di verificare `/it/prompt-mastery/che-cos-e-un-prompt/`, `/it/risorse/` e `/it/video-e-slide/` e le corrispondenti versioni ES/EN.

Dettagli editoriali e verifiche: [Registro video e percorso v0.3](docs/VIDEO_E_PROMPT_V03_REGISTRO.md).

## Procedura storica v0.2

1. Caricare **`site-v0.2.zip`** nella radice del repository tramite [Upload files](https://github.com/manzo8b/manzo-ai/upload/main), senza estrarre il file.
2. Il workflow [Deploy MANZO AI](https://github.com/manzo8b/manzo-ai/actions) si attiva automaticamente.
3. Controllare che il workflow sia riuscito prima di aprire il sito pubblico.
4. Verificare gli indirizzi:
   - IT: `/it/academy/`, `/it/risorse/`, `/it/video-e-slide/`
   - ES: `/es/academia/`, `/es/recursos/`, `/es/videos-y-diapositivas/`
   - EN: `/en/academy/`, `/en/resources/`, `/en/videos-and-slides/`

Il workflow conserva il supporto al file precedente `site-v0.1.zip` finché il nuovo archivio non è presente.

## Collegamento didattico a Prometeus Marcelus

La **Biblioteca Prometeus Marcelus** è la risorsa archivistica collegata per spiegare cosa sia un prompt, come strutturarlo e come valutarlo con esercizi commentati. L'integrazione nella pagina Risorse, in M03 e nel Laboratorio è documentata in [INTEGRAZIONE_BIBLIOTECA_PROMETEUS.md](docs/INTEGRAZIONE_BIBLIOTECA_PROMETEUS.md).

- Biblioteca pubblica IT: https://manzo8b.github.io/marcelus-v-v01/it/library/
- Non importare automaticamente l'intero catalogo e non presentare le voci come prompt tutti testati.
- Lo stato della release v0.2 pubblicata **non cambia** con questa nota documentale.

## Principi

- **Nessun chatbot o API AI**: la ricerca è un indice locale delle risorse del sito.
- Nessun login, tracciamento opzionale o database.
- M01 approvato e online; M02–M06 approvati editorialmente dal Product Owner il 27 ottobre 2026 ma **non ancora pubblicati come lezioni complete**.
- Video YouTube solo come link esterni, senza incorporamento e con attribuzione.
- Slide e nuovi download saranno creati e pubblicati dopo la revisione con il proprietario.

## Codice sorgente

L'archivio delle sorgenti v0.2 è mantenuto separato dal pacchetto di distribuzione, per agevolare aggiornamenti e test. Il workflow attuale pubblica l'archivio statico caricato.

**Non mescolare MANZO AI con il portfolio `marcelus-v-v01`.**