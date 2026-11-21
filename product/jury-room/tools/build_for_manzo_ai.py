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

HOME_CSS='''/* Staging concept only: preserve the existing approved Home challenge */
.ma-jury-home-bridge{display:inline-flex;align-items:center;gap:12px;min-height:44px;
 margin-top:10px;padding:10px 14px;border:1px solid #8ab3df;border-radius:11px;
 color:#154575!important;background:#f3f9ff;text-decoration:none!important;
 font-size:.85rem;font-weight:750;line-height:1.5}
.ma-jury-home-bridge:hover{background:#e7f4ff;border-color:#2265b5}
.ma-jury-home-bridge:focus-visible{outline:3px solid #dd7127;outline-offset:3px}
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
 """Only runs when explicitly selected in a staging build, never by default."""
 home=site/'it'/'index.html'
 if not home.is_file():raise RuntimeError('Home V2 not found at '+str(home))
 doc=BeautifulSoup(home.read_text(encoding='utf-8'),'html.parser')
 sec=doc.select_one('section[data-ma-v2-section="challenge"]')
 if not sec:raise RuntimeError('Approved Home challenge slot absent')
 if doc.select_one('[data-ma-jury-home-preview]'):
  raise RuntimeError('Home staging preview already injected')
 entry=doc.new_tag('a',href=ROUTE)
 entry['class']='ma-jury-home-bridge'
 entry['data-ma-jury-home-preview']='v1'
 entry.string='Entra nella stanza dei giurati · Esperimenti  ↗'
 sec.append(entry)
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
  home=(site/'it/index.html').read_text(encoding='utf-8')
  if home.count('data-ma-jury-home-preview="v1"')!=1:
   raise RuntimeError('Home preview entry missing or duplicate')
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
