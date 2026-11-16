# MANZO AI — Audit globale del sito pubblico e SEO tecnico

**Data:** 16 novembre 2026  
**Repository:** [manzo8b/manzo-ai](https://github.com/manzo8b/manzo-ai)  
**Sito:** https://manzo8b.github.io/manzo-ai/  
**Scopo:** design, corsi, card, colori, UX, mobile, accessibilità, SEO, sitemap e potenziale comparsa dei sitelink  
**Fonte audit:** pacchetto GitHub Pages **Deploy #43936591266**, SHA \`29d7a63407fa7591106cee36365e4eba13c61bc6\`, artefatto \`github-pages\` id \`14260737342\`, più pipeline di verifica dopo [PR #36](https://github.com/manzo8b/manzo-ai/pull/36).  
**Metodo:** ispezione dei file HTML/CSS/JSON-LD e della sitemap del deploy, confronto con il codice di build, test Chromium GitHub Actions su desktop/mobile. Non è una misurazione autenticata Search Console, né un test WCAG certificato, né un Lighthouse sul dominio live.

## 1. Sintesi e stato misurato

| Metrica | Valore audit prima delle correzioni |
|---|---:|
| Pagine \`index.html\` pubblicate | **109** |
| URL canonici indicizzabili elencati in \`sitemap.xml\` | **94** |
| Pagine \`noindex\` correttamente escluse dalla sitemap | **15** |
| Canonical mancante/errato nelle pagine pubbliche | **0** |
| Titoli \`<title>\` mancanti o ripetuti | **0** |
| H1 mancanti/multipli sulle 109 pagine | **0** |
| Immagini HTML prive di attributo \`alt\` | **0** |
| JSON-LD sintatticamente illeggibile | **0** |
| Pagine pubbliche prive di \`og:title\` | **4** |
| Pagine pubbliche prive di \`twitter:card\` | **13** |
| Metadescrizioni pubbliche molto brevi (meno di 75 caratteri) | **27** |
| Titoli SEO pubblici oltre 80 caratteri | **6** — revisione editoriale possibile; non automaticamente sbagliati |
| Pagine private con meta description/canonical assenti | **6**, intenzionalmente \`noindex\`: non trattate come errore SEO pubblico |

**Chiarimento:** i limiti caratteri sono segnali editoriali di revisione, non soglie imposte da Google. Una meta description di 60 caratteri può essere valida. L'integrazione è stata applicata dove aumentava la chiarezza, senza aggiungere informazioni non dimostrate.

## 2. Correzioni realizzate e test

**PR #36** ha introdotto:

1. \`theme/seo-final-polish.py\` dopo gli overlay editoriali e dopo la pulizia dei titoli, per i soli URL pubblici: migliora anteprime Open Graph e Twitter, sincronizza titolo e descrizione con contenuti effettivamente presenti, migliora 27 descrizioni brevi usando terminologia coerente con le rispettive lezioni, uniforma la \`theme-color\` al bianco e completa le alternate linguistiche delle tre mappe HTML.
2. Esclusione esplicita delle pagine con \`noindex\` dalle nuove anteprime social, con mantenimento dei vincoli Auth/privacy.
3. Validazione automatica: titolo univoco, canonical atteso, sitemap XML corrispondente esattamente alle pagine pubbliche, assenza di \`noindex\` in XML, presenza dei metadati Open Graph e Twitter su ogni URL pubblico e descrizione comprensibile.
4. \`theme/build-seo.py\` aggiornato per dare alle mappe HTML IT/EN/ES il linguaggio delle card MANZO AI: **sfondo bianco**, inchiostro blu, contrasto forte, card con bordi morbidi, ombra discreta, risposta hover/focus e rispetto di \`prefers-reduced-motion\`. Non è stata rimodellata la struttura dei corsi o la navigazione approvata.

**Evidenza CI pre-merge:** [Chromatic QA #43944218536](https://github.com/manzo8b/manzo-ai/actions/runs/43944218536), **PASS**:
- \`94 canonical URLs\`, 3 sitemap HTML, sitemap XML valida
- \`SEO polish: 103 pages, 94 public URLs, 9 noindex preserved\`; **97 file arricchiti** nell'artefatto QA (i 6 URL Auth riservati sono aggiunti successivamente solo nel deploy di produzione)
- \`2995 in-site links\`, \`524 fragment targets\`, nessun ID DOM duplicato, attributo lingua presente
- \`33 screenshot di superfici\` (11 tipologie × 3 larghezze), più test specifici Home e Academy IT/EN/ES
- QA dei tre itinerari guidati: click, tastiera, stampa, mobile, movimento ridotto

**Il PASS di una pipeline non garantisce che Google abbia indicizzato il sito, né certifica WCAG, INP/LCP/CLS o la sicurezza applicativa.**

## 3. Design, card e colori

### Risultati verificati
- I test browser confermano il fondo **bianco puro** sulle 11 superfici campionate, il token inchiostro \`#142841\` e l'uso coerente di card forti: blu, verde petrolio e arancione/corallo nelle prime tre card Home.
- La Home include sei risorse Academy reali, due card editoriali principali e quattro secondarie.
- Academy offre filtri, ricerca, sei contenuti esistenti e tre itinerari guidati, senza iscrizioni o progressi fittizi.
- Hover, focus, riduzione del movimento e larghezze 390, 768 e 1440px sono esercitati da Playwright nelle principali pagine.
- Le tre mappe HTML hanno ora card e tipografia coerenti con la direzione MANZO AI; non sono più elenchi generici su sfondo tenue.

### Ancora da misurare con strumenti dedicati
- WCAG 2.2 AA con audit contrasto **di tutti** gli stati e componenti: l'assenza di errori nei test visivi non basta.
- Navigazione tramite screen reader reale e zoom del 200–400%, oltre alla navigazione tastiera già testata.
- Lighthouse e Web Vitals (LCP, INP, CLS) da dispositivo e connessione reali. La palette e le animazioni sono state controllate, non certificate formalmente.

## 4. Formattazione dei corsi e qualità pedagogica

**Presenze reali:**
- 2 percorsi specialistici illustrati, 4 lezioni secondarie; titolo, livello editoriale, descrizione e CTA validati dai file sorgente.
- 3 sequenze per obiettivo: capire l'AI, verificare le risposte e coding controllato.
- Il percorso Allucinazioni e verificabilità dispone di **6 moduli** e **10 casi**; Engineering Assurance di **6 capitoli** e **4 scenari**; quiz ed esercizi originali.
- Check-list e avanzamenti di studio nelle guide pubbliche sono **solo in memoria**, non collegati a Supabase.
- 15 lezioni legacy hanno ricevuto ID di sottosezione univoci da [PR #34](https://github.com/manzo8b/manzo-ai/pull/34).

**Gap non mascherabili con un restyling:** prerequisiti e rubriche sistematiche per tutte le lezioni, misurazione verificata delle competenze, personal learning sincronizzato, dashboard docente/azienda con autorizzazione tenant, questionari di gradimento e feedback da utenti reali. Non rivendicare certificazioni, quantità studenti, valutazioni o corsi assegnati se non esistono.

## 5. SEO, siti collegati, sitemap e sitelink

### Sitemap e canonical
- \`/manzo-ai/sitemap.xml\`: 94 URL indicizzabili, formato valido; nessuna risorsa \`noindex\` elencata e nessuna data \`lastmod\` inventata.
- Le tre mappe navigabili con card e link reali: \`/it/mappa-del-sito/\`, \`/en/site-map/\`, \`/es/mapa-del-sitio/\`.
- Canonical HTTPS univoci e corretti per tutte le pagine pubbliche; \`hreflang\` coerenti sulle homepage e i principali contenuti, ora anche sulle mappe lingua.
- Il file di verifica Google \`googlee8540704606dd6ec.html\` è conservato dalla pipeline, **ma non prova** che Search Console abbia verificato la proprietà o indicizzato i percorsi.

### Sitelink: limite non tecnico
Google seleziona i sitelink **automaticamente** in base a pertinenza, titoli, link e struttura. Abbiamo valorizzato i link importanti verso Academy, Prompt Mastery, laboratorio, ricerca, pensiero critico e risorse, ma nessuno può imporre il sitelink o la sua posizione.

Google supporta i nomi dei siti a livello di **dominio o sottodominio**, non come sito indipendente di una sottocartella GitHub Pages. Con URL \`manzo8b.github.io/manzo-ai/\` non si può garantire il nome separato **MANZO AI** in SERP. Un dominio dedicato alla piattaforma è la soluzione strutturale, ma richiede decisione e costi del titolare.

### Robots
Il \`robots.txt\` distribuito sotto \`/manzo-ai/robots.txt\` **non è** il controllo robot autorevole dell'host \`manzo8b.github.io\`; il robots si trova in \`https://manzo8b.github.io/robots.txt\`. Inviare la sitemap alla proprietà URL-prefix di MANZO AI in Google Search Console è appropriato. Non creare false dichiarazioni di scansione.

### Dati strutturati
L'HTML pubblicato contiene oggetti JSON-LD di tipi \`WebPage\`, \`LearningResource\`, \`NewsArticle\`, \`DefinedTermSet\`, \`Course\`, \`Article\`, \`TechArticle\` e \`VideoObject\`. Audit sintattico: nessun JSON malformato. Non significa automaticamente idoneità a rich result; serve il test ufficiale Google sul singolo URL e conformità ai requisiti del tipo.

### Search Console
Nessuna proprietà o dato Search Console è stato letto: OpenSEO non ha progetti configurati. Non è possibile indicare impressioni, indicizzazione, ranking o sitelink **effettivamente mostrati** senza i dati dell'account.

## 6. Performance e file

Il pacchetto distribuito occupa circa **36,7 MB** complessivi; questo NON è il peso di ogni pagina né l'ammontare scaricato da un visitatore.

- Video \`assets/media/prompt-engineering/Prompt_Engineering.mp4\`: **20,5 MB**. L'elemento usa \`preload=metadata\`, quindi non carica necessariamente tutto al primo accesso; valutare ottimizzazione codec/bitrate e Lighthouse prima di cambiarlo.
- PDF Oracle City: **2,8 MB**; slide PDF **2,4 MB**; PPTX **1,9 MB**. Sono risorse esplicite da scaricare, non parte del rendering principale.
- HTML delle pagine corso/esercizi ~17–60 KB; card e decorazioni prevalentemente CSS, evitando richieste a immagini stock esterne.

## 7. Priorità successive senza fingere completezza

**Tecnico autonomo:** Lighthouse/Core Web Vitals e audit WCAG via strumenti dedicati; rifinitura di eventuali descrizioni troppo lunghe secondo contenuto reale; ottimizzazione asset dopo verifica dei tempi effettivi; ampliamento verifiche SEO e di contrasto alle nuove pagine.

**Accesso del titolare necessario:** proprietà Search Console URL-prefix e dati di indicizzazione; eventuale dominio dedicato e DNS; rollout Auth/SMTP e policy privacy; autorizzazioni reali e flussi B2B su Supabase. La migrazione SQL 0004 resta separata e non è stata applicata da questo audit.

## 8. Fonti

- [Google — Sitelinks](https://developers.google.com/search/docs/appearance/sitelinks)
- [Google — Site names](https://developers.google.com/search/docs/appearance/site-names)
- [Google — Sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Google — Search essentials](https://developers.google.com/search/docs/essentials)
- [MANZO AI SEO pipeline](../theme/build-seo.py)
- [MANZO AI SEO post-build](../theme/seo-final-polish.py)
- [MANZO AI controllo link](../theme/site-integrity-audit.py)
- [MANZO AI design browser smoke](../theme/design-browser-smoke.py)
