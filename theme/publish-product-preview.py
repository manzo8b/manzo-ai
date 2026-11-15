#!/usr/bin/env python3
"""Publish MANZO AI Product Lab. Nontransactional, client-only preview.
No API, checkout, login, trackers, persistence or user-data transfer.
Run after other editorial overlays, before global SEO/navigation.
"""
from __future__ import annotations
from html import escape
import argparse
import json
from pathlib import Path
import re
import shutil

ROOT=Path(__file__).resolve().parent.parent
SRC=ROOT/'product'/'preview'
LOCALES=('it','en','es')
ROUTES={'it':'it/prodotto','en':'en/product','es':'es/producto'}
COURSES={
 'it':'it/impara/allucinazioni-ai-verificabilita',
 'en':'en/learn/ai-hallucinations-verification',
 'es':'es/aprende/alucinaciones-ia-verificacion'
}
BASE='/manzo-ai/'

def e(x):return escape(str(x),quote=True)

def safe_data(d):
 return json.dumps(d,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')

def validate(data):
 assert set(data)==set(LOCALES)
 for locale,d in data.items():
  assert len(d['cards'])==3
  assert len(d['readiness'])==6
  assert len(d['clientOptions'])==4
  assert len(d['sectorOptions'])==4
  assert len(d['moduleOptions'])==3
  for key in ('title','lead','studioTitle','verifyTitle','learningTitle','readinessTitle','disclaimer'):
   assert isinstance(d[key],str) and len(d[key])>3,f'{locale}: {key}'
 for locale,d in data.items():
  assert len(d['lead'])>50 and len(d['disclaimer'])>50, f'{locale}: missing substantive caveat'
 return data

def graphic():
 return '''<div class="meter-art" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 440">
 <defs><linearGradient id="glow" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#f7fbff"/><stop offset="1" stop-color="#e8f3ff"/></linearGradient></defs>
 <circle cx="220" cy="220" r="204" fill="url(#glow)" stroke="#dce9f5"/>
 <g class="meter-spin"><circle cx="220" cy="220" r="174" stroke="#8caed1" fill="none" stroke-width="1.8" stroke-dasharray="7 15"/><circle cx="394" cy="220" r="9" fill="#3979bc"/><circle cx="46" cy="220" r="5" fill="#72baa8"/></g>
 <g class="meter-spin reverse"><circle cx="220" cy="220" r="134" stroke="#a1d8d2" fill="none" stroke-width="1.6" stroke-dasharray="3 12"/><circle cx="220" cy="86" r="9" fill="#d78d7b"/><circle cx="220" cy="354" r="6" fill="#a2a1d9"/></g>
 <circle cx="220" cy="220" r="93" fill="white" stroke="#d4e5f1" stroke-width="2"/>
 <text x="220" y="212" text-anchor="middle" fill="#214d81" font-family="system-ui,sans-serif" font-size="33" font-weight="750">MANZO AI</text>
 <text x="220" y="242" text-anchor="middle" fill="#7390a8" font-family="system-ui,sans-serif" font-size="12" letter-spacing="3">PRODUCT LAB</text>
 </svg></div>'''

def html_page(loc,d):
 route=f'{BASE}{ROUTES[loc]}/'
 canonical='https://manzo8b.github.io'+route
 langs=''.join(f'<a href="{BASE}{ROUTES[l]}/" hreflang="{l}" lang="{l}"'+(' aria-current="page"' if l==loc else '')+f'>{l.upper()}</a>' for l in LOCALES)
 alternates=''.join(f'<link rel="alternate" hreflang="{l}" href="https://manzo8b.github.io{BASE}{ROUTES[l]}/">' for l in LOCALES)
 nav=''.join(f'<a href="#{tag}">{e(label)}</a>' for tag,label in zip(('studio','verify','learning'),d['nav']))
 parts=[f'''<!doctype html><html lang="{loc}" data-product-preview="1"><head>
 <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
 <title>{e(d['brand'])} Product Lab | {e(d['title'])}</title>
 <meta name="description" content="{e(d['lead'])}">
 <meta name="robots" content="noindex,follow">
 <meta name="theme-color" content="#ffffff"><link rel="canonical" href="{e(canonical)}">{alternates}
 <link rel="alternate" hreflang="x-default" href="https://manzo8b.github.io{BASE}{ROUTES['it']}/">
 <link rel="stylesheet" href="{BASE}assets/product/preview.css">
 <script src="{BASE}assets/product/preview.js" defer></script></head>
 <body><a class="skip" href="#main">Skip to content / Vai al contenuto</a>
 <header class="site-head"><div class="shell head-line">
 <a href="{BASE}{loc}/" class="wordmark"><img src="{BASE}assets/manzo-mark.svg" alt="">MANZO <span>AI</span></a>
 <nav class="site-nav" aria-label="Product navigation">{nav}
 <span class="language-switch">{langs}</span></nav></div></header>
 <main id="main">
 <section class="hero"><div class="shell hero-layout"><div>
 <p class="kicker">{e(d['kicker'])}</p><h1>{e(d['title'])}</h1><p class="hero-lead">{e(d['lead'])}</p>
 <p class="hero-note">{e(d['productNote'])}</p>
 <div class="actions"><a class="btn btn-primary" href="#studio">{e(d['action'])} ↗</a>
 <a class="btn" href="{BASE}{loc}/">{e(d['back'])}</a></div>
 <div class="hero-tags"><span>MANZO AI Studio</span><span>Verify</span><span>Learning</span></div>
 </div>{graphic()}</div></section>
 <div class="status-ribbon"><div class="shell"><span class="status-dot" aria-hidden="true"></span>
 <span><strong>{e(d['status'])}.</strong> {e(d['disclaimer'])}</span></div></div>
 <section class="overview"><div class="shell"><div class="section-head">
 <p class="kicker">THREE PRODUCT TRACKS</p><h2>Studio · Verify · Learning</h2>
 <p>{e(d['lead'])}</p></div><div class="product-grid">''']
 for i,(name,title,desc) in enumerate(d['cards'],1):
  parts.append(f'<article class="product-card"><span class="card-number">0{i} / {e(name)}</span><h3>{e(title)}</h3><p>{e(desc)}</p></article>')
 parts.append(f'''</div></div></section>
 <section class="workbench" id="studio"><div class="shell work-layout">
 <aside class="work-meta"><strong>01</strong><p>MANZO AI · STUDIO</p></aside><div class="work-main">
 <h2>{e(d['studioTitle'])}</h2><p>{e(d['studioDesc'])}</p>
 <div class="panel panel-cols"><div>
 <div class="form-field"><label for="project-type">{e(d['clientLabel'])}</label>
 <select class="field" id="project-type">''')
 for opt in d['clientOptions']:parts.append(f'<option>{e(opt)}</option>')
 parts.append(f'''</select></div>
 <div class="form-field"><label for="project-goal">{e(d['goalLabel'])}</label>
 <textarea class="field" id="project-goal" maxlength="1500" placeholder="{e(d['goalPlaceholder'])}"></textarea></div>
 <div class="form-field"><label for="project-audience">{e(d['audienceLabel'])}</label>
 <textarea class="field" id="project-audience" maxlength="1500" placeholder="{e(d['audiencePlaceholder'])}"></textarea></div>
 <div class="form-field"><label for="project-constraints">{e(d['constraintsLabel'])}</label>
 <textarea class="field" id="project-constraints" maxlength="1500" placeholder="{e(d['constraintsPlaceholder'])}"></textarea></div>
 <div class="actions"><button type="button" class="btn btn-primary" id="project-update">{e(d['generate'])}</button>
 <button type="button" class="btn" id="project-export">{e(d['download'])}</button></div>
 </div><div class="output"><h3>{e(d['previewTitle'])}</h3>
 <p>{e(d['previewDesc'])}</p><pre id="brief-json" aria-live="polite"></pre></div></div></div></div></section>
 <section class="workbench white" id="verify"><div class="shell work-layout">
 <aside class="work-meta"><strong>02</strong><p>MANZO AI · VERIFY</p></aside><div class="work-main">
 <h2>{e(d['verifyTitle'])}</h2><p>{e(d['verifyDesc'])}</p>
 <div class="panel">
 <div class="form-field"><label for="inspect-input">{e(d['textLabel'])}</label>
 <textarea id="inspect-input" class="field" rows="5" maxlength="6000" placeholder="{e(d['textPlaceholder'])}"></textarea></div>
 <div class="actions"><button type="button" class="btn btn-primary" id="inspect-text">{e(d['inspect'])}</button></div>
 <p class="claim-count" id="claim-count" aria-live="polite">0 · {e(d['claimCount'])}</p>
 <div id="claim-list" class="claims" aria-live="polite"></div>
 <p class="notice">{e(d['verifierHint'])}</p>
 <div class="output" style="margin-top:19px"><h3>{e(d['evidenceTitle'])}</h3><p>{e(d['evidenceDesc'])}</p></div>
 </div></div></div></section>
 <section class="workbench peach" id="learning"><div class="shell work-layout">
 <aside class="work-meta"><strong>03</strong><p>MANZO AI · LEARNING</p></aside><div class="work-main">
 <h2>{e(d['learningTitle'])}</h2><p>{e(d['learningDesc'])}</p>
 <div class="panel learning-setup"><div>
 <div class="form-field"><label for="org-type">{e(d['sectorLabel'])}</label><select id="org-type" class="field">''')
 for opt in d['sectorOptions']:parts.append(f'<option>{e(opt)}</option>')
 parts.append(f'''</select></div><div class="form-field">
 <label for="team-seats">{e(d['seatsLabel'])}</label>
 <div class="range-row"><input id="team-seats" type="range" min="5" max="100" step="5" value="20"><output id="team-seats-label" for="team-seats">20</output></div>
 </div><div class="form-field"><label for="team-module">{e(d['moduleLabel'])}</label><select id="team-module" class="field">''')
 for opt in d['moduleOptions']:parts.append(f'<option>{e(opt)}</option>')
 parts.append(f'''</select></div></div>
 <div class="output"><h3>{e(d['licenseTitle'])}</h3>
 <p class="license-summary" id="team-summary" aria-live="polite"></p><p>{e(d['licenseDisclaimer'])}</p>
 <button class="btn" type="button" id="copy-proposal">{e(d['copy'])}</button>
 <p class="notice">{e(d['programDesc'])}<br>
 <a class="link-inline" href="{BASE}{COURSES[loc]}/">{e(d['openCourse'])} ↗</a></p></div>
 </div></div></div></section>
 <section class="roadmap" id="readiness"><div class="shell">
 <div class="section-head"><p class="kicker">PRODUCT READINESS</p><h2>{e(d['readinessTitle'])}</h2>
 <p>{e(d['readinessLead'])}</p></div><div class="readiness">''')
 for status,copy in d['readiness']:
  typ='ready' if status==d['statusReady'] else ('verify' if status==d['statusVerify'] else 'pending')
  parts.append(f'<div class="readiness-item {typ}"><span>{e(status)}</span><strong>{e(copy)}</strong></div>')
 parts.append(f'''</div><p class="notice">{e(d['disclaimer'])}</p></div></section></main>
 <footer class="site-foot"><div class="shell"><strong>{e(d['footer'])}</strong>
 <p>{e(d['disclaimer'])}</p>
 <a href="{BASE}{loc}/">{e(d['back'])}</a></div></footer>
 <div id="announce" role="status" aria-live="polite" style="position:absolute;left:-10000px;width:1px;height:1px;overflow:hidden"></div>
 <script type="application/json" id="product-dictionary">{safe_data(d)}</script>
 </body></html>''')
 return ''.join(parts)

def inject_home(page,loc,d):
 if not page.is_file():raise RuntimeError('Required homepage not found: '+str(page))
 html=page.read_text(encoding='utf-8')
 marker='data-manzo-product-preview="v1"'
 if marker in html:return
 url=BASE+ROUTES[loc]+'/'
 block=f'''<section {marker} aria-label="{e(d['kicker'])}" style="max-width:1080px;margin:45px auto;padding:clamp(24px,5vw,48px);border-radius:24px;background:linear-gradient(140deg,#eef8ff,#f5f8ff);border:1px solid #d6e7f3;color:#1d405f">
 <p style="font-size:.76rem;text-transform:uppercase;font-weight:800;letter-spacing:.16em;color:#376aa4">{e(d['kicker'])}</p>
 <h2 style="font-size:clamp(1.7rem,3.5vw,2.7rem);font-weight:670;letter-spacing:-.055em;line-height:1.15;color:#173e68;margin:0 0 17px">{e(d['title'])}</h2>
 <p style="font-size:1.03rem;color:#4c647c;max-width:780px;line-height:1.65">{e(d['lead'])}</p>
 <p style="font-size:.82rem;color:#526f84">{e(d['status'])}</p>
 <a href="{e(url)}" style="display:inline-block;background:#174d85;color:#fff;border-radius:13px;padding:12px 18px;text-decoration:none;font-weight:740">{e(d['action'])} ↗</a></section>'''
 close=re.search(r'</main\s*>',html,flags=re.I)
 if close is None:close=re.search(r'</body\s*>',html,flags=re.I)
 if close is None:raise RuntimeError('No main/body closing: '+str(page))
 page.write_text(html[:close.start()]+block+html[close.start():],encoding='utf-8')

def publish(site,verify_only=False):
 if not (site/'it'/'index.html').exists():raise RuntimeError('Expected MANZO AI site missing')
 d=validate(json.loads((SRC/'content.json').read_text(encoding='utf-8')))
 assets=site/'assets'/'product'
 if not verify_only:
  assets.mkdir(parents=True,exist_ok=True)
  for name in ('preview.css','preview.js'):shutil.copyfile(SRC/name,assets/name)
  for loc in LOCALES:
   out=site/ROUTES[loc]/'index.html';out.parent.mkdir(parents=True,exist_ok=True)
   out.write_text(html_page(loc,d[loc]),encoding='utf-8')
   inject_home(site/loc/'index.html',loc,d[loc])
 for name in ('preview.css','preview.js'):
  assert (assets/name).read_bytes()==(SRC/name).read_bytes()
 for loc in LOCALES:
  out=site/ROUTES[loc]/'index.html'
  assert out.is_file()
  html=out.read_text(encoding='utf-8')
  for token in ('data-product-preview','project-type','inspect-text','team-seats','readiness','noindex,follow','hreflang'):
   assert token in html, f'No {token} in {loc}'
  assert html.count('class="product-card"')==3
  assert html.count('class="readiness-item')==6
  assert (site/loc/'index.html').read_text(encoding='utf-8').count('data-manzo-product-preview="v1"')==1
 print(f'MANZO AI product preview: {len(LOCALES)} locales, Studio Verify Learning, 6 readiness flags, noindex, no user data transfer; verify_only={verify_only}')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--site',required=True,type=Path)
 p.add_argument('--verify-only',action='store_true')
 a=p.parse_args();publish(a.site,a.verify_only)
