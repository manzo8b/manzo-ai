# MANZO AI — Audit del sito distribuito su GitHub Pages

**Data:** 16 novembre 2026  
**Provenienza verificabile:** GitHub Actions `Deploy MANZO AI`, run [43852683965](https://github.com/manzo8b/manzo-ai/actions/runs/43852683965), SHA `76656f6aba305204128bdea776c8debc95c0a1f6`, artefatto `github-pages` id `14219400739`.  
**Operazione:** download dell'artefatto, estrazione del `artifact.tar`, lettura e hashing **senza modificare il sito o Supabase**.  
**Scope:** build completa pubblicata alla data del deploy; non è il solo `site-v0.7.zip`.

## Inventario misurato

| Indicatore | Valore |
|---|---:|
| File estratti | **173** |
| HTML totali | **111** |
| Pagine `index.html` | **109** |
| File diversi da HTML (asset/media/documenti/tecnici) | **62** |
| HTML con `lang=it` | **38** |
| HTML con `lang=en` | **37** |
| HTML con `lang=es` | **35** |
| HTML senza `lang` | **1** |
| HTML con direttiva `noindex` | **15** |
| HTML privi di `noindex` | **96** |
| Pagine Auth/privacy protette da `noindex` | **6 su 6** |
| Pagine con link locale mancante rilevato | **1** |
| Pagine con `h1`–`h6` terminante con punto | **0** |
| Dimensione totale estratta | **36.618.263 byte** |

**Distinzione critica:** le 82 pagine annotate nel workflow sono la sola base del pacchetto v0.7; la pubblicazione finale comprende **109 `index.html`**, oltre a `404.html` e alla verifica Google.

## Difetto concreto individuato

Nella pagina:

`it/video-e-slide/prompt-engineering/index.html`

il pulsante **Approfondisci Prompt Mastery** collega a:

`/manzo-ai/it/prompt-mastery/`

ma nell'artefatto distribuito **non esiste** `it/prompt-mastery/index.html`.

Rotte attualmente presenti sotto lo stesso prefisso:

- `/manzo-ai/it/prompt-mastery/che-cos-e-un-prompt/`
- `/manzo-ai/it/prompt-mastery/laboratorio-tecnico/`

**Azione proposta:** aggiornare `theme/publish-prompt-video.py` al percorso didatticamente più adatto, creare/controllare la pagina rigenerata e ripetere il controllo link. Nessuna modifica al sito live è stata effettuata in questo audit.

## Controlli SEO e privacy

- Le **sei** pagine private (accesso e privacy IT/EN/ES) sono correttamente `noindex`.
- Le pagine senza canonical sono soltanto `404.html`, la verifica Google e le sei pagine private: **non è automaticamente un errore per queste pagine**.
- Nessun titolo `h1`–`h6` con punto finale è stato trovato nel build controllato.
- Il controllo link riguarda gli attributi HTML `href`/`src` verso la medesima piattaforma: non è ancora un crawler di tutte le destinazioni esterne o dei riferimenti CSS/JS dinamici.
- Le **96** pagine prive di `noindex` sono soltanto **candidate all'indicizzazione**. Non è una prova che Google le abbia indicizzate.

## Esito e gate

- **M0:** inventario dei 154 file sorgente GitHub → **PASS** (snapshot separato).
- **M1:** inventario del sito compilato → **MISURATO**, ma rilascio **NON PASS** per 1 link locale mancante.
- **M2–M7:** non avviati; nessuna migrazione contenuti, Storage, API, hosting o dati sensibili.

**Prossima azione controllata:** correggere il riferimento, generare una build di QA e confrontare manifest precedente/nuovo prima di cambiare il sito live. Conservare l'artefatto deploy precedente come riferimento per il rollback.

## Riferimenti

- [Piano maestro](MANZO_AI_MIGRATION_MASTER_PLAN_2026-11-16.md)
- Manifest source: `product/migration/github-source-inventory-2026-11-16.json`
- Scanner post-build: `product/migration/audit_release.py`
- CI QA dedicata: `.github/workflows/migration-inventory-qa.yml`
