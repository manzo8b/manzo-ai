# MANZO AI — Knowledge & Prompt Lab

Portale educativo trilingue (IT, ES, EN), parte dell'ecosistema MARCELUS AI LAB.

**Sito pubblico:** https://manzo8b.github.io/manzo-ai/

## Release

- **v0.1** — Home conversazionale, M01 approvato, glossario, laboratorio e fonti.
- **v0.2 (preparata, in attesa del pacchetto)** — catalogo M01–M06 con stati editoriali, area Risorse, area Video e slide, un video ufficiale Anthropic collegato senza incorporamento YouTube.

M02–M06 rimangono bozze; in v0.2 vengono mostrati **solo titolo e obiettivo**, con indicazione «In revisione editoriale». L'unica lezione completa pubblicata resta M01.

## Pubblicare la release v0.2

1. Caricare **`site-v0.2.zip`** nella radice del repository tramite [Upload files](https://github.com/manzo8b/manzo-ai/upload/main), senza estrarre il file.
2. Il workflow [Deploy MANZO AI](https://github.com/manzo8b/manzo-ai/actions) si attiva automaticamente.
3. Controllare che il workflow sia riuscito prima di aprire il sito pubblico.
4. Verificare gli indirizzi:
   - IT: `/it/academy/`, `/it/risorse/`, `/it/video-e-slide/`
   - ES: `/es/academia/`, `/es/recursos/`, `/es/videos-y-diapositivas/`
   - EN: `/en/academy/`, `/en/resources/`, `/en/videos-and-slides/`

Il workflow conserva il supporto al file precedente `site-v0.1.zip` finché il nuovo archivio non è presente.

## Principi

- **Nessun chatbot o API AI**: la ricerca è un indice locale delle risorse del sito.
- Nessun login, tracciamento opzionale o database.
- M01 approvato, moduli successivi ancora da revisionare.
- Video YouTube solo come link esterni, senza incorporamento e con attribuzione.
- Slide e nuovi download saranno creati e pubblicati dopo la revisione con il proprietario.

## Codice sorgente

L'archivio delle sorgenti v0.2 è mantenuto separato dal pacchetto di distribuzione, per agevolare aggiornamenti e test. Il workflow attuale pubblica l'archivio statico caricato.

**Non mescolare MANZO AI con il portfolio `marcelus-v-v01`.**