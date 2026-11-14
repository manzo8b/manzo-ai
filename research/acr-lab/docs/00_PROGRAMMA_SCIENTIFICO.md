# MANZO AI ACR — Programma scientifico integrato v0.7

**Data:** 14 novembre 2026 · **Stato:** ipotesi e protocolli in progettazione; nessuna dimostrazione sperimentale della superiorità ACR o di Fibonacci.

## Abstract
MANZO AI ACR è un programma di ricerca applicata sull'ottimizzazione dei processi LLM attraverso (A) memoria ricorsiva controllata e verificata, (B) pianificazione dei checkpoint di revisione e (C) composizione dei prompt in componenti di struttura e compito. L'idea matematica originaria — la ricorrenza di Fibonacci — è trattata come ispirazione teorica, **non** come legge empiricamente stabilita sul comportamento dei modelli. La ricerca può produrre risultati positivi, nulli o negativi.

## Che cosa è documentato, cosa è ipotizzato, cosa è stato eseguito

| Oggetto | Fatto/teoria/ipotesi | Stato di evidenza |
|---|---|---|
| Fibonacci: F(n)=F(n-1)+F(n-2) | Identità matematica | Definita, non controversa |
| Prompt articolato in intento, ruolo, contesto, vincoli, esempi e verifica | Modello didattico di progettazione | Non dimostrato universalmente superiore |
| A: memoria verificata vs checklist senza memoria | Ipotesi empirica causale | **NON TESTATA** con LLM |
| B: checkpoint 1,2,3,5,8 vs uniformi/event-driven | Ipotesi sperimentale condizionata | **NON TESTATA** |
| C: 61,8% struttura / 38,2% compito vs altri rapporti | Ipotesi sperimentale indipendente | **NON TESTATA** |
| Verifica browser su fixture locale di v0.6 | Test di strumentazione | 2 regressioni intenzionali rilevate, non un effetto ACR |

## Tre esperimenti, non tre prove di un'unica teoria

### A — Memoria controllata
Domanda: **aggiungere memoria selettiva verificata a una checklist di test riduce le regressioni di modifiche web?**
- Confronto primario: `C3 = checklist + memoria ACR` vs `C2 = stessa checklist, senza memoria`.
- H0: nessuna riduzione delle regressioni; H1: riduzione relativa proposta >=30%, costo <=1,5x e nessuna perdita sostanziale di completamento. Soglie da congelare prima dei dati.
- Trattamento: memoria con scope, origine, evidenza, approvazione umana; gli stessi criteri deterministici in entrambi i bracci.
- Pilot: 2 task indipendenti, poi 12 task × 5 repliche per braccio, più set cieco. Le misure di un pilot non sostituiscono conferma statistica.
- Vedere `experiments/experiment_a/protocol.md`.

### B — Scheduler Fibonacci
Domanda: **con un budget di ispezione identico, controlli intensivi ai passi 1,2,3,5,8 sono migliori di checkpoint regolari o guidati dagli errori?**
- H0: schedule Fibonacci non migliora qualità, regressioni o costo rispetto alle baseline.
- Eseguire solo dopo che A ha prodotto evidenza favorevole e con utilità pratica sufficiente; un esito negativo di A può comunque giustificare uno studio separato di scheduling, ma **non** come conferma dell'ACR.
- A differenza di A (massimo 6 revisioni), B richiede un orizzonte sufficiente per raggiungere l'ottavo passo; si propone 10 revisioni massime per tutti i bracci.
- **Test critici a ogni passaggio**; soltanto le revisioni approfondite sono differite ai checkpoint. Altrimenti si confrontano livelli di sicurezza differenti.
- Vedere `experiments/experiment_b/protocol.md`.

### C — Struttura del prompt
Domanda: **come varia la prestazione al cambiare della quota di testo di impalcatura rispetto all'input dinamico, e 62% ha un vantaggio distintivo?**
- H0: non emergono differenze robuste, oppure l'eventuale rapporto ottimale non è particolarmente vicino a 0,618.
- Non dipende dal risultato di A: può essere studiato con compiti e suite indipendenti dal Curator.
- **Il rapporto non è una variabile isolabile perfettamente senza vincoli**: con totale token fissato, cambiare la quota cambia l'ampiezza dei due contenuti; con compito identico, cambia il totale. Il protocollo impone due studi complementari e controlli di contenuto, lunghezza e ordine.
- Vedere `experiments/experiment_c/protocol.md`.

## Principi di misura
1. Congelare prima di ogni prova definitiva: modelli, versioni, prompt, dataset, test, allocator di token, randomizzazione, soglie, analisi.
2. La stessa specifica, gli stessi test e le stesse condizioni di ambiente per ogni confronto causale. Non scegliere post hoc solo i task in cui ACR vince.
3. Statistiche inferenziali a livello di task/replica, non trattando ogni singolo check come prova indipendente. Pubblicare intervalli di confidenza ed esiti nulli/negativi.
4. Prevedere un **set di validazione indipendente** e controlli antifuga fra bracci e fra repliche.
5. Analizzare qualità e costo congiuntamente. Evitare di premiare il sistema che semplicemente produce meno cambiamenti o non fa mai passare i test.
6. Conservare log completi protetti e output riproducibili privi di dati personali e segreti.
7. Valutatori deterministici per verifiche operative; giudizi LLM qualitativi soltanto come metriche separate, con controlli di affidabilità e campioni valutati da umani.

## Confini interpretativi
- Nessuna architettura descritta equivale a coscienza artificiale o ragionamento interno deterministico.
- Il rapporto aureo resta una **ipotesi confrontabile** con 60%, 62%, 65%, altri rapporti e nessuna impalcatura aggiuntiva, non un principio scientifico acquisito.
- La memoria non fornisce automaticamente protezione contro prompt injection o memory poisoning; validazione e audit sono prerequisiti, non garanzie assolute.
- I test web valutano soltanto il dominio e gli strumenti effettivamente eseguiti. Non generalizzare automaticamente a scrittura, formazione o multimodalità.

## Il contributo che si può cercare
Non è nuovo il principio generale della memoria, del chaining o dell'ottimizzazione dei prompt: esistono Reflexion, CoALA, MemGPT/Letta, Mem0, DSPy/GEPA. L'eventuale contributo di MANZO AI sarebbe una combinazione **replicabile** di governo delle memorie, retrieval con vincoli, verifica indipendente, approvazione umana e misurazione delle regressioni e dei costi.

## Evidenza letteraria e confronto
- Shinn et al. (2023), *Reflexion*, NeurIPS: https://proceedings.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html — memoria episodica e feedback, precedente rilevante per A.
- Sumers et al., *Cognitive Architectures for Language Agents*: https://arxiv.org/abs/2309.02427 — tassonomia delle memorie.
- Packer et al., *MemGPT*: https://arxiv.org/abs/2310.08560 ; Letta https://docs.letta.com/ ; Chhikara et al., *Mem0*, https://doi.org/10.3233/FAIA251160 — sistemi già esistenti di memoria.
- Agrawal et al. (2025), *GEPA*: https://arxiv.org/abs/2507.19457 — ottimizzazione riflessiva dei prompt, baseline concettuale.
- Sánchez-Torrón et al. (2026), *To Write or to Automate Linguistic Prompts*: https://aclanthology.org/2026.eamt-1.8/ — efficacia dipendente dal compito e dal modello.
- Mao et al. (2024), *Do Prompt Positions Really Matter?*: https://aclanthology.org/2024.findings-naacl.258/ ; Liu et al. (2024), *Lost in the Middle*: https://aclanthology.org/2024.tacl-1.9/ — controllare anche la posizione dell'informazione.
- Dash et al. (2026), *From Untrusted Input to Trusted Memory*: https://arxiv.org/abs/2606.04329 — rischio di memory poisoning.

## Provenienza delle due fonti utente
Versioni integrali e inalterate dei documenti ricevuti in `sources/user/`: `Fibonacci_Prompt_Engineering_v2.md` e `MANZO_AI_ACR_v0.4.md`. Il presente documento amplia, non sostituisce e non retrodata, la strumentazione v0.6.
