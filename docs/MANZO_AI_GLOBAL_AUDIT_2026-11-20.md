# MANZO AI — Audit generale della piattaforma
**Data:** 20 novembre 2026  
**Repository:** [manzo8b/manzo-ai](https://github.com/manzo8b/manzo-ai) · ramo `main`  
**Pubblicazione:** https://manzo8b.github.io/manzo-ai/it/  
**Ambito:** esperienza utente, design, architettura web, contenuti e didattica, localizzazione, SEO, accessibilità, prestazioni, sicurezza, governance, readiness commerciale.  
**Tipo:** audit diagnostico basato su evidenze. **Non sono state modificate pagine, componenti, database, autenticazione, infrastruttura o pubblicazione.** È stato creato soltanto il presente documento.

## A · Limiti e metodo

1. Consultazione del repository GitHub corrente, dei file `theme/`, del ramo `main`, del processo di rilascio, del registro formativo e dei rapporti del progetto.
2. Lettura dei **log della pipeline conclusa con successo**: [Deploy MANZO AI #44725699053](https://github.com/manzo8b/manzo-ai/actions/runs/44725699053), eseguita il 20/11/2026 sul commit `1a69819640…`.
3. Esame del **contenuto testuale della Home IT effettivamente aperta nel browser**, disponibile come scheda della sessione utente. Questo non equivale a un audit pixel-perfect né a un test delle interazioni su iPhone.
4. Controllo su fonti pubbliche di **due affermazioni campione**: esistenza e oggetto del [Regolamento (UE) 2026/1744](https://eur-lex.europa.eu/legal-content/it/TXT/?uri=oj:L_202601744) e dati dell'[AI Index 2026, Responsible AI](https://hai.stanford.edu/ai-index/2026-ai-index-report/responsible-ai) sui 362 incidenti documentati nel 2025 e 233 nel 2024.
5. Consultazione di rapporti già presenti nel repository. **Le verifiche registrate il 16 novembre sono storiche, non misure nuove al 20 novembre**.

**Non effettuati:** Lighthouse, Web Vitals LCP/INP/CLS sul sito live, scanner WCAG 2.2 AA con screen reader reale, verifica Safari/iOS corrente, crawl live totale delle 141 pagine, prova Google Search Console autenticata, audit indipendente di sicurezza o test live cross-tenant. Il contenuto del sito pubblico non è stato scaricato e rieseguito integralmente in un browser di test da questa sessione. L'assenza di misure non equivale al rilevamento di un difetto.

## B · Stato misurato dalla pipeline

| Parametro | Evidenza tecnica |
| --- | --- |
| Deploy GitHub Pages | **SUCCESS** — run #44725699053 |
| Pagine HTML generate | **141** |
| URL pubblici canonici nella sitemap | **132** |
| Pagine `noindex` preservate | **9** |
| Collegamenti interni controllati | **3.788** |
| Riferimenti ad ancore in pagina controllati | **948** |
| Corsi censiti con sorgenti IT/EN/ES | **8 su 9** |
| Copertura completa di tutte le pagine IT/EN/ES | **NON CERTIFICATA** |
| AI Teaching Lab | **5 lezioni pubblicate in italiano**; EN/ES ancora incomplete |
| Verifiche browser automatizzate | Chromium / Playwright e contratti nei workflow; non certificazione Safari/WCAG |
| Backend commerciale end-to-end | **NON ATTIVO**; My Learning API disabilitata |

**Passaggi automatici positivi:** generazione sitemap, canonical, titoli univoci, metadati Open Graph/Twitter, integrità dei link interni, ID DOM univoci, `lang` delle pagine, QA di una serie di laboratori e flussi di front-end. Il PASS non significa che le 132 pagine siano effettivamente indicizzate su Google.

La Home italiana presenta **6 card curate originarie più 7 corsi aggiunti**, ossia 13 card sotto la medesima selezione Academy, a fronte dell'etichetta testuale visibile «6 risorse pubblicate». La differenza è osservabile nel contenuto della Home. I corsi possono inoltre apparire in altre sezioni: questo non equivale a 13 corsi editoriali distinti dal resto del catalogo.

## C · Esiti per area

| Area | Stato del risultato | Giudizio |
| --- | --- | --- |
| Base statica e deploy GitHub Pages | Test superati e sito consultabile | **Solida per portale pubblico**, non per SaaS |
| SEO tecnico on-site | 132 URL, controllo canonical, meta e link | **Buono a livello di build**, risultati Search non misurati |
| Internationalisation | 8/9 sorgenti editoriali completi; parte del sito non verificata | **Incompleta** |
| Esperienza Home e Academy | Card coerenti a livello di classi e verifiche; contatore errato, densità crescente | **Da riorganizzare senza ripartire dal design** |
| Didattica | Letture, laboratori, rubriche e test sostanziali; casi documentati | **Buona base**, non prova di efficacia formativa su utenti |
| Accessibilità | Focus e responsive smoke test; no audit completo assistivo | **Copertura parziale da certificare** |
| Prestazioni | Asset rilevanti individuati; no misure Lighthouse live | **Non misurate** |
| Sicurezza dei prototipi | Moduli client-side locali, blocchi e feature flag presenti | **Approccio conservativo**, non prova di sicurezza SaaS |
| Backend Learning B2B | Supabase pilota documentato; API di apprendimento non distribuita | **Non pronto all'esercizio commerciale** |
| Commercial readiness | Posizionamento e struttura preliminari, mancano utenti/contratti/incassi attestati | **Pre-commerciale** |

## D · Problemi verificati e decisioni consigliate

### F01 — P0 · Dichiarazione di disponibilità trilingue non equivalente al catalogo

**Evidenza:** `theme/audit-academy-i18n.py`, log del run #44725699053, `editorial/learning/ai-teaching-lab/`. L'audit riferisce **8/9** corsi con sorgenti completi. Per AI Teaching Lab l'italiano ha cinque moduli e fonti JSON, mentre per `en/` e `es/` risultano soltanto **module-01.md–module-04.md**: `module-05.md`, `course.json`, `narrative.json`, `assessment-bank.json`, `glossary.json` non sono ancora presenti. Il glossario italiano include **79 voci**. Il publisher `theme/publish-ai-teaching-lab.py` continua a leggere i file da `DATA=SRC/"it"`.

**Impatto:** un visitatore potrebbe interpretare il messaggio generico IT/EN/ES come promessa di equivalenza funzionale. Le pagine Academy EN ed ES segnalano correttamente che AI Teaching Lab è per ora in italiano; mantenere questa trasparenza.

**Azione:** completare sorgenti e risorse mancanti in blocchi incrementali; aggiungere publisher nativi EN/ES soltanto dopo parità di struttura, quiz, feedback e glossario; validare il cambio lingua sullo stesso punto del corso. **Non ricominciare gli otto corsi già tradotti.**

**Gate:** 9/9 nel registro dei sorgenti + test di corrispondenza delle pagine effettivamente pubblicate + controlli di tutte le altre pagine del portale. Non certificare il sito trilingue limitandosi al 9/9.

### F02 — P0 editoriale · Contatore Academy visibile non aggiornato

**Evidenza:** `theme/publish-home-showcase.py` contiene le costanti «6 risorse pubblicate» / «6 published resources» / «6 recursos publicados». Nella Home IT aperta sono visibili 13 card nella selezione, comprese le aggiunte successive (Prompt vs Skill, Affidabilità, Centroni City, Costruire in sicurezza, Governare l'autonomia, Compliance dinamica, Intelligenza aumentata).

**Impatto:** messaggio quantitativo ambiguo; il catalogo reale appare in contrasto con la presentazione editoriale.

**Azione:** separare il numero di **sei risorse originarie in evidenza** dal **numero di schede effettivamente esposte** o, preferibilmente, rimuovere il numero fisso e utilizzare una descrizione del catalogo. Evitare conteggi hard-coded in più publisher.

**Gate:** un test del render verifica testo, definizione di “risorsa” e numero coerente su IT/EN/ES.

### F03 — P1 UX · Lunghezza e gerarchia della Home

**Evidenza:** la Home aperta presenta hero, quattro porte d'ingresso, una seconda sezione di quattro card, tredici card Academy, ulteriori percorsi consigliati, risorse, media, ricerca, corso professionale, Product Lab e mappa del sito. Il codice mantiene molte sezioni storiche oltre ai nuovi publisher.

**Impatto:** la crescita editoriale aumenta carico di scelta, scroll e ripetizione di destinazioni. È una criticità di architettura informativa desumibile dalla quantità e dall'ordine delle sezioni; **non sono disponibili dati utente** per quantificare abbandono o difficoltà.

**Azione:** Home breve e inclusiva per obiettivi; massimo una selezione di ingressi curati e un CTA Academy; catalogo completo in Academy con filtri per livello, ambito e risultato; progressiva divulgazione di sezioni di ricerca e anteprime. Non rimuovere corsi né progettare una Home rivolta soltanto a docenti.

**Gate:** primo compito utente comprensibile in 5–10 secondi in test guidati, senza utilizzare questa soglia come risultato già misurato; meno duplicazioni; test tastiera e telefono.

### F04 — P1 design · Coerenza della geometria, ma varianti testuali e CSS crescenti

**Evidenza:** `theme/ACADEMY_CARD_STANDARD.md` stabilisce uno standard; le nuove card condividono classi principali, due badge e CTA. I publisher mostrano tuttavia etichette diverse («Corso», «Corso completo», «CORSO AVANZATO», «CORSO PROFESSIONALE»), testi CTA differenti, più CSS di override e copertine particolari.

**Impatto:** disallineamenti di altezza o densità possono emergere in stringhe EN/ES lunghe e negli ultimi breakpoint, pur superando l'integrità HTML.

**Azione:** estrarre realmente un solo renderer/card component alimentato da dati di corso, mantenendo le copertine diverse. Fissare tassonomia dei tipi, limiti editoriali di descrizione e test visuale delle tredici card su desktop e mobile; mantenere il divieto di punti finali nei titoli.

**Gate:** snapshot delle tre lingue e verifica di altezza, padding, CTA su una riga, focus e reduced motion.

### F05 — P1 architettura · Archivio ZIP come sorgente storica di 82 pagine + overlay

**Evidenza:** `.github/workflows/deploy-pages.yml` seleziona `site-v0.7.zip` e lo estrae in `_site`; il commento lo definisce autorevole per 82 pagine. Seguono decine di `theme/publish-*.py`, riscritture della Home, dei corsi e dell'SEO. Nel repository sono conservate sette versioni ZIP e vari file Python duplicati/nominati in due stili.

**Impatto:** la build passa, ma aumenta il rischio di disallineamenti, regressioni e difficoltà di comprendere dove modificare realmente una pagina. Il problema è di manutenibilità e costo della modifica, non la prova che il sito stia fallendo.

**Azione:** rendere ogni pagina **riproducibile da sorgenti dichiarativi** e da componenti condivisi; procedere con migrazione a piccoli gruppi di rotte senza sostituire l'intero sito. Versionare un manifest e predisporre confronto HTML/hash tra prima e dopo. Eliminare ZIP storici solo dopo aver verificato riproducibilità, backup e impatto dei riferimenti.

**Gate:** stesso output e stessi URL con una build da sorgenti, niente regressioni in sitemap, card, CSS e pagine, rollout reversibile.

### F06 — P1 misurazione · Mancano performance e WCAG complete sul sito corrente

**Evidenza:** i test `theme/design-browser-smoke.py` e `theme/mobile-browser-smoke.py` usano Chromium/Playwright, includono screenshot a 390/768/1440 e controlli di overflow/focus selezionati. I rapporti del 16 novembre dichiarano esplicitamente **nessun Lighthouse live e nessun audit WCAG certificato**.

**Impatto:** non è possibile affermare che LCP, INP, CLS o WCAG 2.2 AA siano soddisfatti per tutte le 141 pagine e tutti gli stati interattivi.

**Azione:** misurare su almeno Home, Academy, un corso nuovo, AI Teaching Lab, ricerca e Product Lab, in IT/EN/ES. Eseguire Lighthouse mobile/desktop, axe o equivalente, screen reader VoiceOver su iPhone/Mac, zoom 200–400%, tastiera, focus, contrasto, aria-live e reduced motion.

**Gate:** registrare i valori misurati, correggere i difetti riproducibili e ripetere la prova. Non inventare uno score di performance.

### F07 — P1 prestazioni · Risorse pesanti e warning del build

**Evidenza:** il tree GitHub contiene `editorial/video/prompt-engineering/Prompt_Engineering.mp4` di circa **20,52 MiB**, un archivio media Teaching Lab di **6,49 MiB**, vari PDF; le pagine Home non devono per questo essere considerate lente, perché non tutte queste risorse sono scaricate all'apertura. I log CI riportano «FFmpeg unavailable: retaining playable video with branded poster fallback» e avvisi di deprecazione Node/punycode/url.parse nel tooling.

**Impatto:** rischio da misurare sulla pagina che incorpora il video e opportunità di migliorare la toolchain; **nessuna conclusione sulle prestazioni di rete senza waterfall reale**.

**Azione:** test dei bytes trasferiti per pagina; anteprima video con preload appropriato, poster ottimizzato e codec/bitrate adeguati; verificare artefatti e cache. Risolvere warning aggiornando con cautela action/dipendenze, dopo test di compatibilità.

**Gate:** benchmark prima/dopo e video sempre fruibile, non semplice riduzione del file nel repository.

### F08 — P1 SEO · Presenza on-page verificata, risultati Google sconosciuti

**Evidenza:** CI verifica **132 URL pubblici**, canonical, meta description, titoli univoci, OG/Twitter, sitemap e assenza di `noindex` non intenzionale. `theme/build-seo.py` ricorda che un `robots.txt` in `/manzo-ai/` non è il `robots.txt` del dominio root. Non abbiamo consultato una proprietà Search Console.

**Impatto:** i segnali tecnici non dimostrano indicizzazione, traffico organico o sitelink reali. Su un dominio GitHub Pages condiviso alcune impostazioni a livello root non sono gestibili direttamente dal progetto.

**Azione:** verificare proprietà Search Console idonea, sitemap effettivamente letta da Google, pagine indicizzate/non indicizzate, soft 404, Core Web Vitals, query, comparsa di pagine preferite e coerenza degli `hreflang`. Non promettere di “attivare” sitelink: Google li genera autonomamente.

**Gate:** report Search Console con dati reali; monitoraggio nel tempo. Nessuna richiesta di acquisto dominio o servizi durante l'audit.

### F09 — P1 prodotto · Demo e SaaS commerciale devono restare distinti

**Evidenza:** `product/preview/preview.js` elabora solo localmente; `product/auth-staging` è un pilota invite-only con config client-side pubblicabile; `product/auth-staging/src/workspace.js` contiene un gate per `workspaceApiEnabled`; la pipeline ha verificato **My Learning API=false e Auth=true**; `product/backend/edge/README.md` dichiara adapter source-only, nessuna Edge Function distribuita. I documenti del 16 novembre attestano un progetto Supabase staging e RLS, ma non un endpoint Learning pronto alla vendita.

**Impatto:** vendere o presentare il preview come piattaforma LMS commerciale completa sarebbe inaccurato. Non è dimostrata una falla RLS sulla base dei soli sorgenti o del flag disattivato.

**Azione:** preservare etichette “anteprima”, “simulazione locale”, “accesso pilota” nei punti di ingresso. Prima di clienti reali occorrono database/backup verificati, integrazione sicura, autorizzazione tenant, workflow email, trattamento dati, supporto, test E2E con sessioni reali e approvazione del titolare.

**Gate:** nessun prodotto a pagamento o elaborazione di dati clienti finché i requisiti di sicurezza, servizio e conformità non sono provati. Budget attuale **0 €**: non abilitare servizi con fatturazione senza consenso esplicito.

### F10 — P1 governance · Mission Copilot non è un'AI generativa operativa sul sito

**Evidenza:** `product/mission-copilot/wrangler.toml` ha `workers_dev=false`, gate Free/Model/Data Protection disabilitati; `docs/MANZO_AI_COPILOT_P4_BETA_PRIVATA_ZERO_EURO_2026-11-18.md` conferma nessun Worker distribuito né inferenza reale. I simulatori presenti sono invece **interazioni deterministiche** o locali. Le verifiche CI attuali testano la politica di blocco, non output da modello online.

**Azione:** distinguere nel copy “simulatore”, “interfaccia deterministica”, “tutor prompt esterno” e “servizio AI attivo”, evitando equivalenze fittizie. Nessuna attivazione prima di check contrattuali, costi, privacy, quota e consenso.

### F11 — P1 documentazione e affidabilità editoriale · Registri in ritardo sulle release

**Evidenza:** `README.md` e `theme/ACADEMY_I18N_STANDARD.md` continuano in alcuni passaggi a riportare **6/9** e a dichiarare mancanti *Modelli mentali* e *Centroni City*, mentre la pipeline del 20 novembre verifica **8/9** sorgenti completi. Un'altra parte dell'inventario segnala tali traduzioni come non presenti. `docs/AI_TEACHING_LAB_I18N_INCREMENTAL_PLAN.md` è più recente e corretta.

**Impatto:** informazioni contraddittorie per manutentori, futuri collaboratori e agenti, con rischio di ricominciare lavori già completati.

**Azione:** generare una sola tabella automatica dal manifest corsi/sorgenti, includere lo stato della pubblicazione e data/commit, aggiornare README/standard dalle evidenze attuali, segnalare come “storico” gli audit precedenti. Non modificare retroattivamente le prove storiche.

**Gate:** nessun rapporto corrente che dichiari mancante una traduzione presente e verificata; ogni nuova release aggiorna il manifest.

### F12 — P1 qualità pedagogica · Molta offerta, ma efficacia non ancora dimostrata

**Evidenza:** repository con corsi specialistici, casi pratici, quiz, feedback, simulatori e rubriche in più lingue. Per AI Teaching Lab sono presenti cinque moduli italiani, laboratori e 79 termini nel glossario. Il front-end di valutazione pubblica pubblica le risposte e si presenta correttamente come **formativo**, non come esame protetto. Non risultano nell'audit esiti documentati di cohorti reali o valutazioni d'impatto di questi ultimi corsi.

**Azione:** campionare per ciascun percorso obiettivo osservabile, prova autentica, feedback che spieghi perché, risposta al caso limite, trasferibilità, fonti e ultimo aggiornamento. Coinvolgere un piccolo gruppo di adulti e almeno un docente per AI Teaching Lab; correggere in base agli errori osservati e non soltanto alle preferenze estetiche. Non introdurre attestati o progressi persistenti fittizi.

**Gate:** rubrica pedagogica per corso e task test con risultati documentati; ciò non equivale automaticamente a certificazione riconosciuta.

### F13 — P2 proprietà, licenze e fonti

**Evidenza:** sito pubblico, contenuti editoriali originali, ZIP storici, video, slide, documenti, codice e riferimenti a fonti esterne. Sono presenti informazioni legali e un metodo editoriale, ma questo audit non ha esaminato contratti/licenze di **ogni** asset o diritto di distribuzione commerciale.

**Azione:** inventario asset e prove di licenza/attribuzione, verifica termini di tool AI e dei media, policy di aggiornamento fonti su compliance/AI Act, data di verifica e responsabile, informativa privacy specifica per eventuali futuri dati B2B.

**Gate:** nessun riutilizzo commerciale di contenuti di titolarità incerta e nessuna affermazione di certificazione normativa senza review professionale.

## E · Quadro delle priorità e ordine di esecuzione

| Priorità | Intervento | Dipendenze | Costo diretto previsto |
| --- | --- | --- | --- |
| **P0 — chiarezza pubblica** | Correggere il contatore fisso «6 risorse» e l'eventuale promessa troppo ampia IT/EN/ES | Aggiornamento copy + test locale | **0 €** |
| **P0 — prodotto formativo** | Concludere AI Teaching Lab EN/ES e distinguere origine delle risorse tradotte da vera pubblicazione | Modulo 05, corso/narrative/assessment/glossary JSON, renderer e QA | **0 €** di hosting aggiuntivo sulla base attuale |
| **P1 — esperienza** | Ridurre duplicazioni Home, mostrare catalogo completo nell'Academy, affinare filtri e navigazione | Revisione UX di una schermata campione per lingua | **0 €** |
| **P1 — coerenza UI** | Unificare renderer delle card e tassonomia, verificare 390/768/1440 e iPhone Safari | Standard card, screenshot/click/keyboard | **0 €** con strumenti disponibili |
| **P1 — misure** | Lighthouse, accessibilità, contenuti delle nuove pagine e video | Browser/device, audit assistivo | **0 €** con misure locali/strumenti gratuiti se disponibili |
| **P1 — architettura** | Piano di superamento graduale dello ZIP e riduzione degli overlay | Manifest, snapshot, confronto output | **0 €** |
| **P1 — SEO e contenuti** | Dati Search Console, citazioni e monitoraggio delle fonti, correzione documenti stantii | Proprietà Google e supervisione umana | **0 €** con Search Console |
| **P2 — prodotto commerciale** | Discovery clienti, scelta verticale, API reale, sicurezza, privacy, budget e supporto | Gate separati e autorizzazioni | **Non attivare spese senza approvazione** |

### Rilascio consigliato in tre sprint, non in un “restyling totale”

**Sprint 0 — Stabilizzazione**  
Allineare i messaggi pubblici, completare la localizzazione di AI Teaching Lab in parti piccole, registrare il manifest e rafforzare il gate i18n. Non toccare le card già visualmente approvate salvo correzioni riproducibili.

**Sprint 1 — AI Web Production e QA visuale**  
Applicare in modo verificabile principi di **Apple Design** (tipografia, comportamento, accessibilità, motion), **Hallmark v2.0** (non-genericità, informazioni reali, design token e anti-cliché), **Impeccable** (rifinitura e QA) e **design-taste-frontend** (direzione originale). Queste sono **linee guida per interventi successivi**: l'audit presente non afferma di aver eseguito launcher esterni delle Skill. Cominciare da Home e Academy, poi da un corso lungo in ognuna delle tre lingue. Test con schermate e decisione di approvazione.

**Sprint 2 — Semplificazione tecnica e prodotto**  
Ridurre overlay e packaging storico con migrazione reversibile, correggere problemi di performance **solo dopo la misura**, pianificare ricerca di mercato e una sola verticale di prodotto professionale. Nessun rollout di backend o servizi fatturabili senza nuovo gate.

## F · Criteri di accettazione della fase di ottimizzazione

- Il portale **non** indica “6 risorse” quando mostra un numero diverso senza spiegarne il significato.
- Le pagine sono nella lingua dichiarata; ogni selettore preserva corso e contesto; nessuna parte IT è mascherata da traduzione.
- Le card Academy rispettano **un'unica geometria**, con due badge massimo e CTA accessibile; titoli senza punti finali.
- Navigazione e ricerca puntano a pagine esistenti; tutti i collegamenti interni, canonical e sitemap passano la CI.
- Zero errori critici riproducibili nei test su telefono, tastiera, screen reader e contrasto dei percorsi prioritari, documentando la copertura reale.
- Performance con valori LCP/INP/CLS misurati e riportati, senza inventare punteggi non osservati.
- Stato Beta, demo, fonte e limite legale dei simulatori rimangono comprensibili.
- Nessun dato personale reale, fatturazione, inferenza esterna o backend commerciale attivati per effetto dell'ottimizzazione grafica.
- Report di audit e checklist di interventi fanno riferimento a commit, evidenza e verifica del risultato.

## G · Fonti e tracciabilità

- [Workflow di rilascio PASS del 20 novembre](https://github.com/manzo8b/manzo-ai/actions/runs/44725699053)
- [CI / orchestrazione](../.github/workflows/deploy-pages.yml)
- [Generatore SEO](../theme/build-seo.py) · [Polish SEO](../theme/seo-final-polish.py) · [Audit link](../theme/site-integrity-audit.py)
- [Copertura editoriale IT/EN/ES](../theme/audit-academy-i18n.py) · [Standard](../theme/ACADEMY_I18N_STANDARD.md)
- [Card Academy](../theme/ACADEMY_CARD_STANDARD.md) · [Publisher Home showcase](../theme/publish-home-showcase.py)
- [AI Teaching Lab IT publisher](../theme/publish-ai-teaching-lab.py) · [Piano localizzazione incrementale](AI_TEACHING_LAB_I18N_INCREMENTAL_PLAN.md)
- [Product Readiness Gate](MANZO_AI_PRODUCT_RELEASE_GATE_2026-11-15.md) · [Backend foundation](../product/backend/README.md)
- [Stato Copilot P4 — non attivo](MANZO_AI_COPILOT_P4_BETA_PRIVATA_ZERO_EURO_2026-11-18.md)
- [Auditoria storica 16 novembre](MANZO_AI_GLOBAL_SITE_AUDIT_2026-11-16.md) — non confondere con lo stato presente
- [Dichiarazione fonti normative: Regolamento UE 2026/1744](https://eur-lex.europa.eu/legal-content/it/TXT/?uri=oj:L_202601744)
- [Stanford HAI AI Index 2026](https://hai.stanford.edu/ai-index/2026-ai-index-report/responsible-ai)

## Conclusione tecnica

**MANZO AI è utilizzabile come portale pubblico di formazione e sperimentazione controllata, con una pipeline di validazione consistente.** Non è però certificata in tutte le sue parti come piattaforma trilingue, accessibile WCAG o veloce secondo i Web Vitals, né è pronta come LMS/SaaS commerciale end-to-end. I principali rischi correggibili nel breve termine sono **informazioni editoriali discordanti**, **localizzazione incompleta di AI Teaching Lab**, **densità crescente della Home** e **complessità delle sorgenti ZIP+overlay**.

**Decisione consigliata:** ottimizzare incrementalmente la base attuale. Non ricominciare il progetto, non aggiungere corsi e non attivare infrastruttura a pagamento prima che i gate siano soddisfatti.
