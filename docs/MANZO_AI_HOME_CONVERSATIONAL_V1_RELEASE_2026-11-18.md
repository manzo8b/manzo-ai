# MANZO AI — Home conversazionale + Academy v1

**Data:** 18 novembre 2026  
**Area:** homepage interne IT / EN / ES  
**Stato:** codice e test pubblicati sul branch principale; il risultato più recente del deploy GitHub Pages e i test visivi di Safari iPhone non sono ancora stati verificati in questa sessione. Non dichiarare `LIVE` o `WCAG 2.2 AA` senza prove.

## Decisione di prodotto
**Gateway lingua → Scoperta conversazionale → Risorse Academy → Studio / Verify / Learning.**

La pagina radice `/manzo-ai/`, con la selezione centrale delle tre lingue, rimane **inalterata**. Il lavoro interessa solo `/it/`, `/en/` e `/es/`.

## Che cosa è stato implementato
1. L'hero esistente mantiene la ricerca originaria e la scena di prodotto; i componenti non sono cancellati.
2. Aggiunta interfaccia guidata con quattro domande operative: progettare una lezione, migliorare prompt, verificare risposte, creare un sito/workflow.
3. Scegliendo un obiettivo cambiano titolo, spiegazione e link suggerito; il comportamento è **deterministico, locale, senza backend o inferenza IA**.
4. Link didattici per Prompt Engineering e fact-check ricavati dalle **sei card realmente pubblicate** dall'Academy della lingua corrispondente, controllati durante la build. Mission Studio è **in italiano**; le homepage inglese e spagnola lo dichiarano.
5. Collegamento Studio alla demo Product Lab reale nella lingua selezionata, **non** a un generatore siti IA attivo.
6. L'interazione resta utilizzabile senza JavaScript grazie ai link nativi degli obiettivi.
7. UI mirata, alta leggibilità: bianco `#FFFFFF`, nero `#111827`, blu `#205BEB`, arancione, giallo e rosso semantici; focus da tastiera, motion reduction, niente scroll causato dagli elementi interattivi progettati.
8. Su iPhone gli obiettivi precedono la scena decorativa, preservando lo spazio per l'azione principale.
9. Le sei card Academy e i tre percorsi guidati già pubblicati restano presenti. Nessun catalogo duplicato.
10. Nessun account, certificato, metrica di iscrizione, generazione IA o valutazione automatica inventati.

## Source of truth
- `theme/publish-home-conversational.py`
- `theme/home-conversational.css`
- `theme/home-conversational.js`
- `theme/tests/test_home_conversational.py`
- `theme/tests/test_home_conversational_js.cjs`
- `theme/home-conversational-browser-smoke.py`
- `.github/workflows/deploy-pages.yml`
- Decisione ADR: `docs/MANZO_AI_HOME_CONVERSATIONAL_LEARNING_ADR_2026-11-17.md`

Il publisher gira **dopo** `publish-home-showcase.py` e `publish-academy-journeys.py`, ma prima dell'audit di integrità e dell'ultimo SEO. Copia asset in `_site/assets/` e aggiorna soltanto le tre homepage di lingua. Non altera `site-v0.7.zip` o la root di selezione linguistica.

## Verifiche eseguite durante la revisione
- **PASS**: compilazione sintattica JS del file `home-conversational.js`.
- **PASS**: esercitazione della logica JS su DOM simulato: scelta iniziale, cambio goal, aggiornamento link, matching lessicale, meta-click nativo.
- **PASS**: verifica statica del publisher e della pipeline: route dal catalogo reale, nessun accesso a servizi IA, nessuna sovrascrittura della landing lingua, supporto responsive e reduced motion.
- **PASS**: verifica sintetica della correttezza delle espressioni regex fondamentali del parser Python.
- **Implementato, esito GitHub non osservato**: test unitario di fixture Python, test Node, gate `--verify-only` nel workflow.
- **Non eseguito**: Playwright sulle pagine servite; audit manuale e strumentale iPhone; esito finale GitHub Actions e pubblicazione HTTP.

## Comandi per Codex / QA
```bash
python3 -m py_compile theme/publish-home-conversational.py
python3 -m unittest discover -s theme/tests -p 'test_home_conversational.py' -v
node --check theme/home-conversational.js
node theme/tests/test_home_conversational_js.cjs

# Dopo il build normale della site directory
python3 theme/publish-home-conversational.py --site _site --verify-only

# Dopo aver servito _site al prefisso /manzo-ai/ e installato Playwright
python3 theme/home-conversational-browser-smoke.py --base http://127.0.0.1:8000/manzo-ai --screenshots /tmp/manzo-home-qa
```

## Gate prima di dichiarare pronta la release
1. GitHub Actions concluse con successo; nessun errore nel publisher o nei gate.
2. URL pubblici IT/EN/ES raggiungibili e root linguistica invariata.
3. Ricerca originale funzionante, quattro obiettivi navigabili, catalogo Academy non modificato.
4. Nessun overflow su 320/390/1440 px e nessun elemento di navigazione sovrapposto.
5. Esame manuale di focus, tastiera, contrasto e lettore schermo.
6. Verifica che nessun messaggio suggerisca un vero assistente generativo non disponibile.
7. Documentazione del prima/dopo e feedback sul tempo necessario per trovare il primo corso; **non inventare metriche**.

## Fuori ambito
Non sono stati modificati Supabase, autenticazione, database, billing, chiavi API, pagamenti, contenuti dei cinque moduli o pagina iniziale di scelta lingua. L'eventuale chat con un vero modello sarà una futura funzione distinta, che richiede backend sicuro, consenso, governance dei dati, costi e limiti documentati.
