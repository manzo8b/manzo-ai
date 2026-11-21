#!/usr/bin/env python3
"""End-to-end acceptance checks for correction brief #2 (non-public prototype)."""
from pathlib import Path
from bs4 import BeautifulSoup as BS
from playwright.sync_api import sync_playwright
import shutil, re, mistune, base64
ROOT=Path(__file__).resolve().parents[1]
md=mistune.create_markdown(plugins=['table','strikethrough','task_lists'])
for page,source in [('officina-locale.html','MANZO_AI_Esperimento_03_Officina.md'),('sala-dei-confini.html','MANZO_AI_Esperimento_02_Governo.md')]:
 src=(ROOT/'sources'/source).read_text(encoding='utf-8')
 d=BS((ROOT/page).read_text(encoding='utf-8'),'html.parser')
 r=BS(md(src),'html.parser')
 for h in r.find_all(re.compile('^h[1-5]$')):h.name='h'+str(min(int(h.name[1])+1,6))
 actual=d.select_one('.room-source-body')
 norm=lambda s:re.sub(r'\s+',' ',str(s)).strip()
 assert norm(actual.decode_contents())==norm(str(r)),(page,'document source differs from regenerated Markdown')
 assert len(d.select('h1'))==1
 assert d.select_one('.room-dossier-hero>img').get('fetchpriority')=='high'
 assert d.select_one('.room-dossier-hero>img').get('loading')!='lazy'
 assert 'Senza JavaScript' in d.select_one('noscript').get_text()
for page in ['index.html','banco-di-prova.html','officina-locale.html','sala-dei-confini.html']:
 d=BS((ROOT/page).read_text(encoding='utf-8'),'html.parser')
 assert d.select_one('meta[name=robots]')['content']=='noindex,nofollow'
 assert len(d.select('h1'))==1
 assert not re.search(r'\bapprovato\b',d.get_text(' ',strip=True),flags=re.I),(page,'unearned approval')
 assert not d.select('script[src^="http"],link[href^="http"]')
for img in ['palazzo-stendardi-manzo.webp','hero-palazzo-futuristico.webp']:
 assert (ROOT/'assets'/img).stat().st_size<250000,(img,'hero weight')
assert not re.search(r'\bfetch\s*\(|XMLHttpRequest|localStorage|sessionStorage|sendBeacon',((ROOT/'assets/app.js').read_text()+(ROOT/'assets/room-practices.js').read_text()))
print('PASS: source fidelity, noindex, no external scripts, metadata, static documents, hero sizes')

def render(page,filename,js=True):
 d=BS((ROOT/filename).read_text(encoding='utf-8'),'html.parser')
 for tag in list(d.select('script[src],link[rel="stylesheet"]')):tag.decompose()
 for img in d.select('img[src^="assets/"]'):
  source=ROOT/img['src'];mime='image/svg+xml' if source.suffix=='.svg' else 'image/webp'
  img['src']='data:'+mime+';base64,'+base64.b64encode(source.read_bytes()).decode()
 style=(ROOT/'assets/styles.css').read_text()+'\n'+(ROOT/'assets/rooms.css').read_text()
 if not js:
  inline=d.new_tag('style');inline.string=style;d.head.append(inline)
 page.set_content(str(d),wait_until='domcontentloaded')
 if js:page.add_style_tag(content=style)
 if js:
  if filename=='banco-di-prova.html':page.add_script_tag(content=(ROOT/'assets/experiment-data.js').read_text())
  if filename in ['banco-di-prova.html','index.html']:page.add_script_tag(content=(ROOT/'assets/app.js').read_text())
  else:page.add_script_tag(content=(ROOT/'assets/room-practices.js').read_text())

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path=shutil.which('chromium'),args=['--no-sandbox','--disable-dev-shm-usage'])
 for w in (375,768,1440):
  context=browser.new_context(viewport={'width':w,'height':900},reduced_motion='reduce')
  page=context.new_page(); page.set_default_timeout(9000)
  errors=[];requests=[]
  page.on('pageerror',lambda err:errors.append(str(err)))
  page.on('request',lambda req:requests.append(req.url) if req.url.startswith(('http://','https://')) else None)
  def go(name):
   render(page,name)
   assert page.locator('h1').is_visible(),(name,w,'h1 hidden')
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+3'),(name,w,'overflow')
  go('index.html')
  assert page.locator('.room-status').all_inner_texts()==['Anteprima interattiva']*3
  assert page.locator('#room-dialog').count()==0
  go('banco-di-prova.html')
  page.locator('a[href="#registro"].stage-nav-link').click()
  assert page.locator('#record-gap-locked').is_visible()
  assert not page.locator('#record-gap-unlocked').is_visible()
  assert 'Aliquota IVA non indicata' not in page.locator('#trial-form').inner_text()
  page.locator('a[href="#lacune"].stage-nav-link').click()
  assert page.locator('#gap-options .gap-id').all_inner_texts()==[str(i) for i in range(1,10)]
  page.locator('#reveal-evaluation').click()
  assert 'Falso allarme' in page.locator('#gap-options').inner_text()
  page.locator('a[href="#registro"].stage-nav-link').click()
  assert page.locator('#record-gap-unlocked').is_visible()
  page.locator('a[href="#verdetto"].stage-nav-link').click()
  page.on('dialog',lambda d:d.accept())
  page.locator('#reset-all').click()
  page.locator('a[href="#registro"].stage-nav-link').click()
  assert page.locator('#record-gap-locked').is_visible()
  assert not page.locator('#record-gap-unlocked').is_visible()
  page.locator('#skip-diagnosis').click()
  assert page.locator('#record-gap-unlocked').is_visible()
  go('officina-locale.html')
  assert page.locator('[data-run="v1"]').count()==18
  assert page.locator('[data-run="v2"]').count()==18
  pane=page.locator('[data-sim-product="pane"]');foc=page.locator('[data-sim-product="focaccia"]');cake=page.locator('[data-sim-product="torta"]')
  pane.fill('2');foc.fill('1')
  assert '23,00' in page.locator('#sim-results').inner_text()
  page.locator('#sim-days').select_option('1')
  page.locator('#sim-weekday').select_option('lun')
  assert 'Regola 2 · Ritiro tra le 7:30 e le 13:00, escluso lunedì: Non rispettata' in page.locator('#sim-results').inner_text()
  cake.fill('1')
  assert 'Regola 3 · Torte con due giorni di calendario: Non rispettata' in page.locator('#sim-results').inner_text()
  page.locator('[data-test="T6"] [data-run="v1"][data-repetition="1"]').select_option('fail')
  assert 'Almeno un errore registrato' in page.locator('#trial-summary').inner_text()
  assert '1 / 18 prove registrate per v1' in page.locator('#trial-summary').inner_text()
  for sel in page.locator('[data-run]').all():sel.select_option('ok')
  assert '18 / 18 prove registrate per v1' in page.locator('#trial-summary').inner_text()
  assert '18 / 18 prove registrate per v2' in page.locator('#trial-summary').inner_text()
  go('sala-dei-confini.html')
  page.locator('[data-action="A1"] [data-autonomy]').select_option('conferma')
  page.locator('[data-action="A3"] [data-autonomy]').select_option('autonomo')
  page.locator('#show-autonomy-map').click()
  assert 'Manca chi decide' in page.locator('#autonomy-map').inner_text()
  assert 'effetto esterno' in page.locator('#autonomy-map').inner_text()
  page.locator('[data-incident="2"] [data-incident-action]').select_option('A3')
  page.locator('[data-incident="2"] [data-incident-level]').select_option('umano')
  page.locator('#show-final-map').click()
  assert '1 azione modificata' in page.locator('#final-autonomy-map').inner_text()
  before_after=page.locator('.room-before-after tr').filter(has=page.locator('th:text-is("A3")')).inner_text()
  assert 'Autonomo' in before_after and 'Solo umano' in before_after and 'Sì · Cambiato' in before_after
  page.locator('#change-confini').fill('Ho visto il rischio di invio esterno')
  assert not errors,(w,'console errors',errors)
  assert not requests,(w,'network requests',requests)
  print(f'PASS: width={w} no spoiler, reset, deterministic rule tests, 18×2, before/after, privacy, no overflow')
  context.close()
 for w in (375,768,1440):
  ctx=browser.new_context(viewport={'width':w,'height':850},java_script_enabled=False,reduced_motion='reduce')
  page=ctx.new_page()
  for filename in ('banco-di-prova.html','officina-locale.html','sala-dei-confini.html'):
   render(page,filename,False)
   assert page.locator('noscript').is_visible()
   if filename.startswith('officina'):
    assert page.locator('.room-case-dossier').inner_text()
    assert page.locator('.room-source-file').count()==1
   if filename.startswith('sala'):
    assert page.locator('[data-incident]').count()==4
    assert page.locator('tr[data-action]').count()==12
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+3'),(filename,w,'no JS overflow')
  ctx.close()
  print(f'PASS: width={w} document fallback without JavaScript')
 browser.close()
print('PASS brief #2 acceptance suite')
