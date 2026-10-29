# MANZO AI — Revisione cromatica pedagogica v0.7.1

Data: 29 ottobre 2026 · Repository: `manzo8b/manzo-ai` · Stato: intervento visivo dedicato.

## Problema e obiettivo
La v0.7 aveva una struttura coerente ma quasi tutte le superfici e i controlli erano nelle stesse tonalità bianco / grigio-verde / petrolio. Si è differenziato l'uso del colore per favorire orientamento, attenzione e scansione dell'attività didattica, evitando colori saturi sotto paragrafi lunghi.

## Palette semantica
| Colore | Codice | Funzione |
| --- | --- | --- |
| Blu profondo | #244F9B | Navigazione, lezioni, conoscenza |
| Petrolio | #0C615D | Azioni, metodo e pulsanti primari |
| Terracotta | #B13F28 | Pratica, casi, richiami |
| Viola | #67439A | Riflessone, pensiero critico, dilemmi |
| Ambra scura | #7B4B10 | Verifica, quiz, feedback |

Tutti gli accenti scuri hanno rapporto di contrasto almeno 4,5:1 sul bianco e sul canvas chiaro. Sfondo aula, codice tecnico, grafica delle slide e test interattivi mantengono il proprio funzionamento.

## Componenti coinvolti
- Sidebar con fondo tenue sfumato, link attivo più marcato e contrasto selezione.
- Home/ricerca con hero blu–terracotta, chip differenziati, schede con fascia colorata.
- Academy, Risorse, Video e slide: schede, tag, bottoni, callout, gerarchia dei titoli.
- Articoli M01–M06: titoli, sommario, richiami ed esempi.
- Critical Thinking: cards/approfondimenti, cruciverba, dilemmi e relative aree di scelta.
- Prompt Mastery: evidenza dei titoli e codice senza cambiamenti ai contenuti.

## Deployment conservativo
La versione **v0.7** rimane la fonte dei dati e della navigazione: il sito è ancora generato da `site-v0.7.zip`. La nuova risorsa testuale `theme/learning-colors.css` è concatenata in fondo a `_site/style.css` da GitHub Actions al momento della pubblicazione; il controllo `theme/check-theme.py` confronta **byte per byte** tutti i 105 file originali diversi da `style.css`, convalida gli 82 HTML, gli stylesheet collegati e il contrasto della palette.

Il risultato è una *patch grafica* indipendente e reversibile, senza nuovo ZIP, senza modifiche alle 82 pagine, al JavaScript, a PDF/PPTX, ai dati interattivi o alle notizie. La Business Academy non fa parte di MANZO AI e non viene toccata.

## Accettazione
1. CI PR: integrità della v0.7, contrasto, struttura CSS, controllo dei percorsi localizzati.
2. Deploy GitHub Pages concluso con successo.
3. Controllo manuale: homepage IT/ES/EN, lezioni, quiz, cruciverba, laboratorio tecnico e smartphone.
4. Nessuna novità contenutistica o commerciale e nessuna raccolta dati.

Si tratta di una revisione dell'interfaccia, non di un certificato di accessibilità formale. Il feedback dell'utente resta decisivo sull'intensità dei colori.
