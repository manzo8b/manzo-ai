# MANZO AI — Engineering Assurance · Modulo 06

**Edizione:** 15 novembre 2026 · **Stato:** implementazione editoriale in IT/EN/ES, in attesa di collaudo CI e deployment
**Titolo IT:** Il codice che sembrava corretto
**Sottotitolo:** Allucinazioni nello sviluppo software, controllo qualità e responsabilità verso il cliente

## Obiettivo formativo

Distinguere allucinazione tecnica (API, pacchetto, configurazione, prova di test inventati) da difetto software non necessariamente riconducibile a un'allucinazione (autorizzazioni, robustezza, race conditions). Comprendere la catena che collega il difetto alla possibile esposizione del committente e definire un processo di rilascio sostenuto da evidenze.

### Architettura di contenuto

Sei sezioni:
1. La demo non è la consegna
2. Che cosa significa allucinare mentre si programma
3. Dal difetto tecnico al rischio commerciale
4. La responsabilità del professionista
5. Verificare prima di un rilascio
6. Il valore economico della verifica

Il dossier contiene un esempio tecnico di accesso improprio tra tenant (con correzione dichiarata **parziale**), cinque fasi di propagazione del rischio, otto quality gate, quattro casi e quattro domande con risposta motivata.

### Qualità della scrittura

- Prosa argomentativa, non aneddotica o sensazionalista.
- Nessuna uguaglianza automatica fra codice generato e codice vulnerabile.
- Nessuna equivalenza tra errore tecnico e allucinazione.
- Nessun importo o perdita contrattuale attribuiti ad aziende reali senza prove.
- Esempio economico **fittizio**: 3 ore × €12.000/h = €36.000 di impatto ipotetico, escluse altre voci.
- Ruolo del committente: la qualità del servizio comprende sicurezza, affidabilità, evidenze, manutenzione e responsabilità, non soltanto velocità di programmazione.
- Coerenza scientifica e giuridica: le conseguenze commerciali e contrattuali sono **possibili**, non inevitabili.

## Fonti e limiti

- **F9 GitHub Docs** — Review AI-generated code. https://docs.github.com/en/copilot/tutorials/review-ai-generated-code
- **F10 OWASP LLM05:2025** — Improper Output Handling. https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/
- **F11 NIST SP 800-218** — SSDF v1.1 (final 2022). https://csrc.nist.gov/pubs/sp/800/218/final
- **F12 Spracklen et al., USENIX Security '25** — We Have a Package for You! https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen

Lo studio USENIX analizza un determinato insieme di modelli, prompt e campioni; eventuali percentuali non sono trasferite ad altri sistemi o periodi. OWASP LLM05 riguarda *improper output handling* nei sistemi LLM: non definisce ogni errore di codice come allucinazione. Il SSDF NIST contiene buone pratiche per sviluppo sicuro, non una certificazione automatica.

## Percorsi

- IT: `/manzo-ai/it/impara/allucinazioni-ai-verificabilita/coding/`
- EN: `/manzo-ai/en/learn/ai-hallucinations-verification/coding/`
- ES: `/manzo-ai/es/aprende/alucinaciones-ia-verificacion/coding/`

Il sesto modulo viene aggiunto al curriculum della pagina principale e il dossier specialistico collegato automaticamente in fase di pubblicazione. La lezione principale risulta composta da **6 moduli, 10 casi e 10 quiz di base**, ai quali si affiancano **4 casi e 4 quesiti specialistici**, per 14+14 complessivi; restano 70 caselle nel cruciverba e 12 fonti nella bibliografia principale.

## Implementazione e QA

Sorgenti in `editorial/learning/hallucinations/coding-{it,en,es}.json`, `coding.css`, `coding.js`. Il publisher `theme/publish-hallucinations-coding.py` viene eseguito **dopo** il publisher del corso generale e **prima** di SEO/navigazione. Il rilascio `site-v0.7.zip` resta invariato.

Verifiche richieste:
- Publisher idempotent per quanto riguarda le card già pubblicate; verifica delle pagine e dei collegamenti.
- Controllo di sintassi Python e JavaScript.
- Desktop e mobile con Playwright: sezioni, casi, checkbox, quiz, navigazione, overflow orizzontale.
- Stessa esperienza IT/EN/ES e nessuna trasmissione o archiviazione delle risposte dell'utente.
- Deploy GitHub Pages riuscito e test delle tre URL prima di dichiararle online.

La spunta di una checklist è un'interazione didattica; non equivale alla prova di avvenuto controllo di qualità.
