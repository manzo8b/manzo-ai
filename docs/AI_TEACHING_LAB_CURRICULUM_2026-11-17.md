# MANZO AI · AI Teaching Lab
## Intelligenza Artificiale per la Didattica — progettare, insegnare e valutare nell'era dell'IA

**Versione:** proposta editoriale 0.1 · 17 novembre 2026  
**Stato:** bozza operativa per revisione pedagogica e QA; NON pubblicato, NON accreditato, NON erogato  
**Origine:** rielaborazione didattica del documento fornito «IA per la didattica — percorso formativo docenti»  
**Pubblico:** docenti di scuola primaria e secondaria, formatori e referenti digitali; adattamenti necessari per infanzia, sostegno e istruzione adulti  
**Modalità progettate:** laboratorio in presenza con formatore; versione digitale guidata in fase di sviluppo  
**Carico previsto:** 20 ore = 5 moduli × 4 ore; per erogazione asincrona l'effort va ancora validato in un pilota  
**Lingua redazionale:** IT; EN/ES future solo con revisione disciplinare e localizzazione normativa  
**Competenze in uscita:** saper selezionare strumenti, individuare limiti ed errori, produrre materiali accessibili, progettare feedback e verifiche, costruire un prototipo sicuro di tutor, documentare decisioni e responsabilità.

### Posizionamento e promessa formativa

Non «impara 20 tool IA» ma «sai decidere se e come usare l'IA per raggiungere un obiettivo educativo, dimostrandone il valore e controllandone i rischi».

Il corso segue il principio **obiettivo → evidenza dell'apprendimento → attività → tecnologia → verifica**, in coerenza con il *constructive alignment*: obiettivi osservabili, pratica autentica, criteri espliciti. La piattaforma non si sostituisce a un formatore, al dirigente, al DPO o a consulenti qualificati.

### Prerequisiti, accesso ed equità

Nessuna programmazione richiesta. Occorrono capacità digitali di base (browser, file, testo); strumenti esterni SOLO se autorizzati dall'istituto/erogatore, con esempi sintetici alternativi offline. Nessun account studente è necessario per le simulazioni. Il corso deve offrire versione testuale, trascrizioni, controllo della tastiera e media alternativi, con eventuali materiali stampabili.

### Learning outcomes misurabili

Al termine il corsista:
1. Formula un obiettivo didattico osservabile e distingue benefici da novità tecnologica, motivando una scelta o un non-uso.
2. Descrive il funzionamento essenziale di un LLM, individua almeno tre categorie di errore e verifica affermazioni tramite fonti primarie.
3. Progetta prompt contestualizzati, produce materiali e li sottopone a revisione contenutistica, cognitiva e di accessibilità.
4. Riprogetta una valutazione con criteri trasparenti, documentazione del processo e alternative con/senza IA.
5. Riconosce i rischi relativi a dati personali, trasparenza, bias e impieghi vietati/critici, decidendo quando sospendere o chiedere autorizzazioni.
6. Prototipa un tutor socratico con limiti di comportamento, prove di funzionamento e supervisione umana.
7. Consegna un'unità di apprendimento riutilizzabile, illustrandone obiettivi, evidenze, rischi, adattamenti e revisioni.

### Competenze e riferimenti

- **UNESCO AI Competency Framework for Teachers (2024):** human-centred mindset; ethics of AI; foundations and applications; AI pedagogy; AI for professional development. Percorso soprattutto Acquire → Deepen. Non rivendica livello Create in 20 ore.
- **DigCompEdu:** impegno professionale, risorse digitali, insegnamento/apprendimento, valutazione, valorizzazione studenti, facilitazione competenze digitali.
- **CAST UDL Guidelines 3.0:** possibilità alternative di coinvolgimento, rappresentazione, azione ed espressione; no semplificazione uniforme per tutti.
- **Commissione europea, Ethical Guidelines for educators aggiornate 2026:** scenari, checklist, uso critico e prudente dei dati.
- **AI Act / GDPR / MIM:** consultare sempre testi consolidati, atti nazionali vigenti e policy dell'istituzione alla data di erogazione. Un parere su schema di decreto NON equivale a decreto definitivo.

### Struttura metodologica

Ogni modulo dura **240 min**, ripartiti in **48 min di input/analisi guidata, 144 min di lavoro su caso e laboratorio, 48 min di restituzione/feedback e trasferimento**. Durante la sperimentazione verificare che le attività richiedano davvero tale tempo. L'esperienza digitale suddivide gli stessi obiettivi in microlezioni fruibili anche su smartphone e attività autogestite; non basta assegnare 4 ore a una pagina web.

Prima del modulo 1: **diagnosi iniziale (non selettiva, 10–15 minuti integrata nel modulo)** su lessico, scelta strumenti, valutazione fonti e privacy. Al termine di ogni modulo: microverifica non punitiva, rubriche di feedback e un artefatto. Nessun percorso forzato se le risorse non sono accessibili.

---

## Modulo 1 — Prima il problema, poi lo strumento

**Domanda motrice:** se lo stesso obiettivo è raggiungibile senza IA, qual è la prova che l'IA migliori il processo?  
**Competenze:** progettare la scelta; distinguere efficacia da velocità; confrontare privacy, accessibilità, costo e affidabilità.

**Input guidato (48 min):** esaminare «insegnare il ciclo dell'acqua in una classe quinta» in tre varianti (spiegazione, esperimento, interrogazione) e definire indicatori osservabili. Mappare tipologie di sistemi (LLM, generazione immagini/audio, traduzione, trascrizione, tutor) senza pubblicizzare prodotti. Distinguerne capacità dimostrate da marketing.

**Laboratorio (144 min):**
1. **Caso di partenza** — descrivere classe, prerequisiti, obiettivo, vincoli (nessun identificativo di minori).
2. **Comparazione A/B** — due soluzioni alternative, di cui una può essere senza IA. Testare con input sintetici identici, registrare output, limiti e costi.
3. **Matrice di decisione 0–3** per: coerenza con obiettivo, verificabilità, accessibilità, protezione dati, tempo/costo, controllo docente. Soglie di esclusione: non ammissibile se uno strumento richiede dati reali non autorizzati o introduce un uso vietato, indipendentemente dal punteggio.

**Debrief (48 min):** ogni gruppo difende una scelta o una rinuncia; peer review controlla se i criteri sono giustificati.

**Artefatto M1:** Scheda A+ (obiettivo, prova di apprendimento, test, matrice, esito, motivazione, rischio residuo).  
**Errore da prevenire:** selezionare il chatbot «più creativo» senza valutare le esigenze didattiche.

## Modulo 2 — Dentro l'IA, oltre le risposte convincenti

**Domanda motrice:** come distinguo una risposta plausibile da una risposta utilizzabile in classe?  
**Competenze:** spiegare LLM senza antropomorfismi o assoluti non dimostrati; classificare errori; applicare verifica delle fonti; costruire prompt con criteri.

**Input (48 min):** token e previsione probabilistica del token successivo (semplificazione didattica); ruolo di istruzioni, contesto, dati esterni, limiti di aggiornamento; differenza tra risposta, evidenza e decisione. RAG e citazioni possono aiutare, ma non garantiscono la verità. Un LLM non è un sostituto della verifica bibliografica.

**Laboratorio (144 min):**
1. **Caccia alle prove** — testo IA simulato: «Nel 2019 Maria Montessori scrisse una guida all'IA nelle scuole, pubblicata a Roma». Il docente distingue anacronismo storico, affermazione non verificata e fonte inventata; non deve cercare solo un prompt «più forte».
2. **Diagnosi dei fallimenti** — etichettare 8 affermazioni come verificata / non verificata / smentita con motivazione e fonte; distinguere bias, errore aritmetico, citazione inesistente e prompt injection in un documento non attendibile.
3. **Prompt laboratorio** — stendere versione iniziale e revisionata: ruolo (facoltativo), obiettivo, pubblico, input consentito, vincoli, struttura output, istruzione di esprimere incertezza e separare fatti/ipotesi. Ripetere 2 prove con stessa rubrica.

**Debrief (48 min):** confronto del registro delle evidenze e casi in cui «non so» è la risposta corretta.

**Artefatto M2:** registro claim → fonte primaria → passaggio/data → esito → revisore → azione, con due prompt versionati.  
**Nota:** non insegnare che «scrivere il prompt perfetto elimina le allucinazioni».

## Modulo 3 — Il laboratorio dei contenuti

**Domanda motrice:** quando un contenuto generato aiuta davvero a imparare?  
**Competenze:** progettare contenuti multimediali cognitivamente coerenti e accessibili, con verifica e licenze.

**Input (48 min):** carico cognitivo, essenzialità e segnalazione visiva, leggibilità, testo alternativo, trascrizioni, sottotitoli, diritto d'autore e provenienza. Evitare animazioni puramente ornamentali che ostacolano la comprensione.

**Laboratorio (144 min):**
1. Produrre una spiegazione breve con obiettivo, prerequisiti ed esempio corretto verificato.
2. Costruire tre risorse coordinate: **scheda di una pagina, quiz di 5 item con feedback per ogni distrattore, schema o immagine con descrizione testuale alternativa**. Possibile sostituire l'immagine con una tabella testuale accessibile.
3. Simulare una revisione a tre ruoli: docente disciplinare, lettore che cerca ambiguità, revisore di accessibilità. Registrare versione prima/dopo.

**Debrief (48 min):** presentazione del kit e motivazione degli adattamenti.

**Artefatto M3:** micro-kit con obiettivo osservabile, fonti, indicazione d'uso dell'IA, checklist accessibilità, licenze, registro modifiche.  
**Nota:** nessuna immagine con testo IA non controllato deve essere assunta come corretta.

## Modulo 4 — Una classe, molte possibilità di apprendere

**Domanda motrice:** posso rendere accessibile il percorso senza abbassare gli obiettivi?  
**Competenze:** differenziazione, UDL, feedback formativo, integrità, valutazione del processo.

**Input (48 min):** differenza tra accessibilità, personalizzazione e profilazione; uso degli strumenti compensativi nei contesti consentiti; UDL (engagement, representation, action/expression); limiti del rilevamento automatico di testo IA e dei punteggi opachi.

**Laboratorio (144 min):**
1. Partire da un caso sintetico: gruppo di studenti con letture diverse, plurilinguismo e preferenze di espressione differenti, senza diagnosi o profili reali.
2. Riprogettare **lo stesso obiettivo** in almeno due percorsi: testo chiaro + supporti visivi/lettura assistita; percorso con approfondimento. Esplicitare quello che rimane comune e il criterio di successo.
3. Convertire una prova in due versioni: **con IA dichiarata e controllata** e **senza IA**, entrambe con evidenze di ragionamento, revisione e restituzione orale/situata. Creare feedback descrittivo (cosa è riuscito, cosa manca, prossimo passo).

**Debrief (48 min):** analisi dei bias introdotti e della sostenibilità per il docente.

**Artefatto M4:** prova doppia, rubrica 4 livelli, esempi di feedback, adattamenti motivati.  
**Nota:** vietato inferire diagnosi, disabilità o capacità individuali tramite chatbot su dati reali.

## Modulo 5 — Progettare esperienze intelligenti e sicure

**Domanda motrice:** come verifico che un tutor aiuti senza sostituire lo studente o compromettere i dati?  
**Competenze:** progettare tutor socratico, guardrail, test; documentare privacy, controllo umano e limiti; integrare le evidenze dei quattro moduli.

**Input (48 min):** specifica di un tutor formativo (ambito, target, contenuti autorizzati, non-obiettivi, escalation). Distinguere uso docente, uso collettivo su proiezione e accesso individuale con account.

**Laboratorio (144 min):**
1. Definire un tutor «guida, non risolve»: uno stimolo alla volta, domanda socratica, esempi progressivi, adattamento della spiegazione, richiesta di giustificazioni, limiti epistemici.
2. Condurre **6 test con input sintetici**: (a) richiesta di soluzione completa; (b) contenuto errato; (c) tentativo di estrarre dati; (d) richiesta di giudizio su studente reale; (e) linguaggio discriminatorio; (f) richiesta di istruzioni fuori tema. Registrare risposta attesa, osservata e intervento correttivo. Non promettere comportamento infallibile.
3. Finalizzare unità di apprendimento: obiettivi, durata, attività, uso/non-uso di IA, kit M3, prova M4, criteri di valutazione, matrice rischi e responsabilità del docente/istituzione.

**Debrief (48 min):** demo, revisione fra pari e decisione motivata: da usare / da rivedere / da non usare.

**Artefatto M5:** unità didattica finale + 6 test + scheda rischio + dichiarazione di uso IA.  
**Nota:** nessun prototipo è pronto per minori o classi reali senza specifica adozione e autorizzazione organizzativa.

---

## Matrice di valutazione finale

Valutazione autentica su **100 punti**, con evidenze richieste e feedback motivato:

| Criterio | Punti | Evidenze richieste |
|---|---:|---|
| Allineamento pedagogico | 25 | Obiettivi, attività, assessment coerenti |
| Accuratezza e verificabilità | 20 | Fonti, verifiche, correzioni documentate |
| Protezione dati e gestione rischi | 20 | Minimizzazione, matrice rischi, decisione go/no-go |
| Inclusione e accessibilità | 15 | Alternative UDL, leggibilità, supporti e barriere |
| Documentazione del processo | 10 | Prompt/prototipi, versioni, interventi umani |
| Riflessione professionale | 10 | Limiti, miglioramenti, trasferimento in classe |

**Criterio proposto di superamento didattico:** almeno 75/100, almeno metà dei punti in ciascun criterio e nessun *critical fail*: dati personali reali di minori conferiti a tool non autorizzati; decisione automatica che incide su persone; impiego vietato dall'AI Act; evidenza/fonti intenzionalmente inventate presentate come vere. Il punteggio proposto è una **rubrica editoriale**: non è un voto scolastico né una certificazione riconosciuta. Il controllo dei critical fail avviene tramite revisione umana. La correzione di quiz pubblici sul client non equivale a valutazione sicura per attestati.

Per un'erogazione guidata si prevede: prova d'ingresso, 5 checkpoint formativi, portfolio di 5 artefatti, progetto valutato, autoriflessione e, ove autorizzato, feedback qualitativo a 30–60 giorni. L'efficacia della formazione va misurata su prestazioni comparabili e non solo sul gradimento.

## Esempio di esperienza interattiva: dilemma di uso responsabile

**Scenario simulato:** «Un docente ha 27 elaborati, con nomi e voti; un servizio IA gratuito propone di caricarli per generare feedback».  
**Scelte:** A. caricare tutto; B. cancellare i soli nomi e procedere; C. fermarsi, verificare autorizzazione/policy e usare nel frattempo esempi sintetici senza dati personali.

**Esito formativo:** C è la scelta corretta per la simulazione. Rimuovere nomi non garantisce anonimato e non sostituisce valutazione del titolare/responsabile. Il sistema deve chiedere la motivazione prima di mostrare il feedback, non limitarsi a un badge «giusto/sbagliato».

**Trasferimento:** scrivere un prompt didattico equivalente su un elaborato completamente fittizio; registrare il rischio residuo e chi autorizza l'uso. L'output non deve essere caricato o memorizzato.

## Schede riutilizzabili

**A+ — Decisione strumento**
- ID caso, ordine e disciplina, obiettivo osservabile, prova di apprendimento
- Soluzioni comparate inclusa alternativa senza IA; input sintetici identici
- Criteri (0–3), fonti delle caratteristiche dichiarate, data del test
- Condizioni di esclusione, decisione, controlli e reversibilità

**B+ — Prompt e verifica**
- Problema, destinatari, prerequisiti, fonti ammesse, dati vietati, formato, vincoli
- Fatti da verificare, incertezza, registro claim, esito e azione
- Iterazioni A/B, valore osservato rispetto all'obiettivo

**C+ — Accessibilità e valutazione**
- Obiettivo invariato, barriere anticipate, alternative di accesso/espressione
- Rubrica comune, evidenze di processo, feedback azionabile
- Modalità dichiarata di assistenza IA e possibili alternative senza IA

**D+ — Unità finale**
- Scuola/grado in termini generici; disciplina; prerequisiti; obiettivi; durata
- Attività, sequenza, strumenti, ruolo IA/docente, fallback offline
- Risorse e licenze, accessibilità, verifica, trasparenza, registro fonti
- Dati previsti, base e ruoli del trattamento da verificare con istituzione/DPO
- Risk register, test, decisione go/no-go, limiti e manutenzione

## Governance, sicurezza e formulazioni accurate

1. **Non usare dati personali di studenti** in sistemi esterni non autorizzati. Se sono coinvolti dati reali, prima stabilire scopi, ruoli, base giuridica, accordi e misure, coinvolgendo dirigente e DPO ove necessario; un docente non inventa da solo una base di liceità.
2. **Anonimizzazione ≠ pseudonimizzazione.** Eliminare soltanto nomi, matricole e indirizzi può lasciare elementi reidentificanti. Usare preferibilmente casi interamente sintetici durante il corso.
3. **AI Act:** alfabetizzazione art. 4; alcuni usi in istruzione e formazione (es. accesso/ammissione, certe valutazioni) sono classificati ad alto rischio nel perimetro previsto dalla norma; non ogni chatbot educativo è «alto rischio». Inferenza delle emozioni in istruzione generalmente vietata, salvo le eccezioni definite dalla legge. Verificare applicabilità e calendario aggiornato.
4. **Italia:** Linee guida MIM 2025 (DM 166/2025). Il Garante ha espresso il 20 ottobre 2026 parere su uno *schema* di decreto con allegato tecnico; non presentare lo schema come disciplina definitiva senza verificare il decreto pubblicato.
5. **Valutazione:** evitare affidamento esclusivo su rilevatori di testo IA per accuse, voti o sanzioni. Non pretendere «compiti a prova di IA»; usare pratiche verificabili e resilienti.
6. **Tutoring:** supervisione effettiva, nessuna profilazione occulta, logging proporzionato, niente promesse di diagnosi o valutazione automatica.
7. **Conformità:** il percorso è educazione professionale; non equivale a parere legale e non attesta di per sé adempimento dell'art. 4 o certificazione del singolo.

## Esperienza prodotto MANZO AI — design/UX

**Card Academy:** «AI Teaching Lab», kicker «EDUCATION / PROFESSIONAL LEARNING», 5 moduli, 20 h di progetto, livello base/intermedio; CTA «Esplora il percorso». Nessun finto rating, recensione, numero iscritti, badge accreditamento o certificato.

**Pagina corso:** hero bianco con tipografia leggera e accento cobalto/turchese; valore pratico e prerequisiti; 5 card colore intenso coordinate con gli altri corsi; indice compatto; esempi; glossario; fonti e data revisione; dichiarazione «proposta formativa in sviluppo» finché non pronto.

**Lettore:** unità brevi con «questo imparerai», esempio annotato, interazione *scenario → scelta → motivazione → feedback*, checklist, risorsa scaricabile, riepilogo; progressi solo se salvataggio reale implementato. Hover discreto, focus evidente, reduced-motion, contrasto WCAG da misurare, mobile 390 px senza overflow, niente punto finale in H1–H6.

**Funzionalità in ordine di rilascio:**
- Fase 1: source JSON + redazione approvata + esempi pubblici statici; nessuna raccolta dati
- Fase 2: pagina corso IT e lezioni nella build ufficiale; SEO/canonical/sitemap; test manuali e CI, localizzazione EN/ES validata
- Fase 3: dati e progressi riservati su Supabase solo dopo gates RLS, tenant, backup, assessment server-side e privacy
- Fase 4: eventuale offerta B2B/docenti, con condizioni e accrediti solo dopo verifica specifica

**Non alterare senza approvazione:** login pilota, tabelle esistenti, migration M2/M3, checkout, homepage approvata e corsi esistenti. Gli export pubblici di quiz contengono risposte e non sono idonei a una banca d'esame privata.

## Quality assurance prima della pubblicazione

- Pedagogia: tutti gli obiettivi misurabili; evidenze per unità; esempio realmente completabile; rubrica coerente; tempi verificati nel pilota; almeno un caso in cui non usare IA.
- Accuratezza: fonti primarie consultabili e datate; affermazioni normative perimetrare; test che distinguono errore, non verificato e falso.
- Accessibilità: tastiera, focus, ordine di lettura, alternative media, no solo colore, dimensionamento e contrasto.
- Privacy: niente dati reali, terze parti di tracciamento non necessarie, controllo policy e licenze.
- Tecnica: schema contenuti validato, link non rotti, URL e canonical consistenti, sitemap aggiornata, 0 errori JS, responsive e reduced-motion.
- Governance: denominazione del prodotto veritiera, nessun accredito/attestato dichiarato, revisore responsabile e data ultima verifica.

### Registro delle fonti verificate il 17 novembre 2026

1. UNESCO — AI Competency Framework for Teachers, 2024: https://www.unesco.org/en/articles/ai-competency-framework-teachers
2. Commissione europea — DigCompEdu: https://education.ec.europa.eu/document/european-framework-for-the-digital-competence-of-educators-digcompedu
3. Commissione europea — Ethical guidelines aggiornate, 2026: https://education.ec.europa.eu/focus-topics/digital-education/actions/plan/ethical-guidelines-for-educators-on-using-artificial-intelligence
4. CAST — UDL Guidelines 3.0: https://udlguidelines.cast.org/
5. AI Act Service Desk — Articolo 4: https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4
6. AI Act Service Desk — Education and vocational training: https://ai-act-service-desk.ec.europa.eu/en/education-and-vocational-training
7. MIM — Linee guida IA scuole v1.0 (2025): https://www.mim.gov.it/documents/8099600/8784171/MIM_Linee%2Bguida%2BIA%2Bnella%2BScuola_09_08_2025-signed.pdf/4bfecbc5-70e1-2973-940f-1aa818a9f3f6?version=1.0
8. Garante Privacy — parere 20 ottobre 2026 su schema di decreto: https://www.garanteprivacy.it/web/guest/home/docweb/-/docweb-display/docweb/10315228
9. EEF — Teacher Feedback to Improve Pupil Learning: https://educationendowmentfoundation.org.uk/education-evidence/guidance-reports/feedback

**Editorial risk:** queste fonti cambiano. Ogni release richiede controllo del testo vigente, soprattutto AI Act e provvedimenti nazionali. Le citazioni normative hanno fine divulgativo.

---
**MANZO AI · Bozza per progettazione e QA · Non pubblicare come corso erogabile o certificato senza i gate sopra indicati**
