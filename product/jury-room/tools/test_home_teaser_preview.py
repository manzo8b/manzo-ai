#!/usr/bin/env python3
"""Isolated, never-deployed Home novelty badge smoke tests (IT Home v2 only)."""
from __future__ import annotations
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

mock='''<!DOCTYPE html><html lang="it"><head><meta charset="utf-8">
<title>Home MANZO AI preview</title></head><body data-ma-surface="landing">
<header id="nav">MANZO AI</header><main id="content">
<section data-ma-v2-section="hero"><h1>Chiedi, controlla, decidi</h1></section>
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
assert ratio('#135c64','#e4f5f4')>=4.5
assert ratio('#ffffff','#164f78')>=4.5

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
 teaser=result.select('aside[data-ma-jury-home-preview="v2"]')
 assert len(teaser)==1
 assert teaser[0].select_one('.ma-jury-preview-badge').get_text(strip=True)=='Nuovo esperimento'
 assert teaser[0].select_one('.ma-jury-preview-title').get_text(strip=True)=='La stanza dei giurati'
 assert teaser[0].select_one('.ma-jury-preview-note').get_text(strip=True).endswith('In italiano')
 assert teaser[0].select_one('a.ma-jury-preview-action')['href']==route
 assert result.select_one('section[data-ma-v2-section="challenge"] > a')['href']=='/manzo-ai/it/sfida/'
 assert not result.select('[data-ma-jury-home-preview] + [data-ma-jury-home-preview]')
 assert (site/'assets/jury-home-preview.css').is_file()
 try:
  insert(site)
 except RuntimeError as err:
  assert 'already injected' in str(err)
 else:raise AssertionError('Duplicate injection should fail')
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
  for width in (375,768,1440):
   page=browser.new_page(viewport={'width':width,'height':900},reduced_motion='reduce')
   page.set_content(home.read_text(encoding='utf-8'),wait_until='domcontentloaded')
   page.add_style_tag(content=main_css)
   page.add_style_tag(content=(site/'assets/jury-home-preview.css').read_text(encoding='utf-8'))
   badge=page.locator('.ma-jury-preview-badge')
   assert badge.is_visible(),f'Badge hidden at {width}px'
   assert page.locator('.ma-jury-preview-action').is_visible()
   assert page.locator('.ma-jury-preview-action').get_attribute('href')==route
   assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 2'),f'Horizontal overflow at {width}px'
   assert page.locator('[data-ma-v2-card]').count()==6
   assert page.locator('section[data-ma-v2-section]').count()==5
   page.locator('.ma-jury-preview-action').focus()
   assert page.evaluate("document.activeElement.classList.contains('ma-jury-preview-action')")
   page.close()
  browser.close()
print('PASS Home novelty teaser: 5 sections, 6 cards, Italian-only link, contrast, keyboard, 375/768/1440')
