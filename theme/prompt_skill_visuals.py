#!/usr/bin/env python3
"""Accessible HTML information graphics for MANZO AI's Prompt vs Skill course.

Educational diagrams are native HTML, not images. Each figure restates the
documented lesson as an explanatory flow without implying a universal syntax.
The family case is a fictional exercise: the visual makes its reasoning visible
even when the long final reading is collapsed.
"""
from __future__ import annotations

PROMPT_MAP = '''
<figure class="ps-viz ps-viz--prompt" id="mappa-prompt" aria-labelledby="ps-viz-prompt-title">
  <figcaption>
    <span class="ps-viz-eyebrow">MAPPA VISIVA / 01</span>
    <strong id="ps-viz-prompt-title">L'architettura di un prompt</strong>
    <span>Otto elementi da scegliere in modo proporzionato al compito, non una formula obbligatoria</span>
  </figcaption>
  <ol class="ps-viz-prompt-grid">
    <li><span class="ps-viz-index">01</span><strong>Obiettivo</strong><small>Che cosa voglio ottenere?</small></li>
    <li><span class="ps-viz-index">02</span><strong>Contesto</strong><small>Per chi e in quale situazione?</small></li>
    <li><span class="ps-viz-index">03</span><strong>Materiali</strong><small>Con quali dati e documenti?</small></li>
    <li><span class="ps-viz-index">04</span><strong>Compito</strong><small>Che cosa deve fare il modello?</small></li>
    <li><span class="ps-viz-index">05</span><strong>Procedura</strong><small>Quali passaggi servono?</small></li>
    <li><span class="ps-viz-index">06</span><strong>Vincoli</strong><small>Quali limiti deve rispettare?</small></li>
    <li><span class="ps-viz-index">07</span><strong>Output</strong><small>In quale forma rispondere?</small></li>
    <li><span class="ps-viz-index">08</span><strong>Verifica</strong><small>Come controllo il risultato?</small></li>
  </ol>
  <div class="ps-viz-conclusion"><span aria-hidden="true">✓</span><p><strong>Il prompt organizza la richiesta</strong> · Le istruzioni devono essere sufficientemente chiare da poter essere controllate, non soltanto lunghe.</p></div>
</figure>'''

DECISION_MAP = '''
<figure class="ps-viz ps-viz--decision" id="mappa-salto" aria-labelledby="ps-viz-decision-title">
  <figcaption>
    <span class="ps-viz-eyebrow">MAPPA VISIVA / 02</span>
    <strong id="ps-viz-decision-title">Quando conviene passare dal prompt alla skill?</strong>
    <span>Il salto non è automatico: ogni domanda può suggerire una soluzione più semplice</span>
  </figcaption>
  <div class="ps-viz-decision-track">
    <div class="ps-viz-decision-row">
      <div class="ps-viz-question"><span>DOMANDA 1</span><strong>È un incarico occasionale?</strong><small>Mi serve una risposta specifica una sola volta</small></div>
      <div class="ps-viz-decision-answer"><span class="ps-viz-branch-tag">SÌ</span><strong>Prompt</strong><small>La soluzione più diretta</small></div>
    </div>
    <div class="ps-viz-decision-down"><span>NO · Il compito ritorna</span><b aria-hidden="true">↓</b></div>
    <div class="ps-viz-decision-row">
      <div class="ps-viz-question"><span>DOMANDA 2</span><strong>Cambiano solo poche informazioni?</strong><small>La struttura è stabile, ma variano argomenti e dati</small></div>
      <div class="ps-viz-decision-answer"><span class="ps-viz-branch-tag">SÌ</span><strong>Prompt template</strong><small>Riutilizza il testo con variabili</small></div>
    </div>
    <div class="ps-viz-decision-down"><span>NO · Il metodo è più articolato</span><b aria-hidden="true">↓</b></div>
    <div class="ps-viz-decision-row">
      <div class="ps-viz-question"><span>DOMANDA 3</span><strong>Ci sono procedure, risorse e controlli ricorrenti?</strong><small>E ho un agente compatibile, tempo per test e manutenzione?</small></div>
      <div class="ps-viz-decision-answer ps-viz-decision-answer--skill"><span class="ps-viz-branch-tag">SÌ, SE UTILE</span><strong>Skill</strong><small>Un procedimento riutilizzabile</small></div>
    </div>
  </div>
  <p class="ps-viz-footnote">Se la risposta all'ultima domanda è no, resta su un prompt template o documenta prima il workflow. Una skill non garantisce risultati migliori: occorre provarla.</p>
</figure>'''

SKILL_MAP = '''
<figure class="ps-viz ps-viz--skill" id="mappa-skill" aria-labelledby="ps-viz-skill-title">
  <figcaption>
    <span class="ps-viz-eyebrow">MAPPA VISIVA / 03</span>
    <strong id="ps-viz-skill-title">L'architettura di una skill ottimizzata</strong>
    <span>Nel formato Agent Skills, metadati e istruzioni abitano nel file SKILL.md</span>
  </figcaption>
  <div class="ps-viz-skill-root"><span class="ps-viz-file-icon" aria-hidden="true">⌁</span><div><strong>ripasso-guidato/</strong><small>Cartella della skill</small></div></div>
  <div class="ps-viz-skill-connector" aria-hidden="true"></div>
  <div class="ps-viz-skill-core">
    <div class="ps-viz-skill-file"><span>FILE CENTRALE · OBBLIGATORIO</span><strong>SKILL.md</strong><small>Testo in Markdown con metadati YAML</small></div>
    <div class="ps-viz-skill-inner">
      <div><span class="ps-viz-mini">01 / METADATI</span><strong>name + description</strong><small>Identità e quando usare la skill</small></div>
      <div><span class="ps-viz-mini">02 / ISTRUZIONI</span><strong>Obiettivo e procedura</strong><small>Input, passaggi, vincoli, output e controlli</small></div>
    </div>
  </div>
  <div class="ps-viz-skill-connector ps-viz-skill-connector--optional" aria-hidden="true"></div>
  <div class="ps-viz-skill-resources" aria-label="Risorse aggiuntive facoltative">
    <div><span>FACOLTATIVO</span><strong>references/</strong><small>Documenti di riferimento</small></div>
    <div><span>FACOLTATIVO</span><strong>assets/</strong><small>Modelli e materiali</small></div>
    <div><span>FACOLTATIVO</span><strong>scripts/</strong><small>Codice da verificare</small></div>
  </div>
  <div class="ps-viz-conclusion"><span aria-hidden="true">✓</span><p><strong>La skill organizza un metodo</strong> · I dati di un singolo incarico restano nel prompt dell'utente; la procedura stabile nella skill.</p></div>
</figure>'''

FAMILY_MAP = '''
<section class="ps-shell ps-family-map" id="mappa-famiglia" aria-labelledby="ps-family-title">
  <div class="ps-family-map-panel">
    <div class="ps-family-heading">
      <div><p class="ps-viz-eyebrow">MAPPA VISIVA / 04 · CASO DIDATTICO FITTIZIO</p>
        <h2 id="ps-family-title">Una famiglia, quattro figli, molte decisioni</h2>
        <p>Il procedimento imparato con prompt e skill diventa una griglia per riflettere su problemi reali, senza chiedere all'IA di decidere al nostro posto.</p></div>
      <span class="ps-family-icon" aria-hidden="true">2 + 4</span>
    </div>
    <div class="ps-family-domains" aria-label="Aree di organizzazione della famiglia">
      <div><span aria-hidden="true">▦</span><strong>Scuola</strong><small>Orari, compiti, verifiche</small></div>
      <div><span aria-hidden="true">✚</span><strong>Salute</strong><small>Visite e necessità</small></div>
      <div><span aria-hidden="true">◷</span><strong>Lavoro</strong><small>Turni e disponibilità</small></div>
      <div><span aria-hidden="true">€</span><strong>Finanze</strong><small>Budget e scadenze</small></div>
      <div><span aria-hidden="true">✧</span><strong>Ferie</strong><small>Riposo e spostamenti</small></div>
    </div>
    <p class="ps-family-center-note">La domanda di partenza: <strong>come conciliare esigenze diverse senza trascurare ciò che conta?</strong></p>
    <ol class="ps-family-process">
      <li><span>01</span><strong>Comprendere</strong><small>Qual è il problema reale?</small></li>
      <li><span>02</span><strong>Raccogliere</strong><small>Che cosa sappiamo? Che cosa manca?</small></li>
      <li><span>03</span><strong>Valutare</strong><small>Tempo, risorse, bisogni e priorità</small></li>
      <li><span>04</span><strong>Decidere</strong><small>Chi fa cosa, quando e perché?</small></li>
    </ol>
    <div class="ps-family-disruption">
      <div class="ps-family-alert"><span aria-hidden="true">!</span><div><span>IMPREVISTO · MARTEDÌ</span><strong>Uno dei figli si ammala</strong><p>Il calendario non è più sufficiente: un impegno va rivisto, le persone vanno ascoltate, le priorità possono cambiare.</p></div></div>
      <span class="ps-family-reframe" aria-hidden="true">↓</span>
      <div class="ps-family-revision"><span>RAGIONAMENTO E REVISIONE</span><strong>Raccogliere nuovi dati → confrontare alternative → concordare un nuovo piano</strong><p>La procedura è utile se aiuta a riconoscere quando il piano iniziale non funziona. Salute, relazioni e responsabilità non sono semplici caselle da ottimizzare.</p></div>
    </div>
    <div class="ps-family-outcome"><strong>Che cosa rimane, senza IA?</strong><span>La capacità di formulare domande, distinguere fatti e ipotesi, motivare una decisione e correggerla quando la situazione cambia</span></div>
    <a class="ps-family-reading-link" href="#lettura-6" data-open-reading="lettura-6">Leggi il racconto completo e prova il laboratorio senza IA <span aria-hidden="true">↗</span></a>
    <p class="ps-family-limit">Questo è un esercizio pedagogico, non una prova che il prompt engineering migliori automaticamente le capacità cognitive.</p>
  </div>
</section>'''

def decorate_reading(index:int, html:str)->str:
    """Inject a figure before its corresponding explanatory subheading."""
    figures={
        2: ('<h3>Dalla versione breve alla versione progettata</h3>', PROMPT_MAP),
        3: ('<h3>Non sempre serve una skill</h3>', DECISION_MAP),
        4: ('<h3>La cartella e i file</h3>', SKILL_MAP),
        6: ('<h3>Una struttura utile non sostituisce i valori</h3>',
            '<p class="ps-viz-reading-ref">Per osservare le decisioni, consulta anche la '
            '<a href="#mappa-famiglia">mappa visiva della famiglia con quattro figli</a>, '
            'poi torna al racconto e alla sua riflessione.</p>'),
    }
    if index not in figures: return html
    needle,extra=figures[index]
    if html.count(needle)!=1:
        raise RuntimeError(f"Missing or repeated visual insertion point in reading {index}: {needle}")
    return html.replace(needle,extra+"\n"+needle,1)

def family_map()->str:
    return FAMILY_MAP
