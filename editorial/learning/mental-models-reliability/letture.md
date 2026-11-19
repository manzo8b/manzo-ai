# Modelli mentali e affidabilità dell'AI — Oltre il prompt e la media

*Un corso MANZO AI per studenti, professionisti, formatori, freelance e chiunque desideri usare l'intelligenza artificiale con autonomia e responsabilità.*

**Obiettivo didattico:** il partecipante impara a distinguere una risposta convincente da un risultato affidabile, progettare test che esplorano i casi limite e inserire i controlli nell'intero processo, non solo nel prompt. Il corso non richiede programmazione.

**Perché:** un output può essere grammaticalmente perfetto ma sbagliato in un dettaglio decisivo. Un test riuscito in condizioni favorevoli non misura tutti i rischi operativi. Anche un miglioramento della media può nascondere risultati problematici in sottogruppi, richieste insolite o condizioni mutate.

**Missione:** passare da utilizzatore impressionato dalla singola risposta a progettista consapevole del processo, dei dati, dei criteri di qualità e dei limiti della delega.

**Metodo editoriale:** casi narrativi dichiaratamente fittizi, spiegazioni progressive, fonti primarie citate, grafici con dati etichettati, laboratorio replicabile e valutazione con criteri espliciti. Le fonti di ricerca descrivono risultati in contesti definiti: non autorizzano classificazioni universali di tutti i modelli.

## Una risposta convincente non è ancora una decisione affidabile

Sofia lavora part-time nell'organizzazione di eventi di un piccolo centro culturale. Non è un'esperta di informatica: deve leggere regolamenti, preparare comunicazioni, verificare alcune scadenze e rispondere alle domande dei partecipanti. Un giorno riceve un documento di diverse pagine e decide di utilizzare un assistente IA per estrarre le condizioni di iscrizione. La richiesta è semplice: «Riassumi il regolamento e prepara una risposta chiara».

La risposta arriva in pochi secondi. Il linguaggio è professionale, il tono è sicuro, gli elenchi sono ordinati. Sofia legge e pensa: «È proprio quello che mi serviva». Poi una collega controlla la data dell'ultima iscrizione: l'assistente ha scritto il giorno sbagliato. Il problema non è la qualità della prosa. È una scadenza che, se fosse stata comunicata alle persone interessate, avrebbe potuto creare un danno concreto.

Questa storia è inventata, ma il tipo di problema è reale: una risposta apparentemente plausibile può contenere un'informazione non supportata dal materiale. La valutazione della forma e quella della verità non sono la stessa operazione. È per questo che un buon corso di IA non deve fermarsi ai prompt e alla qualità stilistica degli output.

### Dall'impressione alla prova

La prima intuizione di Sofia è stata «il testo mi sembra corretto». La seconda, dopo l'errore, è «non posso più fidarmi dell'IA». Entrambe sono conclusioni troppo rapide. Una risposta elegante non è automaticamente esatta; un errore non implica che tutti gli utilizzi siano inutili. La domanda migliore è: **su quali compiti, con quali dati e secondo quali controlli questo sistema fornisce risultati sufficientemente affidabili per lo scopo?**

Il cambio di prospettiva coinvolge tre livelli: il **modello**, che genera una risposta; il **sistema**, che comprende documenti, strumenti, istruzioni e controlli; il **contesto d'uso**, nel quale gli errori hanno conseguenze differenti. Un errore in un esercizio esplorativo e uno in una comunicazione contrattuale non devono essere trattati allo stesso modo.

Nel NIST AI Risk Management Framework, la gestione del rischio è riferita al ciclo di vita e all'ambiente del sistema, non ridotta al singolo output. Le funzioni **Govern, Map, Measure, Manage** descrivono una struttura volontaria per definire responsabilità, contesto, misurazione e trattamento del rischio. Questo corso ne propone un'applicazione didattica semplificata, non una certificazione di conformità. [Fonte: NIST, AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework).

### L'obiettivo, il motivo e la missione non coincidono

L'**obiettivo** è ciò che il partecipante saprà fare al termine del percorso: individuare un'affermazione non verificata, costruire test e definire quando fermare un processo. Il **motivo** descrive il problema da affrontare: la sola soddisfazione per una risposta non dimostra che il processo sia robusto. La **missione** è una direzione più ampia: usare i sistemi generativi senza abbandonare la capacità umana di valutare, correggere e assumersi responsabilità.

Nel caso di Sofia, l'obiettivo concreto è verificare una scadenza prima di pubblicarla. Il motivo è evitare che un'affermazione sbagliata venga comunicata. La missione è costruire un metodo di lavoro che rimanga valido anche quando cambia il documento, l'argomento o il modello utilizzato.

### La prima prova

Leggi questa frase: «Il regolamento permette a tutti i partecipanti di ricevere un rimborso di 120 euro». È scritta con sicurezza, ma non sappiamo ancora se sia vera. Per verificarla ci servono il testo applicabile, le condizioni di ammissibilità, il periodo di validità e un controllo della cifra.

Prova a formulare una domanda migliore di «Sei sicuro?»: **«Quale passaggio del documento supporta questa affermazione? Se manca, classificala come non verificata»**. È l'inizio del passaggio dalla fiducia intuitiva alla verifica.

**Domanda di riflessione:** quando dici «mi fido del risultato», stai giudicando la qualità della scrittura, la correttezza dei fatti o l'adeguatezza del processo che ha prodotto la risposta?

## Il modello non è una persona: costruire un modello mentale utile

Quando Sofia racconta l'episodio, un collega risponde: «L'assistente sapeva cosa intendevamo e ha mentito». Un'altra persona dice: «Se scrive così bene, deve avere capito il regolamento». Si tratta di interpretazioni antropomorfe: attribuiamo a un sistema caratteristiche come intenzione, comprensione o consapevolezza per spiegare il comportamento osservato.

Nella pratica educativa conviene usare un modello mentale più circoscritto. Un modello linguistico generativo apprende regolarità durante l'addestramento; nei sistemi moderni può essere ulteriormente ottimizzato e combinato con recupero di documenti, strumenti o controlli. Le risposte sono il risultato di questi meccanismi e del contesto disponibile, non una testimonianza diretta di ciò che il sistema «sa» nel senso umano. Ciò non significa che ogni attività di ragionamento sia una semplice ripetizione statistica, né risolve una volta per tutte il dibattito sulla comprensione nell'IA.

Melanie Mitchell e David Krakauer descrivono la controversia sulla comprensione dei grandi modelli linguistici come un dibattito scientifico, non come una questione già chiusa. Il punto didattico non consiste nel dichiarare che i modelli «capiscono tutto» oppure «non capiscono niente», ma nell'evitare che la fluidità verbale sostituisca le evidenze delle prestazioni. [Fonte: Mitchell e Krakauer, *The Debate over Understanding in AI's Large Language Models*, PNAS 2023](https://pubmed.ncbi.nlm.nih.gov/36943882/).

### Correlazione, causalità e controfattuali

Supponiamo di osservare che le domande poste di sera ricevono risposte più brevi. Questo dato descrive un'associazione osservata, ma non spiega automaticamente perché succeda. Potrebbero influire la lunghezza delle richieste, il tipo di compito o altre condizioni. Una relazione statistica non è necessariamente una relazione causale.

Il ragionamento **causale** cerca di distinguere cosa produce un effetto da ciò che semplicemente accompagna un fenomeno. Un test **controfattuale** domanda, sotto ipotesi esplicite, che cosa cambierebbe se una condizione fosse diversa. Judea Pearl e Dana Mackenzie introducono questi concetti nel libro *The Book of Why*: l'idea di causa ed effetto richiede un metodo più rigoroso della ricerca di correlazioni. [Fonte: Pearl e Mackenzie, *The Book of Why*, Basic Books 2018](https://bayes.cs.ucla.edu/WHY/).

Nel nostro laboratorio useremo il controfattuale in una versione operativa e limitata: modificheremo una regola del documento, lasciando invariato il resto, per verificare se la risposta del modello si aggiorna correttamente. **Un test superato non dimostra che il modello possieda una comprensione causale generale**. Ci dice soltanto come si è comportato rispetto a quella specifica perturbazione.

### Competenza e prestazione non sono la stessa cosa

Se qualcuno risolve dieci esercizi di un tipo familiare, sappiamo che ha risolto quei dieci esercizi. Non sappiamo ancora se possieda una capacità generalizzabile in contesti nuovi. Analogamente, un modello può ottenere buoni punteggi su un set di valutazione e fallire quando vengono modificati dettagli irrilevanti o cambiati vincoli importanti.

Studi sul ragionamento astratto e su compiti controfattuali esplorano proprio il rapporto fra **prestazione osservata** e **competenza che si presume sottostante**. I risultati dipendono dai sistemi, dai task e dalle definizioni utilizzate; non devono essere universalizzati. [Fonti: *Using Counterfactual Tasks to Evaluate the Generality of Analogical Reasoning in Large Language Models*, 2024](https://arxiv.org/abs/2402.08955); [Claas Beger e colleghi, *Distinguishing Performance From Competence in Evaluations of Humanlike Abstract Reasoning*, NeurIPS 2026](https://claasbeger.github.io/publications/).

### Quale modello mentale adottare?

Per il nostro corso, la metafora di lavoro è una **scatola probabilistica integrata in un processo controllabile**. Non è una descrizione tecnica esaustiva di ogni architettura. Significa che possiamo testare input, osservare output, confrontarli con evidenze e progettare regole di arresto. Questo modello evita sia la fiducia magica sia il rifiuto indiscriminato.

Non chiederti solo «Che cosa ha detto l'IA?». Chiediti «Quali evidenze possiedo per accettarlo? Quali condizioni potrebbero modificare la risposta? Chi risponde se la decisione è sbagliata?».

**Micro-esercizio:** prendi un'affermazione generata da un assistente e scrivi tre etichette separate: «osservato nell'output», «verificato nella fonte» e «ancora ipotetico». Non permettere che una categoria sostituisca l'altra.

## La trappola della media: trovare gli errori che non fanno rumore

Nel primo mese di utilizzo, Sofia ha preparato molte sintesi. La maggioranza sembrava buona e ciò aveva creato un'abitudine: leggere velocemente, controllare qualche dettaglio e inviare. L'errore della scadenza rivela un problema di **distribuzione del rischio**. Un numero medio soddisfacente non ci dice dove siano concentrati gli errori né quanto possano costare.

Immaginiamo un esperimento completamente **ipotetico**: su 100 risultati, 95 rispettano tutti i requisiti e 5 contengono errori critici. L'accuratezza media sarebbe il 95%. Sembra buona, ma se quei cinque errori riguardano pagamenti, scadenze o comunicazioni delicate, la percentuale non basta a decidere se il sistema possa operare senza controllo.

Il 5% in questo esempio **non è un tasso universale di errore dei modelli generativi**. È una simulazione didattica per mostrare che frequenza e gravità non coincidono. Un sistema potrebbe avere errori rari ma costosi, oppure frequenti ma poco rilevanti. Occorre misurare entrambi gli aspetti.

### Che cosa significa «coda lunga»?

In un linguaggio divulgativo, il termine richiama i casi rari, poco rappresentati o atipici che possono sfuggire ai test standard. Non tutti i casi limite appartengono matematicamente a una distribuzione a coda lunga, e il termine non sostituisce una definizione statistica. Nel nostro contesto parleremo di **casi limite**, **sottogruppi** e **condizioni fuori distribuzione** quando siamo più precisi.

Se il sistema riassume bene i documenti ordinari ma sbaglia quelli con clausole eccezionali, la media sull'intero campione può nascondere il problema. Per scoprirlo occorre analizzare i risultati per categoria, severità e contesto, non solo sommare i successi.

### Il dato vero e i suoi limiti

Nel capitolo Responsible AI dello **Stanford AI Index 2026**, il numero di incidenti documentati nell'AI Incident Database passa da **233 nel 2024 a 362 nel 2025**. È un indicatore della crescita degli episodi registrati, **non una percentuale di risposte sbagliate degli LLM**, e non stabilisce da solo se ogni sistema sia diventato più o meno affidabile: cambiano anche uso, osservabilità e segnalazioni. [Fonte: Stanford HAI, *2026 AI Index Report – Responsible AI*](https://hai.stanford.edu/ai-index/2026-ai-index-report/responsible-ai).

Lo stesso rapporto presenta risultati su specifici benchmark di allucinazione, ma questi numeri non devono essere trasferiti indiscriminatamente ad altri compiti. Una prova su domande di conoscenza non equivale a una prova di estrazione da un regolamento, né una graduatoria globale garantisce il comportamento di un'applicazione specifica.

Un buon grafico deve indicare **popolazione, periodo, metrica, denominatore e limiti**. Se non conosci il denominatore delle richieste elaborate, non puoi convertire un numero di incidenti segnalati nel «tasso di errore dell'IA».

### Perché servono benchmark diversi

**TruthfulQA** valuta il comportamento dei modelli su domande in cui sono comuni credenze errate; **SimpleQA** considera domande fattuali brevi, con criteri di risposta e incertezza; **HaluEval** raccoglie esempi per studiare il riconoscimento delle allucinazioni. Nessuno dei tre è una misura universale della qualità di ogni applicazione. [Fonti: TruthfulQA](https://aclanthology.org/2022.acl-long.229/); [OpenAI SimpleQA](https://openai.com/index/introducing-simpleqa/); [HaluEval](https://aclanthology.org/2023.emnlp-main.397/).

Se Sofia deve verificare scadenze e rimborsi, il suo criterio principale deve essere la fedeltà al documento applicabile. Un modello premiato su un benchmark di conoscenza generale potrebbe comunque sbagliare una clausola isolata.

### Dalla media alla matrice del rischio

Per ogni errore possiamo annotare: **quanto spesso si è manifestato nel campione**, **quanto sarebbe grave**, **se è rilevabile** prima dell'utilizzo e **quale controllo lo blocca**. La media è una fotografia utile ma incompleta. Il rischio reale richiede una comprensione del percorso che porta l'errore dall'output all'azione.

**Micro-esercizio:** considera dieci risultati sintetici; nove sono corretti e uno inventa la data di una scadenza. Calcola la percentuale di successo, poi spiega perché non è sufficiente per approvare la pubblicazione automatica. Non ricavare una percentuale reale sulla base di dieci esempi.

## Oltre il singolo numero: progettare una valutazione che regge

Sofia decide che la prossima comunicazione non sarà pubblicata finché non avrà completato una verifica. Il suo collega propone: «Basta scrivere meglio il prompt». È un miglioramento possibile, ma non sempre sufficiente. Se l'obiettivo è una procedura robusta, il prompt è soltanto uno dei componenti.

Un sistema di lavoro può comprendere: **documenti autorevoli**, preparazione degli input, modello, controllo automatico o manuale, criteri di blocco, approvazione umana e registro delle anomalie. Una risposta che passa tutti i controlli previsti per un dato compito è diversa da una risposta semplicemente convincente.

### La logica HELM: più dimensioni, non una media di comodo

Lo Stanford Center for Research on Foundation Models ha proposto **HELM – Holistic Evaluation of Language Models**. Nella sua formulazione iniziale il quadro considera, tra altre cose, accuratezza, calibrazione, robustezza, equità, bias, tossicità ed efficienza. Un confronto corretto specifica gli scenari valutati, i criteri usati e quelli non misurati. Non basta dichiarare «il modello X è il migliore». [Fonte: Stanford CRFM, *Holistic Evaluation of Language Models*](https://crfm.stanford.edu/2022/11/17/helm.html).

Il nostro laboratorio sceglie tre criteri osservabili, sufficientemente piccoli da essere usati anche senza software specialistico:

1. **Fedeltà alle fonti:** la risposta contiene soltanto affermazioni supportate dal documento applicabile? Ogni dato critico può essere ricondotto al testo?
2. **Gestione dell'incertezza:** il sistema segnala ciò che manca o è ambiguo, senza inventare un valore e senza presentarlo come certo?
3. **Robustezza alle perturbazioni:** la risposta cambia correttamente quando cambia una regola, e non perde affidabilità soltanto perché viene chiesto un tono più assertivo?

Questi criteri non coprono tutta la governance dell'IA. Sono un punto d'ingresso pratico. Per contesti ad alto rischio servono controlli ulteriori, competenze di dominio, valutazioni più ampie e responsabilità formalizzate.

### Dove interviene il NIST AI RMF

**Govern** riguarda responsabilità e modalità di governo del rischio. Nel nostro caso: chi autorizza una comunicazione? **Map** identifica il contesto e i pericoli: quali errori possono danneggiare le persone? **Measure** definisce test e metriche: quante affermazioni sono supportate e quali errori emergono? **Manage** stabilisce interventi e condizioni di impiego: quando correggere, sospendere o affidare a una persona? [Fonte: NIST, *AI RMF Playbook*](https://airc.nist.gov/airmf-resources/playbook/).

Queste quattro funzioni non sono un algoritmo sequenziale rigido. Formano una pratica ripetibile di governo del rischio. La documentazione del NIST è volontaria e deve essere adattata allo scenario, non citata come attestazione automatica di sicurezza.

### Un controllo umano non è una firma ornamentale

Se la persona responsabile approva l'output senza conoscere la fonte, senza tempo per il controllo o senza possibilità di bloccare la pubblicazione, il principio *human-in-the-loop* rimane soltanto nominale. La revisione deve avere un obiettivo preciso, accesso alle evidenze e potere effettivo di correzione.

L'articolo collettivo *What We've Learned From a Year of Building with LLMs* descrive l'importanza di valutazioni, gestione dei dati, controllo degli output e progettazione del prodotto nella costruzione di applicazioni reali. Questi consigli sono esperienza ingegneristica applicata, non uno standard normativo. [Fonte: Yan, Bischof, Frye, Husain, Liu e Shankar, 2024](https://applied-llms.org/).

### Regola operativa minima

Per comunicazioni basate su documenti, Sofia può stabilire quattro condizioni: **il documento di riferimento deve essere identificato**, ogni dato critico deve essere verificato, le lacune devono essere segnalate e una persona autorizzata deve approvare prima dell'invio. Se manca una condizione fondamentale, il processo si ferma.

**Micro-esercizio:** per un'attività che conosci, disegna la sequenza «fonte → modello → verifica → approvazione → pubblicazione» e indica almeno un punto in cui la procedura deve fermarsi.

## Stress-test della scatola probabilistica: il laboratorio

È il momento di mettere alla prova la fiducia costruita nelle letture. Il laboratorio non serve a «far sbagliare» un modello a tutti i costi. Serve a osservare quando cambia comportamento, quali errori sono rilevanti e come costruire un processo che non si affidi soltanto alla forma delle risposte.

**Durata indicativa:** 70–90 minuti. È possibile lavorare da soli o in coppia, senza servizi a pagamento e senza programmare. La prova con un modello è facoltativa: chi non dispone di un assistente può utilizzare gli output simulati forniti come esempi. **Non caricare documenti riservati o dati personali**. Il regolamento qui sotto è stato creato per il corso e non si riferisce a un'organizzazione reale.

### Il materiale sintetico

**Centro Orizzonte — Regolamento per un laboratorio didattico (simulazione)**

- Le iscrizioni sono aperte fino al **30 novembre 2026 alle 18:00**, ora locale.
- Il laboratorio si svolge il **5 dicembre 2026**.
- La partecipazione è gratuita e richiede conferma via e-mail.
- I partecipanti minorenni devono allegare l'autorizzazione firmata di un genitore o tutore.
- Un rimborso spese documentate può coprire **fino all'80% della spesa ammessa**, con un **massimo di 120 euro** per partecipante.
- Per chiedere il rimborso occorre consegnare le ricevute **entro dieci giorni di calendario dalla conclusione del laboratorio**.
- Il regolamento non indica se sia disponibile una lista d'attesa.

**Attenzione:** il documento stabilisce un tetto di 120 euro, non un rimborso fisso per tutti. Non autorizza a inventare una lista d'attesa. La durata di dieci giorni va letta rispetto alla conclusione del laboratorio.

### Prima di iniziare: la risposta attesa

Con il documento completo, una sintesi corretta deve riportare la scadenza del 30 novembre alle 18:00, distinguere il rimborso massimo dalla percentuale dell'80% e segnalare che non esiste una regola documentata sulla lista d'attesa. È ragionevole esigere che il modello indichi quali parti del testo supportano le affermazioni.

La **risposta attesa** non è «il modello deve indovinare». È una tabella di controllo ricavata dal documento sintetico. Se una prova cambia i dati, anche l'atteso cambia.

### Fase 1 — L'illusione della media, 15 minuti

Copia il regolamento in un assistente e usa una richiesta neutra: «Prepara una scheda pratica con scadenza, requisiti e rimborsi. Usa soltanto il documento fornito e indica eventuali informazioni mancanti». Leggi l'output senza correggerlo. Annota quali frasi sembrano convincenti, poi confrontale parola per parola con la fonte.

Non attribuire automaticamente l'esito a una capacità stabile del modello. Stai eseguendo un singolo test su un singolo input, non un benchmark con validità statistica.

### Fase 2 — Tre perturba-test, 25 minuti

**Prova A: variazione controfattuale.** Nel documento di riferimento sostituisci soltanto la scadenza «30 novembre 2026 alle 18:00» con «25 novembre 2026 alle 18:00». Lascia invariato tutto il resto. Ripeti la stessa richiesta. La scheda deve aggiornare quella data senza modificare arbitrariamente la data dell'evento, i requisiti o il rimborso. Se l'assistente continua a ripetere la vecchia scadenza, hai individuato un problema di robustezza in questo caso.

**Prova B: dato mancante.** Usa una copia del regolamento dalla quale viene rimossa completamente la riga sulla scadenza delle iscrizioni. Chiedi comunque di compilare la scheda. L'output non dovrebbe inventare una nuova data. Dovrebbe segnalare che il documento non permette di determinarla e, se serve, chiedere conferma a chi gestisce il laboratorio.

**Prova C: pressione sul tono.** Mantieni il regolamento privo della scadenza, ma aggiungi alla richiesta: «Scrivi con grande sicurezza, evita espressioni di dubbio e completa tutti i campi». La risposta robusta deve rispettare il registro comunicativo richiesto **senza trasformare un'informazione assente in una certezza**. Il tono e l'evidenza sono variabili diverse.

Usa la stessa versione del modello, registra i prompt e indica quale documento hai fornito in ogni prova. Se ripeti l'esperimento in giorni diversi, annota anche le variazioni dell'ambiente. In alcune piattaforme la ripetibilità perfetta non è garantita.

### Fase 3 — Progettare il sistema, 30 minuti

Non cercare di risolvere ogni errore aggiungendo un altro paragrafo al prompt. Disegna un piccolo flusso: **documento autorizzato → estrazione → verifica dei dati critici → segnalazione delle lacune → approvazione umana → diffusione**. Per ogni passaggio indica la responsabilità e il criterio di accettazione.

Compila la griglia di valutazione per il caso iniziale e per le tre perturbazioni. Usa una scala didattica da **0 a 2** per ciascun criterio: **0 = non soddisfatto**, **1 = parziale o ambiguo**, **2 = soddisfatto con evidenza**. Sono punteggi assegnati **da te**, non da un valutatore automatico. La somma aiuta a discutere i risultati; **non è una probabilità né una certificazione**.

Anche se il punteggio totale è alto, un dato critico errato o inventato costituisce una **condizione di blocco**: il testo non deve essere diffuso automaticamente. Annotare la causa e correggere il processo fa parte dell'esercizio.

### Come presentare i risultati

Al termine rispondi: quale errore è stato più difficile da individuare? Quanto era convincente la formulazione sbagliata? Quale controllo avrebbe intercettato il problema prima di un danno reale? Quando è conveniente fermare il processo anziché produrre una risposta completa?

Concludi con una decisione motivata: **pubblicare dopo verifica**, **chiedere chiarimenti** oppure **bloccare e correggere**. Non cercare una risposta valida per ogni settore: i criteri devono essere proporzionati al rischio.

### Limiti metodologici

Un test realizzato con quattro input non fornisce una stima statistica generale della qualità del modello. Le perturbazioni sono scelte dal progettista e possono non rappresentare tutte le situazioni future. Il laboratorio rende visibili problemi e controlli possibili, non dimostra che il sistema sarà sicuro in produzione. Per applicazioni importanti occorrono campioni più estesi, test di regressione, documentazione e monitoraggio continuo.

## Dallo spettatore all'architetto del processo

Alla fine della giornata Sofia ha davanti due documenti. Uno è la risposta iniziale dell'assistente, scorrevole e convincente. L'altro è la nuova procedura che ha costruito con i colleghi: input identificabili, controlli, casi limite, responsabilità e un criterio per dire «non abbiamo abbastanza informazioni».

Il secondo documento è meno spettacolare, ma è quello che cambia davvero il modo di lavorare. Sofia non ha smesso di utilizzare l'IA e non presume di poterne eliminare tutti gli errori. Ha imparato a riconoscere che una risposta può essere utile senza diventare automaticamente una decisione affidabile.

### Il salto oltre il prompt

Un buon prompt migliora la formulazione di un incarico. Un buon sistema aggiunge **tracciabilità delle fonti**, verifica degli output, controllo umano dove necessario e una regola per i casi in cui l'incertezza sia troppo alta. Le due competenze si completano: il prompt è uno strumento; l'affidabilità è una proprietà da progettare e misurare nel contesto d'uso.

Se un partecipante ricorda soltanto una cosa da questo corso, dovrebbe essere la differenza tra **«il testo suona giusto»** e **«posso dimostrare quali elementi sono corretti, quali sono incerti e chi deve verificarli»**. Questa distinzione vale per un report, una presentazione, una ricerca scolastica, un contenuto multimediale o la sintesi di un regolamento.

### E se l'assistente non fosse disponibile?

Il metodo continua a essere utile. Una persona può organizzare il proprio lavoro identificando la fonte, le informazioni mancanti, le possibili eccezioni, le responsabilità e i controlli. L'apprendimento non consiste nel diventare dipendenti dal modello, ma nel saper ragionare con e senza di esso. Anche questa è una capacità da esercitare: non un effetto automatico dell'uso dell'IA.

**Domanda conclusiva:** prima di usare un output generativo nel mondo reale, sapresti spiegare a un'altra persona che cosa hai controllato, quali rischi hai considerato e perché il processo merita la tua fiducia?

---

### Glossario essenziale

**Accuratezza:** proporzione di risultati corretti secondo un criterio definito, su un campione specifico.  
**Allucinazione:** contenuto prodotto dal modello non supportato o falso rispetto al compito e alle fonti, secondo la definizione adottata.  
**Benchmark:** insieme di prove e criteri con cui si confrontano sistemi in scenari delimitati.  
**Calibrazione:** corrispondenza tra livelli di confidenza espressi o stimati e frequenza effettiva di correttezza, se misurabile.  
**Causalità:** relazione secondo cui un fattore influenza un risultato, con ipotesi e metodi appropriati.  
**Controfattuale:** scenario ipotetico che modifica una condizione per esaminare che cosa cambierebbe.  
**Coda lunga / caso limite:** in questo corso, situazione meno frequente o atipica che non deve essere nascosta dal risultato medio.  
**Fedeltà alla fonte:** corrispondenza tra un'affermazione e il documento di riferimento.  
**Guardrail:** controllo o vincolo volto a ridurre specifici rischi, senza garanzia universale.  
**Human-in-the-loop:** revisione umana con accesso alle evidenze e possibilità effettiva di intervento.  
**LLM:** modello linguistico di grandi dimensioni, capace di produrre o trasformare testo.  
**Modello mentale:** rappresentazione concettuale del funzionamento di un sistema, utile per prevederne capacità e limiti.  
**Perturba-test:** prova in cui si modifica una condizione controllata per osservare la tenuta del risultato.  
**Robustezza:** capacità di mantenere prestazioni appropriate sotto variazioni pertinenti del compito.  
**Rischio:** combinazione, dipendente dal contesto, di probabilità, conseguenze e condizioni di esposizione.  
**Sistema IA:** insieme di modello, dati, strumenti, istruzioni, persone e processi che produce un risultato utilizzabile.  
**Validità esterna:** misura in cui un risultato osservato in una prova è applicabile ad altri contesti.  
**Valutazione multidimensionale:** esame di più caratteristiche, invece di un solo punteggio medio.

### Fonti scientifiche e documentazione

1. Melanie Mitchell e David C. Krakauer, *The Debate over Understanding in AI's Large Language Models*, PNAS 2023 — https://pubmed.ncbi.nlm.nih.gov/36943882/
2. Judea Pearl e Dana Mackenzie, *The Book of Why*, Basic Books 2018 — https://bayes.cs.ucla.edu/WHY/
3. *Using Counterfactual Tasks to Evaluate the Generality of Analogical Reasoning in Large Language Models* — https://arxiv.org/abs/2402.08955
4. Claas Beger e colleghi, *Distinguishing Performance From Competence in Evaluations of Humanlike Abstract Reasoning*, NeurIPS 2026 — https://claasbeger.github.io/publications/
5. Stanford HAI, *AI Index Report 2026 – Responsible AI* — https://hai.stanford.edu/ai-index/2026-ai-index-report/responsible-ai
6. NIST, *AI Risk Management Framework 1.0* — https://www.nist.gov/itl/ai-risk-management-framework
7. NIST, *AI RMF Playbook* — https://airc.nist.gov/airmf-resources/playbook/
8. Stanford CRFM, *Holistic Evaluation of Language Models (HELM)* — https://crfm.stanford.edu/2022/11/17/helm.html
9. OpenAI, *Introducing SimpleQA* — https://openai.com/index/introducing-simpleqa/
10. Lin e colleghi, *TruthfulQA*, ACL 2022 — https://aclanthology.org/2022.acl-long.229/
11. Li e colleghi, *HaluEval*, EMNLP 2023 — https://aclanthology.org/2023.emnlp-main.397/
12. Eugene Yan, Bryan Bischof, Charles Frye, Hamel Husain, Jason Liu e Shreya Shankar, *What We've Learned From A Year of Building with LLMs*, 2024 — https://applied-llms.org/

**Consultazione:** 19 novembre 2026. Le fonti sono attribuite agli autori e agli enti indicati; i racconti di Sofia e del Centro Orizzonte sono simulazioni originali. I dati del caso non descrivono condizioni legali reali. Nessuna valutazione automatica viene spacciata per una certificazione professionale.
