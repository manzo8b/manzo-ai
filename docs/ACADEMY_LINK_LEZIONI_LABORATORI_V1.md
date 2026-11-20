# MANZO AI Academy — Mappa lezioni → pratica → verifica → passo successivo
**Versione:** v1, 20 novembre 2026 · **Stato:** audit e specifica del collegamento, nessuna URL live modificata
**Base:** `/manzo-ai/` · Tutte le rotte vanno validate su `_site` prima dell'inserimento in UI.

## A. Fondamenti M01–M06

| Modulo | Destinazione italiana verificata nel deploy | Pratica nella lezione | Collegamento didattico esistente | Passo successivo consigliato |
|---|---|---|---|---|
| M01 · Che cos'è davvero l'IA | `it/impara/che-cos-e-l-intelligenza-artificiale/` | Quiz / attività di classificazione | Laboratorio generale AI oppure automazione; URL puntuale da estrarre dalla pagina finale | M02 |
| M02 · Come funziona un modello linguistico | `it/impara/come-funziona-un-modello-linguistico/` | Esercizio guidato e quiz statico | Nessun lab interattivo dedicato | M03 |
| M03 · Come costruire un prompt efficace | `it/impara/come-costruire-un-prompt-efficace/` | Esercizio guidato e quiz statico | Laboratorio tecnico prompt; URL puntuale da estrarre dalla pagina finale | M04 |
| M04 · Come verificare le risposte IA | `it/impara/come-verificare-le-risposte-ai/` | Esercizio guidato e quiz statico | Nessun lab interattivo dedicato | M05 |
| M05 · Progettare e valutare un workflow IA | `it/impara/progettare-un-workflow-ai/` | Esercizio guidato e quiz statico | Nessun lab interattivo dedicato | M06 |
| M06 · IA nella storia, nel lavoro e nella società | `it/impara/ai-storia-lavoro-societa/` | Esercizio guidato e quiz statico | Nessun lab interattivo dedicato | Catalogo Academy |

**Regola d'implementazione:** il “passo successivo” della sequenza di base si può collegare alle rotte sopra. Un “Apri laboratorio” compare solo se la destinazione è davvero presente nel rendering verificato: nessun link a un laboratorio previsto ma non esistente.

### Collegamenti localizzati (fonte: workflow di deploy)
| Unità | Italiano | English | Español |
|---|---|---|---|
| M01 | `it/impara/che-cos-e-l-intelligenza-artificiale` | Percorso non verificato in questa mappa | Percorso non verificato in questa mappa |
| M02 | `it/impara/come-funziona-un-modello-linguistico` | `en/learn/how-a-language-model-works` | `es/aprende/como-funciona-un-modelo-de-lenguaje` |
| M03 | `it/impara/come-costruire-un-prompt-efficace` | `en/learn/how-to-build-an-effective-prompt` | `es/aprende/como-construir-un-prompt-eficaz` |
| M04 | `it/impara/come-verificare-le-risposte-ai` | `en/learn/how-to-verify-ai-answers` | `es/aprende/como-verificar-las-respuestas-de-ia` |
| M05 | `it/impara/progettare-un-workflow-ai` | `en/learn/designing-an-ai-workflow` | `es/aprende/disenar-un-flujo-de-trabajo-con-ia` |
| M06 | `it/impara/ai-storia-lavoro-societa` | `en/learn/ai-history-work-and-society` | `es/aprende/ia-historia-trabajo-sociedad` |

Per M01 non inferire slug EN/ES sulla base della traduzione del titolo. La mancanza nella mappa significa **rotta non ancora verificata**, non dimostra assenza del contenuto.

## B. Nove corsi: localizzazione della pratica

Gli anchor seguenti derivano dai publisher e sono **candidati verificabili al momento della build**, non certificazione live di ogni punto.

| Corso | Pratica effettiva | Anchor o studio documentato | CTA contestuale consigliata |
|---|---|---|---|
| Allucinazioni IA e verificabilità | Laboratorio interattivo | `#hx-lab` (publisher Learning Experience) | Vai al laboratorio |
| Modelli mentali e affidabilità | Stress-test guidato/interattivo | `#mr-laboratorio` | Vai al laboratorio |
| Intelligenza aumentata, non sostituita | Laboratorio di giudizio | `#ft-lab` | Vai al laboratorio |
| Prompt vs Skill | Laboratorio senza IA | `#laboratorio` | Vai al laboratorio |
| Centroni City | Blueprint operativo | `#cc-blueprint` | Crea il tuo blueprint |
| Costruire in sicurezza | Laboratorio decisionale | `#safe-laboratory` | Vai al laboratorio |
| Governare l'autonomia | Simulatore Mission Control | `#ga-mission-control` | Apri Mission Control |
| Compliance dinamica e governance continua | Laboratorio interattivo | `#ft-lab` | Vai al laboratorio |
| AI Teaching Lab | Due laboratori guidati per modulo + sei ambienti separati | Vedi elenco C | Apri l'attività collegata, con lingua esplicita |

**Validazione:** la build verifica che l'anchor sia realmente presente nella pagina localizzata PRIMA di esporre la CTA e verifica che non si creino due `id` uguali.

## C. AI Teaching Lab (pubblicazione italiana)

**Corso principale:** `it/formazione/ia-per-la-didattica/`  
**Cinque moduli narrativi:** `it/formazione/ia-per-la-didattica/modulo-01/` ... `modulo-05/`. Ogni modulo ha due laboratori narrativi; il loro testo non si trasforma automaticamente in app interattiva.

**Ambienti di lavoro documentati e raggiungibili dal corso:**

1. Mission Studio — `it/formazione/ia-per-la-didattica/inizia/`
2. Studio immagini — `it/formazione/ia-per-la-didattica/studio-immagini/`
3. Studio voce — `it/formazione/ia-per-la-didattica/studio-voce/`
4. Studio video — `it/formazione/ia-per-la-didattica/studio-video/`
5. Workspace multimediale — `it/formazione/ia-per-la-didattica/workspace-multimediale/`
6. Laboratorio di produzione — `it/formazione/ia-per-la-didattica/laboratorio-multimediale/`

**Divieto:** non presentare questi URL italiani come studi tradotti in inglese o spagnolo. In EN/ES mostrare «Disponibile in italiano», e non una CTA che sembri restare nella stessa lingua.

## D. Regola per la CTA a fondo lezione

| Situazione effettiva | CTA primaria | CTA secondaria |
|---|---|---|
| Lezione con laboratorio validato | Apri il laboratorio | Passo successivo |
| Lezione con attività guidata in pagina | Vai all'attività | Apri il prossimo modulo |
| Lezione con quiz finale | Verifica ciò che hai imparato | Torna al programma |
| Fine percorso | Torna al Catalogo Academy | Scopri un percorso consigliato |
| Lab di altro locale disponibile | Apri il laboratorio in italiano | Torna al corso |

Se non esiste l'anchor della pratica, non costruire `href="#laboratorio"` fittizio: usare un vero ID verificato o un link a pagina reale.

## E. Prova minima per uno sprint di collegamento

1. `academy/catalog-v1.json` definisce un solo ID per contenuto e non inventa rotta/lang
2. Un report di build risolve URL e fragment in tutte le lingue effettive
3. I collegamenti M01/M03 vengono estratti dalle pagine generate e confrontati con la destinazione (niente route hardcode non verificato)
4. M02/M04/M05/M06 conservano l'attività guidata senza badge «Lab interattivo»
5. Breadcrumb e CTA successiva vengono verificati da tastiera, su mobile e con menu lingue
6. Nessun cambiamento a My Learning, Auth, Supabase, attestati o dati di utenti

**Stato del rilascio:** non è stato alterato alcun collegamento di produzione da questo documento. Implementazione reversibile in branch dopo QA.
