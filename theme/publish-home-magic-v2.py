#!/usr/bin/env python3
"""MANZO AI Home v2 — QUESTION > EVIDENCE > DECISION, IT/EN/ES.

DRAFT / BRANCH-ONLY until owner approves. No public deployment, sidebar, footer,
root language gateway, its styling or switcher behaviour are modified.
Reads exact destinations and titles from existing Academy and the 7 real Home
course cards; appends a minimal, unstyled-by-default index to each Academy
so no course disappears from public navigation.

Usage:
  python3 theme/publish-home-magic-v2.py --site _site
  python3 theme/publish-home-magic-v2.py --site _site --verify-only

This script must run AFTER all existing Home card publishers and SEO polish
in the preview build. It replaces the main content inside <main id="content">
and preserves the main wrapper, sidebar, language controls, footer and root page.
"""
from __future__ import annotations

import argparse
from html import escape, unescape
from pathlib import Path
import re
import hashlib
import shutil

ROOT=Path(__file__).resolve().parent
BASE="/manzo-ai/"
CSS=ROOT/"home-magic-v2.css"
JS=ROOT/"home-magic-v2.js"
MARKER='data-ma-home-v2="preview"'
LOCALES=("it","en","es")
ACADEMY={"it":"academy","en":"academy","es":"academia"}
ABOUT={"it":"chi-siamo","en":"about","es":"quienes-somos"}
PROF={"it":"it/formazione/costruire-in-sicurezza","en":"en/learning/build-safely","es":"es/formacion/construir-con-seguridad"}
TEACHING_IT="it/formazione/ia-per-la-didattica/inizia"
PAGES={
 "it":{
  "title":"L’IA ti ha risposto con sicurezza. Ma è vero? | MANZO AI",
  "desc":"Impara a fare le domande giuste, verificare le risposte dell'intelligenza artificiale e scegliere percorsi pratici di formazione in MANZO AI.",
  "eyebrow":"MANZO AI / IMPARA A PENSARE, NON SOLO A CHIEDERE",
  "h1":"L’IA ti ha risposto con sicurezza. Ma è vero?",
  "lead":"Impara a fare le domande giuste, a controllare le risposte e a decidere tu.",
  "primary":"Inizia dalle basi",
  "secondary":"Prova una sfida di pensiero critico",
  "magic_alt":"La scatola sembra una magia. Aprirla significa vedere il metodo: domanda, verifica e decisione.",
  "magic_note":"La magia incuriosisce. Il metodo ti rende autonomo.",
  "pause":"Metti in pausa l’animazione","play":"Riprendi l’animazione",
  "pause_short":"Pausa","play_short":"Riprendi","lab_label":"Conoscenza e prompt",
  "magic_steps":["LA DOMANDA","IL METODO","LA PROVA"],
  "featured":"Percorsi in evidenza",
  "featured_lead":"Sei ingressi, un obiettivo: passare dalla risposta plausibile a una scelta consapevole.",
  "academy":"Esplora tutta l’Academy",
  "kind":["Corso","Modulo","Lezione","Lezione","Lezione","Lezione"],
  "codes":["AI / 01","DEV / 02","AI / 03","LAB / 04","QA / 05","OPS / 06"],
  "hooks":[
   "Come riconosci un errore che sembra perfetto?",
   "Quel codice generato dall’IA, lo metteresti in produzione?",
   "Perché l’IA a volte si inventa le cose?",
   "Perché la stessa domanda dà risposte così diverse?",
   "Come controlli una risposta prima di usarla?",
   "Chi risponde quando l’IA sbaglia nel tuo lavoro?"
  ],
  "tags":[["Fonti","Verificabilità"],["Coding","Controllo"],["Modelli","Fondamenti"],["Prompt","Metodo"],["Qualità","Evidenze"],["Processi","Supervisione"]],
  "open":"Apri il percorso",
  "focus_title":"L’IA cambia i compiti. Il giudizio resta tuo",
  "focus_intro":"Approfondisci con percorsi pensati per chi insegna e per chi prende decisioni sul lavoro.",
  "teacher":"Porta l’IA in classe senza perdere il controllo",
  "teacher_text":"Progetta attività, verifica i materiali e mantieni centrale la responsabilità educativa.",
  "teacher_note":"Il corso completo è attualmente disponibile in italiano",
  "teacher_cta":"Esplora AI Teaching Lab",
  "professional":"Quando un errore dell’IA costa caro",
  "professional_text":"Dati, sicurezza e supervisione umana: costruisci flussi che puoi controllare.",
  "professional_cta":"Impara a costruire in sicurezza",
  "challenge_eyebrow":"IL PENSIERO CRITICO SI ALLENA",
  "challenge":"Sai distinguere un’intuizione da una prova?",
  "challenge_text":"Metti alla prova le tue certezze. Non serve conoscere tutte le risposte: serve sapere cosa controllare.",
  "challenge_cta":"Accetta la sfida",
  "closing":"Un progetto indipendente, costruito sulle fonti",
  "closing_text":"MANZO AI è curato da Marcelo Javier Fernandez Caballero, sotto il marchio MARCELUS AI LAB.",
  "about":"Scopri chi siamo",
  "extra":"Altri percorsi da esplorare",
  "extra_lead":"Sono già pubblicati e rimangono disponibili in questa Academy.",
  "note":"Risorse formative aperte · Senza attestati inventati",
 },
 "en":{
  "title":"AI answered confidently. But is it true? | MANZO AI",
  "desc":"Learn to ask better questions, verify AI answers, and make your own informed decisions with practical MANZO AI learning paths.",
  "eyebrow":"MANZO AI / LEARN TO THINK, NOT JUST TO PROMPT",
  "h1":"AI answered confidently. But is it true?",
  "lead":"Learn to ask better questions, check the evidence and decide for yourself.",
  "primary":"Start with the basics",
  "secondary":"Try a critical-thinking challenge",
  "magic_alt":"The box looks like magic. Opening it reveals a method: question, verification and decision.",
  "magic_note":"Magic sparks curiosity. Method builds independence.",
  "pause":"Pause the animation","play":"Resume the animation",
  "pause_short":"Pause","play_short":"Resume","lab_label":"Knowledge & Prompt Lab",
  "magic_steps":["THE QUESTION","THE METHOD","THE EVIDENCE"],
  "featured":"Featured learning paths",
  "featured_lead":"Six entry points, one goal: move beyond plausible answers towards informed decisions.",
  "academy":"Explore the full Academy",
  "kind":["Course","Module","Lesson","Lesson","Lesson","Lesson"],
  "codes":["AI / 01","DEV / 02","AI / 03","LAB / 04","QA / 05","OPS / 06"],
  "hooks":[
   "How can an error look entirely convincing?",
   "Would you put that AI-generated code into production?",
   "Why does AI sometimes make things up?",
   "Why can one question lead to different answers?",
   "How do you check an answer before using it?",
   "Who is accountable when AI fails at work?"
  ],
  "tags":[["Sources","Evidence"],["Coding","Review"],["Models","Foundations"],["Prompts","Method"],["Quality","Verification"],["Workflows","Oversight"]],
  "open":"Open learning path",
  "focus_title":"AI changes the work. Judgment stays with you",
  "focus_intro":"Go deeper with learning paths for educators and working professionals.",
  "teacher":"Bring AI into your classroom without losing control",
  "teacher_text":"Design activities, verify materials and keep educational responsibility human.",
  "teacher_note":"The full AI Teaching Lab is currently available in Italian",
  "teacher_cta":"Explore the Italian Teaching Lab",
  "professional":"When an AI error has real consequences",
  "professional_text":"Protect data, manage operational risk and design workflows with human oversight.",
  "professional_cta":"Learn to build safely",
  "challenge_eyebrow":"CRITICAL THINKING TAKES PRACTICE",
  "challenge":"Can you tell an intuition from evidence?",
  "challenge_text":"Challenge your assumptions. You need not know every answer; you need to know what to check.",
  "challenge_cta":"Take the challenge",
  "closing":"An independent project grounded in sources",
  "closing_text":"MANZO AI is curated by Marcelo Javier Fernandez Caballero under the MARCELUS AI LAB brand.",
  "about":"About this project",
  "extra":"More learning paths",
  "extra_lead":"These published courses remain available through the Academy.",
  "note":"Open learning resources · No unearned certificates",
 },
 "es":{
  "title":"La IA respondió con seguridad. ¿Pero es verdad? | MANZO AI",
  "desc":"Aprende a formular preguntas, comprobar las respuestas de la IA y decidir con criterio mediante itinerarios prácticos de MANZO AI.",
  "eyebrow":"MANZO AI / APRENDE A PENSAR, NO SOLO A PREGUNTAR",
  "h1":"La IA respondió con seguridad. ¿Pero es verdad?",
  "lead":"Aprende a formular buenas preguntas, comprobar las respuestas y decidir por tu cuenta.",
  "primary":"Empieza por lo básico",
  "secondary":"Prueba un reto de pensamiento crítico",
  "magic_alt":"La caja parece magia. Al abrirse muestra un método: pregunta, comprobación y decisión.",
  "magic_note":"La magia despierta curiosidad. El método te da autonomía.",
  "pause":"Pausar la animación","play":"Reanudar la animación",
  "pause_short":"Pausar","play_short":"Reanudar","lab_label":"Conocimiento y prompts",
  "magic_steps":["LA PREGUNTA","EL MÉTODO","LA PRUEBA"],
  "featured":"Itinerarios destacados",
  "featured_lead":"Seis puertas de entrada, un objetivo: pasar de respuestas plausibles a decisiones informadas.",
  "academy":"Explora toda la Academia",
  "kind":["Curso","Módulo","Lección","Lección","Lección","Lección"],
  "codes":["AI / 01","DEV / 02","AI / 03","LAB / 04","QA / 05","OPS / 06"],
  "hooks":[
   "¿Cómo reconoces un error que parece perfecto?",
   "¿Publicarías ese código generado por IA?",
   "¿Por qué a veces la IA inventa cosas?",
   "¿Por qué una misma pregunta da respuestas tan distintas?",
   "¿Cómo compruebas una respuesta antes de utilizarla?",
   "¿Quién responde si la IA se equivoca en tu trabajo?"
  ],
  "tags":[["Fuentes","Evidencias"],["Código","Revisión"],["Modelos","Fundamentos"],["Prompts","Método"],["Calidad","Comprobación"],["Procesos","Supervisión"]],
  "open":"Abrir itinerario",
  "focus_title":"La IA cambia el trabajo. El criterio sigue siendo tuyo",
  "focus_intro":"Profundiza con itinerarios para docentes y profesionales.",
  "teacher":"Lleva la IA al aula sin perder el control",
  "teacher_text":"Diseña actividades, verifica materiales y mantén la responsabilidad educativa en manos humanas.",
  "teacher_note":"El curso completo AI Teaching Lab está disponible actualmente en italiano",
  "teacher_cta":"Explora AI Teaching Lab en italiano",
  "professional":"Cuando un error de IA tiene consecuencias",
  "professional_text":"Datos, seguridad y control humano: diseña procesos que puedas supervisar.",
  "professional_cta":"Aprende a construir con seguridad",
  "challenge_eyebrow":"EL PENSAMIENTO CRÍTICO SE ENTRENA",
  "challenge":"¿Sabes distinguir una intuición de una prueba?",
  "challenge_text":"Pon a prueba tus certezas. No hace falta saber todas las respuestas, sino saber qué comprobar.",
  "challenge_cta":"Acepta el reto",
  "closing":"Un proyecto independiente basado en fuentes",
  "closing_text":"MANZO AI está coordinado por Marcelo Javier Fernandez Caballero bajo la marca MARCELUS AI LAB.",
  "about":"Quiénes somos",
  "extra":"Más itinerarios disponibles",
  "extra_lead":"Estos cursos publicados siguen disponibles en la Academia.",
  "note":"Recursos formativos abiertos · Sin certificados inventados",
 },
}

CARD=re.compile(r'<article\b(?=[^>]*data-ma-course-card=["\']1["\'])[^>]*>.*?</article\s*>',re.I|re.S)
EXTENDED=re.compile(r'<article\b(?=[^>]*data-ma-home-course=["\'][^"\']+["\'])[^>]*>.*?</article\s*>',re.I|re.S)
ANCHOR=re.compile(r'<a\b[^>]*href=["\']([^"\']+)["\']',re.I)
HEADING=re.compile(r'<h3\b[^>]*>(.*?)</h3>',re.I|re.S)
MAIN=re.compile(r'<main\b[^>]*id=["\']content["\'][^>]*>',re.I|re.S)
END_MAIN=re.compile(r'</main\s*>',re.I|re.S)
END_HEAD=re.compile(r'</head\s*>',re.I)
SECTION_CHALLENGE=re.compile(r'<section\b[^>]*class=["\'][^"\']*\bchallenge-home\b[^"\']*["\'][^>]*>.*?</section\s*>',re.I|re.S)
BODY_LOCALE=re.compile(r'<html\b[^>]*lang=["\']([^"\']+)["\']',re.I)
SECTION_TAG='<section data-ma-v2-section='
COLORS=["blue","midnight","teal","amber","violet","rose"]
ICONS=[
'<path d="M12 28h17m8 0h13M31 9v12m0 14v11"/><circle cx="31" cy="28" r="9"/><circle cx="31" cy="28" r="2" fill="currentColor" stroke="none"/>',
'<path d="m23 16-11 13 11 13m17-26 11 13-11 13M36 10l-10 39"/><path d="m37 50 5 5 9-10"/>',
'<circle cx="31" cy="31" r="19"/><circle cx="31" cy="31" r="7"/><path d="M31 12v12m0 14v12M12 31h12m14 0h12"/>',
'<path d="M14 18h28M14 30h22M14 42h34"/><path d="m39 11 10 10-10 10"/>',
'<circle cx="31" cy="31" r="21"/><circle cx="31" cy="31" r="12"/><path d="m23 31 6 6 13-14"/>',
'<rect x="10" y="12" width="16" height="16" rx="3"/><rect x="38" y="34" width="16" height="16" rx="3"/><path d="M26 20h18v14m-5-6 5 6 6-6M38 42H22V28"/>'
]

def e(s):return escape(str(s),quote=True)
def strip(s):return unescape(re.sub(r'<[^>]+>','',s)).strip()
def link(loc,sub):return BASE+loc+'/'+sub.strip('/')+'/'
def file_for(site,href):
 if not href.startswith(BASE) or not href.endswith('/'):
  raise RuntimeError("Invalid local route "+href)
 page=site/href[len(BASE):]/"index.html"
 if not page.is_file():raise RuntimeError("Unpublished target "+href)
 return page

def academy_path(loc):return link(loc,ACADEMY[loc])
def academy_card_markup(site,loc):
 """Use exactly the six approved Academy card components from the generated catalog.

 No alternate HTML, duplicated metadata, static mockups or cloned interaction CSS.
 The existing Academy stylesheet remains the single visual source of truth.
 """
 academy=file_for(site,academy_path(loc)).read_text(encoding="utf-8")
 cards=CARD.findall(academy)
 if len(cards)!=6:raise RuntimeError(f"{loc}: expected six Academy components; got {len(cards)}")
 seen=set()
 for index,raw in enumerate(cards,1):
  links=ANCHOR.findall(raw)
  titles=HEADING.findall(raw)
  if len(links)!=1 or len(titles)!=1:
   raise RuntimeError(f"{loc}: card {index} must contain one real link and heading")
  href=unescape(links[0])
  if not href.startswith(BASE+loc+"/"):
   raise RuntimeError(f"{loc}: card links to another language: {href}")
  file_for(site,href)
  if href in seen:raise RuntimeError(f"{loc}: duplicate Academy destination {href}")
  if not strip(titles[0]):raise RuntimeError(f"{loc}: blank Academy title {index}")
  seen.add(href)
 return cards

def target_cards(site,loc):
 result=[]
 for raw in academy_card_markup(site,loc):
  result.append((unescape(ANCHOR.search(raw).group(1)),
                 strip(HEADING.search(raw).group(1))))
 return result

def extra_cards(site,loc,home):
 cards=EXTENDED.findall(home)
 if len(cards)!=7:
  raise RuntimeError(f"{loc}: expected 7 previously published new course cards; got {len(cards)}")
 result=[]
 for raw in cards:
  href=ANCHOR.search(raw);heading=HEADING.search(raw)
  if not href or not heading:raise RuntimeError(f"{loc}: incomplete added course card")
  destination=unescape(href.group(1))
  file_for(site,destination)
  result.append((destination,strip(heading.group(1))))
 if len({x[0] for x in result})!=7:
  raise RuntimeError(f"{loc}: duplicates among newly published course cards")
 return result

def challenge(site,loc,home):
 # The original challenge-home section contains the actual published destination.
 m=SECTION_CHALLENGE.search(home)
 if not m:raise RuntimeError("Original challenge banner missing: "+loc)
 hrefs=[unescape(h) for h in ANCHOR.findall(m.group())]
 candidates=[h for h in hrefs if h.startswith(BASE) and h.endswith('/') and (site/h[len(BASE):]/'index.html').is_file()]
 if not candidates:raise RuntimeError("Challenge link has no published target "+loc)
 return candidates[0]

def icon(i):
 return (f'<svg aria-hidden="true" viewBox="0 0 64 64" fill="none" stroke="currentColor" '
         f'stroke-width="2.9" stroke-linecap="round" stroke-linejoin="round">{ICONS[i]}</svg>')

def magic_box(loc):
 d=PAGES[loc]
 # A decorative SVG; narrative is available as text in the figcaption.
 scene='''<svg class="ma-v2-box-svg" viewBox="0 0 560 500" aria-hidden="true" focusable="false">
 <defs>
   <linearGradient id="v2-face-left" x1="0" y1="0" x2="1" y2="1">
     <stop offset="0" stop-color="#255c8a"/><stop offset="1" stop-color="#1c4773"/>
   </linearGradient>
   <linearGradient id="v2-face-right" x1="0" y1="0" x2="1" y2="1">
     <stop offset="0" stop-color="#196f7a"/><stop offset="1" stop-color="#14495b"/>
   </linearGradient>
   <linearGradient id="v2-lid" x1="0" y1="0" x2="1" y2="1">
     <stop offset="0" stop-color="#f7fbff"/><stop offset="1" stop-color="#c9e5ef"/>
   </linearGradient>
 </defs>
 <ellipse cx="280" cy="431" rx="170" ry="26" fill="#224d70" opacity=".10"/>
 <g class="ma-v2-orbit">
   <ellipse cx="278" cy="230" rx="200" ry="90" fill="none" stroke="#8cc5d2" stroke-dasharray="5 12" opacity=".46"/>
 </g>

 <g class="ma-v2-box">
   <path d="M115 242 277 160 438 243 276 326Z" fill="#153955" stroke="#2d687f" stroke-width="3"/>
   <path d="M115 242 276 326 276 415 115 331Z" fill="url(#v2-face-left)" stroke="#244e75" stroke-width="2"/>
   <path d="M276 326 438 243 438 329 276 415Z" fill="url(#v2-face-right)" stroke="#164d62" stroke-width="2"/>
   <path d="M132 270 265 336M290 337 422 269" stroke="#ffffff" opacity=".28" stroke-width="2" fill="none"/>
   <path d="M229 361l23 13v-22l27 15v22l23-13" stroke="#d2eaf0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity=".86"/>
   <g class="ma-v2-lid">
     <path d="M105 231 277 142 451 231 278 321Z" fill="url(#v2-lid)" stroke="#245570" stroke-width="3"/>
     <path d="M105 231v20l173 90v-20Z" fill="#d4eaf0" stroke="#245570" stroke-width="2"/>
     <path d="M278 321v20l173-90v-20Z" fill="#b6d8e2" stroke="#245570" stroke-width="2"/>
     <path d="m211 229 62 35 70-37" fill="none" stroke="#3d8192" stroke-width="3" stroke-linecap="round"/>
   </g>
 </g>
 <!-- These symbols render after the lid while it opens, so they remain visible.
      They are faded out when the lid closes, preserving the closed-box silhouette. -->
 <g class="ma-v2-artifacts">
   <g class="ma-v2-artifact ma-v2-a"><rect x="207" y="85" rx="12" width="82" height="72" fill="#fff" stroke="#3d88a1" stroke-width="2"/><path d="M225 113h46m-46 17h30" stroke="#3d88a1" stroke-width="4" stroke-linecap="round"/><circle cx="266" cy="132" r="4" fill="#cf9042"/></g>
   <g class="ma-v2-artifact ma-v2-b"><rect x="306" y="77" rx="13" width="80" height="76" fill="#fffaf1" stroke="#bb8545" stroke-width="2"/><path d="m325 113 16 16 25-32" stroke="#ae762b" stroke-width="6" stroke-linecap="round" fill="none"/></g>
   <g class="ma-v2-artifact ma-v2-c"><circle cx="170" cy="143" r="32" fill="#e8f7f3" stroke="#238875" stroke-width="2"/><path d="M170 122v22m0 10v2" stroke="#238875" stroke-width="6" stroke-linecap="round"/></g>
 </g></svg>'''
 return ('<figure class="ma-v2-magic" aria-label="'+e(d['magic_alt'])+'">'
         '<div class="ma-v2-magic-stage">'+scene+'</div>'
         '<div class="ma-v2-magic-steps">'+''.join('<span>'+e(t)+'</span>' for t in d['magic_steps'])+'</div>'
         '<figcaption>'+e(d['magic_note'])+'</figcaption>'
         '<button type="button" hidden class="ma-v2-motion-toggle" data-ma-v2-motion-control '
         'aria-pressed="false" aria-label="'+e(d['pause'])+'" '
         'data-pause="'+e(d['pause'])+'" data-play="'+e(d['play'])+'" '
         'data-pause-short="'+e(d['pause_short'])+'" data-play-short="'+e(d['play_short'])+'">'
         +e(d['pause_short'])+'</button></figure>')

def render(loc,cards,brain,academy_cards):
 d=PAGES[loc]
 hero=(
 '<section data-ma-v2-section="hero" class="ma-v2-hero" aria-labelledby="ma-v2-heading">'
 '<div class="ma-v2-hero-copy"><p class="ma-v2-kicker">'+e(d["eyebrow"])+'</p>'
 '<h1 id="ma-v2-heading">'+e(d["h1"])+'</h1>'
 '<p class="ma-v2-lead">'+e(d["lead"])+'</p>'
 '<div class="ma-v2-actions">'
 '<a class="ma-v2-primary" href="'+e(cards[2][0])+'">'+e(d["primary"])+' <span aria-hidden="true">↗</span></a>'
 '<a class="ma-v2-secondary" href="'+e(brain)+'">'+e(d["secondary"])+' <span aria-hidden="true">↗</span></a>'
 '</div></div>'+magic_box(loc)+'</section>'
 )
 # Transfer the native Academy HTML verbatim; add only a stable test marker
 # to each source <article>. The same markup and CSS power both locations.
 cards_html=[]
 for i,source in enumerate(academy_cards,1):
  if not re.match(r'<article\b',source,re.I):
   raise RuntimeError("Academy source card is not an article")
  cards_html.append(re.sub(r'<article\b',
      '<article data-ma-v2-card="'+str(i)+'"',source,count=1,flags=re.I))
 featured=(
 '<section data-ma-v2-section="courses" class="ma-v2-courses" aria-labelledby="ma-v2-courses-title">'
 '<div class="ma-v2-section-head"><span class="ma-v2-section-id">01 / ACADEMY</span>'
 '<h2 id="ma-v2-courses-title">'+e(d["featured"])+'</h2><p>'+e(d["featured_lead"])+'</p></div>'
 '<div class="ma-course-grid ma-v2-native-grid">'+''.join(cards_html)+'</div>'
 '<a class="ma-v2-academy-link" href="'+e(academy_path(loc))+'">'+e(d["academy"])+' <span aria-hidden="true">↗</span></a></section>'
 )
 teacher=link('it',TEACHING_IT.split('it/',1)[1])
 professional=BASE+PROF[loc]+'/'
 filepaths=[(teacher,"Teaching Lab"),(professional,"Professional safety")]
 focus=(
 '<section data-ma-v2-section="audiences" class="ma-v2-focus" aria-labelledby="ma-v2-focus-title">'
 '<div class="ma-v2-section-head"><span class="ma-v2-section-id">02 / MANZO AI</span>'
 '<h2 id="ma-v2-focus-title">'+e(d["focus_title"])+'</h2><p>'+e(d["focus_intro"])+'</p></div>'
 '<div class="ma-v2-focus-grid">'
 '<a class="ma-v2-focus-card ma-v2-focus-teacher" href="'+e(teacher)+'">'
 '<span class="ma-v2-focus-label">AI TEACHING LAB</span><h3>'+e(d["teacher"])+'</h3>'
 '<p>'+e(d["teacher_text"])+'</p>'
 '<small>'+e(d["teacher_note"])+'</small>'
 '<strong>'+e(d["teacher_cta"])+' <span aria-hidden="true">↗</span></strong></a>'
 '<a class="ma-v2-focus-card ma-v2-focus-pro" href="'+e(professional)+'">'
 '<span class="ma-v2-focus-label">AI / GOVERNANCE</span><h3>'+e(d["professional"])+'</h3>'
 '<p>'+e(d["professional_text"])+'</p>'
 '<strong>'+e(d["professional_cta"])+' <span aria-hidden="true">↗</span></strong></a>'
 '</div></section>'
 )
 challenge_section=(
 '<section data-ma-v2-section="challenge" class="ma-v2-challenge" aria-labelledby="ma-v2-challenge-title">'
 '<div><span class="ma-v2-section-id">'+e(d["challenge_eyebrow"])+'</span>'
 '<h2 id="ma-v2-challenge-title">'+e(d["challenge"])+'</h2>'
 '<p>'+e(d["challenge_text"])+'</p></div>'
 '<a href="'+e(brain)+'">'+e(d["challenge_cta"])+' <span aria-hidden="true">↗</span></a></section>'
 )
 closing=(
 '<section data-ma-v2-section="closing" class="ma-v2-closing" aria-labelledby="ma-v2-closing-title">'
 '<div><h2 id="ma-v2-closing-title">'+e(d["closing"])+'</h2>'
 '<p>'+e(d["closing_text"])+'</p></div>'
 '<div class="ma-v2-closing-links">'
 '<a href="'+e(link(loc,ABOUT[loc]))+'">'+e(d["about"])+' ↗</a>'
 '<a href="'+e(academy_path(loc))+'">'+e(d["academy"])+' ↗</a></div></section>'
 )
 return hero+featured+focus+challenge_section+closing

def add_academy_index(site,loc,extras,css_hash):
 target=file_for(site,academy_path(loc))
 html=target.read_text(encoding="utf-8")
 if 'data-ma-v2-academy="preview"' in html:
  raise RuntimeError("Repeated Academy augmentation "+loc)
 m=list(END_MAIN.finditer(html))
 if len(m)!=1:raise RuntimeError("Academy must have one main closing tag "+loc)
 d=PAGES[loc]
 markup=(
 '<section class="ma-v2-academy-index" data-ma-v2-academy="preview" '
 'aria-labelledby="ma-v2-extra-title-'+loc+'">'
 '<div class="ma-v2-academy-intro"><h2 id="ma-v2-extra-title-'+loc+'">'+e(d["extra"])+'</h2>'
 '<p>'+e(d["extra_lead"])+'</p></div>'
 '<div class="ma-v2-extra-grid">'
 +''.join('<a href="'+e(h)+'" class="ma-v2-extra-link">'
          '<span>'+e(name)+'</span><span aria-hidden="true">↗</span></a>' for h,name in extras)
 +'</div></section>'
 )
 pos=m[0].start()
 if html.count('</head>')!=1:raise RuntimeError("Academy missing unique head close "+loc)
 html=html.replace('</head>',f'<link rel="stylesheet" data-ma-v2-academy-style="preview" href="{BASE}assets/{CSS.name}?v={css_hash}"></head>',1)
 target.write_text(html.replace('</main>',markup+'</main>',1),encoding="utf-8")

def patch_meta(html,d):
 title=re.compile(r'(<title\b[^>]*>).*?(</title>)',re.I|re.S)
 if len(title.findall(html))!=1:raise RuntimeError("Page title not unique")
 html=title.sub(lambda m:m.group(1)+e(d["title"])+m.group(2),html,count=1)
 # Attribute-order independent match for named meta tags.
 for attribute,value in (("name","description"),("property","og:title"),("property","og:description"),
                         ("name","twitter:title"),("name","twitter:description")):
  pattern=re.compile(r'<meta\b(?=[^>]*\b'+attribute+r'=["\']'+re.escape(value)+r'["\'])[^>]*>',re.I)
  def change(m):
   text=m.group(0)
   replacement=d["desc"] if "description" in value else d["title"]
   if re.search(r'\bcontent=["\'][^"\']*["\']',text,re.I):
    return re.sub(r'\bcontent=["\'][^"\']*["\']','content="'+e(replacement)+'"',text,count=1,flags=re.I)
   return text[:-1]+' content="'+e(replacement)+'">'
  html=pattern.sub(change,html,count=1)
 return html

def publish(site,verify=False):
 if not CSS.is_file() or not JS.is_file():raise RuntimeError("Missing Home magic sources")
 css_hash=hashlib.sha256(CSS.read_bytes()).hexdigest()[:12]
 js_hash=hashlib.sha256(JS.read_bytes()).hexdigest()[:12]
 for locale in LOCALES:
  path=site/locale/"index.html"
  if not path.is_file():raise RuntimeError("Home absent "+locale)
  html=path.read_text(encoding="utf-8")
  if verify:
   if html.count(MARKER)!=1:raise RuntimeError("Missing preview marker "+locale)
   if html.count(SECTION_TAG)!=5:raise RuntimeError("Five-section contract changed "+locale)
   if len(re.findall(r'<h1\b',html,re.I))!=1:raise RuntimeError("Home H1 count changed "+locale)
   if len(re.findall(r'data-ma-v2-card="[1-6]"',html))!=6:raise RuntimeError("Six featured cards missing "+locale)
   # Confirm the Home contains the actual Academy component, not the retired mock.
   home_articles=CARD.findall(html)
   original_articles=academy_card_markup(site,locale)
    if len(home_articles)!=6 or any('class="ma-v2-course' in card for card in home_articles):
     raise RuntimeError("Home did not use six native Academy components "+locale)
   for i,(home_card,academy_card) in enumerate(zip(home_articles,original_articles),1):
    expected=re.sub(r'<article\b',
     '<article data-ma-v2-card="'+str(i)+'"',academy_card,count=1,flags=re.I)
    if home_card!=expected:
     raise RuntimeError(f"{locale}: Home Academy card {i} markup diverges from source")
   if html.count('ma-course-grid ma-v2-native-grid')!=1:
    raise RuntimeError("Native Academy card grid is missing "+locale)
   if f'{BASE}assets/learning-experience/guide.css' not in html:
    raise RuntimeError("Native Academy styling absent from Home "+locale)
   # SVG painter order is significant: the lid must not obscure the emerging symbols.
   box_start=html.find('<g class="ma-v2-box">')
   symbols_start=html.find('<g class="ma-v2-artifacts">')
   if box_start<0 or symbols_start<=box_start:
    raise RuntimeError("Magic-box artwork must render emerging symbols above the lid "+locale)
   for file in (CSS.name,JS.name):
    if file not in html:raise RuntimeError("Asset not linked "+locale+" "+file)
   ai=file_for(site,academy_path(locale)).read_text(encoding="utf-8")
   if ai.count('data-ma-v2-academy="preview"')!=1 or ai.count('class="ma-v2-extra-link"')!=7:
    raise RuntimeError("Seven added courses not discoverable in Academy "+locale)
   for target in re.findall(r'<a\b[^>]*href=["\']([^"\']+)["\']',html,re.I):
    if target.startswith(BASE):
     file_for(site,unescape(target))
   continue
  if MARKER in html:raise RuntimeError("Home magic overlay already exists "+locale)
  canonical=target_cards(site,locale)
  # The Academy card CSS must be shared, not recreated with Home-only effects.
  if not (site/"assets/learning-experience/guide.css").is_file():
   raise RuntimeError("Approved Academy stylesheet not staged "+locale)
  extended=extra_cards(site,locale,html)
  if {href for href,_ in canonical}&{href for href,_ in extended}:
   raise RuntimeError("Duplicate existing Academy and extra course route "+locale)
  brain=challenge(site,locale,html)
  for href in (BASE+PROF[locale]+'/', BASE+TEACHING_IT+'/', link(locale,ABOUT[locale])):
   file_for(site,href)
  opening=MAIN.search(html)
  closings=list(END_MAIN.finditer(html))
  if not opening or len(closings)!=1 or closings[0].start()<opening.end():
   raise RuntimeError("Expected one distinct main wrapper; leave language UI safe")
  before=html[:opening.end()];after=html[closings[0].start():]
  # Topbar/sidebar are before the main tag, the footer is after it.
  if '<aside class="rail" id="rail">' not in before or '<header class="topbar">' not in before:
   raise RuntimeError("Site's sidebar/topbar layout changed; refusing to replace "+locale)
  if '<footer class="site-footer">' not in after:
   raise RuntimeError("The original footer was not preserved "+locale)
  # Only the generic topbar descriptor changes per locale; language UI is immutable.
  original_label='<span class="top-label">Knowledge & Prompt Lab</span>'
  if before.count(original_label)!=1:raise RuntimeError("Unexpected topbar descriptor "+locale)
  before=before.replace(original_label,'<span class="top-label">'+e(PAGES[locale]["lab_label"])+'</span>',1)
  inner=render(locale,canonical,brain,academy_card_markup(site,locale))
  new=before+inner+after
  new=patch_meta(new,PAGES[locale])
  assets=(
   '<link rel="stylesheet" data-ma-home-v2="preview" '
   f'href="{BASE}assets/{CSS.name}?v={css_hash}">'
   '<script defer data-ma-home-v2-script="preview" '
   f'src="{BASE}assets/{JS.name}?v={js_hash}"></script>'
  )
  new,num=END_HEAD.subn(assets+'</head>',new,count=1)
  if num!=1:raise RuntimeError("Missing head close "+locale)
  # Sidebar, language controls and footer remain untouched.
  if '<aside class="rail" id="rail">' not in new or '<footer class="site-footer">' not in new:
   raise RuntimeError("Lost site chrome")
  path.write_text(new,encoding="utf-8")
  add_academy_index(site,locale,extended,css_hash)
 if not verify:
  target=site/"assets"
  target.mkdir(exist_ok=True,parents=True)
  shutil.copyfile(CSS,target/CSS.name)
  shutil.copyfile(JS,target/JS.name)
  publish(site,verify=True)
 else:
  for source in (CSS,JS):
   if (site/"assets"/source.name).read_bytes()!=source.read_bytes():
    raise RuntimeError("Staged asset does not match tested source "+source.name)
  print("PASS Home: IT/EN/ES, five sections, six EXACT native Academy components + shared stylesheet, seven further Academy paths; original language menu/sidebar/footer untouched.")

if __name__=="__main__":
 parser=argparse.ArgumentParser()
 parser.add_argument("--site",required=True,type=Path)
 parser.add_argument("--verify-only",action="store_true")
 args=parser.parse_args()
 publish(args.site,args.verify_only)
