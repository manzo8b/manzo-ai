# 01 · Carta scientifica — Esperimento A

**Nota di completezza v0.7:** questo documento descrive il *solo* Esperimento A. Per l’intero programma (A, B e C), vedere `00_PROGRAMMA_SCIENTIFICO.md` e i nuovi protocolli sotto `experiments/`.

## Oggetto

Valutare **la sola contribuzione della memoria selettiva verificata** a una pipeline che già esegue una checklist di regressione a ogni revisione di una UI web. Non valutiamo memoria autobiografica generale, coscienza dell'AI o una «legge aurea» dei prompt.

## Domanda e ipotesi preregistrabili

- **H0:** a parità di vincoli, la pipeline ACR non ottiene un tasso di regressione inferiore alla checklist senza memoria.
- **H1:** ACR riduce il tasso di regressione di **almeno il 30% relativo**, mantenendo un costo monetario **non superiore a 1,5 volte** quello della checklist e senza peggiorare materialmente il successo finale del compito.
- **Importante:** 30% e 1,5x sono soglie **provvisorie** da congelare *prima* della raccolta dei dati definitivi. Un campione iniziale non prova la generalizzabilità.

## Disegno minimo credibile

- Dominio: revisione iterativa di interfacce web.
- Confronto causale primario: **C2** = ultima versione, feedback, test automatici; **C3** = tutto C2 **più** memoria verificata, selettiva, delle ultime due revisioni.
- Baseline complementari: **C0** senza checklist; **C1** cronologia troncata e checklist; **C4** checklist + tutte le memorie pertinenti (ablazione dell'ordine due). **C5**, opzionale, semplice riassunto non curato.
- Piano esplorativo: 12 task (accessibilità/landing, form, navigazione mobile), 5 ripetizioni/task/braccio, massimo 6 revisioni, 8–12 test deterministici/task. Sono **300 esecuzioni complete** sui cinque bracci C0–C4, non 300 test di programma.
- Test indipendenti dal Curator: Playwright, axe-core, lint e test funzionali; Lighthouse solo diagnostico, con ambiente riproducibile.
- Congelare prima della valutazione: compiti, suite, versioni modello/tool, seed, budget, prompts, procedura di analisi e criteri di successo.

## Metrica primaria

Una regressione si verifica quando **lo stesso test, nella stessa versione**, era `PASS` alla revisione r-1 ed è `FAIL` alla r.

`regression_rate = count(PASS -> FAIL) / count(PASS -> {PASS, FAIL})`

Una prova `PASS` non rieseguita o `SKIP` viene tracciata come *follow-up mancante*; non va conteggiata automaticamente come successo. Riportare anche copertura dei test e **pass-rate finale**, per non premiare un agente che non risolve mai i problemi.

Metriche secondarie: task success, revisioni a convergenza, token, costo, interventi umani, memorie escluse/rifiutate, conflitti e falsi recuperi.

## Come interpretare gli esiti

- C3 batte C2 sui task esplorativi: **segnale favorevole**, non ancora prova generale.
- C3 e C2 simili: la checklist può bastare. Non reinterpretare un risultato nullo come equivalenza dimostrata.
- C3 consuma troppo: vantaggio potenzialmente non sostenibile.
- C3 peggiora risultati o recupera memorie errate: **fallimento informativo** e revisione dell'architettura.

## Condizioni per parlare di efficacia

Test su compiti indipendenti dal pilot, dati e codice riproducibili, confronto appaiato per task/ripetizione, intervalli di confidenza con bootstrap raggruppato per task, pubblicazione degli errori e delle deviazioni dal protocollo. Se il pilot produce segnali utili, pianificare uno studio confermatorio con dimensionamento campionario basato sulla variabilità osservata.

## Fibonacci

**Escluso dall'Esperimento A.** La sequenza 1,2,3,5,8 è soltanto una possibile pianificazione dei checkpoint per un successivo esperimento B contro checkpoint regolari ed event-driven a parità di costo. Senza prova del valore della memoria, non ha senso attribuirle un vantaggio.

## Bibliografia di partenza

- Shinn et al. (2023), *Reflexion*: https://arxiv.org/abs/2303.11366
- Sumers et al. (2024), *Cognitive Architectures for Language Agents*: https://arxiv.org/abs/2309.02427
- Packer et al. (2023), *MemGPT*: https://arxiv.org/abs/2310.08560
- Mem0: https://github.com/mem0ai/mem0
- Letta: https://docs.letta.com/
- LangMem: https://github.com/langchain-ai/langmem

**Originalità:** la novità non è «inventare la memoria». Va cercata, se emerge, nell'effetto misurabile di governance, provenienza, controllo umano e recupero selettivo sulle regressioni, rispetto a baseline forti.
