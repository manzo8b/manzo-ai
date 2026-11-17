# AI Teaching Lab — Studio voce v0.1

Data: 17 novembre 2026
Stato: codice e integrazione nel publisher completati; GitHub Pages, Safari/iPhone, microfono e riproduzione audio reali non ancora convalidati.

## Funzioni introdotte
- Brief (titolo, disciplina, destinatari, obiettivo osservabile, verifica di apprendimento)
- Copione editabile e scaletta locale (non generata con IA)
- Stima di durata basata sulle parole; indicativa e non cronometrata
- Prompt modificabile da copiare verso un servizio vocale esterno, senza API integrate
- Ascolto di prova tramite SpeechSynthesis del browser, esplicitamente NON definito voce IA
- Registrazione microfono con getUserMedia e MediaRecorder dopo consenso browser
- Importazione e ascolto file audio (limite 30 MB)
- Download dell'audio nel formato originario supportato dal browser
- Trascrizione manuale e download .txt
- Provenienza audio: registrazione personale, servizio IA esterno o altra fonte
- Checklist su contenuto, qualità acustica, trascrizione e diritti/privacy
- Gate di approvazione docente con invalidazione al successivo cambiamento dei contenuti
- Esportazione JSON di metadati, con audio scaricato separatamente

## Sicurezza e trasparenza
- Nessuna richiesta a un provider IA, nessuna chiamata audio al backend; nessun token API esposto
- Non utilizzare voci identificabili di minori, imitazioni di persone reali o registrazioni senza consenso
- Il JSON contiene dichiarazioni del docente, non è una certificazione indipendente
- File audio residente nella sessione del browser; nessuna conservazione cloud dichiarata
- Registrazione microfono solo HTTPS/localhost e nei browser supportati
- Non promettere che tutti i browser supportino identici codec o il motore vocale di sistema

## Integrazione
- Sorgente: tools/ai-teaching-voice-studio/index.html
- Publisher: theme/publish-ai-teaching-lab.py
- Pagina risultante prevista: /manzo-ai/it/formazione/ia-per-la-didattica/studio-voce/
- Collegamenti previsti da landing e laboratorio multimediale
- Workflow: .github/workflows/deploy-pages.yml, con trigger per tools/ai-teaching-voice-studio/** e test file/link

## Test da eseguire realmente
1. Workflow Pages completato con esito positivo, collegamenti 200, nessun conflitto con lezioni o laboratorio immagini
2. Desktop Chrome: consenso microfono, start/stop, riproduzione, download e riapertura file
3. Safari macOS e Safari iPhone: gestione permessi, codec reale, stop, import, download, HTTPS
4. Negare permesso e verificare messaggio e nuova prova senza blocchi
5. Audio importato: provenienza obbligatoria, controlli di privacy e licenza
6. Approvazione: negata senza audio/trascrizione/check; consentita dopo verifica; invalidata da modifica
7. Controlli accessibilità: tastiera, zoom 200%, VoiceOver e contrasto
8. Verificare che i file non siano caricati remotamente e che JSON non contenga audio
9. Docenti pilota: verificare che il percorso formi alla scrittura e revisione del copione, non soltanto alla registrazione

## Evoluzione successiva
- Studio video integrato nel laboratorio multimediale
- Solo in seguito valutare un provider vocale con backend protetto, consenso esplicito, costi, licenze e GDPR
