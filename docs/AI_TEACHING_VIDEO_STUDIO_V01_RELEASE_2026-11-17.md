# AI Teaching Lab — Studio video v0.1 · Registro di rilascio
Data: 17 novembre 2026

## Stato
Implementazione sorgente e publisher GitHub Pages aggiornati su branch main. Controlli statici sul codice e i riferimenti superati. **Deploy e verifica dal browser reale non confermati.** Non dichiarare la pagina pubblicata prima del riscontro del workflow e di un HTTP 200.

## Funzioni sviluppate
- Brief didattico: destinatari, disciplina, obiettivi, motivazione del mezzo video, verifica dell'apprendimento
- Storyboard modificabile e riordinabile (fino a 12 scene) con durata 2–30 secondi ciascuna, funzione pedagogica e didascalia
- Immagini PNG/JPEG/WebP importate localmente, massimo 10 MB ciascuna, provenienza/diritti/modello dichiarati
- Prompt scene-by-scene esportabile verso generatori esterni: **nessuna API o modello generativo effettivamente integrato**
- Anteprima temporizzata nel browser con immagini e didascalie
- Audio importabile soltanto come riferimento separato, non sincronizzato e non incorporato
- Esportazione video WebM **silenzioso** via Canvas.captureStream + MediaRecorder nei browser compatibili, max 180 secondi
- Sottotitoli WebVTT basati sulla durata delle scene e inserimento di una riga per scena, da verificare manualmente
- Descrizione accessibile, checklist di controllo, gate approvazione e invalidazione dopo modifiche
- JSON contenente dati, metadati e stato di verifica, senza incorporare file audio/video/immagine

## Percorsi
Sorgente: tools/ai-teaching-video-studio/index.html
Publisher: theme/publish-ai-teaching-lab.py
Destinazione attesa: /manzo-ai/it/formazione/ia-per-la-didattica/studio-video/
Link in landing del corso e laboratorio multimediale
Workflow: .github/workflows/deploy-pages.yml (include trigger tools/** e controlli pagina)

## Verifiche da eseguire
1. Deploy Pages success e HTTP 200 sulla rotta; link dalla home e dal laboratorio
2. Test senza scene, scena incompleta, riordinamento, eliminazione e limite 12 scene
3. Import immagini corrette e file >10 MB o formato errato
4. Anteprima stop/play, sequenza e cronologia durata
5. Generazione video WebM in Chrome desktop, controllo durata/video silenzioso; fallback Safari/iOS se captureStream non supportato
6. WebVTT: cue validi e correzione manuale della sincronizzazione
7. Verifica privacy/provenienza, impossibilità approvare materiale senza checklist, immagini, sottotitoli e reviewer
8. Invalidazione approvazione su modifica storyboard, sottotitoli e dati
9. Accessibilità tastiera, VoiceOver, zoom 200%, reduced motion, contrasto
10. Esportazione JSON priva di media binari e coerenza degli identificatori scene
11. QA pedagogica con docenti; nessuna pubblicazione automatica dei lavori

## Limiti da spiegare
Non è un editor non lineare completo; non sincronizza/concatena l'audio né monta clip video importate. Non incorpora sottotitoli nel file WebM e non genera immagini/voci/video con IA. Il video locale silenzioso è dimostrativo e dipende da supporto browser, risorse disponibili e mantenimento attivo della scheda.

## Prossimo salto
Realizzare un unico workspace che unisca asset approvati degli Studi immagini, voce e video, con pacchetto di consegna e manifest di provenienza verificabile, prima di qualsiasi API IA esterna.
