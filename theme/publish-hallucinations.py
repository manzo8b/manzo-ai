#!/usr/bin/env python3
"""Publish the MANZO AI professional course without changing the release ZIP.
Locales: Italian, English, Spanish. Offline interactive exercises, quiz and crossword.
Runs before SEO and global navigation; generated pages are deterministic and accessible.
"""
from __future__ import annotations
import argparse
from html import escape
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'editorial' / 'learning' / 'hallucinations'
BASE = '/manzo-ai/'
ROUTES = {
    'it': 'it/impara/allucinazioni-ai-verificabilita',
    'en': 'en/learn/ai-hallucinations-verification',
    'es': 'es/aprende/alucinaciones-ia-verificacion',
}
HUBS = {
    'it': ['it/index.html', 'it/academy/index.html', 'it/risorse/index.html'],
    'en': ['en/index.html', 'en/academy/index.html', 'en/resources/index.html'],
    'es': ['es/index.html', 'es/academia/index.html', 'es/recursos/index.html'],
}
SOURCES = [
    ('F1','Kalai et al. · OpenAI (2025)','Why Language Models Hallucinate','https://openai.com/index/why-language-models-hallucinate/'),
    ('F2','NIST · AI 600-1 (2024)','Generative AI Profile — Confabulation, §§ 2.2, 2.7','https://doi.org/10.6028/NIST.AI.600-1'),
    ('F3','Anthropic · Claude Platform','Reduce hallucinations — official guidance','https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations'),
    ('F4','Google AI for Developers','Grounding with Google Search — Gemini API','https://ai.google.dev/gemini-api/docs/google-search'),
    ('F5','Farquhar et al. · Nature (2024)','Detecting hallucinations in LLMs using semantic entropy','https://doi.org/10.1038/s41586-024-07421-0'),
    ('F6','European Union · AI Act','Regulation (EU) 2024/1689 — Articles 4 and 14','https://eur-lex.europa.eu/eli/reg/2024/1689'),
    ('F7','ESMA (30 May 2024)','AI in retail investment services — Public Statement','https://www.esma.europa.eu/press-news/esma-news/esma-provides-guidance-firms-using-artificial-intelligence-investment-services'),
    ('F8','FATF/GAFI (2025)','Money Laundering National Risk Assessment Guidance — risk-based analysis','https://www.fatf-gafi.org/content/fatf-gafi/en/publications/Methodsandtrends/Money-Laundering-National-Risk-Assessment-Guidance.html'),
    ('F9','GitHub Docs','Review AI-generated code','https://docs.github.com/en/copilot/tutorials/review-ai-generated-code'),
    ('F10','OWASP GenAI Security Project','LLM05:2025 Improper Output Handling','https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/'),
    ('F11','NIST · SP 800-218 (2022)','Secure Software Development Framework (SSDF) v1.1','https://csrc.nist.gov/pubs/sp/800/218/final'),
    ('F12','Spracklen et al. · USENIX Security 2025','We Have a Package for You! Package hallucinations in coding models','https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen'),
]

def e(value):
    return escape(str(value), quote=True)

def jscript(value):
    return json.dumps(value, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')

def validate_data(locale, content):
    h = content['head']
    for key in ('title1','title2','desc','start','notice','quizCheck','crossCheck'):
        assert h.get(key), f'{locale}: missing {key}'
    assert len(content['modules']) == 6, f'{locale}: expected six modules'
    assert len(content['cases']) == 10, f'{locale}: expected ten cases'
    assert len(content['quiz']) == 10, f'{locale}: expected ten quiz questions'
    assert len(content['method']) == 7
    assert len(content['clues'][0]) == 7
    for i, q in enumerate(content['quiz']):
        prompt, options, correct, explanation = q
        assert prompt and explanation
        assert len(options) in (2,4)
        assert 1 <= len(correct) <= 3
        assert all(isinstance(x,int) and 0 <= x < len(options) for x in correct)
        assert len(correct) == len(set(correct)), f'{locale}: repeated quiz keys {i}'
        if len(options)==2:
            assert len(correct)==1, f'{locale}: invalid true/false key'
    return content

def orbit():
    rings = ''.join(f'<circle cx="220" cy="220" r="{r}" stroke="{col}" stroke-width="1.5" fill="none" stroke-dasharray="{dash}"/>'
        for r,col,dash in [(178,'#b9cfe9','6 12'),(135,'#d4e4f4','2 9'),(94,'#a8d9df','3 8')])
    return ('''<div class="hx-orbit" aria-hidden="true"><svg viewBox="0 0 440 440" xmlns="http://www.w3.org/2000/svg">
        <defs><radialGradient id="hxGrad"><stop stop-color="#fff"/><stop offset="1" stop-color="#e8f5fe"/></radialGradient></defs>
        <circle cx="220" cy="220" r="204" fill="url(#hxGrad)" opacity=".68"/>''' + rings +
        '''<g class="hx-rotate"><circle cx="398" cy="220" r="9" fill="#3469b9"/><circle cx="42" cy="220" r="5" fill="#88adc9"/></g>
        <g class="hx-rotate rev"><circle cx="220" cy="85" r="7" fill="#c35b60"/><circle cx="220" cy="355" r="4" fill="#3aa19a"/></g>
        <circle cx="220" cy="220" r="79" fill="#fff" stroke="#c6dcea" stroke-width="2"/>
        <text x="220" y="212" font-size="36" text-anchor="middle" font-weight="650" font-family="system-ui" fill="#1e4d87">VERIFY</text>
        <text x="220" y="245" font-size="12" text-anchor="middle" letter-spacing="3" font-weight="700" font-family="system-ui" fill="#6483a8">01 / 07</text>
        </svg></div>''')

def source_marks(ids):
    return ' '.join(f'<a href="#hx-{e(ref.lower())}" title="{e(ref)}" class="hx-cite">[{e(ref)}]</a>' for ref in ids)

def build(locale, content):
    h = content['head']
    route = BASE + ROUTES[locale] + '/'
    canonical = 'https://manzo8b.github.io' + route
    alternates = ''.join(f'<link rel="alternate" hreflang="{lang}" href="https://manzo8b.github.io{BASE}{ROUTES[lang]}/">'
                         for lang in ROUTES)
    langlinks = ''.join(f'<a href="{BASE}{ROUTES[lang]}/" hreflang="{lang}" lang="{lang}"'
                        + (' aria-current="page"' if lang == locale else '') + f'>{lang.upper()}</a>'
                        for lang in ROUTES)
    schema = {
      '@context':'https://schema.org','@type':'Course',
      'name':h['title1']+' '+h['title2'],'description':h['desc'],'inLanguage':locale,
      'url':canonical,'isAccessibleForFree':True,
      'provider':{'@type':'Organization','name':'MANZO AI'},
      'author':{'@type':'Person','name':'Marcelo Fernandez'},
      'datePublished':'2026-11-15','dateModified':'2026-11-15',
      'educationalLevel':'Professional continuing education',
      'timeRequired':'PT6H15M',
      'citation':[url for _ref,_author,_title,url in SOURCES]
    }
    html = [f'''<!doctype html><html lang="{locale}"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>{e(h['title1']+' '+h['title2'])} | MANZO AI Professional Learning</title>
    <meta name="description" content="{e(h['desc'])}">
    <meta name="robots" content="index,follow"><meta name="theme-color" content="#ffffff">
    <meta property="og:type" content="website"><meta property="og:title" content="{e(h['title1']+' '+h['title2'])}">
    <meta property="og:description" content="{e(h['desc'])}"><meta property="og:url" content="{e(canonical)}">
    <link rel="canonical" href="{e(canonical)}">{alternates}
    <link rel="alternate" hreflang="x-default" href="https://manzo8b.github.io{BASE}{ROUTES['it']}/">
    <link rel="stylesheet" href="{BASE}assets/learning/hallucinations/course.css">
    <script src="{BASE}assets/learning/hallucinations/course.js" defer></script>
    <script type="application/ld+json">{jscript(schema)}</script></head><body class="hx-page" data-hx-course="1">
    <a class="hx-skip" href="#hx-main">Skip to content / Vai al contenuto</a>
    <header class="hx-header"><div class="hx-wrap hx-head-inner">
    <a class="hx-logo" href="{BASE}{locale}/"><img src="{BASE}assets/manzo-mark.svg" alt="">MANZO <i>AI</i></a>
    <nav class="hx-nav" aria-label="Course navigation">
    <a class="hx-navlink" href="#hx-program">{e(h['program'])}</a>
    <a class="hx-navlink" href="#hx-lab">{e(h['practice'])}</a>
    <a class="hx-navlink" href="#hx-quiz">{e(h['assessment'])}</a>
    <a class="hx-navlink" href="#hx-sources">{e(h['sources'])}</a>
    <span class="hx-langs">{langlinks}</span>
    </nav></div></header>
    <main id="hx-main"><section class="hx-hero"><div class="hx-wrap hx-hero-layout">
    <div><p class="hx-kicker">{e(h['kicker'])}</p><h1>{e(h['title1'])}<span>{e(h['title2'])}</span></h1>
    <p class="hx-intro">{e(h['desc'])}</p>
    <p class="hx-ledger">{e(h['strap'])}</p>
    <div class="hx-actions"><a class="hx-btn hx-btn-primary" href="#hx-program">{e(h['start'])} ↗</a>
    <a class="hx-btn" href="#hx-lab">{e(h['try'])} ↗</a></div>
    <div class="hx-meta"><span class="hx-tag">{e(h['tag1'])}</span><span class="hx-tag">{e(h['tag2'])}</span>
    <span class="hx-tag">{e(h['tag3'])}</span></div></div>{orbit()}</div></section>
    <div class="hx-band"><div class="hx-wrap hx-band-row">
    <div class="hx-fact"><strong>{e(h['metric1'])}</strong><small>{e(h['metric1b'])}</small></div>
    <div class="hx-fact"><strong>{e(h['metric2'])}</strong><small>{e(h['metric2b'])}</small></div>
    <div class="hx-fact"><strong>{e(h['metric3'])}</strong><small>{e(h['metric3b'])}</small></div>
    </div></div>
    <section class="hx-section" id="hx-program"><div class="hx-wrap">
    <div class="hx-headline"><p class="hx-kicker">{e(h['programK'])}</p><h2>{e(h['programH'])}</h2><p>{e(h['programD'])}</p></div>''']
    for i, module in enumerate(content['modules'],1):
        html.append(f'''<article class="hx-module"><div class="hx-module-aside"><span class="hx-num">{i:02d}</span>
        <span>{e(module['duration'])}</span></div><div class="hx-module-body">
        <h3 class="hx-module-title">{e(module['title'])}</h3>''')
        html.extend(f'<p>{e(p)}</p>' for p in module['p'])
        html.append(f'<div class="hx-evidence">{e(module["evidence"])} <span class="hx-note">{source_marks(module["sources"])}</span></div></div></article>')
    html.append('''</div></section>''')
    html.append(f'''<section class="hx-section hx-peach" id="hx-method"><div class="hx-wrap">
        <div class="hx-headline"><p class="hx-kicker">{e(h['methodK'])}</p><h2>{e(h['methodH'])}</h2><p>{e(h['methodD'])}</p></div>
        <div class="hx-principles">''')
    for no,name,copy in content['method']:
        html.append(f'<article class="hx-principle"><b>{e(no)}</b><h3>{e(name)}</h3><p>{e(copy)}</p></article>')
    html.append('</div></div></section>')
    html.append(f'''<section class="hx-section hx-tint" id="hx-lab"><div class="hx-wrap">
        <div class="hx-headline"><p class="hx-kicker">{e(h['practiceK'])}</p><h2>{e(h['practiceH'])}</h2>
        <p>{e(h['practiceD'])}</p><p class="hx-note">{e(h['exerciseProgress'])}: <strong id="hx-case-progress">0 / 10</strong></p></div>
        <div class="hx-cases">''')
    for i,(sector,title,scenario,task,solution) in enumerate(content['cases'],1):
        html.append(f'''<article class="hx-case"><div class="hx-case-head"><span class="hx-case-no">CASE {i:02d}</span>
            <span class="hx-sector">{e(sector)}</span></div><h3>{e(title)}</h3>
            <p class="hx-quote">{e(scenario)}</p><p><strong>{e(task)}</strong></p>
            <label for="hx-case-answer-{i}">{e(h['exerciseLabel'])}</label>
            <textarea class="hx-answer" id="hx-case-answer-{i}" rows="4" maxlength="5000"></textarea>
            <div class="hx-case-actions"><button type="button" class="hx-btn hx-reveal" disabled>{e(h['compare'])}</button>
            <span class="hx-note hx-case-status" aria-live="polite">{e(h['exInput'])}</span></div>
            <div class="hx-case-feedback" hidden>{e(solution)}</div></article>''')
    html.append('</div></div></section>')
    html.append(f'''<section class="hx-section" id="hx-quiz"><div class="hx-wrap">
        <div class="hx-headline"><p class="hx-kicker">{e(h['quizK'])}</p><h2>{e(h['quizH'])}</h2>
        <p>{e(h['quizD'])}</p></div>
        <div class="hx-quiz"><div class="hx-quiz-progress" aria-hidden="true"><b id="hx-quiz-bar"></b></div>
        <p class="hx-q-status" id="hx-quiz-position">1 / 10</p>
        <div id="hx-question" aria-live="polite"></div>
        <div id="hx-quiz-feedback" class="hx-feedback" hidden role="status"></div>
        <div id="hx-quiz-result" class="hx-result" hidden aria-live="polite"></div>
        <div class="hx-quiz-controls">
          <button type="button" class="hx-btn hx-btn-primary" id="hx-quiz-check">{e(h['quizCheck'])}</button>
          <button type="button" class="hx-btn" id="hx-quiz-next" hidden>{e(h['next'])}</button>
        </div></div>
        <script type="application/json" id="hx-quiz-data">{jscript([
            {'prompt':prompt,'options':opts,'correct':keys,'explain':explain}
            for prompt,opts,keys,explain in content['quiz']
        ])}</script></div></section>''')
    clue_numbers = [1,3,4,5,6,7,8]
    html.append(f'''<section class="hx-section hx-tint" id="hx-crossword"><div class="hx-wrap">
        <div class="hx-headline"><p class="hx-kicker">{e(h['crossK'])}</p><h2>{e(h['crossH'])}</h2>
        <p>{e(h['crossD'])}</p></div>
        <div class="hx-cross-layout"><div><div class="hx-cross-grid" id="hx-cross-grid" role="group" aria-label="{e(h['crossH'])}"></div>
        <div class="hx-actions"><button class="hx-btn hx-btn-primary" type="button" id="hx-cross-check">{e(h['crossCheck'])}</button>
        <button class="hx-btn" type="button" id="hx-cross-reset">{e(h['reset'])}</button></div>
        <p class="hx-cross-status" id="hx-cross-status" aria-live="polite"></p></div><div>
        <h3>{e(h['across'])}</h3>''')
    for no,clue in zip(clue_numbers,content['clues'][0]):
        html.append(f'<p class="hx-clue"><strong>{no:02d}</strong> · {e(clue)}</p>')
    html.append(f'<h3>{e(h["down"])}</h3><p class="hx-clue"><strong>02</strong> · {e(content["clues"][1])}</p></div></div></div></section>')
    html.append(f'''<section class="hx-section" id="hx-sources"><div class="hx-wrap">
        <div class="hx-headline"><p class="hx-kicker">{e(h['sourceK'])}</p><h2>{e(h['sourceH'])}</h2>
        <p>{e(h['sourceD'])}</p></div><div class="hx-sources">''')
    for ref,author,title,url in SOURCES:
        html.append(f'''<a class="hx-source" id="hx-{e(ref.lower())}" href="{e(url)}" target="_blank" rel="noopener noreferrer">
          <b>{e(ref)} · {e(author)} ↗</b><p>{e(title)}</p></a>''')
    html.append(f'''</div></div></section></main>
      <footer class="hx-foot"><div class="hx-wrap"><strong>{e(h['closing'])}</strong>
      <p>{e(h['notice'])}</p><a href="{BASE}{locale}/">{e(h['back'])} ↗</a></div></footer>
      <script type="application/json" id="hx-ui-labels">{jscript({
        name:h[name] for name in ('exInput','exReady','compare','hide','correct','incorrect',
          'select','next','finish','score','restart','quizEnd','cell','crossSuccess',
          'crossResult','crossReset')
      })}</script></body></html>''')
    return ''.join(html)

def inject_hub(page, locale, content):
    if not page.is_file():
        raise RuntimeError('Missing site hub: ' + str(page))
    h = content['head']
    text = page.read_text(encoding='utf-8')
    marker = 'data-hx-feature="1"'
    if marker in text:
        return
    title = h['title1'] + ' ' + h['title2']
    link = BASE+ROUTES[locale]+'/'
    block = f'''<section {marker} aria-label="{e(title)}" style="width:min(1100px,calc(100% - 32px));margin:42px auto;padding:clamp(26px,5vw,54px);background:linear-gradient(120deg,#f2f9ff,#eef9f5);border:1px solid #d9e8ef;border-radius:26px;color:#183d5c;box-sizing:border-box">
    <p style="font-size:.75rem;letter-spacing:.15em;font-weight:800;color:#3e679a;margin:0 0 12px">{e(h['kicker'])}</p>
    <h2 style="font-size:clamp(1.7rem,3vw,2.7rem);line-height:1.13;letter-spacing:-.045em;color:#173d68;margin:0 0 15px">{e(title)}</h2>
    <p style="font-size:1rem;line-height:1.7;max-width:780px;color:#4b6477;margin:0 0 22px">{e(h['desc'])}</p>
    <a href="{e(link)}" style="display:inline-block;background:#174d8a;border-radius:13px;padding:12px 20px;color:white;font-weight:740;text-decoration:none">{e(h['start'])} ↗</a></section>'''
    match = re.search(r'</main\s*>', text, flags=re.I)
    if not match:
        match = re.search(r'</body\s*>', text, flags=re.I)
    if not match:
        raise RuntimeError('Hub HTML has no closing main/body: '+str(page))
    page.write_text(text[:match.start()]+block+text[match.start():], encoding='utf-8')

def crossword_check():
    words=[('PROVENIENZA',0,5,0,1),('VERIFICABILITA',0,8,1,0),
           ('RISCHIO',2,8,0,1),('FONTE',4,8,0,1),('TRACCIABILITA',6,5,0,1),
           ('PROBATORIO',8,5,0,1),('CONTROLLO',10,2,0,1),('CONTESTO',12,5,0,1)]
    letters={}
    for word,row,col,dr,dc in words:
        for idx,ch in enumerate(word):
            r,c=row+idx*dr,col+idx*dc
            assert 0<=r<14 and 0<=c<18
            assert (r,c) not in letters or letters[(r,c)]==ch, f'Invalid crossword cross {r,c}'
            letters[(r,c)]=ch
    assert len(letters)>60
    return len(letters)

def publish(site, verify_only=False):
    if not (site / 'it' / 'index.html').is_file():
        raise RuntimeError('Missing original MANZO AI site')
    data={loc:validate_data(loc,json.loads((SRC/f'{loc}.json').read_text(encoding='utf-8'))) for loc in ROUTES}
    count=crossword_check()
    assets=site / 'assets' / 'learning' / 'hallucinations'
    if not verify_only:
        assets.mkdir(parents=True,exist_ok=True)
        for name in ('course.css','course.js'):
            shutil.copyfile(SRC/name,assets/name)
        for loc in ROUTES:
            page=site/ROUTES[loc]/'index.html'
            page.parent.mkdir(parents=True,exist_ok=True)
            page.write_text(build(loc,data[loc]),encoding='utf-8')
        for loc in ROUTES:
            for name in HUBS[loc]:
                inject_hub(site/name,loc,data[loc])
    for name in ('course.css','course.js'):
        assert (assets/name).is_file() and (assets/name).read_bytes()==(SRC/name).read_bytes()
    for loc in ROUTES:
        page=site/ROUTES[loc]/'index.html'
        assert page.is_file()
        html=page.read_text(encoding='utf-8')
        for token in ('data-hx-course','hx-quiz-data','hx-cross-grid','hx-case-answer-10','hx-source','hreflang'):
            assert token in html, f'{loc}: missing {token}'
        assert html.count('class="hx-case"')==10
        assert html.count('class="hx-module"')==6
        for hub in HUBS[loc]:
            assert (site/hub).read_text(encoding='utf-8').count('data-hx-feature="1"')==1
    print(f'MANZO AI course: 3 locales, 6 modules, 10 core cases, 10 core quiz questions, {count} crossword letters, 12 sources; verify_only={verify_only}')

if __name__=='__main__':
    arg=argparse.ArgumentParser()
    arg.add_argument('--site',required=True,type=Path)
    arg.add_argument('--verify-only',action='store_true')
    a=arg.parse_args()
    publish(a.site,a.verify_only)
