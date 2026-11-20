# MANZO AI — Home V2 | Revisione trilingue e scatola magica

**Data:** 20 novembre 2026
**Branch:** preview/home-magic-trilingual-v2
**Stato release:** approvata dall'autore il 20 novembre 2026 e integrata nel branch `main` tramite [PR #51](https://github.com/manzo8b/manzo-ai/pull/51), commit `a946802d625dccd2ff72a22d665dad60cf763d4f`. Il workflow GitHub Pages è configurato per applicarla alla build; **l'esito remoto del deploy non è stato verificato direttamente**. Menù delle lingue, relativi effetti e routing invariati.

## Idea editoriale

La Home non è un catalogo né una chat simulata: è una pagina editoriale di apprendimento che genera una domanda e aiuta a decidere dove approfondire. Il precedente vincolo di una Home conversazionale è esplicitamente superato.

- IT: «L’IA ti ha risposto con sicurezza. Ma è vero?»
- EN: «AI answered confidently. But is it true?»
- ES: «La IA respondió con seguridad. ¿Pero es verdad?»

Metafora distintiva: **la scatola magica** si apre mostrando simbolicamente domanda, metodo e prova; si richiude e riparte lentamente. Morale: la magia incuriosisce, il metodo rende autonomi. È un SVG animato con CSS, non un video, un'immagine generata o una dipendenza esterna.

## Cinque sezioni nelle tre lingue · revisione UX del 20 novembre

1. Hero con promessa, due CTA e scatola animata con pausa/riprendi discreto
2. Sei card coerenti, i cui titoli e collegamenti derivano dai cataloghi Academy nativi
3. Docenti e professionisti con percorsi appropriati
4. Una sfida di pensiero critico, con destinazione verificata nella Home precedente
5. Chiusura con riferimento all'autore, MARCELUS AI LAB e Academy

Le quattro porte-domanda intermedie sono state eliminate perché duplicavano le prime card. Numerazione 01/02 riallineata e sei codici card 01–06 invariati. La card 06 usa una tonalità rosa-ardesia, distinta dalla 03 petrolio.

**Academy:** le sei card originarie sono preservate. Una lista separata con i sette corsi aggiuntivi ne garantisce la reperibilità senza trasformare l'Academy in una copia della Home.

## Invarianti

- Architettura completa IT/EN/ES, senza attendere un successivo restyling linguistico
- Menù lingue, effetti, animazioni, sidebar, footer e gateway iniziale conservati; solo il descrittore non-brand della topbar viene localizzato
- Nessuna modifica ai corsi o quiz
- EN/ES non fingono che AI Teaching Lab sia già tradotto integralmente: il collegamento è esplicitamente verso il corso italiano
- Nessun livello, durata, certificazione o metrica inventati
- Nessuna API, servizio a pagamento, database, nuovo font o tracciamento
- Decorazioni SVG inline e CSS luminoso, niente librerie di animazione
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

**Convalida ricevuta e integrazione effettuata.** Il publisher è stato inserito nel workflow Pages di `main`, dopo i generatori precedenti e i controlli editoriali. Verificare conclusione effettiva della pipeline e collaudo Safari/iPhone prima di chiudere il release gate. I vecchi test Home girano prima del nuovo publisher; la verifica finale richiede 5 sezioni e 6 card. L'eventuale approvazione della grafica non equivale alla conclusione della localizzazione di AI Teaching Lab.

**Pubblicazione autorizzata e avviata mediante il merge su `main`.** Il risultato live non può essere dichiarato confermato finché GitHub Actions non completa con successo il job `Deploy to GitHub Pages`.


## Iterazione estetica — ispirazione Pinterest, senza clonazione

Brief approvato in chat: superfici chiare, sfumature luminose azzurro/turchese/lavanda, griglia tecnica semitrasparente, profondità morbida e microinterazioni disciplinate. L'Hero conserva la scatola magica come unica narrazione animata; il resto mantiene gerarchia editoriale e leggibilità. Soltanto CSS radiali, gradients, maschere progressive e pseudo-elementi; nessuna immagine di terzi, nessuna dipendenza, zero nuovo costo.

## Revisione responsive e linguistica del 20 novembre

- A 1100 px e sotto: Hero su una colonna, testo sopra e scatola sotto, senza spezzature artificiose nel titolo
- A 768 px: una card Academy per riga, per preservare spazio utile accanto alla sidebar originale
- A 375 px: barra mobile compatta e screenshot ripresi dall'inizio pagina; una card per riga sotto i 540 px
- Pulsante pausa/riprendi ridimensionato, con etichetta accessibile per screen reader
- IT: «Sai distinguere un’intuizione da una prova?». ES: «decidir por tu cuenta»
- Descrittore topbar IT «Conoscenza e prompt», ES «Conocimiento y prompts», EN invariato «Knowledge & Prompt Lab»
- Test automatici aggiornati: 5 sezioni, 6 card, 7 ulteriori destinazioni Academy, impilamento tablet, navigazione mobile, no-JS e reduced motion

**Release gate:** modifiche committate sul solo branch di anteprima. Lo stato dei precedenti run CI riguarda commit antecedenti a questa revisione: non attribuire automaticamente il loro PASS all'ultima variante. Verificare nuova pipeline, schermate reali Safari/iPhone, contenuti nelle tre lingue e autorizzazione esplicita prima di pubblicare.

## Changelog rilascio · 20 novembre 2026

- PR #51 integrata in `main`, con autorizzazione esplicita alla produzione
- Menu laterale Home: pill ovale effetto vetro, hover lift/luminosità, supporto `prefers-reduced-motion`, `prefers-reduced-transparency`, `prefers-contrast`
- Verifica locale di rendering: 3 lingue × 1440/768/375 px = 9 combinazioni senza overflow orizzontale, con Hero impilato su tablet e card singola su smartphone. Le risorse esterne e la navigazione mobile dinamica non erano caricabili nel renderer inline; non è un collaudo end-to-end del dominio pubblico
- Workflow `.github/workflows/deploy-pages.yml` aggiornato per generare IT/EN/ES, verificare 5 sezioni e 6 card, controllare asset CSS/JS e integrità del sito prima dell'upload Pages
- Attesa di conferma del deployment remoto da GitHub Actions; non affermare che il sito è online con la V2 finché il job non è riuscito
