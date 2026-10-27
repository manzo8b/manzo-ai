# MANZO AI — Knowledge & Prompt Lab

Portale educativo trilingue (IT, ES, EN), parte dell'ecosistema MARCELUS AI LAB.

**Sito pubblico:** https://manzo8b.github.io/manzo-ai/

## Release

- **v0.4 (preparata, in attesa del pacchetto)** — otto slide 16:9 M01, visualizzatore localizzato, PDF/PowerPoint italiano e guida docente. Collegamenti da Home, Academy, M01, Risorse e Video. [Dettagli della release](docs/SLIDE_M01_V04_RELEASE.md).

- **v0.1** — Home conversazionale, M01 approvato, glossario, laboratorio e fonti.
- **v0.2 (pubblicata)** — catalogo M01–M06 con stati editoriali, area Risorse, area Video e slide, un video ufficiale Anthropic collegato senza incorporamento YouTube.
- **v0.3 (preparata, in attesa del pacchetto)** — percorso introduttivo «Che cos'è un prompt e come si scrive?» (IT/ES/EN), collegamento alla Biblioteca Prometeus dalla sezione Risorse e quattro video tutorial esterni selezionati. M01 rimane invariato; M03 resta in revisione.

M02–M06 rimangono bozze; in v0.2 vengono mostrati **solo titolo e obiettivo**, con indicazione «In revisione editoriale». L'unica lezione completa pubblicata resta M01.

## Pubblicare la release v0.4

Caricare **`site-v0.4.zip`** tramite [Upload files](https://github.com/manzo8b/manzo-ai/upload/main) senza estrarlo. Il workflow controlla le tre pagine, le otto immagini e i download PDF/PPTX, quindi pubblica la release più recente. Dopo il deploy verificare navigazione, schermo intero e download nel browser. Non considerare le slide definitivamente approvate prima della revisione visuale.

## Procedura storica v0.3

Carica **`site-v0.3.zip`** nella radice del repository tramite [Upload files](https://github.com/manzo8b/manzo-ai/upload/main), senza estrarlo. Il workflow pubblica automaticamente la versione più recente disponibile. Attendere un run riuscito prima di verificare `/it/prompt-mastery/che-cos-e-un-prompt/`, `/it/risorse/` e `/it/video-e-slide/` e le corrispondenti versioni ES/EN.

Dettagli editoriali e verifiche: [Registro video e percorso v0.3](docs/VIDEO_E_PROMPT_V03_REGISTRO.md).

## Procedura storica v0.2

1. Caricare **`site-v0.2.zip`** nella radice del repository tramite [Upload files](https://github.com/manzo8b/manzo-ai/upload/main), senza estrarre il file.
2. Il workflow [Deploy MANZO AI](https://github.com/manzo8b/manzo-ai/actions) si attiva automaticamente.
3. Controllare che il workflow sia riuscito prima di aprire il sito pubblico.
4. Verificare gli indirizzi:
   - IT: `/it/academy/`, `/it/risorse/`, `/it/video-e-slide/`
   - ES: `/es/academia/`, `/es/recursos/`, `/es/videos-y-diapositivas/`
   - EN: `/en/academy/`, `/en/resources/`, `/en/videos-and-slides/`

Il workflow conserva il supporto al file precedente `site-v0.1.zip` finché il nuovo archivio non è presente.

## Collegamento didattico a Prometeus Marcelus

La **Biblioteca Prometeus Marcelus** è la risorsa archivistica collegata per spiegare cosa sia un prompt, come strutturarlo e come valutarlo con esercizi commentati. L'integrazione nella pagina Risorse, in M03 e nel Laboratorio è documentata in [INTEGRAZIONE_BIBLIOTECA_PROMETEUS.md](docs/INTEGRAZIONE_BIBLIOTECA_PROMETEUS.md).

- Biblioteca pubblica IT: https://manzo8b.github.io/marcelus-v-v01/it/library/
- Non importare automaticamente l'intero catalogo e non presentare le voci come prompt tutti testati.
- Lo stato della release v0.2 pubblicata **non cambia** con questa nota documentale.

## Principi

- **Nessun chatbot o API AI**: la ricerca è un indice locale delle risorse del sito.
- Nessun login, tracciamento opzionale o database.
- M01 approvato, moduli successivi ancora da revisionare.
- Video YouTube solo come link esterni, senza incorporamento e con attribuzione.
- Slide e nuovi download saranno creati e pubblicati dopo la revisione con il proprietario.

## Codice sorgente

L'archivio delle sorgenti v0.2 è mantenuto separato dal pacchetto di distribuzione, per agevolare aggiornamenti e test. Il workflow attuale pubblica l'archivio statico caricato.

**Non mescolare MANZO AI con il portfolio `marcelus-v-v01`.**