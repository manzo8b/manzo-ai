#!/usr/bin/env python3
"""Publish the final two MANZO AI Academy courses, fully localised in IT/EN/ES.

A single renderer enforces source-depth parity, native interface strings,
complete learning activities, source references and 4 inline HTML infographics.
It never invokes AI at runtime or stores submitted data. Educational STOP does
not assert real-life legal compliance.
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
from final_two_i18n_base import ROOT,BASE,CONTENT,LOCALES,COURSES,SHARED,CONTENT_UI,ACADEMY,RESOURCES
import final_two_i18n_aug  # noqa: F401 — adds the second course's translated content
from final_two_quiz import QUIZ

SCRIPT=ROOT/"theme/final-two-courses.js"
STYLE=ROOT/"theme/final-two-courses.css"
CSS_NAME="final-two-courses.css"
JS_NAME="final-two-courses.js"
MARKERS={"compliance":'data-ma-last-course="compliance"',
         "augmented":'data-ma-last-course="augmented"'}
HEADINGS={"it":r"Lettura","en":r"Reading","es":r"Lectura"}
TOOL_TITLES={
    "it":("Strumenti operativi",),
    "en":("Operational toolkit","Operational tools"),
    "es":("Herramientas operativas",)
}
MAIN_MARK="data-ma-final-course"

def e(v):return escape(str(v),quote=True)
def canonical(course,locale):
    return "https://manzo8b.github.io/manzo-ai/"+COURSES[course]["routes"][locale]+"/"
def ucourse(course,locale):
    return BASE+COURSES[course]["routes"][locale]+"/"

def source_content(course,locale):
    conf=COURSES[course]
    path=CONTENT/conf["source"]/(locale+".md")
    if not path.is_file():raise RuntimeError("Missing full course translation "+str(path))
    text=path.read_text(encoding="utf-8")
    if len(text)<conf["source_min"]:
        raise RuntimeError(f"{course} {locale}: abridged or incomplete source ({len(text)} characters)")
    pattern=r"(?m)^## "+HEADINGS[locale]+r" ([1-6]) · ([^\n]+)\n"
    matches=list(re.finditer(pattern,text))
    if len(matches)!=6 or [int(x.group(1)) for x in matches]!=[1,2,3,4,5,6]:
        raise RuntimeError(course+" "+locale+": requires six intact, ordered readings")
    primary=conf["primary"]
    if primary not in text:raise RuntimeError(f"{course} {locale}: primary source absent")
    initial=text[:matches[0].start()].strip()
    if "\n" in initial:initial=initial.split("\n",1)[1].strip()
    readings=[]
    toolkit=""
    for i,m in enumerate(matches):
        end=matches[i+1].start() if i<5 else len(text)
        part=text[m.end():end].strip()
        if i==5:
            heading_re="|".join(map(re.escape,TOOL_TITLES[locale]))
            tool_match=re.search(r"(?m)^## (?:"+heading_re+r")\s*$",part)
            if not tool_match:
                raise RuntimeError(f"{course} {locale}: reference toolkit and glossary missing")
            toolkit=part[tool_match.start():].strip()
            part=part[:tool_match.start()].strip()
        if len(part)<1450:
            raise RuntimeError(f"{course} {locale}: in-depth reading {i+1} too brief")
        readings.append((m.group(2),part))
    if len(toolkit)<1300:raise RuntimeError(f"{course} {locale}: toolkit truncated")
    return initial,readings,toolkit

def md(value):
    return markdown.markdown(value,extensions=["fenced_code","tables","sane_lists"])

def language_nav(course,locale):
    t=SHARED[locale]
    items=[]
    for lang in LOCALES:
        attr=' aria-current="page"' if lang==locale else ""
        items.append(f'<a href="{ucourse(course,lang)}" hreflang="{lang}" lang="{lang}"{attr}>{lang.upper()}</a>')
    return f'<nav class="ft-languages" aria-label="{e(t["langNav"])}">{"".join(items)}</nav>'

def diagram(number,title,description,steps,variant="flow",note=None):
    children=[]
    if variant=="quadrant":
        for i,(name,detail) in enumerate(steps,1):
            children.append(f'<article><span>{i:02d}</span><strong>{e(name)}</strong><p>{e(detail)}</p></article>')
        content='<div class="ft-quadrants">'=>""
    else:
        for i,(name,detail) in enumerate(steps,1):
            children.append(f'<li><span class="ft-stage-n">{i:02d}</span><strong>{e(name)}</strong><small>{e(detail)}</small></li>')
    if variant=="quadrant":
        content='<div class="ft-quadrants">'+"".join(children)+'</div>'
    elif variant=="framework":
        content='<div class="ft-frameworks">'+"".join(f'<article><strong>{e(name)}</strong><p>{e(desc)}</p></article>' for name,desc in steps)+'</div>'
    else:
        content='<ol class="ft-visual-flow">'+"".join(children)+'</ol>'
    footer=f'<p class="ft-viz-foot">{e(note)}</p>' if note else ""
    return f'''<figure class="ft-viz ft-viz-{variant}" id="ft-map-{number}">
<figcaption><span class="ft-overline">MANZO AI / VISUAL {number} / 04</span>
<strong>{e(title)}</strong><span>{e(description)}</span></figcaption>{content}{footer}</figure>'''

def visual_maps(course,locale):
    t=CONTENT_UI[course][locale]
    if course=="compliance":
        sets=[(t["mapSteps"],"flow"),(t["roleSteps"],"flow"),(t["frameworks"],"framework"),(t["driftSteps"],"flow")]
    else:
        sets=[(t["quadrants"],"quadrant"),(t["humanSteps"],"flow"),
              (t["repairSteps"],"flow"),(t["disclosure"],"disclosure")]
    output=[]
    for i,(items,kind) in enumerate(sets,1):
        if kind=="disclosure":
            output.append('<figure class="ft-viz ft-viz-framework" id="ft-map-4"><figcaption><span class="ft-overline">MANZO AI / VISUAL 4 / 04</span><strong>'+
                          e(t["mapTitles"][3])+'</strong><span>'+e(t["mapDescs"][3])+'</span></figcaption><div class="ft-disclosure">'+
                          ''.join('<article><b>'+e(code)+'</b><strong>'+e(name)+'</strong><small>'+e(desc)+'</small></article>' for code,name,desc in items)+
                          '</div><p class="ft-viz-foot">'+e(t["visualNote"])+'</p></figure>')
        else:
            output.append(diagram(i,t["mapTitles"][i-1],t["mapDescs"][i-1],items,kind,t["visualNote"] if i==4 else None))
    return output

def crossword(course,locale):
    # Compact crossword with valid horizontal/vertical intersections,
    # no adjacent parallel letters forming unintended words.
    words=CONTENT_UI[course][locale]["cross"]
    if len(words)!=8:raise RuntimeError("Eight-word crossword required")
    clean=[]
    for word,clue in words:
        if not word or not word.isascii() or not word.isalpha() or word.upper()!=word:
            raise RuntimeError(f"Invalid crossword entry in {course}/{locale}: {word}")
        clean.append((word,clue))
    board={(0,x):letter for x,letter in enumerate(clean[0][0])}
    orient={(0,x):{"H"} for x in range(len(clean[0][0]))}
    starts=[(0,0,"H")]
    for word,clue in clean[1:]:
        candidates=[]
        for direction in ("V","H"):
            dy,dx=(1,0) if direction=="V" else (0,1)
            for j,letter in enumerate(word):
                for (row,col),existing in list(board.items()):
                    if letter!=existing or direction in orient.get((row,col),set()):continue
                    y0=row-j*dy;x0=col-j*dx
                    cells=[(y0+k*dy,x0+k*dx) for k in range(len(word))]
                    if any(cell in board and (board[cell]!=char or direction in orient.get(cell,set())) for cell,char in zip(cells,word)):continue
                    if (y0-dy,x0-dx) in board or (y0+len(word)*dy,x0+len(word)*dx) in board:continue
                    # New letters cannot touch existing words sideways.
                    sideways=[(0,1),(0,-1)] if direction=="V" else [(1,0),(-1,0)]
                    invalid=False
                    for cell in cells:
                        if cell in board:continue
                        if any((cell[0]+sy,cell[1]+sx) in board for sy,sx in sideways):
                            invalid=True;break
                    if invalid:continue
                    overlaps=sum(cell in board for cell in cells)
                    if not overlaps:continue
                    coords=list(board)+cells
                    ys=[y for y,x in coords];xs=[x for y,x in coords]
                    area=(max(ys)-min(ys)+1)*(max(xs)-min(xs)+1)
                    candidates.append((area,-overlaps,int(direction=="V"),y0,x0,cells,direction))
        if not candidates:
            raise RuntimeError(f"{course}/{locale}: cannot fit {word} as a real crossing word")
        _,_,_,y0,x0,cells,direction=min(candidates)
        for cell,letter in zip(cells,word):
            board[cell]=letter
            orient.setdefault(cell,set()).add(direction)
        starts.append((y0,x0,direction))
    miny=min(y for y,x in board);maxy=max(y for y,x in board)
    minx=min(x for y,x in board);maxx=max(x for y,x in board)
    widths=maxx-minx+1
    if widths>38:raise RuntimeError(f"{course}/{locale}: crossword too wide for meaningful mobile scroll")
    labels={}
    for n,(r,c,direction) in enumerate(starts,1):
        labels[(r,c)]=labels.get((r,c),"")+("," if (r,c) in labels else "")+str(n)
    cells=[]
    for r in range(miny,maxy+1):
        for c in range(minx,maxx+1):
            if (r,c) not in board:
                cells.append('<span class="ft-cross-blank" aria-hidden="true"></span>')
            else:
                number=labels.get((r,c),"")
                index=f'<span aria-hidden="true">{number}</span>' if number else ""
                aria={"it":f"Riga {r-miny+1}, colonna {c-minx+1}",
                      "en":f"Row {r-miny+1}, column {c-minx+1}",
                      "es":f"Fila {r-miny+1}, columna {c-minx+1}"}[locale]
                cells.append(f'<label class="ft-cross-cell">{index}<input data-answer="{board[(r,c)]}" type="text" maxlength="1" autocomplete="off" spellcheck="false" inputmode="text" aria-label="{e(aria)}"></label>')
    t=SHARED[locale]
    clues=[]
    for n,((word,clue),(r,c,direction)) in enumerate(zip(clean,starts),1):
        label=t["down"] if direction=="V" else t["across"]
        clues.append(f'<li><strong>{n} {e(label)}</strong> · {e(clue)} ({len(word)})</li>')
    return f'''<section class="ps-shell ft-crossword" id="ft-crossword">
<p class="ft-overline">MANZO AI / LANGUAGE</p><h2>{e(t["words"])}</h2>
<div class="ft-cross-layout"><div class="ft-cross-surface"><div class="ft-cross-scroll">
<div class="ft-crossboard" style="--ft-cols:{widths}" role="group" aria-label="{e(t["words"])}">{"".join(cells)}</div></div>
<div class="ft-actions"><button type="button" id="ft-cross-check" class="ft-button">{e(t["crossCheck"])}</button>
<button type="button" id="ft-cross-clear" class="ft-button ft-secondary">{e(t["crossClear"])}</button></div>
<p class="ft-result" id="ft-cross-result" aria-live="polite" role="status"></p></div>
<div class="ft-cross-surface"><ol class="ft-clues">{"".join(clues)}</ol></div></div></section>'''

def make_select(options,identifier,label,klass=""):
    return '<select id="'+e(identifier)+'" class="'+e(klass)+'" aria-label="'+e(label)+'">'+''.join(
        '<option value="'+e(value)+'">'+e(title)+'</option>' for value,title in options)+'</select>'

def lab(course,locale):
    s=SHARED[locale];t=CONTENT_UI[course][locale]
    stages=[]
    if course=="compliance":
        tool_rows=[]
        for i,title in enumerate(t["tools"]):
            tool_rows.append('<div class="ft-lab-row"><label for="ft-tool-'+str(i)+'">'+e(title)+'</label>'+
               make_select(t["toolChoices"],"ft-tool-"+str(i),title,'ft-tool-choice')+
               '<p class="ft-explanation" aria-live="polite"></p></div>')
        stage1=f'''<div class="ft-lab-grid" id="ft-tool-grid">{"".join(tool_rows)}</div>
<div class="ft-field"><label for="ft-owner">{e(t["owner"])}</label>
<input id="ft-owner" type="text" maxlength="95" autocomplete="off" placeholder="{e(t["ownerExample"])}"></div>'''
        rows=[]
        for i,(heading,description,options,answer,why) in enumerate(t["cases"]):
            choices=[("",s["selected"])]+[(str(k),label) for k,label in enumerate(options)]
            rows.append(f'<div class="ft-lab-row ft-case"><h4>{e(heading)}</h4><p>{e(description)}</p>'+
                        make_select(choices,"ft-case-"+str(i),heading,"ft-case-choice")+
                        '<p class="ft-explanation" aria-live="polite"></p></div>')
        stage2=f'<p>{e(t["riskIntro"])}</p><div class="ft-lab-grid" id="ft-case-grid">{"".join(rows)}</div>'
        metrics=[]
        triggers=[]
        for i in range(3):
            items=''.join('<div class="ft-field"><label for="ft-m-'+str(i)+'-'+str(j)+'">'+e(label)+'</label>'+
             '<input id="ft-m-'+str(i)+'-'+str(j)+'" type="text" maxlength="150" autocomplete="off" class="ft-metric-input"></div>'
              for j,label in enumerate(t["metricFields"]))
            metrics.append('<div class="ft-lab-row"><strong>'+'0'+str(i+1)+'</strong><div class="ft-entry-grid">'+items+'</div></div>')
            items2=''.join('<div class="ft-field"><label for="ft-t-'+str(i)+'-'+str(j)+'">'+e(label)+'</label>'+
              '<input id="ft-t-'+str(i)+'-'+str(j)+'" type="text" maxlength="150" autocomplete="off" class="ft-trigger-input"></div>'
              for j,label in enumerate(t["triggerFields"]))
            triggers.append('<div class="ft-lab-row"><strong>'+'0'+str(i+1)+'</strong><div class="ft-entry-grid">'+items2+'</div></div>')
        stage3=f'''<p>{e(t["metricIntro"])}</p><div class="ft-entry-stack" id="ft-metrics">{"".join(metrics)}</div>
<h4>{e(t["triggerIntro"])}</h4><div class="ft-entry-stack" id="ft-triggers">{"".join(triggers)}</div>'''
        stage4=''
    else:
        task_rows=[]
        for i,(name,category,why) in enumerate(t["tasks"]):
            task_rows.append('<div class="ft-lab-row"><label for="ft-task-'+str(i)+'">'+e(name)+'</label>'+
               make_select(t["taskChoices"],"ft-task-"+str(i),name,"ft-task-choice")+
               '<p class="ft-explanation" aria-live="polite"></p></div>')
        stage1=f'<div class="ft-lab-grid" id="ft-tasks">{"".join(task_rows)}</div>'
        checks=[]
        for i,(question,options,answer,why) in enumerate(t["checkQuestions"]):
            choices=[("",s["selected"])]+[(str(k),label) for k,label in enumerate(options)]
            checks.append(f'<div class="ft-lab-row ft-case"><h4>{e(question)}</h4>'+
                make_select(choices,"ft-check-"+str(i),question,"ft-workslop-choice")+
                '<p class="ft-explanation" aria-live="polite"></p></div>')
        stage2=f'''<p>{e(t["workslopIntro"])}</p><blockquote class="ft-false-text">{e(t["workslopText"])}</blockquote>
<div class="ft-lab-grid" id="ft-workslop">{"".join(checks)}</div>'''
        stage3=f'''<div class="ft-field"><label for="ft-prior">{e(t["prior"])}</label>
<textarea id="ft-prior" rows="4" maxlength="1800" placeholder="{e(t["priorHint"])}"></textarea></div>
<div class="ft-field"><label for="ft-rewrite">{e(t["rewrite"])}</label>
<textarea id="ft-rewrite" rows="4" maxlength="1800" placeholder="{e(t["rewriteHint"])}"></textarea></div>
<p>{e(t["charterIntro"])}</p>'''
        for i,rule in enumerate(t["charterRules"]):
            stage3+=f'<div class="ft-field"><label for="ft-rule-{i}">{e(rule)}</label><input id="ft-rule-{i}" type="text" maxlength="260" autocomplete="off"></div>'
        stage3+=f'''<div class="ft-field"><label for="ft-data-rule">{e(t["dataRule"])}</label><input id="ft-data-rule" type="text" maxlength="260" autocomplete="off" placeholder="{e(t["dataRuleHint"])}"></div>'''
        stage4=''
    rubric=''.join(f'<div class="ft-rubric-row"><label for="ft-rubric-{i}">{e(label)}</label>'+
      make_select([("",s["selected"]),("0","0"),("1","1"),("2","2")],"ft-rubric-"+str(i),label,"ft-rubric-choice")+'</div>'
      for i,label in enumerate(t["rubric"]))
    stage4=f'''<p>{e(t["rubricIntro"])}</p><div id="ft-rubric">{rubric}</div>
<div class="ft-actions"><button id="ft-release" type="button" class="ft-button">{e(s["release"])}</button>
<button id="ft-copy" type="button" class="ft-button ft-secondary">{e(s["copy"])}</button></div>
<p class="ft-release-result" id="ft-decision" role="status" aria-live="polite" hidden></p>
<p class="ft-result" id="ft-copy-status" role="status" aria-live="polite"></p>'''
    sections=[]
    for i,contents in enumerate((stage1,stage2,stage3,stage4)):
        sections.append(f'''<section class="ft-station" id="ft-station-{i+1}">
<h3>{e(t["stages"][i])}</h3>{contents}</section>''')
    return f'''<section class="ps-shell ft-lab" id="ft-lab">
<p class="ft-overline">MANZO AI / PRACTICE</p><h2>{e(t["labTitle"])}</h2>
<p class="ft-lab-lead">{e(t["labLead"])}</p><p class="ft-privacy">{e(s["note"])}</p>
{"".join(sections)}</section>'''

def catalog_card(site,course,locale):
    t=SHARED[locale];c=CONTENT_UI[course][locale];marker=MARKERS[course]
    for category,path in (("academy",ACADEMY[locale]),("resources",RESOURCES[locale])):
        dest=site/path/"index.html"
        if not dest.is_file():raise RuntimeError(f"{course} {locale}: {category} index missing")
        html=dest.read_text(encoding="utf-8")
        if marker in html:raise RuntimeError(f"{course} {locale}: duplicate catalog card")
        if "</main>" not in html:raise RuntimeError("Catalogue has no main")
        id=f"ft-{course}-{locale}-{category}"
        card=f'''<section class="ps-academy-discovery" {marker} aria-labelledby="{id}">
<div class="ps-discovery-top"><span>MANZO AI · {e(t["tag"])}</span><span>{e(t["free"])}</span></div>
<div class="ps-discovery-content"><div><p class="ps-discovery-kicker">{e(t["tag"])}</p>
<h2 id="{id}">{e(c["title"])}</h2><p>{e(c["homeDescription"])}</p></div>
<a class="ps-discovery-cta" href="{ucourse(course,locale)}">{e(t["enroll"])} <span aria-hidden="true">↗</span></a>
</div></section>'''
        html=html.replace("</main>",card+"</main>",1)
        if "prompt-vs-skill.css" not in html:
            html=html.replace("</head>",f'<link rel="stylesheet" href="{BASE}assets/prompt-vs-skill.css"></head>',1)
        dest.write_text(html,encoding="utf-8")

def page(site,course,locale):
    s=SHARED[locale];t=CONTENT_UI[course][locale];conf=COURSES[course]
    introduction,readings,toolkit=source_content(course,locale)
    maps=visual_maps(course,locale)
    # Maps appear at the point where their ideas are taught, not all at the end.
    positions={"compliance":{1:0,3:1,4:2,5:3},
               "augmented":{2:0,4:1,1:2,5:3}}[course]
    panels=[];nav=[]
    map_target=[]
    for index,(heading,body) in enumerate(readings,1):
        marker="ft-reading-"+str(index)
        nav.append(f'''<a class="ps-toc-card" href="#{marker}" data-open-reading="{marker}">
<span class="ps-toc-count">{e(s["reading"])}</span><strong>{e(t["short"][index-1])}</strong>
<small>{e(s["open"])} <span aria-hidden="true">↗</span></small></a>''')
        map_html=maps[positions[index]] if index in positions else ""
        panels.append(f'''<section class="ps-reading" id="{marker}"><details {"open" if index==1 else ""}>
<summary><span class="ps-reading-index">{e(s["reading"])} <em>{index} / 6</em></span>
<span class="ps-reading-title">{e(heading)}</span><span class="ps-reading-toggle" aria-hidden="true">+</span></summary>
<div class="ps-reading-copy">{md(body)}{map_html}
<label class="ps-completion"><input type="checkbox" class="ps-read-check"> {e(s["done"])}</label>
<a href="#ft-readings" class="ps-back">{e(s["back"])} ↑</a></div></details></section>''')
    map_to_reading={value:key for key,value in positions.items()}
    for idx,title in enumerate(t["mapTitles"]):
        n=map_to_reading[idx]
        map_target.append(f'<a href="#ft-map-{idx+1}" data-open-reading="ft-reading-{n}">{e(title)} ↗</a>')
    quizzes=QUIZ[course][locale]
    if len(quizzes)!=10:raise RuntimeError(course+" "+locale+": incomplete quiz bank")
    data={"kind":course,"ui":{**s,**t},
          "quiz":[{"q":q,"options":options,"answer":answer,"why":why}
                  for q,options,answer,why in quizzes]}
    payload=json.dumps(data,ensure_ascii=False).replace("<","\\u003c")
    schema={"@context":"https://schema.org","@type":"Course",
            "name":t["title"]+" — "+t["subtitle"],"description":t["lead"],
            "inLanguage":locale,"isAccessibleForFree":True,"url":canonical(course,locale),
            "provider":{"@type":"Organization","name":"MANZO AI"},
            "datePublished":"2026-11-20"}
    schema_json=json.dumps(schema,ensure_ascii=False).replace("<","\\u003c")
    alternates=''.join(f'<link rel="alternate" hreflang="{lang}" href="{e(canonical(course,lang))}">' for lang in LOCALES)
    alternates+='<link rel="alternate" hreflang="x-default" href="'+e(canonical(course,"it"))+'">'
    intro_html=md(introduction)
    toolkit_html=md(toolkit)
    preroute=conf["related"][locale]
    pills=''.join('<span>'+e(item)+'</span>' for item in s["readPills"])
    html=f'''<!doctype html><html lang="{locale}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(t["title"])} · MANZO AI</title><meta name="description" content="{e(t["lead"])}">
<meta name="robots" content="index,follow"><meta name="theme-color" content="#ffffff">
<link rel="canonical" href="{e(canonical(course,locale))}">{alternates}
<meta property="og:type" content="article"><meta property="og:title" content="{e(t["title"])}">
<meta property="og:url" content="{e(canonical(course,locale))}">
<link rel="stylesheet" href="{BASE}assets/prompt-vs-skill.css">
<link rel="stylesheet" href="{BASE}assets/{CSS_NAME}">
<script type="application/ld+json">{schema_json}</script></head>
<body data-ma-prompt-skill="course-v1" data-ma-final-course="{course}" data-ft-version="v1">
<a class="ps-skip" href="#ft-main">{e(s["skip"])}</a>
<header class="ps-topbar"><div class="ps-shell ps-topbar-row">
<a class="ps-brand" href="{BASE}{locale}/">MANZO<span>AI</span></a>
<nav aria-label="{e(s["courseNav"])}"><a href="{BASE}{ACADEMY[locale]}/">{e(s["academy"])}</a>
<a href="#ft-readings">{e(s["readings"])}</a><a href="#ft-lab">{e(s["lab"])}</a>
<a href="#ft-quiz">{e(s["quiz"])}</a></nav></div></header>
<main id="ft-main">
<section class="ps-hero ft-hero ft-hero-{course}"><div class="ps-shell">{language_nav(course,locale)}
<p class="ps-eyebrow">MANZO AI / {e(s["tag"])}</p><p class="ps-context">{e(t["subtitle"])}</p>
<h1>{t["hero"]}</h1><p class="ps-subtitle">{e(t["lead"])}</p>
<div class="ps-hero-bottom">{pills}</div>
<a class="ps-main-cta" href="#ft-readings">{e(s["start"])} <span aria-hidden="true">↘</span></a></div></section>
<section class="ps-shell ft-related"><a href="{BASE}{preroute}/">{e(s["previous"])} <span aria-hidden="true">↗</span></a>
<p>{e(t["hint"])}</p></section>
<section class="ps-shell ft-overview"><details><summary>{e(t["title"])} · {e(s["sources"])} <span aria-hidden="true">+</span></summary>
<div class="ft-markdown">{intro_html}</div></details></section>
<section class="ps-shell ps-guide" id="ft-readings"><div class="ps-section-heading">
<div><p class="ps-overline">MANZO AI / AI ACADEMY</p><h2>{e(s["readings"])}</h2></div>
<p>{e(t["readIntro"])}</p></div><div class="ps-toc">{"".join(nav)}</div>
<nav class="ft-map-nav" aria-label="{e(s["maps"])}"><strong>{e(s["maps"])}</strong>{"".join(map_target)}</nav>
<p class="ps-counter" id="ft-progress" role="status" aria-live="polite">0 / 6</p></section>
<div class="ps-shell ps-readings">{"".join(panels)}</div>
{lab(course,locale)}
<section class="ps-shell ft-tools" id="ft-tools"><details><summary>{e(s["sources"])} · {e(t["copyTitle"])} <span aria-hidden="true">+</span></summary>
<div class="ft-markdown">{toolkit_html}</div></details></section>
{crossword(course,locale)}
<section class="ps-shell ft-quiz-section" id="ft-quiz">
<p class="ft-overline">MANZO AI / ASSESSMENT</p><h2>{e(s["quiz"])}</h2>
<p>{e(s["quizNote"])}</p><div id="ft-quiz-host"></div>
<script type="application/json" id="ft-payload">{payload}</script></section>
<section class="ps-shell ft-conclusion"><h2>{e(t["title"])}</h2><p>{e(t["hint"])}</p>
<p>{e(s["notCertificate"])}</p><a href="{BASE}{ACADEMY[locale]}/">{e(s["academy"])} ↗</a></section></main>
<footer class="ps-footer"><div class="ps-shell"><p><strong>MANZO AI</strong> · {e(t["title"])}</p>
<p>{e(s["footer"])}</p><a href="{BASE}{ACADEMY[locale]}/">{e(s["academy"])}</a></div></footer>
<script src="{BASE}assets/{JS_NAME}" defer></script></body></html>'''
    dest=site/conf["routes"][locale]/"index.html"
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(html,encoding="utf-8")

def verify(site):
    for course in COURSES:
        for loc in LOCALES:
            html=(site/COURSES[course]["routes"][loc]/"index.html").read_text(encoding="utf-8")
            if html.count('class="ps-reading"')!=6 or html.count('class="ps-toc-card"')!=6:
                raise RuntimeError(course+" "+loc+": six complete lessons/cards missing")
            for number in (1,2,3,4):
                if html.count('id="ft-map-'+str(number)+'"')!=1:
                    raise RuntimeError(course+" "+loc+": missing visual "+str(number))
            if html.count('class="ft-cross-cell"')<27:raise RuntimeError(course+" "+loc+": crossword incomplete")
            if html.count('class="ft-station"')!=4:raise RuntimeError(course+" "+loc+": four lab stages missing")
            for lang in LOCALES:
                if f'hreflang="{lang}"' not in html:raise RuntimeError(course+" "+loc+": no "+lang+" hreflang")
            m=re.search(r'<script type="application/json" id="ft-payload">(.+?)</script>',html)
            if not m:raise RuntimeError("Missing assessment JSON")
            payload=json.loads(m.group(1))
            if len(payload["quiz"])!=10:raise RuntimeError("Ten native-language questions required")
            if course=="compliance":
                if html.count('class="ft-tool-choice"')!=8 or html.count('class="ft-case-choice"')!=4:
                    raise RuntimeError("Eight tools + four legal scenarios missing")
            else:
                if html.count('class="ft-task-choice"')!=8 or html.count('class="ft-workslop-choice"')!=4:
                    raise RuntimeError("Eight tasks + four workslop checks missing")
            for dirname in (ACADEMY[loc],RESOURCES[loc]):
                index=(site/dirname/"index.html").read_text(encoding="utf-8")
                if index.count(MARKERS[course])!=1 or ucourse(course,loc) not in index:
                    raise RuntimeError(course+" "+loc+": missing translated catalog link")
    for asset in (CSS_NAME,JS_NAME):
        if not (site/"assets"/asset).is_file():raise RuntimeError("Missing asset "+asset)
    print("MANZO AI final courses: 2 × 3 full translations, 36 readings, 24 visual diagrams, 6 interactive labs, 6 crosswords, 60 explainable quizzes PASS")

def publish(site):
    (site/"assets").mkdir(parents=True,exist_ok=True)
    for source,name in ((SCRIPT,JS_NAME),(STYLE,CSS_NAME)):
        if not source.is_file():raise RuntimeError("Missing "+str(source))
        shutil.copy2(source,site/"assets"/name)
    for course in COURSES:
        for loc in LOCALES:
            page(site,course,loc)
            catalog_card(site,course,loc)
    verify(site)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--site",type=Path,required=True)
    parser.add_argument("--verify-only",action="store_true")
    args=parser.parse_args()
    verify(args.site) if args.verify_only else publish(args.site)
