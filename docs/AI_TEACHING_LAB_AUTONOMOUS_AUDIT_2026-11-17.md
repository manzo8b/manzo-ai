# AI Teaching Lab — Audit autonomo e correzioni
**Data:** 17 novembre 2026  
**Repository:** manzo8b/manzo-ai (branch principale)  
**Ambito:** Studio immagini, Studio voce, Studio video, Workspace multimediale, QA GitHub Pages

## 1. Correzioni eseguite senza input dell'utente

### A — Riprendi una bozza del kit
- Aggiunto nel Workspace un controllo «Hai già lavorato qui? Riapri una bozza salvata»
- Accetta soltanto manifest JSON v0.1 del Workspace fino a 2 MB
- Ripristina titolo, destinatari, obiettivi, pianificazione, note e schede dei tre Studi
- **Non** ripristina automaticamente la decisione di approvazione finale: checklist azzerata e nuovo controllo obbligatorio
- **Non** contiene o recupera immagini, audio o video originali: questi file devono essere conservati separatamente
- Nessun backend o autosalvataggio occulto nel dispositivo; l'utente esporta e reimporta volontariamente

### B — Provenienza delle scene video
- Corretto import: il Workspace ora conserva la lista delle scene, origine (locale/IA esterna/terzi), fonte/licenza e nome del file associato
- Queste informazioni compaiono in una sezione espandibile delle schede nel Workspace
- Aggiunta la provenienza dichiarata al documento HTML esportato; i contenuti sono sottoposti a escaping prima di produrre HTML
- Conservazione delle quattro conferme di revisione come conteggio anche dopo il ripristino del manifest

### C — Import robusto
- Validazione della famiglia di schemi (immagini/voce/video), della struttura e delle approvazioni dichiarate
- Un video dichiarato approvato senza scene non viene accettato
- Una scheda con checklist assenti o falsificate con valori diversi da `true` viene respinta
- Le approvazioni restano **autodichiarazioni**, non verifiche crittografiche o certificazioni indipendenti

### D — Riduzione scroll nei tre Studi
- In Studio immagini, voce e video gli esempi contestuali dei campi ora sono `details` apribili su richiesta
- Il percorso introduttivo in tre card diventa su mobile una guida espandibile
- Campi a 16px su mobile per limitare lo zoom involontario di Safari
- Conservati i link di collegamento al Workspace e la procedura di validazione del docente
- Mantieni titolo senza punto finale e gerarchia visiva bianco/nero/blu/arancione/giallo/rosso

### E — Contract QA automatica
Aggiunto `theme/check-ai-teaching-lab-contracts.cjs` (solo moduli standard Node):
- Sintassi JavaScript di tutti gli script inline dei quattro Studi
- Duplicazione degli ID statici, presenza dei gate di approvazione
- Coerenza degli schemi JSON e dei link tra gli Studi
- Presenza delle guide per principianti e dei controlli di ripristino
- Integrità della provenienza delle scene
- Test di normalizzazione e import con schede video valide/corrotte
- Presenza di tutte le pagine generate, quando eseguito con `--site _site`
- Workflow GitHub Pages aggiornato: trigger su modifiche del test e esecuzione durante il build

## 2. Test svolti
- **PASS**: 11 script inline dei quattro moduli compilano senza errori sintattici (3+3+3+2)
- **PASS**: ID statici univoci nei quattro documenti
- **PASS**: prova funzionale isolata della validazione di scheda video; provenienza e conteggio delle verifiche conservati
- **PASS**: una checklist con stringhe al posto di valori booleani viene respinta
- **PASS**: workflow sorgente contiene il richiamo al contratto QA prima della pubblicazione

> Questi PASS derivano da ispezioni del codice e prove isolate eseguite durante la revisione. Il nuovo script CI è stato aggiunto, ma l'esito dell'esecuzione su GitHub Actions **non** è stato osservato in questa sessione.

## 3. Non verificato / vincoli
- GitHub Pages: esito aggiornato di Actions e raggiungibilità HTTP 200 non confermati
- Interazioni reali con iPhone Safari / desktop Chrome e VoiceOver non collaudate
- Microfono, codec audio, esportazione WebM e riproduzione dei file su dispositivi reali non testati
- Esperimenti didattici con docenti principianti non ancora realizzati
- Nessun modello generativo è stato connesso: la generazione di immagini/voce/video rimane esterna

## 4. Lavori che richiedono ambiente o feedback esterno
1. Controllare il risultato di GitHub Actions e il deploy pubblico dopo il commit
2. Smoke test manuale Safari iPhone / desktop, inclusi input JSON e ripristino
3. Esercizio assistito con almeno un docente principiante, osservando gli errori reali
4. Test su materiali audiovisivi reali e relative licenze
5. Eventuale integrazione API protetta solo dopo valutazione privacy/costi

## 5. Collegamenti
- `tools/ai-teaching-image-studio/index.html`
- `tools/ai-teaching-voice-studio/index.html`
- `tools/ai-teaching-video-studio/index.html`
- `tools/ai-teaching-workspace/index.html`
- `theme/check-ai-teaching-lab-contracts.cjs`
- `.github/workflows/deploy-pages.yml`

**Criterio del progetto:** Il docente progetta, l'IA assiste, il docente verifica e decide.
