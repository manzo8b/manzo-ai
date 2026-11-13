# MANZO AI — SEO, sitemap e Google Search Console
Data audit tecnico: 13 novembre 2026
Sito ufficiale: https://manzo8b.github.io/manzo-ai/
Repository: https://github.com/manzo8b/manzo-ai

## Modifiche applicate
La pubblicazione GitHub Pages estrae la versione v0.7, applica il tema e le estensioni editoriali (podcast, Oracle City), poi esegue **theme/build-seo.py** per produrre la sitemap definitiva e il collegamento delle sezioni.

- Sitemap XML finale: https://manzo8b.github.io/manzo-ai/sitemap.xml
- Indice navigabile IT: https://manzo8b.github.io/manzo-ai/it/mappa-del-sito/
- Indice navigabile ES: https://manzo8b.github.io/manzo-ai/es/mapa-del-sitio/
- Indice navigabile EN: https://manzo8b.github.io/manzo-ai/en/site-map/
- Le homepage IT/ES/EN espongono link HTML alle sezioni realmente presenti, in aggiunta alla navigazione esistente.
- Ogni pagina pubblicata include URL canonico assoluto HTTPS; le homepage e la landing includono alternates per le tre lingue e x-default.
- La sitemap è rigenerata dall'inventario reale delle pagine HTML della build finale; non contiene priorità arbitrarie né date di modifica inventate.
- Test pipeline: https://github.com/manzo8b/manzo-ai/actions/runs/43446911297 — completato con successo. Log: 84 URL canonici, 3 mappe HTML navigabili, XML validato.

## Cosa non è stato ancora dimostrato
Un workflow GitHub Pages riuscito NON dimostra che Google abbia indicizzato le pagine.
Non è stata eseguita una lettura autenticata della proprietà Search Console in questa revisione.
La selezione dei sitelink è automatica e non è controllabile manualmente.
Il conteggio dei risultati della ricerca pubblica non è un indicatore affidabile della copertura reale.

## I sitelink più desiderabili
Favorire la chiarezza dei titoli e dei collegamenti a:
- AI Academy
- Prompt Mastery
- Laboratorio tecnico
- AI Brain Challenge / Pensiero critico
- Risorse e Biblioteca
- Video e Podcast

Google potrà scegliere link differenti o non mostrarne alcuno.

## Azione del proprietario in Google Search Console
1. Accedere a https://search.google.com/search-console/.
2. Aggiungere proprietà **Prefisso URL**, esattamente: `https://manzo8b.github.io/manzo-ai/`.
3. Verificare la proprietà con il metodo realmente offerto da Google. Se sono necessari un file HTML o meta tag di verifica, aggiungerli con il valore effettivo fornito da Google (mai inventarne uno).
4. Aprire **Sitemap**, inviare `https://manzo8b.github.io/manzo-ai/sitemap.xml`.
5. In **Controllo URL** ispezionare separatamente:
   - `https://manzo8b.github.io/manzo-ai/it/`
   - `https://manzo8b.github.io/manzo-ai/en/`
   - `https://manzo8b.github.io/manzo-ai/es/`
   - `https://manzo8b.github.io/manzo-ai/it/academy/`
   - `https://manzo8b.github.io/manzo-ai/it/prompt-mastery/`
   - `https://manzo8b.github.io/manzo-ai/it/pensiero-critico/`
6. Per ogni pagina, controllare: scansione consentita, indicizzazione consentita, ultima scansione, canonical dichiarato e canonical scelto da Google.
7. Se la pagina è valida ma assente, dopo verifica dei problemi usare *Richiedi indicizzazione*. L'esito non è garantito.
8. Monitorare per almeno quattro settimane impressioni, clic, CTR, query, pagine e paese; non inventare valori di traffico.

## robots.txt su GitHub Pages project URL
Per una proprietà sotto `/manzo-ai/`, il robots autorevole si trova alla radice host `https://manzo8b.github.io/robots.txt`, non in `/manzo-ai/robots.txt`. Non creare un file inefficace nella directory del progetto come soluzione fittizia. L'assenza del file robots host-root non implica di per sé blocco di scansione. Il controllo del robots radice resta separato perché non è stato identificato in questo intervento un repository host-root modificabile.

## Site name e dominio
Google supporta il nome del sito al livello dominio/sottodominio, non come sito indipendente per la sottocartella GitHub Pages. Quindi le etichette di progetto non garantiscono che venga mostrato MANZO AI come site name. Un dominio personalizzato dedicato potrebbe aiutare in futuro, quando sia giustificato dal budget e dalla strategia.

## Prossima fase editoriale e misurazione
- Controllare unicità e pertinenza dei tag title e description per tutte le pagine.
- Estendere i collegamenti contestuali fra moduli, laboratorio, Prometeus Marcelus e Biblioteca.
- Valutare dati strutturati pertinenti e verificabili (senza promettere risultati avanzati).
- Fare un audit Lighthouse e accessibilità reale dopo i cambiamenti.
- Pubblicare un post LinkedIn con screenshot autentico e collegamento alla home IT; monitorare click con parametri UTM non indicizzati come URL canonici.

## Documentazione ufficiale
- https://developers.google.com/search/docs/appearance/sitelinks
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- https://support.google.com/webmasters/answer/9012289
