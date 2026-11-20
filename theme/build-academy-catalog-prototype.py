#!/usr/bin/env python3
"""Build an independent MANZO AI Academy prototype (NOT part of the public deploy).
Derived only from academy/catalog-v1.json: no duplicate catalog content.
Creates a standalone HTML preview, with real source-evidenced destinations.
"""
from __future__ import annotations
import argparse
import json
from html import escape
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
SOURCE=ROOT/"academy/catalog-v1.json"
BASE="/manzo-ai/"
CAT_LABEL={
 "foundations":"Fondamenti e alfabetizzazione",
 "prompt_build":"Prompt e progettazione",
 "reliability":"Affidabilità e pensiero critico",
 "governance":"Sicurezza e governance",
 "teaching":"Didattica e produzione",
}
PRACTICE={
 "interactive":"Laboratorio interattivo",
 "guided":"Esercizio guidato",
 "separate_studio":"Studio collegato",
 "assessment":"Quiz e verifica",
 "static_activity":"Attività nella lezione",
}
HEAD={
 "course":("Percorsi formativi","Corso","Apri il corso"),
 "foundation_module":("Base essenziale","Modulo fondativo","Apri il modulo")
}
CSS=r'''
:root{--ink:#15344d;--blue:#2656d8;--muted:#5a7187;--line:#dce6f1;--bg:#fff}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f7faff;color:var(--ink);font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
a{color:inherit}button,select{font:inherit}button:focus-visible,select:focus-visible,a:focus-visible{outline:3px solid #d27131;outline-offset:3px}
.shell{width:min(1200px,calc(100% - 38px));margin:auto}.top{display:flex;align-items:center;gap:20px;justify-content:space-between;padding:21px 0}
.logo{font-weight:900;letter-spacing:-.04em;font-size:1.15rem;text-decoration:none}.logo span{color:#326ce2}.top a:last-child{font-size:.82rem;color:#2253a8}
.crumbs{font-size:.78rem;color:#53718c;padding:14px 0}.crumbs a{text-decoration:underline;text-underline-offset:3px}
.hero{isolation:isolate;position:relative;overflow:hidden;min-height:260px;padding:44px clamp(25px,5vw,70px);border:1px solid #d1e0f4;border-radius:27px;background:radial-gradient(circle at 90% 30%,#dce6ff 0%,transparent 37%),radial-gradient(circle at 80% 80%,#c8f2ef 0%,transparent 25%),linear-gradient(120deg,#fff,#f5faff);box-shadow:0 18px 56px #2047650e}
.hero:after{position:absolute;content:"";width:300px;height:300px;right:-65px;top:-75px;border:1px solid #96b9e457;border-radius:50%;box-shadow:0 0 0 29px #96b9e40d,0 0 0 70px #96b9e409;pointer-events:none}
.eyebrow{font-size:.66rem;letter-spacing:.16em;text-transform:uppercase;font-weight:840;color:#236abc;margin:0 0 20px}
.hero h1{font-size:clamp(2.45rem,5vw,4.6rem);max-width:20ch;line-height:1.08;letter-spacing:-.055em;margin:0 0 17px}
.hero p:last-child{max-width:67ch;line-height:1.65;color:#48677f;font-size:1.02rem}
.find{background:#fff;border:1px solid var(--line);border-radius:21px;margin:23px 0 42px;padding:24px 26px;box-shadow:0 10px 28px #2047650b}
.find h2{font-size:1.08rem;letter-spacing:-.025em;margin:0 0 17px}.filters{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.filters label{font-size:.73rem;color:#3e5b74;font-weight:760;display:grid;gap:7px}
.filters select{min-width:0;width:100%;min-height:45px;padding:10px 12px;border:1px solid #c1d4e5;background:#fff;border-radius:11px;color:#214966}
.filter-bottom{display:flex;justify-content:space-between;align-items:center;gap:15px;flex-wrap:wrap;margin-top:17px}.count{color:#557087;font-size:.82rem}.reset{border:1px solid #bcd1e6;background:#f3f8ff;padding:9px 13px;border-radius:10px;cursor:pointer;color:#1b55a0;font-weight:760}
.group{margin-bottom:50px}.grouphead{display:flex;align-items:end;justify-content:space-between;gap:12px;border-bottom:1px solid #cddfed;margin-bottom:19px;padding-bottom:14px}
.grouphead h2{font-size:clamp(1.45rem,2.3vw,2.1rem);letter-spacing:-.045em;margin:0}.grouphead p{font-size:.82rem;color:#5a758c;margin:0}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:17px}
.card{border:1px solid #d3e1ed;border-radius:18px;background:#fff;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 7px 24px #16446113;min-width:0;transition:transform .23s ease,box-shadow .23s ease,border-color .23s ease}
.card:hover,.card:focus-within{transform:translateY(-5px);border-color:#9cbce8;box-shadow:0 20px 42px #1644612a}
.art{height:130px;background:linear-gradient(120deg,var(--tone),var(--tone2));position:relative;overflow:hidden;padding:17px;color:white;display:flex;flex-direction:column;justify-content:space-between;font-size:.73rem;letter-spacing:.11em;font-weight:790}
.art:after{content:"";position:absolute;border:1px solid #ffffff60;border-radius:50%;width:180px;height:180px;top:-90px;right:14%;box-shadow:0 0 0 25px #ffffff12,0 0 0 52px #ffffff0a;transition:transform .3s}
.card:hover .art:after{transform:translate(-16px,16px) scale(1.07)}
.art .symbol{position:absolute;right:14%;top:44%;transform:translateY(-50%);font-size:2.5rem;font-weight:650;opacity:.8}
.card-body{padding:20px;display:flex;flex:1;flex-direction:column;gap:11px}
.meta{font-size:.68rem;color:#39718c;font-weight:810;text-transform:uppercase;letter-spacing:.075em}
.card h3{font-size:1.24rem;line-height:1.26;letter-spacing:-.027em;margin:0;font-weight:720}
.tags{display:flex;flex-wrap:wrap;gap:6px}.tags span{border:1px solid #d7e5f0;background:#f2f7fc;border-radius:7px;padding:5px 7px;color:#3f617a;font-weight:700;font-size:.69rem}
.outcome{font-size:.85rem;line-height:1.5;color:#385b74;margin:0}
.outcome strong{display:block;font-size:.67rem;color:#2d6590;letter-spacing:.07em;text-transform:uppercase;margin-bottom:3px}
.audience{font-size:.76rem;line-height:1.5;color:#5a7187;margin:0}
.audience strong{font-weight:760;color:#365977}
.note{font-size:.76rem;line-height:1.45;color:#5a7187;margin:0}.go{margin-top:auto;text-decoration:none;border-top:1px solid #e2eaf2;padding-top:12px;font-size:.83rem;font-weight:780;display:flex;align-items:center;justify-content:space-between;color:#245da4}
.go span{border-radius:50%;background:#eaf0ff;color:#2456c3;width:29px;height:29px;display:grid;place-items:center}
.card:hover .go span{background:#255ce0;color:#fff}
.no-results{display:none;padding:30px;border:1px solid #cfdcec;border-radius:16px;text-align:center;color:#456980}
.extra{border-radius:20px;background:linear-gradient(120deg,#eaf4ff,#eefaf8);padding:24px 28px;margin-bottom:44px;display:flex;justify-content:space-between;gap:12px;align-items:center}
.extra h2{font-size:1.4rem;letter-spacing:-.035em;margin:0 0 8px}.extra p{margin:0;color:#47667e;font-size:.85rem;line-height:1.5}
.extra a{white-space:nowrap;font-size:.85rem;font-weight:790;color:#164f9a}
.foot{border-top:1px solid #d5e5f0;padding:24px 0 45px;color:#657c91;font-size:.8rem;line-height:1.6}
[hidden]{display:none!important}
@media(max-width:960px){.cards{grid-template-columns:repeat(2,minmax(0,1fr))}.filters{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:600px){.shell{width:min(100% - 24px,1200px)}.hero{padding:27px 22px}.cards,.filters{grid-template-columns:1fr}.extra{display:block}.extra a{display:inline-block;margin-top:16px}.card h3{font-size:1.2rem}}
@media(hover:none){.card:hover{transform:none}.card:hover .art:after{transform:none}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{transition:none!important;animation:none!important;scroll-behavior:auto!important}.card:hover{transform:none!important}}
'''
JS=r'''
"use strict";
(()=>{
 const controls=[...document.querySelectorAll("[data-filter]")];
 const cards=[...document.querySelectorAll("[data-card]")];
 const count=document.querySelector("[data-count]");
 const groups=[...document.querySelectorAll("[data-group]")];
 const empty=document.querySelector("[data-empty]");
 function apply(){
   const state=Object.fromEntries(controls.map(c=>[c.name,c.value]));
   let shown=0;
   for(const card of cards){
     const terms=card.dataset;
     const ok=(state.topic==="all"||terms.topic===state.topic)&&
       (state.kind==="all"||terms.kind===state.kind)&&
       (state.practice==="all"||terms.practice.split(" ").includes(state.practice))&&
       (state.language==="all"||terms.languages.split(" ").includes(state.language));
     card.hidden=!ok;if(ok)shown++;
     const target=state.language==="all"?"it":state.language;
     const href=terms["url"+target.charAt(0).toUpperCase()+target.slice(1)];
     const link=card.querySelector(".go");
     if(ok&&href)link.href=href;
   }
   for(const group of groups)
     group.hidden=group.querySelectorAll("[data-card]:not([hidden])").length===0;
   count.textContent=shown+" risultati su "+cards.length+" unità principali";
   empty.hidden=shown!==0;
 }
 for(const c of controls)c.addEventListener("change",apply);
 document.querySelector("[data-reset]").addEventListener("click",()=>{
   for(const c of controls)c.value="all";apply();
 });
 apply();
})();
'''
def safe(t):return escape(str(t),quote=True)
def render_card(item):
    cat=item["category"]
    tones={
      "reliability":("#1d5c88","#263e69","◇"),
      "prompt_build":("#206e93","#384ca0","⌘"),
      "governance":("#2d637b","#3a415d","◎"),
      "teaching":("#6659a0","#455f99","✦"),
      "foundations":("#246b87","#1b4b77","◈"),
    }
    bg1,bg2,symbol=tones[cat]
    route={k:BASE+v+"/" if v else "" for k,v in item["route"].items()}
    available=" ".join(k for k,v in route.items() if v)
    href=route["it"]
    kind_name=HEAD[item["kind"]][1]
    open_label=HEAD[item["kind"]][2]
    practice_label=next((PRACTICE[x] for x in item["practice"] if x in PRACTICE),"Attività nella lezione")
    tags="".join("<span>"+safe(PRACTICE[x])+"</span>" for x in item["practice"][:2] if x in PRACTICE)
    if item["kind"]=="foundation_module" and item["lab_relation"]=="no_dedicated_interactive_lab":
       tags="<span>Attività nella lezione</span><span>Nessun laboratorio dedicato</span>"
    lang_display=" · ".join(k.upper() for k in ("it","en","es") if route[k])
    code=(" · "+item["code"]) if "code" in item else ""
    attrs=" ".join(f'data-url-{k}="{safe(v)}"' for k,v in route.items())
    return f'''<article class="card" data-card="{safe(item["id"])}" data-kind="{safe(item["kind"])}"
      data-topic="{safe(cat)}" data-practice="{safe(" ".join(item["practice"]))}"
      data-languages="{safe(available)}" {attrs}>
      <div class="art" style="--tone:{bg1};--tone2:{bg2}"><span>MANZO AI / {safe(kind_name)}</span>
        <span class="symbol" aria-hidden="true">{symbol}</span><span>{safe(item["id"].upper())}</span></div>
      <div class="card-body"><span class="meta">{safe(kind_name+code)} · {safe(CAT_LABEL[cat])}</span>
      <h3>{safe(item["title_it"])}</h3>
      <p class="outcome"><strong>Risultato atteso</strong>{safe(item["outcome_it"])}</p>
      <p class="audience"><strong>A chi serve</strong> · {safe(item["audience_it"])}</p>
      <div class="tags">{tags}</div>
      <p class="note">Lingue con rotta documentata: {safe(lang_display)}</p>
      <a class="go" href="{safe(href)}">{safe(open_label)}<span aria-hidden="true">↗</span></a>
      </div></article>'''

def make():
    data=json.loads(SOURCE.read_text(encoding="utf-8"))
    items=data["items"]
    if len(items)!=15 or len({i["id"] for i in items})!=15:
       raise ValueError("Catalog inventory invalid: 15 unique units expected")
    options=lambda values:''.join(f'<option value="{safe(key)}">{safe(value)}</option>' for key,value in values)
    filters=[
       ("topic","Tema",[("all","Tutti i temi"),*[(k,v) for k,v in CAT_LABEL.items()]]),
       ("kind","Tipo di contenuto",[("all","Tutti i tipi"),("course","Corso"),("foundation_module","Modulo fondativo")]),
       ("practice","Tipo di pratica",[("all","Tutte le pratiche"),*[(k,v) for k,v in PRACTICE.items()]]),
       ("language","Lingua",[("all","Tutte le lingue"),("it","Italiano"),("en","English"),("es","Español")]),
    ]
    fields=''.join(f'<label>{safe(label)}<select name="{safe(name)}" data-filter>{options(opts)}</select></label>' for name,label,opts in filters)
    sections=[]
    for kind in ("course","foundation_module"):
       subset=[i for i in items if i["kind"]==kind]
       sections.append(f'<section class="group" data-group="{kind}"><div class="grouphead"><h2>{HEAD[kind][0]}</h2><p>{len(subset)} unità censite</p></div><div class="cards">'
                       +''.join(render_card(i) for i in subset)+'</div></section>')
    html=f'''<!doctype html><html lang="it"><head><meta charset="utf-8">
 <meta name="viewport" content="width=device-width,initial-scale=1">
 <meta name="robots" content="noindex,nofollow">
 <title>Anteprima Catalogo Academy | MANZO AI</title>
 <style>{CSS}</style></head><body>
 <div class="shell"><header class="top"><a class="logo" href="/manzo-ai/it/">MANZO <span>AI</span></a>
 <a href="/manzo-ai/it/academy/">Torna all'Academy attuale</a></header>
 <nav class="crumbs" aria-label="Percorso di navigazione"><a href="/manzo-ai/it/">Home</a> › Catalogo Academy (anteprima)</nav>
 <main><section class="hero"><p class="eyebrow">MANZO AI / ACADEMY · PROTOTIPO IN REVISIONE</p>
 <h1>Scegli cosa imparare, non solo cosa aprire</h1>
 <p>Parti dall'obiettivo. Distingui un corso da un modulo fondativo, scopri le pratiche davvero disponibili e scegli la lingua di studio.</p></section>
 <section class="find" aria-label="Filtri del catalogo"><h2>Trova il percorso più adatto</h2>
 <div class="filters">{fields}</div><div class="filter-bottom"><p class="count" data-count role="status" aria-live="polite"></p>
 <button class="reset" type="button" data-reset>Azzera filtri</button></div></section>
 <div data-empty class="no-results" hidden>Nessun risultato con questi filtri. Prova a cambiarli.</div>
 {''.join(sections)}
 <aside class="extra"><div><h2>Percorsi consigliati</h2><p>Tre sequenze guidate sono già disponibili nell'Academy. Non sono corsi aggiuntivi.</p></div>
 <a href="/manzo-ai/it/academy/#ma-journey-title-it">Esplora i percorsi guidati ↗</a></aside>
 <aside class="extra"><div><h2>Laboratori, strumenti e risorse</h2>
 <p>Glossari, simulatori, AI Radar e materiali complementari hanno una sezione distinta dai corsi.</p></div>
 <a href="/manzo-ai/it/risorse/">Apri le risorse ↗</a></aside>
 </main><footer class="foot">Anteprima UX non pubblicata · 9 corsi editoriali + 6 moduli fondativi.
 Le rotte provengono dai publisher e dai test di deploy; disponibilità finale da verificare.
 Gli obiettivi sintetici delle card sono proposte editoriali da validare contro i programmi.
 Nessuna iscrizione, avanzamento o attestato simulato.</footer></div>
 <script>{JS}</script></body></html>'''
    return html

def run(out:Path):
    html=make()
    if html.count('data-card="')!=15 or html.count("data-filter")!=5: # four selects + JS string
       raise ValueError("Preview card/filter generation mismatch")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(html,encoding="utf-8")
    print(f"PASS Academy prototype: {out}, 15 unique cards, four filters, mobile CSS, noindex")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    run(args.output)
