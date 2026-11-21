#!/usr/bin/env python3
"""Staging-only test: cinematic, full-width jury-room showcase in Home IT Hero."""
from __future__ import annotations
import base64
import runpy
from pathlib import Path
from tempfile import TemporaryDirectory
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[3]
mod=runpy.run_path(str(ROOT/'product/jury-room/tools/build_for_manzo_ai.py'))
insert=mod['insert_home_preview']
route=mod['ROUTE']
main_css=(ROOT/'theme/home-magic-v2.css').read_text(encoding='utf-8')
original_image=ROOT/'product/jury-room/assets/palazzo-stendardi-manzo.webp'
assert original_image.is_file(), 'Approved palace artwork required'

mock='''<!DOCTYPE html><html lang="it"><head><meta charset="utf-8">
<title>Home MANZO AI preview</title></head><body data-ma-surface="landing">
<header id="nav">MANZO AI</header><main id="content">
<section data-ma-v2-section="hero" class="ma-v2-hero" aria-labelledby="ma-v2-heading">
<div class="ma-v2-hero-copy"><p class="ma-v2-kicker">MANZO AI / IMPARA A PENSARE</p>
<h1 id="ma-v2-heading">Chiedi meglio. Controlla sempre. Decidi tu</h1>
<p class="ma-v2-lead">Dalla domanda alla prova.</p>
<div class="ma-v2-actions"><a class="ma-v2-primary" href="/manzo-ai/it/academy/">Inizia dalle basi</a></div>
</div>
<figure class="ma-v2-magic"><div class="ma-v2-magic-stage">La scatola magica</div></figure>
</section>
<section data-ma-v2-section="courses" class="ma-v2-courses">
''' + ''.join(f'<article data-ma-v2-card="{n}">Corso {n}</article>' for n in range(1,7)) + '''
</section><section data-ma-v2-section="audiences"></section>
<section data-ma-v2-section="challenge" class="ma-v2-challenge"
aria-labelledby="ma-v2-challenge-title">
<div><span class="ma-v2-section-id">IL PENSIERO CRITICO SI ALLENA</span>
<h2 id="ma-v2-challenge-title">Sai distinguere un’intuizione da una prova?</h2>
<p>Metti alla prova le tue certezze</p></div>
<a href="/manzo-ai/it/sfida/">Accetta la sfida</a>
</section><section data-ma-v2-section="closing"></section>
</main><footer id="footer">MANZO AI</footer></body></html>'''

def ratio(a,b):
 def lum(rgb):
  r,g,bl=[int(rgb[i:i+2],16)/255 for i in (1,3,5)]
  v=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in (r,g,bl)]
  return sum(x*y for x,y in zip(v,(.2126,.7152,.0722)))
 la,lb=lum(a),lum(b)
 return (max(la,lb)+.05)/(min(la,lb)+.05)
assert ratio('#ffffff','#a7233b')>=4.5
assert ratio('#124366','#ffffff')>=4.5

with TemporaryDirectory() as tmp:
 site=Path(tmp); (site/'it').mkdir()
 home=site/'it/index.html'; home.write_text(mock,encoding='utf-8')
 original=BeautifulSoup(mock,'html.parser')
 insert(site)
 result=BeautifulSoup(home.read_text(encoding='utf-8'),'html.parser')
 assert result.select_one('#nav').decode_contents()==original.select_one('#nav').decode_contents()
 assert result.select_one('#footer').decode_contents()==original.select_one('#footer').decode_contents()
 assert len(result.select('section[data-ma-v2-section]'))==5
 assert len(result.select('article[data-ma-v2-card]'))==6
 assert len(result.select('h1'))==1
 assert result.select_one('section[data-ma-v2-section="challenge"] > a')['href']=='/manzo-ai/it/sfida/'
 assert len(result.select('section[data-ma-v2-section="hero"] [data-ma-jury-home-preview="v3"]'))==1
 assert not result.select('aside[data-ma-jury-home-preview]')
 assert result.select_one('.ma-jury-top-notice')['href']=='#ma-jury-hero-feature'
 assert result.select_one('.ma-jury-feature-title').get_text(strip=True)=='La stanza dei giurati'
 assert result.select_one('.ma-jury-feature-meta').get_text(strip=True).endswith('italiano')
 assert result.select_one('a.ma-jury-feature-action')['href']==route
 assert 'palazzo-stendardi-manzo.webp' in result.select_one('.ma-jury-feature-image')['src']
 assert result.select_one('.ma-jury-feature-image')['alt'].count('MANZO')==1
 assert (site/'assets/jury-home-preview.css').is_file()
 try:
  insert(site)
 except RuntimeError as err:
  assert 'already injected' in str(err)
 else:raise AssertionError('Repeated showcase insertion must fail')

 injected=home.read_text(encoding='utf-8')
 hero_data='data:image/webp;base64,'+base64.b64encode(original_image.read_bytes()).decode('ascii')
 doc=BeautifulSoup(injected,'html.parser')
 doc.select_one('.ma-jury-feature-image')['src']=hero_data
 screen_html=str(doc)
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
  for width in (375,768,1440):
   page=browser.new_page(viewport={'width':width,'height':900},reduced_motion='reduce')
   page.set_content(screen_html,wait_until='domcontentloaded')
   page.add_style_tag(content=main_css)
   page.add_style_tag(content=(site/'assets/jury-home-preview.css').read_text(encoding='utf-8'))
   assert page.locator('.ma-jury-top-notice').is_visible(),f'Top notification hidden at {width}px'
   assert page.locator('.ma-jury-hero-feature').is_visible(),f'Cinematic feature hidden at {width}px'
   assert page.locator('a.ma-jury-feature-action').is_visible(),f'CTA hidden at {width}px'
   assert page.locator('a.ma-jury-feature-action').get_attribute('href')==route
   assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 2'),f'Horizontal overflow at {width}px'
   assert page.locator('[data-ma-v2-card]').count()==6
   assert page.locator('section[data-ma-v2-section]').count()==5
   assert page.locator('h1').count()==1
   assert page.locator('.ma-jury-feature-image').evaluate('(el)=>el.complete && el.naturalWidth>0')
   feature=page.locator('.ma-jury-hero-feature').bounding_box()
   container=page.locator('section[data-ma-v2-section="hero"]').bounding_box()
   assert feature['width'] > .8 * container['width'],f'Feature must be full width at {width}px'
   page.locator('a.ma-jury-feature-action').focus()
   assert page.evaluate("document.activeElement.classList.contains('ma-jury-feature-action')")
   page.close()
  browser.close()
print('PASS cinematic Home Hero: full-width palace, intro badge, 5 sections/6 cards, contrast, focus, 375/768/1440')
