# ACR-EXP-B · Fibonacci come scheduling dei checkpoint

**Stato:** protocollo proposto; non preregistrato; non eseguito. **Dipendenza:** preferibilmente dopo un risultato utile nell'Esperimento A; mai presentarlo come prova della legge aurea.

## Domanda e ipotesi
La pianificazione dei controlli approfonditi ai passi `[1, 2, 3, 5, 8]` migliora qualità, prevenzione dei difetti o costo rispetto a pianificazioni alternative a ugual numero e costo di audit?
- H0: Fibonacci non riduce il tasso di regressioni né migliora task success/costo rispetto alla pianificazione uniforme o event-driven.
- H1: una differenza favorevole riproducibile appare su almeno una delle metriche prefissate senza compromissione di qualità.

## Orizzonte e bracci
Fissare **10 revisioni massime** per consentire il checkpoint n.8. Usare stessi test base, task, modello, seed/blocchi, limiti e disponibilità di memoria (se usata) su ogni braccio.

| Braccio | Audit approfonditi | Ruolo |
|---|---|---|
| B-FIB | 1, 2, 3, 5, 8 | Trattamento |
| B-UNIF | 2, 4, 6, 8, 10 | Baseline uniforme, 5 audit |
| B-EVENT | Trigger da punteggio di anomalia fissato sul development set; al massimo 5 audit | Baseline guidata dagli errori |

I checkpoint sono **tempi del controllo approfondito**, non sostituiscono i test critici eseguiti dopo ogni modifica. Il consumo di B-EVENT può essere inferiore ai cinque audit: confrontare sia costo effettivo sia analisi con budget controllato. Se è richiesta parità esatta dei cinque audit, usare policy di fallback predeterminata, mai decisa dopo aver visto i risultati. Non far vedere a un braccio più feedback complessivo senza contabilizzarlo.

## Unità sperimentale e misure
- Task × replica, randomizzazione appaiata; 12 task e 5 repliche sono **pilot** ipotetico, non stima di potenza.
- Primaria: regressioni per 100 transizioni di test eleggibili, con intervalli per cluster di task.
- Secondarie: pass-rate e task success finali, costo audit+token+latency, difetti rilevati per audit, revisioni al completamento e defect escape rate.
- Audit approfonditi devono essere esattamente la stessa suite versionata, lanciata in condizioni identiche; in ogni passaggio rimane la suite critica di sicurezza/qualità.
- Analisi dei checkpoint nello stesso budget: quanti difetti non rilevati a tempo debito? La qualità finale non deve essere sacrificata per un risultato di regressioni migliore.

## Controlli e minacce alla validità
- Differenze temporali tra checkpoint e feedback modificano il comportamento dell'Executor: fanno parte del trattamento, quindi vanno dichiarate.
- La possibile diminuzione della spesa su B-EVENT è un risultato costo-efficienza, non prova di pari costo.
- Distinguere STOP precoce da 10 revisioni: preregistrare stopping; analizzare dati censurati e task incompleti.
- Non selezionare solo compiti in cui i primi checkpoint Fibonacci coincidono con errori frequenti.

## Prima dell'esecuzione
Congelare orizzonte, suite critica, suite approfondita, trigger B-EVENT, fallback, costo normalizzato, ordine dei task, test di analisi e ambiente. Testare che ogni braccio raggiunga, quando applicabile, i medesimi criteri finali.

**Esito non deciso**: potrebbe vincere B-UNIF, B-EVENT oppure nessuno; in quel caso Fibonacci resta solo metafora.
