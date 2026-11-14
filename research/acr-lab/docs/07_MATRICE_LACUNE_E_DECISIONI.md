# Matrice di completezza: v0.6 → v0.7

| Area | Stato v0.6 | Fonte allegata rilevante | Intervento v0.7 | Rimane da fare |
|---|---|---|---|---|
| Corpus teorico Fibonacci | Ridotto a note di scheduling | `Fibonacci_Prompt_Engineering_v2.md` | Reintegrati i sei livelli e la critica delle analogie | Verifica sperimentale |
| Esperimento A | Documentato ma senza LLM | `MANZO_AI_ACR_v0.4.md` | Conservato e collegato al programma integrato | Pilot C2 vs C3 in sandbox |
| Esperimento B | Accenno nei documenti | Entrambi | Protocollo, bracci e budget audit espliciti | Registrazione e implementazione scheduler |
| Esperimento C | **Assente** | Sezione 6b della v0.4 | Protocollo separato e manifest draft | Prompt reali equivalenti, API/tokenizer, test |
| Rapporto 61,8 / 38,2 | Non messo alla prova | Entrambi | Falsificabilità e controlli 60%/65% | Dataset, analisi preregistrata |
| Confondimento lunghezza/rapporto | Non trattato | v0.4 fissa 1500 token | Studio C in due fasi, confronto semantico e fattoriale | Audit umano delle varianti |
| Ordine degli elementi | Non considerato | Documento Fibonacci v2 | Controllo di posizione/ordine, randomizzato o fisso per braccio | Generatore varianti e validazione |
| Stato dell'arte | Prevalenza memory systems | Entrambi | Fonte verificata su prompting e memoria | Revisione sistematica strutturata se si vuole pubblicare |
| Sicurezza della memoria | Policy, no gateway completo | v0.4 | Riconfermato per A | Autenticazione ed evidence registry |
| Risultati di efficacia | Nessuno | nessuno | **Nessuna cifra inventata** | Esecuzione studi A/B/C |

## Tre problemi scientifici irrisolti (non nasconderli)
1. **Identificabilità dell'effetto percentuale**: a lunghezza totale fissa, varia necessariamente la massa di informazioni associata a ogni sezione. Uno studio Cβ misura una strategia di distribuzione, non un 'numero aureo' in isolamento puro.
2. **Potenza e dipendenza dei dati**: 12 task e 5 ripetizioni sono un pilot, non campioni statisticamente indipendenti di 60 task. Bootstrap a cluster per task e campione confermatorio separato.
3. **Validità esterna**: benchmark web UI non prova che risultati si estendano alla multimodalità o a modelli diversi.

## Gate di avanzamento
- G0: integrazione documentale (questa versione) — **completato**.
- G1: runner C2/C3, logging di prompt, token, costi, evidenze — **aperto**.
- G2: pilot controllato di A — **non eseguito**.
- G3: analisi A e decisione motivata su B — **non eseguito**.
- G4: generazione controllata di prompt e studio C indipendente — **non eseguito**.

**Decisione:** non presentare v0.7 come un risultato scientifico nuovo; è una versione di integrazione delle fonti e dei protocolli, compatibile con il codice v0.6.
