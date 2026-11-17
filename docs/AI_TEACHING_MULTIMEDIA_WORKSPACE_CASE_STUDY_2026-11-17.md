# AI Teaching Lab · Case study tecnico e pedagogico
Data: 17 novembre 2026 · MANZO AI · Autore/curatore del progetto: Marcelo Javier Fernandez Caballero

## Problema
Molti percorsi formativi sull'IA mostrano come generare contenuti ma non insegnano a definire una funzione cognitiva, scegliere il media adatto, verificare fonti, rispettare l'accessibilità e documentare la decisione del docente.

## Soluzione sviluppata
Un ambiente di authoring didattico che collega quattro strumenti: Studio immagini, Studio voce, Studio video e Workspace multimediale unificato, affiancati al corso AI Teaching Lab.

**Principio:** il docente progetta, l'IA assiste, il docente verifica e decide.

### Componenti
1. Studio immagini: brief, scelta formato/strumento, prompt, importazione immagine, testo alternativo, controllo qualità, scheda JSON.
2. Studio voce: copione, prompt esterno, sintesi locale di prova via browser (non IA), registrazione microfono, import audio, trascrizione, approvazione, scheda JSON.
3. Studio video: storyboard fino a 12 scene, anteprima temporizzata, importazione immagini, supporto audio solo di riferimento, esportazione WebM **silenzioso** nei browser compatibili, VTT separati, gate docente, scheda JSON.
4. Workspace: importazione delle tre schede JSON, registro di provenienza e approvazione dichiarata, progettazione della sequenza didattica, gate di approvazione finale, manifest JSON e documento HTML offline.

### Modello di qualità
- *Intento*: definire destinatari e obiettivo osservabile prima del media
- *Pertinenza*: ogni asset/scene deve svolgere una funzione didattica specifica
- *Accuratezza*: verifiche su fatti, licenze, privacy e consenso
- *Inclusione*: alt text, trascrizione, sottotitoli, alternative
- *Governance*: approvazione esplicita, invalidata dalle modifiche

## Tecnologia e limiti
HTML/CSS/JavaScript, MediaRecorder/getUserMedia, Web Speech API per lettura di prova di sistema, Canvas captureStream nei browser compatibili, Blob/URL per download, JSON/HTML/WebVTT come formati di esportazione; distribuzione tramite publisher Python su GitHub Pages.

Tutto è progettato senza account o backend obbligatori. Nessun modello generativo esterno è integrato nei quattro moduli. La produzione del browser non deve mai essere etichettata come generazione IA.

**Importante:** il Workspace non importa file binari dagli altri studi e non realizza un pacchetto ZIP con media; importa solo schede JSON, e allegati audiovisivi devono essere conservati separatamente. Le approvazioni registrate nei JSON sono autodichiarazioni, non attestazioni indipendenti.

## Evidence-based release
- Moduli e integrazione nel publisher registrati su GitHub (main)
- Workflow Pages aggiornato con trigger e gate sui file attesi
- Verifiche statiche delle dipendenze e dei marcatori effettuate
- **Non verificati in questa fase:** completamento del deploy, URL pubblico, browser UI, Safari/iPhone, Chrome, microfono, codec, reale file WebM, VoiceOver e prove pedagogiche con docenti
- Non dichiarare utenti, risultati sperimentali, risparmi di tempo, tassi di completamento o impatto formativo senza misurazione

## Impiego in portfolio e colloqui
Presentare il progetto come **prototipo EdTech di authoring multimediale governato dal docente**, con architettura progressiva e controlli espliciti. Illustrare problema, flusso completo, decisioni privacy/accessibilità, limiti tecnici e roadmap per un test con docenti reali.

## QA e prossime milestone
1. Confermare GitHub Pages e tutti i collegamenti HTTP 200
2. Eseguire smoke test desktop + iPhone su 4 strumenti
3. Testare import/export di JSON reali dai tre studi, compresi schema non valido, sostituzione risorsa e modifica dopo approvazione
4. Verificare navigazione tastiera, VoiceOver, leggibilità e zoom 200%
5. Eseguire osservazione didattica con 3–5 docenti (campione esplorativo), misurando comprensione e autonomia senza interpretare il campione come evidenza generalizzabile
6. Valutare, dopo security/legal review, un servizio IA pilota con backend protetto e consenso esplicito

## Percorsi
- tools/ai-teaching-image-studio/index.html
- tools/ai-teaching-voice-studio/index.html
- tools/ai-teaching-video-studio/index.html
- tools/ai-teaching-workspace/index.html
- theme/publish-ai-teaching-lab.py
- .github/workflows/deploy-pages.yml
