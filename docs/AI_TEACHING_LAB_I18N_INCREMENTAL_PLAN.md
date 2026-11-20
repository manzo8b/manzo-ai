# MANZO AI · Completamento multilingue — piano incrementale

**Stato verificato il 20 novembre 2026:** l'ultima pipeline di deploy riuscita registra **8/9 corsi** con sorgenti editoriali completi IT/EN/ES. Non ripetere le traduzioni già pubblicate di *Modelli mentali e affidabilità* e *AI Product Builder — Centroni City*.

## Unico blocco ancora da localizzare: AI Teaching Lab

Percorso sorgente: `editorial/learning/ai-teaching-lab/`.

L'italiano rimane il riferimento strutturale. In `en/` e `es/` devono esistere questi file, realmente tradotti e con struttura compatibile con `it/`:

| Consegna | File per lingua | Criterio di completamento |
| --- | --- | --- |
| A · Modulo 01 | `module-01.md` | Testo completo, esempi, attività, note pedagogiche e riferimenti |
| B · Modulo 02 | `module-02.md` | Testo completo, esempi, attività, note pedagogiche e riferimenti |
| C · Modulo 03 | `module-03.md` | Multimedialità, prompt, modelli e controlli accessibilità |
| D · Moduli 04–05 | `module-04.md`, `module-05.md` | Inclusione, valutazione, tutor e controllo umano |
| E · Dati del corso | `course.json`, `narrative.json` | Tutte le sezioni e le narrazioni tradotte senza alterare ID, chiavi e logica |
| F · Verifiche e glossario | `assessment-bank.json`, `glossary.json` | Quiz, feedback, cruciverba, esempi e 79 voci glossario tradotti |

**Regola fondamentale:** creare una scheda o una Home in EN/ES non significa che il corso sia tradotto. Non pubblicare un corso che usa in silenzio contenuti italiani come fallback.

## Sequenza di sviluppo e test

1. Tradurre e registrare *una consegna alla volta*. Effettuare il controllo completo dei sorgenti prima di procedere alla successiva.
2. Conservare gli identificatori di attività, moduli, strutture JSON, source URL e corrette risposte; tradurre testo visibile, istruzioni, feedback, esempi e alternative.
3. Mantenere gli stessi vincoli di sicurezza: nessun dato reale di studenti, nessun certificato non previsto, supervisione dei docenti e nessuna attribuzione di risultati falsi.
4. Pubblicare percorsi EN/ES soltanto quando i file sono completi e un generatore realmente li utilizza: non basta il risultato `8/9` del controllo sui sorgenti.
5. Verificare le tre lingue, navigation e hreflang, leggibilità desktop/iPhone, quiz, glosssario e strumenti multimediali.
6. Concludere con un **audit di copertura totale**. Il successivo audit AI Web Production rimane una fase separata.

## Parti già verificate — da non rifare

- *Modelli mentali e affidabilità* — sorgenti IT/EN/ES e pagine localizzate già pubblicate.
- *AI Product Builder — Centroni City* — sorgenti IT/EN/ES e pagine localizzate già pubblicate.
- Altri sei corsi censiti — sorgenti IT/EN/ES già presenti secondo il controllo automatico.
- Card uniformi preesistenti — preservare la geometria.
- AI Teaching Lab italiano — preservare cinque moduli, laboratori, rubriche, vocabolario e strumenti già realizzati.

## Verifica dello stato effettivo

L'ultima pipeline ha confermato: `[NEEDS TRANSLATION] ai-teaching-lab: IT=source, EN=MISSING, ES=MISSING`. Fonte: [GitHub Actions](https://github.com/manzo8b/manzo-ai/actions/runs/44725699053).

**Non contrassegnare alcuna consegna come completata prima dell'esistenza e della verifica dei relativi file.**
