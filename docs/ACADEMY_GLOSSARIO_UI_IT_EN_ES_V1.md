# MANZO AI Academy — Glossario ufficiale UI IT/EN/ES
**Versione:** v1, proposta operativa del 20/11/2026 · **Ambito:** catalogo, schede, breadcrumb, CTA, stati del laboratorio e lingue
**Stato:** definizione editoriale in branch di progettazione; non equivale a rilascio pubblicato

## 1. Regola base dei formati

| ID interno (mai badge visibile) | Italiano | English | Español | Uso |
| --- | --- | --- | --- | --- |
| `course` | Corso | Course | Curso | Percorso editoriale autonomo con obiettivi, contenuti e pratica; i nove censiti |
| `foundation_module` | Modulo fondativo | Foundation module | Módulo fundamental | M01–M06: unità brevi della base, NON sei corsi aggiuntivi da vendere |
| `lab` | Laboratorio | Lab | Laboratorio | Spazio di sperimentazione, autonomo o collegato |
| `resource` | Risorsa | Resource | Recurso | Glossario, dossier, slide, lettura, podcast, cruciverba, notizia |
| `learning_path` | Percorso consigliato | Guided path | Itinerario recomendado | Sequenza di elementi ESISTENTI, non corso aggiuntivo né iscrizione |

**Navigazione:** prima mostrare l'obiettivo; il badge format evita ambiguità. Un corso può contenere lezioni, esercizi o laboratori senza che ogni elemento sia un nuovo corso.

## 2. Pratica: badge testuali (non lettere isolate)

| ID | IT | EN | ES | Regola di verità |
| --- | --- | --- | --- | --- |
| `interactive` | Laboratorio interattivo | Interactive lab | Laboratorio interactivo | Input, scelta o manipolazione effettiva verificata sulla pagina |
| `guided` | Esercizio guidato | Guided exercise | Ejercicio guiado | Consegna o rubrica esplicita, eseguibile anche fuori piattaforma |
| `separate_studio` | Studio collegato | Linked studio | Estudio vinculado | Ambiente interno separato e collegato con URL controllato |
| `assessment` | Quiz e verifica | Quiz and review | Cuestionario y revisión | Prova con feedback, o indicare "Quiz da correggere autonomamente" |
| `static_activity` | Attività nella lezione | In-lesson activity | Actividad en la lección | Attività scritta senza strumento interattivo specifico |
| `none` | Nessun laboratorio dedicato | No dedicated lab | Sin laboratorio específico | Informazione esplicita; non equivale a "nessuna pratica" |
| `external_tool` | Strumento esterno | External tool | Herramienta externa | Solo per servizio effettivamente esterno al sito, non per studio interno |

Non mostrare `I/G/E/P` agli studenti. Gli ID restano nel modello dati e nell'audit.

## 3. Lingue e stati di disponibilità

| Contesto | IT | EN | ES |
| --- | --- | --- | --- |
| Titolo metadato | Lingue disponibili | Available languages | Idiomas disponibles |
| Locale completo | Italiano disponibile | Available in English | Disponible en español |
| Solo versione italiana | Disponibile in italiano | Available in Italian | Disponible en italiano |
| Locale non completato | Traduzione in preparazione | Translation in progress | Traducción en preparación |
| Stato confermato | Disponibile | Available | Disponible |
| Stato editoriale ambiguo | Da verificare | To be verified | Por verificar |
| Laboratorio non pubblicato | Laboratorio in preparazione | Lab in development | Laboratorio en preparación |

**AI Teaching Lab:** indicare “Disponibile in italiano · Inglese e spagnolo in preparazione”. Non esporre le traduzioni narrative come corso nativo EN/ES finché gli strumenti e le pagine non sono davvero pubblicati.

## 4. Navigazione, CTA e microcopy

| ID | IT | EN | ES |
| --- | --- | --- | --- |
| `catalog` | Catalogo Academy | Academy catalog | Catálogo de la Academia |
| `guided` | Percorsi consigliati | Guided paths | Itinerarios recomendados |
| `foundations` | Base essenziale | Essential foundations | Fundamentos esenciales |
| `labs_and_tools` | Laboratori e strumenti | Labs and tools | Laboratorios y herramientas |
| `resources` | Risorse e approfondimenti | Resources and further reading | Recursos y lecturas adicionales |
| `objective` | Cosa imparerai a fare | What you'll be able to do | Qué aprenderás a hacer |
| `audience` | A chi è rivolto | Who it's for | A quién va dirigido |
| `practice` | Come si fa pratica | How you'll practice | Cómo practicarás |
| `requirements` | Prima di iniziare | Before you start | Antes de empezar |
| `curriculum` | Programma | Syllabus | Programa |
| `begin` | Inizia il corso | Start course | Empezar el curso |
| `begin_module` | Apri il modulo | Open module | Abrir el módulo |
| `open_lab` | Apri il laboratorio | Open lab | Abrir laboratorio |
| `continue` | Passo successivo | Next step | Siguiente paso |
| `back_catalog` | Torna al catalogo | Back to catalog | Volver al catálogo |
| `filters` | Filtri | Filters | Filtros |
| `theme` | Tema | Topic | Tema |
| `format` | Tipo di contenuto | Content type | Tipo de contenido |
| `language` | Lingua | Language | Idioma |
| `practice_filter` | Tipo di pratica | Practice type | Tipo de práctica |
| `no_results` | Nessun risultato con questi filtri | No results for these filters | No hay resultados con estos filtros |
| `reset_filters` | Azzera filtri | Clear filters | Borrar filtros |

## 5. Convenzioni editoriali

- **MANZO AI** e **AI Teaching Lab** sono nomi propri invarianti. IT/ES usano **IA** nella prosa ordinaria; EN usa **AI**. Titoli di corsi registrati non si rinominano automaticamente.
- “M01–M06” sono codici secondari sotto il titolo; “i18n”, “P0/P1”, “LMS”, “SaaS”, codici di build e classificazioni tecniche non devono comparire come etichette rivolte allo studente.
- “Area personale” / “Per aziende” indicano funzioni o servizi distinti, non corsi. Nessun messaggio di attestato, avanzamento sincronizzato, docente certificato o pagamento se non realmente implementato.
- **Durate e livelli** vanno mostrati solo quando esplicitamente documentati e verificati sul singolo percorso; mai riempiti con stime.
- Non inserire il punto finale nelle intestazioni H1–H6 e nei titoli delle card. Usare focus visibile, reduced-motion, target accessibili e CTA che descrivano la destinazione.
- Uno stesso documento può appartenere a **un percorso principale e a più temi secondari**, ma possiede un ID canonico e si conta una sola volta.

## 6. Governance del vocabolario

Prima di pubblicare: controllare parità EN/ES nei contenuti collegati, disponibilità reale delle pratiche, URL pubblicato e descrizione del risultato atteso. Fonte di verità futura: `academy/catalog-v1.json`, non contatori duplicati nelle Home.
