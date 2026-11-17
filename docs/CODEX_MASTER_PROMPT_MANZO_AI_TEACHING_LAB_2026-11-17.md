# CODEX — MASTER PROMPT / MANZO AI × AI TEACHING LAB
Versione: 2026-11-17 · Lingua operativa: italiano

## RUOLO E MISSIONE
Agisci come lead engineer, architetto software, instructional designer, UX/UI lead, esperto di accessibilità, QA engineer, reviewer di sicurezza e SEO editoriale. Se l'harness Codex supporta subagenti, delega revisioni indipendenti e integra criticamente i risultati; altrimenti esegui gli stessi controlli in sequenza.

OBIETTIVO: trasformare AI Teaching Lab da beta sviluppata in un ambiente EdTech coerente, robusto, intuitivo per un docente principiante e dimostrabile in un colloquio professionale. Solo dopo il completamento del primo gate, estendi le stesse regole di qualità alla piattaforma MANZO AI. Non reinventare il progetto, non sostituire contenuti approvati con un template generico, non dichiarare nulla senza prova.

PRINCIPIO NON NEGOZIABILE:
“Il docente progetta, l'IA assiste, il docente verifica e decide”.

LAVORA DAVVERO: inventaria, riproduci problemi, modifica i sorgenti, aggiungi test, esegui test, documenta l'evidenza, crea commit piccoli e una PR/release verificabile. Non fermarti a un piano teorico; non chiedere conferme per cambiamenti a basso rischio, reversibili e già coerenti con questi vincoli. Se una funzione non può essere verificata, scrivi NON VERIFICATO.

## REPOSITORY E BASE DI PARTENZA
- Repository: https://github.com/manzo8b/manzo-ai
- Branch di riferimento: main; apri un branch di lavoro dedicato e controlla eventuali AGENTS.md/istruzioni preesistenti prima di agire.
- Rotta pubblica prevista: /manzo-ai/it/formazione/ia-per-la-didattica/
- Publisher: theme/publish-ai-teaching-lab.py
- Workflow: .github/workflows/deploy-pages.yml e .github/workflows/ai-teaching-lab-qa.yml
- Corso sorgente: editorial/learning/ai-teaching-lab/it/ (course.json, module-01.md ... module-05.md, assessment-bank.json, scenarios.json)
- Anteprima/codice: editorial/learning/ai-teaching-lab/preview/
- Studio immagini: tools/ai-teaching-image-studio/index.html
- Studio voce: tools/ai-teaching-voice-studio/index.html
- Studio video: tools/ai-teaching-video-studio/index.html
- Workspace: tools/ai-teaching-workspace/index.html
- Mission Studio (micro-web-app formativa): tools/ai-teaching-launchpad/index.html, pubblicata dal publisher sotto /inizia/
- Contract QA: theme/check-ai-teaching-lab-contracts.cjs
- Leggi README.md, editorial/learning/ai-teaching-lab/README.md e le note di audit in docs/.
- La build Pages attuale deriva da un archivio statico site-v0.7.zip integrato da publisher: trova la reale source of truth; NON correggere soltanto HTML già generato nella cartella di output.

STATO DA NON FALSIFICARE: cinque moduli in italiano; durata complessiva di 20 ore solo STIMATA e non validata con docenti; beta non accreditata; nessun certificato, scoring ufficiale o misurazione di efficacia. Le funzioni IA generative remote NON sono integrate nei quattro Studi. Il video locale esportabile è silenzioso quando il browser lo supporta. I JSON non contengono i media binari. Il Workspace aggrega schede e approvazioni dichiarate; non certifica indipendentemente la veridicità delle verifiche. Il sito può avere codice e workflow senza che l'ultimo deploy risulti realmente completato: controllalo.

## VINCOLI DI PRODOTTO E DESIGN
- Docente principiante al centro: ogni campo e fase deve chiarire COSA FARE, PERCHÉ, ESEMPIO CORRETTO, COME CONTROLLARE IL RISULTATO, PASSO SUCCESSIVO.
- Mantieni lezioni, attività, fonti, esercitazioni, cruciverba, scenari, metodo MANZO AI come PROPOSTA operativa e non standard accreditato.
- Linguaggio italiano rigoroso, scorrevole, comprensibile, senza gergo non spiegato; titoli senza punto finale.
- UI contemporanea, non scolastica, non burocratica, non da template universitario. Sfondo #FFFFFF, testo #111827, blu #205BEB, arancione #E97E17, giallo #EDB120, rosso #DF3D34; verde soltanto per un vero stato approvato. Usa colore con significato, non come decorazione casuale. Niente beige/avorio/grigio carta, sfondi neri o testi slavati.
- Card dinamiche con gerarchia, inviti all'azione e stati chiari; non creare muri di box. Esempi avanzati e note tecniche in accordion accessibili; percorso a tappe, navigazione sempre raggiungibile.
- Mobile-first (iPhone Safari), senza doppie barre ingombranti, scroll orizzontale, menu sovrapposti, pulsanti troppo piccoli o focus nascosto. Preserva il menu MANZO AI e gli stati del corso.
- Nessuna immagine o voce di studenti reali, nessun registro, dato sanitario o identificativo di minori negli esempi. Usa esclusivamente materiali sintetici, dimostrativi o autorizzati.
- Accessibilità target WCAG 2.2 AA, da misurare e non dichiarare raggiunta senza audit.
- Nessuna chiave API nel frontend; nessuna integrazione remota fittizia. Non modificare Auth, Supabase, billing, pagamenti, segreti, dati utente o politiche di accesso senza autorizzazione esplicita, migration/review e test di sicurezza.

## FASE 0 — INVENTARIO E BASELINE OBBLIGATORIA
1. Leggi tutta l'architettura del corso e della pipeline GitHub Pages. Elenca le pagine effettivamente generate e quelle solo pianificate.
2. Controlla stato working tree, branch, cambi preesistenti e CI; non sovrascrivere lavoro non tuo.
3. Esegui i test esistenti PRIMA di cambiare codice. Registra comando, esito, errore riproducibile e cause probabili. Non dichiarare PASS se non hai eseguito un test.
4. Mappa i flussi docente: corso → Mission Studio (/inizia/) → brief locale → Studio immagini/voce/video → JSON + file originario → Workspace → revisione → export manifest/HTML → ripresa bozza. Valuta con precisione la differenza tra il brief Mission Studio e il manifest del Workspace: non fingere interoperabilità automatica tra formati distinti.
5. Crea un backlog P0/P1/P2/P3 con file coinvolti, gravità, impatto pedagogico, rischio privacy, criterio di accettazione.
6. Identifica fatti, simulazioni, esempi, funzionalità vere e meri placeholder.

## FASE 1 — HARDENING TECNICO AI TEACHING LAB
- Correggi crash, errori JS/Python, dipendenze, link interrotti, mancati file e rotture nel publisher.
- Testa i cinque schemi JSON (incluso ai-teaching-lab-mission-v0.1), import/export, reimportazione, sovrascrittura consapevole, errori su file non validi, stato di approvazione e invalidazione dopo modifiche.
- Preserva la provenienza di ogni asset e singola scena video; visualizza fonte, modello, licenza dichiarata e limiti.
- Verifica che l'importazione di una scheda non attribuisca automaticamente validità alle sue dichiarazioni; i materiali originali restano da controllare.
- Esamina memoria, URL.createObjectURL/revokeObjectURL, MediaRecorder, permessi microfono, fallback Safari, gestione errori, metadati temporali, formati audio, sottotitoli e accessibilità.
- Non promettere montaggio completo audio+video né generazione IA senza integrazione reale. Se non supportato, usa fallback comprensibile e testabile.
- Preferisci modifiche progressive, componenti riusabili e schema migration controllata. Mantieni compatibilità con i manifest v0.1 già esportati, se tecnicamente possibile.

## FASE 2 — AUDIT PEDAGOGICO E TESTI
Valuta ogni modulo e studio come farebbe un insegnante di scuola secondaria di primo grado con poca esperienza digitale e tempo limitato.
- Per ogni attività verifica: prerequisiti → obiettivo osservabile → esempio guidato → produzione attiva → prova di apprendimento → feedback → verifica docente.
- Rendi esplicito cosa scrivere, con esempi realistici, non generici. Esempio: titolo «Il viaggio di una goccia d'acqua»; risultato «ordinare e motivare le fasi del ciclo»; evidenza osservabile.
- Controlla il carico cognitivo: scorrimenti, lunghezza testi, numero di decisioni simultanee, troppe card, interazioni non spiegate, messaggi di errore.
- Mantieni UDL come riferimento contestualizzato; non attribuire risultati quantitativi a Mayer/Papert/CAST senza fonte primaria pertinente.
- Correggi ortografia, grammatica, incoerenze, fonti errate, anacronismi, affermazioni assolute, numeri inventati e link rotti. Distingui fonte primaria, deduzione, simulazione e ipotesi.
- Non riscrivere tutto per «rendere più corto»: conserva la profondità narrativa approvata, ma usa una presentazione progressiva, esempi contestuali e navigazione leggibile.
- Non cambiare il principio del controllo finale umano.

## FASE 3 — RESTYLING UX/UI E ACCESSIBILITÀ
- Unifica pattern degli Studi e del Workspace: header, sidebar, card, pulsanti, etichette, help contestuali, stati, tipografia, icone e progressione.
- Verifica su viewport 320, 375, 390, 430, 768, 1024 e 1440 px. Scatta screenshot di confronto prima/dopo, se strumenti browser disponibili.
- Correggi la barra MANZO AI + header interno + navigazione a tappe per evitare tre livelli sticky e occupazione eccessiva dello schermo.
- Mostra sul telefono prima l'attività del docente, poi i riepiloghi. Usa accordion chiari; evita blocchi introduttivi lunghissimi.
- Testa uso con tastiera, Tab, Escape, focus visibile, etichette accessibili, aria-live senza rumore e preferenza reduced motion.
- Mantieni input almeno 16px su Safari iPhone per ridurre zoom non voluto; tasti touch raggiungibili; nessun overflow.
- Non introdurre animazioni fini a sé stesse che rallentino utenti o nascondano istruzioni.

## FASE 4 — PROVA END-TO-END CON DATI SINTETICI
Implementa/automatizza il massimo di questo percorso:
1. Brief didattico sintetico.
2. Studio immagini: import immagine fittizia, alt text, checklist, JSON valido.
3. Studio voce: copione, audio sintetico o fixture autorizzata, trascrizione, JSON.
4. Studio video: due-tre scene, provenance, didascalie, WebVTT, JSON, fallback del WebM silenzioso.
5. Workspace: import dei tre JSON, stato dichiarato, verifica, export JSON/HTML, riapertura del manifest.
6. Prova negativa: file malformato, schema sconosciuto, checklist falsa, file troppo grande, approvazione invalidata, risorsa mancante.
7. Non creare né conservare dati personali. Se il browser reale non è disponibile, testa quanto consentito con fixture e segnala il resto NON TESTATO.
Prepara un esercizio pilota A di 35–45 minuti utilizzabile da un docente principiante; l'osservazione reale con docenti sarà svolta dall'autore del progetto, NON simulata come risultato.

## FASE 5 — PIPELINE, SEO, DOCUMENTAZIONE E PRODOTTO
- Usa gli script e workflow già presenti; riduci duplicazioni e fragilità. Non reinventare build o frontend senza prova del beneficio.
- Esegui almeno:
  python3 -m unittest discover -s editorial/learning/ai-teaching-lab/tests -p 'test_*.py' -v
  node --check editorial/learning/ai-teaching-lab/preview/app.js
  node --check editorial/learning/ai-teaching-lab/preview/production-studio.js
  node theme/check-ai-teaching-lab-contracts.cjs
  python3 -m py_compile theme/publish-ai-teaching-lab.py
- Segui il workflow esistente per generare la site directory; poi esegui il publisher --verify-only, i test di build e i contratti con --site. Se hai Playwright/browser, esegui smoke test del corso pubblicato e dei quattro laboratori.
- Verifica SEO/metadata/canonical/JSON-LD/sitemap, link Academy e titoli coerenti. Non inventare traduzioni EN/ES: mantenere chiaro che AI Teaching Lab è attualmente in italiano.
- Verifica privacy/cookie/legal dichiarati contro il comportamento reale e i provider effettivamente usati.
- Nessuna affermazione «WCAG conforme», «AI Act conforme», «accreditato» o «efficacia dimostrata» senza documentazione sufficiente.

## FASE 6 — SOLO DOPO IL GATE: PIATTAFORMA MANZO AI
**Decisione di architettura della HOME già definita:** leggi `docs/MANZO_AI_HOME_CONVERSATIONAL_LEARNING_ADR_2026-11-17.md`. Preserva la pagina iniziale di selezione IT/EN/ES. Le homepage localizzate devono unire un ingresso conversazionale per la scoperta degli obiettivi con un catalogo formativo e accessi a Learning/Verify/Studio. Non costruire una falsa chat generativa: se non esiste inferenza IA reale, il campo di ingresso è una ricerca guidata esplicitamente etichettata, con risultati e link autentici. Non trasformare la home in un clone di Coursera o ChatGPT. Documenta una variante di layout e benchmark prima di modificarla e applicala solo dopo il Gate 1. La scelta strategica non va riaperta per ragioni puramente estetiche.
Quando il percorso AI Teaching Lab è stabile:
- Audita homepage, Academy, percorsi formativi, navigazione IT/EN/ES, Sitelinks, sitemap, breadcrumbs, mobile, performance, coerenza tipografica e conversione verso percorsi gratuiti/premium.
- Confronta ciò che appare nella UI con il README e lo stato reale delle funzioni; My Learning, Supabase Auth e backend SaaS non devono essere descritti come pienamente operativi se sono demo, mock o non distribuiti.
- Trasferisci design tokens, accessibilità e pattern efficaci dal Teaching Lab senza modificare arbitrariamente i prodotti non correlati.
- Evita modifiche al billing, ai dati o ai servizi produttivi senza autorizzazione esplicita e un piano di rollback.

## HARNESS OPERATIVO
Se disponibile, organizza review indipendenti per: (A) architettura e deploy, (B) pedagogia e fact-check, (C) UX/mobile/accessibilità, (D) QA/sicurezza, (E) SEO/prodotto. Il supervisore integra i risultati e elimina le contraddizioni. Ogni reviewer deve citare FILE + LINEA o TEST riproducibile, non opinioni generiche.

Ciclo di lavoro per ciascun problema:
Rileva → Riproduci → Classifica rischio → Correggi il sorgente → Aggiungi test regressione → Esegui test → Valuta l'effetto UX → Commit atomico → Registra evidenza.
Non fare refactor massivi simultanei. Non rompere funzionalità esistenti per ottenere una schermata più bella.

## GATE DI ACCETTAZIONE
GATE 1 / Teaching Lab:
- Tutte e cinque le lezioni, Mission Studio e i quattro ambienti si aprono, con link andata/ritorno funzionanti.
- Flusso sintetico end-to-end completabile o eventuale limite dichiarato; nessuna perdita silenziosa di lavoro.
- Tutti i test riproducibili obbligatori passano. Zero errori bloccanti JS nei percorsi smoke effettivamente eseguiti.
- Nessun overflow orizzontale / pannello che nasconde il modulo sui viewport testati.
- Strumenti locali, API IA e approvazioni umane descritti senza ambiguità.
- Revisione editoriale e provenance coerenti e audit trail delle modifiche.
- Esito Pages e URL pubblici verificati separatamente dal solo esito del commit.

GATE 2 / MANZO AI:
- Navigazione, UX, SEO e pagine dei percorsi rilevanti verificati senza regressioni sugli altri progetti.
- Stato reale del frontend/SaaS dichiarato con precisione.
- CI e pubblicazione verificati.
Non attribuire un punteggio 8,5/10 o 9/10 come risultato scientifico: presentalo eventualmente come obiettivo qualitativo e usa prove riproducibili per convalidarlo.

## MODALITÀ DI ESECUZIONE E CONSEGNA
1. Inizia subito con audit e test baseline, senza interromperti per conferme superflue.
2. Crea un branch dedicato e commit piccoli e leggibili. Non forzare push, non cancellare branch, non sovrascrivere lavoro di altri.
3. Se l'account consente PR e CI, prepara una PR con diff, immagini di confronto e gate. Integra/pubblica modifiche statiche a basso rischio solo dopo CI verde e verifica del sito; per cambi di Auth, database, billing, dati e segreti chiedi approvazione.
4. Non lavorare «in background» senza una vera esecuzione: completa i passi eseguibili nella sessione, segnala i blocchi e continua sul lavoro indipendente.
5. Produci un report finale in italiano, strutturato così:
   - Stato iniziale realmente verificato
   - Bug e criticità per P0/P1/P2, con file e prove
   - Modifiche implementate e commit/PR
   - Test eseguiti, comandi, PASS/FAIL/NOT RUN
   - Verifiche desktop/mobile e screenshot, se disponibili
   - Stato deploy, indirizzi controllati e limitazioni
   - Valutazione pedagogica: cosa riesce a fare oggi un docente principiante
   - Lavori residui che non richiedono l'autore
   - Solo le azioni che richiedono davvero l'autore
6. Non presentare intenzioni come risultati; non inventare metriche, recensioni, certificazioni, approvazioni scolastiche o nuove funzionalità IA.

## PRIMA AZIONE DA ESEGUIRE ORA
Apri il repository manzo8b/manzo-ai. Leggi le istruzioni locali e i file di AI Teaching Lab. Esegui baseline test, controlla il publisher/CI, ricostruisci la user journey da iPhone e desktop e produci il backlog P0. Correggi subito i problemi P0 verificati, con test e commit, prima di passare all'estetica della piattaforma generale.
