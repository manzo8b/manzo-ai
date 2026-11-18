# MANZO AI · Mission Copilot P2 — Sicurezza e quote globali

**Data:** 18 novembre 2026  
**Budget autorizzato:** **0 € assoluti**  
**Stato:** implementazione *source-only* — non attivata e non collegata alla micro-app pubblica

## Obiettivo

Predisporre le condizioni minime per eseguire in futuro un modello IA in un backend privato: **identità autenticata da Cloudflare Access**, contatore globale atomico, tetto per utente e interruzione automatica delle chiamate se manca qualsiasi requisito.

La demo `?copilot=preview` di Mission Studio rimane una **simulazione locale non generativa**. Il nuovo codice non aggiunge alcuna credenziale, backend pubblico, cookie o richiesta IA al sito GitHub Pages.

## Architettura

```text
Cloudflare Access, configurato dal titolare in un futuro progetto Free
   ↓  Identity autenticata dal runtime (ctx.access)
Worker /api/plan (COPILOT_ENABLED=false per impostazione predefinita)
   ↓  Se e solo se Access, audience, binding e conferme piano Free valide
HMAC-SHA256 dell'indirizzo autenticato (con sale segreto server-side)
   ↓
Durable Object SQLite singolo: CopilotQuota
   ↓  Prenotazione atomica non rimborsabile del budget giornaliero
Workers AI (solo dopo abilitazione separata; NON ATTIVO ORA)
   ↓
Risultato JSON non approvato (teacherApproval=false)
```

### Cosa protegge realmente

- **Cloudflare Access:** l'identità è accettata dal runtime con `ctx.access`, e il codice confronta `ctx.access.aud` con `ACCESS_AUD`. Un token o un indirizzo email aggiunti arbitrariamente in una richiesta HTTP **non** sono sufficienti. Il servizio è disattivato se Access non è configurato.
- **Pseudonimizzazione:** non salva email in chiaro nel contatore; usa un HMAC-SHA256 basato su un segreto server `QUOTA_HASH_SALT` (almeno 32 caratteri), che **non deve finire su GitHub o nel browser**. I dati trasmessi nella richiesta didattica non sono conservati da questo prototipo.
- **Limiti atomici:** il Worker prenota capacità in un unico Durable Object con backend SQLite, individuato sempre dallo stesso nome. Il limite non dipende dalla regione geografica che riceve la richiesta.
- **Limiti P2 conservativi:** 20 generazioni globali per giorno UTC; 3 richieste per identità autenticata ogni giorno UTC; almeno 60 secondi tra richieste della stessa identità. Il contatore si reimposta cambiando giorno UTC.
- **Fallimenti conservativi:** se Access, segreti, quota, piano Free o modello non sono configurati il Worker restituisce un errore e **non** chiama l'IA. Le prenotazioni non si annullano nemmeno quando il modello restituisce errori: evita di aggirare il tetto facendo retry.
- **Budget:** `COPILOT_ENABLED="false"`, `FREE_PLAN_CONFIRMED="false"` e `MODEL_FREE_CONFIRMED="false"` sono i valori predefiniti. Non ci sono route pubbliche, `workers_dev=false`, nessun deployment Worker e nessun account/billing da attivare.
- **Esposizione:** nessun header CORS per la pagina GitHub Pages. Gli eventuali futuri collegamenti frontend richiederanno una specifica aggiuntiva con autenticazione web, consenso e protezione antiabuso. **Non mettere credenziali nel frontend.**

## Esempio del comportamento previsto

Il primo utente autenticato e validato può chiedere fino a 3 bozze al giorno, rispettando un intervallo di 60 secondi. Il 21° tentativo complessivo della giornata viene rifiutato indipendentemente dall'utente. Se la connessione al contatore non è disponibile, il Worker blocca tutte le generazioni anziché proseguire senza limiti.

Sono limiti **di numero richieste**, non un calcolo preciso di Neurons, token, costi o sicurezza dei dati. Su Workers Free, il servizio AI ha un limite proprio di 10.000 Neurons al giorno; superarlo deve comportare errore, senza passare a Workers Paid.

## Cosa è disponibile gratuitamente secondo Cloudflare

- [SQLite-backed Durable Objects nel piano Workers Free](https://developers.cloudflare.com/durable-objects/platform/limits/)
- [Prezzi e quote Durable Objects](https://developers.cloudflare.com/durable-objects/platform/pricing/)
- [Cloudflare Access per Workers — ctx.access](https://developers.cloudflare.com/workers/configuration/cloudflare-access/)
- [Cloudflare Zero Trust Free — istruzioni di configurazione](https://developers.cloudflare.com/cloudflare-one/setup/)
- [Workers AI Free 10.000 Neurons al giorno](https://developers.cloudflare.com/workers-ai/platform/pricing/)
- [Gemma 4 26B — ancora disponibile sul piano Free nel changelog del 28 luglio 2026](https://developers.cloudflare.com/changelog/post/2026-07-28-models-require-workers-paid/)

Queste condizioni possono cambiare. **Non** è stato creato o collegato alcun account Cloudflare; il budget zero si verifica su un piano effettivamente Free **prima** di ogni esecuzione reale.

## Implementazione nel repository

- `product/mission-copilot/worker.mjs`: P2 Access, HMAC identità, controllo quota, generazione opzionale solo dopo i gate
- `product/mission-copilot/wrangler.toml`: binding `GLOBAL_QUOTA` verso `CopilotQuota`, migrazione SQLite `new_sqlite_classes`, tutte le flag OFF
- `product/mission-copilot/worker.test.mjs`: casi senza rete di Access falsificato, mancanza di segreti, concorrenza, tetti giornalieri, errori del modello, mancata approvazione
- `.github/workflows/deploy-pages.yml`: test obbligatori prima di pubblicare la **normale** pagina statica GitHub Pages, senza pubblicare il Worker

## Gate per il prossimo livello (non autorizzato automaticamente)

1. Conferma del titolare: Cloudflare Free e Zero Trust Free disponibili nell'account e nessuna carta/abbonamento necessario
2. Configurazione manuale Cloudflare Access con policy a invito e pubblico ristretto, `ACCESS_AUD` corretto, sale HMAC gestito come segreto
3. Verifica del modello e delle quote gratuite **nel giorno dell'attivazione**; eventuale provider alternativo solo se anch'esso gratuito e verificabile
4. Collaudo con richieste sintetiche, misura del consumo reale Neurons, monitoraggio errori e audit privacy/UX
5. Solo in seguito un'architettura login frontend idonea: non usare `PREVIEW_ACCESS_TOKEN`, cookie di terze parti non affidabili o CORS pubblico con credenziali

## Esclusioni fondamentali

Questo lavoro **non equivale** ad avere autenticazione attiva, un account Cloudflare operativo, un Worker distribuito, un modello reale connesso o un servizio pubblico pronto. Non copre ogni possibile dato personale né dimostra efficacia didattica. Se il provider richiede una spesa, la funzionalità resta disattivata: **nessuna eccezione al tetto 0 €**.
