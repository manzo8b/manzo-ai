# MANZO AI — Home V2 | Revisione trilingue e scatola magica

**Data:** 20 novembre 2026
**Branch:** preview/home-magic-trilingual-v2
**Stato:** candidata completa su branch separato, **non distribuita sul sito pubblico**. Nessuna modifica al branch main né al menù delle lingue.

## Idea editoriale

La Home non è il catalogo. La Home genera una domanda e aiuta a decidere dove approfondire.

- IT: «L’IA ti ha risposto con sicurezza. Ma è vero?»
- EN: «AI answered confidently. But is it true?»
- ES: «La IA respondió con seguridad. ¿Pero es verdad?»

Metafora distintiva: **la scatola magica** si apre mostrando simbolicamente domanda, metodo e prova; si richiude e riparte lentamente. Morale: la magia incuriosisce, il metodo rende autonomi. È un SVG animato con CSS, non un video, un'immagine generata o una dipendenza esterna.

## Sei sezioni nelle tre lingue

1. Hero con promessa, due CTA e scatola animata con pausa/riprendi
2. Quattro domande di ingresso ai contenuti pubblicati
3. Sei card coerenti, i cui titoli e collegamenti derivano dai cataloghi Academy nativi
4. Docenti e professionisti con percorsi appropriati
5. Una sfida di pensiero critico, con destinazione verificata nella Home precedente
6. Chiusura con riferimento all'autore, MARCELUS AI LAB e Academy

**Academy:** le sei card originarie sono preservate. Una lista separata con i sette corsi aggiuntivi ne garantisce la reperibilità senza trasformare l'Academy in una copia della Home.

## Invarianti

- Architettura completa IT/EN/ES, senza attendere un successivo restyling linguistico
- Menù lingue, effetti, animazioni, sidebar, topbar, footer e gateway iniziale conservati
- Nessuna modifica ai corsi o quiz
- EN/ES non fingono che AI Teaching Lab sia già tradotto integralmente: il collegamento è esplicitamente verso il corso italiano
- Nessun livello, durata, certificazione o metrica inventati
- Nessuna API, servizio a pagamento, database, nuovo font o tracciamento
- Decorazioni SVG inline, niente librerie di animazione
- Riduzione movimento: la scatola appare aperta, senza animazione
- Comando accessibile pausa/riprendi; animazioni sospese fuori schermo
- Senza JavaScript, link e contenuti restano disponibili

## File del candidato

- theme/publish-home-magic-v2.py — pagine native IT/EN/ES, collegamenti e indice Academy
- theme/home-magic-v2.css — design responsivo e scatola in movimento
- theme/home-magic-v2.js — pausa/riprendi e gestione movimento
- theme/home-magic-v2-browser-smoke.py — browser QA desktop/tablet/mobile, motion e no-JS
- .github/workflows/home-magic-v2-preview.yml — build, test e screenshot su branch senza deployment GitHub Pages

## QA

Prima esecuzione riuscita: [GitHub Actions #44751048913](https://github.com/manzo8b/manzo-ai/actions/runs/44751048913) — build, collegamenti, screenshot nelle tre lingue a 375, 768 e 1440 px, pausa/riprendi, reduced motion e fallback senza JS.

Revisione finale: [GitHub Actions #44751534406](https://github.com/manzo8b/manzo-ai/actions/runs/44751534406) — include sospensione della grafica fuori vista e screenshot separati: attendere esito prima della chiusura.

Il QA automatizzato non equivale a WCAG 2.2 AA certificato né a verifica Safari/iPhone su dispositivo fisico. Nessuna metrica Lighthouse è stata inventata.

## Gate di pubblicazione

**Attendere la convalida dell'autore della versione completa trilingue**. Solo allora integrare il publisher nel workflow Pages di main, correggere i vecchi test Home che contano le 13 card, rieseguire la build, ispezionare desktop/iPhone e distribuire. L'eventuale approvazione della grafica non equivale alla conclusione della localizzazione di AI Teaching Lab.

**Nessuna pubblicazione pubblica è stata autorizzata o effettuata in questa fase.**
