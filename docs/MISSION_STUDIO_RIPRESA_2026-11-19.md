# MANZO AI · Mission Studio — Ripresa operativa del 19 novembre 2026

**Destinatario:** titolare del progetto · **Stato:** pronto alla revisione, NON alla pubblicazione · **Budget:** €0, nessun metodo di pagamento

## 1. Risultati consolidati fino al 18 novembre

| Lavoro | Evidenza | Esito |
|---|---|---|
| P4 · simulazione locale Mission Studio | `tools/ai-teaching-launchpad/copilot-preview.mjs` | Pubblico solo sotto `?copilot=preview`, nessuna IA reale |
| P5.5 · compatibilità modello Gemma 4 / gestione errori | PR #47, CI GitHub | Offline completato |
| P5.6 · accesso Cloudflare Zero Trust | Dossier + screenshot checkout | **Bloccato**: Zero Trust Free richiede metodo di pagamento |
| P5.7 · Supabase Auth alternativa | PR #48 | Sviluppo offline; non collegato |
| P5.8–P5.11 · dashboard Supabase | screenshot del titolare | Account email verificato; registrazioni/anon disabilitate; rate limits configurati; CAPTCHA disabilitato |
| P5.12 · pre-auth rate limit | PR #49 | Offline completato, binding non provato sull'account |
| P5.13 · CORS, origin check e client browser dormiente | PR #50 (in bozza) | Offline completato, nessun Worker deploy |
| Prima inferenza con Worker nell'account | — | **Non eseguita** |
| Spesa per questo progetto | Operazioni eseguite | **Nessuna attivazione a pagamento / nessun deploy** |

## 2. Punti già verificati nella dashboard

- Cloudflare: account con **Workers Free** $0 e quota Workers 100.000 richieste/die. Catalogo Gemma 4 disponibile; Playground ha restituito `FUNZIONA`, ma questo non misura il consumo Neurons dell'account né la compatibilità via Worker.
- Cloudflare Zero Trust Free: checkout mostrava $0/mese e richiesta di un metodo di pagamento; per il vincolo di €0 senza rischi di addebito abbiamo interrotto il percorso.
- Supabase: organizzazione MANZO AI su **Free**, progetto già esistente nella regione UE; Auth email abilitato, iscrizioni libere e anonime disabilitate, un primo tester già confermato (non copiare il suo UUID in repository o documenti).
- Supabase Auth: access token TTL **3600 secondi**, refresh token reuse interval **10 secondi** e revoca token riutilizzati attiva. Durata massima e timeout sessioni personalizzati richiedono piano Pro: non attivarli.
- Supabase Auth: rate limits esistenti per login, OTP e refresh; CAPTCHA e leaked-password protection non attivati. Quest'ultima funzione è nel piano Pro. La mancanza di CAPTCHA non è un'autorizzazione ad esporre endpoint senza una protezione applicativa.
- Redirect Supabase: tre URL esatti dell'area Learning B2B in italiano/inglese/spagnolo. **Non modificarli** per Mission Studio e non spezzare il login dell'altro prodotto.
- GitHub: le PR sono separate e impilate. Il branch `main` e la pubblicazione GitHub Pages non vengono modificati.

## 3. Checklist di revisione assieme al titolare

**A. Aspetti economici (STOP se qualcosa non è verificato)**

- [ ] Controllare Worker e Workers AI quota reale, limiti attivi, eventuali funzioni tariffate e billing *senza* aggiornamento Paid.
- [ ] Verificare che Rate Limiting binding sia disponibile con Workers Free e che `namespace_id="51218"` non collida con altri Workers dello stesso account.
- [ ] Verificare i limiti di Durable Objects SQLite Free e osservabilità per evitare addebiti inattesi; nessun upgrade e nessuna carta.
- [ ] Non creare una route pubblica finché i gate privacy/autenticazione non sono approvati.

**B. Identità e protezione dati**

- [ ] Ricontrollare i criteri di privacy, le condizioni dei fornitori e la conservazione dei log. Il primo collaudo userà **solo casi sintetici**.
- [ ] Verificare che l'account Supabase di prova sia ancora attivo e confermato; niente nuovi utenti, inviti o registrazioni libere.
- [ ] Preparare *in dashboard Cloudflare, non nel codice* `SUPABASE_ALLOWED_TESTER_IDS` (un solo UUID) e `QUOTA_HASH_SALT` (segreto casuale robusto). Non pubblicare screenshot con valori sensibili.
- [ ] Verificare il token lato server, revoca e gestione del logout. L'Access Token da 1 ora può essere rinnovato: non equivale a una sessione di durata massima 1 ora.
- [ ] Riconoscere che `https://manzo8b.github.io` è una sola origine condivisa fra diversi repository: CORS non isola singoli percorsi né sostituisce l'allowlist.

**C. Endpoint e test (solo se i gate A/B vengono approvati separatamente)**

- [ ] Confermare l'unica route autorizzata `/api/plan` e come disattivarla immediatamente. `workers.dev` sarebbe pubblicamente indirizzabile: richiede una decisione esplicita, non è un endpoint segreto.
- [ ] Prima di qualunque invocazione del modello: verificare OPTIONS autorizzato, OPTIONS errato, origin errato, bearer mancante, bearer invalido, limite 429 e servizio in errore 503.
- [ ] Prima inferenza con `scenarioId=water_cycle` e nient'altro, quota atomica verificata. Il risultato deve mantenere `teacherApproval=false`.
- [ ] Misurare i Neurons effettivi, controllare lo storico dell'account e valutare pedagogicamente l'output.
- [ ] Solo dopo, pianificare un'eventuale UI login/bozza su Mission Studio: il client sorgente oggi resta disattivato, senza endpoint, e non è importato nella pagina.

## 4. Cosa NON fare

- Nessuna modifica alla pagina live, alla SEO, alla sitemap, alle altre risorse dell'account o al login Learning B2B.
- Nessun `wrangler deploy`, nessun endpoint aperto, nessuna API token in GitHub.
- Nessun inserimento di carta, Cloudflare Zero Trust checkout o upgrade Supabase.
- Non impostare autonomamente `COPILOT_ENABLED=true`, `SUPABASE_AUTH_CONFIRMED=true` o `BROWSER_CONNECTION_CONFIRMED=true`.
- Non utilizzare studenti o dati personali nei prompt.
- Non effettuare merge delle PR #47, #48, #49 o #50 fino alla verifica di tutti i gate.

## 5. Lavori autonomi eseguiti / da fare con proprietario

**Completati senza Codex:** codice e test backend, filtro prima dell'autenticazione, origine e preflight stretti, client sessione non pubblicato, QA su risposte AI e validazione JSON, documentazione, CI offline.

**Richiedono intervento del titolare:** scelta esplicita dell'endpoint e dei rischi collegati; approvazione delle condizioni commerciali e privacy; configurazione dei segreti e dell'allowlist nell'account; eventuale primo deploy; prima inferenza privata e verifica dei consumi.

## 6. Riferimenti

- P5.5–P5.6: https://github.com/manzo8b/manzo-ai/pull/47
- P5.7: https://github.com/manzo8b/manzo-ai/pull/48
- P5.12: https://github.com/manzo8b/manzo-ai/pull/49
- P5.13: https://github.com/manzo8b/manzo-ai/pull/50
- Documenti di fase: `docs/MANZO_AI_COPILOT_P5_*.md`

**Decisione corrente: GO per ulteriori test offline; NO-GO per deploy, configurazione account e IA reale.**
