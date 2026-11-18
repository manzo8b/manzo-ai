# MANZO AI · Mission Copilot P3
## Verifica preventiva di costi, privacy e attivabilità — 18 novembre 2026

**Tetto autorizzato:** €0 effettivi, senza upgrade, addebiti automatici o credito prepagato.  
**Esito:** **preflight dei sorgenti PASS; attivazione reale BLOCCATA.**  
**Cloudflare connesso:** NO. **Modello IA chiamato:** NO. **Consumi Neurons misurati:** NO.

### 1. Stato tecnico verificabile

Nel repository sono disponibili:
- `product/mission-copilot/worker.mjs`: IA bloccata se non sussistono approvazioni distinte di piano, modello e trattamento dati; autenticazione Cloudflare Access; quota globale atomica su Durable Object.
- `product/mission-copilot/wrangler.toml`: `workers_dev=false`, nessuna route pubblica, `COPILOT_ENABLED=false`, `FREE_PLAN_CONFIRMED=false`, `MODEL_FREE_CONFIRMED=false`, `DATA_PROTECTION_CONFIRMED=false`; logging Worker e invocation logs disabilitati. Nessuna credenziale pubblicata.
- `product/mission-copilot/zero-euro-preflight.mjs`: verifica statica offline; produce un rapporto JSON con stato `BLOCKED_NOT_CONNECTED` e stima conservativa; **non può leggere il tuo account Cloudflare né chiamare modelli**.
- `product/mission-copilot/zero-euro-preflight.test.mjs`: test di costo, quote, manomissione della configurazione e mancanza di log.
- `tools/ai-teaching-launchpad/copilot-preview.mjs`: demo locale non generativa dietro `?copilot=preview`, senza connessione all'API.

La build GitHub Pages verifica che le impostazioni rimangano disattivate, che i test superino i controlli e che il preflight possa produrre un rapporto `configSafe=true` pur indicando `safeToEnablePublicInference=false`. Questo doppio risultato **è corretto**: sicurezza dei file non implica autorizzazione di un servizio reale.

### 2. Preventivo tecnico — NON fatturazione effettiva

Fonte Cloudflare Workers AI Pricing, verificata il **18/11/2026**:
- Modello ipotizzato: `@cf/google/gemma-4-26b-a4b-it` (indicato disponibile su Free).
- Listino: **9.091 Neurons / milione di token in input** e **27.273 Neurons / milione di token in output**.
- Quota Workers AI Free: **10.000 Neurons per giorno**, reset alle 00:00 UTC.
- Controllo applicativo predisposto: **20 richieste totali al giorno** (max **3 per docente**, intervallo almeno 60 secondi).
- Scenario prudenziale ipotizzato: **6.000 token input + 650 output per richiesta**. Il server già limita l'output a 650 token, ma non può conoscere con assoluta certezza il numero di token interni del modello.
- Stima **1.446 Neurons/giorno** usando il massimo di 20 richieste dello scenario. Moltiplicando per un **fattore cautelativo 4**: **5.784 Neurons/giorno**, sotto la soglia interna di pianificazione di 8.000.
- Questo calcolo **NON garantisce** il consumo reale, il valore tariffario futuro, il numero di token nascosti o che altre app dello stesso account non consumino la quota condivisa. Il limite di 20 richieste non è un contatore preciso di Neurons. Resta indispensabile il controllo dal dashboard Cloudflare.

**Vincolo di release:** se l'account non è rigorosamente Workers Free, se il modello diventa Paid, se la quota cambia o se occorrono addebiti/crediti, Mission Copilot resta OFF.

Fonti ufficiali:
- https://developers.cloudflare.com/workers-ai/platform/pricing/
- https://developers.cloudflare.com/changelog/post/2026-07-28-models-require-workers-paid/
- https://developers.cloudflare.com/workers-ai/models/gemma-4-26b-a4b-it/
- https://developers.cloudflare.com/durable-objects/platform/pricing/

### 3. Cloudflare Access — blocco esterno ancora esistente

Cloudflare Zero Trust Free richiede nella procedura di onboarding **dati di pagamento**, benché Cloudflare indichi che il piano Free non viene addebitato. Non ho accesso a un account Cloudflare collegato né ho creato un account. Non è autorizzato alcun inserimento di carta, upgrade o collegamento automatico.

Prima di realizzare un test reale, l'amministratore deve esaminare:
1. Tipo di account e piano Workers **Free**, nessun upgrade o billing a consumo.
2. Eventuale Zero Trust Free e condizioni di inserimento dati pagamento.
3. Applicazione Cloudflare Access privata a invito, con identità test non di studenti.
4. Verifica dell'audience effettiva `ACCESS_AUD` senza inserirla nel codice pubblico; chiave `QUOTA_HASH_SALT` come segreto server.
5. `GLOBAL_QUOTA` SQLite disponibile nel Free e quota a livello account.
6. Strumenti dashboard per registrare **Neurons usati**, errori e richieste aggregate, senza conservare prompt e risposte.

Fonti:
- https://developers.cloudflare.com/cloudflare-one/setup/
- https://developers.cloudflare.com/workers/configuration/cloudflare-access/

### 4. Privacy-by-design — controllo prima dei dati reali

**Ambito ammesso nella futura beta:** solo docenti maggiorenni e briefing didattici con argomenti generali o sintetici. Non usare nomi reali, fotografie, voci, indirizzi, numeri di registro, dati sanitari, valutazioni, PEI o informazioni riconducibili a studenti.

Dati che l'architettura potrebbe trattare dopo attivazione:
- **Identità del docente** gestita da Cloudflare Access; il Worker la usa per creare un HMAC pseudonimo. L'email può essere comunque trattata dai sistemi di autenticazione di Cloudflare; l'HMAC **non rende completamente anonimo** il trattamento.
- **Brief didattico** inviato temporaneamente a Workers AI per ricevere proposte; il prototipo non lo salva nel Durable Object. Il modello e il provider lo elaborano come contenuto del cliente.
- **Contatori quota**: giorno UTC, identificatori HMAC, numero delle prenotazioni e ultimo timestamp; il modello non riceve email.
- **Eventuali metadati infrastrutturali** e log a livello account, da verificare autonomamente. Disattivare `[observability]` impedisce la registrazione configurata del Worker ma non dimostra l'assenza di tutti i log di servizi esterni.

**Punti prima del via libera:** identificare titolare e responsabili, finalità e base giuridica, informativa specifica sull'uso IA, DPA/condizioni Cloudflare, localizzazione/trasferimenti dati, gestione dei diritti, conservazione, valutazione del rischio e necessità o meno di DPIA. La pagina pubblica non deve dichiarare che il sito non tratta dati se verrà effettivamente attivato un login.

Riferimenti ufficiali:
- Cloudflare data usage: https://developers.cloudflare.com/workers-ai/platform/data-usage/
- Cloudflare Gateway logging (se in futuro usato): https://developers.cloudflare.com/ai-gateway/observability/logging/
- Cloudflare Workers Logs: https://developers.cloudflare.com/workers/observability/logs/workers-logs/
- Garante Privacy, parere sull'IA nelle scuole del 20/10/2026: https://www.garanteprivacy.it/web/guest/home/docweb/-/docweb-display/docweb/10315228

Il Garante evidenzia la necessità di evitare dati personali di studenti nei sistemi IA generativi e di definire tutele appropriate nell'ambito scolastico. L'attuale filtro automatico basato su pattern è **solo una barriera parziale**, non una garanzia di anonimizzazione.

### 5. Checklist per l'accettazione

| Controllo | Stato |
|---|---|
| Sorgenti disattivati e segreti assenti | PASS (statico) |
| Test quote globali e identità simulate | PASS (mock) |
| Modello gratuito verificato da documentazione pubblica | PASS (alla data) |
| Calcolatore conservativo offline | PASS (assunzioni dichiarate) |
| Worker pubblicato ed autenticazione Cloudflare attiva | NON ESEGUITO |
| Piano e dati pagamento verificati sull'account utente | NON VERIFICABILE |
| Neurons misurati sul dashboard dell'account | NON ESEGUITO |
| Valutazione privacy e documentazione legale approvate | DA COMPLETARE |
| Pubblicazione pubblica dell'IA | VIETATA fino ai gate |

### 6. Prossima decisione

Per ora **non creare un account o chiedere credenziali**. Se l'onboarding Cloudflare richiede una carta o un piano incompatibile con le condizioni desiderate, si manterrà il copilota locale e si valuterà un provider o una soluzione alternativa effettivamente gratuita. Il passaggio successivo concreto è la verifica consapevole dell'account e dell'informativa privacy, prima di eseguire la **prima inferenza sintetica**.

**Sicurezza ≠ efficacia pedagogica**: anche con account gratuito e privacy chiarita serviranno test qualitativi con materiali fittizi, revisione critica delle proposte e prova su Safari iPhone.
