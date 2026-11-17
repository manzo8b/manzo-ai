# Studio immagini — rilascio tecnico v0.1
Data: 2026-11-17

## Implementato
File: `tools/ai-teaching-image-studio/index.html`
- Cinque fasi con tab accessibili: brief, modello, prompt, immagine, verifica
- Brief e prova di apprendimento separati
- Registro dei provider dichiarativo: ChatGPT, Gemini Nano Banana, altro, locale
- Prompt locale editabile e copiabile; nessuna chiamata API
- Importazione PNG/JPEG/WebP ≤10 MB e anteprima locale
- Provenienza esplicita, alt text, responsabile, quattro controlli e approvazione
- Invalidazione dell'approvazione dopo modifica dei campi
- Export della scheda JSON senza binario dell'immagine
- Layout responsive, indicatori di focus, regioni aria-live

## Limiti verificabili
- Creato un file HTML nel repository, non risulta da questo commit un deploy autonomo di GitHub Pages: il workflow esistente potrebbe pubblicare un archivio ZIP statico al posto dei file sorgente.
- Non è un plugin del corso precedente: la navigazione AI Teaching Lab non è ancora collegata.
- Nessun provider di immagini è connesso, nessuna API viene invocata.
- Nessuna persistenza: dati ed anteprima sono temporanei, esportare prima di chiudere.
- Il JSON contiene metadati ma non il file immagine e non costituisce prova indipendente delle verifiche dichiarate.
- Il prototipo non è ancora stato sottoposto a test automatici o QA fisico su iPhone.

## Test di accettazione da eseguire
1. Aprire HTML su desktop e iPhone Safari, controllare leggibilità e navigazione a schede.
2. Compilare brief, selezionare modello, costruire e copiare prompt.
3. Importare PNG/JPEG/WebP e verificare blocco >10 MB e formati differenti.
4. Tentare approvazione senza dati, senza importazione, senza checklist: deve fallire.
5. Approvare correttamente con tutti i dati e poi modificare un campo: deve tornare in bozza.
6. Esportare JSON e confermare assenza dei dati binari di immagine.
7. Test tastiera, screen reader e contrasto; non considerare completato finché non verificato.

## Integrazione successiva
Identificare in modo certo il repository e la pagina hosting di AI Teaching Lab; quindi collegare questo modulo nel menu senza sostituire i componenti esistenti. Valutare il workflow Pages di MANZO AI e l'eventuale pubblicazione secondo il processo del progetto. Solo dopo QA, parlare di pagina online.
