# MANZO AI — Audit della tassonomia didattica e dei laboratori
**Data:** 20 novembre 2026 · **Stato:** ricognizione editoriale per una futura IA (information architecture); navigazione non modificata
**Fonti:** sorgenti GitHub `main`, `theme/audit-academy-i18n.py`, `theme/ACADEMY_CARD_STANDARD.md`, `docs/MANZO_AI_GLOBAL_AUDIT_2026-11-20.md`; controllo di titoli, rotte, headings, link, input e script HTML nel pacchetto di staging Home V2 del 20/11/2026 (14:15 UTC). L'artefatto contava 150 file `index.html`, incluse traduzioni, pagine accessorie e schermate pilota. **Non corrispondono a 150 corsi**, e non costituiscono un crawl del sito live dopo l'ultimo deploy.

## Definizioni per evitare doppi conteggi
- **Percorso principale**: sequenza didattica autonoma con obiettivi; nel conteggio di base includiamo i 9 corsi del registro editoriale e i 6 moduli fondativi M01–M06 (come unità di apprendimento, non corsi professionali equivalenti).
- **Sottounità**: capitolo/modulo appartenente a un corso principale (es. i 5 moduli Teaching Lab e il coding specialistico).
- **Laboratorio interattivo**: percorso o componente con strumenti per inserire scelte/input e svolgere verifiche. Un input non prova automaticamente correttezza pedagogica o persistenza.
- **Laboratorio guidato**: compito descritto in pagina, da svolgere offline/con applicazioni esterne, eventualmente con soluzioni/rubrica. Non equivale a un laboratorio interattivo nel sito.
- **Quiz statico**: domande e spiegazioni già nel documento, senza correzione interattiva nella stessa pagina.
- **Risorsa**: podcast, slide, fonti, notizia, glossario, ricerca; non si conta automaticamente come corso.

## Numeri verificabili nel perimetro censito
| Oggetto | Numero | Rapporto |
|---|---:|---|
| Corsi editoriali principali registrati in `audit-academy-i18n.py` | 9 | 8/9 con sorgenti IT/EN/ES completi; AI Teaching Lab ancora incompleto nella pubblicazione EN/ES |
| Moduli del percorso fondativo M01–M06 | 6 | 6/6 con esercizio/attività e verifica scritta; 0/6 con un laboratorio interattivo direttamente incorporato nella pagina |
| Unità principali considerando 9 corsi + 6 M01–M06 | 15 | **Somma didattica convenzionale**, non 15 corsi commerciali |
| Moduli narrativi interni di AI Teaching Lab | 5 | 2 laboratori guidati per modulo = 10 |
| Studi/ambienti separati di AI Teaching Lab | 6 | Mission Studio; Studio immagini; Studio voce; Studio video; Workspace multimediale; Laboratorio di produzione |
| Approfondimento tecnico di allucinazioni nel coding | 1 | Pagina specialistica, già inclusa nella famiglia Allucinazioni del registro, non nuovo corso indipendente |
| Laboratori/pagine prompt aggiuntivi | 2 | Introduzione al prompt e laboratorio tecnico; fuori dal registro dei 9 |
| Laboratorio generalista AI vs automazione | 1 | Pagina con input e strumenti |
| Attività AI Brain Challenge | 8 | 3 cruciverba + 3 analisi di notizie + 2 dilemmi |
| Sei card Academy originarie + sette ulteriori collegamenti | 13 collegamenti | Sono selezioni editoriali, non 13 nuovi corsi da aggiungere ai 9 o ai 6 |

## A · Catalogo editoriale (9 percorsi)

Legenda laboratori: **I** = input/quiz/scenari interattivi all'interno del corso; **G** = esercizi guidati offline; **E** = studi esterni al singolo modulo; **P** = pratica presente, ma non attestata individualmente per ogni sottounità. La presenza di JavaScript o input è una prova strutturale, non una certificazione d'efficacia.

| Categoria suggerita | Corso | Laboratorio/pratica verificata | Stato |
|---|---|---|---|
| Affidabilità e verifica | Allucinazioni AI e verificabilità | 6 moduli dichiarati, 10 casi, quiz formativo, cruciverba; attività e campi interattivi nella pagina | I · sì |
| Affidabilità e metodo | Modelli mentali e affidabilità dell'AI | Caso simulato Centro Orizzonte, scelte e input di verifica con `reliability-course.js` | I · sì |
| Affidabilità e metodo | Intelligenza aumentata, non sostituita | Esercitazioni di valutazione/giudizio, campi e quiz con `final-two-courses.js` | I · sì |
| Prompt e sviluppo | Prompt vs Skill | Laboratorio senza IA, rubriche e quiz con risposte selezionabili | I/G · sì |
| Prompt e prodotto | AI Product Builder — Centroni City | Sei decisioni progettuali, task, input/textarea e quiz con `centroni-city-course.js` | I · sì |
| Sicurezza | Costruire in sicurezza | Laboratorio del costruttore sicuro, scenari, quiz con `build-safely-course.js` | I · sì |
| Governance agentica | Governare l'autonomia | Incidenti simulati, decisioni, quiz/debugging con `govern-autonomy-course.js` | I · sì |
| Compliance e governance | Compliance dinamica e governance continua | Laboratorio di classificazione, casi, quiz finale con `final-two-courses.js` | I · sì |
| Didattica e produzione | AI Teaching Lab | 5 moduli, 2 laboratori narrativi per modulo; 6 ambienti pratici separati, quiz e strumenti di produzione; EN/ES native incomplete | G/E · sì, non ogni modulo possiede uno studio interattivo individuale |

**Conclusione:** 9/9 offrono pratica in qualche forma; **non** equivale a 9/9 con laboratorio dedicato, interattivo e con la stessa parità linguistica per ogni sottounità.

## B · Fondamenti M01–M06 (6 unità aggiuntive)

| Codice | Modulo | Pratica | Laboratorio specifico sul sito |
|---|---|---|---|
| M01 | Che cos'è davvero l'intelligenza artificiale | Attività AI o automazione, verifica e rubrica | Link al laboratorio generalista; non incorporato nel modulo |
| M02 | Come funziona un modello linguistico | Esempio svolto, attività autonoma, quiz e rubrica | **No**: attività/soluzioni statiche nel modulo |
| M03 | Come costruire un prompt efficace | Esempio svolto, attività autonoma, quiz e rubrica | Link al laboratorio tecnico prompt; non incorporato |
| M04 | Come verificare le risposte AI | Esempio svolto, attività autonoma, quiz e rubrica | **No**: attività/soluzioni statiche nel modulo |
| M05 | Progettare e valutare un workflow AI | Esempio svolto, attività autonoma, quiz e rubrica | **No**: attività/soluzioni statiche nel modulo |
| M06 | AI nella storia, nel lavoro e nella società | Esempio svolto, attività autonoma, quiz e rubrica | **No**: attività/soluzioni statiche nel modulo |

**Esito M01–M06:** 6/6 con attività; 2/6 con link dal corpo lezione a un laboratorio correlato; 0/6 con laboratorio interattivo autonomo nella stessa pagina. I link globali della sidebar non sono considerati un collegamento didattico puntuale.

## C · AI Teaching Lab: moduli e laboratori

| Modulo | Tema | Laboratori guidati | Interazione nella pagina di lettura |
|---|---|---:|---|
| 01 | Insegnare nell'era dell'intelligenza artificiale | 2 | Nessun input/button del modulo; esercizi testuali |
| 02 | Pensiero critico e informazioni affidabili | 2 | Nessun input/button del modulo; esercizi testuali |
| 03 | Progettare materiali che fanno imparare | 2 | Esercizi testuali + link a Mission Studio e produzione multimediale |
| 04 | Una scuola che include e fa progredire | 2 | Nessun input/button del modulo; esercizi testuali |
| 05 | Tutor intelligenti, persone responsabili | 2 | Nessun input/button del modulo; esercizi testuali |

**Sei ambienti effettivi:** `inizia/` (Mission Studio), `studio-immagini/`, `studio-voce/`, `studio-video/`, `workspace-multimediale/`, `laboratorio-multimediale/`. I sei ambienti hanno controlli/form; non costituiscono sei nuovi corsi. `glossario/` (79 voci), `presentazione/` e la pagina introduttiva sono risorse accessorie.

## D · Materiali e attività fuori dal nucleo dei 15

| Area | Risorse presenti | Conteggio | Trattamento nel catalogo futuro |
|---|---|---:|---|
| Coding/verifica | Engineering Assurance nel coding, figlio di Allucinazioni | 1 approfondimento (6 capitoli e 4 scenari dichiarati) | Sottopercorso specialistico |
| Prompt | Che cos'è un prompt e come si scrive? + Laboratorio tecnico di Prompt Engineering | 2 pagine | Lezione introduttiva e laboratorio, non nuovi programmi completi |
| Laboratorio generale | AI oppure automazione? | 1 pagina interattiva | Strumento condiviso |
| Pensiero critico | Cruciverba affidabilità, fonti, governance | 3 attività | Esercitazioni |
| Pensiero critico | AI Radar: notizie AI Act, istruzione, competenze docenti | 3 analisi | Casi di fact checking/lettura guidata |
| Pensiero critico | Dilemmi: selezione personale e apprendimento | 2 attività | Scelte argomentate |
| Media | Slide M01, video Prompt Engineering, podcast episodio 00 | 3 risorse tipizzate | Supporti, non corsi |
| Ricerca | Dossier ACR | 1 dossier | Ricerca, non formazione strutturata |
| SaaS | Product Lab, My Learning, Learning B2B | Servizi/prototipi | **Non** presentare come corsi o laboratori certificati |

## E · Temi trattati / analisi di copertura
1. **Fondamenti e alfabetizzazione IA:** differenza IA/automazione, machine learning e LLM, prompt, inferenza, storia, trasformazioni del lavoro — copertura ampia nell'introduzione.
2. **Prompting e sviluppo controllato:** architettura dei prompt, XML/schema, Prompt vs Skill, progettazione del workflow, test di output e Centroni City — copertura concreta; manca raccordo navigazionale coerente tra M03, laboratorio tecnico e corso specialistico.
3. **Affidabilità, fonti e pensiero critico:** allucinazioni, verifica, bias/limiti, qualità della prova, codifica e QA, modelli mentali, simulazioni/dilemmi — asse distintivo molto sviluppato; rischi di sovrapposizioni tra lezioni.
4. **Sicurezza e governance dell'IA:** Shadow AI, dati, controllo umano, agenti, livelli di autonomia, compliance continua, AI Act — offerta specialistica robusta; aggiornamenti delle fonti essenziali.
5. **IA e didattica:** progettazione pedagogica, verifica materiali, inclusione, feedback, tutor socratici, scelta degli strumenti, produzione immagini/voce/video — percorso avanzato con 10 compiti guidati e 6 ambienti, localizzazione non equivalente in tutte le lingue.
6. **Ricerca/implicazioni sociali:** lavoro e società, ACR, responsabilità, informazione e istruzione — contenuti presenti, ma non tutti strutturati come curriculum con obiettivi e laboratorio.

## F · Problemi e priorità
- **P0 (pedagogia):** definire se ogni *unità* richieda un laboratorio interattivo o se basti un compito autentico guidato; non promettere universalità finché la tassonomia non è approvata.
- **P0 (i18n):** AI Teaching Lab EN/ES non è un corso nativo completo; 8/9 esamina solo sorgenti dei corsi registrati.
- **P1 (discovery):** oggi l'Academy mostra 6 card principali, 7 collegamenti aggiuntivi e un ingresso separato Teaching Lab: questo non è un catalogo centralizzato completo con filtri per risultati attesi, tipo di pratica e livello.
- **P1 (navigazione):** il percorso M01–M06 non comunica chiaramente quali moduli abbiano un laboratorio collegato; attività statiche e pratiche interattive non sono distinte.
- **P1 (consistenza):** standard Academy richiede riuso di un solo sistema card; nuova Home usa un renderer distinto. La v3 aggiunge effetti visivi equivalenti ma non risolve il debito architetturale di componentizzazione.
- **P1 (valutazione):** non esistono dati verificati di efficacia in classi/coorti, né progressi LMS commerciali persistenti. Quiz in pagina = attività formativa, non certificazione.

## G · Proposta di navigazione (NON applicata)
**Macro-categorie consigliate:** (1) Fondamenti e alfabetizzazione, (2) Prompt e costruzione, (3) Affidabilità e pensiero critico, (4) Sicurezza e governance, (5) Didattica e creatività. Ricerca e strumenti in una sezione trasversale.
Ogni scheda di catalogo dovrà descrivere: tipo (corso/modulo/laboratorio/risorsa), obiettivo osservabile, prerequisiti, lingue effettive, tempo solo se documentato, laboratorio (integrato/collegato/guidato/assente), prova di apprendimento, aggiornamento fonti, risultato trasferibile.
**Prossimo gate:** validare questa tassonomia e il criterio di laboratorio, poi progettare il catalogo filtrabile Academy; nessun menu di produzione modificato in questa fase.

## Tracciabilità
- https://github.com/manzo8b/manzo-ai/blob/main/theme/audit-academy-i18n.py
- https://github.com/manzo8b/manzo-ai/blob/main/theme/ACADEMY_CARD_STANDARD.md
- https://github.com/manzo8b/manzo-ai/blob/main/docs/MANZO_AI_GLOBAL_AUDIT_2026-11-20.md
- https://github.com/manzo8b/manzo-ai/blob/main/theme/publish-home-magic-v2.py
