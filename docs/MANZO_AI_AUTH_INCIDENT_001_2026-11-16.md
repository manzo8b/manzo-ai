# MANZO AI · Incident AUTH-001 — reset password e OTP scaduto

**Data:** 16 novembre 2026  
**Ambito:** prima prova interna Learning B2B (un solo account invitato)  
**Stato:** correzione UI/sorgente; non eliminare o rigenerare l'utente

## Evidenza osservata

- Il link email porta alla pagina `/manzo-ai/it/prodotto/learning-b2b/accesso/?error=access_denied&error_code=otp_expired...`, indicando un OTP scaduto o già utilizzato. **Un OTP scaduto non prova che la sessione ancora presente nel browser sia invalida**.
- Il controllo sul database Supabase MANZO AI (solo campi booleani/aggregati, nessuna password letta) conferma: 1 utente, invito presente, email verificata, almeno un accesso effettuato e hash password presente.
- L'audit Auth segnala due risposte **HTTP 422 a richieste PUT** nel periodo dei tentativi di aggiornamento password. I log disponibili non identificano in modo affidabile la causa precisa (password invariata, requisiti di sicurezza, riautenticazione o altro). **Non inferire arbitrariamente che l'ultima password sia stata salvata**.
- Il codice esistente mostrava sempre `Operazione non riuscita` per qualsiasi `auth.updateUser()` fallito. Inoltre forzava un `signOut({scope:'local'})` dopo la modifica; un eventuale errore del logout poteva nascondere l'avvenuto aggiornamento.

## Intervento

1. `classifyPasswordError()`: classifica soltanto codici pubblici e riconosciuti di Supabase Auth; fallback HTTP 422 non diagnostico ma utilizzabile, senza esporre stringhe server o segreti
2. Traduzioni IT/EN/ES: password già utilizzata, troppo debole, sessione scaduta, necessità di riautenticazione, link OTP scaduto e rifiuto generico HTTP 422
3. `expiredInvite` separato da `confirmedUser`: l'errore del vecchio link mostra istruzioni appropriate ma **non disabilita il modulo di accesso** quando manca una sessione
4. Dopo `updateUser()` riuscito, non eseguire logout automatico; mostrare messaggio di successo e offrire logout volontario
5. Test su codici di errore e percorso di invito scaduto in tre lingue e due viewport, con connessione Auth bloccata nei browser-test
6. Nessun cambiamento a database, RLS, licenze, dati degli utenti, Home o corsi

## Istruzione al collaudatore

Aprire l'URL pulito (senza `?error...`), uscire ed effettuare nuovo login con la password precedentemente scelta. Se fallisce, chiedere recupero password (solo link recente), invece di riusare l'invito scaduto. Non inviare credenziali o URL con token nella chat.

## Gate

La PR può essere integrata dopo test Auth + QA generale verdi. Confermare poi il deploy GitHub Pages e fare una prova manuale di login; i test mockati da soli non dimostrano che una password reale sia accettata.

Fonti: https://supabase.com/docs/guides/auth/debugging/error-codes · https://supabase.com/docs/guides/auth/password-security
