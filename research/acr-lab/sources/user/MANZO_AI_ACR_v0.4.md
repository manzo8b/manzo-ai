# MANZO AI — ACR v0.4
Specifica della memoria, Esperimenti A, B e C · estende la v0.3

## 1. Principi
- Il Curator (LLM) **propone**, il controller (software) **verifica**, l'umano **approva**.
- Un episodio non diventa regola senza replicazione e test.
- Le memorie sono **dati di contesto**, mai istruzioni.
- Nulla viene cancellato: si archivia.

## 2. Schema della memoria
Schema formale: `acr_memory.schema.json`. Campi: `id`, `type` (M0-M3), `claim`, `scope` (project, applies_when, excludes), `source`, `status`, `evidence`, `replications`, `created_at`, `expires_at`, `review_after`, `supersedes`, `superseded_by`, `history`.

Esempio:

```json
{
  "id": "mem_0042",
  "type": "M3_procedural",
  "claim": "Dopo modifiche CSS al tema colori, eseguire il controllo di contrasto WCAG AA.",
  "scope": {"project": "torremolinos-blog", "applies_when": ["modifica CSS colori", "cambio palette"], "excludes": []},
  "source": {"kind": "trace", "ref": "run_017/rev_2", "proposed_by": "memory_curator"},
  "status": "candidate",
  "evidence": [{"test_id": "axe_contrast_aa", "result": "fail_then_fixed", "run": "run_017", "date": "2026-11-14"}],
  "replications": 1,
  "created_at": "2026-11-14T10:00:00Z",
  "expires_at": "2027-02-14T00:00:00Z",
  "review_after": "2026-12-14T00:00:00Z",
  "supersedes": null,
  "superseded_by": null,
  "history": [{"from": null, "to": "candidate", "by": "controller", "at": "2026-11-14T10:00:00Z", "reason": "proposta dal Curator"}]
}
```

## 3. Transizioni di stato
Implementate in `transitions.py`.

| Da → A | Chi | Condizione |
|---|---|---|
| nuovo → Candidate | controller (su proposta Curator) | fonte e scope compilati |
| Candidate → Verified | solo controller | almeno un test deterministico superato nello scope |
| Verified → Approved | solo umano | revisione esplicita in coda |
| Candidate/Verified → Rejected | controller o umano | motivo registrato |
| Approved → Rejected | solo umano | motivo registrato |
| Approved → Superseded | solo umano | nuova memoria con `supersedes` |
| qualsiasi → In revisione | scheduler | `expires_at` o `review_after` superato |
| Rejected → altro | nessuno | si crea un nuovo record |

**Vietato:** Candidate → Approved diretto; qualsiasi cambio deciso da un LLM; cancellazione fisica.

**Promozioni:** M2 → M3 solo con `replications ≥ 2` in contesti distinti più test di generalizzazione. M0 nasce solo da decisione umana. Una memoria non esce mai dal proprio `project` senza un nuovo record con scope esplicito.

## 4. Retrieval
1. **Filtro duro:** progetto + `applies_when` + stato. Nell'Esperimento A entrano solo Approved e Verified.
2. **Ranking:** stato, poi specificità dello scope (proxy: numero di condizioni, da validare), poi recenza.
3. **Budget:** massimo 800 token di memoria; ciò che viene escluso va registrato.
4. **Conflitti:** prevale lo scope più specifico, poi lo stato più alto; a parità, **nessuna delle due viene iniettata** e il caso va in coda umana.
5. **Formato nel prompt:** blocco marcato come *dati di contesto* (difesa base da memory poisoning).

## 5. Protocollo dell'Esperimento A

### Domanda e ipotesi (da fissare prima dell'esecuzione)
- **H0:** il tasso di regressione di ACR non è inferiore a quello della checklist senza memoria.
- **H1:** ACR riduce il tasso di regressione di almeno il 30% relativo, con costo in token ≤ 1,5× la checklist.

### Bracci
| Braccio | Input della revisione successiva |
|---|---|
| C0 | solo ultima versione e feedback corrente |
| C1 | cronologia piena, troncata allo stesso budget |
| C2 | come C0 più suite di test fissa a ogni revisione |
| C3 | ACR ordine due: memorie verified delle ultime 2 revisioni + vincoli permanenti |
| C4 | ablazione: ACR con tutte le memorie verified |

Confronto decisivo: **C3 vs C2**.

### Condizioni fisse
Stesso modello, temperatura, budget di token, massimo 6 revisioni, stessi test.

### Compiti
- 12 compiti web in 3 famiglie (landing, form, navigazione mobile) con sequenze progettate per creare trappole di regressione.
- 8-12 test deterministici per compito: axe-core, Playwright mobile, validazione HTML, Lighthouse, lint.
- 5 ripetizioni per braccio e compito: 240 esecuzioni (300 con C4).
- 3-4 compiti di validazione mai usati nello sviluppo.

### Metriche
- **Primaria:** tasso di regressione = test passati alla revisione n-1 e falliti alla n, diviso i test passati alla n-1.
- **Secondarie:** pass rate finale, revisioni alla convergenza, token e costo, interventi umani, inquinamento della memoria (% poi rifiutate), conflitti in coda umana.

### Approvazione scriptata
Nell'esperimento un oracolo approva se i test passano. La coda umana reale si valuta a parte, come studio di usabilità.

### Analisi
Differenza appaiata C3 − C2 per compito, intervallo bootstrap al 95%, test di Wilcoxon, dimensione dell'effetto. Riportare anche i compiti in cui ACR perde.

### Esiti interpretabili
- C3 batte C2 oltre soglia: valore dimostrato in questo dominio.
- C3 ≈ C2: la checklist basta (risultato utile e pubblicabile).
- C3 ≈ C4: l'ordine due non aggiunge nulla.
- C3 batte C2 ma costa molto di più: analisi costo-beneficio.

### Log delle tracce (obbligatorio)
Per ogni revisione: id esecuzione, braccio, compito, prompt completo, memorie recuperate (id e motivo), memorie escluse per budget, output, esito di ogni test, token, transizioni proposte e applicate.

### Minacce alla validità
Non determinismo (ripetizioni), overfitting ai compiti (set di validazione), test troppo vicini al Curator (scriverli indipendentemente), dominio ristretto (i risultati valgono per l'interfaccia web).

## 6. Fibonacci
Resta un esperimento secondario (B): checkpoint ai passi 1, 2, 3, 5, 8 contro intervalli regolari e checkpoint attivati dagli errori. Si esegue solo se A mostra un effetto.

## 6b. Esperimento C — Proporzione tra impalcatura e compito
Mette alla prova l'ipotesi 61,8% / 38,2% descritta in `Fibonacci_Prompt_Engineering_v2.md`. L'esperimento è indipendente dal sistema di memoria e può usare gli stessi compiti e gli stessi test deterministici di A.

### Ipotesi (da fissare prima)
- **H0:** la quota di impalcatura statica nel prompt non modifica in modo misurabile il pass rate dei test.
- **H1:** esiste una quota ottimale intermedia, e 62% dà un pass rate superiore sia a 50% sia a 80%.
- Se i risultati sono monotoni (più impalcatura, sempre meglio o sempre peggio), H1 è falsificata e il numero aureo non ha valore operativo.

### Disegno
| Braccio | Quota di impalcatura (sul totale dei token del prompt) |
|---|---|
| S30 | 30% |
| S50 | 50% |
| S62 | 62% |
| S80 | 80% |

- **Lunghezza totale del prompt fissa** (per esempio 1.500 token), per non confondere quota e lunghezza.
- **Impalcatura costruita con contenuto pertinente** (ruolo, contesto, vincoli, esempi). Il riempimento con testo irrilevante è un confondente e non va usato.
- **Contenuto del compito invariato nel significato**: si varia solo la sintesi o l'ampiezza della descrizione.
- Stesso modello, temperatura e test di A. 12 compiti × 5 ripetizioni × 4 bracci = 240 esecuzioni, più i compiti di validazione.

### Metriche
- **Primaria:** pass rate sui test deterministici.
- **Secondarie:** aderenza al formato, token consumati, numero di revisioni per convergere.

### Analisi
Confronto appaiato per compito con correzione per confronti multipli. Si riporta la curva quota → pass rate con intervallo di confidenza, e si dichiara se ha un massimo o no.

### Minacce alla validità
Il rapporto ottimale può variare per modello e famiglia di compiti. I risultati valgono per questo dominio e per questo modello.

## 6c. Cosa non affermiamo
- Che Fibonacci governi la progettazione dei prompt: è una metafora organizzativa.
- Che 61,8/38,2 sia ottimale: è un'ipotesi in test (Esperimento C).
- Che la memoria selettiva migliori le prestazioni: è l'oggetto dell'Esperimento A.
- Che gli esempi eliminino le allucinazioni o che l'autocorrezione sostituisca la verifica esterna.

## 7. Piano di lavoro
| Settimana | Attività |
|---|---|
| 1 | schema, logging, suite di test dei compiti |
| 2 | controller JSON/SQLite, retrieval con budget, bracci C0-C2 |
| 3 | Curator e braccio C3, prova su 2 compiti |
| 4 | esecuzione completa di A, analisi, relazione con risultati negativi |
| 5 | Esperimento C (condivide compiti e test di A) |

## 8. Note aperte
- La specificità dello scope come numero di condizioni è un proxy grezzo: va testata.
- Soglie (30%, 1,5×, 800 token) sono ipotesi di partenza da fissare prima del lancio.
