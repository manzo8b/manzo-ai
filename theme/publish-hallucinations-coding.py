#!/usr/bin/env python3
"""MANZO AI: publish a trilingual long-form coding assurance module.
Run after publish-hallucinations.py and before SEO + navigation overlays.
The ZIP remains immutable. No client data or analytics.
"""
from __future__ import annotations
import argparse
from html import escape
import json
from pathlib import Path
import re
import shutil

ROOT=Path(__file__).resolve().parent.parent
SRC=ROOT/'editorial'/'learning'/'hallucinations'
BASE='/manzo-ai/'
ROUTES={
 'it':'it/impara/allucinazioni-ai-verificabilita/coding',
 'en':'en/learn/ai-hallucinations-verification/coding',
 'es':'es/aprende/alucinaciones-ia-verificacion/coding'
}
PARENTS={
 'it':'it/impara/allucinazioni-ai-verificabilita',
 'en':'en/learn/ai-hallucinations-verification',
 'es':'es/aprende/alucinaciones-ia-verificacion'
}
SOURCE_DOCS=[
 ('F9','GitHub Docs','Review AI-generated code','https://docs.github.com/en/copilot/tutorials/review-ai-generated-code'),
 ('F10','OWASP GenAI Security Project','LLM05:2025 — Improper Output Handling','https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/'),
 ('F11','NIST · SP 800-218 (2022)','Secure Software Development Framework (SSDF) v1.1','https://csrc.nist.gov/pubs/sp/800/218/final'),
 ('F12','Spracklen et al. · USENIX Security 2025','We Have a Package for You!','https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen'),
]
def e(x):
 return escape(str(x),quote=True)
def safe_json(x):
 return json.dumps(x,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
def validate(d,loc):
 assert d['locale']==loc
 assert len(d['chapters'])==6
 assert len(d['pipeline'])==5
 assert len(d['gates'])==8
 assert len(d['cases'])==4
 assert len(d['quiz'])==4
 assert [x['id'] for x in d['chapters']]==['01','02','03','04','05','06']
 assert all(len(v['paragraphs'])>=3 for v in d['chapters'])
 assert all(150<=len(x['paragraphs'][0]) for x in d['chapters'])
 for q in d['quiz']:
  assert len(q['options'])==4 and 0<=q['answer']<4 and q['why']
 assert set(d['sources'])=={x[0] for x in SOURCE_DOCS}
 return d
def refs(keys):
 return ' '.join(f'<a href="#hc-{e(key.lower())}">[{e(key)}]</a>' for key in keys)
def html_page(loc,d):
 h=d['labels']
 route=BASE+ROUTES[loc]+'/'
 parent=BASE+PARENTS[loc]+'/'
 canonical='https://manzo8b.github.io'+route
 alters=''.join(f'<link rel="alternate" hreflang="{l}" href="https://manzo8b.github.io{BASE}{path}/">' for l,path in ROUTES.items())
 langs=''.join(f'<a href="{BASE}{ROUTES[l]}/" hreflang="{l}" lang="{l}"'+(' aria-current="page"' if l==loc else '')+f'>{l.upper()}</a>' for l in ROUTES)
 schema={'@context':'https://schema.org','@type':'LearningResource','name':d['title'],'description':d['lead'],
   'inLanguage':loc,'isAccessibleForFree':True,'educationalLevel':'Professional',
   'datePublished':'2026-11-15','dateModified':'2026-11-15',
   'author':{'@type':'Person','name':'Marcelo Fernandez'},
   'publisher':{'@type':'Organization','name':'MANZO AI'},
   'isPartOf':{'@type':'Course','name':'AI Hallucinations & Output Verification','url':'https://manzo8b.github.io'+parent},
   'url':canonical,'citation':[url for _,_,_,url in SOURCE_DOCS]}
 parts=[f'''<!doctype html><html lang="{loc}"><head><meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{e(d['title'])} | MANZO AI Engineering Assurance</title>
  <meta name="description" content="{e(d['subtitle']+' — '+d['lead'][:120])}">
  <meta name="robots" content="index,follow"><meta name="theme-color" content="#ffffff">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{e(d['title'])}">
  <meta property="og:description" content="{e(d['lead'][:160])}">
  <meta property="og:url" content="{e(canonical)}">
  <link rel="canonical" href="{e(canonical)}">{alters}
  <link rel="alternate" hreflang="x-default" href="https://manzo8b.github.io{BASE}{ROUTES['it']}/">
  <link rel="stylesheet" href="{BASE}assets/learning/hallucinations/course.css">
  <link rel="stylesheet" href="{BASE}assets/learning/hallucinations/coding.css">
  <script src="{BASE}assets/learning/hallucinations/coding.js" defer></script>
  <script type="application/ld+json">{safe_json(schema)}</script>
  </head><body class="hx-page hc-page" data-hc-module="v1">
  <a class="hx-skip" href="#hc-main">Skip to content / Vai al contenuto</a>
  <header class="hx-header"><div class="hx-wrap hx-head-inner">
  <a class="hx-logo" href="{BASE}{loc}/"><img src="{BASE}assets/manzo-mark.svg" alt="">MANZO <i>AI</i></a>
  <nav class="hx-nav" aria-label="Engineering Assurance">
  <a class="hx-navlink" href="#hc-lesson">{e(h['program'])}</a>
  <a class="hx-navlink" href="#hc-lab">{e(h['cases'])}</a>
  <a class="hx-navlink" href="#hc-gate">{e(h['gate'])}</a>
  <a class="hx-navlink" href="#hc-sources">{e(h['sources'])}</a>
  <span class="hx-langs">{langs}</span></nav></div></header>
  <main id="hc-main"><section class="hc-hero"><div class="hc-content">
  <p class="hx-kicker">{e(d['eyebrow'])}</p><h1>{e(d['title'])}</h1>
  <p class="hc-hero-lead">{e(d['lead'])}</p><p class="hc-thesis">{e(d['thesis'])}</p>
  <div class="hc-utility"><a class="hx-btn hx-btn-primary" href="#hc-lesson">{e(h['program'])} ↗</a>
  <a class="hx-btn" href="{e(parent)}">{e(h['home'])} ↗</a></div>
  <div class="hc-pills"><span>{e(h['time'])}</span><span>4 CASE STUDIES</span><span>4 REVIEW DECISIONS</span></div>
  </div></section><div class="hc-body" id="hc-lesson"><div class="hc-content">''']
 for ch in d['chapters']:
  parts.append(f'''<section class="hc-section" id="hc-section-{e(ch['id'])}">
  <aside class="hc-side"><p class="hc-id">{e(ch['id'])}</p><p class="hc-eyebrow">{e(d['eyebrow'])}</p></aside>
  <article class="hc-prose"><h2>{e(ch['title'])}</h2><p class="hc-deck">{e(ch['deck'])}</p>''')
  parts.extend('<p>'+e(p)+'</p>' for p in ch['paragraphs'])
  if 'points' in ch:
   parts.append('<div class="hc-taxonomy">')
   for title,desc in ch['points']:
    parts.append(f'<article><strong>{e(title)}</strong><p>{e(desc)}</p></article>')
   parts.append('</div>')
  parts.append(f'<aside class="hc-evidence">{e(ch["note"])} <span>{refs(ch["refs"])}</span></aside></article></section>')
  if ch['id']=='03':
   ex=d['codeExample']
   parts.append(f'''<div class="hc-code-panel"><header><h3>{e(ex['title'])}</h3><p>{e(ex['context'])}</p></header>
   <div class="hc-code-grid"><div class="hc-code-block"><strong>INPUT · UNVERIFIED</strong><pre><code>{e(ex['before'])}</code></pre></div>
   <div class="hc-code-block"><strong>REVIEW · PARTIAL FIX</strong><pre><code>{e(ex['after'])}</code></pre></div></div>
   <footer>{e(ex['takeaway'])}</footer></div>
   <div class="hc-banner"><p class="hc-eyebrow" style="color:#aed4f6">{e(h['impact'])}</p>
   <h2>{e(h['riskTitle'])}</h2><p>{e(ch['deck'])}</p>
   <div class="hc-pipeline">''')
   for number,title,desc in d['pipeline']:
    parts.append(f'<div class="hc-stage"><small>{e(number)}</small><strong>{e(title)}</strong><p>{e(desc)}</p></div>')
   parts.append('</div></div>')
  if ch['id']=='05':
   parts.append(f'''<section id="hc-gate" style="scroll-margin-top:90px">
     <h2 style="font-size:clamp(1.8rem,3vw,2.6rem);letter-spacing:-.05em">{e(h['gate'])}</h2>
     <p style="max-width:740px;color:#536d83">{e(h['principle'])}. {e(ch['note'])}</p>
     <div class="hc-steps">''')
   for title,desc in d['gates']:
    parts.append(f'''<label class="hc-gate"><input type="checkbox" data-hc-gate="1">
      <span><b>{e(title)}</b><em>{e(desc)}</em></span></label>''')
   parts.append('<div class="hc-gate-status" data-hc-gate-status aria-live="polite"></div></div></section>')
 parts.append(f'''</div></div><section class="hc-lab" id="hc-lab"><div class="hc-content">
 <div class="hx-headline"><p class="hx-kicker">{e(h['cases'])}</p><h2>{e(h['quizLabel'])}</h2>
 <p>{e(h['quizLead'])}</p></div><div class="hc-card-grid">''')
 for i,case in enumerate(d['cases'],1):
  parts.append(f'''<article class="hc-case" data-hc-case="1"><span class="hc-case-kicker">SCENARIO {i:02d} · {e(case['sector'])}</span>
  <h3>{e(case['title'])}</h3><p class="hc-scene">{e(case['scenario'])}</p>
  <p><strong>{e(case['task'])}</strong></p>
  <label for="hc-response-{i}">{e(h['casePrompt'])}</label>
  <textarea id="hc-response-{i}" rows="4" maxlength="5000"></textarea>
  <div class="hc-utility"><button class="hx-btn" type="button" data-hc-review disabled>{e(h['reveal'])}</button></div>
  <span class="hc-help" data-hc-help>{e(h['min'])}</span>
  <div class="hc-answer" data-hc-solution hidden>{e(case['solution'])}</div></article>''')
 parts.append(f'''</div></div></section>
 <section class="hc-assessment" id="hc-quiz"><div class="hc-content">
 <div class="hx-headline"><p class="hx-kicker">{e(h['quizLabel'])}</p>
 <h2>{e(h['quizLabel'])}</h2><p>{e(h['quizLead'])}</p></div>
 <div class="hc-quiz-shell"><div class="hc-quiz-meter" aria-hidden="true"><span data-hc-bar></span></div>
 <p class="hc-eyebrow" data-hc-position>1 / 4</p><div data-hc-question aria-live="polite"></div>
 <div data-hc-feedback class="hc-quiz-feedback" role="status" hidden></div>
 <div data-hc-result class="hc-quiz-feedback" aria-live="polite" hidden></div>
 <div class="hc-utility"><button type="button" class="hx-btn hx-btn-primary" data-hc-submit>{e(h['check'])}</button>
 <button type="button" class="hx-btn" data-hc-next hidden>{e(h['next'])}</button></div></div></div></section>''')
 parts.append(f'''<section class="hx-section hx-tint" id="hc-sources"><div class="hc-content">
 <div class="hx-headline"><p class="hx-kicker">{e(h['sources'])}</p>
 <h2>{e(h['sources'])}</h2><p>{e(h['sourceNote'])}</p></div><div class="hc-refs">''')
 for ref,publisher,title,url in SOURCE_DOCS:
  parts.append(f'''<a id="hc-{e(ref.lower())}" class="hc-ref" href="{e(url)}" target="_blank" rel="noopener noreferrer">
  <b>{e(ref)} · {e(publisher)} ↗</b><small>{e(title)}</small></a>''')
 parts.append(f'''</div><p class="hc-disclaimer">{e(h['sourceNote'])}</p></div></section></main>
 <footer class="hx-foot"><div class="hx-wrap"><strong>{e(h['principle'])}</strong>
 <p>{e(h['sourceNote'])}</p>
 <a href="{e(parent)}">{e(h['back'])} ↗</a></div></footer>
 <script type="application/json" id="hc-quiz-data">{safe_json(d['quiz'])}</script>
 <script type="application/json" id="hc-labels">{safe_json({**h,'gateReminder':{
 'it':'Selezionare una casella non costituisce prova di esecuzione: allegare i risultati.',
 'en':'Ticking a box is not evidence of execution; attach the actual results.',
 'es':'Marcar una casilla no demuestra que el control se haya ejecutado; hay que adjuntar resultados.'}[loc],
 'choose':{'it':'Seleziona una risposta.','en':'Choose one option.','es':'Selecciona una opción.'}[loc],
 'correct':{'it':'Corretta','en':'Correct','es':'Correcta'}[loc],
 'wrong':{'it':'Da rivedere','en':'Review required','es':'Revisar'}[loc]
 })}</script></body></html>''')
 return ''.join(parts)

def link_to_course(page,loc,d):
 if not page.exists():raise RuntimeError('Missing core course '+str(page))
 s=page.read_text(encoding='utf-8')
 marker='data-hc-coding-chapter="1"'
 if marker in s:return
 label=d['title'];link=BASE+ROUTES[loc]+'/'
 card=f'''<section {marker} style="max-width:1150px;margin:50px auto;padding:clamp(27px,4vw,55px);border-radius:27px;background:linear-gradient(125deg,#edf7ff,#f5f8ff);border:1px solid #d5e5f2;color:#143a62">
  <p style="text-transform:uppercase;letter-spacing:.14em;font-size:.78rem;font-weight:800;color:#366aaa;margin:0 0 12px">{e(d['eyebrow'])}</p>
  <h2 style="font-size:clamp(1.9rem,4vw,3rem);color:#173d68;letter-spacing:-.055em;line-height:1.13;margin:0 0 16px">{e(label)}</h2>
  <p style="font-size:1.02rem;line-height:1.7;max-width:830px;margin-bottom:20px">{e(d['subtitle'])}. {e(d['lead'])}</p>
  <a href="{e(link)}" style="display:inline-flex;padding:13px 22px;background:#174d8a;border-radius:13px;color:#fff;text-decoration:none;font-weight:700">{e(d['labels']['program'])} ↗</a></section>'''
 where=re.search(r'<section[^>]*class="hx-section hx-peach"[^>]*id="hx-method"',s,re.I)
 if not where:raise RuntimeError('Main course method insertion anchor not found: '+str(page))
 s=s[:where.start()]+card+s[where.start():]
 page.write_text(s,encoding='utf-8')

def publish(site,verify_only=False):
 assets=site/'assets'/'learning'/'hallucinations'
 data={loc:validate(json.loads((SRC/f'coding-{loc}.json').read_text(encoding='utf-8')),loc) for loc in ROUTES}
 if not verify_only:
  assets.mkdir(parents=True,exist_ok=True)
  for name in ('coding.css','coding.js'):shutil.copyfile(SRC/name,assets/name)
  for loc,d in data.items():
   page=site/ROUTES[loc]/'index.html'
   page.parent.mkdir(parents=True,exist_ok=True)
   page.write_text(html_page(loc,d),encoding='utf-8')
   link_to_course(site/PARENTS[loc]/'index.html',loc,d)
 for name in ('coding.css','coding.js'):
  assert (assets/name).read_bytes()==(SRC/name).read_bytes()
 for loc,d in data.items():
  page=site/ROUTES[loc]/'index.html'
  assert page.is_file()
  html=page.read_text(encoding='utf-8')
  for token in ('data-hc-module','hc-quiz-data','data-hc-gate','data-hc-case','hc-sources','hreflang'):
   assert token in html,f'{loc} missing {token}'
  assert html.count('class="hc-section"')==6
  assert html.count('class="hc-case"')==4
  assert html.count('class="hc-ref"')==4
  assert (site/PARENTS[loc]/'index.html').read_text(encoding='utf-8').count('data-hc-coding-chapter="1"')==1
 print('MANZO AI Engineering Assurance: 3 languages, 6 editorial sections, 4 cases, 4 decision questions, 8 quality gates, 4 primary references; verify_only='+str(verify_only))

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--site',required=True,type=Path)
 p.add_argument('--verify-only',action='store_true')
 args=p.parse_args()
 publish(args.site,args.verify_only)
