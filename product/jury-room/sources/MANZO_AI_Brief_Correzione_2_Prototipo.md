# Brief di correzione n. 2 — Prototipo «La stanza dei giurati»

**Progetto:** MANZO AI · MARCELUS AI LAB · **Autore:** Marcelo Javier Fernandez Caballero
**Versione:** 1.0 · **Data:** 21 novembre 2026
**Destinatario:** harness di sviluppo (Codex / Claude Code)
**File in oggetto:** `index.html`, `banco-di-prova.html`, `officina-locale.html`, `sala-dei-confini.html`, `assets/styles.css`, `assets/rooms.css`, `assets/app.js`, `assets/experiment-data.js`, `assets/room-practices.js`, immagini e video in `assets/`

---

## 1. Contesto

La prima serie di correzioni è stata applicata bene: testi di onestà sistemati, contenuti nell’HTML, rete affermazioni-fonti, prima/dopo, registro con caselle e più modelli, tre stanze collegate dall’indice.

Questo secondo brief riguarda i problemi emersi rileggendo i quattro file. **La revisione è stata fatta sul solo HTML:** `app.js`, `room-practices.js`, i CSS, il video e le immagini non sono stati letti. La Fase 0 serve a verificarli.

---

## 2. Regole che non cambiano

1. Nessun risultato inventato e nessun test dichiarato «superato» dalla pagina.
2. Nessuna API AI e nessun servizio a pagamento: solo HTML, CSS e JavaScript puro su GitHub Pages.
3. Solo dati fittizi, con avviso visibile.
4. Nessun tracciamento e nessuna memorizzazione sul dispositivo. I dati restano nella memoria della pagina.
5. `noindex,nofollow` finché Marcelo non autorizza la pubblicazione.
6. Il testo dei contenuti è fedele ai sorgenti (`MANZO_AI_Progetto_Esperimenti.md`, `MANZO_AI_Esperimento_02_Governo.md`, `MANZO_AI_Esperimento_03_Officina.md`). I sorgenti sono stati rivisti: vedi punto 9.
7. Ogni elemento sintetico o scritto da noi è dichiarato come tale.
8. Colore mai da solo: stati e livelli hanno sempre etichetta testuale.

---

## 3. Priorità

| Priorità | Punti | Tema |
|---|---|---|
| **P0** | 1, 2, 3 | Spoiler della chiave e affermazioni da correggere |
| **P1** | 4, 5, 6, 7 | Struttura, caricamento e interazione delle stanze |
| **P2** | 8, 9, 10 | Dettagli e allineamento dei testi |

Ordine di lavoro: Fase 0 → P0 → P1 → P2.

---

## 4. P0 — Spoiler e onestà

### Punto 1 — Il registro rivela la chiave prima dell’indagine

**Problema.** In `banco-di-prova.html` il passo 05 (registro) elenca per intero le otto lacune L1–L8 con il testo completo, mentre il passo 02 chiede all’utente di trovarle da solo. Chi scorre la pagina vede le risposte prima di fare l’esercizio.

**Cosa fare.**
1. Il blocco «Lacune individuate nella risposta del modello» del registro resta nascosto finché l’utente non ha completato il passo 02 (clic su «Confronta con la chiave»).
2. Prima di allora il blocco mostra un messaggio: *«La lista delle lacune si sblocca dopo l’indagine del passo 02.»* con un pulsante secondario **«Salta l’indagine e mostra la lista»**, per chi vuole usare solo la Parte 2.
3. Lo stato di sblocco vive nella memoria della pagina; «Ricomincia la prova» lo azzera.
4. Il blocco «Come classificare gli errori» (4 classi) può restare sempre visibile: non rivela la chiave.

**Verifica.** Aprendo la pagina e scorrendo fino al registro senza fare il passo 02, nessuna lacuna è leggibile. Dopo il confronto (o dopo «Salta…») la lista compare.

### Punto 2 — L’ID «FA» rivela il falso allarme

**Problema.** Nel passo 02 le opzioni sono L1–L8 più una voce con ID **«FA»** («La validità di 30 giorni non è indicata»). Le otto lacune hanno tutte un ID «L#»: l’unica voce con un ID diverso è il falso allarme.

**Cosa fare.**
1. Durante la selezione, **non mostrare gli ID** delle opzioni (né «L#» né «FA»): usare solo il testo, con un segnaposto neutro (per esempio un cerchio o un numero progressivo da 1 a 9 nell’ordine visualizzato).
2. Dopo «Confronta con la chiave», ogni opzione mostra la sua etichetta reale: **L1–L8** oppure **«Falso allarme»**, con testo (non solo colore).
3. Verificare che l’ordine delle opzioni resti mescolato e che i `value` interni non appaiano nel testo visibile.

**Verifica.** Prima del confronto, nessun elemento visibile distingue il falso allarme dalle lacune vere.

### Punto 3 — «Pilota approvato» e stato delle card in Home

**Problema.** Nell’indice, la sezione «Il nostro patto» dice che *«il Banco di prova è il pilota approvato»*. Nessuna approvazione è avvenuta. Inoltre le tre card portano il badge «In preparazione» mentre le stanze sono ora anteprime interattive.

**Cosa fare.**
- Sostituire il testo con: *«Tre esercizi basati su scenari fittizi, tutti in anteprima interattiva: il Banco di prova è il primo sviluppato. Nessun risultato viene inventato e nessun dato viene inviato a server.»*
- Badge delle tre card: **«Anteprima interattiva»** (non «In preparazione»). Eliminare il doppione «PROTOTIPO INTERATTIVO» / «PROVA INTERATTIVA» dal kicker, che resta solo con il nome della stanza.
- Nella topbar di Officina e Sala: etichetta *«Anteprima · Non pubblicata»*, come nell’indice.
- La pagina dell’indice conserva ancora un `<dialog id="room-dialog">` e l’attributo `data-room-preview`, ora inutilizzati: dopo aver controllato `app.js`, rimuoverli.

**Verifica.** Nessun testo contiene «approvato»; le tre card hanno la stessa etichetta di stato.

---

## 5. P1 — Struttura e interazione

### Punto 4 — Titolo e immagini della parte alta

**Problema A — titolo dell’indice.** L’`<h1>` ha la classe `palace-accessible-title`. Se la classe lo nasconde e la nuova immagine non contiene testo, la pagina non ha un titolo visibile.
**Cosa fare.** Verificare a occhio a 375, 768 e 1440 px. Se l’`<h1>` è nascosto, renderlo **visibile in HTML** (sopra o sull’immagine, con contrasto AA). Non usare `visually-hidden` per l’unico titolo della pagina, a meno che non esista un titolo visibile equivalente.

**Problema B — caricamento.** Le immagini dell’hero in `banco-di-prova.html`, `officina-locale.html` e `sala-dei-confini.html` hanno `loading="lazy"` ma stanno nella parte alta della pagina, e questo ritarda la loro comparsa.
**Cosa fare.** Rimuovere `loading="lazy"` e usare `fetchpriority="high"` (una sola per pagina) con `decoding="async"`. Il lazy resta per le immagini sotto la piega.

**Problema C — pesi.** Verificare il peso di `palazzo-stendardi-manzo.webp`, dell’altra immagine usata nel Banco, del poster `hero-palazzo-futuristico.webp` e di `filmato-concept.mp4`. Obiettivo indicativo: immagini sotto circa 250 KB. Il video resta con `preload="none"`, ha sempre il controllo di pausa e non deve dipendere dall’audio.

**Verifica.** Il titolo è visibile e selezionabile; l’immagine dell’hero compare subito; i pesi sono annotati nelle note.

### Punto 5 — Officina locale: la pagina quasi non reagisce

**Problema.** Dopo la diagnosi (che dà un confronto), il costruttore della skill e i sei test sono moduli di appunti: nulla risponde. Inoltre il protocollo richiede tre ripetizioni per messaggio, mentre la tabella registra un solo esito per test e versione.

**Cosa fare — 5a. Mini simulatore «Le regole fisse al lavoro».** Nuovo blocco nel capitolo 01 (Diagnosi), dopo il confronto con la chiave. Non usa alcun modello: mostra cosa fanno regole deterministiche con il listino fittizio.

Input:
- prodotti e quantità (dal listino della scheda);
- giorni di anticipo con cui arriva l’ordine (stesso giorno, 1, 2, 3 o più);
- ora di arrivo dell’ordine;
- giorno e ora di ritiro.

Output, ognuno con etichetta testuale **Rispettata / Non rispettata** (non solo colore):
- **Totale** calcolato dal listino.
- **Ordine entro le 18:00 del giorno prima** (regola 1).
- **Ritiro tra le 7:30 e le 13:00** e **non di lunedì** (regola 2).
- **Torte con 48 ore di anticipo** (regola 3), con la semplificazione dichiarata *«qui si usano due giorni di calendario»*.

Chiusura del blocco, in evidenza: *«Questa parte non usa nessun modello: sono regole fisse. Ora prova a scrivere a mano, in un modulo, il messaggio «ciao! domani passo verso le 8, mi tieni due pani grandi e una focaccia?». Il linguaggio informale è un problema diverso.»* Il testo di esempio può essere collegato al test T1.

**5b. Tre ripetizioni.** Nella tabella dei sei test, per ogni test e per ciascuna versione (v1, v2) prevedere **tre prove** (Prova 1, 2, 3) con scelta *Non provata / Senza errori / Con errore*. Riepilogo per versione: «n / 18 prove registrate», e per T6: *«Nessun errore registrato»* oppure *«Almeno un errore registrato»*. Il testo della pagina non dice mai che un test è «superato» o che la skill «funziona».

**Verifica.** Il simulatore calcola correttamente almeno questi tre casi: due pani casarecci e una focaccia = 23,00 €; ritiro di lunedì = non rispettata; torta ordinata il giorno prima = non rispettata. La tabella consente fino a 18 prove per versione.

### Punto 6 — Sala dei confini: manca il prima/dopo e un controllo di coerenza

**Problema.** Dopo gli incidenti l’utente non rivede le sue scelte e non vede cosa è cambiato, come invece avviene nel Banco di prova.

**Cosa fare — 6a. Prima/dopo.**
1. Al clic su «Mostra la mappa provvisoria» le classificazioni delle 12 azioni vengono congelate come **«Prima»**.
2. Nel passo 03, per ogni incidente l’utente indica l’azione coinvolta (menu con A1–A12) e può cambiarne il livello.
3. La **mappa finale** mostra per ogni azione: *Prima · Dopo · Cambiato*; un conteggio «n azioni modificate» (o «Nessuna azione modificata», senza giudizio); un campo facoltativo *«Cosa ti ha fatto cambiare idea?»*, solo in pagina.
4. Riusare lo stesso componente del Banco, se possibile.

**6b. Controlli di coerenza (informativi, non punteggi).**
- Azione «Con conferma» o «Solo umano» **senza responsabile** → avviso: *«Manca chi decide»*.
- Azione «Autonomo» con una di queste caratteristiche → avviso: *«Secondo la regola didattica di partenza di solito richiede conferma o è solo umana. Se la mantieni, scrivi perché.»*

Caratteristiche per l’avviso (**proposta da validare**: sono un’ipotesi, non una soluzione):

| Azione | Effetto esterno | Denaro | Difficile da annullare |
|---|---|---|---|
| A3 Inviare risposta senza revisione | Sì | — | Sì |
| A5 Cancellare un corso | — | — | Sì |
| A7 Inviare l’elenco iscritti a un docente esterno | Sì | — | Sì |
| A8 Incollare email in un servizio esterno | Sì | — | Sì |
| A9 Applicare uno sconto concordato a voce | — | Sì | — |
| A10 Registrare un pagamento | — | Sì | — |
| A11 Rispondere a una richiesta di rimborso | Sì | Sì | — |

Il testo dell’avviso cita la caratteristica concreta («effetto esterno», «denaro», «difficile da annullare»). **Nessuna azione è dichiarata «sbagliata»**: la pagina continua a dire che le valutazioni non sono corrette automaticamente.

**Verifica.** Cambiando un livello dopo gli incidenti, la mappa finale mostra Prima/Dopo e il conteggio. Un’azione gialla senza responsabile produce l’avviso.

### Punto 7 — Controllo della resa e dei fallback delle due nuove stanze

**Cosa fare (Fase 0 e QA).**
- Senza JavaScript, in Officina e Sala restano leggibili listino, regole, azioni, incidenti, esiti attesi e scheda integrale, e il `<noscript>` lo dice con onestà.
- Tutte le tabelle (listino, diagnosi, azioni, test) scorrono dentro il loro contenitore, senza scroll orizzontale della pagina a 375 px.
- Menu a tendina e radio sono usabili da tastiera e hanno etichette (nelle tabelle il `aria-label` c’è: verificare anche le righe generate da JS).

---

## 6. P2 — Dettagli e allineamento

### Punto 8 — Dettagli

1. **Campi numerici del registro (Banco):** i cinque campi sono obbligatori ma il testo dice «Lascia vuoto finché non hai controllato». Cambiare in: *«Inserisci 0 se non hai osservato errori di quel tipo.»*
2. **Domande guida degli incidenti (Sala):** iniziano con la minuscola («quale azione è coinvolta?»). Maiuscola iniziale e un’etichetta «Domande guida».
3. **Eyebrow della Sala e dell’Officina:** coerenti con il Banco (`LA STANZA DEI GIURATI · …`).
4. **Frase del Banco:** *«un giudizio può migliorare senza perdere dignità»* è enfatica: sostituire con *«un giudizio può migliorare quando incontra nuove prove»*.

### Punto 9 — Sorgenti rivisti: aggiornare le schede integrali

I file sorgente sono stati corretti:
- `MANZO_AI_Esperimento_03_Officina.md`: «Era necessario l’IA?» diventa «Era necessaria l’IA?»; nel «Prossimo passo» «Esperimento #01» e «#02» diventano **Banco di prova** e **Sala dei confini**.
- `MANZO_AI_Esperimento_02_Governo.md`: lo stesso allineamento dei rimandi.

Le copie integrali dentro `officina-locale.html` e `sala-dei-confini.html` («Testo fornito dall’autore, senza riscritture») vanno **rigenerate dai file aggiornati**, non modificate a mano. Il confronto con i sorgenti è un criterio di accettazione.

### Punto 10 — Coerenza di nomi

Nell’interfaccia visibile usare solo i nomi delle stanze (Officina locale, Banco di prova, Sala dei confini) e i passaggi del ciclo (Chiedi, Controlla, Decidi). I numeri «Esperimento #01–#03» restano solo nei nomi dei file e nei documenti di lavoro.

---

## 7. Fasi di lavoro

1. **Fase 0 — Ispezione (nessuna modifica).** Leggere `app.js`, `room-practices.js`, `rooms.css`, `styles.css`, `experiment-data.js`, immagini, video. Note su: `<h1>` visibile o nascosto, codice inutilizzato (dialog), pesi dei file, come viene calcolato il confronto del Banco e come è tenuto lo stato.
2. **Fase 1 — P0 (punti 1-3).**
3. **Fase 2 — P1.** Ordine: punto 4 → 5 → 6 → 7.
4. **Fase 3 — P2 (punti 8-10).**
5. **Fase 4 — QA** a 375, 768 e 1440 px, con tastiera, senza JavaScript e con `prefers-reduced-motion`.

A fine fase: riepilogo di cosa è cambiato, file modificati, punti dubbi. **Nessuna pubblicazione** senza conferma di Marcelo.

---

## 8. Criteri di accettazione

**Onestà e spoiler**
- [ ] Prima del passo 02, nessuna lacuna è leggibile nel registro; esiste il pulsante «Salta l’indagine…».
- [ ] Prima del confronto, nessun elemento visibile distingue il falso allarme dalle lacune.
- [ ] Nessun testo contiene «approvato» o «pilota approvato».
- [ ] Le tre card hanno lo stesso stato («Anteprima interattiva»).
- [ ] Nessuna pagina dichiara che un test è «superato» o che la skill «funziona».

**Contenuto**
- [ ] Le schede integrali coincidono con i sorgenti aggiornati.
- [ ] Il testo del simulatore dell’Officina dichiara che non usa alcun modello e la semplificazione delle 48 ore.
- [ ] Le caratteristiche della tabella del punto 6 sono presentate come regola didattica di partenza, non come soluzione.

**Interazione**
- [ ] Il simulatore calcola correttamente i tre casi del punto 5.
- [ ] L’Officina permette fino a 18 prove per versione.
- [ ] La Sala mostra Prima / Dopo / Cambiato e gli avvisi di coerenza.
- [ ] Nessun punteggio numerico né giudizio sulle scelte dell’utente.

**Tecnica e accessibilità**
- [ ] Titolo di ogni pagina visibile e selezionabile; un solo `<h1>`.
- [ ] Immagini hero senza lazy loading; pesi annotati.
- [ ] Controlli operabili da tastiera; avvisi con testo oltre al colore; contrasto AA.
- [ ] Nessuno scroll orizzontale a 375 px; nessuna parola spezzata nei titoli a 768 px.
- [ ] Senza JavaScript restano leggibili tutti i contenuti.
- [ ] Nessuna chiamata di rete, nessuna memorizzazione sul dispositivo.
- [ ] Tutti i link interni funzionano.

---

## 9. Decisioni aperte

| Tema | Proposta di partenza |
|---|---|
| Nascondere o mostrare il numero «8 lacune» nell’intestazione del Banco | Mostrarlo (è un obiettivo chiaro) |
| Caratteristiche delle azioni per gli avvisi della Sala | Tabella del punto 6, da validare |
| Semplificazione «48 ore = 2 giorni di calendario» | Accettata e dichiarata nella pagina |
| Testi dei messaggi di avviso | Bozza del harness, da approvare |
| Video concept | Mantenerlo facoltativo; ricontrollare peso e accessibilità |
| Pubblicazione del prototipo | Solo dopo la validazione di Marcelo |

---

## 10. Fuori ambito

- Collegamento a un modello AI reale.
- Versioni ES ed EN.
- Cambiamenti alla Home del sito principale.
- Analytics, cookie, account utente, salvataggio dei progressi.
- Compilazione dei risultati reali degli esperimenti.
- Rigenerazione dell’immagine dell’hero (già sostituita).
