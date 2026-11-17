# AI Teaching Lab — Sprint UX 8.5 · 17 novembre 2026

## Scopo
Elevare la chiarezza pedagogica e la qualità percepita del laboratorio oltre il prototipo a form, con una guida credibile per docenti principianti.

## Lavori eseguiti su main
- **Studio immagini**: pagina bianca, testi scuri, card con accenti funzionali, introduzione a tre fasi, guida iniziale, 11 indicazioni contestuali sui campi, esempio di brief compilabile, handoff visibile al Workspace, gestione delle frecce da tastiera tra le fasi.
- **Studio voce**: stesso linguaggio visivo, 12 indicazioni contestuali, esempio di copione/brief, guida alla registrazione e trascrizione, handoff, navigazione da tastiera.
- **Studio video**: stesso linguaggio, 10 spiegazioni contestuali sui campi statici e istruzioni sui campi dinamici per scena, esempio di brief, handoff, frecce da tastiera.
- **Workspace**: precedente guida per principianti e 10 esempi guidati conservati; ora 5 step visibili (progettazione, raccolta, sequenza, revisione, consegna), modalità «Mostra tutto», comandi avanti/indietro, esempio di progetto compilabile, gerarchia cromatica marcata.
- **GitHub Pages CI**: test di presenza guida, esempio e step navigation aggiunti oltre ai precedenti gate di pubblicazione.

## Identità UI
- Fondo #FFFFFF; testi #111827; blu #205BEB come struttura
- Arancione #E97E17 per attività e supporto docente
- Giallo #EDB120 per attenzione, rosso #DF3D34 per correzione
- Verde soltanto per gli esiti realmente approvati
- Card con bordi evidenti e microcopy comprensibile senza conoscenze tecniche preliminari

## Principio pedagogico
Ogni fase risponde alle domande «che cosa faccio, perché, cosa inserisco, come verifico?». I demo compilano solo contenuti fittizi e non approvano, generano o pubblicano materiale.

## Verifiche effettuate
- Quattro file HTML aggiornati su GitHub
- Tutti gli script inline rilevati nei quattro file passano il controllo di sintassi JavaScript tramite compilazione senza esecuzione
- Marcatori guida, demo, navigazione e link finali presenti
- Workflow aggiornato con gate sui nuovi marcatori

## Non ancora convalidato
- Completamento della nuova build GitHub Pages e risposta HTTP 200
- Rendering visuale e test di interazione effettivi desktop/Chrome e iPhone/Safari
- WCAG 2.2 AA, lettore VoiceOver, contrasto attraverso audit strumentale
- Registrazione audio e video nel browser reale
- Test con un gruppo pilota di docenti

## Valutazione professionale
Obiettivo di qualità visuale/pedagogica: **almeno 8,5/10**; obiettivo di progettazione raggiunto secondo revisione statica, ma **non assegnare un punteggio UX convalidato prima dei test reali**. In una prossima sessione usare desktop e iPhone per consolidare e correggere.

## Collegamenti codice
- tools/ai-teaching-image-studio/index.html
- tools/ai-teaching-voice-studio/index.html
- tools/ai-teaching-video-studio/index.html
- tools/ai-teaching-workspace/index.html
- .github/workflows/deploy-pages.yml
