# MANZO AI — Standard vincolante per le card Academy

**Decisione editoriale e UX approvata il 19 novembre 2026.** Tutte le nuove card di corsi, laboratori o moduli pubblicate nella Home di MANZO AI devono rispettare la stessa struttura visuale e dimensionale delle card Academy esistenti.

## Regole di progetto

1. **Un solo sistema di card**, con le classi condivise `ma-course-grid`, `ma-course-card`, `ma-course-art`, `ma-course-info` e `ma-course-link`. Vietato creare una nuova card dall'aspetto autonomo senza un'esplicita decisione progettuale.
2. **Simmetria tra card**, a parità di viewport: larghezza, altezza complessiva, altezza della copertina, raggi degli angoli, padding, spaziatura verticale, tipografia e pulsante allineato in basso.
3. **Copertina differenziata ma coerente**: sono consentiti variazioni cromatiche e un simbolo specifico per il corso; devono restare le proporzioni e il linguaggio grafico del catalogo. Non trasformare una copertina in un hero alto quasi quanto l'intera card.
4. **Informazione breve e uniforme**: un'etichetta di tipo (es. «Lezione» o «Corso»), titolo non chiuso dal punto, una descrizione concisa e massimo due badge tematici. Il contenuto integrale resta nella pagina del corso.
5. **CTA su una riga**: testo «Apri il percorso» a sinistra, icona freccia in un cerchio a destra. Non spezzare la CTA su due righe e non spostare l'icona sotto il testo.
6. **Mobile-first**: verificare desktop, tablet e smartphone senza overflow, tagli, troncamenti arbitrari, badge isolati, caratteri sproporzionati o elementi che escono dai contenitori.
7. **Accessibilità**: HTML semantico, un unico link principale per il corso, focus ben visibile, contrasti sufficienti, riduzione del movimento rispettata.
8. **QA prima di pubblicare**: controllare la parità visiva rispetto ad almeno due card preesistenti sulla stessa Home, non soltanto che il codice compili. Il successo di GitHub Actions non sostituisce il collaudo visivo umano.

## Applicazione in codice

- Showcase dei corsi preesistenti: `theme/publish-home-showcase.py` e `theme/home-showcase.css`.
- Corso **Prompt vs Skill**: `theme/publish-prompt-skill-home.py` e `theme/prompt-skill-home-card.css`. Quest'ultimo è una rifinitura compatibile con le classi condivise, non un secondo design system.
- I prossimi publisher devono riutilizzare lo stesso componente o estrarre un componente condiviso. Non devono aggiungere override isolati che mutino proporzioni, CTA o densità editoriale.
- Mantenere la pipeline GitHub Pages e i test di integrità delle card. Se la card non è uniforme, il lavoro non è considerato visualmente approvato.

**Decisione da preservare:** *le card possono distinguersi per soggetto e colore, ma devono essere uniformi nella geometria, nella struttura informativa e nel comportamento responsivo*.