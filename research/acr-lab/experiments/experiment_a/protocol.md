# MANZO AI ACR — Esperimento A, protocollo preregistrabile v0.4

**Stato:** proposta di preregistrazione. Nessun test sperimentale LLM eseguito; non si rivendicano miglioramenti prestazionali. Data: 2026-11-14.

## Domanda
In una pipeline di revisione web dotata di checklist automatizzata a ogni iterazione, aggiungere memorie selettive verificate dalle ultime due revisioni riduce le regressioni senza costi sproporzionati?

## Ipotesi e decisione predefinita
- **H0**: ACR + checklist non riduce le regressioni rispetto alla checklist sola.
- **H1**: ACR + checklist produce almeno il 30% di riduzione relativa del tasso di regressione rispetto alla checklist sola, con costo monetario <=1,5x e senza deterioramento materiale del pass-rate finale.
- Il 30% e 1,5x sono soglie di progetto, *non* risultati osservati. Congelarle prima del test definitivo.
- La valutazione esplorativa è positiva solo se l'effetto punto stimato raggiunge la soglia, la CI al 95% del rischio relativo esclude 1 a favore di C3, e il costo rimane sotto la soglia. Riportare sempre intervalli, risultati negativi e perdita per singolo compito. Con 12 compiti, l'assenza di significatività non dimostra equivalenza.

## Bracci e isolamento causale
| Braccio | Pipeline | Ruolo |
|---|---|---|
| C0 | Ultima versione + feedback corrente; nessuna checklist | Controllo debole diagnostico |
| C1 | Cronologia integrale, troncata al budget, + checklist | Controllo con memoria grezza |
| C2 | Ultima versione + feedback + **stessa checklist automatizzata** | **Baseline primaria** |
| C3 | **C2 identico** + retrieval di memorie verificate ultime due revisioni + M0 approvate | **Trattamento** |
| C4 | **C2 identico** + tutte le memorie verificate pertinenti + M0 | Ablazione finestra due revisioni |
| C5 (facoltativo) | C2 + riassunto automatico delle ultime due revisioni senza curator | Baseline forte aggiuntiva |

**Essenziale:** C3 deve ricevere gli stessi risultati dei test di C2, negli stessi momenti. L'unica differenza sperimentale primaria è il contesto di memoria. Stessa politica di editing, stessi tool, stesse precondizioni e stesso limite globale di token. Le memorie consumano il proprio sotto-budget (massimo 800 token) senza aumentare il tetto complessivo; riportare anche costi effettivamente consumati. C1 e C4 usano lo stesso sotto-budget.

## Dataset
- 12 compiti web, 3 famiglie: landing/accessibilità, form/validazione, navigazione mobile/responsività.
- 8-12 test deterministici per compito, esplicitando esattamente ambiente, browser, viewport e versioni.
- 5 ripetizioni/blocco per compito e braccio, semi preregistrati, ordini randomizzati e controllati; un seed non garantisce perfetta determinazione dei modelli remoti.
- 5 bracci x 12 compiti x 5 ripetizioni = 300 **esecuzioni complete**, fino a 6 revisioni ciascuna (massimo 1800 passaggi di revisione); C5 rende le esecuzioni 360.
- 3-4 task di validazione ciechi separati dal pilot; non ottimizzare Curator e criteri sul set di valutazione.
- Preferire compiti realmente osservati da revisione siti; evitare trappole progettate per favorire la memoria.

## Verificatore
- Suite **esterna e indipendente** dal Curator: Playwright mobile, axe-core (accessibilità), lint, test di comportamento UI; Lighthouse come metrica diagnostica con ambiente riproducibile, non unico giudice della qualità.
- Valutazioni qualitative LLM, se usate, sono metriche secondarie e marcate come tali.
- Distinguere **test di regressione** da **nuovi criteri introdotti** a ogni passo.
- Un test che fallisce in partenza non è eleggibile a essere contato come regressione nella transizione successiva.

## Formula della metrica primaria
Per ogni coppia di revisioni consecutive, definire per ciascun test stabile:
`eligible = PASS_{r-1}`; `regressed = PASS_{r-1} and FAIL_{r}`.

`regression_rate = sum(regressed) / sum(eligible)`.

Se un blocco non ha test eleggibili, registrare `NA` e non attribuire un tasso zero. Escludere test aggiunti tra r-1 e r dal calcolo di tale transizione. Fornire anche regressioni per 100 test eleggibili.

**Criticità:** la metrica può premiare agenti che non fanno mai passare test. Per questo va interpretata insieme al pass-rate finale e a una metrica di successo del compito. Definire a priori la soglia minima di successo.

## Metriche secondarie
1. Pass-rate e task success finali; 2. revisioni necessarie fino al raggiungimento dei criteri; 3. costo in USD/EUR, token input/output e latenza; 4. rollback e interventi umani (in esperimento automatizzato separarli dal successivo studio UX); 5. memorie proposte/verificate/rifiutate; 6. errori di retrieval e conflitti; 7. potenziali episodi di memory poisoning bloccati.

## Analisi preregistrata
- Estimand primario: differenza C3-C2 nel tasso di regressione, con reporting del relativo risk ratio C3/C2.
- Analisi appaiata per task x ripetizione, preferibilmente controllando l'ordine/blocco. Usare cluster bootstrap al livello del **compito** (non trattare singoli test UI come unità indipendenti); riportare anche una stima gerarchica o analisi di sensibilità.
- 12 compiti sono un campione esplorativo; definire un successivo studio confermatorio con dimensionamento campionario empirico.
- Rapporto costo/beneficio e intervalli, non solo p-value.
- Confronti C3-C4 e C3-C5 sono secondari, etichettati come tali; non reinterpretare un esito nullo come prova di equivalenza.

## Logging e protezione dati
Per ogni revisione: run_id, task_id, seed/blocco, arm, revision, modello/versione, tool versions, prompt hash e riferimento al prompt completo in deposito protetto, IDs delle memorie recuperate ed escluse con motivi, output hash/referenza, test_id con prima/dopo, costo, token, azioni del Curator, decisioni del controller e operatore. Conservarne le tracce con accesso limitato, oscurando dati personali e segreti prima di eventuale pubblicazione.

## Punti da congelare prima dell'esperimento
Compiti, test, seed, modello e versione, variabili di generazione, prompt d'istruzione, tokenizer, limiti globali, mapping status, criterio successo e analisi statistica. Qualsiasi modifica successiva va nel registro delle deviazioni. Il pilot serve per verificare infrastruttura e raccolta delle tracce, non per selezionare i task più favorevoli ad ACR.

## Fibonacci
**Non è incluso nell'Esperimento A.** I checkpoint 1,2,3,5,8 diventano un esperimento B separato solo se emerge un segnale di valore della memoria, con baseline di checkpoint uniformi ed event-driven e budget uguali.

## Letteratura minima verificata
- Shinn et al., *Reflexion: Language Agents with Verbal Reinforcement Learning*, NeurIPS 2023: https://arxiv.org/abs/2303.11366
- Sumers et al., *Cognitive Architectures for Language Agents (CoALA)*, TMLR 2024: https://arxiv.org/abs/2309.02427
- Packer et al., *MemGPT: Towards LLMs as Operating Systems*, 2023: https://arxiv.org/abs/2310.08560
- Chhikara et al., *Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory*, ECAI 2025 proceedings published 2026: https://doi.org/10.3233/FAIA251160
- Letta: https://docs.letta.com/
- LangMem: https://github.com/langchain-ai/langmem

**Differenziazione da verificare:** governance e provenienza delle memorie, workflow umano di approvazione, confronti con test deterministici e ottimizzazione contro regressioni. Queste funzionalità prese singolarmente non vanno dichiarate nuove; l'eventuale novità dipenderà dalla combinazione implementata e da evidenze comparative.
