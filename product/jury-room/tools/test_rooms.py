from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import base64,re,shutil
ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'QA'; QA.mkdir(exist_ok=True)
css=(ROOT/'assets/styles.css').read_text()+'\n'+(ROOT/'assets/rooms.css').read_text()
js=(ROOT/'assets/room-practices.js').read_text()
# Script-only and source-HTML fallback assertions
for f in ['index.html','banco-di-prova.html','officina-locale.html','sala-dei-confini.html']:
 d=BeautifulSoup((ROOT/f).read_text(encoding='utf-8'),'html.parser')
 assert len(d.select('h1'))==1,(f,len(d.select('h1')))
 assert d.select_one('meta[name="robots"]')['content']=='noindex,nofollow'
 assert not d.select('script[src^="http"],link[href^="http"]')
 assert d.select_one('img[src="assets/palazzo-stendardi-manzo.webp"]'),f
 if f in ('officina-locale.html','sala-dei-confini.html'):
  assert d.select_one('.room-source-file .room-source-body')
  assert 'Non caricare dati reali o riservati' in d.get_text(' ',strip=True)
  assert 'Fonti normative da completare' in d.get_text(' ',strip=True) if f.startswith('sala') else True
  assert len(d.select('.room-source-body table'))>=3
assert not re.search(r'\bfetch\s*\(|XMLHttpRequest|localStorage|sessionStorage|document\.cookie|navigator\.sendBeacon',js)
assert len(BeautifulSoup((ROOT/'officina-locale.html').read_text(),'html.parser').select('[data-test]'))==6
assert len(BeautifulSoup((ROOT/'sala-dei-confini.html').read_text(),'html.parser').select('tr[data-action]'))==12

def render(page,name):
 d=BeautifulSoup((ROOT/name).read_text(),'html.parser')
 for tag in list(d.select('script[src],link[rel="stylesheet"]')):tag.decompose()
 for tag in d.select('img'):
  src=tag.get('src','')
  if src.startswith('assets/'):
   data=(ROOT/src).read_bytes()
   mime='image/webp' if src.endswith('.webp') else 'image/svg+xml'
   tag['src']='data:'+mime+';base64,'+base64.b64encode(data).decode()
 page.set_content(str(d),wait_until='domcontentloaded')
 page.add_style_tag(content=css)
 if name in ('officina-locale.html','sala-dei-confini.html'):page.add_script_tag(content=js)
 else:
  page.add_script_tag(content=(ROOT/'assets/experiment-data.js').read_text())
  page.add_script_tag(content=(ROOT/'assets/app.js').read_text())

with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=shutil.which('chromium') or None,args=['--no-sandbox','--disable-dev-shm-usage'])
 for width in (375,390,768,1440):
  context=browser.new_context(viewport={'width':width,'height':900},device_scale_factor=1)
  page=context.new_page();page.set_default_timeout(6500)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  for name in ['index.html','banco-di-prova.html','officina-locale.html','sala-dei-confini.html']:
   render(page,name)
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 3'),(name,width,page.evaluate('document.documentElement.scrollWidth'),page.evaluate('innerWidth'))
   assert page.locator('h1').is_visible(),(name,width,'heading hidden')
   assert page.locator('.topbar').is_visible(),(name,width,'nav hidden')
   if width in (375,1440) and name in ('index.html','officina-locale.html','sala-dei-confini.html'):
    page.screenshot(path=str(QA/f'{name.replace(".html","")}-{width}.png'),full_page=(width==1440))
   if name=='officina-locale.html':
    page.locator('[data-task="C1"] select').select_option('regole')
    page.locator('[data-task="C7"] select').select_option('persona')
    page.locator('#compare-diagnosis').click()
    assert page.locator('#diagnosis-comparison').is_visible()
    assert 'C1' in page.locator('#diagnosis-comparison').inner_text()
    page.locator('[data-skill="role"]').fill('Assistente forno — scenario fittizio')
    page.locator('#copy-skill').click()
    assert 'copiat' in page.locator('#announce').inner_text().lower() or 'copia non riuscita' in page.locator('#announce').inner_text().lower()
    page.locator('[data-test="T6"] [data-run="v1"][data-repetition="1"]').select_option('fail')
    assert 'T6' in page.locator('#trial-summary').inner_text()
    assert 'Almeno un errore registrato' in page.locator('#trial-summary').inner_text()
    page.locator('#copy-officina').click()
    page.locator('#reset-officina').click()
    assert page.locator('#diagnosis-progress').inner_text().startswith('0 di 8')
    assert page.locator('[data-test="T6"] [data-run="v1"][data-repetition="1"]').input_value()=='fail'
   if name=='sala-dei-confini.html':
    page.locator('[data-action="A1"] select').select_option('conferma')
    page.locator('[data-action="A1"] input').fill('Direttrice fittizia')
    page.locator('[data-action="A5"] select').select_option('umano')
    page.locator('#show-autonomy-map').click()
    assert page.locator('#autonomy-map').is_visible()
    assert '2 di 12' in page.locator('#autonomy-progress').inner_text()
    assert 'Manca chi decide' in page.locator('#autonomy-map').inner_text()
    page.locator('[data-incident="1"] textarea').fill('Bloccare e chiedere revisione')
    page.locator('#copy-confini').click()
    page.locator('#reset-confini').click()
    assert page.locator('#autonomy-progress').inner_text()=='0 di 12 azioni classificate'
    assert page.locator('[data-incident="1"] textarea').input_value()=='Bloccare e chiedere revisione'
  assert not errors,(width,errors)
  print('PASS',width,'index, banco, officina, confini, scripts, no overflow',flush=True)
  context.close()
 browser.close()
print('PASS: static markup, accessible content, privacy, core interactions',flush=True)
