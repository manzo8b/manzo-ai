# Brief per il harness — La stanza dei giurati

**Progetto:** MANZO AI (https://manzo8b.github.io/manzo-ai/) · **Autore:** Marcelo Javier Fernandez Caballero · MARCELUS AI LAB
**Versione:** 1.0 · **Data:** 20 novembre 2026
**Destinatario:** harness di sviluppo (Codex / Claude Code)

---

## 1. Obiettivo

Creare nel sito la sezione **La stanza dei giurati** (sottotitolo: *Esperimenti*), una pagina indice con tre schede di esperimento e un punto d’ingresso nella Home italiana. I contenuti sono già scritti: il lavoro è **impaginarli**, non riscriverli.

**Fonti dei contenuti (da aggiungere al repository come sorgente, senza modificarle):**

| File | Contenuto |
|---|---|
| `MANZO_AI_Progetto_Esperimenti.md` | Progetto completo; la sezione 7 contiene l’**Esperimento #01** (Banco di prova) |
| `MANZO_AI_Esperimento_02_Governo.md` | **Esperimento #02** (Sala dei confini) |
| `MANZO_AI_Esperimento_03_Officina.md` | **Esperimento #03** (Officina locale) |

Il file del progetto serve da riferimento. Nel sito vanno pubblicate **le tre schede**, non l’intero progetto.

---

## 2. Cosa NON cambia

- La Home italiana v2 già approvata, tranne il punto 6 di questo brief.
- Gli URL esistenti e il selettore lingua IT / ES / EN.
- Il sistema visivo delle card (header colorato con codice, titolo, tag, CTA) e i colori esistenti.
- Il tono rigoroso e verificabile del progetto.

---

## 3. Regole di contenuto (vincolanti)

1. **Testo fedele ai file sorgente.** Non riscrivere, riassumere o «migliorare» i testi. Si possono correggere solo refusi evidenti, segnalandoli in un file di note.
2. **Nessun dato inventato.** Livello e tempo stimato sono `[da definire]` nei sorgenti: non vanno sostituiti con valori. Nella scheda si mostra «Da definire».
3. **Nessun risultato inventato.** Le schede risultati restano da compilare. Nella pagina compaiono come **modelli vuoti** con la dicitura «Risultati in arrivo».
4. **Fonti normative dell’Esperimento #02:** nel sorgente c’è un segnaposto. Finché non sono inserite, la scheda #02 ha stato **In preparazione** e non si presenta come completa.
5. **Avviso sui dati fittizi** visibile in cima a ogni scheda: *«Non caricare dati reali o riservati.»*
6. **Nessuna promessa di certificazione** e nessun testo che suoni come consulenza legale.
7. **Il nome della sezione e delle tre stanze sta in un solo punto** (costante o file di configurazione), perché la verifica di marchio è ancora da fare e il nome potrebbe cambiare. Nessun nome hardcoded in più file.

---

## 4. Architettura della pagina indice

**Collocazione:** dentro *Laboratorio*, nella sezione *Pratica* del menu. Percorso indicativo: `/it/laboratorio/stanza-dei-giurati/` (**verificare** la struttura reale del repository e seguire le convenzioni esistenti).

### 4.1 Blocchi

1. **Intestazione**
   - Eyebrow: *Laboratorio · Esperimenti*
   - Titolo: **La stanza dei giurati**
   - Sottotitolo: *Esperimenti per imparare a dubitare bene*
   - Testo breve (manifesto): *Dalla teoria alla prova. Esperimenti replicabili per imparare a chiedere meglio, controllare le risposte e decidere con criterio.*
2. **Il ciclo in tre passi** (una riga, non una sezione pesante): Chiedi → Controlla → Decidi, ciascuno collegato alla stanza corrispondente.
3. **Tre card** (una per esperimento), nell’ordine di pubblicazione: #01, #03, #02.
4. **Come funziona un esperimento** (box breve): dati fittizi, metodo dichiarato, risultati e limiti pubblicati, nessuna certificazione. Fonte: sezione 2 del progetto.
5. **Link** a Laboratorio e Academy.

La pagina resta corta: al massimo tre schermate su desktop.

### 4.2 Le tre card (stesso componente delle card della Home)

| Codice | Stanza | Titolo | Domanda gancio | Stato | Destinazione |
|---|---|---|---|---|---|
| ESP / 01 | Banco di prova | Stress-test su un preventivo | Quanto regge un assistente IA prima di inventare? | In preparazione | scheda #01 |
| ESP / 03 | Officina locale | Sfida di quartiere | Serve davvero l’IA per risolvere questo problema? | In preparazione | scheda #03 |
| ESP / 02 | Sala dei confini | La mappa dei confini | Fino a dove può agire un’IA senza una persona? | In preparazione | scheda #02 |

**Regole delle card**
- Stessa anatomia della Home: header colorato con codice, tipo («Esperimento»), domanda gancio, titolo, massimo due tag, CTA «Apri l’esperimento».
- Un colore per stanza, scelto tra quelli già in uso nel sito. Il colore non basta mai da solo: stato e stanza hanno sempre etichetta testuale.
- **Stato** visibile come badge testuale: *In preparazione*, *In corso*, *Concluso*, *Replicato*. Valore letto dai metadati di ogni scheda.
- Livello e durata: campo previsto, mostrato come «Da definire» finché vuoto.
- Illustrazione di header: icona SVG leggera per stanza (bilancia o lente per il Banco di prova, schema a livelli per la Sala dei confini, ingranaggio o chiave per l’Officina). Decorativa e nascosta agli screen reader.

---

## 5. Template della pagina di esperimento

Ogni scheda segue i **5 blocchi** definiti nel progetto. Nei sorgenti i titoli di sezione sono già numerati e vanno mantenuti nell’ordine.

| Blocco | Sezione nel sorgente |
|---|---|
| 1. Scheda | «Scheda» (tabella con laboratorio/stanza, obiettivo, formato, livello, tempo, lingue, stato, avviso) |
| 2. Domanda e ipotesi | «Domanda e ipotesi» |
| 3. La prova | «La prova» (scenario, materiali, procedura, rubrica) |
| 4. Risultati e limiti | «Risultati e limiti» (scheda risultati vuota + limiti) |
| 5. Cosa porti via | «Cosa porti via» (artefatto, checklist, prossimo passo) |

### 5.1 Impaginazione

- **Blocco 1 «above the fold»:** titolo, domanda in grande, stanza, stato, avviso sui dati fittizi, bottone «Inizia l’esperimento» che porta al blocco 3.
- **Indice laterale o in cima** con i cinque blocchi, per spostarsi rapidamente (ancore, navigabile da tastiera).
- **Tabelle:** responsive, con `overflow-x: auto` dentro un contenitore proprio. Nessuno scroll orizzontale della pagina. Intestazioni di colonna semantiche (`<th scope>`).
- **Blocchi di codice** (prompt, documenti di prova): contenitore con sfondo distinto e **pulsante «Copia»** accessibile (etichetta testuale, annuncio «Copiato» per screen reader). È la funzione più utile per #01 e #03, dove si copiano prompt e messaggi di prova.
- **Chiave di risposta dell’Esperimento #01:** mostrata in un blocco **richiudibile** («Mostra la chiave di risposta»), chiuso di default, perché va letta dopo la prova. Usare `<details>` nativo.
- **Checklist** (`- [ ]`): rese come elenco statico con segno di spunta decorativo. Niente stato salvato, nessun JavaScript.
- **Test dell’#03:** la tabella dei sei messaggi con «Esito atteso» resta visibile; il test T6 (sicurezza) è evidenziato con etichetta testuale «Obbligatorio».
- **Livelli dell’#02** (Autonomo / Con conferma / Solo umano): sempre con etichetta testuale oltre al colore, contrasto AA.

### 5.2 Navigazione tra esperimenti

In fondo a ogni scheda: «Prossimo passo nel ciclo», con link alle altre due stanze e ai corsi collegati già presenti nei sorgenti. Verificare che ogni link punti a una pagina esistente; se non esiste, mostrare il testo senza link e annotarlo.

---

## 6. Home: punto d’ingresso

Il blocco 5 della Home v2 (la sfida di pensiero critico) diventa un **blocco doppio**:

| Card sinistra | Card destra |
|---|---|
| **Sfida di pensiero critico** (contenuto già esistente, invariato) | **La stanza dei giurati** |

**Card destra (testo proposto):**
- Eyebrow: *Esperimenti*
- Titolo: **Entra nella stanza dei giurati**
- Testo: *Prova a mettere alla prova una risposta dell’IA, con casi fittizi e un metodo che puoi ripetere.*
- CTA: **Entra**

**Vincoli**
- La Home resta a sei blocchi e a circa tre schermate su desktop.
- Su mobile le due card si impilano; la CTA primaria dell’hero resta visibile.
- Nessun altro punto della Home cambia.

**Nota:** se il blocco doppio rende la Home troppo densa, in alternativa si sostituisce la sfida con la card della stanza e la sfida resta raggiungibile dal menu. Decide Marcelo dopo aver visto una anteprima.

---

## 7. Menu e sidebar

- **Sidebar (sezione Pratica):** aggiungere la voce *La stanza dei giurati* subito sotto *Laboratorio*, solo nella versione italiana.
- **ES ed EN:** la voce compare con la nota «Disponibile in italiano», come già fatto per l’AI Teaching Lab. Nessuna pagina ES/EN per ora.
- Nessuna modifica alle altre voci.

---

## 8. Vincoli tecnici

- **Hosting:** GitHub Pages, sito statico. Nessuna nuova dipendenza né build tool senza autorizzazione.
- **Prima di scrivere codice:** ispezionare il repository e descrivere in un file di note come sono costruite oggi pagine, card e menu. Riusare i componenti esistenti.
- **Conversione dei sorgenti:** se il sito non ha già una pipeline Markdown → HTML, convertire i tre file in pagine HTML statiche con una piccola procedura documentata. Non incollare a mano.
- **URL:** nessun URL esistente cambia. Nuovi URL in italiano, minuscolo, con trattini.
- **Performance:** niente librerie di animazione né font esterni nuovi. Icone in SVG inline. Rispettare `prefers-reduced-motion`.
- **SEO:** un solo H1 per pagina, `title` e `meta description` propri, Open Graph coerente. Attributo `lang="it"`.
- **Accessibilità:** navigazione completa da tastiera, contrasto AA, testi dei link comprensibili fuori contesto, immagini decorative con `alt` vuoto, pulsanti «Copia» con etichetta.
- **Stile di scrittura già adottato:** titoli senza punto finale e apostrofi tipografici (’).

---

## 9. Fasi di lavoro

1. **Fase 0 — Ispezione.** Note sulla struttura del repository, sui componenti riusabili e sugli URL toccati. Nessuna modifica.
2. **Fase 1 — Esperimento #01.** Pagina completa con tutti i componenti (tabelle, copia, chiave richiudibile). Serve da modello.
3. **Fase 2 — Pagina indice e card.** Card nello stile della Home, badge di stato, indice del ciclo.
4. **Fase 3 — Esperimenti #03 e #02.** Riuso degli stessi componenti.
5. **Fase 4 — Home e menu.** Blocco doppio e voce di sidebar (sezioni 6 e 7).
6. **Fase 5 — QA.** Controlli della sezione 10 su 375, 768 e 1440 px, in IT; verifica del comportamento di ES ed EN.

A fine di ogni fase: riepilogo di cosa è cambiato, file modificati, punti dubbi. **Nessuna pubblicazione** finché Marcelo non convalida.

---

## 10. Criteri di accettazione

- La pagina indice e le tre schede sono raggiungibili da Home e menu, in italiano.
- Il testo delle schede coincide con i sorgenti (confronto riga per riga; differenze solo di formattazione).
- Nessun valore di livello, tempo o risultato inventato; i campi vuoti mostrano «Da definire» o «Risultati in arrivo».
- L’avviso sui dati fittizi è visibile in cima a ogni scheda.
- Le tabelle non provocano scroll orizzontale della pagina a 375 px.
- I pulsanti «Copia» funzionano da tastiera e annunciano l’esito.
- La chiave di risposta dell’#01 è chiusa di default.
- Livelli e stati hanno etichetta testuale oltre al colore; contrasto AA.
- Un solo H1 per pagina; nessuna parola spezzata a 768 px nei titoli.
- Nomi di sezione e stanze definiti in un unico punto del codice.
- Tutti i link interni rispondono; nessun URL esistente è rotto.
- La Home resta a sei blocchi e a circa tre schermate su desktop.
- ES ed EN: voce di menu con nota «Disponibile in italiano», nessuna pagina rotta.

---

## 11. Decisioni aperte

| Tema | Proposta di partenza |
|---|---|
| Nome definitivo di sezione e stanze | Quelli in questo brief, ma centralizzati; verifica di marchio (UIBM, EUIPO) ancora da fare |
| Livello e tempo stimato | «Da definire» finché non verificati |
| Fonti normative dell’#02 | Da inserire prima di togliere lo stato «In preparazione» |
| Home: blocco doppio o sostituzione | Blocco doppio; decide Marcelo su anteprima |
| Artefatti scaricabili (PDF o Markdown) | Fase successiva, fuori da questo brief |
| Traduzioni ES ed EN | Dopo la validazione dell’italiano |

---

## 12. Fuori ambito

- Riscrittura o traduzione dei contenuti degli esperimenti.
- Esecuzione dei test e compilazione delle schede risultati.
- Correzioni alla Home non legate al blocco 5 (hero, card, tablet): hanno un brief a parte.
- Nuovi menu principali, sezioni «Open Lab» o nuove aree del sito.
- Download degli artefatti, area personale o salvataggio dei progressi.
- Pubblicazione delle versioni ES ed EN.
