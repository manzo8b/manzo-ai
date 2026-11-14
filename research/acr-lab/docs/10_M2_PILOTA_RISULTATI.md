# MANZO AI ACR · v0.8 · Rapporto M2: verifica pilota offline

**Data:** 14 novembre 2026  
**Stato:** infrastruttura verificata, **Esperimento A con LLM NON eseguito**.

## Procedura

- Due task HTML locali indipendenti (`navigation_contrast` e `form_layout`).
- Due bracci C2/C3, quattro snapshot predeterminati per task.
- Catalogo identico di 6 controlli browser: menu, contrasto, form, overflow, titoli, landmark.
- Chromium/Playwright reale; ogni snapshot testato una sola volta e osservazioni immutabili riutilizzate nei due bracci **solo nel replay offline**.
- Registro SQLite append-only applicativo, identificatori di memorie, hash dei prompt e stato delle verifiche.
- C3 riceve un record `verified` dell'ultimo fix osservato dalla propria traccia; C2 resta privo di memoria.

## Risultati tecnici

| Compito | Braccio | Regressioni / transizioni eleggibili | Tasso | Memoria usata al quarto snapshot |
|---|---|---:|---:|---|
| Navigazione e contrasto | C2 | 2/16 | 12,5% | No |
| Navigazione e contrasto | C3 | 2/16 | 12,5% | Sì, mem_1001 |
| Modulo e layout | C2 | 2/16 | 12,5% | No |
| Modulo e layout | C3 | 2/16 | 12,5% | Sì, mem_1001 |

- **4 run**, **16 snapshot logici**, **96 test registrati**, **48 controlli browser eseguiti su snapshot univoci**, **52 eventi SQLite**.
- **44 test software superati** nella suite locale della v0.8.
- **12 bozze Cα** generate con la parte dinamica byte-identica; **Cβ bloccato** fino al blocco del tokenizer e al controllo semantico.
- **0 chiamate LLM, 0 costi API**. Nessun risultato statistico di efficacia ACR.

## Interpretazione scientifica

I risultati C2 e C3 sono **identici per costruzione**: il componente editor non è ancora collegato e quindi la memoria non può influenzare le modifiche. I prompt cambiano, gli snapshot non cambiano. Questo replay NON deve essere usato per stimare l'effetto causale della memoria. I casi e le loro regressioni sono deliberatamente costruiti per verificare la strumentazione; non fanno parte del dataset scientifico preregistrato.

## Cosa è stato verificato

1. Isolamento delle tracce per `task × arm`.
2. Compilazione con medesimo contenuto e politiche base, salvo il blocco di memoria.
3. Registrazione di prove Playwright e creazione/recupero selettivo di memorie verificate.
4. Stessa suite browser e stessi snapshot tra i bracci.
5. Regressioni rilevate e correttamente registrate come PASS→FAIL, senza scambiare test mancanti per PASS.

## Limiti e gate verso il vero Esperimento A

- **Necessario un provider LLM/editor** identico per C2 e C3, in workspace isolati, con generazione e modifiche realmente differenti in funzione del prompt. Nessun provider è configurato.
- Necessari tokenizer reale, tetto globale verificato, usage/costi, versioni e seeds bloccati.
- Evidenze da un servizio fidato persistente; registrazione con policy di accesso e separazione dalle memorie candidate.
- La suite attuale è uno smoke catalog di 6 check, **non** un audit WCAG/axe/Lighthouse completo.
- Necessari task indipendenti e repliche con piano statistico congelato, per evitare test costruiti a favore della memoria.
- I bytes UTF-8 del replay **non sono token LLM**.
- Il materiale Cα è una bozza; non costituisce un'analisi dell'ottimalità del 62%.

## Riproduzione

```bash
python -m pip install -e '.[test,browser]'
python -m pytest -q
python examples/run_offline_pilot.py --out /tmp/acr_offline_rerun
python scripts/prepare_experiment_c.py
```

L'output include `summary.json`, `config.json`, `traces.sqlite3`. Ripetere in directory vuota per preservare il registro.
