# MANZO AI · Mission Copilot P1 — integrazione locale e UX

**Data:** 18 novembre 2026  
**Vincolo economico:** massimo **0 €**  
**Stato:** interfaccia pilota offline, test automatici, **nessun modello IA attivato**.

## Che cosa è stato realizzato

1. **Ponte tra i due formati:** il brief preesistente `ai-teaching-lab-mission-v0.1` viene trasformato nei cinque campi attesi dal backend P0:
   `tema`, `destinatari`, `durataMinuti`, `tipoRisorsa`, `obiettivo`. I campi non previsti non vengono trasferiti.
2. **Simulazione locale di una proposta didattica:** obiettivo, due attività ed evidenza di verifica. Le frasi sono costruite da **regole statiche**, non da un modello, e cambiano in base alla tipologia di risorsa scelta.
3. **Anteprima visiva opzionale:** accessibile soltanto tramite `?copilot=preview`; nel normale flusso Mission Studio rimane nascosta. Una volta aperta, mostra sempre «Simulazione locale · Nessuna IA attiva».
4. **Controllo umano:** l'utente può, con conferma, applicare soltanto l'obiettivo suggerito al brief esistente. Il brief non viene mai approvato automaticamente. Ogni modifica al form invalida l'anteprima, evitando di applicare suggerimenti superati.
5. **Sicurezza P1:** nessun token, API endpoint esterno, `fetch`, account, scrittura remota, cookie, salvataggio persistente o chiamata IA dal browser. Il filtro dei contatti è prudenziale e **non può garantire l'anonimizzazione dei dati**.
6. **Non impatta il sito pubblico corrente:** l'utente senza query flag vede esattamente il percorso ordinario, mantenendo import/export JSON e laboratori.

## Codice

- `tools/ai-teaching-launchpad/mission-adapter.mjs` — pure functions di mapping, validazione e dimostrazione locale.
- `tools/ai-teaching-launchpad/copilot-preview.mjs` — interfaccia con stato invalidabile e conferma docente.
- `tools/ai-teaching-launchpad/index.html` — card P1 nascosta per impostazione predefinita e import del controller solo in modalità preview.
- `tools/ai-teaching-launchpad/mission-adapter.test.mjs` — **10 test** Node senza rete e senza modelli.
- `theme/publish-ai-teaching-lab.py` — pubblica i due moduli `.mjs` a fianco del Mission Studio.
- `theme/check-ai-teaching-lab-contracts.cjs` e `.github/workflows/deploy-pages.yml` — impediscono di distribuire la preview senza file, marcatori e test.

## Indirizzo di prova (non chat generativa)

`https://manzo8b.github.io/manzo-ai/it/formazione/ia-per-la-didattica/inizia/?copilot=preview`

Questo indirizzo **non** produce risultati IA e non connette Cloudflare. Serve esclusivamente a provare le interazioni, il controllo docente e il percorso della bozza.

## QA e criteri di accettazione

- Test dell'adapter in quattro tipologie e quattro pubblici: input accettati dal validatore P0 del Worker.
- Validazione degli output e rifiuto di approvazioni, status o schemi contraffatti.
- Simulazione localmente deterministica e riconoscibile, con `teacherApproval:false` e `modelUsed:false`.
- Applicazione dell'obiettivo soltanto con consenso; i cambiamenti invalidano proposte precedenti.
- Integrità dei file pubblicati verificata dai controlli del publisher.
- **Da verificare prima di approvare visivamente:** Safari iPhone reale, Chrome/desktop, VoiceOver, focus e overflow, senza assumere che una build verde sia un audit accessibilità.

## Fuori ambito · nessuna spesa autorizzata

Il prossimo livello **non** consiste nell'inserire nel front-end un token privato del Worker. Prima del collegamento reale occorre una soluzione di autenticazione/abuso e un contatore distribuito per utilizzo globale, verificando che rientrino davvero nel Free Tier senza billing. Le chiavi non si pubblicano e non si richiede ancora alcun accesso Cloudflare.

Il principio resta: *l'IA propone; il docente rivede, verifica e decide*.
