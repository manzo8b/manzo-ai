# Nota di ispezione del prototipo originale e decisioni v0.2

## Stato originale verificato

- `index.html`: palazzo futuristico come singola immagine con titolo, breadcrumb e CTA impressi, H1 nativo nascosto su desktop, link trasparente sopra l'immagine. Le luci decorative erano presentate come connessioni significative senza esserlo.
- `banco-di-prova.html`: sei passi; preventivo, prompt e chiave caricati da JS, quindi contenuti principali non leggibili senza JavaScript. Presente frase inaccurata «non generata dall'AI».
- `assets/experiment-data.js`: conteneva testo integrale del documento e prompt e la chiave, con logica JS dipendente dal file.
- `assets/app.js`: rete a stella che accendeva i nodi L1–L8 senza rappresentare affermazioni e fonti; confronto esterno A/B e registro di dieci prove complessive, senza raggruppamento per modello.
- `assets/styles.css`: estetica e navigazione mobile mature, mantenute come base; aggiunti componenti di narrazione ed esercitazione.
- Asset: hero originale WebP 207 KB circa, immagine Banco 379 KB circa, video MP4 allegato 3,5 MB (ottimizzato a circa 208 KB). Nuova hero originale senza lettere, creata per evitare testi disegnati dentro l'immagine.

## Correzioni applicate

**P0:** frase sulla chiave corretta; didascalia ora dichiara decorazione; riferimento interno rimosso; preventivo, prompt, chiave e definizioni visibili anche con JS disabilitato; noscript corretto.

**P1:** due parti (interna e facoltativa esterna), otto affermazioni originali, valutazione tramite radio/select, SVG collegato solo alle scelte effettive, giudizio Prima/Dopo/Chiave, spiegazioni e campo di riflessione; registro di tre modelli con cinque A e cinque B per ciascuno, spunte per lacune e contatori; risultati reali vuoti.

**P2:** doppia numerazione eliminata dal catalogo; topbar in italiano; HTML `<span>` al posto di `<icon>`; hero senza testo e H1 HTML nativo; animazione allegata resa filmato opzionale; legenda sempre testuale; reduced motion e focus visibile.

## Decisioni non prese al posto dell'autore

1. L'efficacia del percorso va valutata dall'autore e, idealmente, con persone reali: i soli test non dimostrano apprendimento.
2. I brevi testi di spiegazione delle frasi R1–R8 sono una proposta editoriale nuova da approvare; le frasi R1–R8 stesse sono identiche al brief.
3. L'immagine di Banco contiene una scritta decorativa nel disegno storico; non è usata come controllo né come sostituto del titolo HTML. Sostituibile con una nuova illustrazione se richiesto.
4. L'animazione è facoltativa perché contiene UI e parole disegnate: non va trasformata in hero cliccabile o testo di navigazione.
5. Nessuna modifica al repository o al sito ufficiale, come richiesto dal brief.
