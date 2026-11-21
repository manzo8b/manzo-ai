# La stanza dei giurati — staging v0.4

**Stato:** staging tecnico non pubblicato; **non effettuare merge** prima di aggiungere gli asset approvati e verificare il contrasto dopo il deploy.

## Architettura

Prototipo approvato: tre esperienze all'interno di Laboratorio, nell'ordine didattico Chiedi → Controlla → Decidi. L'immagine del palazzo conserva due stendardi MANZO. Il Banco di prova ha la narrazione Prima / Dopo / Chiave, un documento fittizio, prompt A/B ed errori verificabili. Officina locale ha sei casi sintetici, Sala dei confini dodici azioni e quattro incidenti; quest'ultima resta In preparazione finché non sono inserite fonti normative ufficiali.

### Percorsi già previsti

- /it/laboratorio/stanza-dei-giurati/
- /it/laboratorio/stanza-dei-giurati/banco-di-prova/
- /it/laboratorio/stanza-dei-giurati/officina-locale/
- /it/laboratorio/stanza-dei-giurati/sala-dei-confini/

## Sorgenti necessari prima di attivare il publisher

Collocare **senza riscriverli** in `product/jury-room/` i file approvati nel pacchetto v0.4, cioè i quattro HTML, `assets/` (CSS, JavaScript, immagini compresa `palazzo-stendardi-manzo.webp`, SVG e video compresso), e `sources/` con i quattro documenti originali. Inserire anche i test `tools/test_contrast.py`, `tools/test_experience.py`, `tools/test_rooms.py`, `tools/check_source_content.py` e `tools/check_rooms_sources.py`.

Il pacchetto integrale è stato consegnato come ZIP nella conversazione; GitHub non è la fonte definitiva finché questi file non sono stati trasferiti. Non si usa un segnaposto o una versione precedente delle immagini approvate.

## Regole di rilascio

- Nessuna modifica al menu lingue o ai blocchi Home approvati senza anteprima specifica
- Le pagine mantengono `noindex,nofollow`, non sono disponibili in EN/ES e non devono comparire nella sitemap
- Dati e identità degli scenari sono fittizi; niente API AI, cookie o risultati precompilati
- I componenti devono essere operabili da tastiera, con etichette testuali oltre ai colori e `prefers-reduced-motion`
- Almeno 4,5:1 sul testo ordinario a sfondo solido; controlli supplementari sugli sfondi fotografici e gli stati disabilitati
- In questa tranche l'accesso dalla Home è una **preview opzionale**, non un nuovo blocco pubblico
- Il publisher non va aggiunto al workflow di Pages prima del collaudo dei file nel branch

## Comandi di staging dopo l'aggiunta delle sorgenti

```bash
python3 theme/publish-jury-room.py --site _site
python3 theme/publish-jury-room.py --site _site --verify-only
python3 product/jury-room/tools/test_contrast.py
```

La modifica alla Home, una volta approvata, si esegue **dopo** `publish-home-magic-v2.py` e **prima** degli ultimi controlli di integrità. Conservare sempre il numero dei cinque blocchi, le sei card esistenti e la navigazione condivisa.

Questo documento e il publisher sono lo **scheletro di integrazione**, non la pubblicazione del prodotto.
