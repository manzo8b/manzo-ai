# MANZO AI — Presentazione M01 · Release v0.4

**Decisione:** sviluppo e integrazione direttamente in MANZO AI con ChatGPT, senza delegare a Codex.

**Pacchetto pronto, ma non ancora pubblicato:** `site-v0.4.zip`.

## Cosa contiene

- Otto slide 16:9 originali in italiano sul modulo M01.
- Visualizzatore con miniatura, navigazione, tastiera, schermo intero (se disponibile).
- Pagina di presentazione con interfaccia localizzata IT, ES, EN. Le **immagini restano in italiano**: la pagina lo segnala.
- Download PDF, PowerPoint e guida docente in italiano.
- Collegamenti da Home, AI Academy, M01, Risorse e Video.
- Nessuna modifica al testo approvato di M01; M02–M06 restano in revisione.

## Nuovi percorsi

- IT `/it/slides/che-cos-e-davvero-l-intelligenza-artificiale/`
- ES `/es/diapositivas/que-es-la-inteligencia-artificial/`
- EN `/en/slides/what-is-artificial-intelligence/`

## Precisioni didattiche

1. La slide 5 raffigura **addestramento** e **inferenza** nello stesso schema solo a fini divulgativi. Sono fasi distinte.
2. I casi della slide 7 non dimostrano tutti automaticamente l'uso di AI: un chatbot e un motore di raccomandazione possono essere implementati con modelli oppure regole. Le scelte grafiche non sono pulsanti interattivi.
3. Le slide visuali sono una **bozza da approvare**, separata dall'approvazione già data al contenuto scritto M01.
4. Il PowerPoint contiene immagini a pagina intera, non elementi editabili singolarmente.

## Verifiche locali effettuate

- 37 pagine HTML principali, sitemap e alternates in tre lingue.
- Nessun link interno mancante nel pacchetto.
- Un unico H1 e JSON-LD sintatticamente valido per pagina.
- PDF e PowerPoint hanno otto pagine/slide.
- Asset delle otto immagini presenti e dimensioni 1672×941.
- Il contenuto dell'articolo M01 è identico alla v0.3.
- Sintassi JS verificata, navigazione interattiva **da verificare dopo la pubblicazione** per blocco amministrativo del browser automatico locale.

## Procedura di aggiornamento

Caricare in radice al repository pubblico GitHub `site-v0.4.zip` **senza estrarlo**. Il workflow già predisposto seleziona il pacchetto più recente. Dopo successo GitHub Actions, verificare a mano navigazione slide, modalità schermo intero e download da smartphone e desktop.

Non toccare il repository `marcelus-v-v01`.
