# ACR-EXP-C · Proporzione struttura/compito del prompt

**Stato:** ipotesi sperimentale indipendente; non preregistrata né eseguita. Origine: sezione 6b di `sources/user/MANZO_AI_ACR_v0.4.md` e `sources/user/Fibonacci_Prompt_Engineering_v2.md`.

## Oggetto misurabile
Studiare se la quota di token di *impalcatura* S, rispetto ai token del *compito dinamico* D, influenza il successo in compiti di generazione/verifica. Quota operativa: `r=S/(S+D)`, **non** misura della qualità, dell'informazione semantica o della capacità cognitiva del modello.

Categorie di classificazione preregistrate:
- S: struttura generale, descrizione dei ruoli/strumenti, criteri e vincoli riutilizzabili, esempi generici.
- D: richiesta specifica, dati dell'utente, target, esempi pertinenti solo a quel task.
- Istruzioni dell'ambiente e del sistema: riportate separatamente, non manipolate; il totale valutato `S+D` esclude il prompt di sistema fisso del provider. Tokenizer e delimitatori devono essere contati e riportati.

## Ipotesi
- H0-C: nessuna relazione riproducibile tra quota e prestazione; in particolare la quota 0,62 non ha vantaggio robusto sui comparatori.
- H1-C-esplorativa: prestazione non monotona con massimo intermedio, eventualmente vicino a 0,62.
- H1-C-confermatoria **solo se giustificata dal pilot**: S62 superiore a S60 e S65 su un set held-out con dimensionamento e correzione multipla fissati. Non usare gli stessi task per scegliere il 62 e confermarlo.

## Problema di identificazione (essenziale)
**È matematicamente impossibile mantenere contemporaneamente costante il totale S+D, la lunghezza di D e il rapporto r mentre r varia.** Dunque:
- Se il totale è costante, una quota S maggiore implica un compito D più corto; confronti includono variazioni di dettaglio del compito.
- Se il compito D è identico byte-per-byte, aumentare S aumenta anche la lunghezza totale e quindi confonde la quota con la lunghezza.
- Riempire con testo irrilevante NON risolve il confondimento: crea una nuova variabile di rumore.

## Due sotto-studi complementari

### Cα: compito identico, impalcatura variabile
- Mantenere identico D: stesso hash e stesso tokenizer del testo specifico in tutti i bracci.
- S: quattro livelli preregistrati di dettaglio pertinente; usare frammenti di informazione validati e una libreria fissa di template.
- Il totale cambia; riportarlo. Questo studio stima l'effetto di **aggiungere struttura**, non un rapporto aureo isolato.
- Includere una baseline minima senza impalcatura aggiuntiva, se eticamente e tecnicamente appropriato.

### Cβ: totale token fissato, rapporto variabile
- Bracci esplorativi S30, S50, S62, S80: rispettivamente 30%, 50%, 62%, 80% di `S+D`.
- Con totale ipotetico di 1500 token, le quote dinamiche diventano rispettivamente 1050, 750, 570, 300 token: **non** affermare che tutte contengano gli stessi caratteri/informazioni.
- Preparare per ciascun task e braccio una riscrittura semanticamente equivalente, con criteri e dati essenziali **presenti in ogni versione**. Un valutatore indipendente e cieco giudica perdita, ambiguità e aderenza alle informazioni; fallimenti d'equivalenza vengono registrati ed esclusi secondo regola prima definita, non corretti a posteriori dopo aver visto il punteggio del modello.
- Per non attribuire a una singola parafrasi l'effetto del rapporto, produrre più varianti semantiche con ordine controbilanciato per braccio.
- Come controllo, ripetere Cβ con almeno un secondo budget (es. 1000 e 1500, se il contenuto minimo cabe in entrambi) e verificare interazione quota × lunghezza.
- Prompt che non rispettano budget o non conservano il contenuto minimo vanno marcati come **non fattibili**, mai padded con filler.

## 62% come proprietà speciale: test ravvicinato
Solo se il pilot suggerisce un massimo in prossimità di 0,62, pianificare **held-out** S60/S62/S65 (più controllo S50 e S80 se il budget lo consente), con criterio confermatorio e correzione per confronti multipli. Un massimo generico intermedio non è prova di una proprietà aurea.

## Input e test
- Compiti web verificabili indipendentemente dal Curator: accessibilità, validazione form, responsività, regressioni funzionali.
- Stesso modello/versione, temperatura (o effort), ambiente, istruzioni di sistema fisse, ordine di presentazione controllato, costi.
- Primaria: tasso di successo task completo (non solo test individuali), definito prima dell'esecuzione.
- Secondarie: quota di test deterministici PASS, correttezza dei vincoli, token reali, latenza/costo, regressioni e giudizi umani ciechi.
- L'esperimento sulla proporzione non richiede le memorie ACR: disabilitare retrieval e autocorrezione per evitare contaminazione.

## Analisi
- Stime appaiate per task e replica con intervalli bootstrap cluster per task; modello gerarchico come sensibilità.
- Valutare trend monotono, non-monotono e interazioni con lunghezza e famiglia di task; correzione per confronti multiple dove necessaria.
- Prevedere almeno 12 task × 5 repliche esplorative per braccio *solo come piano logistico*, non come potenza statistica garantita.
- Documento di risultati deve riportare anche fallimenti di fattibilità e le prestazioni di 30/50/80, non soltanto di 62.

## Misure di sicurezza e interpretazione
- Esempi che rivelano la soluzione attesa del benchmark sono proibiti; controllare leakage tra generazione dei prompt e test.
- Non interpretare il risultato come 'ottimo universale': dipende da task, modello, lunghezza e contenuto.
- Se il 62 non prevale, il rapporto aureo NON va mantenuto come regola prescrittiva del prodotto.

## Preregistrazione ancora necessaria
Modello, tokenizer, versioni, task, fattibilità del budget, prompt reali, rubrica equivalenza, randomizzazione, output schema, analisi, cost cap, percentuali effettive e STOP rule.
