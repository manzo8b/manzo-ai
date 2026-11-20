# MANZO AI — Sprint 1 · Home come percorso di apprendimento

**Intervento:** 20 novembre 2026  
**Obiettivo:** rendere immediatamente comprensibile l'offerta per cittadini, studenti, professionisti, formatori e persone senza competenze AI, senza aggiungere finte funzionalità né rifare i corsi.  
**Pagine interessate:** \`/manzo-ai/it/\`, \`/manzo-ai/en/\`, \`/manzo-ai/es/\`.  
**Elemento escluso per istruzione esplicita:** pagina di ingresso per scegliere la lingua (\`/manzo-ai/\`), selettore delle lingue del sito, relativi effetti e animazioni. **Nessun file del componente lingua è stato modificato.**

## Direzione artistica e pedagogica

Una Home didattica non deve iniziare con tredici copertine e chiedere al visitatore di dedurne una progressione.

La nuova idea distintiva è il **Learning Blueprint**: il metodo visibile diventa l'elemento formale, dalla domanda fino al prodotto. Quattro verbi costituiscono la grammatica del progetto:

1. **Comprendi** — fatti, possibilità e limiti dei modelli
2. **Sperimenta** — prompt e risultato comparabile
3. **Verifica** — fonti, incertezze e condizioni di arresto
4. **Costruisci** — progetto civico Centroni City come caso reale di progettazione, senza spacciarlo per sportello ufficiale

Le quattro schede hanno destinazioni reali, valide per ciascuna lingua e verificate nell'output di build. Il percorso non promette un diploma né progresso salvato.

## Applicazione delle Skill di AI Web Production

- **Apple Design:** proporzioni tipografiche fluide, feedback immediato nei comandi, focus visibile, transizioni brevi, riduzione del movimento; nessuna manipolazione del selettore lingua.
- **Hallmark v2.0:** un'idea basata sul soggetto (il processo formativo), una sola interazione utile sul catalogo, tonalità distinte per le quattro fasi, niente numeri inventati, componenti leggibili anche con JS disattivato.
- **design-taste-frontend:** Home come sequenza editoriale intenzionale; quattro fasi con output pratici anziché card generiche. Nessun gradiente scuro decorativo e nessun mockup di un prodotto inesistente.
- **Impeccable:** riduzione della quantità iniziale di scelte, tipografia più leggera, gerarchia, responsive, no-JS fallback, messaggi localizzati e qualità dei link. L'eseguibile proprietario del launcher della skill non è stato eseguito in questa sessione: sono stati applicati i principi delle istruzioni disponibili, senza attribuirsi audit automatici non effettuati.

## Modifiche

### Hero
- Nuovo titolo e sottotitolo in IT, EN ed ES; una promessa comprensibile a persone diverse.
- Un'azione per accedere al metodo e un'azione per visitare l'Academy.
- Schema leggero \`capire / provare / verificare / costruire\` come motivo visivo del processo.
- **Ricerca, gateway, sidebar, voce di chi cura il progetto e navigazione precedente preservati.**

### Quattro passi
- Sostituzione editoriale delle card di ingresso ridondanti con quattro tappe progressive.
- Quarta tappa: AI Product Builder con Centroni City nelle tre lingue, non un caso generico.
- Nessuna nuova funzione legale o civica: la pagina rimanda al corso educativo.

### Academy nella Home
- Tutte le **6 card originarie e 7 card aggiunte** sono ancora nel codice e accessibili.
- Per il primo caricamento JS, vengono esposte **4 card**; il pulsante localizzato consente di mostrarle tutte o tornare alla selezione.
- Senza JavaScript, **tutte e 13** le card restano visibili e cliccabili; il pulsante è nascosto.
- Lo stato dell'espansione è rappresentato con \`aria-expanded\`, \`aria-controls\` e un breve annuncio \`aria-live\`.
- Per il catalogo esteso resta la pagina Academy, che contiene i percorsi completi.

## Implementazione e reversibilità

- Publisher: \`theme/publish-sprint1-home.py\`.
- CSS circoscritto: \`theme/sprint1-home.css\`.
- JavaScript senza richieste esterne, archiviazione o tracciamento: \`theme/sprint1-home.js\`.
- Test browser: \`theme/sprint1-home-browser-smoke.py\`, più l'aggiornamento dei contratti di \`theme/browser-smoke.py\` e \`theme/home-showcase-browser-smoke.py\`.
- Inserimento **dopo** i publisher delle card, prima di SEO/integrità HTML, nelle workflow \`deploy-pages.yml\` e \`theme-qa.yml\`.
- Per annullare, basta rimuovere le due invocazioni del publisher dai workflow e ricostruire il sito; le pagine dei corsi non cambiano. Nessuna migrazione del database.

## Gate di controllo

- [x] Sorgenti IT/EN/ES e asset creati
- [x] Publisher incluso nel processo di deploy
- [x] Primo errore di verifica da HTML escape corretto
- [x] Deployment principale GitHub Pages riuscito sul commit \`c2a9a55576\`
- [ ] Browser QA finale 1440/390 px nelle tre lingue — **controllo in corso al momento della redazione**
- [ ] Ispezione visiva umana del rendering su iPhone Safari e desktop reale (distinta da test Chromium)
- [ ] Feedback dell'utente sulla nuova architettura dopo visione pubblica

Il successo CI non equivale a prova di accessibilità WCAG completa, efficacia pedagogica misurata o qualità estetica approvata dall'utente.

## Vincoli preservati

- **0 €** di nuovi servizi
- Nessun conto utente, stato di apprendimento fittizio, registrazione o tutor AI non reale
- Nessuna perdita di contenuti, URL, link, strumenti o card
- Nessuna alterazione del menù lingue o delle sue animazioni
- Nessun titolo che termina con il punto

## Prossimo passo

Dopo il browser QA, aprire le Home IT/EN/ES su desktop e iPhone. Correggere solo i problemi osservabili e verificare l'effettivo effetto sulle scelte. Lo Sprint 0 prosegue separatamente per la localizzazione di AI Teaching Lab; non si deve confondere il nuovo design della Home con il completamento della piattaforma trilingue.
