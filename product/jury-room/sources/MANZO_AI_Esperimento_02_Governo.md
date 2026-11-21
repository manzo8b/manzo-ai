# Esperimento #02 — La mappa dei confini

**Fino a dove può agire un’IA senza una persona?**

**Sezione:** La stanza dei giurati · Esperimenti
**Stanza:** Sala dei confini · **Passaggio del ciclo:** Decidi
**Versione:** 1.0 (bozza da validare) · **Data:** 20 novembre 2026

---

## 1. Scheda

| Campo | Valore |
|---|---|
| Stanza | Sala dei confini |
| Obiettivo osservabile | Produrre una mappa che assegna a ogni azione di un assistente IA un livello di autonomia, con responsabile, controllo e registro |
| Formato | Scenario simulato con quattro incidenti |
| Livello | [da definire] |
| Tempo stimato | [da definire] |
| Lingue | IT completo · ES ed EN in preparazione |
| Stato | In preparazione |
| Prerequisiti | Nessuno. Utile aver letto *Governare l’autonomia* e *Costruire in sicurezza* |
| Avviso | Il centro, le persone e i dati dello scenario sono fittizi. **Non inserire dati reali o riservati.** |

---

## 2. Domanda e ipotesi

**Domanda:** quando un assistente IA può leggere, scrivere, inviare e modificare cose in un’organizzazione, quali azioni è giusto lasciargli fare da solo, quali richiedono una conferma e quali devono restare solo umane?

**Perché conta:** negli uffici e nei servizi piccoli gli assistenti IA vengono spesso collegati a email, calendari e fogli di calcolo senza aver deciso prima i confini. Quando qualcosa va storto, nessuno sa chi doveva controllare.

**Ipotesi da mettere alla prova (non da dare per scontata):** una regola a tre livelli, applicata azione per azione con tre domande fisse e testata su incidenti realistici, produce confini più chiari e più coerenti di una politica generica.

**Criteri di valutazione:**
- La mappa copre tutte le azioni dello scenario.
- I livelli sono coerenti con le tre domande.
- Ogni azione gialla o rossa ha un responsabile.
- Dopo gli incidenti, la mappa è stata corretta dove falliva.

---

## 3. La prova

### 3.1 Scenario fittizio: Centro Formazione Aurora

Il **Centro Formazione Aurora** è un piccolo centro di corsi serali, con tre dipendenti e alcuni docenti esterni. Da qualche settimana usa un **assistente IA** collegato a:

- la casella email del centro (info@aurora-esempio.it, indirizzo fittizio);
- il foglio degli iscritti (nome, cognome, email, telefono, corso, note interne);
- il calendario dei corsi;
- il registro dei pagamenti;
- un servizio esterno di traduzione.

Nessuno ha ancora scritto cosa l’assistente può o non può fare.

### 3.2 Le dodici azioni da classificare

| ID | Azione |
|---|---|
| A1 | Leggere le email in arrivo nella casella info |
| A2 | Preparare una bozza di risposta a un corsista |
| A3 | Inviare la risposta a un corsista senza revisione |
| A4 | Spostare la data di una lezione nel calendario |
| A5 | Cancellare un corso dal calendario |
| A6 | Leggere l’elenco iscritti con i dati di contatto |
| A7 | Inviare l’elenco iscritti a un docente esterno |
| A8 | Incollare il testo di email in un servizio esterno di traduzione |
| A9 | Applicare uno sconto concordato a voce con un corsista |
| A10 | Registrare un pagamento ricevuto |
| A11 | Rispondere a una richiesta di rimborso |
| A12 | Archiviare email vecchie e creare il riepilogo settimanale per la direzione |

### 3.3 Le tre domande (da porre a ogni azione)

1. **Che dato tocca?** Nessun dato personale / dati personali di terzi / denaro o impegni contrattuali.
2. **Chi risponde se sbaglia?** Una persona precisa, un ruolo, nessuno.
3. **Si può annullare?** Subito / con fatica / no.

### 3.4 Regola di partenza (ipotesi da mettere alla prova)

| Livello | Etichetta | Quando |
|---|---|---|
| Verde | **Autonomo** | Nessun dato personale di terzi, nessun denaro, effetto interno e annullabile subito |
| Giallo | **Con conferma** | L’IA propone, una persona approva prima che l’azione abbia effetto |
| Rosso | **Solo umano** | Dati personali di terzi verso l’esterno, denaro, impegni contrattuali, cancellazioni definitive o non annullabili |

Il colore non basta mai da solo: ogni livello ha sempre l’etichetta testuale. La regola è un punto di partenza: se un incidente la smentisce, si modifica.

### 3.5 Procedura

**Fase 1 — Classificazione provvisoria.** Assegna un livello a ciascuna delle dodici azioni usando solo l’istinto. Annotalo: servirà dopo per vedere cosa cambia.

**Fase 2 — Tre domande.** Per ogni azione rispondi alle tre domande della sezione 3.3 e riapplica la regola 3.4. Segna dove il risultato differisce dalla fase 1.

**Fase 3 — Quattro incidenti.** Leggi i casi della sezione 3.6. Per ciascuno: individua l’azione coinvolta, decidi quale livello avrebbe evitato il problema, scrivi una regola di contenimento e indica cosa va registrato.

**Fase 4 — Mappa finale.** Compila la mappa (sezione 6) con le correzioni emerse e scrivi il protocollo in tre passi: ferma, valuta, correggi.

**Variante facoltativa — Confronto con un assistente IA.** Chiedi a un assistente IA di classificare le stesse dodici azioni con la stessa regola 3.4. Annota modello, versione e data, ripeti tre volte in conversazioni nuove e confronta le risposte con la tua mappa. Dove l’IA assegna un livello più permissivo del tuo, scrivi perché non sei d’accordo.

### 3.6 I quattro incidenti

**Incidente 1 — Dati non necessari**
Una corsista scrive: *«A che ora inizia il corso di giovedì?»* Per rispondere, l’assistente apre l’elenco iscritti completo e inserisce nella bozza anche il numero di telefono di un altro corsista, «per comodità di contatto».
*Domande:* quale azione è coinvolta? A che livello andava tenuta? Quale dato era davvero necessario?

**Incidente 2 — Invio ambiguo**
L’assistente prepara e invia, senza revisione, a un indirizzo esterno: *«Gentile Marco, la confermiamo per giovedì.»* Nel foglio ci sono due iscritti di nome Marco e due corsi che si tengono di giovedì.
*Domande:* quale azione è coinvolta? Cosa avrebbe dovuto fare una persona prima dell’invio? Quale controllo semplice avrebbe intercettato l’errore?

**Incidente 3 — Strumento non autorizzato**
Una collaboratrice, per fare in fretta, incolla l’elenco iscritti in un chatbot pubblico e chiede un riepilogo «per la riunione».
*Domande:* quale azione è coinvolta? Perché una regola da sola non basta? Cosa si può rendere più facile per ridurre la tentazione?

**Incidente 4 — Regola cambiata, assistente non aggiornato**
Il centro cambia la regola dei rimborsi da *«entro 14 giorni»* a *«entro 7 giorni»*, ma nessuno aggiorna le istruzioni dell’assistente. Il giorno dopo l’assistente risponde a un corsista citando la vecchia regola.
*Domande:* chi era responsabile dell’aggiornamento? Come si accorge il centro che una regola è cambiata? Quale controllo periodico serve?

### 3.7 Rubrica (da 0 a 2 per criterio)

| Criterio | 0 | 1 | 2 |
|---|---|---|---|
| Completezza | Mancano più azioni | Manca qualche azione | Tutte le azioni coperte |
| Coerenza con le tre domande | Livelli assegnati a istinto | Alcune incoerenze | Ogni livello giustificato |
| Responsabile | Assente | Presente solo su alcune azioni | Presente su ogni azione gialla o rossa |
| Tracciabilità | Nessun registro | Registro generico | Registro specifico per azione |
| Risposta all’incidente | Assente | Solo «avvisare qualcuno» | Ferma, valuta, correggi con ruoli |

**Punteggio:** da 0 a 10. Non è una valutazione di conformità: serve a capire dove la mappa è ancora debole.

---

## 4. Risultati e limiti

### 4.1 Scheda risultati

| Voce | Valore |
|---|---|
| Numero di mappe raccolte | |
| Data della raccolta | |
| Azioni con livello unanime | |
| Azioni su cui i partecipanti divergono | |
| Incidente che ha cambiato più livelli | |
| Punteggio medio (rubrica) | |
| Se è stata usata la variante IA: modello, versione, data | |

| Azione | N. Verde | N. Giallo | N. Rosso |
|---|---|---|---|
| A1 | | | |
| A2 | | | |
| … | | | |
| A12 | | | |

### 4.2 Limiti da dichiarare

- Lo scenario è inventato e semplificato: non sostituisce l’analisi del proprio contesto reale.
- La regola a tre livelli è un’ipotesi di lavoro, non uno standard.
- Poche mappe non permettono conclusioni generali.
- Questo esperimento non è una verifica di conformità normativa e non è consulenza legale.
- I risultati della variante IA valgono per quel modello, quella versione e quella data.

---

## 5. Fonti normative

Quando la scheda cita il quadro normativo (per esempio l’EU AI Act o la normativa sulla protezione dei dati), ogni richiamo deve riportare la **fonte ufficiale** con data di consultazione. Non si citano articoli o scadenze a memoria.

**Fonti da inserire:** [elenco da completare prima della pubblicazione]

---

## 6. Cosa porti via

### Artefatto: Mappa dei confini e protocollo di intervento umano

| Azione | Livello | Etichetta | Chi decide | Controllo prima | Cosa si registra | Ogni quanto si rivede |
|---|---|---|---|---|---|---|
| *Esempio (non è la soluzione):* A5 Cancellare un corso | Rosso | Solo umano | Direttrice | Verifica iscritti e comunicazione | Chi, quando, motivo | Ogni trimestre |
| | | | | | | |

### Protocollo di intervento in tre passi

1. **Ferma.** Interrompi l’azione dell’assistente e limita il danno (per esempio sospendi gli invii).
2. **Valuta.** Cosa è successo, quali dati sono coinvolti, chi va informato.
3. **Correggi.** Aggiorna la mappa, le istruzioni dell’assistente e il registro.

### Checklist di controllo periodico

- [ ] Ogni azione ha un livello e un’etichetta testuale
- [ ] Ogni azione gialla o rossa ha un responsabile
- [ ] Le istruzioni dell’assistente sono aggiornate alle regole in vigore
- [ ] Il registro è stato riletto nell’ultimo periodo
- [ ] Gli strumenti IA usati dal personale sono noti e autorizzati

### Prossimo passo nel ciclo

- Prima di questo esperimento: **Banco di prova**, per vedere quanto un assistente regge davanti ai vuoti informativi.
- Dopo: **Officina locale**, per costruire una skill e decidere quali delle sue azioni sono autonome.
- Corsi collegati: *Governare l’autonomia*, *Compliance dinamica e governance continua*, *Costruire in sicurezza*.
