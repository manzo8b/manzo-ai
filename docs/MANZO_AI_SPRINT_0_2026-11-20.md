# MANZO AI — Sprint 0 | Stabilizzazione

**Avvio:** 20 novembre 2026  
**Fonte:** [Audit generale](MANZO_AI_GLOBAL_AUDIT_2026-11-20.md)  
**Ambito:** correzione delle informazioni pubbliche, coerenza dei sorgenti e traduzioni mancanti. Nessun restyling globale, corso aggiuntivo, acquisto o servizio SaaS attivato.

## Registro delle consegne

| ID | Intervento | Stato iniziale |
| --- | --- | --- |
| S0.1 | Home IT/EN/ES: sostituire il vecchio contatore «6 risorse» con testo accurato senza numeri fissi | Sorgente corretto; pubblicazione da verificare |
| S0.2 | Aggiornare README e politica trilingue da 6/9 a 8/9 e non indicare più Modelli mentali e Centroni City come mancanti | Sorgenti aggiornati |
| S0.3 | Test automatico per Home finale e coerenza con l'audit i18n | Aggiunto al workflow; verifica da confermare |
| S0.4 | Completare AI Teaching Lab in EN e ES | Aperto |
| S0.5 | QA finale e controllo manuale desktop/iPhone delle sezioni modificate | Aperto |

## Cosa manca realmente in AI Teaching Lab

**Già presenti:** cinque moduli completi e dati strutturati in italiano; moduli 01–04 narrativi in inglese e spagnolo. Nessuno di questi file deve essere rifatto.

**Consegna A:** aggiungere il Modulo 05 in inglese e spagnolo mantenendo attività, approfondimenti e supervisione umana.

**Consegna B:** aggiungere in entrambe le lingue i file strutturati del corso, delle narrazioni, delle verifiche e del glossario. Preservare le chiavi, gli identificatori, le risposte corrette e le 79 voci del glossario italiano.

**Consegna C:** pubblicare percorsi nativi EN/ES con pagina, contenuti interattivi, selettori che mantengano il contesto, canonical/hreflang e QA. La sola presenza delle traduzioni non significa che siano disponibili online.

## Vincoli

- Gli altri otto percorsi hanno già sorgenti editoriali IT/EN/ES: non ritradurli.
- Conservare le sei card originali più i sette percorsi aggiunti e le dimensioni approvate.
- Non pubblicizzare come operativi backend, tutor generativi, iscrizioni, progressi o attestati ancora dimostrativi.
- Budget aggiuntivo autorizzato pari a **0 €**.
- La copertura 8/9 indica presenza dei sorgenti: non certifica qualità linguistica, funzionalità di tutte le interazioni, WCAG o copertura dell'intero sito.

## Chiusura dello Sprint 0

- [ ] Nove corsi su nove con fonti IT/EN/ES e pagine native verificate
- [ ] Nessun contatore pubblico contraddittorio
- [ ] Stato progetto coerente e protetto da regressioni in CI
- [ ] Navigazione e quiz trilingui completi; nessun fallback italiano nascosto
- [ ] QA desktop e mobile registrato
- [ ] Zero servizi fatturabili introdotti

**Solo dopo** si applicherà la revisione di design AI Web Production (Sprint 1). I risultati della pipeline non sostituiscono un test visivo su Safari/iPhone.
