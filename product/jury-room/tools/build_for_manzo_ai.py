#!/usr/bin/env python3
"""Stage approved jury-room prototype into the generated MANZO AI Pages tree.

The staging publisher does not publish, mutate main, or alter current Home routes.
The Home bridge can be generated separately for owner preview with --home-preview.
"""
from __future__ import annotations
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import argparse, hashlib, shutil, re

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'
BASE='/manzo-ai/'
ROUTE=BASE+'it/laboratorio/stanza-dei-giurati/'
PAGES={
 'index.html':ROUTE,
 'banco-di-prova.html':ROUTE+'banco-di-prova/',
 'officina-locale.html':ROUTE+'officina-locale/',
 'sala-dei-confini.html':ROUTE+'sala-dei-confini/',
}

HOME_CSS='''/* Optional IT-only Home preview: an editorial teaser within the existing challenge. */
#content .ma-v2-challenge:has(.ma-jury-home-bridge){flex-wrap:wrap}
#content .ma-jury-home-bridge{
 box-sizing:border-box;flex:0 0 100%;order:3;min-width:0;
 display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;
 gap:clamp(18px,2.4vw,32px);
 padding:clamp(18px,2.5vw,28px);
 margin-top:4px;border:1px solid #9bc8d6;border-radius:17px;
 background:linear-gradient(112deg,#fff 0%,#f4fbff 74%,#ebf5ff 100%);
 box-shadow:0 12px 32px rgba(25,67,106,.065);
}
#content .ma-jury-preview-info{min-width:0}
#content .ma-jury-preview-badge{
 display:inline-flex;align-items:center;gap:8px;
 padding:7px 11px;border-radius:99px;border:1px solid #a6cbd2;
 background:#e4f5f4;color:#135c64;font-size:.68rem;
 font-weight:830;line-height:1.4;letter-spacing:.065em;
 text-transform:uppercase;
}
#content .ma-jury-preview-badge:before{
 content:"";width:7px;height:7px;border-radius:50%;
 background:#197f7c;flex:none;
}
#content .ma-jury-preview-title{
 font-size:clamp(1.3rem,2vw,1.75rem)!important;
 font-weight:760!important;line-height:1.22!important;
 letter-spacing:-.025em!important;color:#173e59!important;
 margin:12px 0 7px!important;max-width:none!important;
}
#content .ma-jury-preview-description{
 color:#39576d!important;font-size:.93rem!important;
 line-height:1.55!important;margin:0 0 7px!important;max-width:64ch;
}
#content .ma-jury-preview-note{
 color:#506e7e!important;font-size:.77rem!important;
 line-height:1.4!important;margin:0!important;
}
#content .ma-jury-preview-action{
 display:inline-flex;align-items:center;justify-content:center;
 min-height:48px;min-width:190px;padding:12px 18px;gap:10px;
 border:1px solid #154e74;border-radius:11px;
 background:#164f78;color:#fff!important;
 text-decoration:none!important;font-size:.9rem;font-weight:740;
 line-height:1.4;text-align:center;white-space:normal;
 transition:background-color .18s,transform .18s;
}
#content .ma-jury-preview-action:hover{
 background:#103957;transform:translateY(-2px)
}
#content .ma-jury-preview-action:focus-visible{
 outline:3px solid #a64013!important;outline-offset:4px!important
}
@media(max-width:730px){
 #content .ma-jury-home-bridge{grid-template-columns:1fr;gap:15px;padding:18px}
 #content .ma-jury-preview-action{width:100%;min-width:0;box-sizing:border-box}
}
@media(prefers-reduced-motion:reduce){
 #content .ma-jury-preview-action{transition:none!important;transform:none!important}
}
'''

def transformed_html(source:Path):
 doc=BeautifulSoup(source.read_text(encoding='utf-8'),'html.parser')
 for element in doc.select('[href],[src]'):
  for key in ('href','src'):
   if not element.has_attr(key):continue
   val=element[key]
   if val.startswith('assets/'):
    asset=ASSETS/val.removeprefix('assets/')
    if not asset.is_file():raise RuntimeError('Missing prototype asset '+val)
    # Cache safe when updating the source; links remain absolute for Pages subpath.
    digest=hashlib.sha256(asset.read_bytes()).hexdigest()[:12]
    element[key]=BASE+'assets/jury-room/'+asset.name+'?v='+digest
   elif val.startswith('index.html'):
    element[key]=ROUTE+val.removeprefix('index.html')
   else:
    for file,destination in PAGES.items():
     if file!='index.html' and val.startswith(file):
      element[key]=destination+val.removeprefix(file)
      break
 page_route=PAGES[source.name]
 head=doc.head
 if head is None:raise RuntimeError('Document without head '+source.name)
 canonical=doc.new_tag('link',rel='canonical',href='https://manzo8b.github.io'+page_route)
 head.append(canonical)
 title=doc.title.get_text(strip=True)
 image='https://manzo8b.github.io/manzo-ai/assets/jury-room/palazzo-stendardi-manzo.webp'
 for name,value in [('og:title',title),('og:type','website'),('og:image',image)]:
  head.append(doc.new_tag('meta',attrs={'property':name,'content':value}))
 return '<!DOCTYPE html>\n'+str(doc.html)

def insert_home_preview(site:Path):
 """Only runs when explicitly selected for preview, never by default.

 Adds one Italian editorial promo to the existing five-section Home.
 No Academy card, navigation control, or published route is modified.
 """
 home=site/'it'/'index.html'
 if not home.is_file():raise RuntimeError('Home V2 not found at '+str(home))
 doc=BeautifulSoup(home.read_text(encoding='utf-8'),'html.parser')
 sec=doc.select_one('section[data-ma-v2-section="challenge"]')
 if not sec:raise RuntimeError('Approved Home challenge slot absent')
 if doc.select_one('[data-ma-jury-home-preview]'):
  raise RuntimeError('Home staging preview already injected')
 before_sections=len(doc.select('section[data-ma-v2-section]'))
 before_cards=len(doc.select('[data-ma-v2-card]'))
 if before_sections!=5 or before_cards!=6:
  raise RuntimeError('Approved Home V2 contract missing (5 sections and 6 cards)')
 entry=doc.new_tag('aside',attrs={
  'class':'ma-jury-home-bridge',
  'data-ma-jury-home-preview':'v2',
  'aria-labelledby':'ma-jury-preview-title',
 })
 info=doc.new_tag('div',attrs={'class':'ma-jury-preview-info'})
 badge=doc.new_tag('span',attrs={'class':'ma-jury-preview-badge'})
 badge.string='Nuovo esperimento'
 info.append(badge)
 title=doc.new_tag('h3',attrs={'class':'ma-jury-preview-title','id':'ma-jury-preview-title'})
 title.string='La stanza dei giurati'
 info.append(title)
 description=doc.new_tag('p',attrs={'class':'ma-jury-preview-description'})
 description.string='Chiedi, controlla, decidi: tre stanze interattive per mettere alla prova il tuo giudizio davanti a nuove prove.'
 info.append(description)
 note=doc.new_tag('p',attrs={'class':'ma-jury-preview-note'})
 note.string='Scenari fittizi · Nessuna IA collegata · In italiano'
 info.append(note)
 entry.append(info)
 action=doc.new_tag('a',attrs={'class':'ma-jury-preview-action','href':ROUTE})
 action.string='Entra nell’esperimento'
 entry.append(action)
 sec.append(entry)
 if len(doc.select('section[data-ma-v2-section]'))!=before_sections:
  raise RuntimeError('Home sections changed during preview')
 if len(doc.select('[data-ma-v2-card]'))!=before_cards:
  raise RuntimeError('Home cards changed during preview')
 css=site/'assets'/'jury-home-preview.css'
 css.parent.mkdir(parents=True,exist_ok=True)
 css.write_text(HOME_CSS,encoding='utf-8')
 head=doc.head
 head.append(doc.new_tag('link',href=BASE+'assets/jury-home-preview.css',rel='stylesheet'))
 home.write_text('<!DOCTYPE html>\n'+str(doc.html),encoding='utf-8')

def build(site:Path,verify_only:bool=False,home_preview:bool=False):
 asset_out=site/'assets'/'jury-room'
 if not verify_only:
  asset_out.mkdir(parents=True,exist_ok=True)
  for f in ASSETS.iterdir():
   if f.is_file() and f.suffix in {'.js','.css','.svg','.webp','.mp4'}:
    shutil.copy2(f,asset_out/f.name)
 for file,route in PAGES.items():
  target=site/route.removeprefix(BASE)/'index.html'
  if verify_only:
   if not target.is_file():raise RuntimeError('Missing experiment route '+str(target))
   actual=target.read_text(encoding='utf-8')
   if actual!=transformed_html(ROOT/file):
    raise RuntimeError('Generated experiment drift '+str(target))
   h=BeautifulSoup(actual,'html.parser')
   if len(h.select('h1'))!=1 or h.select_one('meta[name="robots"]')['content']!='noindex,nofollow':
    raise RuntimeError('H1 or noindex contract failed '+file)
   for el in h.select('[href],[src]'):
    for key in ('href','src'):
     if not el.has_attr(key):continue
     val=el[key]
     if val.startswith(BASE+'assets/jury-room/'):
      asset_name=val.split('?',1)[0].rsplit('/',1)[-1]
      if not (asset_out/asset_name).is_file():raise RuntimeError('Missing deployed asset '+asset_name)
     if re.match(r'^(?:index|banco-di-prova|officina-locale|sala-dei-confini)\.html',val):
      raise RuntimeError('Unconverted prototype link '+file+' '+val)
   continue
  if target.exists():
   raise RuntimeError('Refusing to overwrite an existing published path: '+str(target))
  target.parent.mkdir(parents=True,exist_ok=True)
  target.write_text(transformed_html(ROOT/file),encoding='utf-8')
  print('STAGED',str(target))
 if home_preview and not verify_only:
  insert_home_preview(site)
 if home_preview and verify_only:
  home=BeautifulSoup((site/'it/index.html').read_text(encoding='utf-8'),'html.parser')
  promo=home.select('aside[data-ma-jury-home-preview="v2"]')
  if len(promo)!=1:
   raise RuntimeError('Home editorial teaser absent or duplicate')
  if len(home.select('section[data-ma-v2-section]'))!=5 or len(home.select('[data-ma-v2-card]'))!=6:
   raise RuntimeError('Home V2 section/card count changed in preview')
  if promo[0].select_one('a.ma-jury-preview-action')['href']!=ROUTE:
   raise RuntimeError('Home editorial teaser destination incorrect')
  if not (site/'assets/jury-home-preview.css').is_file():
   raise RuntimeError('Missing Home editorial teaser CSS')

 if verify_only:
  print('PASS: 4 staging pages, all referenced assets, noindex, canonical and absolute URLs')

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--site',type=Path,required=True)
 parser.add_argument('--verify-only',action='store_true')
 parser.add_argument('--home-preview',action='store_true',help='Optional Home v2 review only, not default')
 args=parser.parse_args()
 build(args.site,args.verify_only,args.home_preview)
if __name__=='__main__':main()
