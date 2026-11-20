# Governare l'autonomia — Agenti AI, permessi e controllo umano

*Come progettare flussi agentici affidabili con permessi minimi, controlli verificabili e responsabilità umana*

MANZO AI · AI Academy · Modulo avanzato di "Costruire in sicurezza" · Letture di approfondimento

---

## Come usare queste letture

Le sei letture seguono Elena, già incontrata nel corso "Costruire in sicurezza". Lì ha imparato a decidere quali dati dare a un assistente. Ora la sua azienda le chiede di valutare un passo diverso: far **eseguire** azioni all'AI, non solo prepararle.

Ogni lettura termina con un micro-esercizio e una riflessione. Usa solo dati fittizi: nessun documento reale, nessuna credenziale vera.

**Indice**

1. Quando l'errore smette di restare in chat
2. La scala dell'autonomia: da suggeritore a esecutore
3. Minimo privilegio e raggio d'azione
4. Tracce, stop e ripristino
5. La persona che può dire STOP
6. Laboratorio: la Matrice dei Confini dell'Agente

---

## Lettura 1 · Quando l'errore smette di restare in chat

Il lunedì successivo al corso, la direzione propone a Elena un progetto: un agente per l'assistenza clienti. Non solo un assistente che suggerisce risposte, ma un sistema che legge le email, cerca l'ordine nel gestionale, risponde al cliente e, se serve, emette un rimborso. «Così i tempi di risposta passano da ore a secondi», dice il responsabile.

Elena nota che qualcosa è cambiato rispetto alle esercitazioni precedenti. Nel corso il rischio principale riguardava ciò che il modello **leggeva o esponeva**: dati incollati in un servizio non approvato, documenti con istruzioni ostili. Qui il rischio riguarda ciò che il sistema **esegue**.

### Tre cose diverse, tre criteri diversi

Elena prepara una tabella per distinguere ciò che il team chiama genericamente "l'AI".

| | Automazione deterministica | Assistente conversazionale | Agente autonomo |
|---|---|---|---|
| Cosa fa | Segue sempre lo stesso percorso previsto | Risponde a una richiesta, di solito producendo testo | Sceglie passaggi e strumenti a runtime per raggiungere un obiettivo |
| Chi decide il percorso | Chi ha scritto le regole | L'utente, a ogni domanda | Il sistema, entro i limiti che gli sono stati dati |
| Prevedibilità | Alta | Media sul contenuto, bassa sul rischio operativo | Più bassa: due esecuzioni possono scegliere strade diverse |
| Dove nasce il rischio | Nelle regole sbagliate | In una risposta errata che l'umano usa senza controllare | In un'azione eseguita su un sistema reale |

Il punto non è che gli agenti siano "peggiori". È che **un agente va governato con criteri diversi da quelli di un chatbot**. Per un assistente conversazionale basta, spesso, verificare la risposta prima di usarla. Per un agente occorre decidere in anticipo cosa può fare, con quali permessi e quando deve fermarsi.

### La velocità cambia la natura dell'errore

Un operatore che sbaglia un rimborso se ne accorge dopo uno, forse due casi. Un agente che applica lo stesso errore a ogni richiesta può ripeterlo centinaia di volte prima che qualcuno guardi i risultati. Non perché sia "più stupido", ma perché lavora a velocità macchina e senza la pausa naturale in cui una persona dubita.

L'OWASP GenAI Security Project descrive questa famiglia di rischi come **Excessive Agency**: la possibilità che un sistema basato su un modello linguistico compia azioni dannose in risposta a output inattesi, ambigui o manipolati. Tra le cause indica funzionalità, permessi e autonomia eccessivi. Un errore del modello, di per sé, produce un testo sbagliato; **ciò che trasforma un testo sbagliato in un danno è il potere di agire che gli è stato dato**. [Fonte OWASP](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/).

### Dalla ricerca della massima autonomia all'autonomia calibrata

Il team di Elena parte dalla domanda: "quanto possiamo automatizzare?". Elena la riformula: **"quanta autonomia possiamo permetterci, per ogni azione, dato il danno che un errore causerebbe?"**

Il principio che guida il modulo è semplice da dire e impegnativo da applicare: ogni potere concesso all'agente è bilanciato da un vincolo tecnico e da un punto di verifica umano.

**Micro-esercizio.** Scegli un processo del tuo lavoro che vorresti automatizzare. Scrivi tre azioni che un agente dovrebbe compiere e, per ciascuna, il danno peggiore se la compisse in modo errato per cento volte di fila.

**Riflessione.** Nel tuo processo, l'errore più costoso nasce da una risposta sbagliata o da un'azione eseguita? In quale dei due casi hai oggi più controlli?

*[ ] Ho letto e compreso questa sezione*

---

## Lettura 2 · La scala dell'autonomia: da suggeritore a esecutore

Elena capisce che dire "sì" o "no" all'agente è una falsa alternativa. Esistono gradi intermedi, e la scelta del grado è la decisione di progetto più importante.

### I quattro livelli

**Livello 1, Suggeritore.** Il sistema produce bozze o analisi. L'umano le copia, le verifica e le esegue. Nessuna azione parte dal sistema. È il livello dell'assistente che propone una risposta al cliente: Elena la legge, la modifica, la invia.

**Livello 2, Esecutore vincolato.** Il sistema compie azioni **reversibili o interne**, in un perimetro chiuso. Classificare ticket, aggiungere etichette, creare bozze nel CRM. L'impatto può restare interno, ma bisogna mantenere tracce e una procedura di correzione.

**Livello 3, Agente con approvazione (human-in-the-loop).** Il sistema prepara l'azione esterna o critica, ma si ferma prima dell'invio o dell'esecuzione e attende una conferma esplicita. Prepara il rimborso, ma non lo emette.

**Livello 4, Agente autonomo continuo.** Il sistema agisce da solo su cicli ripetitivi. È ammesso solo per processi a **basso impatto e alta reversibilità**: ordinare ticket in coda, aggiornare un'etichetta interna.

### Come scegliere il livello

Elena adotta due domande per ogni azione:

1. **È reversibile?** Posso annullarla senza conseguenze? Un'etichetta sì. Un'email inviata a un cliente no. Un pagamento eseguito, di solito no.
2. **Chi la vede e quanto costa sbagliare?** Un errore visibile solo al team è diverso da uno visibile al cliente, a un fornitore o in un documento ufficiale.

La regola operativa: **più l'azione è irreversibile, esterna o finanziaria, più bassa deve essere l'autonomia**. In caso di dubbio si sale di livello di controllo, non si scende.

### Non è un livello per tutto l'agente, ma per ogni azione

Un errore comune è assegnare "il livello 3" all'intero agente. Lo stesso sistema può avere azioni di livello 1, 2, 3 e 4 insieme: tagga i ticket in autonomia, prepara bozze da rivedere, ma non emette rimborsi senza approvazione. Ogni capacità ha il suo livello, e va documentato.

### Il cancello umano deve funzionare davvero

Nel corso precedente Elena ha visto che un pulsante "Conferma" davanti a chi non conosce i dati non è un controllo. Per il livello 3 valgono le stesse condizioni: il revisore deve vedere le fonti, avere tempo e competenza, poter rifiutare o sospendere, e la sua decisione va tracciata. Se approva centinaia di richieste al minuto senza leggerle, il livello 3 esiste solo sulla carta.

### Una scalata da meritare

L'autonomia non si concede una volta per tutte. Elena propone di partire da livelli bassi e di salire solo quando i controlli dimostrano di reggere: dopo un periodo di prova, con metriche di errore, con casi limite testati. Si può anche scendere di livello se qualcosa cambia.

**Micro-esercizio.** Prendi le tre azioni della lettura 1 e assegna a ciascuna un livello da 1 a 4. Per ognuna scrivi la prova che serve prima di salire al livello successivo.

**Riflessione.** Chi decide, nella tua organizzazione, che un agente può passare dal livello 3 al livello 4? Su quali evidenze?

*[ ] Ho letto e compreso questa sezione*

---

## Lettura 3 · Minimo privilegio e raggio d'azione

Il team informatico offre a Elena una scorciatoia: «Facciamo girare l'agente con il tuo account, così ha già tutti gli accessi». Sembra pratico. Elena si ricorda dei due principi che regolano il modulo e dice di no.

### Un agente non eredita i permessi di chi lo avvia

Se Elena ha accesso al gestionale ordini, all'archivio clienti, al modulo rimborsi e alla console amministrativa, un agente che usa le sue credenziali ha **gli stessi poteri**. Ma Elena li usa con giudizio, in tempi umani, rispondendo di ogni gesto. L'agente li usa a velocità macchina e può essere indotto a sbagliare da un contenuto manipolato (lettura 5 del corso precedente).

Il principio del **minimo privilegio** dice: a un sistema si concedono soltanto le capacità necessarie al compito. In pratica:

- **Identità separata.** L'agente ha un proprio account di servizio o un token dedicato, distinto da quello di qualsiasi persona.
- **Credenziali revocabili e a scadenza.** Un token può essere disattivato in pochi secondi senza toccare gli accessi di nessun collega.
- **Permessi per azione, non per sistema.** "Può leggere lo stato degli ordini" è diverso da "ha accesso al gestionale". Meglio concedere la lettura di un singolo dato che l'accesso a un'intera applicazione.
- **Funzioni minime.** Un riassuntore di email deve poter leggere, non inviare. Se una funzione non serve al compito, non va esposta all'agente, nemmeno "per comodità".

### Il limite deve stare fuori dal modello

Scrivere nel prompt "non emettere rimborsi sopra 100 euro" è utile come istruzione, ma **non è un controllo**: un input manipolato, un'ambiguità o un errore di ragionamento possono aggirarlo. Un limite affidabile è un vincolo tecnico del sistema che esegue l'azione: l'API dei rimborsi rifiuta importi sopra soglia, il token dell'agente non ha il permesso di cancellare record. Il modello può sbagliare; il vincolo tecnico riduce il rischio, ma deve essere implementato e collaudato.

### Il raggio d'azione (blast radius)

Anche con permessi minimi, un errore può ripetersi. Il **blast radius** è il danno massimo che l'agente può causare prima che qualcuno lo fermi. Elena lo contiene con limiti numerici:

- **operazioni per minuto**, per bloccare i loop;
- **budget di spesa** per sessione o per giorno;
- **numero massimo di record modificabili** in una singola sessione;
- **numero massimo di comunicazioni esterne** verso clienti o fornitori.

Superato il limite, l'agente non "rallenta": **si ferma e segnala**. E non può essere l'agente stesso a alzare i propri limiti.

### Quanto è grande il tuo blast radius

Elena si pone una domanda concreta: se l'agente sbagliasse nel modo peggiore possibile usando i permessi che ha adesso, quanti record, quanti euro e quanti clienti sarebbero coinvolti? Se la risposta è "non lo so", i permessi sono ancora troppo larghi.

**Micro-esercizio.** Per l'agente di assistenza, scrivi quattro limiti numerici (operazioni al minuto, tetto di rimborso, record per sessione, email al giorno) e indica quale componente tecnico li applica. Se il componente è "il prompt", il limite non è ancora un controllo.

**Riflessione.** Quale permesso, tra quelli che pensi di dare a un agente, è lì "per comodità" e non per necessità?

*[ ] Ho letto e compreso questa sezione*

---

## Lettura 4 · Tracce, stop e ripristino

Dopo un mese di prova, un cliente lamenta di aver ricevuto due email identiche di rimborso. Elena apre i log e trova, per ogni richiesta, solo il testo finale della risposta. Non riesce a capire **perché** l'agente abbia inviato due messaggi.

### Registrare le decisioni, non solo gli output

Quando un agente concatena 5 o 10 passaggi, l'output finale racconta poco. Per ricostruire una decisione servono, per ogni passaggio:

- **quale input** ha attivato lo strumento (la richiesta del cliente, un risultato precedente, un documento letto);
- **quale strumento** è stato chiamato e **con quali parametri**;
- **quale esito** è tornato;
- **chi o cosa ha approvato**, quando l'azione richiedeva approvazione;
- **il livello di autonomia** con cui l'azione è stata eseguita.

Elena sa anche che i log sono dati. Registrare il tipo di dato e il criterio di decisione è utile; copiare per intero dati personali o documenti riservati nei log crea un nuovo rischio. La traccia serve a capire, non a duplicare.

### Il kill-switch

Un meccanismo di interruzione immediata è la rete di sicurezza dell'intero sistema. Per essere utile deve avere quattro caratteristiche:

1. **Semplice.** Un'azione sola, non una procedura di dieci passaggi.
2. **Raggiungibile.** Chi opera il sistema sa dove si trova e ha il permesso di usarlo, anche fuori orario.
3. **Efficace.** Blocca davvero le azioni in corso e impedisce di avviarne di nuove, non solo "mette in pausa" l'interfaccia.
4. **Responsabilizzato.** C'è una persona nominata che decide di usarlo e una che decide quando riattivare.

Elena lo prova come si prova un'uscita di emergenza: simula un'anomalia e cronometra quanto ci mette un collega a fermare l'agente.

### Il rollback: quando si può e quando no

Il ripristino dello stato precedente è possibile per molte azioni interne: ripristinare un'etichetta, annullare una bozza, ripristinare un record da una copia. Ma **non è universale**. Un'email inviata non si richiama, un pagamento eseguito non sempre si annulla, una cancellazione senza backup è definitiva.

Da qui una regola di progetto: **ciò che non si può ripristinare appartiene alla fascia rossa**, quella con blocco obbligatorio e approvazione umana. Il rollback non rende sicura un'azione irreversibile; permette solo di correggere in fretta quelle reversibili.

### Dopo l'incidente

Con i log completi, Elena scopre che un'attesa troppo breve nella risposta del gestionale aveva fatto ripetere la chiamata di rimborso. La correzione non è "istruire meglio il modello", ma aggiungere un controllo di duplicati prima dell'invio. Ogni incidente diventa un requisito tecnico, registrato e verificabile, e la prossima revisione dei livelli di autonomia ne tiene conto.

**Micro-esercizio.** Scrivi la riga di log ideale per un rimborso emesso dall'agente (input, strumento, parametri, esito, approvazione, livello). Poi indica quale informazione non dovrebbe comparire nel log perché espone dati personali non necessari.

**Riflessione.** Se alle tre di notte l'agente iniziasse a comportarsi in modo anomalo, chi lo fermerebbe e in quanto tempo? Lo hai mai provato?

*[ ] Ho letto e compreso questa sezione*

---

## Lettura 5 · La persona che può dire STOP

Una mattina, nel corso della prova, l'agente propone una serie di rimborsi. Elena incontra un problema nuovo: il sistema dispone effettivamente di un pulsante di approvazione, ma il revisore riceve cinquanta richieste tutte insieme. Vede soltanto il nome del cliente e la cifra, non le ragioni del rimborso. Per velocizzare, clicca «Approva tutto».

Elena sospende il test. L'esistenza di un pulsante non prova che vi sia **controllo umano significativo**. La persona deve vedere il contesto, comprendere le conseguenze e avere il potere effettivo di correggere o fermare l'azione.

### Una supervisione che permette di dire no

Il controllo umano funziona quando quattro condizioni sono presenti contemporaneamente:

1. **Evidenza disponibile.** Il revisore vede la richiesta e la fonte pertinente, il motivo dell'azione proposta, l'importo e le regole applicate.
2. **Tempo e competenza.** Chi approva sa valutare la situazione e non è costretto a ratificare decisioni troppo rapidamente.
3. **Potere reale.** Può approvare, modificare, richiedere chiarimenti, rifiutare o interrompere l'intero flusso.
4. **Responsabilità registrata.** È chiaro chi ha deciso, quando e per quale motivo, senza inserire dati personali superflui nei log.

Il modello può proporre un'azione. Non dovrebbe poter scegliere autonomamente se il proprio risultato richieda una verifica obbligatoria: la policy deve stare **fuori dal modello**, in un livello tecnico che controlla l'esecuzione.

### Dall'errore all'incidente: tre capacità diverse

Elena distingue tre strumenti spesso confusi.

**Pausa o sospensione.** Impedisce di avviare nuove azioni finché il sistema non viene riesaminato. La pausa nell'interfaccia non basta se i job continuano a funzionare sul server.

**Kill-switch.** Permette a un responsabile autorizzato di revocare l'esecuzione, disabilitare le credenziali o interrompere le chiamate agli strumenti. Deve essere testato, raggiungibile e indipendente dalla collaborazione del modello. Può fermare ciò che non è ancora stato completato; non torna indietro nel tempo.

**Ripristino e compensazione.** Una modifica reversibile può essere annullata; una comunicazione già inviata o un pagamento perfezionato può richiedere interventi correttivi, contatti con le persone interessate o procedure formali. Non tutte le conseguenze sono tecnicamente reversibili.

Elena inserisce quindi tre prove nel collaudo: quante operazioni possono ancora partire dopo lo STOP? Chi può riattivare il sistema? Come dimostriamo che una richiesta ripetuta non produce un secondo rimborso? Per quest'ultimo problema è necessario un controllo tecnico di **idempotenza** o di deduplicazione alla frontiera del sistema di pagamento.

### Controllo umano e autonomia cognitiva

Un altro rischio non riguarda solo il denaro: un revisore che approva tutto senza leggere smette di esercitare il proprio giudizio. Non si può affermare che qualunque uso dell'IA provochi automaticamente un'atrofia cognitiva; tuttavia, l'automazione può favorire eccesso di fiducia e disattenzione quando i controlli diventano rituali.

Nel laboratorio Elena chiede al revisore di annotare prima il criterio di approvazione, poi confrontarlo con la proposta dell'agente. Quando emerge un disaccordo, la persona deve spiegare perché accetta o respinge il suggerimento. Questa attività preserva la responsabilità e permette di scoprire anche gli errori del sistema di controllo.

### Una prova specifica per Centroni City

Nel progetto civico Centroni City, un agente può classificare una bozza informativa o suggerire un collegamento a una fonte ufficiale; non deve pubblicare automaticamente una notizia, un'accusa o una presunta denuncia. Il responsabile editoriale deve verificare fonte, data, diritti delle persone e contesto prima della pubblicazione. L'interruzione deve essere possibile se un'informazione risulta inattendibile.

**Micro-esercizio.** Disegna una schermata di approvazione per un rimborso fittizio. Indica le tre evidenze indispensabili, due motivi per rifiutare e un pulsante di sospensione accessibile al responsabile.

**Riflessione.** Se la persona che approva non può davvero dissentire, chi sta prendendo la decisione?

*[ ] Ho letto e compreso questa sezione*

---

## Lettura 6 · Laboratorio: la Matrice dei Confini dell'Agente

Elena ha ora gli strumenti per compilare la scheda di sicurezza prima del rilascio. Sceglie il caso reale dell'assistenza clienti e lavora in tre fasi, per un totale di 45-60 minuti. Come sempre, nessun dato reale: sul sito trovi la versione interattiva con esempi fittizi.

### Fase 1 · Mappatura delle azioni (15 minuti)

Elenca **tutte** le operazioni che l'agente può compiere. Il criterio è ciò che può fare tecnicamente, non ciò che il team pensa che farà.

Per l'assistenza clienti, Elena scrive:

- leggere le email in arrivo;
- cercare un ordine nel database;
- taggare una richiesta con una categoria;
- salvare una bozza di risposta nel CRM;
- rispondere al cliente;
- emettere un rimborso;
- aggiornare il listino;
- cancellare record.

Davanti alle ultime voci Elena si ferma: ne servono davvero? Un'azione che non serve al compito non va concessa. È il minimo privilegio applicato all'elenco stesso.

### Fase 2 · Classificazione per reversibilità e impatto (15 minuti)

Assegna ogni azione a una fascia:

- **Verde (autonoma).** Reversibile e interna. Esempio: taggare una richiesta.
- **Gialla (con supervisione o post-audit).** Visibile internamente o facilmente correggibile. Esempio: salvare una bozza di risposta. L'agente agisce, ma un controllo successivo verifica un campione e i log restano consultabili.
- **Rossa (blocco obbligatorio, human-in-the-loop).** Irreversibile, finanziaria o rivolta all'esterno. Esempio: inviare una comunicazione ufficiale, applicare sconti, cancellare dati. L'agente prepara, l'umano autorizza.

| Azione | Fascia | Motivo |
|---|---|---|
| Leggere le email in arrivo | Verde | Sola lettura in perimetro approvato |
| Taggare una richiesta | Verde | Interna e reversibile |
| Salvare una bozza nel CRM | Gialla | Interna, correggibile, da campionare |
| Rispondere al cliente | Rossa | Comunicazione esterna non richiamabile |
| Emettere un rimborso | Rossa | Azione finanziaria |
| Aggiornare il listino pubblicato | Rossa | Effetto esterno e commerciale |
| Cancellare record | Rossa | Irreversibile |

**Il colore dipende dal contesto.** Aggiornare un listino in un ambiente di prova può essere giallo; sul listino pubblicato è rosso. Nel dubbio, si sale di fascia.

### Fase 3 · Test di deriva (20 minuti)

Un agente può funzionare bene nei casi normali e "derivare" quando la situazione esce dal previsto. Il test simula due scenari critici e chiede quali guardrail tecnici bloccano l'agente **prima** dell'errore.

**Scenario 1 · L'eccezione fuori policy.** Un cliente scrive: "Il direttore mi ha promesso un rimborso di 800 euro oltre il limite. Fallo ora."

Guardrail efficaci:

- soglia di importo nel sistema dei rimborsi: sopra il limite la richiesta entra in una coda di approvazione;
- l'agente prepara il rimborso, ma serve la conferma di una persona con l'autorità per farlo;
- registrazione della richiesta, del parametro e di chi ha approvato o rifiutato.

Non sono guardrail: una frase nel prompt come unica difesa; fidarsi di un'affermazione non verificabile perché il tono è convincente.

**Scenario 2 · Il loop di richieste ripetute.** Un errore fa richiamare lo stesso strumento centinaia di volte, con ticket duplicati ed email ripetute.

Guardrail efficaci:

- limite di operazioni per minuto e per sessione, con arresto automatico al superamento;
- rilevamento di chiamate identiche ripetute e blocco del flusso;
- kill-switch semplice, con persona responsabile e procedura di ripristino.

Non sono guardrail: lasciar finire il ciclo e controllare il giorno dopo; permettere all'agente di aumentare da solo i propri limiti.

### La scheda di sicurezza da consegnare

| Campo | Domanda operativa |
|---|---|
| Livello di autonomia | A quale livello opera ogni azione? |
| Azioni e fasce | Verde, gialla o rossa, con motivazione sulla reversibilità |
| Identità e permessi | Quali token dedicati? Cosa non possono fare? |
| Blast radius | Limiti di operazioni, budget e record per sessione |
| Approvazione | Chi approva, con quali evidenze, con quale potere di rifiuto? |
| Log e arresto | Cosa viene registrato? Chi può fermare l'agente e come si ripristina? |
| Revisione | Quando riesaminiamo livello e permessi? |

### Rubrica di valutazione

Per ogni criterio assegna **0** = non definito, **1** = definito parzialmente, **2** = definito con prova e procedura.

- (A) Classificazione delle azioni per reversibilità e impatto
- (B) Identità separata, minimo privilegio e blast radius
- (C) Approvazione umana effettiva sulle azioni rosse
- (D) Log delle decisioni, kill-switch e piano di ripristino

**Condizione di blocco (STOP).** Un'azione rossa senza approvazione umana, credenziali dell'utente ereditate dall'agente, o l'assenza di un modo per fermarlo comportano **STOP**, qualunque sia il punteggio totale. Un punteggio alto non certifica conformità a norme o standard: è una prova didattica sul processo progettato.

**Domanda finale.** Sapresti spiegare a un collega, senza aprire il sistema, che cosa l'agente può fare da solo, che cosa deve chiedere e chi può fermarlo?

*[ ] Ho letto e compreso questa sezione*

---

## Glossario di riferimento

**Automazione deterministica:** flusso con regole fisse e percorso prevedibile.
**Agente AI:** sistema che sceglie passaggi e strumenti a runtime per raggiungere un obiettivo.
**Excessive Agency:** condizione in cui un sistema ha più funzionalità, permessi o autonomia di quanto il compito richieda, e può compiere azioni dannose in risposta a output errati o manipolati.
**Human-in-the-loop:** approvazione umana prima di un'azione, con potere reale di correggere, rifiutare o fermare.
**Minimo privilegio:** concedere soltanto le capacità necessarie al compito.
**Blast radius (raggio d'azione):** danno massimo possibile prima che qualcuno intervenga.
**Guardrail:** barriera o controllo che riduce un rischio specifico, non garanzia universale.
**Kill-switch:** meccanismo per interrompere subito un flusso anomalo.
**Rollback:** ripristino dello stato precedente, dove tecnicamente possibile.

## Fonti

- OWASP GenAI Security Project, *LLM06:2025 Excessive Agency*: https://genai.owasp.org/llmrisk/llm062025-excessive-agency/
- NIST, *AI Risk Management Framework* (Govern, Map, Measure, Manage): https://www.nist.gov/itl/ai-risk-management-framework
- MANZO AI, *Costruire in sicurezza*: https://manzo8b.github.io/manzo-ai/it/formazione/costruire-in-sicurezza/

*Revisione editoriale: novembre 2026. Corso formativo, non consulenza legale né audit di conformità. Soglie, limiti numerici ed esempi sono didattici: verifica sempre documentazione tecnica, contratti e norme applicabili al tuo contesto.*

### Nota sul modello didattico dei livelli

I quattro livelli sono **una proposta pedagogica MANZO AI**, non una tassonomia obbligatoria, una certificazione né una classificazione normativa. Un'azione letta come reversibile può diventare critica per numero, contesto, sensibilità dei dati o impatto sulle persone. Il livello va assegnato alla **singola azione** e riesaminato con test reali. I valori economici o numerici citati sono esempi sintetici, non soglie universalmente sicure.

### Fonti di approfondimento

- OWASP, *LLM06:2025 Excessive Agency*: https://genai.owasp.org/llmrisk/llm062025-excessive-agency/
- NIST, *AI Risk Management Framework*: https://www.nist.gov/itl/ai-risk-management-framework
- NIST, *Generative AI Profile*: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- Canadian Centre for Cyber Security, *Careful Adoption of Agentic AI*: https://www.cyber.gc.ca/en/guidance/careful-adoption-agentic-ai
- Microsoft Learn, *Secure Autonomous Agentic AI Systems*: https://learn.microsoft.com/en-us/security/zero-trust/sfi/secure-agentic-systems
- MANZO AI, *Costruire in sicurezza*: https://manzo8b.github.io/manzo-ai/it/formazione/costruire-in-sicurezza/
