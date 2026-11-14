# M3 — Collegamento LLM e prova esplorativa controllata (v0.9)

## Stato
È stato implementato un runner che può chiamare un provider remoto **solo con chiave API esplicitamente configurata**. I test locali usano un double neutrale e non misurano alcun miglioramento della memoria. Al momento nessuna prova LLM reale è stata eseguita in questa versione.

## Gate prima dell'esperimento preregistrato
1. Isolamento OS/container per HTML e JavaScript generati da un modello; il blocco delle richieste browser non basta come sandbox di sicurezza.
2. Suite separata axe-core, Playwright e Lighthouse controllata per versione e indipendente dal sistema di generazione.
3. Pre-registrazione dei task, dei seed, della versione del modello, del tokenizer, del limite token totale, del rapporto costo/token e delle analisi statistiche.
4. Calibrazione della funzione di successo del task: nessuna modifica non può essere considerata successo, anche se produce zero regressioni.
5. Maggiore numerosità e replicazioni. La prova su 2 task è solo un pilota.
6. Protezione e minimizzazione dei dati nelle tracce: non committare prompt reali, output, token API e risultati privati.

## Come eseguire (solo dopo gate di sicurezza)

```bash
python -m pip install -e '.[test,browser,llm]'
python -m pytest -q
# Copie di fixture sotto controllo, senza accesso ai progetti in produzione
export OPENAI_API_KEY='...'
python examples/run_live_pilot.py --provider openai --model MODEL_ID --revisions 2
```

Nota: il prompt live deve essere verificato con tokenizer e versione del modello scelto, perché l'encoding `o200k_base` qui serve come limite operativo approssimativo, non come contabilizzazione esatta API. I conteggi effettivi vengono acquisiti dalla risposta del provider. I modelli potrebbero non rispettare il formato JSON: in tal caso l'esecuzione fallisce esplicitamente, senza inventare dati.

## Sicurezza
Il modulo genera soltanto HTML in copie locali e blocca nel browser le richieste esterne. Non esegue strumenti terminale a partire dagli output del modello. Il browser non è un contenitore di sicurezza completo: eseguire prove reali in ambiente isolato, su fixture fidate, prima di estendere l'input a contenuti non fidati.

## Interpretazione
Un miglioramento C3 non è una scoperta finché non è misurato su task numerosi, in condizioni appaiate e con intervalli di confidenza, costi effettivi e risultati negativi inclusi.
