# Mission Copilot P5.7 — autenticazione alternativa con Supabase Free

**18 novembre 2026 · preparazione offline · budget vincolante €0 · nessun deploy**

## Decisione tecnica

L'onboarding di Cloudflare Zero Trust Free richiede un metodo di pagamento, come confermano sia la documentazione Cloudflare sia la schermata di checkout mostrata dal titolare. La pagina indica $0/mese ma prevede l'autorizzazione di possibili addebiti successivi. Il progetto non autorizza la memorizzazione di carte, servizi a pagamento o l'attivazione di Zero Trust.

Manteniamo Workers AI Free come motore generativo e proponiamo **Supabase Auth sul piano Free** per identificare esclusivamente i tester. La stessa organizzazione MANZO AI risulta **Free** attraverso la connessione Supabase, con il progetto già esistente `bjydnaejpxwubmxpnpnv` (regione eu-west-1, stato ACTIVE_HEALTHY). Non creare un nuovo progetto Supabase. Nel repository è presente `product/auth-staging/config.json` con `enabled: false` e `authMode: invite-only`; tale funzionalità rimane disattivata in questa fase.

**Attenzione:** la disponibilità del piano Supabase Free non costituisce un permesso di inviare dati degli studenti. Il primo collaudo è limitato ai quattro scenari didattici fittizi già memorizzati lato Worker.

## Flusso proposto (NON collegato a una pagina pubblica)

1. Un tester verificato accede a Supabase Auth attraverso un login a invito, attivato soltanto in un successivo gate.
2. Il browser presenta il *solo token di sessione* nel campo Authorization a un futuro endpoint protetto del Worker.
3. Il Worker controlla il token chiamando **esclusivamente** l'endpoint Auth del progetto MANZO AI, `GET /auth/v1/user`, usando una publishable key server-side. Supabase controlla il token, non il nostro client. Il Worker non si fida di JWT decodificati senza verifica, intestazioni `x-user-id`, email nel browser, app_metadata o user_metadata modificabili dal client.
4. Il Worker accetta soltanto un utente `authenticated`, con email verificata, non anonimo e presente in una **allowlist server-side** di UUID (massimo 5 tester).
5. L'UUID verificato viene trasformato in una chiave HMAC, separata dalle identità Cloudflare Access. Nessun token o email viene salvato nel Durable Object.
6. Il Worker prenota la quota globale prima dell'inferenza e invia a Gemma 4 esclusivamente uno dei quattro casi sintetici. Il docente riceve soltanto una proposta **non approvata**.

Il controllo remoto `/auth/v1/user` è stato scelto perché Supabase supporta JWT di sessione sia firmati con chiavi asimmetriche sia con la vecchia chiave HS256. La verifica JWT locale via JWKS è possibile **solo se la chiave di firma del progetto è asimmetrica**; non abbiamo modificato il metodo di firma del progetto reale. Non usare una JWT secret HS256 nel browser o nel codice pubblico.

## Patch sul branch di audit

- `product/mission-copilot/supabase-auth.mjs`: verifica server-to-server contro un host predefinito, identity allowlist e HMAC.
- `product/mission-copilot/worker.mjs`: selezione server-only del provider con `AUTH_PROVIDER`. Default `access` e Supabase non utilizzabile senza `SUPABASE_AUTH_CONFIRMED=true`.
- `product/mission-copilot/wrangler.toml`: `AUTH_PROVIDER="access"`, `SUPABASE_AUTH_CONFIRMED="false"`; tutte le precedenti approvazioni di spesa/privacy rimangono false.
- `product/mission-copilot/supabase-auth.test.mjs`: simulazioni di autenticazione riuscita/non riuscita, utenti non autorizzati, token inesistenti, risposta provider anomala, e intestazioni falsificate.
- `product/mission-copilot/worker.test.mjs` e preflight: test che l'accesso alternativo resti chiuso, senza contattare provider reali.
- Workflow GitHub Actions soltanto per sintassi, mock e controllo che il Worker rimanga non raggiungibile.

**Nessuna chiave service-role, JWT secret, UUID dei tester reali, sessione, log con token, route o credenziale Cloudflare è stata aggiunta al repository.**

## Punti bloccanti PRIMA del collegamento reale

1. **Autenticazione Supabase ancora inattiva.** Verificare login a invito, conferma email, policy sui redirect e persistenza del token nel browser. Non abilitare iscrizioni libere né utenti anonimi.
2. **Nessun endpoint esposto.** `workers_dev=false`, niente route; il collegamento con GitHub Pages non è possibile ora. Una futura route pubblica, anche se autenticata, comporta un rischio di abuso e richiede una decisione separata.
3. **Pre-auth rate limiting:** validare un controllo degli abusi che limiti chiamate non autorizzate a `/auth/v1/user` prima di esporre il Worker. L'allowlist e la quota post-autenticazione non mitigano un attaccante che sovraccarica Supabase con token arbitrari.
4. **CORS limitato e token nel frontend:** decidere l'unica origine GitHub Pages ammessa; CORS non sostituisce l'autenticazione, e non deve essere wildcard. Evitare token in URL, log, file statici, analytics e errori client.
5. **Gestione revoche:** i JWT di sessione possono restare validi fino alla scadenza anche dopo il logout; valutare durata dei token, scadenze, disabilitazione degli accessi e controllo delle sessioni prima di dati non sintetici.
6. **Privacy e rapporti contrattuali:** verificare informativa, base giuridica, DPA, trasferimenti e localizzazione, logging dei provider e periodo di conservazione. L'utilizzo rimane circoscritto ai quattro casi fittizi.
7. **Controllo zero euro:** confermare contemporaneamente Workers Free e Supabase Free, nessun account Paid/upgrade, quote Neurons reali e limiti su Durable Objects. Non aprire Zero Trust Free se viene chiesto un metodo di pagamento.
8. **Valutazione didattica:** solo dopo i gate, eseguire una inferenza sintetica in una sessione privata autorizzata, misurare Neurons e validare scientificamente la risposta.

## Limiti delle verifiche

I test Auth sono **mock**, non sessioni Supabase reali. L'endpoint `/auth/v1/user` non è stato contattato dal Worker. La CI conferma il comportamento del codice offline, ma non autorizza un rilascio e non dimostra compatibilità end-to-end del browser. Codex non è stato impiegato.

## Fonti

- https://supabase.com/docs/guides/auth/jwts
- https://supabase.com/docs/reference/javascript/auth-getuser
- https://supabase.com/docs/guides/auth/signing-keys
- https://supabase.com/docs/guides/platform/billing-on-supabase
- https://developers.cloudflare.com/workers-ai/platform/pricing/
- https://developers.cloudflare.com/durable-objects/platform/pricing/
- https://developers.cloudflare.com/cloudflare-one/setup/

**Verdetto P5.7:** percorso alternativo tecnicamente predisposto e verificabile offline, ma con gate separati ancora da soddisfare; non abilitare o distribuire.
