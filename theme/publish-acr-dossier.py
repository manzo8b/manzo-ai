#!/usr/bin/env python3
"""Publish a trilingual, research-accurate ACR dossier onto MANZO AI's immutable ZIP build.

Run BEFORE build-seo.py and publish-navigation.py. Never edit the original site ZIP.
No external media or JavaScript dependencies; strictly editorial, no visitor tracking.
"""
from __future__ import annotations
import argparse
from html import escape
import json
from pathlib import Path
import re
import shutil

BASE = '/manzo-ai/'
ROUTES = {'it':'it/ricerca/acr','en':'en/research/acr','es':'es/investigacion/acr'}
HUBS = {'it':'it/risorse/index.html','en':'en/resources/index.html','es':'es/recursos/index.html'}
SRC_ROOT = Path(__file__).resolve().parent.parent / 'editorial' / 'research' / 'acr'
LAB = 'https://github.com/manzo8b/manzo-ai/tree/1a61fdb665f6ec9b7fe384abbe23e9a913d941f9/research/acr-lab'
PAPER_LINKS = [
 ('Shinn et al. (2023)', 'Reflexion · NeurIPS 2023', 'https://proceedings.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html'),
 ('Sumers et al. (2024)', 'Cognitive Architectures for Language Agents · TMLR', 'https://openreview.net/forum?id=1i6ZCyf1QJ'),
 ('Packer et al. (2023)', 'MemGPT: Towards LLMs as Operating Systems', 'https://arxiv.org/abs/2310.08560'),
 ('Khattab et al. (2024)', 'DSPy · ICLR 2024', 'https://proceedings.iclr.cc/paper_files/paper/2024/hash/f1cf02ce09757f57c3b93c0db83181e0-Abstract-Conference.html'),
 ('W3C (2023)', 'Web Content Accessibility Guidelines 2.2', 'https://www.w3.org/TR/WCAG22/'),
 ('MANZO AI (2026)', 'ACR v0.9 · Prototype, protocols and offline pilot', LAB),
]

def e(x: object) -> str:
    return escape(str(x), quote=True)

def orbit(c: dict) -> str:
    circles = []
    for radius, stroke, width, dash, extra in [(266,'#d7e6fb',1.3,'7 11',''),(225,'#adc9ef',1.4,'1 9',''),(184,'#bad9e4',2,'',''),(145,'#e9c8ed',1.5,'3 9',''),(107,'#cad8ef',2.5,'','')]:
        circles.append(f'<circle cx="300" cy="300" r="{radius}" fill="none" stroke="{stroke}" stroke-width="{width}"'+(f' stroke-dasharray="{dash}"' if dash else '')+extra+'/>')
    for rad, color, speed in [(252,'#2860b4',42),(192,'#b64c45',59),(135,'#7451b5',42)]:
        circles.append(f'<g class="orbit-ring {"rev" if speed==59 else ""}"><circle cx="{300+rad}" cy="300" r="{8 if rad==252 else 6}" fill="{color}"/><circle cx="{300-rad}" cy="300" r="3" fill="{color}" opacity=".5"/></g>')
    return (f'<div class="hero-visual" aria-hidden="true"><svg class="orbit" viewBox="0 0 600 600" role="presentation" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="acrg"><stop stop-color="#fff"/><stop offset="1" stop-color="#e5efff"/></radialGradient></defs>'+
            '<circle cx="300" cy="300" r="278" fill="url(#acrg)" opacity=".58"/>'+''.join(circles)+
            '<g class="orbit-pulse"><circle cx="300" cy="300" r="90" fill="#fff" stroke="#bcd2ee" stroke-width="1.5"/><text x="300" y="291" font-size="61" text-anchor="middle" font-weight="650" font-family="system-ui,sans-serif" fill="#2755a0" letter-spacing="-5">ACR</text><text x="300" y="328" font-size="14" text-anchor="middle" font-weight="700" font-family="system-ui,sans-serif" fill="#58718e" letter-spacing="3">LAB · V0.9</text></g>'+
            '<text x="72" y="298" font-size="14" fill="#7c91ae" font-weight="700">1</text><text x="506" y="259" font-size="14" fill="#7c91ae" font-weight="700">2</text><text x="141" y="453" font-size="14" fill="#7c91ae" font-weight="700">3</text><text x="469" y="471" font-size="14" fill="#7c91ae" font-weight="700">5</text><text x="297" y="32" font-size="14" fill="#7c91ae" font-weight="700">8</text></svg>'+
            f'<span class="orbital-label one">{e(c["orb1"])}</span><span class="orbital-label two">{e(c["orb2"])}</span></div>')

def html_document(locale: str, c: dict) -> str:
    loc_url=BASE+ROUTES[locale]+'/'
    lang_labels={'it':'Italiano','en':'English','es':'Español'}
    langs=''.join(f'<a class="lang-button {"active" if l==locale else ""}" href="{BASE+ROUTES[l]}/" lang="{l}" hreflang="{l}" aria-label="{lang_labels[l]}">{l.upper()}</a>' for l in ('it','en','es'))
    mobile=''.join(f'<a href="{BASE+ROUTES[l]}/" hreflang="{l}" lang="{l}">{lang_labels[l]}</a>' for l in ('it','en','es'))
    alternate=''.join(f'<link rel="alternate" hreflang="{l}" href="https://manzo8b.github.io{BASE+ROUTES[l]}/">' for l in ('it','en','es'))
    canonical=f'https://manzo8b.github.io{loc_url}'
    desc=c['hero_lead']
    schema={'@context':'https://schema.org','@type':'TechArticle','headline':c['hero_a']+' '+c['hero_b'],
     'inLanguage':locale,'datePublished':'2026-11-14','dateModified':'2026-11-14',
     'description':desc,'author':{'@type':'Person','name':'Marcelo Fernandez'},
     'publisher':{'@type':'Organization','name':'MANZO AI'},'url':canonical,
     'isAccessibleForFree':True,'creativeWorkStatus':'Working research dossier; not peer reviewed',
     'citation':[url for _,_,url in PAPER_LINKS[:5]]}
    schema_text=json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')
    metadata=f'''<!doctype html><html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(c['hero_a']+' '+c['hero_b'])} | MANZO AI ACR</title><meta name="description" content="{e(desc)}">
<meta name="robots" content="index,follow"><meta name="theme-color" content="#ffffff"><meta property="og:type" content="article"><meta property="og:title" content="{e(c['hero_a']+' '+c['hero_b'])}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canonical}"><meta property="article:published_time" content="2026-11-14T00:00:00+01:00">
<meta name="twitter:card" content="summary"><link rel="canonical" href="{canonical}">{alternate}<link rel="alternate" hreflang="x-default" href="https://manzo8b.github.io{BASE+ROUTES['it']}/"><link rel="stylesheet" href="{BASE}assets/research/acr/dossier.css">
<script src="{BASE}assets/research/acr/dossier.js" defer></script><script type="application/ld+json">{schema_text}</script></head><body>'''
    head=f'''<a class="skip" href="#content">{e(c['skip'])}</a><header class="mast" id="top"><div class="container mast-inner"><a class="brand" href="{BASE+locale}/"><span class="brand-mark"><img src="{BASE}assets/manzo-mark.svg" width="28" height="28" alt=""></span>MANZO <em>AI</em> <span style="font-size:.72rem;font-weight:600;letter-spacing:0;color:#6b7e92">/ RESEARCH</span></a>
<nav class="mast-links" aria-label="{e(c['nav_research'])}"><a href="#program" class="lang-button">{e(c['nav_research'])}</a><a href="#method" class="lang-button">{e(c['nav_methods'])}</a>{langs}<details class="menu-mobile"><summary>{locale.upper()} ▾</summary><div>{mobile}</div></details><a class="back-home" href="{BASE+locale}/">{e(c['nav_home'])}</a></nav></div></header>'''
    hero=f'''<main id="content" data-acr-dossier><section class="hero"><div class="container hero-grid"><div class="hero-copy"><p class="overline">{e(c['eyebrow'])}</p><h1><span>{e(c['hero_a'])}</span><span class="accent">{e(c['hero_b'])}</span></h1><p class="hero-desc">{e(c['hero_lead'])}</p><div class="hero-actions"><a class="btn btn-primary" href="#program">{e(c['hero_action'])} <span aria-hidden="true">↗</span></a><a class="btn btn-light" href="{LAB}" target="_blank" rel="noopener noreferrer">{e(c['hero_second'])} <span aria-hidden="true">↗</span></a></div><div class="hero-meta"><span class="meta-chip">{e(c['hero_tag1'])}</span><span class="meta-chip">{e(c['hero_tag2'])}</span><span class="meta-chip ongoing">{e(c['hero_tag3'])}</span></div><span class="scroll-cue">{e(c['scroll'])}</span></div>{orbit(c)}</div></section>'''
    opening=f'''<section class="section section-intro" id="intro"><div class="container"><div class="opening-statement reveal"><div><p class="section-kicker">{e(c['statement_kicker'])}</p><blockquote>{c['statement_quote']}</blockquote></div><p>{e(c['statement_copy'])}</p></div><div class="metric-row reveal"><article class="metric"><strong>48/48</strong><em>{e(c['stat1'])}</em></article><article class="metric"><strong>0</strong><em>{e(c['stat2'])}</em></article><article class="metric"><strong>3</strong><em>{e(c['stat3'])}</em></article></div><p style="font-size:.81rem;color:#718295;margin:15px 4px">{e(c['stat_disclaimer'])}</p></div></section>'''
    paths=''.join(f'<article class="path {id.lower()} reveal"><div class="id">{id}</div><h3>{e(c["path"+id])}</h3><p>{e(c["path"+id+"_copy"])}</p><div class="path-bottom"><span class="small-pill">{e(c["path"+id+"_state"])}</span><span class="path-arrow" aria-hidden="true">↗</span></div></article>' for id in ('A','B','C'))
    program=f'''<section class="section section-tint" id="program"><div class="container"><div class="section-head reveal"><p class="section-kicker">{e(c['paths_kicker'])}</p><h2 class="section-title">{c['paths_title']}</h2><p>{e(c['paths_intro'])}</p></div><div class="path-grid">{paths}</div></div></section>'''
    tiers=''.join(f'<div class="mem-tier"><span class="mem-num">M{i}</span><div class="mem-copy"><b>{e(c["m"+str(i)])}</b><span>{e(c["m"+str(i)+"_copy"])}</span></div></div>' for i in range(4))
    memory=f'''<section class="section" id="architecture"><div class="container"><div class="section-head reveal"><p class="section-kicker">{e(c['memory_kicker'])}</p><h2 class="section-title">{c['memory_title']}</h2><p>{e(c['memory_intro'])}</p></div><div class="memory-layout"><div class="memory-stair reveal">{tiers}</div><div class="memory-body reveal"><h3>{e(c['memory_body_title'])}</h3><p>{e(c['memory_body_copy'])}</p><span class="formula">{e(c['memory_formula'])}</span><div class="state-chain" aria-label="{e(c['memory_states'])}"><span>Candidate</span><span>Verified</span><span>Approved</span></div></div></div><aside class="safety-panel reveal"><div class="safety-icon" aria-hidden="true">!</div><div><h3>{e(c['safety_title'])}</h3><p>{e(c['safety_copy'])}</p></div></aside></div></section>'''
    buttons=''.join(f'<button type="button" data-demo-step="{i}" aria-pressed="{"true" if i==0 else "false"}">{e(label)}</button>' for i,label in enumerate(c['demo_step']))
    initial=c['demo_data'][0]
    data=json.dumps(c['demo_data'],ensure_ascii=False).replace('<','\\u003c')
    demo=f'''<section class="section section-lilac" id="interactive"><div class="container"><div class="section-head reveal"><p class="section-kicker">{e(c['demo_kicker'])}</p><h2>{e(c['demo_title'])}</h2><p>{e(c['demo_intro'])}</p></div><div class="demo-shell reveal"><div class="demo-top"><h3>{e(c['demo_head'])}</h3><div class="demo-steps" role="group" aria-label="{e(c['demo_head'])}">{buttons}</div></div><div class="demo-core" aria-live="polite" aria-atomic="true"><div class="demo-display"><div class="demo-status" data-demo-status>{e(initial['status'])}</div><h3 data-demo-title>{e(initial['title'])}</h3><p data-demo-description>{e(initial['description'])}</p><span class="demo-flag" data-demo-flag>{e(initial['flag'])}</span></div><div class="demo-log"><span class="label">MANZO ACR / TRACE</span><code data-demo-code>{e(initial['code'])}</code><span class="note">{e(c['demo_intro'])}</span></div></div></div><script type="application/json" id="acr-demo-data">{data}</script></div></section>'''
    result=f'''<section class="section" id="results"><div class="container"><div class="section-head reveal"><p class="section-kicker">{e(c['results_kicker'])}</p><h2 class="section-title">{c['results_title']}</h2><p>{e(c['results_intro'])}</p></div><div class="comparison reveal"><div class="comparison-top"><h3>{e(c['results_head'])}</h3><span class="seal">{e(c['results_warning'])}</span></div><div class="chart-grid"><div class="bar-unit"><div class="bar-h"><span>{e(c['barC2'])}</span><strong>12,5%</strong></div><div class="bar-track" role="img" aria-label="C2: 2 of 16 regression events"><div class="bar-fill"></div></div><p>2 / 16</p></div><div class="bar-unit acr"><div class="bar-h"><span>{e(c['barC3'])}</span><strong>12,5%</strong></div><div class="bar-track" role="img" aria-label="C3: 2 of 16 regression events"><div class="bar-fill"></div></div><p>2 / 16</p></div></div><p class="qualification">{e(c['bar_caption'])}</p><p class="qualification">{e(c['results_caveat'])}</p></div></div></section>'''
    methods=''.join(f'<article class="method reveal"><div class="method-index">0{i}</div><h3>{e(c["meth"+str(i)])}</h3><p>{e(c["meth"+str(i)+"_copy"])}</p><strong>{e(c["meth"+str(i)+"_sub"])}</strong></article>' for i in (1,2,3))
    method=f'''<section class="section section-peach" id="method"><div class="container"><div class="section-head reveal"><p class="section-kicker">{e(c['methods_kicker'])}</p><h2 class="section-title">{c['methods_title']}</h2><p>{e(c['methods_intro'])}</p></div><div class="method-table">{methods}</div></div></section>'''
    truth=f'''<section class="section" id="limits"><div class="container"><div class="truth reveal"><div><p class="section-kicker">{e(c['truth_kicker'])}</p><h2>{e(c['truth_title'])}</h2><p>{e(c['truth_copy'])}</p></div><div class="big-zero">0<span>{e(c['truth_zero'])}</span></div></div></div></section>'''
    refs=''.join(f'<a class="reference reveal" href="{e(link)}" target="_blank" rel="noopener noreferrer"><div class="ref-num">{i:02d}</div><div class="ref-body"><b>{e(name)}</b><span>{e(title)}</span><small>{e(link.split("/")[2])} ↗</small></div></a>' for i,(name,title,link) in enumerate(PAPER_LINKS,1))
    sources=f'''<section class="section section-tint" id="sources"><div class="container"><div class="section-head reveal"><p class="section-kicker">{e(c['sources_kicker'])}</p><h2 class="section-title">{c['sources_title']}</h2><p>{e(c['sources_intro'])}</p></div><div class="refs">{refs}</div></div></section>'''
    final=f'''</main><section class="future-band"><div class="container future-inner"><div><p class="section-kicker">{e(c['future_kicker'])}</p><h2>{e(c['future_title'])}</h2><p>{e(c['future_copy'])}</p></div><div><a class="btn btn-primary" href="{LAB}" target="_blank" rel="noopener noreferrer">{e(c['future_btn'])} <span aria-hidden="true">↗</span></a></div></div></section><footer class="foot"><div class="container foot-inner"><div><strong>MANZO AI · ACR LAB</strong><p>{e(c['footer_note'])}</p></div><nav aria-label="Footer"><a href="{BASE+locale}/">{e(c['footer_back'])}</a><a href="#top">{e(c['footer_top'])}</a></nav></div></footer></body></html>'''
    return metadata+head+hero+opening+program+memory+demo+result+method+truth+sources+final

def inject_feature(page: Path, loc: str, c: dict, is_home: bool):
    if not page.exists():
        raise RuntimeError('Missing mandatory site entry point: '+str(page))
    html=page.read_text(encoding='utf-8')
    route=BASE+ROUTES[loc]+'/'
    if 'data-acr-feature="v1"' in html:
        return
    if route in html:
        raise RuntimeError('Existing ACR route found; refusing duplicate feature '+str(page))
    block=f'''<section data-acr-feature="v1" aria-label="{e(c['nav_research'])}" style="display:block;max-width:1090px;margin:2.3rem auto;padding:clamp(24px,4vw,42px);border:1px solid #cbdcf0;border-radius:32px;background:linear-gradient(115deg,#eef4ff 0%,#fff 53%,#fff0ec 100%);color:#193652;box-shadow:0 18px 48px #244f8a12"><div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap"><span style="color:#2858ab;font-weight:800;font-size:.75rem;letter-spacing:.1em">MANZO AI · ACR LAB</span><span style="font-size:.73rem;font-weight:750;border-radius:99px;background:#fff7df;color:#79510b;border:1px solid #e8d39a;padding:5px 10px">{e(c['hero_tag3'])}</span></div><h2 style="color:#183a66;font-size:clamp(1.5rem,4vw,2.35rem);font-weight:680;letter-spacing:-.05em;line-height:1.16;margin:15px 0">{e(c['hero_a'])} {e(c['hero_b'])}</h2><p style="color:#4c647b;max-width:660px;font-size:1rem;line-height:1.6;margin:0 0 23px">{e(c['hero_lead'])}</p><a href="{route}" style="display:inline-flex;align-items:center;min-height:48px;background:#2458b8;color:#fff;font-weight:800;text-decoration:none;border-radius:999px;padding:12px 23px">{e(c['hero_action'])} <span aria-hidden="true" style="margin-left:8px">↗</span></a></section>'''
    close=re.search(r'</main\s*>',html,re.I)
    if close is None:
        raise RuntimeError('No closing main: '+str(page))
    html=html[:close.start()]+block+html[close.start():]
    page.write_text(html,encoding='utf-8')

def publish(site: Path, source: Path=SRC_ROOT) -> dict:
    if not site.is_dir(): raise RuntimeError('Site directory missing')
    data=json.loads((source/'content.json').read_text(encoding='utf-8'))
    assert set(data)==set(ROUTES)
    assets=site/'assets'/'research'/'acr'
    assets.mkdir(parents=True,exist_ok=True)
    for name in ('dossier.css','dossier.js'):
        shutil.copyfile(source/name,assets/name)
    created=[]
    for loc,route in ROUTES.items():
        dest=site/route/'index.html';dest.parent.mkdir(parents=True,exist_ok=True)
        doc=html_document(loc,data[loc])
        dest.write_text(doc,encoding='utf-8')
        created.append(route)
    # Feature cards are inserted only on six established entry points; never touch the ZIP itself.
    for loc in ROUTES:
        for relative in (f'{loc}/index.html',HUBS[loc]):
            inject_feature(site/relative,loc,data[loc],relative.endswith(f'{loc}/index.html'))
    for loc,route in ROUTES.items():
        html=(site/route/'index.html').read_text(encoding='utf-8')
        assert 'data-acr-dossier' in html and '12,5%' in html and '48/48' in html
        assert html.count('href="https://')>=len(PAPER_LINKS)
    print('ACR dossier overlay: 3 locales, 6 linked hubs, 2 static assets, no external dependencies')
    return {'pages':created,'hubs':6}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--site',required=True,type=Path)
    p.add_argument('--source',type=Path,default=SRC_ROOT)
    a=p.parse_args()
    publish(a.site,a.source)
