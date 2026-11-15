# MANZO AI · Professional Learning — Allucinazioni e verificabilità degli output

**Release editoriale:** 15 novembre 2026 · **Ambito:** formazione professionale, IT/EN/ES
**Percorso:** 5 moduli, 10 casi professionali con riscontro ragionato, 10 quesiti interattivi per lingua, cruciverba da 70 caselle, 8 riferimenti istituzionali e accademici.

## Percorsi

- IT: `/manzo-ai/it/impara/allucinazioni-ai-verificabilita/`
- EN: `/manzo-ai/en/learn/ai-hallucinations-verification/`
- ES: `/manzo-ai/es/aprende/alucinaciones-ia-verificacion/`

## Scelte editoriali

1. **Fatti e ipotesi:** assenza di prova non significa automaticamente falsità; distinguere claim verificato, non verificato e smentito.
2. **Errori diversi:** allucinazione, calcolo errato, informazione non aggiornata e inferenza non supportata sono categorie distinguibili.
3. **Rischio professionale:** esercizi fittizi ma realistici in accounting, mercato, M&A, AML/CFT, legal e audit.
4. **Fonti:** prima parte scientifica (OpenAI 2025, NIST 2024, Anthropic, Gemini Grounding, Farquhar/Nature 2024); seconda parte normativa e regolatoria (AI Act, ESMA, FATF).
5. **Caveat:** le indicazioni ESMA riguardano le imprese che forniscono servizi di investimento; l'art. 14 dell'AI Act si applica ai sistemi di AI ad alto rischio. Le raccomandazioni FATF richiedono attuazione nei rispettivi ordinamenti. Non attribuire ai casi didattici valore di parere professionale.
6. **Metodo MANZO VERIFY:** proposta formativa originale, **non** metodo scientificamente validato, certificazione esterna o norma.

## Architettura

Il workflow Github Pages estrae `site-v0.7.zip`, quindi esegue `theme/publish-hallucinations.py` prima della rigenerazione SEO e del sistema di navigazione.

I materiali modificabili sono conservati in `editorial/learning/hallucinations/`: `it.json`, `en.json`, `es.json`, `course.css`, `course.js`. La fonte `site-v0.7.zip` resta immutata.

## QA

- Convalida strutturale: 3 localizzazioni, 5 moduli/lingua, 10 esercizi/lingua, 10 quiz/lingua, 70 caselle lettera del cruciverba, 8 fonti.
- `python3 -m py_compile theme/publish-hallucinations.py`
- `node --check editorial/learning/hallucinations/course.js`
- `python3 theme/publish-hallucinations.py --site _site --verify-only`
- `python3 theme/hallucinations-browser-smoke.py`: test desktop e mobile, esercizio, quiz e griglia completata.
- QA `MANZO AI Chromatic QA`, PR #9, run 43735666572: **PASS** (15 novembre 2026).

Il workflow di deployment e la raggiungibilità pubblica devono essere controllati dopo il merge: **un build riuscito non prova che una pagina sia indicizzata nei motori di ricerca**.

## Dati e utilizzo

Il corso non usa CDN, font remoti, pubblicità, analytics, cookie, login o chiamate API proprie. Risposte e punteggi sono conservati soltanto nella memoria della pagina durante la sessione e non vengono inviati a un server. Il punteggio è formativo, non costituisce una certificazione.

## Revisioni successive consigliate

- Osservazione su dispositivi fisici con revisione editoriale da parte del curatore.
- Sessione pilota con specialisti AML e giuristi prima di presentare il materiale come formazione aziendale accreditata.
- Aggiornamento periodico dei riferimenti normativi; controllo delle versioni consolidate dell'AI Act e degli standard FATF.
