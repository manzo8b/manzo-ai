# MANZO AI Learning B2B — Rilascio pilota riservato

**Data:** 16 novembre 2026  
**Base dati:** Supabase MANZO AI, `bjydnaejpxwubmxpnpnv`, Irlanda `eu-west-1`  
**Ambito:** esclusivamente test interni su invito. **Non servizio commerciale**

## Impostazioni confermate dal titolare
Lo screenshot aggiornato della pagina **Sign In / Providers** mostra:
- `Allow new users to sign up`: OFF
- `Allow manual linking`: OFF
- `Allow anonymous sign-ins`: OFF
- `Confirm email`: ON
- `Email`: ENABLED

Il titolare ha precedentemente configurato `Site URL` e tre `Redirect URLs` precisi per italiano, inglese e spagnolo.

**Limite di verifica:** i permessi del connettore Supabase non forniscono la lettura diretta delle impostazioni GoTrue. La fonte è lo screenshot della pagina dopo aggiornamento; non rivendicare una verifica programmatica del valore.

## URL pilota

| Lingua | Accesso su invito | Informativa account |
|---|---|---|
| Italiano | https://manzo8b.github.io/manzo-ai/it/prodotto/learning-b2b/accesso/ | https://manzo8b.github.io/manzo-ai/it/prodotto/learning-b2b/privacy/ |
| English | https://manzo8b.github.io/manzo-ai/en/product/learning-b2b/sign-in/ | https://manzo8b.github.io/manzo-ai/en/product/learning-b2b/privacy/ |
| Español | https://manzo8b.github.io/manzo-ai/es/producto/learning-b2b/acceso/ | https://manzo8b.github.io/manzo-ai/es/producto/learning-b2b/privacidad/ |

I sei URL sono `noindex,nofollow,noarchive`, deliberatamente non collegati al sito pubblico e non inclusi nella sitemap generata prima della loro creazione. Non confondere la disponibilità URL con l'approvazione per l'uso commerciale.

## Misure di rilascio

- Il file sorgente `product/auth-staging/config.json` resta **enabled:false**
- `theme/publish-auth-staging.py` abilita il codice browser soltanto con `--enable --live-auth` e variabile `MANZO_AUTH_PILOT_RELEASE=restricted-invite-only`
- Lo script è eseguito **dopo** la generazione SEO, il restyling, i controlli visivi e il guardiano dei titoli; non cambia la Home o i corsi pubblici
- Build JS Supabase pinning + test validazione, divieto signup dal browser, no server keys nel markup
- Le sessioni di prova utilizzano **sessionStorage**, non localStorage persistente; l'accesso è comunque sotto lo stesso origin GitHub Pages di altri progetti. **Non introdurre utenti esterni senza isolare l'origine** (dominio dedicato, preferibilmente cookie HttpOnly e sessioni server)
- Non viene distribuita l'API Edge Functions: l'identità verificata non dà ancora diritto a corsi, progressi o licenze aziendali
- Nessun webhook di pagamento, Stripe o agente AI
- Informative account distinte da quelle del portale pubblico e con contatto già presente nel repository `theme/inject-signature.py`
- Condizioni di trattamento dati, tempi di retention definitivi, DPA/sub-responsabili e privacy per clienti esterni **da validare prima di un pilota commerciale**

## Prima prova reale da eseguire manualmente

1. Confermare dal dashboard che `Sign In / Providers` mantiene `Allow new users to sign up` disattivato
2. Verificare che l'indirizzo email di prova sia autorizzato a ricevere email dal servizio SMTP gratuito Supabase (normalmente solo i membri dell'organizzazione)
3. Aprire `Authentication → Users` sul progetto MANZO AI, usare `Invite user` con **un solo indirizzo di prova autorizzato**, senza inoltrare password o link di conferma in chat
4. Aprire l'email sul dispositivo interessato e controllare che il link finisca sull'URL italiano di accesso e che la sessione venga riconosciuta
5. Impostare una password unica di almeno 12 caratteri, disconnettersi e riprovare l'accesso
6. Verificare che l'account autenticato riporti chiaramente **nessuna licenza aziendale assegnata**
7. Testare recupero password una volta, entro i limiti email consentiti
8. Verificare `auth.users` attraverso il connettore solo per conteggi e stato di conferma (senza esporre indirizzi degli utenti)
9. Pianificare un secondo utente/test su altra organizzazione per l'isolamento tenant prima di collegare dati didattici

**Non creare account mediante SQL in `auth.users`**, né disabilitare confirm email per facilitare i test.

## Fonte e costi
- https://supabase.com/docs/guides/auth/passwords
- https://supabase.com/docs/guides/auth/auth-smtp
- https://supabase.com/docs/guides/auth/redirect-urls
- https://supabase.com/docs/guides/auth/auth-email-templates

Supabase Free, nessun addebito aggiuntivo autorizzato. Per inviti a partecipanti esterni servirà un SMTP approvato e una revisione dei costi.
