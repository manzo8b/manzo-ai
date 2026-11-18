# Mission Copilot — P5.6 · Cloudflare Access e ingresso privato

**18 novembre 2026 · Verifica delle opzioni prima dell'onboarding · Budget autorizzato 0 €**

## Esito

**Access reale NON configurato.** Il titolare ha mostrato in Cloudflare un account sul piano Workers Free ($0); in Workers & Pages compareva `Set up Zero Trust` e nessun Worker esistente. Il Playground ufficiale ha risposto a un prompt sintetico con Gemma 4, ma non è stata fatta alcuna chiamata dall'account via il Worker Mission Copilot. Non sono stati creati servizi, route, API token, sessioni Access, piani Paid o metodi di pagamento.

### Vincolo economico sull'onboarding

La pagina ufficiale **Get started · Cloudflare One** (aggiornata 12 ottobre 2026) richiede prima un'organizzazione Zero Trust e poi un piano. Cloudflare scrive esplicitamente che **i dati di pagamento sono richiesti anche per Zero Trust Free**; dichiara che quel piano non sarà addebitato. Per il progetto non è autorizzato aggiungere carte né accettare servizi a pagamento. Di conseguenza **la configurazione reale di Access resta sospesa** senza decisione separata del titolare.

Il piano **Workers Free** è distinto dal piano **Zero Trust Free**: la presenza del primo non dimostra l'attivazione del secondo.

## Strategia di protezione dopo l'eventuale onboarding

Cloudflare, dal 14 agosto 2026, consente policy Access applicate **direttamente al Worker**, su tutti i suoi domini, anche le preview. È preferibile a una policy limitata a un solo hostname. Per la futura beta:

- solo Worker `manzo-ai-mission-copilot-preview`, non impostazione globale di account;
- policy *Cloudflare account members* con accesso limitato ai tester previsti, non regole *Everyone*, bypass o interi domini email;
- applicare policy prima dell'eventuale esposizione di un endpoint e verificare sul Worker `ctx.access.aud` e `ctx.access.getIdentity()`;
- l'applicazione Worker non deve accettare JWT di intestazioni fornite dal browser come sostituto di `ctx.access`;
- `ctx.access` non viene propagato attraverso Service Bindings, quindi non progettare una catena Worker→Worker basandosi sul passaggio implicito dell'identità;
- `QUOTA_HASH_SALT` e `ACCESS_AUD` solamente nei segreti/variabili server dopo il controllo account; non nel repository né in GitHub Pages.

**Nota operativa:** attualmente `workers_dev=false` e non sono definite route. Il Worker è intenzionalmente irraggiungibile. Non pubblicare un Worker anche privato senza rivedere in un gate separato router, Access, segreti e privacy.

## Simulazione locale senza Access Free e senza pagamento

Cloudflare documenta `access.dev` per `wrangler dev`, utile per verificare gli stessi metodi `ctx.access.aud` e `getIdentity()` senza una sessione reale né deploy. Esempio **soltanto per una copia temporanea locale**, non da aggiungere al `wrangler.toml` protetto e non da distribuire:

```toml
[access.dev]
aud = "access-audience-preview-test-v1"

[access.dev.identity]
email = "fictional-teacher@example.test"
```

Il blocco `access.dev` è simulato, **non è un controllo di accesso in produzione**. **Attenzione:** un vero binding Workers AI può consumare Neurons anche durante `wrangler dev`; il P5.6 non effettua invocazioni del modello e usa esclusivamente test Node con `AI.run` simulato. Il Worker in GitHub continua disattivato con tutti i flag di sicurezza sul valore `false`; pertanto, senza ulteriori fixture, il comportamento previsto dell'endpoint è `COPILOT_DISABLED`. Per verificare *anche* il percorso di inferenza senza chiamate esterne si usano i test Node con `AI.run` mock, quota mock e identità fittizie.

Confermati dal codice:
- `authenticatedPrincipal` verifica audience, ricava l'email da `ctx.access.getIdentity()` e la pseudonimizza con HMAC;
- niente `ctx.access`, audience errata, identity mancante o non valida: risposta 401 e nessuna inferenza;
- quote e controlli privacy precedono ogni `env.AI.run`.

I test P5.6 aggiunti a `worker.test.mjs` ripetono questi controlli con identità inventate e non usano Cloudflare né credenziali.

## Prossimo gate P5.7: verifiche sul dashboard prima dell'attivazione

1. Aprire la dashboard Cloudflare e scegliere `Zero Trust` solo per osservare la schermata iniziale: **non inserire team name, carta o informazioni sensibili**.
2. Verificare se l'account richiede ancora onboarding (probabile, secondo lo screenshot `Set up Zero Trust`) oppure se esiste già un'organizzazione Zero Trust attiva. Uno screenshot con dati oscurati basta per il controllo.
3. Se viene richiesta la carta e il titolare non intende fornirla, interrompere il percorso Access reale e rimanere sulla simulazione locale; non attivare il Worker senza autenticazione.
4. Se il titolare decide separatamente di procedere con le condizioni gratuite, rivedere prima DPA/privacy/log e policy per un solo tester, poi configurare Access prima di qualunque esposizione; documentare sempre l'assenza di addebiti e la quota Workers AI.
5. La prima inferenza privata userà unicamente `scenarioId` fisso, non dati degli studenti; registrare il consumo reale dei Neurons dal dashboard dell'account.

## Fonti ufficiali

- https://developers.cloudflare.com/cloudflare-one/setup/
- https://developers.cloudflare.com/workers/configuration/cloudflare-access/
- https://developers.cloudflare.com/changelog/post/2026-08-14-workers-access/
- https://developers.cloudflare.com/cloudflare-one/access-controls/applications/choose-application-type/

**Verdetto:** P5.6 offline e ricerca documentale pronta; test identità mock da sottoporre a CI; onboarding reale bloccato dal gate di pagamento/privacy. Budget effettivo del progetto invariato: 0 €.
