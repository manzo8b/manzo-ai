# AI Teaching Lab — Mission Studio v0.1

**Data:** 17 novembre 2026  
**Repository:** `manzo8b/manzo-ai`  
**Stato:** micro-web-app creata e collegata al publisher su GitHub; **deploy pubblico e test visivi iPhone/desktop non ancora confermati**.

## Obiettivo
Un prodotto formativo interattivo mobile-first che accompagna docenti senza esperienza di IA dalla scelta di un obiettivo osservabile al primo brief e al laboratorio giusto, senza fingere una chat IA o un backend ancora assente.

## Source of truth
- `tools/ai-teaching-launchpad/index.html` — codice completo HTML/CSS/JavaScript, nessuna libreria o API remota
- `theme/publish-ai-teaching-lab.py` — pubblicazione statica + SEO e link dalla landing
- `.github/workflows/deploy-pages.yml` — trigger sorgente e gate nuova route
- `theme/check-ai-teaching-lab-contracts.cjs` — contratto strutturale del sorgente e dell'output generato
- `docs/CODEX_MASTER_PROMPT_MANZO_AI_TEACHING_LAB_2026-11-17.md` — master Codex aggiornato per includere la micro-app

**Rotta prevista:** `https://manzo8b.github.io/manzo-ai/it/formazione/ia-per-la-didattica/inizia/`  
**Ingresso:** CTA «Avvia Mission Studio» nella landing del corso.

## Funzioni reali
1. Scelta di quattro missioni: immagini, voce, video, verifica delle fonti.
2. Temi di esempio modificabili e testo libero entro limiti ragionevoli.
3. Destinatari e tempo della microattività (15/30/45 minuti).
4. Obiettivo di apprendimento proposto con criterio osservabile, modificabile.
5. Piano visivo a tre passaggi, evidenza di apprendimento e scelta del laboratorio coerente.
6. Esportazione esplicita JSON (`ai-teaching-lab-mission-v0.1`) e copia del brief testuale.
7. Ripristino di una bozza esportata con conferma di sovrascrittura e validazione dello schema; nessuna approvazione viene importata.
8. Collegamenti diretti ai cinque moduli formativi, ai tre Studi, al modulo di fact-check e al Workspace.
9. Responsive da mobile a desktop; riduzione dei contenuti ornamentali sugli schermi stretti; media query `prefers-reduced-motion`.
10. Dati di lavoro mantenuti in memoria della pagina, senza account, localStorage o rete applicativa.

## Limiti dichiarati
- Non è una chat con un modello IA; utilizza regole editoriali locali.
- Non genera immagini, audio o video: rimanda agli Studi per preparazione/importazione di risorse.
- Il JSON del Mission Studio **non è automaticamente importabile nei form degli Studi** né nel Workspace; si tratta di un brief preliminare distinto.
- Nessuna valutazione automatica dell'apprendimento, nessuna certificazione o misura sperimentale di efficacia.
- Un download del brief non include media binari o credenziali.
- Non raccogliere né inserire dati identificabili di studenti.

## Verifiche effettuate nella sessione
- Sintassi JS inline: **PASS** (compilazione senza esecuzione dell'intera UI).
- ID HTML statici: **PASS** (nessun duplicato rilevato).
- Quattro missioni e relativi collegamenti: **PASS** in prova isolata dei dati e del piano.
- Obiettivi generati: **PASS** su quattro percorsi, evitando errori grammaticali con articoli.
- Obiettivo personalizzato: **PASS** (non viene sovrascritto automaticamente).
- Clausola `approval: false` e dichiarazione di no-IA: presenti nel codice.
- Publisher aggiornato per inserire la rotta, metadata e canonical.
- Workflow e contratti QA aggiornati.

## Test ancora necessari
- GitHub Actions completa: risultato non consultato in questa sessione.
- Pagina pubblica: il tentativo di accesso esterno non ha restituito una verifica attendibile; **non dichiarare LIVE**.
- Playwright desktop/iPhone simulator e Safari iPhone reale: da collaudare, compresi overflow, touch target, import/export in file system iOS.
- Browser clipboard e download JSON: da testare su Safari/Chrome reali.
- Audit accessibilità WCAG 2.2 AA: non effettuato.
- Prove con docenti principianti: saranno coordinate dall'autore del progetto.

## Gate di accettazione per il successivo sprint Codex
**P0** CI/deploy + risposta pubblica; smoke test UI completa, export/import e link nei browser reali; zero crash e zero scroll orizzontale su iPhone.  
**P1** migliorare accessibilità, compattezza e chiarezza delle istruzioni, con screenshot e test.  
**P2** valutare interoperabilità opzionale del brief Mission Studio con campi Studi (senza importare approvazioni né dati sensibili) con piano di migrazione dello schema.  
**P3** solo dopo test con docenti: feedback contestuale più ricco, eventuale API IA protetta e funzionalità salvabili con consenso e policy adeguate.

La home di selezione delle lingue MANZO AI non è stata modificata. Questo sprint riguarda l'applicazione formativa italiana del Teaching Lab.
