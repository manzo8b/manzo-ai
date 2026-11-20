#!/usr/bin/env python3
"""MANZO AI · complete EN/ES localisation of two existing Italian courses.

The original Italian full-feature courses are preserved. Their visible
language selectors are added non-destructively. Translated pages contain all
six substantial readings, translated 4-diagram learning maps, task-specific
interactive laboratories, 10 explained quiz cases and native-language labels.
"""
from __future__ import annotations
import argparse
from html import escape
import json
from pathlib import Path
import re
import shutil

try:
    import markdown
except ImportError as ex:
    raise RuntimeError("markdown==3.10 is required") from ex
from legacy_learning_i18n import ROOT, BASE, COURSES, ACADEMY, RESOURCES, SHARED, UI

STYLES=ROOT/"theme/legacy-learning-i18n.css"
SCRIPT=ROOT/"theme/legacy-learning-i18n.js"
CSS_NAME="legacy-learning-i18n.css"
JS_NAME="legacy-learning-i18n.js"
REGIONS=("en","es")
KIND_LIST=("reliability","centroni")
COURSE_ROOT="https://manzo8b.github.io/manzo-ai/"

def e(x):return escape(str(x),quote=True)
def url(kind,locale):return BASE+COURSES[kind]["routes"][locale]+"/"
def absolute(kind,locale):return COURSE_ROOT+COURSES[kind]["routes"][locale]+"/"

def read_source(kind,loc):
    cfg=COURSES[kind];p=cfg["source"]/(loc+".md")
    if not p.is_file():raise RuntimeError(f"Missing {kind} native {loc} source: {p}")
    txt=p.read_text(encoding="utf-8")
    if len(txt)<cfg["min_chars"]:raise RuntimeError(f"{kind}/{loc} source abbreviated")
    heading="Reading" if loc=="en" else "Lectura"
    pattern=r"(?m)^## "+heading+r" ([1-6]) · ([^\n]+)\n"
    matches=list(re.finditer(pattern,txt))
    if len(matches)!=6 or [int(m.group(1)) for m in matches]!=[1,2,3,4,5,6]:
        raise RuntimeError(f"{kind}/{loc}: six ordered reading headings required")
    intro=txt[:matches[0].start()].strip()
    title_line=intro.splitlines()[0] if intro else ""
    intro=intro[len(title_line):].strip()
    readings=[];toolkit=""
    toolkit_label="Operational toolkit" if loc=="en" else "Herramientas operativas"
    for i,m in enumerate(matches):
        block=txt[m.end():matches[i+1].start() if i<5 else len(txt)].strip()
        if i==5:
            split=re.search(r"(?m)^## "+toolkit_label+r"\s*$",block)
            if not split:raise RuntimeError(f"{kind}/{loc}: missing reference toolkit")
            toolkit=block[split.end():].strip()
            block=block[:split.start()].strip()
        if len(block)<1800:raise RuntimeError(f"{kind}/{loc}: abridged reading {i+1}")
        readings.append((m.group(2),block))
    if len(toolkit)<650:raise RuntimeError(f"{kind}/{loc}: incomplete toolkit")
    return intro,readings,toolkit

def md(s):return markdown.markdown(s,extensions=["tables","fenced_code","sane_lists"])
def language_switch(kind,loc):
    t=SHARED[loc]
    return '<nav class="lgi-langs" aria-label="'+e(t["sitemap"])+'">'+''.join(
        '<a href="'+e(url(kind,l))+'" lang="'+l+'" hreflang="'+l+'"'+
        (' aria-current="page"' if l==loc else '')+'>'+l.upper()+'</a>' for l in ("it","en","es"))+'</nav>'
def links(kind):
    return ''.join('<link rel="alternate" hreflang="'+l+'" href="'+e(absolute(kind,l))+'">' for l in ("it","en","es"))+\
           '<link rel="alternate" hreflang="x-default" href="'+e(absolute(kind,"it"))+'">'

def visual(kind,loc,i):
    title,description,steps=UI[kind][loc]["maps"][i]
    parts=[]
    for j,txt in enumerate(steps,1):
        parts.append('<li><span>'+f"{j:02d}"+'</span><strong>'+e(txt)+'</strong></li>')
    return f'''<figure class="lgi-viz" id="lgi-map-{i+1}">
<figcaption><small>MANZO AI / VISUAL {i+1} / 04</small><strong>{e(title)}</strong>
<span>{e(description)}</span></figcaption>
<ol>{"".join(parts)}</ol></figure>'''

def button(text,id,secondary=False):
    return f'<button type="button" id="{id}" class="ft-button{" ft-secondary" if secondary else ""}">{e(text)}</button>'

def score_select(kind,loc,id,score):
    t=UI[kind][loc]
    if not score:
        options=[("",SHARED[loc]["tab"])]
    else:
        options=[("",t["choose"])]+[(str(i),str(i)) for i in range(3)]
    return f'<select id="{e(id)}" aria-label="{e(id)}">'+''.join(
        f'<option value="{e(k)}">{e(v)}</option>' for k,v in options)+'</select>'

def reliability_lab(loc):
    t=UI["reliability"][loc];s=SHARED[loc]
    cards=[]
    for i,(title,fixture,expectation) in enumerate(t["cases"]):
        scores=[]
        for j,criterion in enumerate(t["rubric"]):
            scores.append('<div class="lgi-score"><label for="lgi-r-'+str(i)+'-'+str(j)+'">'+
             e(criterion)+'</label>'+score_select("reliability",loc,"lgi-r-"+str(i)+"-"+str(j),True)+'</div>')
        cards.append(f'''<section class="lgi-case" id="lgi-case-{i+1}"><p class="ft-overline">0{i+1} / 04</p>
<h3>{e(title)}</h3><blockquote>{e(fixture)}</blockquote><p><strong>{e(expectation)}</strong></p>
<div class="lgi-scores">{"".join(scores)}</div></section>''')
    return f'''<section class="ps-shell ft-lab" id="lgi-lab"><p class="ft-overline">MANZO AI / WORKSHOP</p>
<h2>{e(t["labTitle"])}</h2><p class="ft-lab-lead">{e(t["labLead"])}</p>
<p class="ft-privacy">{e(s["note"])}</p>
<div class="lgi-case-grid">{"".join(cards)}</div>
<p class="lgi-note">{e(t["criterion"])}. {e(t["caseNote"])}</p>
<div class="lgi-fields"><label for="lgi-source">{e(t["source"])}</label>
<input type="text" id="lgi-source" maxlength="140" placeholder="{e(t["sourceHint"])}">
<label for="lgi-owner">{e(t["role"])}</label>
<input type="text" id="lgi-owner" maxlength="140" placeholder="{e(t["roleHint"])}">
<label for="lgi-review">{e(t["review"])}</label>
<textarea id="lgi-review" rows="4" maxlength="1800" placeholder="{e(t["reviewHint"])}"></textarea></div>
<div class="ft-actions">{button(s["approve"],"lgi-evaluate")}{button(s["copy"],"lgi-copy",True)}</div>
<p class="ft-release-result" role="status" aria-live="polite" id="lgi-decision" hidden></p>
<p class="ft-result" role="status" aria-live="polite" id="lgi-copy-status" hidden></p></section>'''

def centroni_lab(loc):
    t=UI["centroni"][loc];s=SHARED[loc]
    phases=''.join('<article class="lgi-phase"><span>0'+str(i+1)+'</span><strong>'+e(name)+'</strong><p>'+e(desc)+'</p></article>' for i,(name,desc) in enumerate(t["phases"]))
    fields=''.join('<div class="ft-field"><label for="lgi-'+e(key)+'">'+e(name)+'</label>'+
      ('<textarea rows="3" maxlength="1100" id="lgi-'+e(key)+'" placeholder="'+e(hint)+'"></textarea>' if key in ("problem","process","limits","measure")
       else '<input type="text" maxlength="350" id="lgi-'+e(key)+'" placeholder="'+e(hint)+'">')+
       '</div>' for key,name,hint in t["fields"])
    scenarios=''.join(f'<button type="button" class="lgi-scenario ft-button ft-secondary" data-scenario="{i}">{e(title)}</button>' for i,(title,category,message) in enumerate(t["scenarios"]))
    checks=''.join(f'<label class="lgi-qa"><input type="checkbox" class="lgi-check" data-i="{i}"> {e(name)}</label>' for i,name in enumerate(t["checks"]))
    return f'''<section class="ps-shell ft-lab" id="lgi-lab"><p class="ft-overline">MANZO AI / WORKSHOP</p>
<h2>{e(t["labTitle"])}</h2><p class="ft-lab-lead">{e(t["labLead"])}</p>
<p class="ft-privacy">{e(s["note"])}</p>
<div class="lgi-phases">{phases}</div>
<div class="lgi-fields-grid" id="lgi-blueprint">{fields}</div>
<div class="lgi-simulator"><h3>{e(t["scenarioTitle"])}</h3><p>{e(t["scenarioLead"])}</p>
<div class="ft-actions">{scenarios}</div>
<p class="lgi-scenario-output" id="lgi-scenario-output" role="status" aria-live="polite"></p>
<p class="lgi-official">{e(t["noOfficial"])}</p></div>
<div class="lgi-qa-list"><h3>{e(s["test"])}</h3><p>{e(t["rubric"])}</p>{checks}</div>
<div class="ft-field"><label for="lgi-owner">{e(t["staff"])}</label>
<input type="text" id="lgi-owner" maxlength="140" placeholder="{e(t["staffHint"])}"></div>
<div class="ft-actions">{button(s["approve"],"lgi-evaluate")}{button(s["copy"],"lgi-copy",True)}</div>
<p class="ft-release-result" role="status" aria-live="polite" id="lgi-decision" hidden></p>
<p class="ft-result" role="status" aria-live="polite" id="lgi-copy-status" hidden></p></section>'''

def quiz(kind,loc):
    title=SHARED[loc]["quiz"];return f'''<section class="ps-shell ft-quiz-section" id="lgi-quiz">
<p class="ft-overline">MANZO AI / REVIEW</p><h2>{e(title)}</h2>
<div id="lgi-quiz-host"></div></section>'''

def page(site,kind,loc):
    t=UI[kind][loc];s=SHARED[loc];cfg=COURSES[kind]
    intro,readings,toolkit=read_source(kind,loc)
    toc=[];chapters=[]
    for i,(title,body) in enumerate(readings,1):
        rid=f"lgi-reading-{i}"
        toc.append(f'''<a class="ps-toc-card" href="#{rid}" data-open-reading="{rid}">
<span class="ps-toc-count">{e(s["reading"])} {i}/6</span><strong>{e(t["short"][i-1])}</strong>
<small>{e(s["read"])} <span aria-hidden="true">↗</span></small></a>''')
        visual_html=visual(kind,loc,i-1) if i<=4 else ""
        chapters.append(f'''<section class="ps-reading" id="{rid}"><details {"open" if i==1 else ""}>
<summary><span class="ps-reading-index">{e(s["reading"])} <em>{i} / 6</em></span>
<span class="ps-reading-title">{e(title)}</span><span class="ps-reading-toggle" aria-hidden="true">+</span></summary>
<div class="ps-reading-copy">{md(body)}{visual_html}
<label class="ps-completion"><input type="checkbox" class="ps-read-check"> {e(s["done"])}</label>
<a href="#lgi-readings" class="ps-back">{e(s["back"])} ↑</a></div></details></section>''')
    data={"type":kind,"ui":{**s,**t},"quiz":[{"q":q,"options":opts,"answer":ans,"why":why} for q,opts,ans,why in t["quiz"]]}
    if len(data["quiz"])!=10:raise RuntimeError(kind+"/"+loc+": ten quizzes required")
    payload=json.dumps(data,ensure_ascii=False).replace("<","\\u003c")
    schema=json.dumps({"@context":"https://schema.org","@type":"Course","name":t["title"],
          "description":t["lead"],"url":absolute(kind,loc),"inLanguage":loc,
          "isAccessibleForFree":True,"provider":{"@type":"Organization","name":"MANZO AI"}},ensure_ascii=False).replace("<","\\u003c")
    lab_html=reliability_lab(loc) if kind=="reliability" else centroni_lab(loc)
    html=f'''<!doctype html><html lang="{loc}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(t["title"])} · MANZO AI</title>
<meta name="description" content="{e(t["lead"])}">
<meta name="robots" content="index,follow"><meta name="theme-color" content="#ffffff">
<link rel="canonical" href="{e(absolute(kind,loc))}">{links(kind)}
<link rel="stylesheet" href="{BASE}assets/prompt-vs-skill.css">
<link rel="stylesheet" href="{BASE}assets/final-two-courses.css">
<link rel="stylesheet" href="{BASE}assets/{CSS_NAME}">
<script type="application/ld+json">{schema}</script></head>
<body data-ma-prompt-skill="course-v1" data-ma-legacy-course="{e(kind)}" data-lgi-version="v1">
<a class="ps-skip" href="#lgi-main">{e(s["start"])}</a>
<header class="ps-topbar"><div class="ps-shell ps-topbar-row"><a class="ps-brand" href="{BASE}{loc}/">MANZO<span>AI</span></a>
<nav aria-label="{e(s["outline"])}"><a href="{BASE}{ACADEMY[loc]}/">Academy</a>
<a href="#lgi-readings">{e(s["lessons"])}</a><a href="#lgi-lab">{e(s["lab"])}</a>
<a href="#lgi-quiz">{e(s["quiz"])}</a></nav></div></header>
<main id="lgi-main">
<section class="ps-hero ft-hero lgi-hero lgi-hero-{kind}"><div class="ps-shell">
{language_switch(kind,loc)}<p class="ps-eyebrow">MANZO AI / {e(s["course"])}</p>
<p class="ps-context">{e(t["subtitle"])}</p><h1>{t["hero"]}</h1>
<p class="ps-subtitle">{e(t["lead"])}</p>
<div class="ps-hero-bottom"><span>06 / {e(s["lessons"])}</span><span>{e(s["lab"])}</span><span>10 / {e(s["quiz"])}</span></div>
<a class="ps-main-cta" href="#lgi-readings">{e(s["start"])} <span aria-hidden="true">↘</span></a>
</div></section>
<section class="ps-shell ft-related"><p>{e(t["intro"])}</p></section>
<section class="ps-shell ft-overview"><details><summary>{e(s["outline"])} <span aria-hidden="true">+</span></summary>
<div class="ft-markdown">{md(intro)}</div></details></section>
<section class="ps-shell ps-guide" id="lgi-readings"><div class="ps-section-heading">
<div><p class="ps-overline">MANZO AI / ACADEMY</p><h2>{e(s["lessons"])}</h2></div>
<p>{e(s["summary"])}</p></div><div class="ps-toc">{"".join(toc)}</div>
<p class="ps-counter" id="lgi-progress" aria-live="polite" role="status">0 / 6</p></section>
<div class="ps-shell ps-readings">{"".join(chapters)}</div>
{lab_html}
<section class="ps-shell ft-tools" id="lgi-sources"><details><summary>{e(s["sources"])} <span aria-hidden="true">+</span></summary>
<div class="ft-markdown">{md(toolkit)}</div></details></section>
{quiz(kind,loc)}
<section class="ps-shell ft-conclusion"><h2>{e(t["title"])}</h2>
<p>{e(s["noCert"])}</p><a href="{BASE}{ACADEMY[loc]}/">{e(s["backAcademy"])} ↗</a></section>
</main><footer class="ps-footer"><div class="ps-shell">MANZO AI · {e(s["sourceNote"])}</div></footer>
<script type="application/json" id="lgi-payload">{payload}</script>
<script src="{BASE}assets/{JS_NAME}" defer></script></body></html>'''
    dest=site/cfg["routes"][loc]/"index.html"
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(html,encoding="utf-8")

def catalog(site,kind,loc):
    cfg=COURSES[kind];t=UI[kind][loc];s=SHARED[loc]
    for folder in (ACADEMY[loc],RESOURCES[loc]):
        target=site/folder/"index.html"
        if not target.is_file():raise RuntimeError("Missing "+str(target))
        html=target.read_text(encoding="utf-8")
        if cfg["marker"] in html:raise RuntimeError("Duplicate "+kind+" in "+loc+" catalogue")
        label=f"lgi-{kind}-{loc}-{folder.replace('/','-')}"
        card=f'''<section class="ps-academy-discovery" {cfg["marker"]} aria-labelledby="{label}">
<div class="ps-discovery-top"><span>MANZO AI · {e(s["course"])}</span><span>{e(s["free"])}</span></div>
<div class="ps-discovery-content"><div><p class="ps-discovery-kicker">{e(s["tag"])}</p>
<h2 id="{label}">{e(t["title"])}</h2><p>{e(t["home"])}</p></div>
<a href="{url(kind,loc)}" class="ps-discovery-cta">{e(s["homeOpen"])} <span aria-hidden="true">↗</span></a>
</div></section>'''
        if "</main>" not in html:raise RuntimeError("Missing main in "+str(target))
        html=html.replace("</main>",card+"</main>",1)
        if "prompt-vs-skill.css" not in html:
            html=html.replace("</head>",f'<link rel="stylesheet" href="{BASE}assets/prompt-vs-skill.css"></head>',1)
        target.write_text(html,encoding="utf-8")

def upgrade_it(site,kind):
    dest=site/COURSES[kind]["routes"]["it"]/"index.html"
    if not dest.is_file():raise RuntimeError("Italian course not published "+kind)
    html=dest.read_text(encoding="utf-8")
    if 'data-lgi-switch="v1"' in html:raise RuntimeError("Double Italian language switch")
    html=html.replace("</head>",f'<link rel="stylesheet" href="{BASE}assets/{CSS_NAME}">{links(kind)}</head>',1)
    block='<div class="lgi-italian-switch" data-lgi-switch="v1"><nav class="lgi-langs" aria-label="Lingue del corso">'+\
          ''.join('<a href="'+url(kind,lang)+'" hreflang="'+lang+'" lang="'+lang+'"'+
           (' aria-current="page"' if lang=="it" else '')+'>'+lang.upper()+'</a>' for lang in ("it","en","es"))+'</nav></div>'
    main=re.search(r"<main\b[^>]*>",html)
    if not main:raise RuntimeError(kind+": no Italian main tag")
    html=html[:main.end()]+block+html[main.end():]
    dest.write_text(html,encoding="utf-8")

def verify(site):
    for kind,cfg in COURSES.items():
        for loc in REGIONS:
            route=site/cfg["routes"][loc]/"index.html"
            if not route.is_file():raise RuntimeError(kind+"/"+loc+": course missing")
            doc=route.read_text(encoding="utf-8")
            if doc.count('class="ps-reading"')!=6 or doc.count('class="ps-toc-card"')!=6:
                raise RuntimeError(kind+"/"+loc+": six readings or navigation not present")
            if doc.count('class="lgi-viz"')!=4:raise RuntimeError(kind+"/"+loc+": four visuals absent")
            if doc.count('<script type="application/json" id="lgi-payload">')!=1:
                raise RuntimeError(kind+"/"+loc+": translated interactive payload missing")
            script=re.search(r'<script type="application/json" id="lgi-payload">(.*?)</script>',doc)
            data=json.loads(script.group(1)) if script else {}
            if len(data.get("quiz",[]))!=10:raise RuntimeError(kind+"/"+loc+": assessment incomplete")
            if kind=="reliability":
                if doc.count('class="lgi-case"')!=4 or doc.count('class="lgi-score"')!=12:
                    raise RuntimeError(kind+"/"+loc+": four tests and 12 ratings required")
            if kind=="centroni":
                if doc.count('class="lgi-phase"')!=6 or doc.count('class="lgi-qa"')!=5:
                    raise RuntimeError(kind+"/"+loc+": phases and QA cases missing")
                if doc.count('class="ft-field"')<8 or doc.count('class="lgi-scenario ft-button')!=4:
                    raise RuntimeError(kind+"/"+loc+": blueprint and civic simulation missing")
            for lang in ("it","en","es"):
                if f'hreflang="{lang}"' not in doc:raise RuntimeError("Missing hreflang")
            for folder in (ACADEMY[loc],RESOURCES[loc]):
                cat=(site/folder/"index.html").read_text(encoding="utf-8")
                if cat.count(cfg["marker"])!=1 or url(kind,loc) not in cat:
                    raise RuntimeError(kind+"/"+loc+": untranslated catalog")
        it=(site/cfg["routes"]["it"]/"index.html").read_text(encoding="utf-8")
        if it.count('data-lgi-switch="v1"')!=1:
            raise RuntimeError(kind+": Italian switch absent")
        if any('hreflang="'+lang+'"' not in it for lang in REGIONS):
            raise RuntimeError(kind+": Italian hreflang absent")
    for name in (JS_NAME,CSS_NAME):
        if not (site/"assets"/name).is_file():raise RuntimeError("Missing "+name)
    print("Legacy learning translation: 2 courses × full EN/ES; 24 deep readings; 16 graphics; reliability 8 stress tests/24 ratings; civic 12 phases/8 scenarios; 40 explained quiz questions PASS")

def publish(site):
    (site/"assets").mkdir(parents=True,exist_ok=True)
    for src,name in ((STYLES,CSS_NAME),(SCRIPT,JS_NAME)):
        if not src.is_file():raise RuntimeError("Missing asset source "+str(src))
        shutil.copy2(src,site/"assets"/name)
    for kind in KIND_LIST:
        for loc in REGIONS:
            page(site,kind,loc)
            catalog(site,kind,loc)
        upgrade_it(site,kind)
    verify(site)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--site",type=Path,required=True)
    p.add_argument("--verify-only",action="store_true")
    opts=p.parse_args()
    verify(opts.site) if opts.verify_only else publish(opts.site)
