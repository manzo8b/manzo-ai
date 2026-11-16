# MANZO AI — Benchmark funzionale Coursera e roadmap pedagogica

Data: 16 novembre 2026 — Ambito: IT / EN / ES — Stato: riferimento operativo.

## 1. Che cosa fa Coursera (fonti verificabili)

| Dimensione | Fonte Coursera | Realtà MANZO AI |
|---|---|---|
| Catalogo con filtri per tema, durata, livello, lingua, tipologia | https://www.coursera.org/courses | Sei schede realmente pubblicate; ricerca e filtri per tema, senza durata/valutazioni inventate |
| Percorsi guidati per obiettivo | https://www.coursera.support/s/article/learner-000002219?language=en_US | Tre itinerari costruiti da contenuti esistenti; nuova funzione di questa PR |
| My Learning, In Progress, Saved, Completed | https://www.coursera.support/s/article/learner-000001246?language=en_US | Non ancora disponibile: richiede progressi persistenti collegati a identità e iscrizioni |
| Quiz, pratica, verifiche sommative | https://www.coursera.support/s/article/learner-000001563?language=en_US | Test e casi originali, check-list in-memory sulle due guide professionali; quiz B2B server-side non attivi |
| Certificazioni con valutazioni valide | https://www.coursera.support/s/article/learner-000001268?language=en_US | Nessun diploma, badge o certificato accreditato; non introdurli falsamente |
| Percorsi aziendali e gestione skills | https://www.coursera.org/campus/compare-plans/ | Schema PostgreSQL/RLS reale ma zero organizzazioni, progressi, tenant e API distribuite |

**MANZO AI non è Coursera**: il benchmark è sulla qualità della scoperta, della didattica e dell'esperienza utente, non sulla copia dell'interfaccia o di contenuti proprietari.

## 2. Diagnosi verificata sulla piattaforma

### Elementi già validi
- Sito pubblico GitHub Pages con homepage e catalogo in IT/EN/ES, sei schede in evidenza e link funzionanti.
- Due percorsi specialistici: Allucinazioni AI e verificabilità (6 moduli e 10 casi) e Engineering Assurance nel coding (6 capitoli e 4 scenari).
- Quattro lezioni nell'Academy su modelli linguistici, prompting, verifica, workflow e archivio didattico M01–M06.
- Ricerca e filtro nella Academy, quiz pubblici e progressi didattici solo in memoria sui due moduli specialistici.
- Supabase Auth pilota funzionante; database con 15 tabelle RLS, migrazioni 0001–0003 e email transazionale.
- Backup e restore applicativo verificato, ma NON restore integrale Supabase Auth/SMTP.

### Lacune da non nascondere
- Account "My Learning" con ripresa cross-device, iscrizioni, progressi e risultati persistenti;
- accessi e ruoli amministratore/docente realmente collegati ad API;
- metadata completi per tutti i programmi (obiettivi, prerequisiti, livello e durata realmente validata);
- rubriche e valutazioni uniformi nei sei moduli; attestati rigorosamente verificati;
- gestione programma B2B, isolamento tenant end-to-end, audit, assistenza e contenuti versionati;
- hardening autenticazione, origine privata dedicata, legal/privacy commerciale.

## 3. Percorsi guidati originali (intervento implementato)

Le sequenze seguenti sono orientamenti educativi; NON sono nuove iscrizioni, programmi accreditati o certificazioni:

| Obiettivo | Sequenza di lezioni reali |
|---|---|
| Fondamenta | Come funziona un modello linguistico → Come costruire un prompt efficace → Progettare un workflow AI |
| Verifica | Come funziona un modello linguistico → Come verificare le risposte AI → Allucinazioni AI e verificabilità |
| Coding | Come costruire un prompt efficace → Come verificare le risposte AI → Engineering Assurance nel coding |

Il publisher legge sempre titoli, URL e disponibilità dai sei contenuti effettivamente presenti nella build. Se l'editor modifica il catalogo, la pipeline interrompe il deploy quando i collegamenti non sono più coerenti. Il selettore è accessibile da tastiera e consente la stampa, senza memorizzare o profilare gli interessi.

## 4. Esperienza didattica target

1. **Scoperta**: home → catalogo → obiettivo o filtro, senza sommergere l'utente con opzioni.
2. **Orientamento**: scopo, livello, prerequisiti, risultati osservabili e programma; non inventare durata, certificazioni o valutazioni.
3. **Apprendimento**: moduli brevi e strutturati con esempi e fonti esplicite.
4. **Pratica**: esercizi di recupero attivo con spiegazione dell'errore e criteri di correzione.
5. **Verifica**: distinguere quiz autonomi client-side da prove vincolanti valutate sul server.
6. **Continuità**: proseguire dal punto lasciato solo con account autenticato e stato affidabile; oggi non promettere progressi sincronizzati.
7. **Prossimo passo**: collegare sempre a risorse esistenti, evitando route vuote.

## 5. Criteri design/UX e QA

- Identità MANZO AI: sfondo bianco, blu/teal/coral distintivi, no nero come base e no colori deboli/avorio.
- Card moderne con effetto moderato al passaggio del mouse; outline di focus e movimento ridotto rispettati.
- Gerarchia editoriale e spazio, titoli H1–H6 senza punto finale, CTA coerenti e leggibili.
- Smartphone e desktop (390/768/1440), navigazione con tastiera, aria-pressed, stampa nativa e fallback senza JavaScript.
- Nessun tracking, cookies, archiviazione in background, annunci, dipendenze JS esterne o false metriche in questa iterazione.
- QA: sei schede e URL validi, tre scelte, tre link per scelta, focus, frecce/Home/End, stampa, riduzione movimento, overflow orizzontale e assenza di eccezioni JS.
- Il QA browser NON equivale a certificazione WCAG, pentest o prova di produzione del backend.

## 6. Stato Supabase e gate

Ultimo controllo in sola lettura sul progetto bjydnaejpxwubmxpnpnv: 1 utente Auth, 15 tabelle B2B con RLS, zero organizzazioni, corsi aziendali, iscrizioni, Edge Functions o bucket Storage. SQL 0004 del catalogo pubblico è nel repository ma NON nel database.

**Non aprire un'API pubblica su tabelle private né mostrare un "My Learning" persistente senza JWT verificato server-side.** Il gate M3b rimane aperto per il ripristino Auth/SMTP e privilegi GRANT. Nessuna modifica DDL/utente/pagamento autorizzata da questo benchmark.

## 7. Priorità

**Autonomo oggi**: implementazione del selettore percorsi, test multilingua, responsive e accessibilità, pubblicazione dopo QA.  
**Prossima iterazione sicura**: audit pedagogico M01–M06, miglioramento navigazione inter-lezioni, robustezza delle fonti, SEO/contrasto.  
**Dopo gate e decisioni titolare**: import catalogo M3, progresso autenticato, My Learning, assessment server-side, amministrazione per tenant e policy commerciali.
