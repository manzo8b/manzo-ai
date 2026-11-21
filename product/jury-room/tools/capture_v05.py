from pathlib import Path
from bs4 import BeautifulSoup as BS
from playwright.sync_api import sync_playwright
import base64, shutil
ROOT=Path(__file__).resolve().parents[1]
CSS=(ROOT/'assets/styles.css').read_text()+'\n'+(ROOT/'assets/rooms.css').read_text()
def load(page,fn):
 d=BS((ROOT/fn).read_text(),'html.parser')
 for tag in list(d.select('script[src],link[rel=stylesheet]')):tag.decompose()
 for im in d.select('img[src^="assets/"]'):
  fn2=ROOT/im['src'];mime='image/webp' if fn2.suffix=='.webp' else 'image/svg+xml'
  im['src']='data:'+mime+';base64,'+base64.b64encode(fn2.read_bytes()).decode()
 page.set_content(str(d));page.add_style_tag(content=CSS)
 if fn=='banco-di-prova.html':page.add_script_tag(content=(ROOT/'assets/experiment-data.js').read_text())
 page.add_script_tag(content=(ROOT/'assets/app.js' if fn=='banco-di-prova.html' else ROOT/'assets/room-practices.js').read_text())
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path=shutil.which('chromium'),args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1200,'height':900},device_scale_factor=1,reduced_motion='reduce')
 page=context.new_page()
 load(page,'officina-locale.html');page.locator('[data-sim-product="pane"]').fill('2');page.locator('[data-sim-product="focaccia"]').fill('1');page.locator('#sim-days').select_option('1');page.locator('#sim-weekday').select_option('mar')
 page.locator('#regole-fisse').screenshot(path=str(ROOT/'QA/v05-simulatore-1200.png'))
 load(page,'sala-dei-confini.html');page.locator('[data-action="A3"] [data-autonomy]').select_option('autonomo');page.locator('#show-autonomy-map').click();page.locator('[data-incident="2"] [data-incident-action]').select_option('A3');page.locator('[data-incident="2"] [data-incident-level]').select_option('umano');page.locator('#show-final-map').click()
 page.locator('#final-autonomy-map').screenshot(path=str(ROOT/'QA/v05-sala-prima-dopo-1200.png'))
 load(page,'banco-di-prova.html');page.locator('a[href="#lacune"].stage-nav-link').click();page.locator('#reveal-evaluation').click();page.locator('a[href="#registro"].stage-nav-link').click()
 page.locator('#record-gap-unlocked').screenshot(path=str(ROOT/'QA/v05-banco-chiave-sbloccata-1200.png'))
 context.close();browser.close()
print('PASS: 3 visual snapshots captured from interactive state')
