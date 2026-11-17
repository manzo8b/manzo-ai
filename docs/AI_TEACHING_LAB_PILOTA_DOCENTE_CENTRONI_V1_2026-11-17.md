# AI Teaching Lab — Prova sul campo docente: scenario Centroni, Roma
**Protocollo esplorativo v1.0 — 17 novembre 2026**
**Progetto:** MANZO AI / AI Teaching Lab
**Responsabilità didattica:** docente sperimentatore adulto
**Stato:** protocollo scritto; nessuna sperimentazione è ancora avvenuta

## Scopo e scenario

Immaginiamo una docente di **seconda classe della scuola secondaria di primo grado**, in una scuola dell'area di **Centroni (Roma)**. È una *persona ipotetica*, non un riferimento a una scuola reale o a un numero effettivo di alunni. Usa computer o telefono, ha poco tempo e non deve conoscere linguaggi di programmazione né avere un account con un servizio di IA.

**Domanda di prova:** un insegnante principiante comprende da solo il percorso, progetta una risorsa pedagogicamente pertinente, sa riconoscere la provenienza dei contenuti e riesce a salvare il lavoro senza credere che la piattaforma generi o certifichi contenuti automaticamente?

**Importante:** questo protocollo misura inizialmente l'usabilità e la comprensione del docente, **non l'efficacia sull'apprendimento degli alunni**.

## Che cosa è realmente disponibile
- Cinque moduli del corso, attività e verifiche formative: durata totale di 20 ore **soltanto stimata**.
- Studio immagini: brief, prompt, importazione immagini, testo alternativo, controllo e scheda JSON.
- Studio voce: copione, registrazione/importazione audio, trascrizione, controllo e scheda JSON.
- Studio video: storyboard, anteprima, sottotitoli separati e, solo su browser compatibili, file video WebM **silenzioso**; scheda JSON.
- Workspace: importa e riapre schede JSON, conserva provenienze dichiarate, prepara manifest e scheda HTML.
- **Non disponibili:** generazione diretta con IA via API, montaggio automatico audio+video, integrazione automatica dei media nel JSON, salvataggio online automatico, tracciamento degli avanzamenti, badge o attestati, validazione dell'efficacia del corso.
- Il funzionamento e l'esito più recente di GitHub Pages, Safari/iPhone e Chrome non sono certificati dal solo codice.

## Prova A — docente da solo, 35–45 minuti

**Obiettivo didattico ipotetico:** una classe di seconda media deve distinguere *tempo meteorologico* e *clima* usando una rappresentazione visiva e una domanda di verifica. Evitare dati meteorologici inventati.

**Prima della prova**: usare soltanto contenuti inventati o una semplice figura preparata dal docente (PNG/JPEG/WebP senza alunni); non usare registri, foto o nomi reali. Annotare dispositivo, browser e data/ora. Aprire la pagina pubblica soltanto dopo averne controllato la raggiungibilità.

1. **5 minuti — orientamento.** Dalla pagina del corso, individuare Studio immagini senza aiuto e spiegare a voce: «Che cosa fa questa pagina? Genera direttamente immagini con IA?»
2. **7 minuti — brief.** Inserire titolo, disciplina, destinatari ipotetici, obiettivo osservabile e verifica. Esempio: «Distinguere una giornata di pioggia da una tendenza climatica rilevata su periodi lunghi».
3. **8 minuti — scelta del media.** Motivare diagramma vs illustrazione; produrre o importare una figura locale appropriata. Se si usano modelli esterni, consultarne condizioni e autorizzazioni: non è richiesto per questa prova.
4. **8 minuti — accessibilità e qualità.** Scrivere un testo alternativo che descriva *le informazioni rilevanti*, non soltanto i colori; controllare la correttezza di frecce, parole e implicazioni.
5. **7 minuti — verifica e consegna.** Compilare le quattro conferme soltanto se effettivamente verificate; esportare il JSON e il file immagine separatamente; dire che cosa è contenuto nei due file.

**Esito osservabile:** la docente produce una figura dichiarata e controllata, una scheda JSON e una frase che motiva l'utilità didattica del media. Il completamento non implica che gli studenti abbiano imparato.

## Prova B — percorso completo, 60–90 minuti, *solo dopo Prova A*

1. **Studio voce** — preparare 40–60 secondi di copione, registrare con la propria voce o importare audio autorizzato, ascoltare, correggere la trascrizione, esportare audio e JSON.
2. **Studio video** — preparare 2–3 scene con immagini lecite, obiettivo per scena, didascalia, tempi e WebVTT; esportare JSON. Il WebM prodotto localmente, se supportato, è **senza traccia audio**.
3. **Workspace** — importare i tre JSON, descrivere quando l'immagine, la narrazione e il video verranno usati in aula, verificare provenienze e diritti, approvare soltanto dopo i controlli, esportare manifest e HTML.
4. **Ripresa** — chiudere la pagina, riaprire il manifest del kit e verificare che i testi siano recuperabili, che i media restino separati e che l'approvazione richieda un nuovo controllo.

**Esito osservabile:** cartella locale con risorse originali, tre schede JSON, manifest e scheda HTML. Niente condivisione con studenti o pubblicazione automatica.

## Diario della prova — una scheda per sessione

- Data (solo giorno) ______
- Dispositivo e browser ______
- Percorso A / B ______
- Il docente ha capito subito da dove cominciare? Sì / Con aiuto / No
- Ha saputo scrivere un obiettivo osservabile? Sì / Parzialmente / No
- Ha distinto operazioni locali da generazione con IA? Sì / Parzialmente / No
- Ha trovato da solo import/export? Sì / Con aiuto / No
- Ha saputo spiegare quali file vanno conservati? Sì / Parzialmente / No
- Tempo effettivo (minuti) ______
- Errori bloccanti (descrivere senza dati personali) ______
- Punti di confusione (citazioni anonime, se autorizzate) ______
- Risorsa didattica utile e accurata? Sì / Da correggere / No
- «La useresti per preparare una tua lezione?» Sì / Forse / No — perché ______
- Una sola cosa da cambiare prima della prossima prova ______

**Indicatore pratico P0:** nessuna esposizione di dati personali, nessuna falsa dichiarazione di IA generativa, nessuna perdita irreversibile del lavoro senza un avviso chiaro.
**Indicatore pratico P1:** il docente conclude la prova A senza assistenza continua e sa motivare obiettivi e verifiche.
**Indicatore pratico P2:** il percorso B produce i JSON e li reimporta senza errori bloccanti.
Queste sono *soglie interne di avanzamento*: **una prova singola non fornisce statistiche generalizzabili**.

## Passaggio successivo: 3–5 adulti volontari (se disponibili)

- Profilo eterogeneo: almeno un docente con competenze digitali di base; la partecipazione è volontaria.
- Ripetere la prova A individualmente, senza insegnare in anticipo tutte le funzioni.
- Registrare soltanto note minimizzate; non raccogliere nomi, registrazioni personali, schermate di account o informazioni dei loro studenti senza necessità e informazione/consenso appropriati.
- Dopo le prove, classificare gli ostacoli per gravità: **bloccante**, **ostacolo di comprensione**, **difetto grafico**, **miglioramento opzionale**.
- Nessuna promessa di efficacia didattica o certificazione da questo campione esplorativo.

## Prima di una proposta formale a una scuola

1. Verificare pubblicazione e funzionamento con browser reali, mobile e desktop; fare QA di import/export, microfono, formato video, ritorno nel workspace.
2. Svolgere un audit accessibilità approfondito (WCAG, tastiera, contrasto, VoiceOver) e correggere i problemi bloccanti.
3. Predisporre una *scheda del corso per la scuola*: obiettivi, destinatari, prerequisiti, articolazione, durata dichiarata come stima, costi/servizi esterni opzionali, limitazioni e documentazione di privacy/diritti.
4. Chiarire il ruolo del progetto: **prototipo formativo divulgativo, non corso ministeriale accreditato**; nessun attestato o certificazione di adempimento dell'art. 4 dell'AI Act.
5. Se la prova passa dall'uso personale di adulti all'ambiente istituzionale o coinvolge alunni, concordare il progetto con il dirigente/referente digitale e i responsabili privacy della scuola. Non presentare questo documento come autorizzazione o DPIA già effettuata.
6. Valutare solo successivamente un'eventuale procedura di adozione, licenze dei fornitori esterni, strumenti di accessibilità e impatto sulla didattica reale.

## Backlog ordinato

| Priorità | Mancanza | Condizione di chiusura |
|---|---|---|
| P0 | Verifica stato deploy e link | Pages confermato, tutti gli URL apribili da desktop e telefono |
| P0 | Reale flusso di salvataggio | Prova A senza perdita file; JSON e immagine rintracciabili |
| P0 | Interoperabilità 3 Studi → Workspace | Tre file reali importati, stato revisione e provenienza conservati |
| P0 | QA su dispositivi mobili | Nessuna sezione bloccata o non raggiungibile con iPhone |
| P1 | Accessibilità | Corrette le barriere più gravi rilevate da test e audit |
| P1 | Chiarezza pedagogica | Docente principiante comprende brief, obiettivo e approvazione |
| P1 | Materiali esempio e guida breve | Prova A completabile con un modello di lezione guidato |
| P2 | Analisi del feedback | Registro delle criticità e decisioni motivate di correzione |
| P2 | Presentazione professionale | Case study e scheda del corso coerenti con caratteristiche verificate |
| P3 | API generative | Solo se utili: backend protetto, valutazione sicurezza, privacy, licenze e costi |
| P3 | Funzioni avanzate | Solo dopo riscontri utenti: progressi persistenti, esportazione pacchetto media, accesso istituzionale |

## Riferimenti normativi da contestualizzare
- MIM, *Linee guida per l'introduzione dell'Intelligenza Artificiale nelle Istituzioni scolastiche*, DM 166/2025: https://www.mim.gov.it/documents/20182/0/MIM_Linee%2Bguida%2BIA%2Bnella%2BScuola_09_08_2025-signed.pdf/b70fdc45-4b75-1f7e-73bf-eab12989b928
- Garante, provvedimento n. 787 del 20/10/2026, **parere sullo schema**, non decreto definitivo: https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/10315228
- Articolo 4 AI Act, alfabetizzazione IA: https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4

**Principio permanente:** il docente progetta, l'IA assiste, il docente verifica e decide.
