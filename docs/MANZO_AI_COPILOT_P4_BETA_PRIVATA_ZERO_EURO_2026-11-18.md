# Mission Copilot P4 — Beta privata controllata

**18 novembre 2026 · Budget massimo 0 € · Non attiva**

## Risultato tecnico

È predisposta una prova futura di Mission Copilot riservata a utenti autenticati e **soltanto con materiale fittizio definito dal server**. Non abbiamo collegato Cloudflare, distribuito un Worker, effettuato inferenze reali o autorizzato alcun pagamento.

Il backend accetta esclusivamente un identificativo di scenario. Qualunque campo libero aggiuntivo, dato personale o tentativo di sostituire l'obiettivo viene respinto prima della chiamata al modello. Il controllo è imposto nel Worker, non soltanto nella pagina HTML.

## Quattro prove sintetiche

| ID | Pubblico | Tipo di attività | Compito |
|---|---|---|---|
| water_cycle | Secondaria di primo grado | Immagini | Ordinare le fasi del ciclo dell'acqua |
| historical_source | Secondaria di secondo grado | Verifica | Distinguere una fonte da un'interpretazione |
| sound_and_transcript | Primaria | Voce | Descrivere un paesaggio sonoro inventato |
| workplace_check | Adulti | Video | Analizzare la comunicazione in un gruppo fittizio |

I dati sono definiti in product/mission-copilot/beta-scenarios.mjs. Il client fornisce solo una proprietà chiamata scenarioId; il testo didattico viene costruito dal server e non dall'utente. Nel primo test non è consentito inviare un brief reale di Mission Studio.

## Protezioni prima dell'inferenza

- Attivazione generale, piano Workers Free, modello gratuito e trattamento dati restano **disattivati** in configurazione.
- Un quinto vincolo, **BETA_SYNTHETIC_ONLY=true**, blocca le richieste che non provengono dai quattro scenari.
- Cloudflare Access dovrà autenticare un tester e verificare l'audience. La chiave HMAC e gli identificativi non devono essere pubblicati o inseriti nel frontend.
- La quota atomica resta 20 richieste globali/giorno UTC, massimo 3 per tester e 60 secondi tra richieste dello stesso tester.
- Il Durable Object prova a eliminare automaticamente il registro dei contatori pseudonimi dopo la mezzanotte UTC, tramite un alarm schedulato. La scadenza non dimostra cancellazione garantita di eventuali backup Cloudflare o dei metadati conservati dalla piattaforma.
- Logging applicativo del Worker disabilitato; le impostazioni dei log account, Access e modelli devono essere verificate separatamente.
- Nessuna CORS pubblica, nessuna route e workers.dev disattivato. **Non esiste ancora un endpoint utilizzabile dall'esterno.**
- Le risposte, se abilitate in futuro, rimarranno *bozze non approvate*; la decisione è del docente.

## Valutazione pedagogica quando avremo risposte reali

Per ognuno dei quattro casi una persona competente assegnerà 0 (non soddisfatto), 1 (parziale), 2 (soddisfatto) a: **allineamento obiettivo-attività**, **accuratezza e prove**, **carico cognitivo**, **accessibilità**, **controllo e revisione umana**.

Registrare modello, data, scenario, valutazione, motivazioni e correzioni. Un test tecnico di formato non costituisce validazione pedagogica. **Non attribuire punteggi ai risultati mock.**

## Prova del modello senza accedere al nostro backend

Cloudflare dichiara che il proprio LLM Playground permette una prova nel browser senza configurazione o autenticazione (alla data del controllo). Si può usare esclusivamente per sperimentare manualmente prompt sintetici, non per verificare né attivare l'integrazione con Mission Studio.

https://playground.ai.cloudflare.com/

Se vengono richiesti credenziali di fatturazione, servizi Paid o crediti, interrompere: il tetto resta 0 €.

## Verifica account Cloudflare — ancora da eseguire

Non è disponibile una connessione al tuo account Cloudflare; pertanto **non ho potuto controllare piano, metodi di pagamento, disponibilità effettiva dell'API o consumi reali**.

Quando il titolare sceglierà di effettuare la verifica:

1. Aprire https://dash.cloudflare.com/ e controllare Workers & Pages, piano Free e eventuali servizi a pagamento.
2. Verificare se Zero Trust Free è già attivo. La documentazione ufficiale indica che il suo onboarding richiede **dati di pagamento pur dichiarando il piano non addebitato**. Non completare quel passaggio senza decisione esplicita.
3. Controllare possibilità di policy Access limitata ai soli tester, senza accesso pubblico e senza inserire segreti nel repository.
4. L'attuale configurazione workers_dev=false e senza route rende il Worker irraggiungibile anche a un tester: ogni futura route dovrà essere creata solo dietro Access, dopo revisione.
5. Verificare nel dashboard che Gemma 4 sia disponibile sul Free e che il contatore Neurons parta da quote note. Nessun servizio o modello Paid.
6. Esaminare informativa privacy, DPA, eventuali trasferimenti e log a livello account prima di inviare anche soltanto dati sintetici a un servizio esterno.
7. Soltanto con autorizzazione separata eseguire **una** inferenza sintetica, leggere i Neurons realmente consumati dal dashboard e confrontare il risultato con la rubrica pedagogica.

Non condividere password, segreti, token API, codici di verifica o dati di pagamento. Eventuali schermate di account devono nascondere le informazioni sensibili.

## Fonti ufficiali

- https://developers.cloudflare.com/workers/configuration/cloudflare-access/
- https://developers.cloudflare.com/cloudflare-one/setup/
- https://developers.cloudflare.com/workers-ai/platform/pricing/
- https://developers.cloudflare.com/workers-ai/models/gemma-4-26b-a4b-it/
- https://developers.cloudflare.com/durable-objects/api/alarms/
- https://developers.cloudflare.com/changelog/post/2026-02-24-deleteall-deletes-alarms/

## Gate di rilascio

**Predisposto:** scenari sintetici fissi, autenticazione simulata nei test, quota globale, scadenza contatori, preflight statico, QA automatica.

**Non completato:** verifica dell'account reale, valutazione GDPR definitiva, autenticazione e routing Cloudflare reali, prima chiamata a modello, misura reale dei Neurons, valutazione pedagogica su risposte generative.

**Verdetto:** pronto per un futuro collaudo privato **nel codice**, non attivato. Nessun pagamento o modello è stato eseguito.
