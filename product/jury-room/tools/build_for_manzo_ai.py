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

HOME_CSS='''/* Feature-first preview for the approved MANZO AI Italian Home v2.
   The original hero message, magic illustration and five-page-section contract remain.
   No new sidebar, card grid item or independent banner section is introduced. */
#content .ma-v2-hero:has(.ma-jury-hero-feature){
 padding-bottom:0!important;align-content:start;
}
#content .ma-jury-top-notice{
 display:inline-flex;align-items:center;gap:10px;
 margin:2px 0 18px;padding:9px 15px;max-width:100%;
 color:#fff!important;background:#a7233b;border:1px solid #a7233b;
 border-radius:100px;text-decoration:none!important;
 font-size:.73rem;font-weight:800;line-height:1.35;
 letter-spacing:.025em;transition:background-color .2s,transform .2s;
}
#content .ma-jury-top-notice:hover{background:#75152b;transform:translateY(-2px)}
#content .ma-jury-top-notice:focus-visible,
#content .ma-jury-feature-action:focus-visible{
 outline:3px solid #f7b34b!important;outline-offset:4px!important;
}
#content .ma-jury-top-notice svg{width:14px;height:14px;flex:none}
#content .ma-jury-hero-feature{
 grid-column:1/-1;position:relative;isolation:isolate;min-width:0;
 display:flex;align-items:flex-end;justify-content:stretch;
 min-height:clamp(300px,28vw,398px);overflow:hidden;
 margin:clamp(22px,2.8vw,38px) calc(-1 * clamp(22px,4vw,62px)) 0;
 color:#fff!important;scroll-margin-top:80px;
 background:#14395f;
}
#content .ma-jury-feature-image{
 position:absolute;z-index:-2;inset:0;width:100%;height:100%;
 object-fit:cover;object-position:center 47%;
 filter:saturate(1.06);transform:scale(1.005);
 transition:transform .7s cubic-bezier(.2,.7,.2,1);
}
#content .ma-jury-hero-feature:hover .ma-jury-feature-image{transform:scale(1.045)}
#content .ma-jury-hero-feature:before{
 content:"";position:absolute;z-index:-1;inset:0;
 background:linear-gradient(180deg,rgba(9,25,51,.08) 0%,rgba(10,28,54,.07) 40%,rgba(10,27,53,.65) 67%,rgba(10,27,53,.98) 100%);
 pointer-events:none;
}
#content .ma-jury-feature-content{
 position:relative;display:flex;align-items:flex-end;justify-content:space-between;
 gap:30px;max-width:1180px;width:100%;margin:auto auto 0;
 padding:clamp(92px,11vw,140px) clamp(24px,4.4vw,60px) clamp(25px,3vw,37px);
 box-sizing:border-box;
}
#content .ma-jury-feature-copy{min-width:0;max-width:650px}
#content .ma-jury-feature-eyebrow{
 display:inline-flex;align-items:center;gap:8px;
 margin:0 0 10px!important;color:#dbf5ff!important;
 font-weight:820;font-size:.72rem!important;letter-spacing:.12em;line-height:1.4;
 text-transform:uppercase;
}
#content .ma-jury-feature-eyebrow:before{
 content:"";flex:none;width:8px;height:8px;border-radius:50%;background:#ff536c;
 box-shadow:0 0 0 4px rgba(255,83,108,.20);
}
#content .ma-jury-feature-title{
 color:#fff!important;font-size:clamp(1.9rem,3.8vw,3.35rem)!important;
 font-weight:790!important;letter-spacing:-.035em!important;
 line-height:1.05!important;max-width:20ch!important;
 margin:0 0 10px!important;text-shadow:0 2px 20px rgba(6,26,52,.22);
}
#content .ma-jury-feature-description{
 color:#fff!important;font-size:clamp(.9rem,1.25vw,1rem)!important;
 line-height:1.5!important;margin:0 0 11px!important;max-width:56ch;
}
#content .ma-jury-feature-meta{
 color:#dcecf7!important;font-size:.75rem!important;line-height:1.4!important;
 margin:0!important;
}
#content .ma-jury-feature-action{
 flex:none;display:inline-flex;align-items:center;justify-content:center;
 gap:11px;min-height:52px;padding:13px 22px;min-width:204px;
 box-sizing:border-box;border-radius:11px;border:1px solid #e0f3ff;
 background:#fff;color:#124366!important;text-decoration:none!important;
 font-size:.93rem!important;font-weight:790;line-height:1.4;white-space:normal;
 box-shadow:0 6px 28px rgba(8,28,56,.2);
 transition:background-color .2s,transform .2s;
}
#content .ma-jury-feature-action:hover{
 background:#e1f4ff;transform:translateY(-3px);
}
@media(max-width:1100px){
 #content .ma-jury-hero-feature{
  margin-left:calc(-1 * clamp(22px,4vw,62px));
  margin-right:calc(-1 * clamp(22px,4vw,62px));
 }
}
@media(max-width:760px){
 #content .ma-jury-hero-feature{
  min-height:510px;margin-left:-20px;margin-right:-20px;display:block
 }
 /* Show the COMPLETE palace image on mobile. Neither MANZO banner is cropped. */
 #content .ma-jury-feature-image{
  top:0;left:0;width:100%;height:auto;aspect-ratio:1672/941;
  object-fit:contain;object-position:center top;
 }
 #content .ma-jury-hero-feature:before{
  background:linear-gradient(180deg,
   transparent 0%,transparent 38%,
   rgba(10,27,53,.82) 46%,#0a1b35 54%,#0a1b35 100%)
 }
 #content .ma-jury-feature-content{
  flex-direction:column;align-items:stretch;justify-content:flex-end;
  min-height:510px;gap:17px;
  padding:clamp(200px,58vw,270px) 21px 24px
 }
 #content .ma-jury-feature-title{font-size:clamp(1.8rem,7.8vw,2.5rem)!important}
 #content .ma-jury-feature-action{min-width:0;width:100%}
 #content .ma-jury-top-notice{margin-top:0}
}
@media(max-width:540px){
 #content .ma-jury-top-notice{font-size:.69rem;padding:9px 12px}
 #content .ma-jury-feature-description{font-size:.89rem!important}
}
@media(prefers-reduced-motion:reduce){
 #content .ma-jury-feature-image,#content .ma-jury-top-notice,
 #content .ma-jury-feature-action{transition:none!important;transform:none!important}
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
 """Render a cinematic full-width experiment preview *inside* the Italian Home Hero.

 Only when --home-preview is explicitly selected. Preserves original Hero
 content and animation, the five sections, six Academy cards, and navigation.
 """
 home=site/'it'/'index.html'
 if not home.is_file():raise RuntimeError('Home V2 not found at '+str(home))
 doc=BeautifulSoup(home.read_text(encoding='utf-8'),'html.parser')
 hero=doc.select_one('section[data-ma-v2-section="hero"]')
 copy=hero.select_one('.ma-v2-hero-copy') if hero else None
 kicker=copy.select_one('.ma-v2-kicker') if copy else None
 if not hero or not kicker:raise RuntimeError('Approved Home Hero and kicker absent')
 if doc.select_one('[data-ma-jury-home-preview]'):
  raise RuntimeError('Home staging preview already injected')
 before_sections=len(doc.select('section[data-ma-v2-section]'))
 before_cards=len(doc.select('[data-ma-v2-card]'))
 if before_sections!=5 or before_cards!=6:
  raise RuntimeError('Approved Home V2 contract missing (5 sections and 6 cards)')
 image=ASSETS/'palazzo-stendardi-manzo.webp'
 if not image.is_file():raise RuntimeError('Missing approved jury-room artwork')
 digest=hashlib.sha256(image.read_bytes()).hexdigest()[:12]
 src=BASE+'assets/jury-room/palazzo-stendardi-manzo.webp?v='+digest

 quick=doc.new_tag('a',attrs={'class':'ma-jury-top-notice',
   'href':'#ma-jury-hero-feature','data-ma-jury-top-badge':'v3'})
 quick.string='NUOVO ESPERIMENTO · LA STANZA DEI GIURATI ↓'
 kicker.insert_after(quick)

 feature=doc.new_tag('div',attrs={'class':'ma-jury-hero-feature',
   'id':'ma-jury-hero-feature','data-ma-jury-home-preview':'v3',
   'role':'group','aria-labelledby':'ma-jury-preview-title'})
 preview_image=doc.new_tag('img',attrs={
   'class':'ma-jury-feature-image','src':src,
   'alt':'La stanza dei giurati, con tre porte illuminate e due stendardi MANZO',
   'width':'1672','height':'941','fetchpriority':'high','decoding':'async',
 })
 feature.append(preview_image)
 content=doc.new_tag('div',attrs={'class':'ma-jury-feature-content'})
 block=doc.new_tag('div',attrs={'class':'ma-jury-feature-copy'})
 eyebrow=doc.new_tag('p',attrs={'class':'ma-jury-feature-eyebrow'})
 eyebrow.string='ANTEPRIMA DEL LABORATORIO INTERATTIVO'
 block.append(eyebrow)
 title=doc.new_tag('h2',attrs={'class':'ma-jury-feature-title','id':'ma-jury-preview-title'})
 title.string='La stanza dei giurati'
 block.append(title)
 description=doc.new_tag('p',attrs={'class':'ma-jury-feature-description'})
 description.string='Tre stanze. Tre scelte. Una domanda: sai distinguere una risposta convincente da una prova?'
 block.append(description)
 meta=doc.new_tag('p',attrs={'class':'ma-jury-feature-meta'})
 meta.string='Scenari fittizi · Nessuna IA collegata · Disponibile in italiano'
 block.append(meta)
 content.append(block)
 action=doc.new_tag('a',attrs={'class':'ma-jury-feature-action','href':ROUTE})
 action.string='Entra nell’esperimento ↗'
 content.append(action)
 feature.append(content)
 hero.append(feature)

 if len(doc.select('section[data-ma-v2-section]'))!=before_sections or len(doc.select('[data-ma-v2-card]'))!=before_cards:
  raise RuntimeError('Home structure changed during Hero preview')
 css=site/'assets'/'jury-home-preview.css'
 css.parent.mkdir(parents=True,exist_ok=True)
 css.write_text(HOME_CSS,encoding='utf-8')
 doc.head.append(doc.new_tag('link',href=BASE+'assets/jury-home-preview.css',rel='stylesheet'))
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
  h=BeautifulSoup((site/'it/index.html').read_text(encoding='utf-8'),'html.parser')
  hero=h.select_one('section[data-ma-v2-section="hero"]')
  promo=hero.select('[data-ma-jury-home-preview="v3"]') if hero else []
  if len(promo)!=1 or len(hero.select('[data-ma-jury-top-badge="v3"]'))!=1:
   raise RuntimeError('Cinematic Hero experiment preview missing or duplicated')
  if len(h.select('section[data-ma-v2-section]'))!=5 or len(h.select('[data-ma-v2-card]'))!=6:
   raise RuntimeError('Home section/card count changed in Hero preview')
  if promo[0].select_one('a.ma-jury-feature-action')['href']!=ROUTE:
   raise RuntimeError('Cinematic Hero preview CTA destination incorrect')
  if not (site/'assets/jury-home-preview.css').is_file():
   raise RuntimeError('Missing cinematic Hero preview CSS')
  if not (asset_out/'palazzo-stendardi-manzo.webp').is_file():
   raise RuntimeError('Approved jury art missing from staging assets')

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
