# MANZO AI — professional refinement
3 novembre 2026.

## Ambito e direzione
Perfezionamento visivo autorizzato dal proprietario: conservare struttura tipo chat, navigazione, contenuti e funzioni, con tipografia e palette più professionali. Riferimento indicato: https://ads.openai.com/it-IT. Contenuto della pagina di riferimento letto; visualizzazione diretta non disponibile nel browser per errore/verifica di sicurezza. Nessuna riproduzione esatta del suo layout è dichiarata e nessun font, asset o marchio OpenAI è copiato.

Direzione: ambiente di studio conversazionale, con bianco, grigio caldo, testo quasi nero e tinte molto leggere per distinguere percorsi. Titoli ampi di peso moderato, maggiore respiro, ricerca centrale, barra laterale sobria, bordi sottili e azioni compatte. Font di sistema locali: nessuna nuova richiesta esterna o dipendenza. Feedback di pressione, hover, focus e riduzione del movimento. L’interfaccia resta una ricerca di contenuti locali, non una chat con un modello.

Metodologia: principi di Impeccable per distinguere lettura e uso operativo, critica visiva e correzione dei problemi osservati; skill Sites per processo di progettazione e verifica. Non si dichiara installato o eseguito un pacchetto Impeccable dedicato. Hosting GitHub Pages conservato.

## Implementazione
- `theme/learning-colors.css`: overlay professionale sul pacchetto v0.7 originale.
- `theme/footer-signature.css`: contatto e firma coerenti con la nuova palette.
- Archivio v0.7, HTML, JavaScript, testi, quiz, cruciverba, PDF, PowerPoint e slide rimangono invariati. Conservato il processo esistente di pubblicazione e l’integrazione Oracle City; nessuna modifica a workflow o permessi.
- Risolto overflow mobile del laboratorio tecnico con dimensionamento intrinseco delle colonne e scroll locale dei blocchi di codice.

## Verifiche eseguite
- Ricostruzione da archivio pulito seguendo il workflow esistente. `theme/check-theme.py`: PASS su 82 pagine originali; confronto byte per byte delle risorse originali escluso il foglio CSS previsto.
- `theme/inject-signature.py` e modalità verify-only: PASS su 82 pagine. Successiva integrazione Oracle City: PASS.
- Browser IAB: nove tipologie di pagina a 390 e 1280 px (home IT/ES/EN, Academy, Risorse, Video/slide, Pensiero critico, Cruciverba, Laboratorio tecnico). Un overflow del laboratorio è stato individuato, corretto e ricontrollato senza overflow.
- Home: reflow aggiuntivo a 320, 768 e 1024 px, senza overflow.
- Osservazione visiva di home desktop/mobile e laboratorio tecnico desktop/mobile.
- Ricerca “prompt”: risultati reali; menu mobile: apertura; M02: risposta espandibile aperta; slide M01: passaggio da 1/8 a 2/8. Nessun errore console restituito nei percorsi controllati.
- Contrasto calcolato delle principali coppie: #202020/bianco 16,29:1; #62625F/bianco 6,12:1; #777770/bianco 4,51:1; #52524E/#F7F7F5 7,32:1; #696962/#FAF3EF 5,04:1; bianco/#242424 15,52:1.
- `git diff --check`: PASS.

Limiti: nessun audit completo WCAG o axe; nessuna misura Lighthouse o Core Web Vitals sul campo. Nessuna matrice di dispositivi fisici o motori browser. I controlli di contrasto non coprono ogni stato e combinazione possibile. I font dipendono dal sistema operativo; il fallback è intenzionale. Nessun nuovo contenuto editoriale, chatbot o servizio backend aggiunto.

## Riproduzione e rollback
Il workflow di produzione già presente estrae `site-v0.7.zip`, concatena `theme/learning-colors.css`, esegue il controllo di invarianza, aggiunge firma/contatto e pubblica Oracle City. Ripetere in una directory pulita: non eseguire il controllo di invarianza dopo le iniezioni HTML o sul risultato di una compilazione precedente. Per rollback ripristinare i due file CSS alla revisione precedente mediante un nuovo commit.

## Completamento della landing — 3 novembre
Su richiesta del proprietario, logo originale e scritta MANZO AI si assemblano da frammenti geometrici in circa 2,7 secondi. L’esempio HTML allegato è stato letto come riferimento, senza eseguirne automaticamente il codice. Implementazione originale adattata al logo effettivo, con 36 frammenti temporanei, pulsante Replay, nessun audio, nessun blocco delle lingue. Ripristino degli elementi reali a fine animazione; fallback statico senza JavaScript e con movimento ridotto. Effetto limitato alla scelta lingua.

Aggiunta revisione hash al CSS condiviso per evitare che la cache mostri il tema precedente dopo la pubblicazione. Controlli di integrità dell’archivio eseguiti prima delle iniezioni autorizzate; archivio e contenuti didattici rimangono invariati. Browser: osservati stato running, 36 frammenti, tre lingue utilizzabili e stato complete senza frammenti residui. Movimento ridotto verificato nel codice, non emulato in questa sessione.
