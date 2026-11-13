# MANZO AI MEDIA · EP01
# Il prompt: da una semplice domanda a un'istruzione professionale
**Fonte editoriale originale per NotebookLM / Video Overview · 13 novembre 2026**  
**Lingua:** italiano · **Destinazione:** MANZO AI, sezione Video e slide / Media  
**Formato desiderato:** video podcast esplicativo, dialogo naturale fra due voci, circa 9–12 minuti se il formato lo consente.  
**Pubblico:** principianti, freelance, formatori, professionisti, sviluppatori.  
**Stato:** sorgente pronta per produzione; video non ancora generato né pubblicato.

## Obiettivo
Alla fine del video, lo spettatore deve distinguere un prompt generico da un'istruzione controllabile; saper progettare una richiesta con obiettivo, contesto, vincoli, formato e verifica; riconoscere quando servono fonti, strumenti, dati aggiornati e supervisione umana; comprendere l'uso di esempi, iterazioni e test nel prompt engineering.

## Apertura: non è una formula magica
«Scrivi un articolo.» È un prompt. «Scrivi un articolo divulgativo di 700 parole per lettori senza conoscenze tecniche, spiega che cos'è l'intelligenza artificiale generativa, usa sottotitoli e segnala ogni dato che richiede una fonte» è un prompt molto più utilizzabile.

La differenza non sta nella lunghezza da sola. Sta nella chiarezza del compito e nella possibilità di controllare la qualità del risultato. Un prompt è un input — generalmente scritto, ma talvolta multimodale — con cui una persona orienta il comportamento di un modello di intelligenza artificiale. Non è codice eseguibile nel senso ordinario, non garantisce verità e non trasforma un modello in un esperto infallibile. È una specifica di lavoro.

## Atto I · Livello base: le cinque domande
Per costruire un primo prompt utile, bisogna rispondere a cinque domande:
1. **Obiettivo:** che cosa voglio ottenere, esattamente?
2. **Contesto:** quali informazioni deve conoscere il modello?
3. **Destinatario:** a chi è rivolto il risultato?
4. **Formato:** tabella, testo, elenco, scaletta, codice, JSON, altro?
5. **Criteri di qualità:** come riconosco una risposta valida?

**Esempio base — prima.** «Parlami dei prompt.»

**Esempio base — dopo.** «Spiega a una persona che non ha mai usato l'AI che cos'è un prompt. Usa un esempio tratto dal lavoro quotidiano, un confronto fra una richiesta vaga e una precisa, e concludi con tre errori da evitare. Massimo 300 parole. Non usare termini tecnici senza definirli.»

Analisi: il secondo esempio definisce scopo, pubblico, argomento, struttura, limite e qualità attesa. Non richiede alcun trucco linguistico.

## Atto II · Il passaggio da utente a progettista
Un prompt professionale non si limita a chiedere un contenuto; definisce anche come gestire ambiguità, dati mancanti, rischio di errori e criteri di accettazione.

Formula di lavoro orientativa:
**Prompt = obiettivo + contesto + input + vincoli + output + verifica.**

Non è uno standard universale né una legge matematica. È una checklist pratica. La struttura varia secondo il modello, il compito e l'interfaccia.

**Caso professionale: revisione di una pagina web.**
«Agisci come revisore UX/UI. Analizza il testo e il codice HTML/CSS allegati per individuare problemi di gerarchia tipografica, contrasto, leggibilità mobile e accessibilità. Non cambiare contenuti o JavaScript. Riporta le criticità in tabella con gravità, evidenza, correzione proposta e modalità di test. Non dichiarare test browser o WCAG che non hai effettivamente eseguito. Se non puoi vedere il rendering, indica esplicitamente il limite.»

Questo prompt è più robusto perché delimita responsabilità, prove e comportamento in presenza di informazioni insufficienti. La frase «agisci come» serve a orientare il tipo di analisi; non conferisce qualifiche reali né sostituisce una verifica.

## Atto III · Le tecniche che contano
**Zero-shot:** richiesta senza esempi, sufficiente per compiti comuni e ben specificati.  
**Few-shot:** uno o più esempi di input/output per mostrare tono, classificazione o formato desiderati. Gli esempi devono essere corretti, rappresentativi e privi di dati sensibili non necessari.  
**Scomposizione:** dividere un compito complesso in fasi verificabili; per esempio ricerca, schema, bozza, controllo delle affermazioni, revisione finale.  
**Output strutturato:** chiedere uno schema preciso, come una tabella con colonne fisse o JSON valido, e validarlo con strumenti quando il risultato alimenta un software.  
**Contesto documentale:** fornire materiali pertinenti e delimitare ciò che proviene dalle fonti. In sistemi con retrieval, verificare copertura e attendibilità dei documenti.  
**Iterazione:** confrontare la risposta con criteri espliciti, correggere il prompt o fornire feedback mirato e riprovare.  
**Valutazione sistematica:** per usi ripetuti, costruire casi di test rappresentativi, compresi casi limite e avversi, senza affidarsi a una singola risposta riuscita.

Tecniche come XML o delimitatori possono rendere più chiara la separazione fra istruzioni e documenti. Non sono però una garanzia di sicurezza e non impediscono automaticamente la prompt injection.

## Atto IV · La dimostrazione in tre versioni
**Versione A — vaga:** «Fammi una strategia social.»

**Versione B — definita:** «Prepara una strategia Instagram di quattro settimane per un piccolo progetto culturale. Pubblico: adulti interessati alla divulgazione. Budget pubblicitario: zero. Proponi due post e un video breve a settimana, con obiettivo, formato e indicatore misurabile.»

**Versione C — professionale:**
«Obiettivo: costruire un calendario Instagram di quattro settimane per un progetto culturale indipendente. Pubblico: adulti interessati a scienza e tecnologia; tono: preciso ma accessibile. Vincoli: zero budget ADV, niente statistiche inventate, niente promesse di crescita. Input: descrizione del progetto e post precedenti forniti in allegato. Output: tabella con data, rubrica, messaggio centrale, formato, CTA e metrica. Prima evidenzia le ipotesi dovute a dati mancanti; dopo il piano, proponi tre test A/B realistici e un controllo editoriale delle fonti.»

La versione C non è sempre la migliore: per una domanda semplice, una richiesta breve può essere più efficiente. La precisione è proporzionata alla complessità e al rischio del compito.

## Atto V · Perché anche un buon prompt può fallire
Un modello può inventare riferimenti, interpretare male l'intento, produrre contenuti obsoleti, perdere dettagli in contesti lunghi o rispettare male un formato. La qualità del prompt riduce alcuni errori, ma non garantisce l'affidabilità.

Tre distinzioni fondamentali:
- **Istruzione ≠ prova:** chiedere «usa fonti» non dimostra che le fonti siano state consultate o che siano reali.
- **Fluidità ≠ accuratezza:** una risposta ben scritta può essere falsa.
- **Autonomia ≠ responsabilità:** negli impieghi professionali le decisioni importanti restano soggette a controllo e responsabilità umana.

Per temi sanitari, giuridici, finanziari o di sicurezza, verificare con fonti aggiornate e professionisti competenti; non inserire dati personali riservati senza adeguata autorizzazione e protezione.

## Atto VI · Il ciclo di lavoro professionale
1. **Definire il risultato atteso** e perché serve.
2. **Preparare input e fonti**, privilegiando qualità e pertinenza.
3. **Specificare il prompt**, includendo output e limiti.
4. **Generare un primo risultato.**
5. **Valutare con criteri oggettivi**: accuratezza, completezza, formato, tono, rischio, ripetibilità.
6. **Correggere il prompt o gli input**, non solo la risposta.
7. **Testare su casi diversi**, documentando errori e regressioni.
8. **Sottoporre a controllo umano**, soprattutto prima di pubblicare, automatizzare o prendere decisioni.

Si può mostrare un semplice ciclo visivo: **Definisci → Genera → Verifica → Migliora → Ripeti**.

## Atto VII · Una dimostrazione finale
Chiedere a un modello di progettare una pagina di un corso:
«Progetta la struttura testuale di una pagina didattica intitolata “Prompt professionali”. Il pubblico include principianti e professionisti. Prevedi un'introduzione di massimo 100 parole, tre esempi progressivi, un esercizio con soluzione commentata, una checklist di revisione e un'avvertenza sui limiti dei modelli. Non inventare benchmark, certificazioni né dati sulla performance. Restituisci prima la struttura; attendi revisione prima del codice.»

Il pubblico del video deve vedere che il prompt definisce un processo e non soltanto una risposta.

## Chiusura narrativa
«Non vince chi scrive il prompt più lungo, né chi conosce una formula segreta. Lavora meglio chi sa definire un problema, fornire il contesto utile, chiedere un risultato verificabile e conservare la capacità di giudicare la risposta. Il prompt è il punto di partenza. La competenza è nel metodo.»

**Invito finale:** «Su MANZO AI puoi passare dalla teoria alla pratica, esplorare gli esempi e allenarti nel laboratorio tecnico.»

## Glossario in sovraimpressione
- **Prompt:** istruzione o input inviato al modello.
- **Contesto:** informazioni pertinenti al compito.
- **Vincolo:** requisito o limite esplicito.
- **Output:** risultato generato.
- **Zero-shot / Few-shot:** senza esempi / con esempi.
- **Structured output:** risposta in un formato definito.
- **Hallucination:** contenuto apparentemente plausibile ma inventato o non fondato.
- **Prompt injection:** tentativo di alterare il comportamento del sistema tramite contenuti non affidabili.
- **Evaluation / Evals:** criteri e test per misurare la qualità dei risultati.
- **Human-in-the-loop:** revisione e decisione umana nel processo.

## Regia editoriale per il Video Overview
Titolo a schermo: **IL PROMPT NON È MAGIA**. Sottotitolo: *Dalla prima domanda al metodo professionale*. Due voci naturali in italiano, tono energico e autorevole, senza enfasi pubblicitaria. Apertura immediata con il confronto «Fammi una strategia social» / «Obiettivo, pubblico, vincoli, formato, verifica». Mostrare progressivamente esempi A–B–C, grafica del ciclo iterativo, etichette brevi e leggibili. Design: bianco dominante, nero, accenti blu/verde/corallo/viola coerenti con MANZO AI. No estetica retro, no sfondi grigio carta, no slide dense o infografiche illeggibili. La narrazione deve essere comprensibile senza conoscere termini tecnici. Non attribuire a MANZO AI test o capacità non documentate. Inserire una dicitura finale: «Contenuto educativo realizzato con assistenza di AI generativa e revisione editoriale».

## Fonti metodologiche per verifica editoriale
Queste fonti sono riferimenti da consultare e, se disponibili, importare separatamente come fonti in NotebookLM. Non dichiarare che ogni dettaglio del video sia una citazione diretta:
- OpenAI, Prompt engineering: https://platform.openai.com/docs/guides/prompt-engineering
- Anthropic, Prompt engineering overview: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- Google Cloud, Prompt design strategies: https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies
- NIST, AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
