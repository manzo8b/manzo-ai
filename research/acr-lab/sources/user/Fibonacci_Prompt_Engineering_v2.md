# Dalla matematica all'architettura dei prompt
**La sequenza di Fibonacci come metafora di progettazione nel prompt engineering**
Versione rivista: analogie dichiarate come tali, ipotesi separate dai fatti

## 1. La successione di Fibonacci
La successione parte da 0 e 1, e ogni termine è la somma dei due precedenti:

F(n) = F(n-1) + F(n-2), con F(0) = 0 e F(1) = 1

Si sviluppa così: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144.

Fu introdotta nell'Europa latina da Leonardo Pisano, detto Fibonacci, nel *Liber Abaci* (1202). Il trattato nacque come manuale di calcolo commerciale e fu decisivo per la diffusione in Europa del sistema numerico indo-arabico. Il celebre problema dei conigli è un esempio contenuto al suo interno.

Il rapporto tra due termini consecutivi, F(n) / F(n-1), converge al numero aureo Phi ≈ 1,618034. Dividendo un rettangolo aureo in quadrati si costruisce la spirale aurea.

**Dove la connessione con la natura è solida:** la fillotassi (disposizione delle foglie), le spirali dei semi di girasole e delle pigne seguono numeri di Fibonacci, perché l'angolo aureo (circa 137,5°) distribuisce gli elementi con poche sovrapposizioni.

**Dove va evitato l'eccesso:** la conchiglia del nautilus e i bracci delle galassie sono spirali logaritmiche, con un rapporto di crescita diverso da quello aureo. Citarli come esempi di Fibonacci è un luogo comune impreciso.

## 2. Dal numero allo spazio: proporzione e architettura
L'idea di proporzione armonica attraversa tutta la storia dell'architettura, ma con gradi di certezza diversi:

- **Rinascimento:** Alberti definì la bellezza come armonia delle parti, e Palladio progettò le ville venete con rapporti semplici tra le stanze, ispirati soprattutto ai rapporti interi e alle armonie musicali. L'attribuzione specifica alla sezione aurea è meno documentata.
- **Antichità classica:** la presenza della sezione aurea nel Partenone è un'ipotesi molto discussa, e le misurazioni non la confermano in modo univoco. La presentiamo come una lettura possibile, non come un fatto.
- **Età moderna:** Le Corbusier propose il Modulor (1948), una scala di proporzioni basata sulla statura umana e sui numeri della successione. Qui il legame con Fibonacci è documentato.
- **Oggi:** la progettazione parametrica usa algoritmi ricorsivi e geometrie generative, con interesse per forme organiche e ottimizzazione dei materiali.

## 3. Dall'architettura al prompt: sei livelli di progettazione
Il passaggio al prompt engineering è **un'analogia di progetto**: un prompt di qualità si costruisce per strati, e ogni strato si appoggia sui precedenti. Non esiste una dimostrazione che questi strati si combinino secondo la legge di Fibonacci.

| Livello | Nome | Funzione nel prompt |
|---|---|---|
| 1 | Intento | Il compito in forma atomica (es. «Scrivi un'analisi») |
| 2 | Ruolo | Competenza e prospettiva richieste al modello |
| 3 | Contesto | Scenario, obiettivo, destinatario |
| 4 | Vincoli e formato | Tono, struttura, lunghezza, esclusioni |
| 5 | Esempi | Campioni dell'output atteso, per ancorare stile e formato |
| 6 | Verifica | Criteri di controllo, preferibilmente esterni al modello |

Note di rigore:
- Gli esempi migliorano soprattutto formato e aderenza allo stile. **Non eliminano le allucinazioni.**
- Chiedere al modello di ragionare passo per passo può aiutare in alcuni compiti, ma l'autocorrezione senza un controllo esterno spesso non corregge davvero. Per questo il livello 6 prevede, dove possibile, test deterministici o revisione umana.
- Il ruolo assegnato ("agisci come…") ha un effetto variabile e dipende dal modello.

## 4. Principi applicati
### 4.1 Bilanciamento tra impalcatura e compito (ipotesi)
Un prompt troppo breve produce risposte generiche, mentre un prompt carico di dettagli irrilevanti disperde l'attenzione del modello. Si ipotizza che esista un rapporto favorevole tra:
- **impalcatura statica** (ruolo, contesto, vincoli, esempi);
- **componente dinamica** (compito e dati di input).

La proporzione 61,8% / 38,2% è un'ipotesi di lavoro, **non una regola**. Il rapporto ottimale dipende dal compito, dal modello e dalla lunghezza dell'input. Verrà messa alla prova nell'Esperimento C (vedi specifica ACR v0.4).

### 4.2 Prompt chaining
Per compiti complessi conviene dividere il lavoro in passaggi: l'output di uno diventa input vincolato del successivo (idee → outline → bozza → revisione). È una pratica consolidata. Il collegamento con la progressione di Fibonacci rimane una metafora: ogni passaggio integra il risultato dei precedenti.

### 4.3 Ordine degli elementi nei prompt multimodali
Nei modelli testo-immagine l'ordine dei termini tende a influenzare il risultato, con maggior peso a ciò che compare per primo. Un ordine pratico è: soggetto, atmosfera e stile, dettagli tecnici e luce, parametri e esclusioni. È una tendenza osservata, che varia da modello a modello e va verificata sul sistema in uso.

## 5. Sintesi comparativa
| Livello | Analogia architettonica (metafora) | Funzione nel prompt |
|---|---|---|
| 1 Intento | L'idea di progetto, il primo schizzo | Azione atomica |
| 2 Ruolo | Il committente e la scala di misura | Competenza e prospettiva |
| 3 Contesto | Il sito e la pianta | Scenario, obiettivo, destinatario |
| 4 Vincoli e formato | Le strutture portanti e le altezze limite | Tono, layout, esclusioni |
| 5 Esempi | Plastici e prove sui materiali | Campioni dell'output atteso |
| 6 Verifica | Collaudo e abitabilità | Controlli, test, revisione |
| Rapporto 61,8 / 38,2 | Proporzione dell'involucro | **Ipotesi** da testare |

## 6. Cosa affermiamo e cosa no
**Affermiamo:** un prompt strutturato per livelli è più controllabile di uno monolitico; esempi e vincoli migliorano la coerenza; la verifica esterna è più affidabile dell'autocorrezione.

**Non affermiamo:** che Fibonacci governi il prompt engineering; che il rapporto 61,8/38,2 sia ottimale; che gli esempi eliminino le allucinazioni; che il Partenone o il nautilus siano esempi dimostrati di sezione aurea.
