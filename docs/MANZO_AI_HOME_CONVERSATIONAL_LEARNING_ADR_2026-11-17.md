# ADR — MANZO AI Home: ingresso linguistico + discovery conversazionale + catalogo Learning
**Stato (18 novembre 2026):** implementazione sorgente v1 completata per le homepage IT/EN/ES, collegata al publisher e ai test GitHub Pages; **ultima build, deploy e resa visiva reali non ancora verificati**. La pagina radice per scegliere la lingua non è modificata. La sperimentazione con utenti resta da svolgere.
**Data:** 17 novembre 2026
**Repository:** manzo8b/manzo-ai
**Ambito:** root di selezione lingue e homepage IT/EN/ES, prima dei percorsi formativi.

## Problema
La home linguistica è un tratto identitario da preservare. Le homepage interne hanno progressivamente perso la chiarezza dell'interfaccia conversazionale originaria e rischiano di risultare un catalogo tradizionale senza personalità, mentre la piattaforma propone tre aree distinte: Learning, Verify e Studio. Il backend SaaS e l'inferenza IA live non sono ancora operativi: una chat che finga risposte IA sarebbe fuorviante.

## Alternative valutate
1. **Chat pura**: forte identità, ma nasconde catalogo, percorsi e prove di valore; senza backend reale rischia di simulare un assistente.
2. **Coursera pura**: semplice per catalogo e contenuti, ma indistinguibile da molte Academy e sottorappresenta Verify/Studio.
3. **Mix senza gerarchia**: molte sezioni/chat/card concorrenti; peggiora comprensione e mobile.
4. **Discovery conversazionale + catalogo organizzato**: ingresso personale, orientamento per obiettivo, poi prove visibili di contenuti e strumenti.

**Decisione:** alternativa 4. Definizione interna: **Conversational Learning Gateway**. Non clonare la GUI ChatGPT né Coursera; combinare l'orientamento conversazionale con una vera architettura di scoperta formativa.

## Architettura dell'esperienza
### Livello 0 — Selezione lingua, da conservare
- Root /manzo-ai/: mantiene la scelta centrale IT / EN / ES, logo MANZO AI e identità visuale distintiva; non sovraccaricare con il catalogo.
- Semantica e SEO: collegamenti reali alle homepage localizzate, hreflang/alternate se correttamente applicabili, una lingua dichiarata per ogni pagina e nessuna falsa traduzione dei corsi non disponibili.
- Memorizzazione opzionale della lingua solo nel rispetto delle scelte tecniche/privacy del sito; non aggiungere cookie o tracking non necessari.

### Livello 1 — Homepage localizzata per obiettivo
- Header minimale: logo MANZO AI; navigazione chiaramente etichettata **Impara / Verifica / Progetta** e, se appropriate, sezioni Progetto/Chi siamo.
- Hero prima piega: headline non autoreferenziale, ad esempio «Che cosa vuoi imparare o realizzare oggi?».
- Interazione **a forma conversazionale ma onesta**: campo di ricerca/obiettivo e chip «Preparare una lezione», «Migliorare un prompt», «Verificare un contenuto», «Progettare un sito»; risultato = navigazione o suggerimenti basati su contenuti realmente indicizzati, con etichetta **Esplora i percorsi**, NON «Chat con AI» fino all'esistenza di un vero modello backend.
- Distinguere immediatamente: **Ricerca guidata (disponibile)** vs **Assistente IA (non disponibile/non attivo)**. Non simulare messaggi generativi, typing o risposte da un sistema inesistente.
- Prima di qualsiasi scroll lungo: 2–3 card di percorsi verificabili, con livello, obiettivo, durata **stimata** e CTA «Apri il percorso». Non mostrare voti, certificazioni, posti, iscrizioni o avanzamenti inesistenti.
- Segue un catalogo organizzato con filtri per competenza/ruolo/livello; evitare un interminabile feed di card.
- Sezione breve **Impara → Verifica → Progetta**, che chiarisce la relazione tra Learning, Verify e Studio e distingue i prototipi dalle funzioni operative.
- CTA specifiche e autentiche: «Esplora AI Teaching Lab», «Apri Prompt Engineering» etc. Soltanto se le rotte sono davvero attive.

### Livello 2 — Pagine prodotto e formazione
- Learning: struttura stile Academy con moduli, risultati attesi, esempi, prerequisiti, prova formativa e status.
- Verify: processo di analisi di claim e fonti, dichiarando espressamente quando la verifica è euristica o da svolgere manualmente.
- Studio: brief/prototipi e workflow; non promettere agenti IA operativi o pubblicazioni automatizzate se assenti.
- My Learning: accesso e progressi solo dopo la validazione del relativo backend (flag pubblico oggi OFF).

## Regole visive
- Conservare il design distintivo del gateway di lingua.
- Pagine interne: bianco dominante (#FFFFFF), nero #111827, blu #205BEB per struttura e navigazione, arancione #E97E17 per azione, giallo #EDB120 per attenzione, rosso #DF3D34 per errori. Verde solo per approvazioni realmente registrate. Contrasto elevato, niente beige/avorio/grigi carta o home nera.
- Tipografia moderna e leggera, headline incisiva, card attraenti con effetti lievi e rispettosi di reduced motion, bordi funzionali e spaziature coerenti.
- Su iPhone, il hero e l'ingresso al primo percorso devono essere raggiungibili presto; no triplice sticky header, niente caroselli obbligatori o scroll interminabili.
- Nessun punto finale nei titoli.
- Evitare chat bubbles decorative che non corrispondano a interazioni reali.

## Semplice wireframe di contenuto
```text
[ Gateway /manzo-ai/ ] MANZO AI → [ Italiano ] [ English ] [ Español ]

[ /it/ ]
MANZO AI                         Impara · Verifica · Progetta · Menu
──────────────────────────────────────────────────────────────────
Che cosa vuoi imparare o realizzare oggi?
[ Cerca un percorso, una competenza o uno strumento...           ]
[ Preparare una lezione ] [ Migliorare un prompt ] [ Verificare IA ]
         [ Mostra percorsi coerenti con la mia ricerca ]
──────────────────────────────────────────────────────────────────
Inizia da un progetto concreto
[ AI Teaching Lab ]  [ Prompt Engineering ]  [ Verify: fact-check ]
──────────────────────────────────────────────────────────────────
Impara → Verifica → Progetta
[ Principio e percorso ] [ Prova e fonti ] [ Laboratorio e consegna ]
──────────────────────────────────────────────────────────────────
Tutti i percorsi | Filtri per obiettivo e livello | Stato verificabile
[ Informazioni sul progetto, limiti e contatti ]
```

## Contratti reali / stato dei prodotti
L'audit SaaS del 16 novembre 2026 e il README distinguono portale statico pubblico da My Learning e Edge API non distribuite; nessuna nuova funzione deve confondere tali stati. Home conversazionale, al momento, significa **discovery guidata**, non generazione IA.

## Sequenza per Codex
1. Inventaria il gateway e le tre homepage effettivamente pubblicate, confrontando sorgenti e archivio site-v0.7.zip. Evita di modificare l'archivio senza un piano riproducibile.
2. Esegui screenshot baseline desktop/iPhone e registra gli URL disponibili. Se non puoi, segnala NON VERIFICATO.
3. Prepara una variante in branch e screenshot del nuovo hero «Conversational Learning Gateway» per IT; preserva il gateway di lingua. Non clonare ChatGPT/Coursera.
4. Integra soltanto la ricerca guidata effettivamente realizzabile con dati di catalogo reali, con fallback di navigazione; zero risposte IA fittizie.
5. Presenta due varianti di densità (compatta/immersiva) mantenendo LA STESSA architettura, e valuta su utenti principianti; non riaprire la scelta strategica senza nuove evidenze.
6. Propaga il pattern approvato a EN/ES per struttura, ma mostra soltanto traduzioni autentiche; identifica i corsi attualmente disponibili in una lingua diversa.
7. QA: landmark e accessibilità, tastiera, 320–1440 px, performance, SEO, semantica, no regressioni, menu, search, link e salvataggio lingua.
8. Test compare: tempo per trovare AI Teaching Lab, percentuale dei percorsi realmente apribili, errori di comprensione tra ricerca guidata e chat IA, overflow su mobile. Sono **metriche da misurare**, non risultati attestati.
9. Solo dopo gate, integra nella pipeline Pages e aggiorna la documentazione. Non modificare Supabase/Auth/billing durante questa iniziativa.

## Criteri di accettazione
- Lingua scelta in un gateway ancora distinto e riconoscibile.
- Entro una schermata mobile si capisce che MANZO AI serve a **imparare, verificare e progettare**.
- Il visitatore trova senza confusione AI Teaching Lab e gli altri percorsi disponibili.
- L'interfaccia ha carattere conversazionale, ma non millanta un agente IA attivo.
- Contenuti/catalogo coerenti con link reali, accessibilità e corretto stato beta.
- Nessuna alterazione alle parti commerciali o al login.
- Release documentata con screenshot, test PASS/FAIL/NOT RUN, confronto prima/dopo e percorso di rollback.

**Decisione di prodotto:** *Language gateway → Conversational discovery → Learning cards and tools*. La chat IA reale potrà essere una fase successiva quando siano pronti backend sicuro, privacy, limiti e costi.

## Implementazione v1 — 18 novembre 2026

**Source of truth:** `theme/publish-home-conversational.py` con `theme/home-conversational.css` e `theme/home-conversational.js`.

- La ricerca già esistente nella `home-hero` resta utilizzabile; non viene sostituita con un chatbot simulato.
- Quattro obiettivi cliccabili aggiornano una raccomandazione deterministica, il cui collegamento è una risorsa davvero presente nel sito di build. Senza JavaScript ogni opzione è comunque un collegamento utilizzabile.
- I collegamenti a Prompt Engineering e verifica sono estratti dalle **sei card reali dell'Academy** della lingua scelta; il prodotto Studio punta alla demo prodotto della lingua scelta, non a un generatore IA attivo.
- Il Teaching Lab e Mission Studio esistono **per ora in italiano**: i visitatori EN/ES sono avvertiti esplicitamente prima di aprire la risorsa italiana.
- I nuovi suggerimenti sono inseriti **prima della scena decorativa** nella home hero, in modo che su iPhone le azioni siano prioritarie; conservati l'hero originale, la ricerca, le card Academy e i percorsi guidati.
- La radice `/manzo-ai/` con selezione delle lingue rimane intatta.
- Publisher chiamato dopo l'Academy, prima degli ultimi controlli di SEO e integrità.
- Test inclusi: `python3 -m unittest discover -s theme/tests -p 'test_home_conversational.py' -v`, `node theme/tests/test_home_conversational_js.cjs`, verifica `--site _site --verify-only`, e gate nel workflow di deploy.

**Stato dei controlli:** parser JavaScript, struttura delle dipendenze e presenza dei gate sono stati controllati staticamente. Il risultato effettivo dei test eseguiti su GitHub Actions, la pubblicazione e l'audit iPhone/desktop non sono confermati: non dichiarare `LIVE`, `WCAG AA` o efficacia didattica dimostrata.

**Rilascio:** leggere `docs/MANZO_AI_HOME_CONVERSATIONAL_V1_RELEASE_2026-11-18.md` quando disponibile.
