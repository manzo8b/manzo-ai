# MANZO AI v0.7 — Laboratorio tecnico di Prompt Engineering

Data editoriale: 29 ottobre 2026. **Pacchetto di pubblicazione pronto, ma ZIP binario non ancora caricato su GitHub Pages.**

## Decisione di prodotto

Il nuovo materiale tratta i principi mostrati da Anthropic in «Prompting 101 | Code w/ Claude» come **fonte facoltativa**. Il corso è originale e autonomo: non richiede la visione del video, non usa embed, non trascrive le slide Anthropic e non è affiliato all'azienda.

## Contenuti

- 3 pagine trilingui di laboratorio tecnico (IT, ES, EN), durata stimata 90 min.
- Progettazione a due livelli: istruzioni affidabili e dati dinamici non attendibili.
- Delimitatori XML, esempi few-shot, vincoli e output JSON.
- JSON Schema concettuale, contratti di input/output e controllo di coerenza.
- Quattro fixture sintetiche su controllo di consegne commerciali e prompt injection.
- Script di verifica Python 3 offline con sola libreria standard; non chiama API e non misura modelli.
- Failure modes, criteri di accettazione, metodi per confronti riproducibili e esercizio finale.
- Avvertenza sulla non compatibilità del response prefill con Claude 4.6 e successivi, confermata dalla documentazione ufficiale.

## Percorsi previsti

- `/it/prompt-mastery/laboratorio-tecnico/`
- `/es/prompt-mastery/laboratorio-tecnico/`
- `/en/prompt-mastery/technical-lab/`

I collegamenti sono integrati in M03, AI Academy, Risorse, Guida Prompt Mastery, Video e slide e navigazione del sito.

## Verifiche effettuate localmente

- 82 pagine generate; 3 pagine aggiunte rispetto alla v0.6.
- Tutti i collegamenti interni e frammenti HTML controllati; 0 errori.
- Un solo H1 per pagina, JSON-LD parsabile, alternates trilingue.
- Quattro test di riferimento Python passati; ulteriore controllo delle differenze negative.
- Il codice JavaScript principale supera il controllo sintattico `node --check`.
- Le immagini, il PDF e il PPTX delle slide M01 sono rimasti byte-identici alla v0.6.
- Non effettuati test del corso con un LLM reale né prove di usabilità su browser o smartphone.

## Distribuzione

Il workflow `.github/workflows/deploy-pages.yml` riconosce `site-v0.7.zip`, dà priorità a questo pacchetto rispetto alla v0.6 e verifica le tre nuove pagine, i file Python/JSON e le pagine preesistenti. Il solo aggiornamento del workflow **non pubblica** la versione 0.7: per farlo occorre caricare lo ZIP binario nella radice del repository e verificare un run di GitHub Actions riuscito.

Fonti:
- Video originale Anthropic: https://www.youtube.com/watch?v=ysPbXH0LpIE
- Prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Structured outputs: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- Compatibility / API errors: https://platform.claude.com/docs/en/api/errors
