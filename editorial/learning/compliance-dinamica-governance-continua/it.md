# Compliance Dinamica e Governance Continua: EU AI Act, ISO/IEC 42001 e deriva dei modelli

*Trasformare gli obblighi normativi e il monitoraggio del ciclo di vita in un vantaggio operativo, superando la trappola dei documenti statici*

MANZO AI · AI Academy · Modulo professionale · Letture di approfondimento, laboratorio e strumenti operativi

---

## Scheda del modulo

| | |
|---|---|
| **Durata** | 2,5-3 ore, incluso il laboratorio di 60 minuti |
| **Livello** | Intermedio / operativo |
| **Destinatari** | Management, compliance, DPO e legale, IT e security, project lead, responsabili di processo |
| **Prerequisiti consigliati** | Moduli "Modelli mentali e affidabilità dell'AI" e "Governare l'Autonomia" |
| **Cosa produci** | Registro AI, scheda per sistema, matrice dei ruoli, piano anti-deriva con trigger di blocco |
| **Stato normativo** | Confrontato con EUR-Lex, Commissione europea e ISO/CEN a novembre 2026. Verificare sempre il testo consolidato vigente e gli obblighi di settore prima dell’uso operativo |

### Perché questo modulo è essenziale

La maggior parte delle organizzazioni affronta la governance dell'AI con un approccio documentale: scrive una policy, compila un registro iniziale e archivia il file. Con sistemi probabilistici e servizi aggiornati dal fornitore, questa strategia invecchia in fretta.

Un sistema approvato oggi può cambiare comportamento domani, anche se nessuno tocca la tua configurazione:

- il fornitore aggiorna o sostituisce il modello sottostante;
- cambiano i dati su cui il sistema lavora;
- un reparto inizia a usarlo per uno scopo diverso da quello approvato;
- una nuova funzione AI compare dentro un software già in uso.

Allo stesso tempo, l'EU AI Act e gli standard internazionali chiedono **prove verificabili e continuità di controllo**, non dichiarazioni d'intenti.

### Obiettivo

Mettere i partecipanti in grado di:

1. mappare l'ecosistema AI reale dell'organizzazione, compresa l'AI integrata nei software SaaS;
2. classificare i casi d'uso secondo l'EU AI Act e riconoscere quando un cambio di destinazione d'uso cambia il ruolo giuridico;
3. impostare un ciclo continuo di verifica che intercetti la deriva silenziosa dei modelli (model e compliance drift).

### Missione

Sostituire la documentazione statica con un sistema di governance vivente, integrato nei processi, in cui conformità normativa e affidabilità tecnica procedono insieme.

### Risultati attesi

Al termine saprai:

- costruire e mantenere un **Registro AI** utile a team tecnici, legali e operativi;
- riconoscere i **cambi di destinazione d'uso** che espongono l'organizzazione a obblighi più stringenti;
- definire **metriche, trigger e responsabilità** per sospendere o rivalutare un sistema in produzione;
- distinguere **che cosa serve oggi** da **che cosa servirà più avanti**, evitando sia l'allarmismo sia la falsa tranquillità.

### Indice

1. Il registro che nessuno aggiorna
2. L'inventario dinamico e l'AI nascosta nei fornitori
3. Ruoli e rischio: quando da utilizzatore diventi fornitore
4. La mappa normativa: AI Act, ISO/IEC 42001 e standard tecnici
5. La deriva silenziosa: metriche e trigger
6. Laboratorio: Audit Express dell'ecosistema AI
7. Strumenti operativi, checklist e fonti

---

## Cosa è cambiato (verifica prima di usare questo modulo)

**Fonti primarie di riferimento (20 novembre 2026):** [Regolamento UE 2026/1744, testo ufficiale](https://eur-lex.europa.eu/eli/reg/2026/1744/oj), [AI Act consolidato](https://eur-lex.europa.eu/eli/reg/2024/1689), [Commissione europea – scadenze](https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act), [Commissione europea – prima norma armonizzata](https://digital-strategy.ec.europa.eu/en/library/first-harmonised-standard-supporting-ai-act-published-official-journal). Gli esempi sono didattici e non determinano automaticamente obblighi legali.

Il quadro normativo si è mosso nel 2026. Secondo le fonti consultate a novembre 2026:

| Data | Che cosa | Stato |
|---|---|---|
| 2 febbraio 2025 | Pratiche vietate (art. 5) e art. 4 sull'alfabetizzazione AI | In vigore |
| 2 agosto 2025 | Obblighi per i modelli per finalità generali (GPAI) | In vigore |
| 2 agosto 2026 | Obblighi di trasparenza dell'art. 50 (es. avvisare chi interagisce con un chatbot, etichettare contenuti sintetici) | In vigore. Per l'art. 50(2), la marcatura leggibile da macchina dei contenuti di sistemi già sul mercato ha una proroga al 2 dicembre 2026 |
| 2 dicembre 2027 | Obblighi per i sistemi ad alto rischio dell'allegato III (selezione del personale, valutazione del merito creditizio, ecc.) | Rinviati dal "Digital Omnibus on AI" |
| 2 agosto 2028 | Alto rischio incorporato in prodotti regolati (allegato I) | Rinviato |

Il rinvio è contenuto nel Regolamento (UE) 2026/1744 (Digital Omnibus on AI), entrato in vigore, secondo le fonti consultate, il 27 luglio 2026.

Tre avvertenze pratiche:

- **Il rinvio sposta le date, non gli obblighi.** Prepararsi ora costa meno che rincorrere dopo.
- **L'art. 4 è stato riformulato.** Secondo le fonti consultate, fornitori e utilizzatori devono ora "adottare misure per sostenere" l'alfabetizzazione AI del personale, senza garantire un livello specifico a ogni singola persona. Rimane l'obbligo di adottare misure per sostenere l'alfabetizzazione AI; conservare evidenze delle misure adottate è una buona prassi, non un obbligo generale di rilasciare certificati individuali.
- **Il GDPR e le altre norme si applicano già.** Valutazioni d'impatto, basi giuridiche, decisioni automatizzate (art. 22 GDPR) e normativa settoriale non aspettano le scadenze dell'AI Act.

---

## Lettura 1 · Il registro che nessuno aggiorna

Elena è responsabile dei processi in un'azienda di servizi con 220 dipendenti. Dopo il corso sull'autonomia degli agenti, la direzione le affida un compito: «Verificare che usiamo l'AI in modo conforme».

Trova un registro AI compilato a gennaio, approvato dal comitato, archiviato nella cartella della compliance. Elenca tre strumenti: un chatbot sul sito, un assistente per le email e un tool di sintesi delle riunioni. Tutto in regola, dice il documento.

Elena apre il portale del fornitore del CRM e trova una novità: da due mesi è attiva una funzione che "suggerisce automaticamente il punteggio di priorità dei clienti". Nessuno l'ha chiesta, nessuno l'ha censita. Poi legge la nota di rilascio del fornitore del chatbot: il modello sottostante è stato sostituito con una versione più recente. Le risposte di ieri e quelle di oggi non sono più garantite uguali.

### Il registro è una fotografia, il sistema è un film

Il registro di gennaio era corretto **in quel momento**. Il problema non è la mala fede, è il tempo. Una governance basata sul documento si rompe quando:

- l'organizzazione cambia strumenti o funzioni più in fretta del registro;
- il fornitore modifica il comportamento senza che l'organizzazione tocchi nulla;
- l'uso reale si allontana dall'uso dichiarato;
- nessuno ha la responsabilità di rivedere, e la revisione non ha una scadenza.

### Un registro vivo ha tre caratteristiche

1. **È alimentato da eventi, non solo da compilazioni periodiche.** Un nuovo acquisto, una nota di rilascio, un cambio di termini contrattuali, una richiesta di un reparto: ognuno apre una verifica.
2. **Ha un responsabile per ogni voce.** Senza un System Owner con nome e cognome, nessuno risponde dell'aggiornamento.
3. **Collega ogni sistema ai suoi controlli.** Non basta sapere che esiste: serve sapere quali test lo riguardano, quando sono stati eseguiti e che cosa farebbe scattare una sospensione.

La regola del modulo: **un registro che non si aggiorna da solo, o per scadenza o per evento, è già obsoleto.**

**Micro-esercizio.** Apri il registro, l'elenco degli strumenti o il foglio che la tua organizzazione usa oggi per tenere traccia dell'AI. Scrivi la data dell'ultimo aggiornamento, chi lo ha fatto e che cosa lo farebbe aggiornare domani.

**Riflessione.** Se il fornitore principale cambiasse domattina il modello sottostante, chi nella tua organizzazione lo scoprirebbe e in quanto tempo?

*[ ] Ho letto e compreso questa sezione*

---

## Lettura 2 · L'inventario dinamico e l'AI nascosta nei fornitori

Elena capisce che non può governare ciò che non vede. Decide di partire dalla domanda giusta: non "quali chatbot abbiamo?", ma **"dove tocca l'AI i nostri processi?"**

### Tre famiglie di sistemi

| Famiglia | Esempi | Rischio tipico |
|---|---|---|
| **Sviluppati o configurati internamente** | Chatbot sul sito, agenti, automazioni, prompt condivisi | Dati e permessi mal progettati (vedi modulo precedente) |
| **Acquistati come prodotto AI** | Assistenti di scrittura, tool di trascrizione, piattaforme di selezione | Fornitore, contratto, uso dei dati, versione del modello |
| **AI integrata in software già in uso** | CRM, suite d'ufficio, gestionale HR, helpdesk, strumenti di contabilità | È la più invisibile: la funzione compare con un aggiornamento e può essere attiva per default |

Il rischio maggiore spesso è nella terza riga, perché nessun processo d'acquisto l'ha vista passare.

### Mappatura end-to-end: le informazioni minime

Per ogni sistema, Elena raccoglie:

- **Cosa fa** e **per quale processo** (scopo dichiarato).
- **Dati in ingresso e in uscita:** categorie (personali, riservati, pubblici), provenienza, destinazione.
- **Invio verso modelli esterni:** dove vanno i dati, chi è il fornitore del modello, in quale paese vengono trattati.
- **Garanzie contrattuali:** uso dei dati per addestramento, conservazione, sub-fornitori, preavviso in caso di modifiche.
- **Versione del modello o del servizio**, se il fornitore la dichiara, e come viene comunicato un cambio.
- **System Owner:** persona responsabile della verifica periodica.
- **Utenti e processi coinvolti**, per capire dove un errore farebbe danno.

### Come trovare l'AI che nessuno ha censito

1. **Elenco del software** dalla funzione acquisti o IT, incluse le licenze di reparto.
2. **Note di rilascio e centri impostazioni** dei software principali, cercando funzioni "assistente", "suggerimenti", "riepilogo", "copilot", "insights".
3. **Log di rete e di accesso** (con il supporto dell'IT) per individuare servizi AI esterni.
4. **Domande ai reparti:** "Quali strumenti usi per accelerare il lavoro, anche se non sono ufficiali?" Con un tono che incoraggi la risposta, non la punizione.
5. **Contratti e allegati sui trattamenti dei dati**, per trovare sub-fornitori AI.

### Domande da fare al fornitore

- Quali funzionalità AI integra il prodotto, e quali sono attive per default?
- Quali modelli usa e di quale fornitore? Posso fissare una versione o avere un preavviso sui cambi?
- I miei dati vengono usati per addestrare o migliorare i modelli? In quali condizioni?
- Dove avvengono trattamento e conservazione? Con quali sub-responsabili?
- Quali log posso ottenere per ricostruire cosa ha fatto il sistema?
- Come mi comunicate modifiche sostanziali, incidenti o cambi dei termini?
- Quali evidenze avete di test, valutazioni e gestione dei rischi?

Le risposte vanno **conservate** nel registro, con data e interlocutore.

**Micro-esercizio.** Scegli un software che usi ogni giorno (CRM, suite d'ufficio, gestionale). Cerca nelle impostazioni o nelle note di rilascio se contiene funzioni AI. Annota che cosa fa, quali dati usa e se l'hai attivata tu.

**Riflessione.** Quale strumento nel tuo lavoro ha acquisito funzioni AI dopo l'acquisto? Chi ha deciso di attivarle?

*[ ] Ho letto e compreso questa sezione*

---

## Lettura 3 · Ruoli e rischio: quando da utilizzatore diventi fornitore

Elena nota che il reparto risorse umane ha configurato un assistente generico per **ordinare i curriculum** in base all'aderenza agli annunci. Nessuno ha pensato che si tratti di una scelta giuridicamente rilevante. Il tool è nato per scrivere testi, non per selezionare persone.

### I ruoli dell'AI Act in breve

- **Fornitore (provider):** chi sviluppa un sistema AI, o lo fa sviluppare, e lo immette sul mercato o lo mette in servizio con il proprio nome o marchio.
- **Deployer (utilizzatore professionale):** chi usa un sistema AI sotto la propria autorità, in un contesto professionale.

Gli obblighi sono diversi. Per i sistemi ad alto rischio, il fornitore risponde della conformità tecnica (gestione del rischio, documentazione, valutazione di conformità, monitoraggio dopo la commercializzazione); l'utilizzatore risponde di uso conforme, sorveglianza umana, conservazione dei log e informazione delle persone interessate, tra gli altri.

### L'articolo 25: il cambio di ruolo

L'art. 25 dice, in sostanza, che un utilizzatore (o altro soggetto) **assume gli obblighi del fornitore** di un sistema ad alto rischio quando, tra l'altro:

- mette il proprio nome o marchio su un sistema ad alto rischio già esistente;
- apporta una modifica sostanziale a un sistema ad alto rischio, che resta ad alto rischio;
- **modifica la destinazione d'uso di un sistema non classificato come ad alto rischio, anche generico, in modo che diventi ad alto rischio.**

È il terzo caso quello più trascurato. Un assistente generico usato per ordinare candidature **non cambia software, cambia scopo**. Questo può incidere sulla qualificazione giuridica e, al ricorrere dei presupposti dell'art. 25, determinare obblighi da fornitore; **non è un automatismo basato sul solo utilizzo dell'AI**. Occorre valutare destinazione d'uso, sistema concreto, ruolo e applicabilità dell'art. 6 e dell'allegato III con consulenza competente.

### La destinazione d'uso va scritta e controllata

Nel registro, la **destinazione d'uso approvata** deve essere una frase precisa, per esempio: "Riassumere riunioni interne per uso del team. Non usare per valutare le persone." Ogni uso diverso richiede una nuova valutazione **prima** dell'avvio, non dopo.

### Come classificare un caso d'uso: una sequenza di domande

1. **È una pratica vietata?** (art. 5) Per esempio inferire le emozioni delle persone sul luogo di lavoro, salvo eccezioni mediche o di sicurezza. Se sì: non si fa.
2. **Rientra nell'allegato III (alto rischio)?** Tra gli ambiti: selezione e valutazione del personale; accesso a servizi essenziali, incluso il merito creditizio delle persone fisiche (con l'eccezione del rilevamento delle frodi); istruzione; infrastrutture critiche.
3. **Interagisce direttamente con persone o genera contenuti sintetici?** Allora scattano gli obblighi di trasparenza dell'art. 50.
4. **Altrimenti,** non assumere automaticamente rischio minimo: verifica prima le condizioni dell'art. 6, eventuali obblighi di trasparenza, altre previsioni dell'AI Act e le norme applicabili (GDPR, diritto del lavoro, contratti, sicurezza e policy). Questa sequenza è un filtro didattico, **non una classificazione legale completa**.

Due precisazioni:

- Un caso può rientrare in **più categorie** (un chatbot che raccoglie dati per decisioni sul credito).
- L'art. 6(3) prevede deroghe per sistemi dell'allegato III che non comportano un rischio significativo, ma **chi le invoca deve documentarlo** e, secondo le fonti consultate, l'obbligo di registrazione di queste valutazioni è stato mantenuto dall'Omnibus. È un terreno da concordare con la consulenza legale.

### Obblighi già operativi, indipendentemente dall'alto rischio

- **Pratiche vietate:** si applicano dal 2 febbraio 2025.
- **Alfabetizzazione AI:** misure per sostenere la competenza del personale, da documentare.
- **Trasparenza (art. 50):** se un chatbot interagisce con persone, devono essere informate che parlano con un sistema AI, salvo che sia ovvio dal contesto; i contenuti sintetici vanno gestiti secondo l'art. 50.

**Micro-esercizio.** Prendi un caso d'uso che conosci e scrivi: (a) la destinazione d'uso approvata in una frase; (b) un uso diverso che potrebbe nascere "per comodità" nel reparto; (c) se quell'uso diverso cambierebbe la classificazione.

**Riflessione.** Chi controlla, nella tua organizzazione, che l'uso reale di uno strumento coincida con l'uso approvato?

*[ ] Ho letto e compreso questa sezione*

---

## Lettura 4 · La mappa normativa: AI Act, ISO/IEC 42001 e standard tecnici

Il responsabile legale chiede a Elena: «Dobbiamo certificarci ISO 42001 per essere in regola con l'AI Act?». La risposta onesta è: **no, ma servono strumenti complementari**. Elena disegna una mappa per non confondere piani diversi.

### Tre strumenti, tre funzioni

| Strumento | Che cos'è | A che cosa serve | Punti di attenzione |
|---|---|---|---|
| **EU AI Act** (Regolamento UE 2024/1689, modificato dal Regolamento 2026/1744) | Legge europea, obbligatoria | Definisce ruoli, classi di rischio, divieti, obblighi di trasparenza, alto rischio, sanzioni | Si applica per fasi; le scadenze sono cambiate nel 2026 |
| **ISO/IEC 42001:2023** | Standard internazionale volontario per un sistema di gestione dell'AI (AIMS) | Organizza a livello aziendale ruoli, politiche, valutazione dei rischi e degli impatti, gestione dei fornitori, audit e miglioramento continuo. Integrabile con ISO/IEC 27001 e con il sistema privacy | È certificabile, ma **la certificazione non equivale a conformità all'AI Act** |
| **EN 18286:2026** | Norma europea volontaria sul **sistema di gestione della qualità** per fini regolatori dell'AI Act, sviluppata da CEN-CENELEC JTC 21 | Traduce i requisiti dell'art. 17 (sistema di gestione della qualità dei **fornitori** di sistemi ad alto rischio) in un sistema operativo, costruito sul ciclo di vita del sistema AI | Secondo le fonti consultate è stata pubblicata a luglio 2026 e citata nella Gazzetta ufficiale UE in ottobre. Verifica lo stato sul sito CEN-CENELEC e in Gazzetta ufficiale prima di dichiarare presunzione di conformità |

### Correzione importante rispetto a molte sintesi

Spesso si legge che l'EN 18286 serva a "dimostrare la conformità tecnica del singolo sistema". **Non è così:** è una norma sul **sistema di gestione della qualità** (art. 17), non sulla conformità tecnica del prodotto. I requisiti tecnici (gestione del rischio, qualità dei dati, documentazione tecnica, accuratezza, robustezza, cybersecurity, ecc.) sono oggetto di **altre norme armonizzate** che CEN-CENELEC sta ancora sviluppando.

La distinzione pratica diventa:

- **ISO/IEC 42001**: governo dell'organizzazione sull'AI, a prescindere dal livello di rischio dei singoli sistemi.
- **EN 18286**: QMS del **fornitore** di sistemi ad alto rischio, legato all'art. 17.
- **Norme tecniche di prodotto** (in sviluppo): requisiti dei singoli sistemi ad alto rischio.

Per un'organizzazione che è principalmente **utilizzatore**, ISO 42001 è un riferimento utile di struttura; l'EN 18286 interessa soprattutto se è (o rischia di diventare) fornitore.

### Come evitare duplicazioni

- Parti dal **registro e dai ruoli**: servono a tutti i framework.
- Usa **una sola matrice dei controlli**, con colonne per ciascun riferimento (AI Act, ISO 42001, GDPR, policy interna).
- Se esiste già un sistema ISO 27001 o qualità, **estendilo**, non duplicarlo.
- Conserva **evidenze**, non solo procedure: log, verbali di verifica, esiti di test, approvazioni.

### Il contesto italiano

In Italia è in vigore anche una legge nazionale sull'intelligenza artificiale (Legge 132/2025), che affianca il regolamento europeo e individua autorità nazionali competenti. Verifica con la consulenza legale come si applica al tuo settore.

**Micro-esercizio.** Disegna una tabella a tre colonne (AI Act, ISO 42001, GDPR). Per un caso d'uso che conosci, scrivi in ciascuna una domanda a cui dovresti saper rispondere.

**Riflessione.** Nella tua organizzazione, le funzioni legale, IT, privacy e qualità lavorano su un registro comune o su documenti separati?

*[ ] Ho letto e compreso questa sezione*

---

## Lettura 5 · La deriva silenziosa: metriche e trigger

Una mattina il tasso di ticket inoltrati agli operatori dal chatbot di Elena sale dal 12% al 21%. Nessuno ha cambiato il prompt. Il fornitore ha aggiornato il modello due settimane prima. Le risposte sono più lunghe e meno precise sui prodotti più recenti.

### Le cause della deriva

| Causa | Esempio | Come la noti |
|---|---|---|
| **Aggiornamento del modello da parte del fornitore** | Nuova versione, alias che punta a un modello diverso, deprecazione di una versione | Note di rilascio, cambio di comportamento sui test, variazioni nei log |
| **Deriva dei dati (data drift)** | I clienti scrivono in modo diverso, nuovi prodotti, stagionalità | Cambio nella distribuzione degli input, calo di accuratezza sul campione |
| **Modifiche ai connettori e alle fonti** | Nuovi documenti in una base di conoscenza, API cambiata, permessi aggiornati | Risposte basate su fonti diverse, errori nei richiami |
| **Estensione non autorizzata dell'uso** | Un reparto usa lo strumento per un processo non approvato | Confronto tra utenti e scopi nei log e nel registro |
| **Cambio contrattuale o normativo** | Nuovi termini del fornitore, nuove scadenze legali | Monitoraggio contrattuale e normativo con responsabile |

Il rischio non è solo tecnico: una deriva può spostare il sistema da una fascia di rischio all'altra senza che nessuno lo decida.

### Un controllo continuo ha quattro componenti

1. **Baseline.** Un insieme di casi di prova (campione fisso) con risposte valutate, da rieseguire. Senza baseline non si misura il cambiamento.
2. **Metriche di allarme.** Indicatori concreti, con soglia e frequenza.
3. **Trigger.** Eventi che impongono una verifica o la sospensione, indipendenti dal calendario.
4. **Responsabilità.** Chi misura, chi decide, chi può sospendere, chi riattiva.

### Esempi di metriche di allarme

- **Tasso di escalation umana:** quante conversazioni passano a un operatore. Variazione oltre una soglia concordata.
- **Accuratezza sul campione di prova:** risultato dei test ricorrenti, con soglia minima.
- **Anomalie nei log:** risposte vuote, errori di strumenti, richieste ripetute, rifiuti improvvisi.
- **Reclami o correzioni da parte degli utenti**, classificati per tipo.
- **Contenuti senza fonte** o fuori perimetro, nei sistemi che dovrebbero citare documenti.
- **Segnalazioni di errore su gruppi specifici di persone**, quando il sistema tocca decisioni che li riguardano.

### Esempi di trigger di sospensione o di nuovo audit

- **Cambio di versione del modello** o del servizio sottostante.
- **Aggiornamento dei termini contrattuali** o del trattamento dei dati del fornitore.
- **Estensione a un nuovo processo, reparto o categoria di persone.**
- **Incidente** o segnalazione grave.
- **Modifica normativa** o nuove indicazioni delle autorità competenti.
- **Superamento di una soglia** di metrica per due rilevazioni consecutive.

Per ogni trigger va indicata la risposta: **sospendere**, **ridurre il perimetro**, **rieseguire i test** o **riapprovare**. Un trigger senza azione è solo una nota.

### Quando il sistema ha già fatto danno

La deriva non si previene del tutto. Per questo servono **registro degli incidenti, correzione e lezione appresa**. Per i sistemi ad alto rischio, quando sarà il momento, l'AI Act prevede obblighi di monitoraggio e di segnalazione degli incidenti gravi. Chi ha già un processo funzionante sarà più avanti.

**Micro-esercizio.** Per un sistema che conosci, scrivi tre metriche di allarme (con soglia) e tre trigger (con azione). Poi indica chi riceve l'allarme.

**Riflessione.** Se il fornitore cambiasse versione del modello senza avvisare, quale dei tuoi controlli lo rileverebbe?

*[ ] Ho letto e compreso questa sezione*

---

## Lettura 6 · Laboratorio: Audit Express dell'ecosistema AI

**Durata:** 60 minuti. **Modalità:** individuale o in gruppi di 3-4 persone. **Dati:** solo scenari fittizi, nessun documento reale.

Elena costruisce la scheda operativa di conformità e monitoraggio continuo per un'azienda ipotetica di servizi.

### Fase 1 · Caccia all'AI nascosta (15 minuti)

Analizza questo inventario di 8 strumenti. Per ciascuno decidi: ha funzioni AI (native o di terzi)? Quali dati tratta? Invia dati a modelli esterni? Chi è il System Owner?

| # | Strumento | Nota dell'inventario |
|---|---|---|
| 1 | Gestionale HR | Modulo "suggerimenti candidati" attivo dall'ultimo aggiornamento |
| 2 | CRM vendite | Funzione "priorità del cliente" e riepilogo email |
| 3 | Suite email e calendario | Assistente di scrittura incluso nella licenza |
| 4 | Helpdesk / servizio clienti | Chatbot sul sito, base di conoscenza collegata |
| 5 | Strumento di trascrizione riunioni | Registra, trascrive e riassume |
| 6 | Foglio di calcolo condiviso | Funzione di analisi in linguaggio naturale |
| 7 | Strumento di contabilità | Classificazione automatica delle fatture |
| 8 | Piattaforma di produttività del team | Assistente per task e note, attivabile dai singoli |

**Output richiesto:** una riga di registro per ciascun strumento (usa il modello nella sezione "Strumenti operativi").

**Indicazioni per la correzione.** Gli strumenti 1, 2, 3, 4, 5, 6, 7 e 8 hanno tutti, secondo la nota, funzioni AI. Le differenze stanno in dati e rischio: HR e CRM trattano dati personali e influenzano decisioni su persone; il chatbot interagisce con l'esterno; la trascrizione tratta conversazioni; il foglio di calcolo può ricevere dati riservati. Verifica poi quali funzioni sono state attivate per default e da chi.

### Fase 2 · Semaforo AI Act e cambio di ruolo (20 minuti)

Valuta quattro scenari. Per ciascuno indica: **classificazione**, **obblighi immediati**, **rischio di cambio di ruolo (art. 25)** e **prima azione**.

**Scenario A · Screening automatico e ranking dei CV.** L'azienda usa un assistente generico per ordinare le candidature.

**Scenario B · Assistente conversazionale per il supporto clienti esterno.**

**Scenario C · Sintesi automatica delle riunioni interne del team.**

**Scenario D · Valutazione preliminare dell'affidabilità finanziaria dei clienti.**

### Soluzione guidata (da confrontare con la tua)

| Scenario | Classificazione indicativa | Obblighi e attenzioni | Rischio cambio di ruolo (art. 25) | Prima azione |
|---|---|---|---|---|
| **A** | Selezione e valutazione del personale: ambito dell'allegato III, quindi **alto rischio** (obblighi dal 2 dicembre 2027 secondo il calendario aggiornato) | Già oggi: GDPR (anche art. 22), non discriminazione, informazione dei candidati, art. 4 AI Act, divieti dell'art. 5. Evitare qualsiasi inferenza emotiva | **Da valutare con priorità alta.** L'art. 25 può attribuire obblighi da fornitore quando un cambio di destinazione d'uso soddisfa i presupposti normativi; non basta cambiare un prompt per affermare automaticamente che il ruolo è cambiato | Sospendere l'uso dello strumento generico per il ranking, riportare il processo a decisione umana documentata, avviare la valutazione di un sistema conforme |
| **B** | Rischio limitato con **obblighi di trasparenza** (art. 50) | Informare chi interagisce che si tratta di un sistema AI, salvo che sia evidente; piano di escalation a operatore; gestione dei dati; controllo contenuti | Basso, finché non decide su diritti, crediti o reclami in modo vincolante | Verificare l'avviso nell'interfaccia, il perimetro delle risposte e le metriche di escalation |
| **C** | Rischio minimo ai sensi dell'AI Act, con attenzione a GDPR e policy | Informare i partecipanti, definire conservazione e accessi, vietare l'uso per valutare le persone | Medio se i riepiloghi iniziano a essere usati per giudicare prestazioni o comportamento dei dipendenti; l'inferenza delle emozioni sul lavoro è vietata (salvo eccezioni mediche o di sicurezza) | Scrivere la destinazione d'uso e il divieto di uso valutativo; verificare dove vanno registrazioni e testi |
| **D** | **Dipende dal soggetto valutato.** La valutazione del merito creditizio delle **persone fisiche** rientra nell'allegato III (con eccezione per il rilevamento delle frodi). Per clienti che sono **persone giuridiche** il quadro può essere diverso | GDPR e art. 22, trasparenza verso gli interessati, possibilità di contestare, correttezza dei dati, sorveglianza umana | Alto se uno strumento generico è impiegato per produrre un punteggio su persone fisiche | Chiarire se i clienti sono consumatori, ditte individuali o società; fermare decisioni automatiche finché la classificazione non è confermata dal legale |

Nota didattica: la classificazione è **indicativa**. Un caso reale richiede l'analisi del testo normativo, delle linee guida della Commissione e del contesto. Se due persone competenti danno risposte diverse, **registra il dubbio e applica la lettura più prudente**.

### Fase 3 · Piano anti-deriva e trigger di blocco (25 minuti)

Scegli il sistema più critico emerso dall'analisi e compila:

**A. Tre metriche di allarme**

| Metrica | Soglia | Frequenza | Chi la misura |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

**B. Tre eventi trigger**

| Evento | Azione immediata | Chi decide | Condizione di riattivazione |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

**C. Baseline.** Quanti casi di prova, chi li valuta, ogni quanto vengono rieseguiti.

**D. Evidenze da conservare.** Quali log, esiti di test, verbali e approvazioni dimostrano che il controllo è avvenuto.

### Rubrica di valutazione

Assegna **0** = non definito, **1** = definito parzialmente, **2** = definito con prova e procedura.

| Criterio | 0-2 |
|---|---|
| (A) Inventario completo, con funzioni AI nei software di terzi e System Owner | |
| (B) Classificazione e ruoli, con destinazione d'uso scritta e dubbi registrati | |
| (C) Metriche e baseline misurabili, con soglie | |
| (D) Trigger con azione, responsabile e condizione di riattivazione | |
| (E) Evidenze conservate e verificabili | |

**Condizione di blocco (STOP).** Qualunque sistema in produzione **senza System Owner**, uso in un ambito potenzialmente vietato o ad alto rischio **senza valutazione**, oppure assenza di una persona che possa sospendere il sistema, comporta **STOP**, indipendentemente dal punteggio totale.

Un punteggio alto in laboratorio non certifica la conformità all'AI Act, al GDPR o a ISO/IEC 42001. È una prova didattica sul processo progettato.

**Domanda finale.** Sapresti dire a un revisore, senza aprire nessun documento, quali sistemi AI usi, per che cosa, chi ne risponde e che cosa ti farebbe fermare ciascuno?

*[ ] Ho letto e compreso questa sezione*

---

## Strumenti operativi

### 1. Modello di Registro AI (una riga per sistema)

| Campo | Contenuto |
|---|---|
| ID e nome del sistema | |
| Fornitore e prodotto, piano e versione/modello (se noto) | |
| Tipo | Interno / prodotto AI / AI integrata in software |
| Destinazione d'uso approvata (una frase) | |
| Usi esplicitamente vietati | |
| Reparti e utenti | |
| Dati trattati (categorie) e flussi verso l'esterno | |
| Ruolo dell'organizzazione | Utilizzatore / fornitore / da valutare |
| Classificazione AI Act e motivazione | Vietato / alto rischio / trasparenza / minimo / dubbio |
| Garanzie contrattuali | Non-training, conservazione, sub-fornitori, preavviso modifiche |
| Sorveglianza umana | Chi, come, con quali poteri |
| System Owner e sostituto | |
| Metriche, baseline, trigger | Riferimenti al piano anti-deriva |
| Ultima verifica / prossima verifica | |
| Evidenze | Link a log, test, approvazioni |

### 2. Matrice delle responsabilità (esempio)

| Attività | Business owner | System Owner | IT/Sicurezza | Privacy/DPO | Legale/Compliance |
|---|---|---|---|---|---|
| Censire un nuovo sistema | R | A | C | C | I |
| Approvare la destinazione d'uso | A | R | C | C | C |
| Classificare il rischio | C | C | I | C | A/R |
| Monitorare metriche | I | A/R | R | I | I |
| Sospendere un sistema | A | R | R | I | I |
| Riapprovare dopo un trigger | A | R | C | C | C |

*R = esegue, A = risponde, C = consultato, I = informato. Adatta ruoli e nomi alla tua organizzazione.*

### 3. Calendario di revisione

- **Per evento:** nuovo acquisto, nota di rilascio, cambio di termini, nuova richiesta di uso.
- **Trimestrale:** controllo delle metriche e dei trigger sui sistemi principali.
- **Semestrale:** riesame del registro e delle classificazioni.
- **Annuale:** revisione della policy, dei ruoli e delle misure di alfabetizzazione AI del personale.

### 4. Piano a 30, 60 e 90 giorni

**Primi 30 giorni:** inventario con i reparti, individuazione dei System Owner, elenco delle funzioni AI nei software principali, blocco degli usi in ambito potenzialmente vietato o ad alto rischio.

**Entro 60 giorni:** classificazione dei sistemi, destinazioni d'uso scritte, domande ai fornitori e raccolta delle risposte, avvisi di trasparenza per i chatbot, avvio delle misure di alfabetizzazione.

**Entro 90 giorni:** baseline e metriche sui sistemi critici, trigger con azioni, procedura di sospensione provata, prima revisione del registro con comitato.

---

## Glossario di riferimento

**Registro AI:** inventario vivo dei sistemi AI, con ruoli, usi, dati, rischi, controlli ed evidenze.
**System Owner:** persona responsabile di un sistema AI, della sua verifica periodica e del suo aggiornamento nel registro.
**Fornitore (provider):** chi sviluppa o fa sviluppare un sistema AI e lo immette sul mercato o in servizio con il proprio nome o marchio.
**Utilizzatore (deployer):** chi usa un sistema AI sotto la propria autorità in un contesto professionale.
**Destinazione d'uso:** scopo per cui un sistema è stato progettato e approvato. Cambiarla può cambiare la classificazione e il ruolo.
**Alto rischio:** categoria dell'AI Act per sistemi in ambiti elencati (allegato III e allegato I), con obblighi specifici.
**Modifica sostanziale:** variazione di un sistema che incide sulla sua conformità o sullo scopo previsto.
**AIMS (AI Management System):** sistema di gestione dell'AI secondo ISO/IEC 42001.
**QMS (Quality Management System):** sistema di gestione della qualità; per l'AI Act, art. 17 ed EN 18286.
**Norma armonizzata:** norma europea citata nella Gazzetta ufficiale che, se applicata, dà presunzione di conformità ai requisiti corrispondenti.
**Deriva del modello (model drift):** cambiamento del comportamento di un sistema, per aggiornamenti, dati o contesto, senza interventi diretti dell'organizzazione.
**Deriva dei dati (data drift):** variazione della distribuzione dei dati reali rispetto a quelli di riferimento.
**Trigger:** evento che impone sospensione, nuova verifica o riapprovazione.
**Baseline:** insieme di casi di prova con risultati di riferimento, usato per misurare i cambiamenti.

## Fonti e riferimenti

- Regolamento (UE) 2024/1689 (AI Act), testo su EUR-Lex: https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- Regolamento (UE) 2026/1744 (Digital Omnibus on AI), testo ufficiale: https://eur-lex.europa.eu/eli/reg/2026/1744/oj
- Commissione europea, quadro normativo sull'AI: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
- Commissione europea, standardizzazione dell'AI Act: https://digital-strategy.ec.europa.eu/en/policies/ai-act-standardisation
- ISO/IEC 42001:2023, sistemi di gestione dell'intelligenza artificiale: https://www.iso.org/standard/42001
- Commissione europea, pubblicazione della prima norma armonizzata EN 18286:2026 (art. 17): https://digital-strategy.ec.europa.eu/en/library/first-harmonised-standard-supporting-ai-act-published-official-journal
- NIST, *AI Risk Management Framework*: https://www.nist.gov/itl/ai-risk-management-framework
- MANZO AI, moduli collegati: *Costruire in sicurezza* e *Governare l'Autonomia*

*Revisione editoriale: novembre 2026. Corso formativo, non consulenza legale né audit di conformità. Le date, le classificazioni e gli stati delle norme riportati si basano su fonti secondarie consultate a novembre 2026 e possono cambiare: prima dell'uso operativo verifica i testi ufficiali, i contratti con i fornitori e gli obblighi applicabili al tuo settore, con il supporto di consulenza legale e privacy.*

### Controllo qualità editoriale · November 2026

- **Norma o raccomandazione?** Il regolamento è obbligatorio nel suo campo di applicazione; ISO/IEC 42001 resta volontaria e la conformità all'una non sostituisce l'altra.
- **Classificazione o ipotesi?** Gli scenari A–D sono prove di ragionamento, non determinazioni giuridiche su soggetti identificati.
- **Monitoring o drift?** Cambi di modello, dati e scopo devono generare verifiche separate, con baseline documentata.
- **Regola di arresto:** STOP nella rubrica significa interrompere la simulazione e rivalutare; in un'azienda reale servono competenze e procedure approvate.
