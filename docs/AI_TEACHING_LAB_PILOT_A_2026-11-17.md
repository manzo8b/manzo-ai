# AI Teaching Lab · Pilota A in 40 minuti

**Stato:** protocollo pronto da provare, non eseguito con docenti. I 40 minuti sono un budget progettuale, non un tempo osservato. Se necessario estendere a 45 minuti e annotarlo; non saltare i controlli per rispettare il tempo.

**Scopo:** verificare se un docente principiante riesce a progettare, controllare, salvare e riaprire un piccolo kit nei quattro ambienti. La prova riguarda usabilità e comprensione del docente; non misura l'efficacia sull'apprendimento degli alunni, non rilascia attestati e non convalida le 20 ore stimate del corso.

**Principio:** il docente progetta, l'IA assiste, il docente verifica e decide.

## Prima di iniziare

- Usa un computer o telefono con browser aggiornato e una cartella locale chiamata `pilota-A`. Controlla la raggiungibilità della [pagina del corso](https://manzo8b.github.io/manzo-ai/it/formazione/ia-per-la-didattica/); il solo codice del repository non prova che l'ultima versione sia pubblicata.
- Scarica nella cartella i due disegni sintetici: [forme A e B](../editorial/learning/ai-teaching-lab/it/pilot-a/confronto-forme-01.png) e [forme C e D](../editorial/learning/ai-teaching-lab/it/pilot-a/confronto-forme-02.png). Sono diagrammi geometrici creati in codice per questa prova, senza persone, dati sperimentali o media di terzi. Il [sorgente riproducibile](../editorial/learning/ai-teaching-lab/it/pilot-a/create-images.py) usa soltanto Python standard. Non serve eseguirlo per svolgere il pilota.
- Tieni aperta questa scheda come traccia. Non occorrono account o servizi generativi esterni. Non inserire dati degli studenti, immagini di persone o situazioni sanitarie.
- Per lo Studio voce puoi registrare volontariamente la tua voce adulta sul dispositivo, dopo aver autorizzato il microfono, oppure importare una lettura autorizzata del copione sotto. La registrazione resta fuori dalla raccolta di osservazioni: non inviarla all'osservatore. Se manca un audio utilizzabile, lascia la scheda in bozza e annota il limite; un segnale acustico di collaudo non sostituisce una narrazione didattica.
- Queste immagini servono a una prova interna. Per un'eventuale distribuzione pubblica del kit, il titolare del progetto deve indicare le condizioni di riuso; non inventare una licenza.

## Il brief da personalizzare

| Campo | Esempio da usare e controllare |
|---|---|
| Titolo | Tre lati, una regola |
| Disciplina | Geometria |
| Destinatari | Prima media, classe ipotetica, 11–12 anni |
| Prerequisito | Contare lati e vertici di una figura chiusa composta da segmenti |
| Obiettivo osservabile | Distinguere triangoli e quadrilateri in due coppie di figure e motivare la scelta contando i lati, anche quando cambia l'orientamento |
| Prova di apprendimento | Classificare A, B, C e D; spiegare perché A e C appartengono allo stesso gruppo e correggere l'affermazione «C non è un triangolo perché è inclinato» |
| Criterio | Identificare A e C come triangoli e B e D come quadrilateri, usando numero di lati e chiusura, senza affidarsi soltanto a colore o orientamento |

Questi criteri sono una proposta per l'esercizio, non una rubrica standardizzata. Se il prerequisito manca, inserisci prima un esempio guidato di conteggio; non interpretare l'errore come una caratteristica della persona.

## Percorso del docente

| Minuti indicativi | Operazione | Come controllare e proseguire |
|---|---|---|
| 0–4 | Dalla pagina del corso trova i quattro ambienti; leggi le indicazioni sulle operazioni locali | Spiega a voce che qui si preparano/importano materiali e si registrano dichiarazioni; non parte un modello generativo |
| 4–9 | Nello Studio immagini scrivi il brief della tabella; scegli produzione manuale/locale | Obiettivo e prova devono richiedere di spiegare un criterio, non soltanto guardare una figura |
| 9–15 | Importa `confronto-forme-01.png`, dichiara provenienza e fonte, inserisci il testo alternativo; controlla l'immagine e la checklist, poi esporta il JSON | Conta davvero i lati; confronta la descrizione con il disegno. Conserva il PNG originale e la scheda separati |
| 15–22 | Nello Studio voce copia e personalizza il copione, registra/importa la lettura, ascoltala tutta, correggi la trascrizione e compila i controlli | La trascrizione deve corrispondere a ciò che si sente. Esporta sia audio sia scheda JSON; il copione scritto non dimostra che l'audio sia corretto |
| 22–29 | Nello Studio video prepara due scene da 7 secondi, usando i due PNG, un obiettivo e una didascalia per scena; dichiara la fonte di ciascuna | Controlla ordine, tempi e descrizioni; esporta scheda JSON e sottotitoli WebVTT. Il WebM locale è silenzioso e dipende dal browser: se non disponibile, conserva storyboard, PNG e JSON e annota il fallback |
| 29–36 | Nel Workspace compila il brief comune, importa i tre JSON, descrivi sequenza, alternative e diritti; riapri gli originali e verifica prima di approvare | Lo stato importato è un'approvazione dichiarata nel file. Il Workspace non prova da solo che qualcuno abbia visto/ascoltato i materiali |
| 36–40 | Esporta manifest JSON e scheda HTML, chiudi e riapri il manifest; controlla testi e provenienze | Il kit riaperto deve richiedere nuova verifica. I media restano separati. Modifica poi l'obiettivo di una copia di prova e controlla che l'approvazione precedente venga invalidata |

Se interrompi, esporta una bozza JSON prima di uscire. La ripresa del manifest recupera il progetto nel Workspace; non implica il caricamento dei media né il ripristino automatico delle singole sessioni dei tre Studi. Non lasciare l'unica copia del lavoro nella memoria della pagina.

### Testi pronti da rivedere

**Fonte per i due disegni:** «Diagramma geometrico sintetico MANZO AI, creato in codice per il pilota A; nessun generatore IA o media di terzi; uso interno dimostrativo». Distingui questa dichiarazione da una licenza per la distribuzione pubblica.

**Descrizione dell'immagine 01:** «A è una figura chiusa con tre segmenti e tre vertici, con una base orizzontale. B è una figura chiusa con quattro segmenti e quattro vertici». La descrizione deve rendere disponibili i dati necessari anche senza colore.

**Descrizione dell'immagine 02:** «C è una figura chiusa con tre segmenti e tre vertici, ruotata rispetto ad A. D è una figura chiusa con quattro segmenti e quattro vertici». Il cambio di colore non è il criterio di classificazione.

**Copione da leggere e trascrivere:** «Osserva A e B. Conta i lati di ogni figura chiusa. A ha tre lati: è un triangolo. B ne ha quattro: è un quadrilatero. Ora osserva C: è ruotato. Conta i suoi lati e spiega se l'orientamento cambia il gruppo a cui appartiene». Inserisci eventuali pause reali e correggi la trascrizione dopo l'ascolto.

**Scena 1:** immagine 01; titolo «Osserva e confronta»; obiettivo «Usare il numero dei lati per confrontare A e B»; didascalia «Conta i lati di A e B. Che differenza trovi?».

**Scena 2:** immagine 02; titolo «La regola funziona ancora?»; obiettivo «Applicare il criterio a figure con orientamento diverso»; didascalia «C è inclinato: conta i lati e motiva la classificazione».

**Sequenza per il Workspace:** «1 minuto: osservare A e B e formulare un criterio. 1 minuto: ascoltare o leggere la spiegazione. 1 minuto: osservare C e D, mettere in pausa e classificare. 2 minuti: motivare una scelta e correggere un errore». È una microattività ipotetica, non una durata misurata in aula.

**Alternative accessibili:** descrizioni dei due PNG, trascrizione della voce e storyboard testuale; nessun significato affidato solo al colore. Consenti di leggere in autonomia e di mettere in pausa il video. Verifica che le informazioni siano equivalenti, senza dichiarare conformità WCAG sulla base della sola checklist.

**Feedback previsto su un errore sintetico:** se la risposta è «C non è un triangolo perché è inclinato», chiedi «Conta i segmenti che chiudono C. Quale criterio hai usato per A? Vale anche qui?». Dopo la revisione proponi una nuova figura ruotata; non attribuire uno stile di apprendimento alla persona.

## Verifica della consegna

Il docente deve poter mostrare una cartella con due PNG, l'audio autorizzato, tre schede JSON, WebVTT, manifest e HTML. Il WebM silenzioso è facoltativo quando il browser non lo supporta e il limite va dichiarato. I file di testo non contengono i binari audiovisivi.

Prima di dichiarare il kit pronto, deve spiegare: quale obiettivo osservabile guida i media; quale informazione aggiunge ogni mezzo; quali originali ha controllato; quale errore cambierebbe la decisione; come riaprire il progetto. Le caselle sono attestazioni del docente, non controlli disciplinari automatici. Se una verifica non è stata eseguita, salva una bozza e scrivi **NON ESEGUITA**.

## Scheda di osservazione ancora da compilare

Non registrare nomi, voci, schermate di account o dati degli studenti. Usa un codice della sessione e note sul compito. La scheda è vuota: nessun risultato è stato raccolto o simulato.

| Osservazione | Esito da compilare |
|---|---|
| Giorno, dispositivo e browser | — |
| Tempo effettivo e punto di interruzione | — |
| Trova gli Studi e il Workspace | Da solo / con aiuto / non riesce |
| Distingue operazioni locali, IA esterna e approvazioni dichiarate | Sì / parzialmente / no; frase osservata: — |
| Scrive obiettivo, criterio e verifica coerenti | Sì / da rivedere; esempio osservato: — |
| Trova e conserva JSON e media separati | Sì / con aiuto / no |
| Controlla gli originali prima di spuntare la checklist | Osservato / non osservato / non eseguito |
| Riapre il manifest e comprende la nuova revisione | Sì / con aiuto / no |
| Dopo una modifica riconosce l'invalidazione dell'approvazione | Sì / no / non eseguito |
| Errori, confusione e fallback incontrati | — |
| Una modifica da provare nella sessione successiva | — |

Una sessione esplorativa non dimostra efficacia educativa, conformità, sicurezza generale o usabilità per tutti. La successiva osservazione con adulti volontari spetta all'autore del progetto; eventuale impiego con alunni richiede una valutazione distinta nel contesto scolastico.
