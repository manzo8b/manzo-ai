#!/usr/bin/env python3
"""MANZO AI · Coursera-informed learning guidance for two EXISTING courses.

No content or quiz mutation: source syllabus drives a contextual learning map.
This is an original UX adaptation, not Coursera UI or proprietary content.
No accounts, progress storage, tracking or certificates are added.
"""
from __future__ import annotations

import argparse
from html import escape
import hashlib
import json
from pathlib import Path
import re
import shutil

ROOT=Path(__file__).resolve().parent.parent
SOURCE=ROOT/'product'/'learning-experience'
ORIGINAL=ROOT/'editorial'/'learning'/'hallucinations'
ROUTES={
 'it':('it/impara/allucinazioni-ai-verificabilita','it/impara/allucinazioni-ai-verificabilita/coding'),
 'en':('en/learn/ai-hallucinations-verification','en/learn/ai-hallucinations-verification/coding'),
 'es':('es/aprende/alucinaciones-ia-verificacion','es/aprende/alucinaciones-ia-verificacion/coding'),
}
MARKER='data-ma-learning-guide="v1"'
CSS='/manzo-ai/assets/learning-experience/guide.css'
JS='/manzo-ai/assets/learning-experience/guide.js'

def esc(x): return escape(str(x),quote=True)
def json_script(x):
 return json.dumps(x,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')

def roadmap(d,modules,kind,lang,main_route):
 label=d['moduleLabel'] if kind=='core' else d['codingLabel']
 result=[]
 for i,item in enumerate(modules,1):
  anchor=f'ma-learn-unit-{i}' if kind=='core' else f'hc-section-{i:02}'
  title=item['title']
  duration=item.get('duration','')
  badge=f'<span class="ma-unit-time">{esc(duration)}</span>' if duration else ''
  result.append(
    f'<li class="ma-unit" data-ma-unit="{i}"><a href="#{anchor}" class="ma-unit-link">'
    f'<span class="ma-unit-num">{i:02}</span><span class="ma-unit-copy">'
    f'<strong>{esc(title)}</strong>{badge}</span><span class="ma-unit-arrow" aria-hidden="true">↗</span></a>'
    f'<button type="button" class="ma-mark" data-ma-mark="{i}" aria-pressed="false"'
    f' aria-label="{esc(d["mark"])}: {esc(title)}"><span aria-hidden="true">○</span>{esc(d["mark"])}</button>'
    f'</li>'
  )
 return ''.join(result)

def guide(d,modules,kind,locale,main_route):
 count=len(modules)
 outcomes=d['coreOutcomes'] if kind=='core' else d['codingOutcomes']
 navigation=(
  [('hx-program',d['content']),('hx-lab',d['practiceLabel']),('hx-quiz',d['quizLabel']),
   ('hx-crossword',d['crosswordLabel']),('hx-sources',d['sources'])]
  if kind=='core' else
  [('hc-lesson',d['content']),('hc-lab',d['practiceLabel']),('hc-quiz',d['quizLabel']),
   ('hc-gate',d['assessment']),('hc-sources',d['sources'])]
 )
 steps=''.join(
  f'<a href="#{esc(anchor)}">{esc(title)} <span aria-hidden="true">↗</span></a>'
  for anchor,title in navigation
 )
 goals=''.join(f'<li>{esc(outcome)}</li>' for outcome in outcomes)
 content=roadmap(d,modules,kind,locale,main_route)
 back=(f'<a class="ma-guide-back" href="/manzo-ai/{esc(main_route)}/">'
       f'{esc(d["previous"])} <span aria-hidden="true">↗</span></a>') if kind=='coding' else ''
 return f'''<section {MARKER} class="ma-guidance" id="ma-guide" data-ma-guide-kind="{kind}">
 <div class="ma-guidance-inner">
  <div class="ma-guide-head">
   <div><p class="ma-guide-kicker">{esc(d['name'])}</p>
   <h2>{esc(d['title'])}</h2><p>{esc(d['description'])}</p></div>
   <div class="ma-guide-identity"><span>MANZO AI</span><strong>LEARNING</strong><small>PATH / {count:02}</small></div>
  </div>
  <div class="ma-guide-outcomes">
   <div><p class="ma-guide-overline">{esc(d['objectives'])}</p>
   <ul>{goals}</ul></div>
   <div class="ma-guide-key"><strong>{count:02}</strong><span>{esc(d['moduleLabel'] if kind=='core' else d['codingLabel'])}</span>
   <small>{esc(d['detail'])}</small>{back}</div>
  </div>
  <div class="ma-guide-shell">
   <div class="ma-outline">
    <div class="ma-outline-header"><h3>{esc(d['outline'])}</h3><span>{count:02}</span></div>
    <ol class="ma-units">{content}</ol>
   </div>
   <aside class="ma-study-panel" aria-label="{esc(d['guide'])}">
    <span class="ma-panel-top">{esc(d['guide'])}</span>
    <div class="ma-progress-number"><strong id="ma-progress-current">0</strong><span>/ {count:02}</span></div>
    <p class="ma-progress-label">{esc(d['progress'])}</p>
    <div class="ma-progress-track" role="progressbar" aria-label="{esc(d['progress'])}" aria-valuemin="0" aria-valuemax="{count}" aria-valuenow="0">
     <span id="ma-progress-fill"></span></div>
    <a href="#{ 'ma-learn-unit-1' if kind=='core' else 'hc-section-01'}" class="ma-continue" id="ma-continue">{esc(d['continue'])}<span aria-hidden="true">↗</span></a>
    <button type="button" class="ma-reset" id="ma-reset">{esc(d['reset'])}</button>
    <p class="ma-progress-disclosure">{esc(d['progressNote'])}</p>
   </aside>
  </div>
  <nav class="ma-next-steps" aria-label="{esc(d['practice'])}">
   <span>{esc(d['practice'])} / {esc(d['assessment'])}</span>{steps}
  </nav>
  <p class="ma-guide-notice">{esc(d['noCertificate'])} · {esc(d['assessmentNote'])}</p>
 </div>
 <script type="application/json" id="ma-learning-labels">{json_script(d)}</script>
 </section>'''

def inject(page,kind,loc,d,modules,main_route):
 original=page.read_text(encoding='utf-8')
 if MARKER in original:
  raise RuntimeError('Guidance already injected in '+str(page))
 if kind=='core':
  if original.count('class="hx-module"')!=6:raise RuntimeError('Expected exactly six course modules '+str(page))
  counter=[0]
  def renumber(match):
   counter[0]+=1
   return f'<article class="hx-module" id="ma-learn-unit-{counter[0]}">'
  html=re.sub(r'<article class="hx-module">',renumber,original)
  target='<section class="hx-section" id="hx-program">'
  if target not in html: raise RuntimeError('No program target '+str(page))
 else:
  html=original
  for i in range(1,7):
   if f'id="hc-section-{i:02}"' not in html:raise RuntimeError('Missing coding chapter '+str(i))
  target='<div class="hc-body" id="hc-lesson">'
  if target not in html:raise RuntimeError('No coding lesson target '+str(page))
 html=html.replace(target,guide(d,modules,kind,loc,main_route)+target,1)
 # Existing pages have a single </head>, so add assets using a reversible marker.
 head=re.search(r'</head\s*>',html,re.I)
 if head is None:raise RuntimeError('No html head')
 tag=f'<link rel="stylesheet" data-ma-learning-assets="1" href="{CSS}">'
 tag+=f'<script defer src="{JS}"></script>'
 html=html[:head.start()]+tag+html[head.start():]
 page.write_text(html,encoding='utf-8')

def publish(site,verify_only=False):
 locales=json.loads((SOURCE/'labels.json').read_text(encoding='utf-8'))
 if set(locales)!=set(ROUTES):raise RuntimeError('Incomplete translation dictionaries')
 assets=site/'assets'/'learning-experience'
 if not verify_only:
  assets.mkdir(parents=True,exist_ok=True)
  for name in ('guide.css','guide.js'):
   shutil.copyfile(SOURCE/name,assets/name)
 for name in ('guide.css','guide.js'):
  if (assets/name).read_bytes()!=(SOURCE/name).read_bytes():raise RuntimeError('Asset missing '+name)
 reviewed=0
 for loc,(base,coding) in ROUTES.items():
  d=locales[loc]
  core=json.loads((ORIGINAL/f'{loc}.json').read_text(encoding='utf-8'))
  code=json.loads((ORIGINAL/f'coding-{loc}.json').read_text(encoding='utf-8'))
  expected=((base,'core',core['modules']),(coding,'coding',code['chapters']))
  for route,kind,modules in expected:
   page=site/route/'index.html'
   if not page.is_file():raise RuntimeError('Missing course '+route)
   if len(modules)!=6:raise RuntimeError('Unexpected six-course outline '+route)
   if not verify_only:inject(page,kind,loc,d,modules,base)
   html=page.read_text(encoding='utf-8')
   if html.count(MARKER)!=1 or html.count('data-ma-unit=')!=6:
    raise RuntimeError('Missing/duplicate guidance '+route)
   if html.count('data-ma-mark=')!=6:raise RuntimeError('Incomplete check buttons '+route)
   if 'id="hx-quiz-data"' not in html and kind=='core':raise RuntimeError('Existing quiz vanished')
   if 'id="hc-quiz-data"' not in html and kind=='coding':raise RuntimeError('Existing coding quiz vanished')
   for i in range(1,7):
    anchor=f'ma-learn-unit-{i}' if kind=='core' else f'hc-section-{i:02}'
    if f'id="{anchor}"' not in html:raise RuntimeError('Broken module anchor '+anchor)
   reviewed+=1
 print(f'MANZO AI guided learning: {reviewed} pages, 3 locales, 12 maps + in-memory study progress; verify_only={verify_only}')

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--site',type=Path,required=True)
 p.add_argument('--verify-only',action='store_true')
 a=p.parse_args()
 publish(a.site,a.verify_only)
