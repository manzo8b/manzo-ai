#!/usr/bin/env python3
"""Publish MANZO AI · Governing Autonomy in IT, EN and ES.

Source material preserves the original Elena narrative, expanded to six full
readings and translated without abridging outcomes. Four diagrams, a four-stage
Mission Control simulator, eight-word crossword and ten scenario quiz are
generated in each language. Static pages never connect to operational agents.
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
except ImportError as exc:
    raise RuntimeError("markdown==3.10 required by MANZO AI") from exc
from govern_autonomy_i18n import (
    CONTENT,ROOT,BASE,ROUTES,ACADEMY,RESOURCES,PREREQUISITES,
    SOURCE_URLS,MARKER,UI,ACTIONS,QUIZ,
)
SCRIPT=ROOT/"theme/govern-autonomy-course.js"
STYLES=ROOT/"theme/govern-autonomy-course.css"
ASSET_JS="govern-autonomy-course.js"
ASSET_CSS="govern-autonomy-course.css"
HOMES=["it","en","es"]

def e(text):return escape(str(text),quote=True)

def url(loc):
    return "https://manzo8b.github.io/manzo-ai/"+ROUTES[loc]+"/"

def read(loc):
    source=CONTENT/(loc+".md")
    if not source.is_file():raise RuntimeError(loc+": full language source missing")
    content=source.read_text(encoding="utf-8")
    matches=list(re.finditer(r"(?m)^## (?:Lettura|Reading|Lectura) ([1-6]) · ([^\n]+)\n",content))
    if len(matches)!=6 or [int(m.group(1)) for m in matches]!=[1,2,3,4,5,6]:
        raise RuntimeError(loc+": exactly six ordered in-depth readings are required")
    chapters=[]
    for i,m in enumerate(matches):
        end=matches[i+1].start() if i<5 else len(content)
        body=content[m.end():end].strip()
        if len(body)<1800:raise RuntimeError(loc+": reading "+str(i+1)+" is too short")
        chapters.append((m.group(2),body))
    for reference in SOURCE_URLS:
        if reference not in content:
            raise RuntimeError(loc+": primary source absent "+reference)
    if len(content)<19000:raise RuntimeError(loc+": abridged translation")
    return chapters,content

def languages(loc):
    return '<nav class="ga-languages" aria-label="'+e({"it":"Lingue del corso","en":"Course languages","es":"Idiomas del curso"}[loc])+'">'+''.join(
        '<a href="'+BASE+ROUTES[l]+'/" hreflang="'+l+'" lang="'+l+'"'+(' aria-current="page"' if l==loc else '')+'>'+l.upper()+'</a>'
        for l in HOMES)+'</nav>'

def alternatives():
    return ''.join(f'<link rel="alternate" hreflang="{loc}" href="{e(url(loc))}">' for loc in HOMES)+
    '<link rel="alternate" hreflang="x-default" href="'+e(url("it"))+'">'

def steps(nodes,klass):
    return '<ol class="'+klass+'">'+''.join(
        '<li><strong>'+e(name)+'</strong><span>'+e(desc)+'</span></li>' for name,desc in nodes)+'</ol>'

def visual_maps(t):
    one=f'''<section class="ps-shell ga-viz" id="ga-map-action"><p class="ga-eyebrow">{e(t["visual"])} 01 / 04</p>
<h2>{e(t["visual1Title"])}</h2><p>{e(t["visual1Lead"])}</p>{steps(t["v1"],"ga-flow")}
<p class="ga-note">{e(t["visual1Note"])}</p></section>'''
    cards=''.join(
        '<article><span class="ga-level-num">'+e(num)+'</span><strong>'+e(title)+'</strong><p>'+e(meaning)+'</p></article>'
        for num,title,meaning in t["levels"])
    two=f'''<section class="ps-shell ga-viz" id="ga-map-autonomy"><p class="ga-eyebrow">{e(t["visual"])} 02 / 04</p>
<h2>{e(t["visual2Title"])}</h2><p>{e(t["visual2Lead"])}</p><div class="ga-ladder">{cards}</div>
<p class="ga-note">{e(t["levelsNote"])}</p></section>'''
    bands=''.join('<article><strong>'+e(a)+'</strong><p>'+e(b)+'</p></article>' for a,b in t["matrix"])
    three=f'''<section class="ps-shell ga-viz" id="ga-map-boundaries"><p class="ga-eyebrow">{e(t["visual"])} 03 / 04</p>
<h2>{e(t["visual3Title"])}</h2><p>{e(t["visual3Lead"])}</p><div class="ga-impact">{bands}</div>
<p class="ga-note">{e(t["visual3Note"])}</p></section>'''
    flow='<ol class="ga-cycle">'+''.join('<li>'+e(item)+'</li>' for item in t["cycle"])+'</ol>'
    four=f'''<section class="ps-shell ga-viz" id="ga-map-safety-cycle"><p class="ga-eyebrow">{e(t["visual"])} 04 / 04</p>
<h2>{e(t["visual4Title"])}</h2><p>{e(t["visual4Lead"])}</p>{flow}<p class="ga-stop-path">{e(t["cycleStop"])}</p></section>'''
    return one+two+three+four

def crossword(loc,t):
    words=[word for word,clue in t["crossWords"]]
    if len(words)!=8:raise RuntimeError(loc+": expected eight crossword words")
    for word in words:
        if not word.isalpha() or not word.isascii() or word!=word.upper():
            raise RuntimeError(loc+": crossword must use ASCII upper-case entries: "+word)
    board={(0,n):value for n,value in enumerate(words[0])}
    starts=[(0,0,"H")]
    for word in words[1:]:
        options=[]
        for vertical in (True,False):
            for n,char in enumerate(word):
                for (row,col),existing in list(board.items()):
                    if char!=existing:continue
                    row0=row-n if vertical else row
                    col0=col if vertical else col-n
                    seq=[(row0+j,col0) if vertical else (row0,col0+j) for j in range(len(word))]
                    if any(key in board and board[key]!=value for key,value in zip(seq,word)):continue
                    overlap=sum(key in board for key in seq)
                    if not overlap:continue
                    allcells=list(board)+seq
                    ys=[y for y,x in allcells];xs=[x for y,x in allcells]
                    area=(max(ys)-min(ys)+1)*(max(xs)-min(xs)+1)
                    options.append((area,-overlap,int(vertical),row0,col0,seq))
        if not options:raise RuntimeError(loc+": cannot intersect crossword word "+word)
        _,_,vertical,row0,col0,seq=min(options)
        for key,value in zip(seq,word):board[key]=value
        starts.append((row0,col0,"V" if vertical else "H"))
    miny=min(y for y,x in board);maxy=max(y for y,x in board)
    minx=min(x for y,x in board);maxx=max(x for y,x in board)
    cols=maxx-minx+1
    labels={}
    for n,(y,x,orientation) in enumerate(starts,1):
        labels[(y,x)]=str(n) if (y,x) not in labels else labels[(y,x)]+","+str(n)
    cells=[]
    for y in range(miny,maxy+1):
        for x in range(minx,maxx+1):
            if (y,x) not in board:
                cells.append('<span class="ga-cross-blank" aria-hidden="true"></span>');continue
            label=labels.get((y,x))
            index='<span>'+label+'</span>' if label else ""
            desc={"it":"Riga {r}, colonna {c}","en":"Row {r}, column {c}","es":"Fila {r}, columna {c}"}[loc].format(r=y-miny+1,c=x-minx+1)
            cells.append(f'''<label class="ga-cross-cell">{index}<input type="text" maxlength="1" inputmode="text" autocomplete="off"
spellcheck="false" aria-label="{e(desc)}" data-answer="{board[(y,x)]}"></label>''')
    clue_html=[]
    for i,((word,clue),(_,_,direction)) in enumerate(zip(t["crossWords"],starts),1):
        orientation=t["crossDown"] if direction=="V" else t["crossAcross"]
        clue_html.append(f'<li><strong>{i} · {e(orientation)}</strong> {e(clue)} ({len(word)})</li>')
    return f'''<section class="ps-shell ga-crossword" id="ga-crossword">
<p class="ga-eyebrow">{e(t["visual"])} · 08</p><h2>{e(t["crossTitle"])}</h2><p>{e(t["crossLead"])}</p>
<div class="ga-cross-grid"><div class="ga-cross-surface">
<div class="ga-cross-scroll"><div class="ga-cross-board" style="--ga-cols:{cols}" role="group" aria-label="{e(t["crossTitle"])}">{"".join(cells)}</div></div>
<div class="ga-actions"><button class="ga-button" type="button" id="ga-cross-check">{e(t["crossCheck"])}</button>
<button class="ga-button secondary" type="button" id="ga-cross-reset">{e(t["crossReset"])}</button></div>
<p class="ga-status" id="ga-cross-status" role="status" aria-live="polite"></p></div>
<div class="ga-cross-surface"><ol class="ga-clues">{"".join(clue_html)}</ol></div></div></section>'''

def mission(t):
    limits=''.join(f'''<div class="ga-field"><label for="ga-{e(key)}">{e(label)}</label>
<input id="ga-{e(key)}" type="number" min="0" max="1000000" step="1" inputmode="numeric" placeholder="0">
<small>{e(unit)}</small></div>''' for key,label,unit in t["limits"])
    enforcement='<select id="ga-enforcer" aria-label="'+e(t["enforcement"])+'">'+''.join(
        '<option value="'+e(value)+'">'+e(title)+'</option>' for value,title in t["enforcementOptions"])+'</select>'
    rubric='<div id="ga-rubric" role="group" aria-label="'+e(t["rubricHelp"])+'"></div>'
    return f'''<section class="ps-shell ga-lab" id="ga-mission-control">
<div class="ga-lab-top"><span class="ga-lab-brand">MANZO AI / MISSION CONTROL</span><span class="ga-lab-demo">SANDBOX · 100% SIMULATED</span></div>
<h2>{e(t["labTitle"])}</h2><p class="ga-lab-lead">{e(t["labLead"])}</p><p class="ga-flag">{e(t["labPrivacy"])}</p>
<section class="ga-stage" id="ga-station-actions"><h3>{e(t["stations"][0])}</h3><p>{e(t["actionHelp"])}</p>
<div class="ga-action-grid" id="ga-actions"></div><div class="ga-actions"><button type="button" class="ga-button" id="ga-actions-check">{e(t["actionCheck"])}</button></div>
<p id="ga-actions-status" class="ga-status" role="status" aria-live="polite"></p></section>
<section class="ga-stage" id="ga-station-limits"><h3>{e(t["stations"][1])}</h3><p>{e(t["limitHelp"])}</p>
<div class="ga-limit-grid">{limits}</div><div class="ga-limit-meta"><div class="ga-field">
<label for="ga-enforcer">{e(t["enforcement"])}</label>{enforcement}</div>
<div class="ga-field"><label for="ga-owner">{e(t["owner"])}</label>
<input id="ga-owner" type="text" autocomplete="off" maxlength="90" placeholder="{e(t["ownerPlaceholder"])}"></div></div>
<div class="ga-actions"><button type="button" class="ga-button" id="ga-limits-check">{e(t["limitCheck"])}</button></div>
<p id="ga-limits-status" class="ga-status" role="status" aria-live="polite"></p></section>
<section class="ga-stage" id="ga-station-incidents"><h3>{e(t["stations"][2])}</h3><p>{e(t["incidentHelp"])}</p>
<div class="ga-incident-grid" id="ga-incidents"></div><div class="ga-actions"><button type="button" class="ga-button" id="ga-incidents-check">{e(t["incidentCheck"])}</button></div>
<p class="ga-status" id="ga-incidents-status" role="status" aria-live="polite"></p></section>
<section class="ga-stage" id="ga-station-release"><h3>{e(t["stations"][3])}</h3><p>{e(t["rubricHelp"])}</p>
{rubric}<div class="ga-actions"><button type="button" class="ga-button" id="ga-release-check">{e(t["releaseCheck"])}</button></div>
<div id="ga-release" class="ga-release-result" role="status" aria-live="polite" hidden></div>
<p class="ga-note">{e(t["releaseDesc"])}</p></section>
<div class="ga-actions"><button type="button" class="ga-button secondary" id="ga-copy">{e(t["boundaryCopy"])}</button></div>
<p class="ga-status" id="ga-copy-status" role="status" aria-live="polite"></p>
</section>'''

def add_catalog(site,loc,t):
    for section,name in ((ACADEMY[loc],"academy"),(RESOURCES[loc],"resources")):
        page=site/section/"index.html"
        if not page.is_file():raise RuntimeError(loc+": missing Academy or resources listing "+section)
        html=page.read_text(encoding="utf-8")
        if MARKER in html:raise RuntimeError(loc+": duplicate autonomy course listing")
        if "</main>" not in html:raise RuntimeError(loc+": invalid catalog")
        card=f'''<section class="ps-academy-discovery" {MARKER} aria-labelledby="ga-{loc}-{name}-course">
<div class="ps-discovery-top"><span>MANZO AI · {e(t["catalogStatus"])}</span><span>{e(t["pills"][0])}</span></div>
<div class="ps-discovery-content"><div><p class="ps-discovery-kicker">{e(t["catalogStatus"])}</p>
<h2 id="ga-{loc}-{name}-course">{e(t["catalogTitle"])}</h2><p>{e(t["catalogDesc"])}</p></div>
<a class="ps-discovery-cta" href="{BASE}{ROUTES[loc]}/">{e(t["catalogOpen"])} <span aria-hidden="true">↗</span></a></div></section>'''
        html=html.replace("</main>",card+"</main>",1)
        if "prompt-vs-skill.css" not in html:
            html=html.replace("</head>",f'<link rel="stylesheet" href="{BASE}assets/prompt-vs-skill.css"></head>',1)
        page.write_text(html,encoding="utf-8")

def make_page(site,loc):
    t=UI[loc]
    chapters,source=read(loc)
    cards=[];panels=[]
    for n,(heading,body) in enumerate(chapters,1):
        slug="ga-reading-"+str(n)
        cards.append(f'<a class="ps-toc-card" href="#{slug}" data-open-reading="{slug}"><span class="ps-toc-count">{e(t["reading"])}</span><strong>{e(t["chapters"][n-1])}</strong><small>{e(t["open"])} ↗</small></a>')
        html=markdown.markdown(body,extensions=["fenced_code","tables","sane_lists"])
        panels.append(f'''<section class="ps-reading" id="{slug}"><details {"open" if n==1 else ""}><summary>
<span class="ps-reading-index">{e(t["reading"])} <em>{n} / 6</em></span><span class="ps-reading-title">{e(heading)}</span><span class="ps-reading-toggle" aria-hidden="true">+</span></summary>
<div class="ps-reading-copy">{html}
<label class="ps-completion"><input type="checkbox" class="ps-read-check"> {e(t["done"])}</label>
<a class="ps-back" href="#ga-readings">{e(t["back"])} ↑</a></div></details></section>''')
    payload={
        "ui":{key:t[key] for key in (
            "progress","choices","actionCorrect","actionWarning",
            "limits","enforcement","owner","incidentSelect","incidentGood","incidentBad",
            "incidentCheck","limitGood","limitBad","go","revise","stop","releaseDesc",
            "boundaryTitle","copyOk","copyFail","stations","rubricCriteria","rubricOptions",
            "releaseCheck","crossCells","crossGood","crossBad","crossCleared",
            "quizCorrect","quizReview","quizExpected","quizResult","quizAnswered",
            "quizEnd","quizSubmit",
        )},
        "actions":[{"label":label,"expected":expected,"why":why} for label,expected,why in ACTIONS[loc]],
        "incidents":[{"title":title,"setup":setup,"options":options,"answer":answer,"why":why}
                     for title,setup,options,answer,why in t["incidentScenarios"]],
        "quiz":[{"q":question,"options":options,"answer":correct,"why":why}
                for question,options,correct,why in QUIZ[loc]],
    }
    data_json=json.dumps(payload,ensure_ascii=False).replace("<","\\u003c")
    schema={"@context":"https://schema.org","@type":"Course","name":t["title"]+" — "+t["subtitle"],
            "description":t["lead"],"inLanguage":loc,"isAccessibleForFree":True,
            "url":url(loc),"provider":{"@type":"Organization","name":"MANZO AI"},
            "datePublished":"2026-11-20","citation":SOURCE_URLS}
    schema_json=json.dumps(schema,ensure_ascii=False).replace("<","\\u003c")
    alternate=''.join(f'<link rel="alternate" hreflang="{code}" href="{e(url(code))}">' for code in HOMES)
    alternate+=f'<link rel="alternate" hreflang="x-default" href="{e(url("it"))}">'
    hero_pills=''.join('<span>'+e(p)+'</span>' for p in t["pills"])
    html=f'''<!doctype html><html lang="{loc}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(t["title"])} · MANZO AI</title><meta name="description" content="{e(t["lead"])}">
<meta name="robots" content="index,follow"><meta name="theme-color" content="#ffffff">
<link rel="canonical" href="{e(url(loc))}">{alternate}
<meta property="og:type" content="article"><meta property="og:title" content="{e(t["title"])}"><meta property="og:url" content="{e(url(loc))}">
<link rel="stylesheet" href="{BASE}assets/prompt-vs-skill.css">
<link rel="stylesheet" href="{BASE}assets/{ASSET_CSS}">
<script type="application/ld+json">{schema_json}</script></head>
<body data-ma-prompt-skill="course-v1" data-ga-course="v1"><a class="ps-skip" href="#ga-main">{e(t["skip"])}</a>
<header class="ps-topbar"><div class="ps-shell ps-topbar-row"><a class="ps-brand" href="{BASE}{loc}/">MANZO<span>AI</span></a>
<nav aria-label="{e(t["courseNav"])}"><a href="{BASE}{ACADEMY[loc]}/">{e(t["academy"])}</a>
<a href="#ga-readings">{e(t["navRead"])}</a><a href="#ga-mission-control">{e(t["navLab"])}</a>
<a href="#ga-quiz-section">{e(t["navQuiz"])}</a></nav></div></header>
<main id="ga-main"><section class="ps-hero ga-hero"><div class="ps-shell">{languages(loc)}
<p class="ps-eyebrow">{e(t["eyebrow"])}</p><p class="ps-context">{e(t["tagline"])}</p>
<h1>{t["hero"]}</h1><p class="ps-subtitle">{e(t["lead"])}</p>
<div class="ps-hero-bottom">{hero_pills}</div>
<a class="ps-main-cta" href="#ga-readings">{e(t["start"])} ↘</a></div></section>
<div class="ps-shell"><div class="ga-prereq"><a href="{BASE}{PREREQUISITES[loc]}/">{e(t["prereq"])} ↗</a>
<p>{e(t["prereqText"])}</p></div><p class="ga-flag">{e(t["notice"])}</p></div>
<section class="ps-shell ps-guide" id="ga-readings"><div class="ps-section-heading"><div>
<p class="ps-overline">MANZO AI · AI ACADEMY</p><h2>{e(t["readings"])}</h2></div><p>{e(t["readLead"])}</p></div>
<div class="ps-toc">{"".join(cards)}</div><p id="ga-reading-progress" class="ps-counter" role="status" aria-live="polite">0 / 6</p></section>
<div class="ps-shell ps-readings">{"".join(panels)}</div>
{visual_maps(t)}
{mission(t)}
{crossword(loc,t)}
<section class="ps-shell ga-quiz-section" id="ga-quiz-section"><p class="ga-eyebrow">{e(t["navQuiz"])}</p>
<h2>{e(t["quizTitle"])}</h2><p>{e(t["quizLead"])}</p><div id="ga-quiz"></div>
<script type="application/json" id="ga-data">{data_json}</script></section>
<section class="ps-shell ga-finish"><h2>{e(t["finish"])}</h2>
<p>{e(t["releaseDesc"])}</p><p>{e(t["footer"])}</p>
<a href="{BASE}{PREREQUISITES[loc]}/">{e(t["related"])} ↗</a></section></main>
<footer class="ps-footer"><div class="ps-shell"><p><strong>MANZO AI</strong> · {e(t["title"])}</p><p>{e(t["footer"])}</p>
<a href="{BASE}{ACADEMY[loc]}/">{e(t["academy"])}</a></div></footer>
<script src="{BASE}assets/{ASSET_JS}" defer></script></body></html>'''
    dest=site/ROUTES[loc]/"index.html";dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(html,encoding="utf-8")

def verify(site):
    for loc in HOMES:
        file=site/ROUTES[loc]/"index.html"
        if not file.is_file():raise RuntimeError(loc+": page missing")
        page=file.read_text(encoding="utf-8")
        if page.count('class="ps-reading"')!=6 or page.count('class="ps-toc-card"')!=6:
            raise RuntimeError(loc+": missing one of six full readings")
        for marker in ("ga-map-action","ga-map-autonomy","ga-map-boundaries","ga-map-safety-cycle",
                       "ga-mission-control","ga-station-actions","ga-station-limits","ga-station-incidents",
                       "ga-station-release","ga-crossword","ga-quiz-section"):
            if page.count('id="'+marker+'"')!=1:raise RuntimeError(loc+": missing "+marker)
        if page.count('class="ga-cross-cell"')<25:raise RuntimeError(loc+": crossword grid missing")
        for language in HOMES:
            if 'hreflang="'+language+'"' not in page:raise RuntimeError(loc+": language alternates missing")
        data=json.loads(re.search(r'<script type="application/json" id="ga-data">(.+?)</script>',page).group(1))
        if len(data["quiz"])!=10 or len(data["actions"])!=8 or len(data["incidents"])!=4:
            raise RuntimeError(loc+": incomplete Mission Control or quiz")
        for section in (ACADEMY[loc],RESOURCES[loc]):
            content=(site/section/"index.html").read_text(encoding="utf-8")
            if content.count(MARKER)!=1 or BASE+ROUTES[loc]+"/" not in content:
                raise RuntimeError(loc+": missing Academy or resources discovery")
    for name in (ASSET_JS,ASSET_CSS):
        if not (site/"assets"/name).is_file():raise RuntimeError("Missing "+name)
    print("Governing Autonomy: 3 complete languages, 18 readings, 12 diagrams, 24 permission cases, 12 incidents, 3 crosswords, 30 quiz items PASS")

def publish(site):
    for src,name in ((SCRIPT,ASSET_JS),(STYLES,ASSET_CSS)):
        if not src.is_file():raise RuntimeError("Missing source "+str(src))
        (site/"assets").mkdir(parents=True,exist_ok=True)
        shutil.copy2(src,site/"assets"/name)
    for loc in HOMES:
        make_page(site,loc)
        add_catalog(site,loc,UI[loc])
    verify(site)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--site",required=True,type=Path)
    parser.add_argument("--verify-only",action="store_true")
    args=parser.parse_args()
    verify(args.site) if args.verify_only else publish(args.site)
