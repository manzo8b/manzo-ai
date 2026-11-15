#!/usr/bin/env python3
"""Publish a nontransactional MANZO AI Learning B2B interface preview.

No fake logins, payments, remote calls or personal information.
A simulated client-side workspace demonstrates team-seat workflows while
the actual Postgres functions remain isolated from the public website.
Run AFTER publish-product-preview.py and BEFORE SEO/navigation overlays.
"""
from __future__ import annotations
import argparse
import json
from html import escape
from pathlib import Path
import re
import shutil

ROOT=Path(__file__).resolve().parent.parent
SOURCE=ROOT/'product'/'learning-console'
BASE='/manzo-ai/'
ROUTES={
 'it':'it/prodotto/learning-b2b',
 'en':'en/product/learning-b2b',
 'es':'es/producto/learning-b2b'
}
PARENTS={'it':'it/prodotto','en':'en/product','es':'es/producto'}

def e(value):return escape(str(value),quote=True)
def safe_json(value):
 return json.dumps(value,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')

def validate(data):
 assert set(data)==set(ROUTES)
 for loc,d in data.items():
  assert len(d['stats'])==4 and len(d['courses'])==2
  assert len(d['personNames'])==4 and len(d['capabilities'])==3
  assert len(d['title'])>20 and len(d['warning'])>90
  for field in ('adminTitle','studentTitle','demo','assign','release','unlicensed','reset'):
   assert d[field],f'{loc}: missing {field}'
 return data

def render(locale,copy):
 url=BASE+ROUTES[locale]+'/'
 parent=BASE+PARENTS[locale]+'/'
 lang_links=''.join(
   f'<a href="{BASE}{ROUTES[l]}/" hreflang="{l}" lang="{l}"'
   +(' aria-current="page"' if l==locale else '')
   +f'>{l.upper()}</a>' for l in ROUTES
 )
 alternate=''.join(
   f'<link rel="alternate" hreflang="{l}" href="https://manzo8b.github.io{BASE}{path}/">'
   for l,path in ROUTES.items()
 )
 out=[f'''<!doctype html><html lang="{locale}" data-learning-console="v1"><head>
 <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
 <title>MANZO AI Learning B2B | {e(copy['title'])}</title>
 <meta name="description" content="{e(copy['subtitle'])}">
 <meta name="robots" content="noindex,follow"><meta name="theme-color" content="#ffffff">
 <link rel="canonical" href="https://manzo8b.github.io{url}">
 {alternate}<link rel="alternate" hreflang="x-default" href="https://manzo8b.github.io{BASE}{ROUTES['it']}/">
 <link rel="stylesheet" href="{BASE}assets/product/learning-console.css">
 <script src="{BASE}assets/product/learning-console.js" defer></script></head>
 <body><a class="skip" href="#lc-main">Skip to content / Vai al contenuto</a>
 <header class="site-header"><div class="shell header-inner">
 <a class="mark" href="{parent}">MANZO <strong>AI</strong> <span class="product-mark">/ LEARNING B2B</span></a>
 <nav class="langs" aria-label="Languages">{lang_links}</nav></div></header>
 <main id="lc-main"><section class="hero"><div class="shell">
 <p class="kicker">{e(copy['kicker'])}</p>
 <h1>{e(copy['title'])}</h1>
 <p class="lead">{e(copy['subtitle'])}</p>
 <div class="actions">
 <span class="demo-label">{e(copy['demo'])}</span>
 <a class="button" href="{parent}">{e(copy['back'])} ↗</a>
 </div></div></section>
 <div class="disclosure"><div class="shell"><p><strong>{e(copy['demo'])}.</strong> {e(copy['warning'])}</p></div></div>
 <section class="workspace"><div class="shell">
 <div class="workspace-heading">
 <span class="organization">◈ {e(copy['org'])} · MANZO AI</span>
 <div class="tabs" role="tablist" aria-label="Learning B2B demo">
  <button id="lc-tab-admin" type="button" role="tab" aria-controls="lc-admin-view" aria-selected="true">{e(copy['adminTab'])}</button>
  <button id="lc-tab-student" type="button" role="tab" aria-controls="lc-student-view-panel" aria-selected="false">{e(copy['studentTab'])}</button>
 </div></div>
 <div id="lc-admin-view" role="tabpanel" aria-labelledby="lc-tab-admin">
 <div class="panel-heading"><h2>{e(copy['adminTitle'])}</h2><p>{e(copy['adminLead'])}</p></div>
 <div class="metrics">''']
 for idx,(title,caption) in enumerate(copy['stats']):
  out.append(f'<div class="metric"><small>{e(title)}</small><strong id="lc-metric-{idx}">—</strong><span>{e(caption)}</span></div>')
 out.append(f'''</div>
 <div class="card">
 <h3>{e(copy['adminTitle'])}</h3>
 <div class="bar" aria-hidden="true"><span id="lc-seats-progress" role="progressbar" aria-label="{e(copy['stats'][0][0])}" aria-valuemin="0" aria-valuemax="3" aria-valuenow="2" style="width:66.67%"></span></div>
 <div class="table-wrap"><table><thead><tr><th scope="col">{e(copy['studentCol'])}</th>
 <th scope="col">{e(copy['seatCol'])}</th><th scope="col">{e(copy['enrollCol'])}</th>
 <th scope="col">{e(copy['progressCol'])}</th><th scope="col">{e(copy['actionCol'])}</th></tr></thead>
 <tbody id="lc-members"></tbody></table></div></div>
 <div class="section-two">
 <div class="card">
 <h3>{e(copy['enrollTitle'])}</h3><p class="support">{e(copy['adminLead'])}</p>
 <div class="form-grid">
 <div class="field"><label for="lc-student-admin">{e(copy['studentPick'])}</label>
 <select id="lc-student-admin"></select></div>
 <div class="field"><label for="lc-course-admin">{e(copy['coursePick'])}</label>
 <select id="lc-course-admin">''')
 for cid,name in zip(('hallucinations','coding'),copy['courses']):
  out.append(f'<option value="{cid}">{e(name)}</option>')
 out.append(f'''</select></div></div>
 <button class="button primary" id="lc-enroll" type="button">{e(copy['enroll'])}</button>
 <div id="lc-feedback" class="message" role="status" aria-live="polite">{e(copy['demo'])}</div>
 </div>
 <div class="card"><h3>{e(copy['eventsTitle'])}</h3>
 <p class="support">{e(copy['eventsLead'])}</p>
 <ul class="audit-list" id="lc-events"></ul>
 <div class="actions" style="margin-top:17px"><button class="button" type="button" id="lc-reset">{e(copy['reset'])}</button></div>
 </div></div></div>
 <div id="lc-student-view-panel" role="tabpanel" aria-labelledby="lc-tab-student" hidden>
 <div class="panel-heading"><h2>{e(copy['studentTitle'])}</h2><p>{e(copy['studentLead'])}</p></div>
 <div class="student-layout">
 <aside class="card student-aside">
 <div class="field"><label for="lc-student-view">{e(copy['studentPick'])}</label>
 <select id="lc-student-view"></select></div>
 <p class="notice muted" id="lc-student-access">{e(copy['noLogin'])}</p>
 </aside>
 <div id="lc-student-courses" class="student-course-list" aria-live="polite"></div>
 </div></div>
 </div></section>
 <section class="method-section"><div class="shell">
 <p class="kicker">PRODUCT READINESS</p>
 <h2>{e(copy['howTitle'])}</h2><p>{e(copy['howLead'])}</p>
 <div class="capabilities">''')
 for title,desc in copy['capabilities']:
  out.append(f'<article class="capability"><strong>{e(title)}</strong><p>{e(desc)}</p></article>')
 out.append(f'''</div></div></section></main>
 <footer class="footer"><div class="shell">
 <strong>MANZO AI · LEARNING B2B</strong>
 <p>{e(copy['warning'])}</p>
 <a href="{parent}">{e(copy['back'])} ↗</a>
 </div></footer>
 <script type="application/json" id="lc-content">{safe_json(copy)}</script>
 </body></html>''')
 return ''.join(out)

def link_parent(page,loc,d):
 if not page.is_file():raise RuntimeError('Product Lab is missing: '+str(page))
 raw=page.read_text(encoding='utf-8')
 marker='data-learning-b2b-console="1"'
 if marker in raw:return
 link=BASE+ROUTES[loc]+'/'
 block=f'''<section {marker} style="max-width:1180px;width:calc(100% - 42px);margin:40px auto;padding:clamp(23px,4vw,49px);border:1px solid #d9e8f1;border-radius:23px;background:linear-gradient(140deg,#edfaf5,#f3f7ff);color:#1d4266">
 <p style="font-size:.74rem;font-weight:800;letter-spacing:.15em;color:#267a71;margin-bottom:12px">{e(d['kicker'])}</p>
 <h2 style="font-size:clamp(1.75rem,3.6vw,3rem);font-weight:650;line-height:1.12;letter-spacing:-.06em;margin:0 0 16px">{e(d['title'])}</h2>
 <p style="font-size:1rem;max-width:850px;line-height:1.7;color:#547086">{e(d['subtitle'])}</p>
 <p style="font-size:.83rem;color:#7b6a51">{e(d['demo'])}</p>
 <a href="{e(link)}" style="display:inline-flex;padding:13px 20px;border-radius:12px;background:#174e86;color:#fff;text-decoration:none;font-weight:700">{e(d['adminTab'])} ↗</a></section>'''
 marker2='<section class="roadmap"'
 idx=raw.find(marker2)
 if idx<0:raise RuntimeError('Missing Product Lab roadmap section: '+str(page))
 page.write_text(raw[:idx]+block+raw[idx:],encoding='utf-8')

def publish(site,verify_only=False):
 data=validate(json.loads((SOURCE/'content.json').read_text(encoding='utf-8')))
 assets=site/'assets'/'product'
 if not verify_only:
  assets.mkdir(parents=True,exist_ok=True)
  for inp,out in (('console.css','learning-console.css'),('console.js','learning-console.js')):
   shutil.copyfile(SOURCE/inp,assets/out)
  for loc,d in data.items():
   target=site/ROUTES[loc]/'index.html'
   target.parent.mkdir(parents=True,exist_ok=True)
   target.write_text(render(loc,d),encoding='utf-8')
   link_parent(site/PARENTS[loc]/'index.html',loc,d)
 for inp,out in (('console.css','learning-console.css'),('console.js','learning-console.js')):
  assert (assets/out).read_bytes()==(SOURCE/inp).read_bytes()
 for loc in ROUTES:
  page=site/ROUTES[loc]/'index.html'
  assert page.is_file(),page
  doc=page.read_text(encoding='utf-8')
  for needle in ('data-learning-console','lc-members','lc-student-courses','lc-reset',
                 'noindex,follow','aria-selected','lc-content'):
   assert needle in doc,(loc,needle)
  assert doc.count('class="metric"')==4
  assert (site/PARENTS[loc]/'index.html').read_text(encoding='utf-8').count('data-learning-b2b-console="1"')==1
 print('PASS: trilingual Learning B2B visual simulation, 4 member slots, 3 seats, local-only UI, noindex; verify_only='+str(verify_only))

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--site',required=True,type=Path)
 p.add_argument('--verify-only',action='store_true')
 a=p.parse_args()
 publish(a.site,a.verify_only)
