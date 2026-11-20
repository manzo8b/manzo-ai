# MANZO AI — Politica di localizzazione integrale / Full-content localization policy

**Lingue obbligatorie:** Italiano (`it`), English (`en`), Español (`es`).

## Principio non negoziabile
Ogni percorso formativo deve essere completo in tutte e tre le lingue. **La traduzione della sola Home, della card o del menu non è sufficiente.** Tutti i contenuti, i titoli di unità, le letture narrative, tabelle, infografiche, rubriche, glossari, quiz, spiegazioni delle risposte, messaggi di errore, casi didattici, laboratorio, componenti interattivi e testi di accessibilità devono essere localizzati.

## Regole editoriali
1. Le lingue mantengono **parità didattica e funzionale**: stessa struttura, esempi equivalenti, obiettivi e controlli, ma scrittura naturale in ciascuna lingua. Non pubblicare testi rimasti in italiano sotto un selettore EN o ES.
2. Le citazioni a fonti primarie e gli URL possono rimanere nella lingua originale della fonte, con didascalie esplicative nella lingua della pagina. Date, contesto e limiti delle fonti devono essere preservati.
3. Le pagine adottano `lang="it|en|es"`, `hreflang` reciproci e un selettore visibile che **mantiene il percorso del corso**, senza rimandare alla Home della lingua selezionata.
4. Il titolo completo non si tronca arbitrariamente sulle card. Design delle card identico secondo [ACADEMY_CARD_STANDARD.md](ACADEMY_CARD_STANDARD.md). Le card di ciascuna lingua devono puntare a una pagina nella **stessa lingua**.
5. Non usare traduzione automatica lato browser come surrogato di un contenuto editoriale verificato.
6. Il gate di pubblicazione deve fallire per **nuovi** corsi se una delle lingue manca o sono incompleti quiz, esercizi e interfaccia.
7. Le pagine IT esistenti restano disponibili durante la migrazione. Non dichiarare il prodotto interamente trilingue finché l'audit di tutte le sezioni e i corsi non è superato.
8. Le varianti devono essere sottoposte almeno a controlli di navigazione, contenuto, accessibilità, layout e usabilità su smartphone.

## Inventario iniziale · 20 novembre 2026

| Contenuto | Italiano | Inglese | Spagnolo | Intervento |
|---|---|---|---|---|
| Corso Allucinazioni (base e Coding) | Presente | Presente | Presente | Controllare parità e UI |
| Prompt vs Skill | Presente | Presente | Presente | 6 letture, quattro grafici, quiz, cruciverba e navigazione trilingue: CI PASS, verifica visiva finale da completare |
| Modelli mentali e affidabilità | Presente | Non presente nel sorgente editoriale | Non presente nel sorgente editoriale | Traduzione integrale + link |
| AI Product Builder — Centroni City | Presente | Non presente nel sorgente editoriale | Non presente nel sorgente editoriale | Traduzione integrale + link |
| AI Teaching Lab | Presente | Non presente nella struttura editoriale EN/ES | Non presente nella struttura editoriale EN/ES | Migrazione estesa: corso, 5 moduli, glossario, scenari, valutazioni, narrazioni |
| Costruire in sicurezza | Nuovo corso | Nuovo corso | Nuovo corso | Pubblicazione simultanea nelle tre lingue |
| Altre pagine MANZO AI incluse nel pacchetto base | Da verificare | Da verificare | Da verificare | Audit puntuale prima della dichiarazione di copertura globale |

**Regola operativa:** registrare lo stato reale del lavoro, non sostituire una traduzione mancante con un reindirizzamento silenzioso al testo italiano.

## Glossario tecnico coerente
- Shadow AI: uso di strumenti AI fuori dal perimetro di approvazione e governo dell'organizzazione; `IA en la sombra` in spagnolo con termine inglese alla prima occorrenza.
- Human-in-the-loop: controllo umano con accesso alle informazioni e potere di fermare o modificare un'azione; `human oversight` nel senso ampio di supervisione.
- Anonimizzazione / anonymisation / anonimización: dati non più riferibili a interessati secondo l'analisi contestuale del rischio di reidentificazione.
- Pseudonimizzazione / pseudonymisation / seudonimización: riduzione del collegamento diretto con l'identità, ma il dato resta personale.
- Prompt injection: istruzione avversa incorporata in input o contenuti di fiducia inferiore; non garantire prevenzione tramite semplice prompt.

## Progressi verificati

- **20 novembre 2026 — Prompt vs Skill:** versioni IT/EN/ES pubblicate; QA GitHub Pages superato (letture 6/6, mappe 4/4, cruciverba 8 termini, quiz 10/10, collegamenti Home EN/ES). Controllo visivo su dispositivi reali da completare.
- **Restano da tradurre integralmente:** Modelli mentali e affidabilità, AI Product Builder — Centroni City e AI Teaching Lab (più gli altri contenuti del prodotto non ancora certificati).

## Collaudo prima del rilascio
Verificare il conteggio delle sei letture nelle tre lingue, tutti gli URL, le attività, le domande con feedback, la mancanza di testi italiani residui nelle UI EN/ES, i tag canonici e hreflang e l'uniformità delle card.
