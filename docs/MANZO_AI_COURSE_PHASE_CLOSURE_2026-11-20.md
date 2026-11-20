# MANZO AI — Chiusura fase 1: ultimi due corsi

**Data:** 20 novembre 2026

**Stato:** corsi completi pubblicati nelle tre lingue; deployment GitHub Pages e QA automatico superati. Il collaudo visivo manuale specifico delle nuove sei pagine resta da confermare.

## 1 · Corsi e materiali

- Compliance dinamica e governance continua — EU AI Act, ISO/IEC 42001 e deriva dei modelli
- Intelligenza aumentata, non sostituita — AI literacy, pensiero critico e collaborazione uomo–macchina

Le sei versioni editoriali sono in editorial/learning/compliance-dinamica-governance-continua/ e editorial/learning/intelligenza-aumentata-non-sostituita/, nei file it.md, en.md, es.md.

Ogni corso mantiene sei letture approfondite, gli esercizi narrativi originali e gli strumenti operativi. Le versioni inglese e spagnola non sono semplici sintesi.

## 2 · Revisione scientifica e normativa

**Compliance:** verifica su fonti primarie della modifica all'AI Act introdotta dal Regolamento UE 2026/1744; attenzione al carattere condizionale dell'articolo 25 e all'impossibilità di dedurre automaticamente obblighi da fornitore dal solo cambio di prompt. Distinzione fra AI Act, ISO/IEC 42001 (sistema di gestione volontario), EN 18286 (QMS per art. 17 nell'ambito pertinente) e GDPR. La deriva è valutata per modello, dati, connettori, scopo e termini contrattuali. I casi sono illustrativi e non pareri legali.

**Intelligenza aumentata:** indagine workslop di BetterUp/Stanford presentata come survey auto-riferita; 1 ora e 51 minuti dichiarati per episodio, arrotondati talvolta a due ore. Ricerca CHI 2025 su 319 professionisti e 936 esempi trattata come correlazionale, non come prova che la IA causi inevitabilmente un declino cognitivo. Laboratorio con due errori deliberati: 30% di riduzione da 1.200 lascia 840 ticket; da 1.200 a 780 è il 35%. Una certificazione ISO 42001 del fornitore non determina conformità automatica dell'utilizzatore. Il protocollo D0–D3 è una proposta di governance interna.

## 3 · Componenti e test

Generatori e localizzazioni: theme/publish-final-two-courses.py, theme/final_two_i18n_base.py, theme/final_two_i18n_aug.py, theme/final_two_quiz.py. Attività client-side in theme/final-two-courses.js e layout responsive in theme/final-two-courses.css. Card Home uniformi attraverso theme/publish-final-two-home.py.

**GitHub Pages:** https://github.com/manzo8b/manzo-ai/actions/runs/44716277409 — deployment completato con successo.

**Esiti dei test di rilascio:** 2 corsi × 3 lingue, 36 letture, 24 diagrammi, 6 laboratori, 6 cruciverba e 60 domande spiegate. Verificati i link nativi IT/EN/ES delle card, la conservazione delle sei card curate originali, 128 URL canonici, 137 pagine e 3.678 link interni.

I simulatori usano dati sintetici, non effettuano chiamate a servizi reali e non certificano conformità o autorizzano decisioni reali.

## 4 · Controlli visuali ancora necessari

Desktop: altezza/allineamento delle card, leggibilità diagrammi e tabelle, apertura letture, feedback dei laboratori e funzione di copia.

iPhone: nessun overflow orizzontale della pagina, scorrimento confinato al cruciverba, pulsanti/select utilizzabili, leggibilità e navigazione locale IT/EN/ES.

Accessibilità supplementare: focus, tastiera, screen reader, messaggi dinamici, contrasto e reduced motion. Il successo CI non sostituisce questi test manuali.

## 5 · Roadmap approvata

Fase 1 conclusa: terminare lo sviluppo di nuovi corsi. L'inventario editoriale ora comprende 6 corsi con sorgenti IT/EN/ES su 9 censiti; restano da completare le traduzioni precedenti di Modelli mentali e affidabilità, Centroni City e AI Teaching Lab, oltre all'audit globale di tutte le pagine.

Fase 2: audit MANZO AI completo, seguito dall'applicazione della metodologia AI Web Production (Apple Design, Hallmark, Impeccable, design-taste-frontend) con correzioni verificabili.

Fase 3: ricerca dei bisogni non ben soddisfatti sul mercato italiano e progettazione di un prodotto originale, misurabile e sostenibile; la novità non va presunta senza analisi dei concorrenti.
