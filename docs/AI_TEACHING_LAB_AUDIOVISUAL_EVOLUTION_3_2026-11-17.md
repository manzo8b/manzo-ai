# AI Teaching Lab — Evoluzione 3.0 · Laboratorio audiovisivo assistito

Data: 2026-11-17
Stato: specifica di sviluppo, NON funzionalità IA implementata o pubblicata
Ambito: AI Teaching Lab, mantenendo separata la piattaforma commerciale MANZO AI

## Principio non negoziabile
**Il docente progetta, l'IA assiste, il docente verifica e decide.**
Non generare/pubblicare materiale didattico automaticamente senza consenso esplicito. Non confondere produzione browser/local con output IA.

## Base da preservare
- Percorso operativo esistente: brief -> scelta dei modelli -> storyboard -> produzione -> verifica e consegna
- Output esistenti: JSON del progetto, microlezione HTML, PNG da storyboard, registrazione voce, brevi video locali e prompt contestualizzati
- UX semplificata con sezioni progressive e navigazione mobile; niente lunghi scroll continui
- Accessibilità e didattica prima dell'effetto creativo

## Moduli v3
1. Studio immagini: tipologia (fotografia/illustrazione/schema), scopo pedagogico, target, rapporto d'aspetto, fonti e accuratezza, prompt modificabile, asset importato o generato, annotazioni e scelta finale del docente.
2. Studio voce: copione, lingua, pronuncia, velocità, registrazione locale o sintesi esterna, trascrizione accessibile, diritti e approvazione umana.
3. Studio video: storyboard per scene, tempi, immagini/clip importate o generate, voiceover, sottotitoli, esportazione, revisione di coerenza e accuratezza.

## Registro provider (configurabile, non implicito)
- Ogni provider dichiara capability (image_generate | speech_generate | video_generate), modalità (external_link | protected_api | local), requisiti, limiti, costi indicativi, lingua, privacy e condizioni d'uso da confermare.
- Candidati immagini: ChatGPT / OpenAI Images, Gemini Nano Banana. Non assumere disponibilità di API equivalenti alle interfacce web.
- Voce e video: scelta di provider solo dopo verifica API, licenze, dati e test.
- Mai inserire segreti/API key nel frontend GitHub Pages.
- In assenza di backend, offrire prompt esportabile e collegamento esterno, etichettato “Generazione esterna non integrata”.

## Architettura proposta
Frontend statico (GitHub Pages) -> controller di progetto locale -> adattatore provider (opzionale) -> backend protetto (ad es. Supabase Edge Function) -> API provider.
Autenticazione, autorizzazione, limiti di spesa, rate-limit, audit minimo e consenso esplicito prima di ogni chiamata remota.
Nessun upload di dati personali di studenti, volti o voci identificabili senza verifica della base giuridica e delle autorizzazioni pertinenti.
Preferire esempi sintetici e dati anonimi.
Conservazione locale predefinita; persistenza remota solo se richiesta e documentata.

## Contratto dati (bozza)
Project: id, version, title, subject, targetAge, learningObjectives[], assessmentCriteria[], accessibilityRequirements[], scenes[], assets[], teacherApproval.
Asset: id, kind(image|audio|video), provenance(local|uploaded|ai_external), providerId?, modelId?, prompt?, promptRevision?, source?, license?, altText?, transcript?, captions?, factualReview, accessibilityReview, approvedByTeacher, status(draft|review|approved|rejected).
GenerationJob: id, assetId, providerId, mode, userConfirmed, status(not_started|submitted|completed|failed|cancelled), error?, estimatedCost?, timestamps.
Distinguere sempre “preparato prompt”, “inviata richiesta”, “asset ricevuto”, “validato docente”.

## Flusso UX
1. Brief didattico: obiettivo, destinatari, prerequisiti, prova di apprendimento
2. Scelta media: quale formato migliora l'apprendimento e perché
3. Scelta metodo: manuale/locale, prompt per servizio esterno, integrazione API se disponibile
4. Produzione: anteprima e revisione con storico delle revisioni
5. Check docente: fedeltà alle fonti, coerenza, inclusione, diritti, privacy, audio/video accessibili
6. Consegna: JSON + HTML + asset, registro di provenienza e approvazione

## Priorità di implementazione
P0 — Preservare funzioni esistenti, introdurre etichette veritiere e schema asset/provenienza.
P1 — Studio immagini completo in modalità manuale/importazione e prompt esportabile, senza API.
P2 — Studio voce con registrazione browser, importazione, copione e trascrizione.
P3 — Studio video con timeline/storyboard locale, importazione e sottotitoli.
P4 — Provider registry e un backend protetto con una sola integrazione pilota, dopo security/cost review.
P5 — Benchmark didattico con docenti: qualità, tempi, controllo e accessibilità.

## Definition of Done e test
- Nessun pulsante “Genera con IA” che simuli un risultato locale
- Qualsiasi asset esterno ha provenienza e modello etichettati
- Nessun export/pubblicazione senza revisione docente
- Funzioni locali disponibili offline quando tecnicamente possibile
- Test iPhone Safari, desktop, tastiera, screen reader, sottotitoli, errori API e costi
- Nessuna regressione dei cinque passaggi esistenti
- Stato release descritto secondo evidenza e non intenzioni
