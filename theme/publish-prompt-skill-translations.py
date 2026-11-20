#!/usr/bin/env python3
"""Publish complete English + Spanish Prompt vs Skill course with learning parity.

Italian original remains unchanged except its corrected canonical URL, a
language switcher and reciprocal hreflang. English/Spanish translations
include all 6 deep readings, four translated graphics, a workshop, eight-word
crossword and ten-question quiz with explanatory feedback. No AI at runtime.
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
    raise RuntimeError("Markdown is required by deploy-pages.yml") from ex
from prompt_skill_i18n import ROUTES, ACADEMY, RESOURCES, BASE, HEADINGS, UI, QUIZ, CROSS

ROOT=Path(__file__).resolve().parent.parent
ED=ROOT/"editorial/learning/prompt-vs-skill"
JS=ROOT/"theme/prompt-skill-translated.js"
STYLES=ROOT/"editorial/learning/prompt-vs-skill/course.css"
ASSET="prompt-skill-translated.js"
CSS_NAME="prompt-skill-i18n.css"
MARKER='data-ma-prompt-skill-translated="v1"'
LINKS={
"it":"https://manzo8b.github.io/manzo-ai/"+ROUTES["it"]+"/",
"en":"https://manzo8b.github.io/manzo-ai/"+ROUTES["en"]+"/",
"es":"https://manzo8b.github.io/manzo-ai/"+ROUTES["es"]+"/",
}
SOURCES=[
 "https://developers.openai.com/api/docs/guides/prompt-engineering",
 "https://agentskills.io/specification",
 "https://help.openai.com/en/articles/20001256-plugins-in-chatgpt",
 "https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax",
 "https://www.unesco.org/en/articles/ai-competency-framework-students",
]

def e(value):return escape(str(value),quote=True)

def read(locale):
    file=ED/(locale+".md")
    if not file.is_file():raise RuntimeError(locale+": translated content missing")
    data=file.read_text(encoding="utf-8")
    indexes=[]
    for heading in HEADINGS[locale]:
        token="## "+heading+"\n"
        i=data.find(token)
        if i<0 or indexes and i<=indexes[-1]:
            raise RuntimeError(locale+": reading missing or out of order: "+heading)
        indexes.append(i)
    parts=[]
    for ix,title in enumerate(HEADINGS[locale]):
        start=indexes[ix]+len("## "+title+"\n")
        end=indexes[ix+1] if ix+1<len(indexes) else len(data)
        body=data[start:end].strip()
        if len(body)<2100:raise RuntimeError(locale+": insufficient reading depth: "+title)
        parts.append((title,body))
    for source in SOURCES:
        if source not in data:raise RuntimeError(locale+": primary source missing: "+source)
    if len(data)<20000:raise RuntimeError(locale+": translated material substantially abbreviated")
    return parts

def hreflangs():
    return "".join(f'<link rel="alternate" hreflang="{lang}" href="{e(url)}">' for lang,url in LINKS.items())+f'<link rel="alternate" hreflang="x-default" href="{e(LINKS["it"])}">'

def language_nav(locale):
    label={"it":"Lingue del corso","en":"Course languages","es":"Idiomas del curso"}[locale]
    links=[]
    for lang,url in LINKS.items():
        current=' aria-current="page"' if lang==locale else ""
        links.append(f'<a href="{e(url)}" lang="{lang}" hreflang="{lang}"{current}>{lang.upper()}</a>')
    return '<nav class="ps-i18n-languages" aria-label="'+e(label)+'">'+"".join(links)+'</nav>'

def visual_prompt(t):
    children=[]
    for n,(title,description) in enumerate(zip(t["pElements"],t["pDescriptions"]),1):
        children.append(f'<li><span class="ps-viz-index">{n:02d}</span><strong>{e(title)}</strong><small>{e(description)}</small></li>')
    return f'''<figure class="ps-viz ps-viz--prompt" id="mappa-prompt" aria-labelledby="ps-viz-prompt-title">
<figcaption><span class="ps-viz-eyebrow">{e(t["mapEyebrow"])} / 01</span><strong id="ps-viz-prompt-title">{e(t["pTitle"])}</strong><span>{e(t["pLead"])}</span></figcaption>
<ol class="ps-viz-prompt-grid">{"".join(children)}</ol>
<div class="ps-viz-conclusion"><span aria-hidden="true">✓</span><p>{e(t["pConclusion"])}</p></div></figure>'''

def visual_decision(t):
    nodes=[]
    for i,(question,answer,description) in enumerate(t["decision"],1):
        if i>1:nodes.append('<div class="ps-viz-decision-down"><span>↓</span></div>')
        nodes.append(f'''<div class="ps-viz-decision-row"><div class="ps-viz-question"><span>{i:02d}</span><strong>{e(question)}</strong></div>
<div class="ps-viz-decision-answer"><span class="ps-viz-branch-tag">→</span><strong>{e(answer)}</strong><small>{e(description)}</small></div></div>''')
    return f'''<figure class="ps-viz ps-viz--decision" id="mappa-salto" aria-labelledby="ps-viz-decision-title">
<figcaption><span class="ps-viz-eyebrow">{e(t["mapEyebrow"])} / 02</span><strong id="ps-viz-decision-title">{e(t["decisionTitle"])}</strong><span>{e(t["decisionLead"])}</span></figcaption>
<div class="ps-viz-decision-track">{"".join(nodes)}</div><p class="ps-viz-footnote">{e(t["decisionFinal"])}</p></figure>'''

def visual_skill(t):
    rows=[]
    for ix,(name,description) in enumerate(t["skillItems"]):
        rows.append(f'<div class="ps-i18n-skill-item"><span>{ix+1:02d}</span><strong>{e(name)}</strong><small>{e(description)}</small></div>')
    return f'''<figure class="ps-viz ps-viz--skill" id="mappa-skill" aria-labelledby="ps-viz-skill-title">
<figcaption><span class="ps-viz-eyebrow">{e(t["mapEyebrow"])} / 03</span><strong id="ps-viz-skill-title">{e(t["skillTitle"])}</strong><span>{e(t["skillLead"])}</span></figcaption>
<div class="ps-i18n-skill-items">{"".join(rows)}</div>
<div class="ps-viz-conclusion"><span aria-hidden="true">✓</span><p>{e(t["skillFinal"])}</p></div></figure>'''

def visual_family(t):
    domains=[]
    for name,description in t["familyDomains"]:
        domains.append(f'<div><span aria-hidden="true">◇</span><strong>{e(name)}</strong><small>{e(description)}</small></div>')
    steps=[]
    for i,(name,description) in enumerate(t["familySteps"],1):
        steps.append(f'<li><span>{i:02d}</span><strong>{e(name)}</strong><small>{e(description)}</small></li>')
    return f'''<section class="ps-shell ps-family-map" id="mappa-famiglia" aria-labelledby="ps-family-title">
<div class="ps-family-map-panel"><div class="ps-family-heading"><div>
<p class="ps-viz-eyebrow">{e(t["mapEyebrow"])} / 04</p>
<h2 id="ps-family-title">{e(t["familyTitle"])}</h2><p>{e(t["familyLead"])}</p></div>
<span class="ps-family-icon" aria-hidden="true">2 + 4</span></div>
<div class="ps-family-domains">{"".join(domains)}</div>
<ol class="ps-family-process">{"".join(steps)}</ol>
<div class="ps-family-disruption"><div class="ps-family-alert"><span aria-hidden="true">!</span><div>
<strong>{e(t["familyChange"])}</strong><p>{e(t["familyChangeDesc"])}</p></div></div>
<span class="ps-family-reframe" aria-hidden="true">↓</span>
<div class="ps-family-revision"><strong>{e(t["familyRevision"])}</strong></div></div>
<div class="ps-family-outcome">{e(t["familyOutcome"])}</div>
<a class="ps-family-reading-link" href="#lettura-6" data-open-reading="lettura-6">{e(t["familyLink"])} ↗</a>
<p class="ps-family-limit">{e(t["familyLimit"])}</p></div></section>'''

def crossword(locale,t):
    # Deterministic placement by intersections, not a list of disconnected words.
    words=[word for word,clue in CROSS[locale]]
    board={(0,i):char for i,char in enumerate(words[0])}
    start=[(0,0,"h")]
    for word in words[1:]:
        options=[]
        for vertical in (True,False):
            for pos,letter in enumerate(word):
                for (row,col),old in list(board.items()):
                    if letter!=old:continue
                    y0=row-pos if vertical else row
                    x0=col if vertical else col-pos
                    cells=[(y0+i,x0) if vertical else (y0,x0+i) for i in range(len(word))]
                    if any(cell in board and board[cell]!=char for cell,char in zip(cells,word)):continue
                    overlaps=sum(cell in board for cell in cells)
                    if not overlaps:continue
                    all_positions=list(board)+cells
                    ys=[y for y,x in all_positions];xs=[x for y,x in all_positions]
                    area=(max(ys)-min(ys)+1)*(max(xs)-min(xs)+1)
                    options.append((area,-overlaps,int(vertical),y0,x0,cells))
        if not options:raise RuntimeError(locale+": crossword word cannot intersect: "+word)
        _,_,vertical,y0,x0,cells=min(options)
        for p,char in zip(cells,word):board[p]=char
        start.append((y0,x0,"v" if vertical else "h"))
    miny=min(y for y,x in board);maxy=max(y for y,x in board)
    minx=min(x for y,x in board);maxx=max(x for y,x in board)
    cols=maxx-minx+1
    starts={(y,x):str(i) for i,(y,x,d) in enumerate(start,1)}
    cells=[]
    for row in range(miny,maxy+1):
        for col in range(minx,maxx+1):
            if (row,col) not in board:
                cells.append('<span class="ps-cross-blank" aria-hidden="true"></span>')
                continue
            num=starts.get((row,col),"")
            indicator=f'<span aria-hidden="true">{num}</span>' if num else ""
            aria=e(t["row"]+" "+str(row-miny+1)+", "+t["column"]+" "+str(col-minx+1))
            cells.append(f'<label class="ps-cross-square">{indicator}<input type="text" inputmode="text" maxlength="1" autocomplete="off" spellcheck="false" data-answer="{board[row,col]}" aria-label="{aria}"></label>')
    clue_items=[]
    for i,((word,clue),(_,_,direction)) in enumerate(zip(CROSS[locale],start),1):
        dimension=t["crossDown"] if direction=="v" else t["crossAcross"]
        clue_items.append(f'<li><strong>{i} {e(dimension)}</strong> · {e(clue)} <span class="ps-lettercount">({len(word)} {e(t["letters"])})</span></li>')
    crossword_board=f'<div class="ps-crossboard" style="--ps-cols:{cols}" role="group" aria-label="{e(t["crossTitle"])}">{"".join(cells)}</div>'
    return crossword_board,'<ol class="ps-clues">'+"".join(clue_items)+"</ol>"

def local_card(site,locale,t):
    marker=MARKER
    for sect,dest in ((ACADEMY[locale],"academy"),(RESOURCES[locale],"resources")):
        target=site/sect/"index.html"
        if not target.is_file():raise RuntimeError(locale+": missing catalog "+str(target))
        html=target.read_text(encoding="utf-8")
        if marker in html:raise RuntimeError(locale+": duplicate translated card")
        if "</main>" not in html:raise RuntimeError(locale+": catalog main missing")
        url=BASE+ROUTES[locale]+"/"
        card=f'''<section class="ps-academy-discovery" {marker} aria-labelledby="ps-translation-{locale}-{dest}">
<div class="ps-discovery-top"><span>MANZO AI · {e(t["catalogTag"])}</span><span>{e(t["catalogBadge"])}</span></div>
<div class="ps-discovery-content"><div><p class="ps-discovery-kicker">{e(t["catalogTag"])}</p>
<h2 id="ps-translation-{locale}-{dest}">{e(t["catalogTitle"])}</h2><p>{e(t["catalogDesc"])}</p></div>
<a href="{url}" class="ps-discovery-cta">{e(t["catalogCTA"])} <span aria-hidden="true">↗</span></a></div></section>'''
        html=html.replace("</main>",card+"</main>",1)
        target.write_text(html,encoding="utf-8")

def make_page(site,locale):
    t=UI[locale];readings=read(locale)
    toc=[];blocks=[]
    visual={2:visual_prompt(t),3:visual_decision(t),4:visual_skill(t)}
    for n,(heading,body) in enumerate(readings,1):
        slug="lettura-"+str(n)
        toc.append(f'<a class="ps-toc-card" href="#{slug}" data-open-reading="{slug}"><span class="ps-toc-count">{e(t["reading"])}</span><strong>{e(t["short"][n-1])}</strong><small>{e(t["open"])} <span aria-hidden="true">↗</span></small></a>')
        html=markdown.markdown(body,extensions=["fenced_code","tables","sane_lists"])
        figure=visual.get(n,"")
        blocks.append(f'''<section class="ps-reading" id="{slug}"><details {"open" if n==1 else ""}>
<summary><span class="ps-reading-index">{e(t["reading"])} <em>{n} / 6</em></span><span class="ps-reading-title">{e(heading)}</span><span class="ps-reading-toggle" aria-hidden="true">+</span></summary>
<div class="ps-reading-copy">{figure}{html}<label class="ps-completion"><input type="checkbox" class="ps-read-check"> {e(t["done"])}</label>
<a class="ps-back" href="#indice-letture">{e(t["back"])} ↑</a></div></details></section>''')
    board,clues=crossword(locale,t)
    payload={"ui":{key:t[key] for key in ("progress","quizSubmit","correct","review","expected","quizProgress","quizScore","quizComment","crossCells","crossGood","crossBad","crossCleared")},
             "quiz":[{"q":q,"o":opts,"a":correct,"e":explanation} for q,opts,correct,explanation in QUIZ[locale]]}
    json_quiz=json.dumps(payload,ensure_ascii=False).replace("<","\\u003c")
    canonical=LINKS[locale]
    schema={"@context":"https://schema.org","@type":"Course","name":t["course"],"description":t["lead"],"inLanguage":locale,"isAccessibleForFree":True,"url":canonical,"provider":{"@type":"Organization","name":"MANZO AI"},"dateModified":"2026-11-20","citation":SOURCES}
    json_schema=json.dumps(schema,ensure_ascii=False).replace("<","\\u003c")
    nav=language_nav(locale)
    maplinks=[("lettura-2",t["mapLinks"][0]),("lettura-3",t["mapLinks"][1]),("lettura-4",t["mapLinks"][2]),("mappa-famiglia",t["mapLinks"][3])]
    map_nav="".join(f'<a href="#{id}" '+(f'data-open-reading="{id}"' if id.startswith("lettura") else "")+f'>{e(name)} ↗</a>' for id,name in maplinks)
    step_cards=''.join(f'<article><span>{e(label)}</span><h3>{e(title)}</h3><p>{e(text)}</p></article>' for label,title,text in t["labSteps"])
    html=f'''<!doctype html><html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(t["course"])} | MANZO AI</title><meta name="description" content="{e(t["lead"])}">
<meta name="robots" content="index,follow"><meta name="theme-color" content="#ffffff"><link rel="canonical" href="{canonical}">
{hreflangs()}<meta property="og:type" content="article"><meta property="og:title" content="{e(t["course"])}"><meta property="og:url" content="{canonical}">
<link rel="stylesheet" href="{BASE}assets/prompt-vs-skill.css"><link rel="stylesheet" href="{BASE}assets/{CSS_NAME}">
<script type="application/ld+json">{json_schema}</script></head>
<body data-ma-prompt-skill="course-v1" data-ma-prompt-skill-i18n="v1">
<a class="ps-skip" href="#ps-main">{e(t["skip"])}</a>
<header class="ps-topbar"><div class="ps-shell ps-topbar-row"><a class="ps-brand" href="{BASE}{locale}/">MANZO<span>AI</span></a>
<nav aria-label="{e(t["navLabel"])}"><a href="{BASE}{ACADEMY[locale]}/">{e(t["academy"])}</a><a href="#indice-letture">{e(t["navReadings"])}</a><a href="#laboratorio">{e(t["navLab"])}</a><a href="#verifica">{e(t["navQuiz"])}</a></nav></div></header>
<main id="ps-main">
<section class="ps-hero"><div class="ps-shell">
{nav}<span class="ps-eyebrow">{e(t["eyebrow"])}</span><p class="ps-context">{e(t["context"])}</p>
<h1>Prompt <span class="ps-vs">vs</span> Skill</h1><p class="ps-subtitle">{e(t["lead"])}</p>
<div class="ps-hero-bottom">{"".join("<span>"+e(p)+"</span>" for p in t["pills"])}</div>
<a class="ps-main-cta" href="#indice-letture">{e(t["begin"])} <span aria-hidden="true">↘</span></a></div></section>
<section class="ps-shell ps-intro"><div><p class="ps-overline">{e(t["academy"])}</p><h2>{e(t["introTitle"])}</h2></div><div><p>{e(t["introText"])}</p><p>{e(t["introNote"])}</p></div></section>
<section class="ps-shell ps-guide" id="indice-letture"><div class="ps-section-heading"><div><p class="ps-overline">{e(t["academy"])}</p><h2>{e(t["readings"])}</h2></div><p>{e(t["readingsDesc"])}</p></div>
<div class="ps-toc">{"".join(toc)}</div><nav class="ps-viz-jumps" aria-label="{e(t["maps"])}"><strong>{e(t["maps"])}</strong>{map_nav}</nav>
<p class="ps-counter" id="ps-progress" aria-live="polite">0 / 6</p></section>
<div class="ps-shell ps-readings">{"".join(blocks)}</div>
{visual_family(t)}
<section class="ps-shell ps-lab" id="laboratorio"><p class="ps-overline">{e(t["navLab"])}</p><h2>{e(t["labTitle"])}</h2>
<p>{e(t["labLead"])}</p><div class="ps-step-grid">{step_cards}</div>
<details class="ps-practice"><summary>{e(t["practice"])} <span>+</span></summary><div><p>{e(t["practiceBody"])}</p></div></details></section>
<section class="ps-shell ps-cross" id="cruciverba"><div class="ps-section-heading"><div><p class="ps-overline">{e(t["crossClues"])}</p><h2>{e(t["crossTitle"])}</h2></div><p>{e(t["crossLead"])}</p></div>
<div class="ps-cross-layout"><div>{board}<div class="ps-cross-actions"><button id="ps-check-cross" type="button">{e(t["crossCheck"])}</button>
<button id="ps-clear-cross" type="button" class="ps-outline">{e(t["crossReset"])}</button></div>
<p id="ps-cross-result" role="status" aria-live="polite">{e(t["crossHint"])}</p></div><div><h3>{e(t["crossClues"])}</h3>{clues}</div></div></section>
<section class="ps-shell ps-quiz" id="verifica"><p class="ps-overline">{e(t["navQuiz"])}</p><h2>{e(t["quizTitle"])}</h2>
<p>{e(t["quizLead"])}</p><div id="ps-quiz-form"></div><script type="application/json" id="ps-quiz-data">{json_quiz}</script></section>
<section class="ps-shell ps-outro"><p class="ps-overline">{e(t["navQuiz"])}</p><h2>{e(t["outroTitle"])}</h2><p>{e(t["outroText"])}</p>
<a href="#lettura-6" data-open-reading="lettura-6">{e(t["outroLink"])} <span aria-hidden="true">↗</span></a></section>
</main><footer class="ps-footer"><div class="ps-shell"><p><strong>MANZO AI</strong> · {e(t["course"])}</p><p>{e(t["footer"])}</p>
<a href="{BASE}{ACADEMY[locale]}/">{e(t["academy"])}</a></div></footer>
<script src="{BASE}assets/{ASSET}" defer></script></body></html>'''
    dest=site/ROUTES[locale]/"index.html"
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(html,encoding="utf-8")

def upgrade_italian(site):
    path=site/ROUTES["it"]/"index.html"
    if not path.is_file():raise RuntimeError("Italian original not found")
    html=path.read_text(encoding="utf-8")
    nav=language_nav("it")
    if "ps-i18n-languages" in html:raise RuntimeError("Italian language menu duplicated")
    if '<main id="ps-main">' not in html:raise RuntimeError("Unexpected Italian course markup")
    html=html.replace('<main id="ps-main">','<main id="ps-main">'+nav,1)
    html=html.replace("</head>",hreflangs()+f'<link rel="stylesheet" href="{BASE}assets/{CSS_NAME}"></head>',1)
    incorrect="https://manzo8b.github.io/it/formazione/prompt-vs-skill/"
    html=html.replace(incorrect,LINKS["it"])
    if '<link rel="canonical"' not in html:
        html=html.replace("</head>",f'<link rel="canonical" href="{LINKS["it"]}"></head>',1)
    path.write_text(html,encoding="utf-8")

def verify(site):
    for locale in ("en","es"):
        html=(site/ROUTES[locale]/"index.html").read_text(encoding="utf-8")
        if html.count('class="ps-reading"')!=6:raise RuntimeError(locale+": six readings absent")
        if html.count('class="ps-toc-card"')!=6:raise RuntimeError(locale+": six reading cards absent")
        for id in ("mappa-prompt","mappa-salto","mappa-skill","mappa-famiglia","laboratorio","cruciverba","verifica"):
            if html.count('id="'+id+'"')!=1:raise RuntimeError(locale+": visual or exercise missing: "+id)
        if html.count('class="ps-cross-square"')<24:raise RuntimeError(locale+": crossword not generated")
        payload=json.loads(re.search(r'<script type="application/json" id="ps-quiz-data">(.+?)</script>',html).group(1))
        if len(payload["quiz"])!=10:raise RuntimeError(locale+": quiz incomplete")
        for lang in LINKS:
            if f'hreflang="{lang}"' not in html:raise RuntimeError(locale+": hreflang missing")
        for route in (ACADEMY[locale],RESOURCES[locale]):
            listing=(site/route/"index.html").read_text(encoding="utf-8")
            if listing.count(MARKER)!=1 or BASE+ROUTES[locale]+"/" not in listing:
                raise RuntimeError(locale+": discovery missing in "+route)
    it=(site/ROUTES["it"]/"index.html").read_text(encoding="utf-8")
    if "ps-i18n-languages" not in it or it.count('class="ps-reading"')!=6:
        raise RuntimeError("Italian course altered or lost language navigation")
    for src in (ASSET,CSS_NAME):
        if not (site/"assets"/src).is_file():raise RuntimeError("Missing localized asset: "+src)
    print("Prompt vs Skill locale rollout: English and Spanish 6/6 readings, 4/4 diagrams, 8-word crossword and 10/10 quiz PASS; Italian original preserved")

def publish(site):
    if not JS.is_file() or not STYLES.is_file():raise RuntimeError("Prompt vs Skill translation assets unavailable")
    (site/"assets").mkdir(parents=True,exist_ok=True)
    shutil.copy2(JS,site/"assets"/ASSET)
    shutil.copy2(STYLES,site/"assets"/"prompt-vs-skill.css")
    stylesheet=ROOT/"theme/prompt-skill-i18n.css"
    if not stylesheet.is_file():raise RuntimeError("Localized visuals stylesheet absent")
    shutil.copy2(stylesheet,site/"assets"/CSS_NAME)
    for loc in ("en","es"):
        make_page(site,loc)
        local_card(site,loc,UI[loc])
    upgrade_italian(site)
    verify(site)

if __name__=="__main__":
    arg=argparse.ArgumentParser();arg.add_argument("--site",required=True,type=Path);arg.add_argument("--verify-only",action="store_true")
    opts=arg.parse_args()
    verify(opts.site) if opts.verify_only else publish(opts.site)
