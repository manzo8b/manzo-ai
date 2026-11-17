# AI Teaching Lab — Revisione editoriale, grammaticale e fattuale
**Data:** 17 novembre 2026  
**Repository:** manzo8b/manzo-ai, ramo principale  
**Campo:** lezioni 01–05, metadati corso, README, anteprima, publisher video e test editoriali  
**Metodo:** lettura mirata dei sorgenti pubblicati in repository, scansioni per incongruenze, controllo di quantità dichiarate rispetto ai dati, verifica selettiva di fonti primarie ed esecuzione di controlli statici mirati.

## Esito complessivo
Sono stati corretti errori editoriali reali e alcune affermazioni troppo assolute. Non sono state trovate prove di false attribuzioni nei riferimenti principali sottoposti a controllo selettivo. **Non è una certificazione scientifica, legale o linguistica esaustiva di ogni frase.**

## Correzioni eseguite

### 1. Ortografia, grammatica e punteggiatura
- `una immagine` → `un'immagine` in corso JSON e modulo 03
- `una osservazione` → `un'osservazione` in corso JSON, moduli 03 e 04
- `una esperienza` → `un'esperienza` nel prompt del modulo 05
- rimossa la sequenza errata `Quale dato ci manca?.` nel modulo 03
- migliorata la formulazione sulla progettazione accessibile: la sola aggiunta di trascrizioni o licenze non garantisce conformità/accessibilità

### 2. Affermazioni non dimostrate o ambigue
- Il README annunciava cinque lezioni di «circa 2.000 parole ciascuna»: conteggio sorgenti circa **3432 / 3062 / 5014 / 2897 / 3263** parole. Ora il testo distingue lunghezza reale, attività e **20 ore soltanto stimate**.
- Il modulo 05 include due laboratori principali e un progetto finale come attività distinta: README aggiornato per non confondere attività con conteggi dei laboratori.
- L'anteprima mostrava due durate incompatibili, **07:04** e **7:43**, mentre indicava il video come non incorporato. Entrambe le durate decorative sono rimosse.
- Il placeholder non presume più che una registrazione sia già disponibile e caricabile; dichiara che il player compare solo se esiste il file previsto.
- Il publisher segnala «Video disponibile» solo quando l'asset è presente e rimuove la durata hardcoded dall'etichetta di accessibilità.
- La dichiarazione del modulo 03 è stata limitata al comportamento verificabile del laboratorio: nessuna **trasmissione automatica dei media verso sistemi generativi esterni**, fermo il dovere di non inserire dati personali su servizi non autorizzati.
- Il modulo 05 ora qualifica correttamente il documento del Garante del 20 ottobre 2026 come **parere favorevole con osservazioni su uno schema di decreto**, non come il decreto definitivo né un'autorizzazione generale all'uso di IA in scuola.

### 3. Fonti primarie verificate selettivamente
- **AI Act articolo 4**, alfabetizzazione in materia di IA: https://ai-act-service-desk.ec.europa.eu/it/ai-act/article-4
- **Garante Privacy**, provvedimento n. 787 del 20 ottobre 2026: https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/10315228
- **CAST UDL Guidelines 3.0**, pubblicate nel 2024: https://udlguidelines.cast.org/
- **OpenAI ChatGPT Images 2.5**, pagina ufficiale: https://openai.com/it-IT/index/introducing-chatgpt-images-2-5/
- **Google DeepMind Gemini Image / Nano Banana**: https://deepmind.google/models/gemini-image/
- **Google Gemini Notebook** (evoluzione di NotebookLM): https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/
- **OECD TALIS 2024**, rapporto sulle condizioni del lavoro docente: https://www.oecd.org/en/publications/2025/10/results-from-talis-2024_28fbde1d/full-report/the-demands-of-teaching_0e941e2f.html

L'esercizio del modulo 02 sul training/test, con otto esempi iniziali e quattro nuovi esempi, è coerente con i risultati **8/8 su training per entrambe le regole**, e rispettivamente **2/4 e 4/4 su test**. Resta una simulazione artificiale, non una prova prestazionale di un modello IA reale.

## Test di regressione
È stato aggiunto il controllo `test_editorial_claims_and_preview_integrity` a `editorial/learning/ai-teaching-lab/tests/test_course.py` per impedire il ritorno dei refusi e delle durate del video inventariate sopra.

Controlli locali di contenuto applicati dopo la modifica:
- JSON corso parseabile: **PASS**
- refusi campionati rimossi: **PASS**
- incongruenza delle durate nell'anteprima: **PASS**
- statistiche README e stato editoriale coerenti: **PASS**
- publisher condizionale aggiornato: **PASS**
- sorgente test regressione presente: **PASS**

**Non confermato:** esecuzione di tutti gli unittest su GitHub Actions, esito del deploy Pages, prova nel browser della pagina risultante. La validazione scientifica con docenti rimane da svolgere.

## Criteri editoriali permanenti
- Separare i fatti documentati dagli esempi sintetici, dalle ipotesi e dalle dimostrazioni simulate.
- Non attribuire frasi testuali a pedagogisti senza fonte diretta; i richiami al loro pensiero devono essere riconoscibili come parafrasi.
- Non promettere esiti di apprendimento, sicurezza, accessibilità o conformità legale senza verifiche.
- Nomi commerciali, disponibilità, prezzi e caratteristiche di modelli IA richiedono riesame periodico.
- Differenziare codice sorgente pronto, build eseguita, pagina raggiungibile e funzione collaudata.
- Mantenere **«Il docente progetta, l'IA assiste, il docente verifica e decide»** come principio di responsabilità.
