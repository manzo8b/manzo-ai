# MANZO AI Learning B2B · Console UX Preview

**Stato:** simulazione interattiva con dati fittizi in memoria locale, non un SaaS con account e licenze reali.  
**Data:** 15 novembre 2026.

La console permette di esaminare visivamente l'esperienza di un responsabile della formazione e di uno studente prima di attivare un backend commerciale.

## Cosa fa concretamente

- Gestisce **quattro profili completamente fittizi**, con un catalogo di due percorsi e **tre posti aziendali simulati**.
- Consente di assegnare e liberare un posto, impedendo di superare il massimo.
- Consente a un amministratore simulato di iscrivere un membro con posto attivo a un corso.
- Mostra progressi per persona e percorso e permette di simulare il completamento di un modulo.
- La revoca del posto revoca le iscrizioni attive. Una nuova assegnazione del posto non riattiva automaticamente le iscrizioni.
- Registra azioni in un log **temporaneo** ed espone un pulsante di reset.
- Tutte le funzioni sono disponibili in IT/EN/ES, con layout responsive e QA browser.

**Non avviene alcuna autenticazione. Selezionare un profilo nella UI non significa effettuare un login.** La simulazione non comunica con PostgreSQL né con Stripe. I cambiamenti scompaiono al refresh. Nessun form o dato dell'utente viene inviato o memorizzato.

## Collegamento con il backend

Nella CI le funzioni PostgreSQL della migrazione `product/backend/migrations/0002_learning_b2b.sql` eseguono i corrispondenti controlli reali su organizzazioni, iscrizioni, licenze e progressi, compresa una prova di concorrenza con due connessioni. I test di database e quelli del browser sono **distinti**. Non è corretto sostenere che il nuovo dashboard sia già collegato a quel database.

## URL della demo

- Italiano: `/manzo-ai/it/prodotto/learning-b2b/`
- Inglese: `/manzo-ai/en/product/learning-b2b/`
- Spagnolo: `/manzo-ai/es/producto/learning-b2b/`

Le pagine sono `noindex,follow` e linkate da Product Lab, non configurate come store.

## Piano per il collegamento reale

1. Progettare la convalida del token e l'identità dei membri con un provider appropriato.
2. Scegliere e approvare regione, hosting e budget di un database separato esclusivamente per MANZO AI.
3. Collegare le operazioni alle API documentate; nessuna funzione SQL privata va invocata direttamente dal browser.
4. Implementare area studente con persistenza verificata e dashboard amministrativa con report autorizzati.
5. Integrare eventuali licenze e pagamenti soltanto mediante backend che verifica le firme e le condizioni contrattuali.
6. Collaudare con account di prova reali su un ambiente di staging; completare revisione privacy e sicurezza.

## Comandi di collaudo

Il workflow GitHub `MANZO AI Chromatic QA` pubblica la preview in un filesystem temporaneo e utilizza `theme/learning-console-browser-smoke.py` per testare desktop, mobile, lingua, gestione dei posti, iscrizioni, progressi, reset e assenza di storage persistente.

L'effetto della simulazione non costituisce prova di una funzione SaaS attiva. Il suo scopo è raccogliere riscontri su UX e necessità dei potenziali acquirenti B2B.
