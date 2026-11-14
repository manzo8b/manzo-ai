# M2 · Pilota offline C2/C3 — implementazione v0.8

## Scopo
Eseguire identici snapshot HTML con un browser reale sotto due *configurazioni di prompt*:
- **C2** checklist senza memoria
- **C3** stessa checklist e memoria `verified` ricavata **solo** dai risultati del suo braccio

Il browser e la suite di test sono identici. Il registro SQLite è separato per `task × arm` e registra prompt SHA-256, ID di memoria recuperati/esclusi, hash snapshot, versione browser, risultati dei test e metriche.

**Non è un confronto di efficacia**: le quattro revisioni HTML per ciascun task sono prestabilite. Nessun agente modifica autonomamente il codice. Non si può calcolare una riduzione causale delle regressioni né un costo per LLM. Differenze nei prompt non cambiano gli output del replay. Risultati uguali sono previsti *per costruzione*.

## Task di strumentazione (non del dataset definitivo)
1. `navigation_contrast`: rottura menu mobile, ripristino e rottura contrasto (fixture preesistente).
2. `form_layout`: rottura feedback form, ripristino e overflow orizzontale (fixture distinta).

## Memoria
Quando un test passa dopo un FAIL, l'engine C3 propone un record M2 specifico del braccio. Passa a `verified` solo usando il risultato positivo nel registro indipendente ottenuto dal browser, non mediante l'opinione del modello. Ogni memoria contiene una *osservazione verificabile*, non un comando. Per questa versione il registro di verifica è fornito in memoria volatile: resta da integrare una fonte affidabile persistente.

## Budget e stato del prompt
La compilazione può applicare un limite totale con funzione di tokenizzazione passata dal chiamante. Nel replay offline, il conteggio è esplicitamente **byte UTF-8**, non token reali. Gli studi con LLM saranno bloccati finché tokenizer, provider e condizioni identiche non sono definiti.

## Esecuzione
```
python examples/run_offline_pilot.py --out experiments/experiment_a/results/offline_pilot
python scripts/prepare_experiment_c.py
python -m pytest -q
```

## Gate ancora aperti prima di veri risultati A
- Editor LLM o agente identico per entrambi i bracci, con stesso limite globale e prompt hash dei singoli messaggi
- Modello/versione e tokenizer reali bloccati; contabilità input/output e costi
- Suite estesa versionata (axe-core e controlli aggiuntivi) e outcome del task, non solo pass-rate
- Evidence registry persistente, autenticazione e revisione delle memorie
- Task e seed preregistrati, repliche e analisi statistica cluster a livello task
- Workspaces isolati, dati sanitizzati, nessun repository di produzione modificabile

## Regola
L'Esperimento C è indipendente: in v0.8 si preparano solo bozze C-alpha con D byte-identico. Nessuna prova, né regola prescrittiva, sul valore aureo.
