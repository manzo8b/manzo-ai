# Collaudo · Secondo brief di correzione — v0.5

**Data:** 21 novembre 2026 · **Esito:** test locali automatizzati positivi; validazione editoriale dell'autore ancora necessaria.

## Stato degli interventi

| Priorità / punto | Implementato in v0.5 | Verifica |
|---|---|---|
| P0-1 · Registro non anticipa la chiave | Sì | `#record-gap-unlocked` nascosto all'apertura; confronto o salto sbloccano; reset totale riblocca |
| P0-2 · ID neutri | Sì | 1–9 prima, L1–L8 e «Falso allarme» dopo il confronto |
| P0-3 · Stati delle card | Sì | Tre «Anteprima interattiva», testo onesto, dialogo inutilizzato rimosso |
| P1-4 · Hero e H1 | Sì | H1 visibile e unico a 375/768/1440; una hero prioritaria per pagina; pesi annotati |
| P1-5a · Simulatore | Sì | 2 pani + focaccia = **23,00 €**; lunedì = **Non rispettata**; torta ordinata 1 giorno prima = **Non rispettata** |
| P1-5b · Ripetizioni | Sì | 18 esiti disponibili per v1 + 18 per v2; T6 distingue «Nessun errore registrato» / «Almeno un errore registrato» |
| P1-6 · Mappa finale | Sì | Prima congelato, incidente collegato ad A1–A12, Dopo modificabile, totale variazioni, note facoltative e warning senza punteggi |
| P1-7 · Fallback | Sì | HTML essenziale leggibile senza JS, tabelle a scorrimento interno, etichette accessibili |
| P2-8 · Microtesti | Sì | Registro 0 esplicito, Domande guida in maiuscola, eyebrow coerenti, morale aggiornata |
| P2-9 · Sorgenti | Sì | Regenerate da Markdown locale aggiornato; confronto esatto di HTML normalizzato nella suite v0.5 |
| P2-10 · Nomi | Sì, UI | Nomi di stanza nell'interfaccia; gli ID storici degli esperimenti restano soltanto nelle citazioni dei documenti integrali e nei file sorgenti |

## Test eseguiti

- `test_brief_v05.py`: eseguito e completato con **PASS** su 375 / 768 / 1440 px; comprende sblocco, reset, i tre casi numerici, 18 esiti per versione, Prima/Dopo, warning, nessuna chiamata HTTP e assenza di overflow.
- `test_rooms.py` / `test_experience.py`: **PASS** su 375 / 390 / 768 / 1440 px.
- `test_contrast.py`: **122 campioni** di testo normale su superfici solide con rapporto di contrasto **≥4,5:1** a 375 / 768 / 1440 px. Non è una certificazione WCAG.
- `check_source_content.py`, `check_rooms_sources.py`, `test_registry.py`: **PASS**.
- Rendering senza JavaScript: **PASS** su 375 / 768 / 1440 px per tutte le stanze; i testi originali restano nell'HTML.
- Collegamenti interni: **nessun collegamento o ancora mancanti** tra le quattro pagine.
- Build locale `build_for_manzo_ai.py` e `--verify-only`: **PASS** su struttura di staging isolata, poi rimossa. Nessun deploy.
- Verifica con preferenza `reduced-motion` e browser headless: **PASS** funzionale; la navigazione e le scelte rimangono disponibili.

## Decisioni riservate all'autore

1. Approvare la formulazione dei messaggi di avviso in Sala e le caratteristiche didattiche A3, A5, A7–A11: sono ipotesi, non classificazioni legali.
2. Valutare l'efficacia pedagogica con un piccolo test umano, che non si può inferire dai test del codice.
3. Decidere se mostrare sempre «8 lacune» (per ora sì, come da proposta iniziale).
4. Eventuali fonti normative aggiornate per la Sala, oltre l'ambito di questo prototipo.
5. Autorizzare esplicitamente, in un'altra fase, qualunque caricamento su GitHub, merge o pubblicazione.

## Cosa non è stato fatto

Nessuna API AI, nessuna versione ES/EN, nessuna analisi di dati reali, nessun account o analytics, nessuna modifica alla Home principale, nessuna modifica alla PR GitHub #70 o a `main`, nessuna pubblicazione. Le schermate dentro `QA/` mostrano esclusivamente condizioni **simulate manualmente nei test**, non prestazioni di modelli reali.
