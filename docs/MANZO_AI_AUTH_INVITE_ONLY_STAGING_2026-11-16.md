# MANZO AI · Fase 3 — Accesso Learning B2B via email verificata

**Data:** 16 novembre 2026  
**Supabase:** progetto MANZO AI, ref bjydnaejpxwubmxpnpnv, Irlanda eu-west-1  
**Modalità:** invito dell'amministratore, email + password, conferma dell'indirizzo  
**Stato:** sorgente testabile in GitHub, **non pubblicata, non collegata alla Home**  
**Costo aggiuntivo autorizzato:** zero. Nessun nuovo progetto o ramificazione a pagamento.

## Decisione prodotto

L'area B2B non è un social network, un e-commerce né un portale con registrazione indiscriminata.
La prima versione accetta **solo utenti invitati**. L'accesso con un'identità verificata è
necessario ma **non sufficiente** per frequentare corsi di un'azienda: il diritto deve essere
riconosciuto dal backend PostgreSQL (organizzazione, membership, posto attivo, licenza,
iscrizione), non dichiarato dal browser.

### Funzionalità già scritte (non attive online)

- UI responsiva IT, EN, ES coerente con la Home MANZO AI approvata
- Login email/password tramite SDK ufficiale Supabase, senza endpoint inventati
- Sessione verificata con chiamata \`auth.getUser()\`, non fiducia in un oggetto scritto dall'utente
- Recupero password e form per impostare una nuova password (minimo 12 caratteri)
- Logout e messaggio esplicito in assenza di autorizzazione aziendale
- Nessuna registrazione pubblica tramite \`signUp()\`
- Callback esatte per ciascuna lingua, rifiuto degli URL di redirect arbitrari
- Nessuna autenticazione fittizia né corsi premium sbloccati
- Nessun collegamento alle funzioni di pagamento
- Stato \`enabled:false\` nel file \`product/auth-staging/config.json\`
- Pagine \`noindex,nofollow,noarchive\`, generabili **solo** nel workflow QA con flag
  esplicito \`--enable\`, mai dal publisher GitHub Pages corrente
- Asset JavaScript compilato localmente da \`@supabase/supabase-js\`, senza dipendenza
  da CDN di terzi durante la visita

### I quattro controlli indispensabili nel dashboard Supabase

**1. Provider di autenticazione**

Aprire:
https://supabase.com/dashboard/project/bjydnaejpxwubmxpnpnv/auth/providers

Confermare:
- provider **Email** abilitato
- **Confirm email** abilitato
- registrazione pubblica disabilitata, se l'impostazione è disponibile nella versione
  corrente del pannello; gli inviti amministrativi rimangono il percorso desiderato
- non abilitare OTP, account social, accesso anonimo o telefono per questo MVP

La documentazione Supabase dice che nei progetti hosted Email Auth e la conferma
sono normalmente abilitate per impostazione predefinita. Tuttavia **non è possibile
inferire da quel default lo stato concreto delle impostazioni di questo progetto**.

Fonte: https://supabase.com/docs/guides/auth/passwords

**2. URL Configuration**

Aprire:
https://supabase.com/dashboard/project/bjydnaejpxwubmxpnpnv/auth/url-configuration

Utilizzare i seguenti URL esatti (no wildcard aperte):

\`\`\`text
Site URL:
https://manzo8b.github.io/manzo-ai/it/prodotto/learning-b2b/accesso/

Additional Redirect URLs:
https://manzo8b.github.io/manzo-ai/it/prodotto/learning-b2b/accesso/
https://manzo8b.github.io/manzo-ai/en/product/learning-b2b/sign-in/
https://manzo8b.github.io/manzo-ai/es/producto/learning-b2b/acceso/
\`\`\`

Questi URL sono **prenotati per la futura pubblicazione**, non pagine login
funzionanti nel sito attuale. Non usare la Home né localhost come callback
predefinito, salvo esigenze esplicite in uno sviluppo locale isolato.

Verificare anche i template email per invito e recupero: devono usare le callback
configurate e la provenienza MANZO AI, non redirect verso un altro progetto.

Fonte: https://supabase.com/docs/guides/auth/redirect-urls

**3. Limite del server email gratuito**

La documentazione ufficiale Supabase conferma che l'SMTP predefinito è di prova:
**può spedire soltanto agli indirizzi dei membri autorizzati del team Supabase**,
ed è soggetto a rate limit e assenza di SLA. Per un pilota con studenti esterni
serve configurare prima un provider SMTP personalizzato e verificarne costi,
privacy, reputazione e limiti.

Non presumere che un invito a un'email arbitraria venga consegnato sul piano Free.
Non inviare inviti pubblici prima di aver predisposto e testato SMTP.

Fonte: https://supabase.com/docs/guides/auth/auth-smtp

**4. Verifica privacy e trattamento dei dati**

La vecchia Home informativa dichiarava di non raccogliere dati dei visitatori.
L'attivazione di Auth cambia il quadro: Supabase Auth conserverà email, ID utente,
stato di verifica e sessioni tecniche. **Prima della pubblicazione** serve
aggiornare privacy policy e base giuridica, informativa su fornitori/trasferimenti,
retention, diritti interessati e protezione account. Il client web di staging usa
l'archiviazione di sessione prevista dalla libreria Supabase per permettere i
redirect email e i rinnovi; in un prodotto commerciale va valutata una soluzione
server-side con cookie HttpOnly e CSP in header, riducendo i rischi XSS.

Non attivare analisi, marketing, pagamenti o tracking in questa fase.

## Prima sessione di test: criteri

1. Il proprietario conferma personalmente le impostazioni Email/Confirm Email
   e tutti e tre i redirect esatti nel dashboard
2. Si usa un indirizzo di test dell'organizzazione Supabase autorizzato a
   ricevere posta, oppure un SMTP personalizzato approvato
3. L'amministratore invia un invito tramite Supabase Auth Users (nessuna password
   condivisa nella conversazione)
4. La persona imposta la propria password e conferma la proprietà dell'indirizzo
5. Il browser vede la sessione verificata, ma **non** concede alcuna licenza
6. Solo dopo si crea una prima organizzazione applicativa e una membership
   collegata all'ID utente Auth effettivamente verificato
7. Si eseguono test reali con due organizzazioni per negare accessi cross-tenant
8. Si prepara il deploy della Edge Function con segreti e rate limit, soltanto
   dopo audit backend e privacy
9. Si attiva il publishing di login e i link nel portale, senza cambiare
   le sezioni pubbliche approvate

## Files e test

- \`product/auth-staging/src/auth-policy.mjs\` — validazione, callback fisse e
  controllo formale di email verificata / niente grant lato client
- \`product/auth-staging/src/app.js\` — sign-in, recovery, update, sign-out
- \`product/auth-staging/content.json\` — copia IT/EN/ES
- \`product/auth-staging/auth.css\` — design e accessibilità
- \`product/auth-staging/config.json\` — **chiave publishable**, non segreta;
  modulo comunque disabilitato
- \`theme/publish-auth-staging.py\` — generazione opzionale, mai pubblicata
  automaticamente
- \`theme/auth-staging-browser-smoke.py\` — Chromium, desktop/mobile, 3 lingue
- \`product/auth-staging/tests/auth-policy.test.mjs\` — regole sicurezza
- \`.github/workflows/auth-staging-qa.yml\` — compilazione, unit test,
  controllo senza rete autenticata, screenshots

La chiave \`sb_publishable_...\` è progettata per essere usata in un client browser;
**non è una credenziale segreta**. Le chiavi \`sb_secret_\` e il ruolo
\`service_role\` non sono mai inseriti nei file pubblici.

## Definizione di completamento

- Sorgente + test CI verde: **staging frontend pronto tecnicamente**
- Conferme manuali Auth/Site URLs/SMTP: **ancora necessarie**
- Login verificato con un invito reale: **non ancora eseguito**
- Isolamento tenant con due account reali: **non ancora verificato**
- Prodotto commerciale con compliance, fatturazione, backup e SLA: **non pronto**

L'utente ha approvato il metodo email/password con verifica; non ha autorizzato
la creazione arbitraria di nuovi account reali né eventuali abbonamenti/SMTP
a pagamento. Manteniamo questi vincoli.
