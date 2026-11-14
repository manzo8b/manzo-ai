# Fibonacci e prompt: lettura critica del documento v2

**Fonte primaria dell'utente:** `../sources/user/Fibonacci_Prompt_Engineering_v2.md` (non modificata).

## Cosa viene preservato
La sequenza matematica, il collegamento storico con proporzioni e architettura, e i sei strati di progettazione (intento; ruolo; contesto; vincoli e formato; esempi; verifica) sono una cornice pedagogica comprensibile. La revisione v2 ha opportunamente corretto esempi abusati relativi a Partenone e nautilus e qualifica la sezione aurea come *ipotesi*, non come fatto dell'ingegneria dei prompt.

## Ciò che non va trasferito senza una prova
1. **Sei livelli non sono una ricorrenza di Fibonacci.** Sono categorie semantiche; assegnare loro numeri della serie non fa nascere una dipendenza matematica.
2. **Un prompt multistrato non è necessariamente migliore.** La qualità varia con compito, modello, ordine, lunghezza e informazioni veramente pertinenti.
3. **Rapporto 61,8/38,2**: manca una ragione di ottimalità derivata da una funzione obiettivo, da un modello del transformer o da dati. Il solo accostamento a Φ non è una prova.
4. **Posizione e ordine:** il suggerimento di porre prima soggetto/stile e poi parametri non è un principio universale dei modelli multimodali; va verificato sul modello usato. Anche nei modelli linguistici la posizione dei contenuti può influire.
5. **Compito dinamico e impalcatura statica** devono essere definiti con rigore, anche a livello di token: istruzioni, esempi e contesto talvolta hanno doppia funzione; dichiarare criteri di classificazione e casi ambigui.
6. **La 'verifica' non può essere una richiesta retorica di auto-correzione.** Va tradotta in test esterni quando possibile.

## Operazionalizzazione proposta
- Lo strato `intento` definisce criterio di completamento e output atteso, non un generico ruolo teatrale.
- `contesto` include informazioni di dominio con provenienza; `vincoli` include quelli controllabili con test.
- `esempi` sono un trattamento sperimentale controllato; variarne il numero non deve contaminare l'effetto del rapporto studiato.
- `verifica` è preferibilmente una suite esterna; negli esperimenti non aggiungere istruzioni che rivelino la risposta del benchmark.
- `impalcatura` = sezioni di prompt che descrivono struttura operativa, vincoli, esempi e informazioni comuni; `dinamica` = richiesta specifica, input e dati individuali. Nei protocolli si registrano le sottosezioni e i conteggi reali del tokenizer.

## Conseguenze per la ricerca
- A valuta la memoria controllata senza ricorrere al numero aureo.
- B valuta solo **quando** chiamare un audit più profondo.
- C valuta **quanto** testo assegnare a diverse componenti, controllando per contenuto, lunghezza e ordine.
- Un esito favorevole a C non dimostra Fibonacci come teoria cognitiva degli LLM. Per rivendicare una proprietà speciale del 61,8% servono controlli ravvicinati (es. 60% e 65%) e replica su almeno un'altra famiglia di compiti/modello.

## Riferimenti
- Mao, Middleton e Niranjan (2024), https://aclanthology.org/2024.findings-naacl.258/
- Liu et al. (2024), https://aclanthology.org/2024.tacl-1.9/
- Sánchez-Torrón et al. (2026), https://aclanthology.org/2026.eamt-1.8/
- Il documento v2 ricevuto è fonte progettuale, non risultato sperimentale peer reviewed.
