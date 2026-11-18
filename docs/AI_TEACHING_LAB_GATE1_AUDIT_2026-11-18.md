# AI Teaching Lab — audit e Gate 1

Data: 18 novembre 2026. Revisione locale su `codex/teaching-lab-gate1-audit`,
inizialmente da `943ee22`, riallineata a `dd97247` prima del collaudo finale.
Nessun cambiamento ad autenticazione, database, accessi, pagamenti o segreti.

## Stato iniziale verificato

- La cartella della chat non conteneva sorgenti; creata una copia isolata del repository ufficiale. Il checkout preesistente del 3 novembre non è stato modificato.
- Nessun `AGENTS.md` trovato negli ambiti controllati.
- Baseline: 18 test Python, un FAIL nel modulo 05 per prompt desincronizzato tra JSON e Markdown; sintassi JS, contratti e compilazione publisher PASS.
- Actions separava deploy e QA: ultimo deploy osservato riuscito, QA editoriale fallita. Un deploy riuscito non dimostra il superamento dei test del corso.
- Durante il lavoro main ha aggiunto Mission Studio e la home conversazionale: aggiornamenti integrati, senza sostituirli.

## Architettura e inventario

La base delle 82 pagine storiche è `site-v0.7.zip`; i publisher in `theme/`
aggiungono pagine e asset. Per Teaching Lab le fonti sono `it/`, `preview/`
e i cinque strumenti `tools/ai-teaching-*`; correggere il solo HTML generato
non è sufficiente. Eseguito il blocco statico del workflow Pages, senza i
successivi passi Auth/My Learning o una pubblicazione locale fittizia.

Build verificata: 117 pagine prima dei passi autenticati; 108 URL pubblici
in sitemap, 3.137 collegamenti interni, 546 ancore, ID univoci e lingue dichiarate.

Le 14 pagine Teaching Lab generate sono: landing, `modulo-01/` … `modulo-05/`,
`glossario/`, `presentazione/`, `laboratorio-multimediale/`, `inizia/`,
`studio-immagini/`, `studio-voce/`, `studio-video/`, `workspace-multimediale/`.
Traduzioni EN/ES del corso, generazione IA remota e progressi in account
non sono funzioni implementate di questi laboratori.

## Flusso del docente e confini dei formati

Corso → Mission Studio → brief locale → Studio immagini/voce/video → JSON
dello Studio e media originali separati → Workspace → controllo degli originali
e decisione docente → manifest JSON/scheda HTML → riapertura come bozza.

Il brief Mission non è il manifest Workspace: nessuna importazione automatica
tra questi formati è stata introdotta. Le schede mantengono dichiarazioni,
non prove indipendenti della revisione. Il video WebM locale è silenzioso;
audio di riferimento e WebVTT rimangono separati. I cinque schemi v0.1 sono
esercitati dai test, compresi i manifest Workspace normalizzati precedenti.

## Backlog con prove e criteri di accettazione

Nessun P0 confermato. Le priorità seguenti riguardano difetti riprodotti.

| Priorità | Problema e file | Impatto e rischio privacy | Accettazione / esito |
|---|---|---|---|
| P1 | Restore aggirava la validazione, `tools/ai-teaching-workspace/index.html` | Schede con checklist falsa e media assenti risultavano approvate; affidamento didattico errato | Stesso controllo per import/restore, atomicità e regressioni: PASS |
| P1 | Mutazioni durante export video e audio respinto, `tools/ai-teaching-video-studio/index.html` | Crash/risorse non rilasciate e approvazione incoerente | Snapshot, cleanup e invalidazione testati: PASS |
| P1 | Web Speech poteva scegliere voce remota, `tools/ai-teaching-voice-studio/index.html` | Testo potenzialmente trasmesso contro la dichiarazione locale | Solo `localService === true`, nessun fallback remoto: PASS nei test di stato |
| P1 | Uscita/reset/restore potevano perdere lavoro nei cinque strumenti | Perdita di progettazione; nessuna nuova raccolta dati | Conferme, avvisi, token asincroni e import atomico: PASS |
| P1 | Prompt modulo 05 incoerente, `it/narrative.json` | QA rossa e percorsi editoriali divergenti | Test originale nuovamente PASS |
| P2 | Sidebar prima dell'attività, overflow, focus e tab compressi | Ostacoli per docente principiante su telefono | 140 stati a sette larghezze senza overflow/input piccoli/focus fuori viewport/errori: PASS |
| P2 | Select privo di nome, doppio header mobile, `preview/app.js`, `assets.css` | Uso con tastiera e lettore di schermo meno chiaro | Nome accessibile, una barra mobile quando presente il menu; 70 controlli navigazione: PASS |
| P2 | Attribuzione Papert e tutor con due domande per turno, `it/` | Fonte e modello operativo incoerenti | Correzioni minime sincronizzate; unit PASS |
| P2 residuo | Obiettivo con/senza IA del modulo 04 più ampio delle attività | Verificare allineamento nel pilota; nessun rischio dati aggiunto | Revisione successiva ai riscontri, senza riscrittura generalizzata |
| P3 | Interoperabilità opzionale Mission/Workspace e traduzioni | Richiede progettazione e prova dedicate | Non implementata né promessa |

## Verifiche eseguite

Usato Python in ambiente virtuale con Markdown 3.10 e Playwright 1.55.0.
Il Python di sistema non contiene Markdown: l'errore di import del nuovo test
publisher con quell'interprete è un limite dell'ambiente, risolto nel venv e in CI.

| Comando / prova | Esito |
|---|---|
| `python3 -m unittest discover -s editorial/learning/ai-teaching-lab/tests -p 'test_*.py' -v` | PASS, 21 test |
| `node --check editorial/learning/ai-teaching-lab/preview/app.js` e `production-studio.js` | PASS |
| `node theme/check-ai-teaching-lab-contracts.cjs` e `--site ../site-web/manzo-ai` | PASS |
| `python3 -m py_compile theme/publish-ai-teaching-lab.py` e publisher `--verify-only` | PASS |
| `node editorial/learning/ai-teaching-lab/tests/studio-state.test.cjs` | PASS, 14 regressioni |
| `node editorial/learning/ai-teaching-lab/tests/mission-state.test.cjs` | PASS, 8 regressioni |
| `browser-smoke.py`, `production-studio-smoke.py`, `published-browser-smoke.py` | PASS, Chromium 390/1440 px |
| `studios-workspace-smoke.py` | PASS, Chromium e WebKit 390/1440 px |
| `mission-browser-smoke.py` | PASS, Chromium alle sette larghezze; contrasto CTA da colori calcolati dopo tema globale |
| Layout quattro Studi: 320/375/390/430/768/1024/1440 px | PASS, 140 stati |
| Navigazione corso, cinque lezioni e quattro Studi, stesse larghezze | PASS, 70 combinazioni; Tab/Shift+Tab/Escape/Home/End, menu e skip link |
| Pipeline statica completa, SEO e integrità | PASS locale |
| `git diff --check` | PASS |
| Safari iPhone fisico, VoiceOver, microfono fisico, audit WCAG completo | NOT RUN |
| Osservazione con docenti, durata effettiva, efficacia educativa | NOT RUN |

La fixture audio dell'E2E è PCM sintetico senza voce umana. Le spunte effettuate
dal test sono simulazioni di azioni UI, non revisioni realmente svolte da un docente.
WebKit su macOS non equivale a Safari su iPhone; la build WebKit disponibile è
quella congelata per macOS 13. Non è dichiarata conformità WCAG/AI Act.

## Prove e pilota

- [Prima, immagini 390 px](qa/teaching-lab-gate1/immagini-prima-390.png)
- [Dopo, immagini 390 px](qa/teaching-lab-gate1/immagini-dopo-390.png)
- [Mission Studio, pannello finale](qa/teaching-lab-gate1/mission-contrasto-390.png)
- [Riepilogo layout](qa/teaching-lab-gate1/studi-layout.json)
- [Riepilogo navigazione](qa/teaching-lab-gate1/navigazione.json)
- [Protocollo pilota A di 40 minuti, non eseguito](AI_TEACHING_LAB_PILOT_A_2026-11-17.md)

Un docente può progettare una bozza, importare materiali autorizzati, documentare
le proprie verifiche e consegnare schede e media separati. Il protocollo pilota
serve a osservare le difficoltà reali; non dimostra che ogni principiante completi
il percorso nel tempo proposto. Le 20 ore restano una stima, il corso una beta
non accreditata, senza voti ufficiali o certificati.

## Stato del rilascio

Gate tecnico locale superato. PR, CI remota e pubblicazione delle correzioni
vanno osservate separatamente e registrate nel rapporto conclusivo: questa nota
non attribuisce al sito pubblico le modifiche soltanto perché sono committate.
Prima della PR gli undici URL controllati del corso, Mission, lezioni e quattro
Studi rispondevano HTTP 200 sulla release precedente. Rollback delle correzioni:
revert dei commit della PR; nessuna migrazione dati da invertire.

Il docente progetta, l'IA assiste, il docente verifica e decide.
