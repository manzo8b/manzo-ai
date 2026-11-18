#!/usr/bin/env python3
"""Publish three factual, independent MANZO AI 'About' pages before build-seo.

No invented faculty, certification, awards, client work or educational results.
Canonical/alternate OG/sitemap are added by the existing SEO publishers.
"""
from __future__ import annotations
import argparse
from html import escape
from pathlib import Path

BASE="/manzo-ai/"
AUTHOR="Marcelo Javier Fernandez Caballero"
ROUTES={"it":"chi-siamo","en":"about","es":"quienes-somos"}
COPY={
 "it":{
  "title":"Chi cura MANZO AI","lead":"Un progetto indipendente dedicato alla formazione, alla progettazione di strumenti digitali e alla verifica critica dei contenuti prodotti con l'IA.",
  "owner":"Autore e curatore","heading":"Un laboratorio indipendente, non un ente di certificazione",
  "about":"MANZO AI è ideato e curato da Marcelo Javier Fernandez Caballero. Il progetto unisce progettazione formativa, sperimentazione di strumenti digitali e un metodo di controllo degli output dell'intelligenza artificiale.",
  "method":"Come lavoriamo","principle":"Il docente progetta, l'IA assiste, il docente verifica e decide",
  "method_text":"Le risorse partono da obiettivi concreti, procedono per esempi e laboratori e distinguono le informazioni documentate dalle ipotesi o dalle dimostrazioni. La responsabilità del risultato resta umana.",
  "limits":"Che cosa non promettiamo",
  "limits_text":"Non siamo una scuola, un'università o un ente di formazione accreditato. I laboratori pubblici sono materiali divulgativi e strumenti in evoluzione. Non rilasciano titoli o certificazioni, né dimostrano da soli un miglioramento dell'apprendimento.",
  "transparency":"Trasparenza",
  "transparency_text":"Alcuni contenuti e immagini possono essere realizzati con strumenti di IA generativa e sono sottoposti a revisione editoriale. Le funzioni sperimentali e i limiti tecnici sono identificati nelle rispettive pagine.",
  "back":"Torna alla homepage","learn":"Esplora i percorsi","portfolio":"Portfolio del curatore","github":"Codice e documentazione",
  "desc":"MANZO AI è un progetto indipendente di Marcelo Javier Fernandez Caballero: formazione, strumenti digitali, metodo di verifica e limiti dichiarati."
 },
 "en":{
  "title":"About MANZO AI","lead":"An independent project exploring training, digital tools and critical review of AI-assisted content.",
  "owner":"Creator and curator","heading":"An independent lab, not a certification body",
  "about":"MANZO AI is created and curated by Marcelo Javier Fernandez Caballero. The project brings together educational design, digital-tool prototyping and human review of AI outputs.",
  "method":"Our approach","principle":"Educators design, AI assists, educators verify and decide",
  "method_text":"Resources begin with concrete goals, progress through examples and workshops, and distinguish documented facts from assumptions or demonstrations. People remain accountable for the outcomes.",
  "limits":"What we do not claim","limits_text":"We are not a school, university or accredited training provider. Public labs are educational resources and evolving prototypes. They do not issue qualifications or certificates, nor prove learning gains on their own.",
  "transparency":"Transparency","transparency_text":"Some content and images may be created with generative AI tools and are editorially reviewed. Experimental functions and technical limitations are described on the relevant pages.",
  "back":"Back to homepage","learn":"Explore learning paths","portfolio":"Creator's portfolio","github":"Source code and documentation",
  "desc":"About MANZO AI, an independent educational and digital-tools project curated by Marcelo Javier Fernandez Caballero, with transparent methods and limitations."
 },
 "es":{
  "title":"Quién está detrás de MANZO AI","lead":"Un proyecto independiente de formación, diseño de herramientas digitales y evaluación crítica de contenidos creados con IA.",
  "owner":"Creador y responsable editorial","heading":"Un laboratorio independiente, no una entidad certificadora",
  "about":"MANZO AI es un proyecto creado y dirigido editorialmente por Marcelo Javier Fernandez Caballero. Combina diseño educativo, experimentación con herramientas digitales y revisión humana de los resultados de la IA.",
  "method":"Nuestro método","principle":"El docente diseña, la IA asiste, el docente verifica y decide",
  "method_text":"Los recursos parten de objetivos concretos, avanzan mediante ejemplos y talleres y distinguen los hechos documentados de las hipótesis y simulaciones. La responsabilidad de los resultados sigue siendo humana.",
  "limits":"Qué no prometemos","limits_text":"No somos una escuela, universidad ni entidad de formación acreditada. Los laboratorios públicos son recursos divulgativos y prototipos en evolución. No otorgan títulos ni certificaciones y no demuestran por sí solos una mejora del aprendizaje.",
  "transparency":"Transparencia","transparency_text":"Algunos contenidos e imágenes pueden crearse mediante IA generativa y son objeto de revisión editorial. Las funciones experimentales y sus límites técnicos se indican en cada página.",
  "back":"Volver al inicio","learn":"Explorar formación","portfolio":"Portfolio del creador","github":"Código y documentación",
  "desc":"MANZO AI, proyecto independiente de Marcelo Javier Fernandez Caballero: formación, diseño digital, revisión humana y límites declarados."
 }
}
def e(s):return escape(str(s),quote=True)

def render(lang):
 c=COPY[lang]
 here=BASE+lang+"/"+ROUTES[lang]+"/"
 learning=BASE+lang+("/academia/" if lang=="es" else "/academy/")
 intro=f'<p class="intro">{e(c["lead"])}</p>'
 links=''.join(f'<a href="{BASE}{l}/{ROUTES[l]}/" lang="{l}" {"aria-current=page" if lang==l else ""}>{e({"it":"Italiano","en":"English","es":"Español"}[l])}</a>' for l in ("it","en","es"))
 return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#ffffff">
<title>{e(c["title"])} | MANZO AI</title>
<meta name="description" content="{e(c["desc"])}">
<link rel="canonical" href="{here}">
<style>
:root{{color-scheme:light;font-family:system-ui,-apple-system,"Segoe UI",sans-serif;color:#111827;background:white}}
*{{box-sizing:border-box}}body{{margin:0;background:#fff;color:#111827;line-height:1.58}}a{{color:#205beb}}a:focus-visible{{outline:3px solid #e97e17;outline-offset:4px}}
.wrap{{width:min(100% - 32px,940px);margin:auto}}
header{{border-bottom:1px solid #cdddf1;background:#fff}}
.top{{display:flex;align-items:center;justify-content:space-between;gap:20px;min-height:80px}}
.brand{{font-weight:850;letter-spacing:-.03em;text-decoration:none;color:#111827}}
.languages{{display:flex;gap:11px;flex-wrap:wrap}}.languages a{{font-size:.82rem;padding:7px 9px;border-radius:9px;text-decoration:none}}
.languages a[aria-current=page]{{background:#e8f0ff;font-weight:800}}
main{{padding-top:60px;padding-bottom:65px}}
.kicker{{color:#205beb;font-weight:900;letter-spacing:.12em;text-transform:uppercase;font-size:.77rem;margin:0 0 16px}}
h1{{font-size:clamp(2.3rem,6.5vw,4.8rem);line-height:1.06;letter-spacing:-.06em;margin:0 0 22px;max-width:16ch}}
.intro{{font-size:clamp(1.08rem,2.4vw,1.35rem);line-height:1.52;color:#2e3b51;max-width:66ch}}
.byline{{border-left:5px solid #e97e17;background:#fff2e3;padding:14px 18px;margin:30px 0 35px;border-radius:0 12px 12px 0}}
.byline strong{{display:block;font-size:1.05rem}}.byline span{{font-size:.86rem;color:#4a5670}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
article{{background:white;border:1.5px solid #bfd0ea;border-top:5px solid #205beb;border-radius:18px;padding:25px;min-width:0}}
article:nth-child(2){{border-top-color:#e97e17}}article:nth-child(3){{border-top-color:#edb120}}article:nth-child(4){{border-top-color:#df3d34}}
h2{{margin:0 0 12px;font-size:1.2rem;line-height:1.2;letter-spacing:-.02em}}article p{{margin:0;color:#2e3b51}}
.actions{{margin:35px 0;display:flex;gap:10px;flex-wrap:wrap}}.actions a{{display:inline-flex;align-items:center;justify-content:center;min-height:46px;padding:12px 17px;text-decoration:none;border:1.5px solid #205beb;border-radius:11px;font-size:.87rem;font-weight:800}}
.actions a:first-child{{background:#205beb;color:white}}.actions a:hover{{background:#eff4ff;color:#1548b7}}.actions a:first-child:hover{{background:#1647b8;color:white}}
footer{{border-top:1px solid #d2dfef;padding:22px 0;font-size:.83rem;color:#44546a}}
@media(max-width:600px){{.top{{min-height:68px;flex-wrap:wrap;padding:12px 0}}main{{padding-top:35px}}.grid{{grid-template-columns:1fr}}article{{padding:19px}}h1{{font-size:clamp(2rem,10vw,3.4rem)}}}}
</style>
</head>
<body>
<header><div class="wrap top"><a class="brand" href="{BASE}{lang}/">MANZO AI</a><nav class="languages" aria-label="Lingue / Languages / Idiomas">{links}</nav></div></header>
<main class="wrap"><p class="kicker">MANZO AI / {e(c["owner"])}</p>
<h1>{e(c["title"])}</h1>{intro}
<div class="byline"><strong>{AUTHOR}</strong><span>{e(c["owner"])}</span></div>
<div class="grid">
<article><h2>{e(c["heading"])}</h2><p>{e(c["about"])}</p></article>
<article><h2>{e(c["method"])}</h2><p><strong>{e(c["principle"])}</strong></p><p>{e(c["method_text"])}</p></article>
<article><h2>{e(c["limits"])}</h2><p>{e(c["limits_text"])}</p></article>
<article><h2>{e(c["transparency"])}</h2><p>{e(c["transparency_text"])}</p></article>
</div>
<div class="actions">
<a href="{BASE}{lang}/">{e(c["back"])}</a>
<a href="{learning}">{e(c["learn"])}</a>
<a href="https://manzo8b.github.io/marcelus/it/">{e(c["portfolio"])}</a>
<a href="https://github.com/manzo8b/manzo-ai">{e(c["github"])}</a>
</div>
</main><footer><div class="wrap">MANZO AI · {e(c["owner"])}: {AUTHOR} · Progetto indipendente</div></footer>
</body></html>'''

def apply(site,verify_only=False):
 for lang,slug in ROUTES.items():
  file=site/lang/slug/"index.html"
  if verify_only:
   if not file.is_file():raise RuntimeError("Missing about page: "+str(file))
   html=file.read_text(encoding="utf-8")
   for text in (AUTHOR,'rel="canonical"',f'lang="{lang}"', "non una" if lang=="it" else ctext(lang)):
    if text not in html:raise RuntimeError("Incomplete about page: "+str(file)+" => "+text)
   continue
  if file.is_file():raise RuntimeError("Refuse overwrite of existing about page "+str(file))
  file.parent.mkdir(parents=True,exist_ok=True)
  file.write_text(render(lang),encoding="utf-8")
 print("MANZO AI independent curator pages: IT/EN/ES; checked="+str(verify_only))
def ctext(lang):return "not an" if lang=="en" else "no una"

if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("--site",required=True,type=Path)
 p.add_argument("--verify-only",action="store_true")
 a=p.parse_args()
 apply(a.site,a.verify_only)
