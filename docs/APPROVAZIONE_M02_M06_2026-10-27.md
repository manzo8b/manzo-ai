# MANZO AI — Approvazione editoriale dei moduli M02–M06

**Decisione del Product Owner:** 27 ottobre 2026  
**Esito:** approvati editorialmente M02, M03, M04, M05, M06.  
**Ambito:** contenuti didattici preparati in italiano, spagnolo e inglese, come nelle bozze editoriali già sviluppate.  
**Non riguarda:** traduzioni delle otto slide grafiche M01, che restano un'attività distinta.

## Moduli approvati

| Modulo | Argomento | Stato editoriale |
| --- | --- | --- |
| M02 | Modelli linguistici (LLM) | Approvato dal Product Owner |
| M03 | Prompt e istruzioni efficaci | Approvato dal Product Owner |
| M04 | Verifica e valutazione delle risposte AI | Approvato dal Product Owner |
| M05 | Workflow e processi con l'AI | Approvato dal Product Owner |
| M06 | AI: storia, lavoro e società | Approvato dal Product Owner |

La decisione si riferisce alle bozze complete trilingui preparate nel lavoro editoriale MANZO AI (obiettivi, spiegazioni, esempi, esercizi, soluzioni, quiz, criteri di valutazione, limiti e fonti).

## Stato pubblico e confini dell'approvazione

- La **release pubblica v0.4** è stata distribuita il 27 ottobre 2026 tramite GitHub Actions, commit `20d72370ca11f08666bc03ba7190a295eb4040f5`.
- Il catalogo incluso nella v0.4 può ancora mostrare M02–M06 come «In revisione editoriale», perché il pacchetto statico non è stato rigenerato con questa decisione.
- Le lezioni complete M02–M06 **non sono automaticamente online** per effetto di questa approvazione; non dichiararle pubblicate prima di avere generato e collaudato un nuovo pacchetto.
- M01 resta invariato e già approvato. Le otto slide M01 richiedono una distinta verifica visiva, e le versioni illustrate spagnola/inglese non sono ancora prodotte.

## Passaggio successivo: release contenutistica

1. Recuperare i file sorgente delle bozze editoriali complete M02–M06 già preparate, senza ricostruirli arbitrariamente dai soli titoli del catalogo.
2. Verificare la corrispondenza IT/ES/EN, fonti, leggibilità, navigazione, correttezza dei quiz, lingua e coerenza con M01.
3. Integrare i moduli completi nel sito aggiornando catalogo, pagine dei moduli, collegamenti e indicazioni sullo stato editoriale.
4. Generare la successiva release contenutistica (proposta **v0.5**), eseguire controlli di build, link, accessibilità e mobile e pubblicare tramite il workflow già in uso.
5. Eseguire un collaudo umano dopo il deploy; soltanto allora segnare M02–M06 come «Pubblicate».

**Regola:** l'approvazione del contenuto non sostituisce la verifica tecnica della versione web né implica pubblicazione automatica.

**Proprietà decisionale:** Product Owner; sviluppo MANZO AI direttamente con ChatGPT, senza trasferimento automatico a Codex.
