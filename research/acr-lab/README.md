# MANZO AI — ACR Lab v0.9

**Adaptive Cognitive Recursion — laboratorio di ricerca applicata**

## Stato della ricerca

- **Verificati**: schema di memoria, policy di transizione, tracce SQLite, browser checks, replay offline C2/C3 e runner di editing con un test-double senza rete.
- **Non verificati**: vantaggio dell'ACR rispetto a checklist C2, efficacia di Fibonacci, presunto rapporto aureo ottimale.
- **Non eseguiti**: test comparativi reali con modelli LLM e analisi inferenziale preregistrata.

## Installazione

```bash
python -m pip install -e '.[test,browser]'
python -m pytest -q
python examples/run_offline_pilot.py --out experiments/experiment_a/results/offline_pilot
```

Per un pilota AI **opzionale** (richiede API key a consumo e container separato):

```bash
python -m pip install -e '.[test,browser,llm]'
export OPENAI_API_KEY='YOUR_KEY_HERE'  # mai salvare nel repository
python examples/run_live_pilot.py --provider openai --model MODEL_ID --revisions 2
```

Leggere [docs/11_M3_MODELLO_REALE.md](docs/11_M3_MODELLO_REALE.md) prima di qualsiasi prova con provider remoto.

## Metodologia scientifica

- **Esperimento A (prioritario):** confronto C3 checklist+memoria verificata contro C2 stessa checklist senza memoria. Ipotesi nulla: nessun vantaggio.
- **Esperimento B:** checkpoint Fibonacci (condizionato ai risultati A).
- **Esperimento C:** proporzione di struttura e task nel prompt; separato da A. Nessuna proporzione ottimale presupposta.

Storia scientifica e fonti originali dell'utente nei file `docs/` e `sources/user/`. La v0.9 non apporta modifiche ai siti o repository pubblicati.

## Policy di pubblicazione

Questo laboratorio può essere incluso come materiale di ricerca in una branch dedicata del repository `manzo-ai`; non va integrato nel runtime del sito senza una revisione del codice e un PR. Non committare file `.env`, trace SQLite, output reali dei modelli o dati sensibili.
