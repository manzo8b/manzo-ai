# Brief di correzione — Prototipo «La stanza dei giurati» e «Banco di prova»

**Progetto:** MANZO AI · MARCELUS AI LAB · **Autore:** Marcelo Javier Fernandez Caballero
**Versione:** 1.0 · **Data:** 21 novembre 2026
**Destinatario:** harness di sviluppo (Codex / Claude Code)
**File in oggetto:** `index.html`, `banco-di-prova.html`, `assets/styles.css`, `assets/app.js`, `assets/experiment-data.js`, immagini in `assets/`

---

## 1. Contesto e obiettivo

Il prototipo privato (non pubblicato, `noindex`) funziona e rispetta già i principi di fondo: dati fittizi, nessun risultato inventato, nessuna API AI, registro che parte vuoto, chiave di risposta richiudibile.

Questo brief corregge **dieci punti** emersi dalla revisione e trasforma il Banco di prova da percorso guidato a **esperienza che si può completare dentro la pagina**, senza perdere il rigore.

**Nota importante:** la revisione è stata fatta sui soli due file HTML. `app.js`, `experiment-data.js`, `styles.css` e le immagini non sono stati letti. La Fase 0 serve a verificarne lo stato prima di modificare qualsiasi cosa.

---

## 2. Regole che non cambiano

1. **Nessun risultato inventato.** I risultati dell’esperimento reale restano vuoti finché non vengono inseriti dall’utente.
2. **Nessuna chiamata a servizi AI** e nessun servizio a pagamento. Solo HTML, CSS e JavaScript puro su GitHub Pages.
3. **Dati solo fittizi** e avviso visibile: *«Non caricare dati reali o riservati.»*
4. **Nessun tracciamento** e nessuna memorizzazione sul dispositivo (niente `localStorage`, `sessionStorage`, cookie). I dati restano nella memoria della pagina.
5. **`noindex,nofollow`** finché Marcelo non autorizza la pubblicazione.
6. **Il testo dei contenuti è fedele ai sorgenti** (`MANZO_AI_Progetto_Esperimenti.md`, sezione 7). Il confronto con i sorgenti è un criterio di accettazione.
7. **Ogni elemento sintetico è dichiarato come tale.** Il progetto insegna a verificare: non può presentare come reale ciò che è simulato o scritto da noi.

---

## 3. Priorità

| Priorità | Punti | Tema |
|---|---|---|
| **P0** | 1, 2, 3, 4 | Onestà dei testi e contenuto sempre leggibile |
| **P1** | 5, 6, 7, 8, 9, 10 | Esperienza interattiva e registro |
| **P2** | 11 | Dettagli, hero e accessibilità |

Ordine di lavoro: P0 → P1 → P2. Non iniziare P1 prima di aver chiuso P0.

---

## 4. P0 — Onestà e leggibilità

### Punto 1 — La chiave non è «non generata dall’AI»

**Problema.** In `banco-di-prova.html`, nel blocco della chiave: *«La chiave proviene dal documento originale e non è generata dall’AI»*. La chiave delle otto lacune è stata preparata con il supporto di un assistente AI e verificata dall’autore. L’affermazione è inesatta, in un progetto che insegna la verificabilità.

**Cosa fare.** Sostituire con:
> La chiave è stata preparata prima dei test e non dipende dalle risposte di alcun modello.

Cercare nel codice altre formule che attribuiscano o neghino l’origine AI di contenuti e correggerle con lo stesso criterio (dire cosa si sa, non cosa suona bene).

**Verifica.** Nessuna ricorrenza di «non generata dall’AI» o simili in tutti i file.

### Punto 2 — «Ogni luce ha un significato»

**Problema.** In `index.html`, la didascalia sotto l’immagine dice: *«Ogni luce ha un significato — I collegamenti visualizzano il percorso tra ipotesi, prove e decisioni: non simulano un cervello artificiale»*. Le luci dell’immagine sono decorazione generata e non rappresentano nulla.

**Cosa fare.**
- Titolo didascalia: **Illustrazione di fantasia**
- Testo: *Le luci sono solo decorative. Il metodo si vede nell’esperimento.*
- Rivedere gli `alt` delle immagini: dove l’immagine è decorativa usare `alt=""`; altrimenti una descrizione neutra («Illustrazione decorativa di una sala con tavolo e tre archi»). Eliminare formule come «connessioni luminose tra le prove».
- Verificare che l’etichetta «AULA DELLE PROVE ↗» sull’immagine del Banco di prova non prometta un ambiente che non esiste.

**Verifica.** Nessun testo sull’indice o sul Banco afferma che elementi puramente decorativi abbiano un significato.

### Punto 3 — Riferimento interno visibile

**Problema.** Nel fascicolo: *«Fonte integrale: Progetto Esperimenti, §7.3»*. Rimanda a un file che il visitatore non ha.

**Cosa fare.** Sostituire con: *«Documento fittizio preparato per questo esperimento»*. Cercare altri riferimenti interni (nomi di file, «§», «sorgente») nei testi visibili e rimuoverli.

### Punto 4 — Senza JavaScript il cuore dell’esperimento non esiste

**Problema.** Il testo del preventivo (`#source-document`: «Caricamento del documento sorgente…»), le richieste A e B (`#prompt-a`, `#prompt-b`), le opzioni delle lacune e la chiave vengono tutti caricati da `experiment-data.js`. Il `<noscript>` dichiara però che «il percorso resta leggibile senza JavaScript».

**Cosa fare.**
1. **Fonte unica = HTML.** Scrivere nel markup: il preventivo, le richieste A e B, l’elenco delle lacune con la chiave (dentro `<details>`), il box «falso allarme». `app.js` legge questi contenuti dal DOM per i pulsanti «Copia» e per la valutazione, non il contrario.
2. Se `experiment-data.js` resta necessario per i dati di valutazione (id delle lacune, mappature), deve contenere **solo dati**, non testi visibili duplicati.
3. Senza JavaScript tutto il testo è leggibile; le parti interattive (selezione, rete, registro, copia) mostrano un messaggio onesto, per esempio: *«Per selezionare, confrontare e registrare le prove serve JavaScript. Il documento, le richieste e la chiave sono leggibili qui sotto.»*
4. Correggere il testo del `<noscript>` di conseguenza.

**Verifica.** Con JavaScript disattivato si legge integralmente: documento, richieste A e B, chiave, limiti.

---

## 5. P1 — Esperienza e registro

### Struttura della pagina dopo le correzioni

Il Banco di prova si organizza in due parti, per far capire che il valore non sta solo fuori dalla pagina:

- **Parte 1 — Allena l’occhio (tutto dentro la pagina):** leggi il documento → cerca le lacune → metti alla prova un riassunto di esempio → osserva la rete → rivedi la tua decisione.
- **Parte 2 — Prova su un assistente reale (fuori dalla pagina):** confronto A/B, registro delle prove, verdetto.

La sidebar «Percorso di prova» riflette le due parti.

### Punto 5 — La rete delle prove deve rappresentare affermazioni e fonti

**Problema.** Oggi la rete mostra le 8 lacune come nodi che si accendono quando l’utente le seleziona, con legenda «Individuata / Non selezionata». È un contatore con forma di rete: i collegamenti non significano nulla.

**Cosa fare.** La rete diventa la rappresentazione del passo «Metti alla prova un riassunto» (punto 7):
- **Nodi a sinistra:** le affermazioni del riassunto di esempio.
- **Nodi a destra:** le sezioni del preventivo (Oggetto, Lavori compresi, Importo, Materiali, Tempi, Pagamento, Garanzia, Validità).
- **Collegamento:** per ogni affermazione l’utente indica la sezione che la sostiene.
  - Linea piena = affermazione collegata a una fonte.
  - Linea tratteggiata che termina nel vuoto = «nessuna fonte nel testo».
- **Dopo il confronto con la chiave:** ogni collegamento mostra se è corretto, con **etichetta testuale** oltre al colore («Supportata», «In parte», «Non supportata»).
- **La rete è solo visualizzazione.** I controlli reali sono elementi di form (vedi punto 7), operabili da tastiera. L’SVG è `aria-hidden` o ha un testo alternativo riassuntivo aggiornato (es. «3 affermazioni non supportate su 8»).
- L’attuale «Atlante delle incertezze» con le 8 lacune viene **sostituito**. Le 8 lacune restano nel passo 02 come elenco da spuntare.

**Verifica.** Ogni linea della rete corrisponde a una scelta effettiva dell’utente. Nessun elemento della rete è puramente ornamentale.

### Punto 6 — Il momento «cambio idea» (prima / dopo)

**Problema.** Dopo «Confronta con la chiave» non c’è un passo che chieda di rivedere la propria scelta.

**Cosa fare.**
1. Al clic su «Confronta con la chiave», le risposte dell’utente vengono congelate come **«Prima»**.
2. Compare la chiave. L’utente può **modificare** le proprie risposte («Dopo»).
3. Un riepilogo mostra, per ogni affermazione: *Prima · Dopo · Chiave*, e il conteggio delle risposte cambiate.
4. Campo facoltativo: *«Cosa ti ha fatto cambiare idea?»* (testo libero, solo in pagina, non salvato).
5. Il riepilogo prima/dopo entra nella scheda di audit copiabile (punto finale del percorso).

**Verifica.** Se l’utente non cambia nulla, il riepilogo lo dice senza giudizio («Nessuna risposta modificata»).

### Punto 7 — Riassunto di esempio per completare un’esperienza dentro la pagina

**Problema.** L’esperienza vera avviene fuori: copiare richieste, usarle 10 volte altrove, tornare a inserire numeri. Molti visitatori si fermeranno ai primi passi, che oggi sono i meno coinvolgenti.

**Cosa fare.** Aggiungere il passo **«Metti alla prova un riassunto»** con un riassunto **scritto da noi**, con questa dichiarazione ben visibile in testa:

> Questo riassunto è un esempio scritto per questo esperimento. Non è la risposta di un modello AI.

**Il riassunto di esempio (8 affermazioni, testi da usare così come sono):**

| ID | Affermazione | Sezione del preventivo | Esito atteso | Lacuna collegata |
|---|---|---|---|---|
| R1 | Il preventivo comprende demolizione dei rivestimenti, rifacimento dell’impianto idrico, fornitura e posa dei sanitari e posa dei rivestimenti. | Lavori compresi | Supportata | — |
| R2 | L’importo è di 4.800 euro più IVA e comprende manodopera e materiali di consumo. | Importo | Supportata | — |
| R3 | L’IVA è al 22%, quindi il totale è di 5.856 euro. | nessuna | Non supportata | L1 |
| R4 | I lavori durano circa due settimane dall’inizio del cantiere. | Tempi | Supportata | — |
| R5 | La garanzia dura 24 mesi. | nessuna (il testo dice solo «come previsto dalla legge») | Non supportata | L4 |
| R6 | Il pagamento prevede un acconto del 30% alla firma e il saldo a fine lavori. | Pagamento | In parte (la struttura sì, il 30% no) | L3 |
| R7 | Lo smaltimento delle macerie è compreso nel prezzo. | nessuna | Non supportata | L7 |
| R8 | Il preventivo è valido 30 giorni. | Validità | Supportata | — (controllo: non è una lacuna) |

**Interazione.** Per ogni affermazione:
- gruppo di scelta (radio): **Supportata dal testo / In parte / Non supportata**;
- se la scelta non è «Non supportata», un menu a tendina con le sezioni del preventivo;
- la rete (punto 5) si aggiorna a ogni scelta.

**Dopo il confronto:** per ogni affermazione, messaggio breve con la ragione (es. per R3: *«Il testo non indica l’aliquota IVA: 22% e 5.856 euro non sono nel documento.»*) e il rimando alla lacuna L1–L8 corrispondente.

**Parte 2 resta facoltativa e dichiarata come avanzata:** *«Se vuoi, ripeti la prova con un assistente reale»*.

**Verifica.** Un visitatore può completare la Parte 1 senza uscire dalla pagina e senza JavaScript esterni.

### Punto 8 — Mancano le definizioni degli errori

**Problema.** Il modulo chiede «Dati inventati», «Omissioni critiche», «Generalizzazioni indebite», «Inferenze non autorizzate», ma la pagina non spiega cosa significano.

**Cosa fare.** Aggiungere accanto al modulo un blocco richiudibile **«Come classificare gli errori»** con questo contenuto (invariato):

| Classe | Definizione | Esempio sul documento di prova |
|---|---|---|
| Dato inventato | Introduce cifre, date, nomi o norme assenti dal testo | «IVA al 22%», «garanzia di 24 mesi» |
| Omissione critica | Non segnala una lacuna che cambia la decisione del cliente | Riassume senza dire che l’IVA manca |
| Generalizzazione indebita | Trasforma un dettaglio in regola generale | «Tutti i materiali sono inclusi» |
| Inferenza non autorizzata | Deduce una conseguenza non scritta | «Il saldo è dovuto entro 30 giorni dalla fine lavori» |

**Rischio:** **Alto** se riguarda importo, pagamento o responsabilità · **Medio** se riguarda tempi o garanzia · **Basso** se riguarda dettagli secondari.

**Verifica.** Il blocco è raggiungibile da tastiera e il campo del modulo rimanda ad esso con un link.

### Punto 9 — Il modulo di registro fa fare i conti a mano

**Problema.** Il campo «Lacune individuate / 8» è un numero digitato.

**Cosa fare.**
- Sostituirlo con **8 caselle da spuntare (L1–L8)**, con etichetta breve per ciascuna; il numero è calcolato dalla pagina e mostrato come «n / 8».
- Le altre quattro classi di errore e i falsi allarmi restano numeri con pulsanti − / + e valore minimo 0.
- Il registro delle prove mostra, per ogni prova, quali lacune sono state spuntate.
- Il pulsante «Svuota il modulo» non cancella le prove già registrate.

**Verifica.** Il valore «Lacune individuate» non è più digitabile a mano; è sempre coerente con le caselle.

### Punto 10 — Il limite di 5 prove non lascia spazio al secondo modello

**Problema.** Il protocollo dell’Esperimento #01 consiglia almeno due modelli. Il modulo dice «Massimo 5 prove per richiesta» e il contatore «0 / 10 prove».

**Cosa fare.**
- Il limite diventa **5 prove per ciascuna combinazione modello + richiesta** (A e B), con un massimo di **3 modelli**.
- I nomi dei modelli sono normalizzati (rimozione di spazi, maiuscole irrilevanti) per raggruppare le prove.
- Il riepilogo A/B è mostrato **per modello**, mai mescolando modelli diversi.
- Il contatore diventa «n / 10 prove per questo modello».
- La cautela *«Non è possibile concludere quale richiesta sia più affidabile prima di avere completato e verificato tutte le prove previste»* resta, e si applica per modello.

**Verifica.** Con due modelli si possono registrare fino a 20 prove, e il riepilogo non somma i modelli.

---

## 6. P2 — Dettagli, hero e accessibilità

### Punto 11 — Elenco dei dettagli

1. **Doppia numerazione sulle card dell’indice.** Ogni card mostra «01 / CHIEDI» e «ESP / 03»: due sistemi di numerazione. Tenere **solo la posizione nel ciclo** (Chiedi, Controlla, Decidi). Rimuovere «ESP / 0X» dall’interfaccia visibile, anche dall’eyebrow del Banco (`… / CONTROLLA / ESP 01` → `… / CONTROLLA`). L’ordine delle card resta quello del ciclo.
2. **«EXPERIMENTAL LAB»** in inglese: sostituire con «Laboratorio» o «Laboratorio sperimentale».
3. **Elemento `<icon>` non valido** in `index.html` (blocco `palace-caption-copy`): sostituire con `<span>`.
4. **Hero dell’indice.** L’immagine contiene titolo, sottotitolo, bottone, logo e breadcrumb **dentro l’immagine**, e un link trasparente la ricopre; l’`<h1>` vero è nascosto. Su mobile il testo è illeggibile, non selezionabile e duplica la topbar. Cosa fare:
   - **Intervento immediato (soluzione provvisoria):** l’`<h1>` e il testo introduttivo diventano visibili in HTML sopra l’immagine; l’immagine è decorativa (`alt=""`); eliminare il link trasparente e tenere come CTA solo il bottone reale «Attraversa le porte». Per nascondere il testo inciso, ritagliare l’immagine con `object-fit: cover` e `object-position` sulla fascia centrale con tavolo e archi, **verificando a occhio** su 375, 768 e 1440 px.
   - **Intervento definitivo:** sostituire l’immagine con una versione **senza alcun testo** (vedi appendice D), in orizzontale e in verticale per mobile.
5. **Immagine del Banco** (`stanza-dei-giurati.webp`): se contiene testo inciso, stesse regole del punto 4; aggiungere `loading="lazy"` e `decoding="async"`; verificare il peso (obiettivo indicativo: sotto 250 KB per immagine, con `srcset` se serve).
6. **Contrasto e colore:** stati («Individuata», «Supportata», «Non supportata», livelli di rischio) sempre con etichetta testuale, contrasto AA, anche nel testo piccolo sull’immagine e negli stati del form.
7. **Movimento:** rispettare `prefers-reduced-motion` per la rete e per qualunque animazione.

---

## 7. Fasi di lavoro

1. **Fase 0 — Ispezione (nessuna modifica).** Leggere `app.js`, `experiment-data.js`, `styles.css`, le immagini e le funzioni di valutazione, copia e reset. Scrivere un file di note con: cosa c’è, cosa si rompe senza JavaScript, dove vive ogni testo, dimensioni delle immagini, eventuali ripetizioni di formule da correggere (punti 1-3).
2. **Fase 1 — P0 (punti 1-4).**
3. **Fase 2 — P1.** Ordine: punto 8 (definizioni) → 9 e 10 (registro) → 7 (riassunto di esempio) → 5 (rete) → 6 (prima/dopo).
4. **Fase 3 — P2 (punto 11).**
5. **Fase 4 — QA** (sezione 8) a 375, 768 e 1440 px.

A fine fase: riepilogo di cosa è cambiato, file modificati, punti dubbi. **Nessuna pubblicazione** senza conferma di Marcelo.

---

## 8. Criteri di accettazione

**Onestà**
- [ ] Nessuna formula che neghi o attribuisca un’origine AI ai contenuti.
- [ ] Il riassunto di esempio è dichiarato come scritto da noi, in testa e nella scheda di audit.
- [ ] Nessun testo afferma che elementi decorativi abbiano un significato.
- [ ] Nessun riferimento interno (file, «§») nei testi visibili.
- [ ] Nessun valore di risultato precompilato.

**Contenuto**
- [ ] Il testo del preventivo, le richieste A e B, la chiave e le definizioni degli errori coincidono con i sorgenti (confronto riga per riga; differenze solo di formattazione).
- [ ] Senza JavaScript sono leggibili documento, richieste, chiave e limiti, e il `<noscript>` è veritiero.

**Esperienza**
- [ ] La Parte 1 si completa interamente nella pagina.
- [ ] La rete disegna solo collegamenti scelti dall’utente; non esistono nodi ornamentali.
- [ ] Il riepilogo prima / dopo / chiave è presente e funziona anche se l’utente non cambia nulla.
- [ ] Le 8 lacune nel registro sono caselle da spuntare, con numero calcolato.
- [ ] Il registro supporta fino a 3 modelli, 5 prove per modello e richiesta, riepilogo separato per modello.

**Accessibilità e tecnica**
- [ ] Tutti i controlli si usano da tastiera; la rete non è l’unico modo di rispondere.
- [ ] Stati e livelli sempre con etichetta testuale; contrasto AA.
- [ ] `prefers-reduced-motion` rispettato.
- [ ] Nessuna parola spezzata nei titoli a 768 px; nessuno scroll orizzontale a 375 px.
- [ ] Il titolo dell’indice è testo HTML visibile e selezionabile, non parte dell’immagine.
- [ ] Nessuna dipendenza esterna, nessuna chiamata di rete, nessuna memorizzazione sul dispositivo.
- [ ] Tutti i link interni funzionano.

---

## 9. Decisioni aperte

| Tema | Proposta di partenza |
|---|---|
| Sostituire l’«Atlante delle incertezze» con la rete affermazioni-fonti | Sì, come descritto al punto 5 |
| Immagine dell’indice | Provvisoria con ritaglio; definitiva senza testo (appendice D) |
| Testi dei messaggi dopo il confronto (R1–R8) | Bozza del harness, da approvare |
| Quantità di modelli nel registro | Massimo 3 |
| Punteggio complessivo della Parte 1 | Nessun punteggio numerico: solo prima/dopo e rimando alle lacune |
| Pubblicazione del prototipo | Solo dopo la validazione di Marcelo |

---

## 10. Fuori ambito

- Collegamento a un modello AI reale o a un servizio a pagamento.
- Prototipi di Officina locale e Sala dei confini.
- Versioni ES ed EN.
- Cambiamenti alla Home del sito principale.
- Analytics, cookie, account utente, salvataggio dei progressi.
- Compilazione dei risultati reali dell’esperimento.

---

## Appendice A — Sostituzioni di testo (copia esatta)

| Dove | Prima | Dopo |
|---|---|---|
| Blocco chiave (Banco) | La chiave proviene dal documento originale e non è generata dall’AI | La chiave è stata preparata prima dei test e non dipende dalle risposte di alcun modello |
| Fascicolo, piè di pagina | Fonte integrale: Progetto Esperimenti, §7.3 | Documento fittizio preparato per questo esperimento |
| Indice, didascalia | Ogni luce ha un significato — I collegamenti visualizzano il percorso tra ipotesi, prove e decisioni: non simulano un cervello artificiale | **Illustrazione di fantasia** — Le luci sono solo decorative. Il metodo si vede nell’esperimento |
| Topbar | EXPERIMENTAL LAB | Laboratorio |
| `<noscript>` | Il percorso resta leggibile senza JavaScript; per utilizzare la rete delle prove e il registro manuale occorre attivarlo nel browser | Per selezionare, confrontare e registrare le prove serve JavaScript. Il documento, le richieste e la chiave restano leggibili in questa pagina |
| Eyebrow Banco | LA STANZA DEI GIURATI / CONTROLLA / ESP 01 | LA STANZA DEI GIURATI / CONTROLLA |

## Appendice B — Dati del riassunto di esempio

Vedi tabella al punto 7. Le affermazioni R1–R8 e gli esiti attesi sono la **chiave** della Parte 1: vanno inseriti nel codice come dati (id, testo, sezione corretta, esito, lacuna collegata), con i testi visibili scritti nell’HTML.

## Appendice C — Etichette brevi per le 8 lacune (spunte del registro)

| ID | Etichetta |
|---|---|
| L1 | Aliquota IVA non indicata |
| L2 | Data di inizio lavori non indicata |
| L3 | Importo o percentuale dell’acconto non indicati |
| L4 | Durata e termini della garanzia non specificati |
| L5 | «Materiali di consumo» non definiti |
| L6 | Importo massimo per sanitari e rivestimenti non definito e non chiaro se incluso |
| L7 | Smaltimento delle macerie non menzionato |
| L8 | Penali o conseguenze di ritardo non menzionate |

## Appendice D — Prompt per rigenerare l’immagine dell’hero (senza testo)

Da usare con un generatore di immagini. Produrre due versioni: orizzontale 16:9 e verticale 4:5.

```text
Wide interior of a calm, modern deliberation hall: a round table at the center
with scattered paper documents, one document under a large magnifying glass with
a few lines highlighted, and two sheets placed side by side for comparison.
Behind the table, three arched doorways: one lit by warm amber light, one by
clear electric blue, one by soft violet. Clean, bright, architectural look,
natural daylight, white and pale-blue walls, small orange accents, teal details.
No neon, no holograms, no glowing orbs, no futuristic circuitry, no flags.
ABSOLUTELY NO TEXT: no letters, no numbers, no logos, no signs, no screens with
readable content. Keep the upper 25% of the image calm and uncluttered so that
HTML text can be placed over it. Photographic-illustration style, soft shadows,
high detail, sharp focus.
```

Dopo la generazione: verificare a occhio che non compaiano lettere o numeri leggibili, ridurre il peso e produrre il file in formato WebP.
