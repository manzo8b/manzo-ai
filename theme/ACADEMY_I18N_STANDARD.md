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

## Inventario aggiornato · 20 novembre 2026

| Contenuto | Italiano | Inglese | Spagnolo | Intervento |
|---|---|---|---|---|
| Corso Allucinazioni (base e Coding) | Presente | Presente | Presente | Controllare parità e UI |
| Prompt vs Skill | Presente | Presente | Presente | 6 letture, quattro grafici, quiz, cruciverba e navigazione trilingue: CI PASS, verifica visiva finale da completare |
| Modelli mentali e affidabilità | Pubblicato | Pubblicato | Pubblicato | Sorgenti e percorso nativo IT/EN/ES verificati nella pipeline; QA visiva finale separata |
| AI Product Builder — Centroni City | Pubblicato | Pubblicato | Pubblicato | Sorgenti e percorso nativo IT/EN/ES verificati nella pipeline; QA visiva finale separata |
| AI Teaching Lab | 5 moduli e dati strutturati pubblicati | 5/5 moduli narrativi nei sorgenti, non pubblicati come corso nativo | 5/5 moduli narrativi nei sorgenti, non pubblicati come corso nativo | Mancano i file JSON di corso, narrazioni, valutazioni, glossario, scenari e presentazione EN/ES; test e pubblicazione nativi da completare |
| Costruire in sicurezza | Nuovo corso | Nuovo corso | Nuovo corso | Pubblicazione simultanea nelle tre lingue |
| Governare l'autonomia | Presente | Presente | Presente | Sei letture, Mission Control, quattro diagrammi, quiz e cruciverba; CI trilingue PASS |
| Compliance dinamica e governance continua | Pubblicato | Pubblicato | Pubblicato | 6 letture per lingua, 4 diagrammi e Audit Express, registro, quiz e cruciverba; deploy CI PASS |
| Intelligenza aumentata, non sostituita | Pubblicato | Pubblicato | Pubblicato | 6 letture per lingua, 4 diagrammi, laboratorio anti-workslop, Carta Uomo–AI, quiz e cruciverba; deploy CI PASS |
| Altre pagine MANZO AI incluse nel pacchetto base | Da verificare | Da verificare | Da verificare | Audit puntuale prima della dichiarazione di copertura globale |

**Regola operativa:** registrare lo stato reale del lavoro, non sostituire una traduzione mancante con un reindirizzamento silenzioso al testo italiano.

## Glossario tecnico coerente
- Shadow AI: uso di strumenti AI fuori dal perimetro di approvazione e governo dell'organizzazione; `IA en la sombra` in spagnolo con termine inglese alla prima occorrenza.
- Human-in-the-loop: controllo umano con accesso alle informazioni e potere di fermare o modificare un'azione; `human oversight` nel senso ampio di supervisione.
- Anonimizzazione / anonymisation / anonimización: dati non più riferibili a interessati secondo l'analisi contestuale del rischio di reidentificazione.
- Pseudonimizzazione / pseudonymisation / seudonimización: riduzione del collegamento diretto con l'identità, ma il dato resta personale.
- Prompt injection: istruzione avversa incorporata in input o contenuti di fiducia inferiore; non garantire prevenzione tramite semplice prompt.

## Progressi verificati

- **20 novembre 2026 — Ultimi due corsi completati:** *Compliance dinamica e governance continua* e *Intelligenza aumentata, non sostituita* pubblicati con contenuti IT/EN/ES equivalenti; 36 letture, 24 diagrammi, 6 laboratori e cruciverba, 60 domande spiegate; deploy GitHub Pages e test automatici superati. Collaudo visivo manuale specifico ancora da confermare.
- **Copertura fonti editoriali Academy aggiornata: 8/9 corsi** con sorgenti IT/EN/ES presenti secondo la pipeline [GitHub Pages #44725699053](https://github.com/manzo8b/manzo-ai/actions/runs/44725699053). La parità dei sorgenti non certifica né la qualità redazionale né l'intero sito; AI Teaching Lab resta incompleto. Sprint 0: stabilizzazione, nessun nuovo corso.

- **20 novembre 2026 — Governare l'autonomia:** sei letture IT/EN/ES, quattro mappe concettuali, simulatore Mission Control (otto azioni, quattro incidenti, regole di STOP), cruciverba e dieci quiz per lingua; pubblicazione GitHub Pages riuscita. Collaudo visivo manuale su dispositivi reali non ancora eseguito.

- **20 novembre 2026 — Prompt vs Skill:** versioni IT/EN/ES pubblicate; QA GitHub Pages superato (letture 6/6, mappe 4/4, cruciverba 8 termini, quiz 10/10, collegamenti Home EN/ES). Controllo visivo su dispositivi reali da completare.
- **Traduzioni arretrate da completare:** soltanto AI Teaching Lab tra i nove percorsi censiti; altre pagine e strumenti della piattaforma richiedono ancora un audit di copertura integrale. *Modelli mentali* e *Centroni City* sono già localizzati e pubblicati: non ripetere il lavoro.

## Collaudo prima del rilascio
Per ogni corso, verificare il numero effettivo di letture e moduli previsto dalla sua struttura (non assumere sei per tutti), tutti gli URL, attività, rubriche e risposte spiegate, assenza di residui italiani nelle UI EN/ES, canonical/hreflang, selettore della lingua sul medesimo percorso e uniformità delle card. Lo script `theme/audit-academy-i18n.py` misura solo la presenza dei sorgenti editoriali; le pagine native pubblicate vanno testate separatamente.
