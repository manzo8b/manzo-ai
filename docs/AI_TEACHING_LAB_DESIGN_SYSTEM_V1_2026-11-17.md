# MANZO AI · AI Teaching Lab — Design system educativo v1.0
Data: 17 novembre 2026
Ambito: Studio immagini, Studio voce, Studio video, Workspace multimediale e navigazione dei laboratori

## Principio di progettazione
Il docente principiante deve sempre sapere: **cosa fare, perché farlo, cosa scrivere, come riconoscere un buon risultato, quale sarà il passo successivo**. La pagina non è un modulo amministrativo: è un percorso formativo interattivo.

## Palette definitiva proposta
- Background pagina: **#FFFFFF** bianco puro
- Testo principale: **#111827** quasi nero, alto contrasto
- Testo secondario: **#253044** antracite leggibile
- Blu strutturale: **#205BEB** per navigazione, call to action principali, esempi e Studio immagini
- Blu tenue: **#E8F0FF** solo per piccole superfici informative
- Arancione operativo: **#E97E17** per azioni secondarie attive e Studio voce
- Arancione tenue: **#FFF0DF**
- Rosso correzione: **#DF3D34** per errore/necessità di revisione, oltre che accento editoriale del video
- Rosso tenue: **#FFE8E4**
- Giallo verifica: **#EDB120** per attenzione/bozze e punti di riflessione
- Giallo tenue: **#FFF0B8**
- Verde approvazione: **#12693B** per stato approvato (semantico, solo quando vero)
- Bordi neutri: **#AAC5EA** su sfondo bianco

Non usare rosso per approvazione, verde per bozza, o colore come unico indicatore di stato. Testi su fondo giallo, arancione e rosso tenue devono restare scuri.

## Card e layout
1. Header card: numero progressivo, verbo d'azione e domanda didattica. Niente punto finale ai titoli.
2. Bordo superiore di 6px, colore funzionale. Fondo card bianco, non beige/grigio carta.
3. Ogni card include **Che cosa deve fare il docente?** e un esempio realistico, non soltanto l'etichetta di campo.
4. Le card di accesso ai tre studi hanno identità cromatica distinta, descrizione di 1 riga e affordance chiara.
5. Desktop: colonna operativa + pannello di stato. Mobile: singola colonna e sezioni riducibili; evitare muri di testo.
6. Separare il contenuto formativo dalle note tecniche (es. JSON, browser, licenze), con «Per saperne di più».

## Campi, tendine, search e controlli
- Label sempre leggibile in #111827, mai placeholder usato come unica istruzione.
- Una frase «cosa inserire» + esempio: distinguere chiaramente esempio da valore compilato.
- Focus con anello arancione; errore esplicito testuale e bordo rosso.
- Selezioni con etichette in linguaggio umano e definizioni comprensibili per principianti.
- Il completamento e l'approvazione sono azioni distinte; una modifica invalida la precedente approvazione.
- Import/export: spiegare formato e posizione del file senza assumere competenze tecniche.
- Contrasto e focus testati secondo WCAG 2.2 AA; non dichiarare conformità senza audit.

## Microcopy pedagogica — modello
- Etichetta: **Titolo del kit**
- Spiegazione: «Dai un nome breve alla risorsa che userai in classe».
- Esempio: «Il viaggio di una goccia d'acqua» (non «Scienze»).
- Criterio di qualità: «Un collega comprende tema e scopo leggendo il titolo».
- Azione successiva: «Adesso scegli classe e destinatari».

## Mappa delle priorità
**P0 — comprensione docente:** microcopy, esempi e guida passo passo in tutti i campi chiave, mobile/desktop, stati di errore.
**P1 — coerenza visiva:** palette/tokens, tipografia, card, CTA e navigazione unificati su quattro studi.
**P2 — navigazione fluida:** sezioni accordion su mobile e desktop, indicatore progressi, ripresa del punto di lavoro; evitare scroll interminabili.
**P3 — accompagnamento pratico:** esempio completo esplorabile e compiti autentici, suggerimenti contestuali e mini-criteri di qualità.
**P4 — audit di accessibilità e QA:** test Safari iPhone, Chrome desktop, VoiceOver, tastiera e import/export reali.
**P5 — portfolio/occupabilità:** walkthrough reale breve e case study verificabile senza inventare impatti.

## Stato
La prima revisione beginner-first e contrast-first è applicata al solo Workspace `tools/ai-teaching-workspace/index.html` sul branch main. Questa è una specifica condivisa per estendere progressivamente le stesse regole agli altri tre studi; non dichiara altri moduli già restylizzati o testati.
