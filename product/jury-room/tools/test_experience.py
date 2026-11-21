from pathlib import Path
import json, re, base64
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT.parent/'qa-previews'
DEST.mkdir(parents=True,exist_ok=True)
STYLES=(ROOT/'assets/styles.css').read_text()
APP=(ROOT/'assets/app.js').read_text()
EVAL=(ROOT/'assets/experiment-data.js').read_text()
def render(page,name,enable_js=True):
 d=BeautifulSoup((ROOT/name).read_text(),'html.parser')
 for tag in list(d.select('script[src],link[rel=stylesheet]')):tag.decompose()
 for tag in d.select('img'):
  url=tag.get('src','')
  if url.startswith('assets/'):
   tag['src']='data:image/webp;base64,'+base64.b64encode((ROOT/url).read_bytes()).decode()
 page.set_content(str(d),wait_until='domcontentloaded')
 page.add_style_tag(content=STYLES)
 if enable_js:
  page.add_script_tag(content=EVAL)
  page.add_script_tag(content=APP)

for html in ['index.html','banco-di-prova.html']:
 d=BeautifulSoup((ROOT/html).read_text(),'html.parser')
 assert len(d.select('h1'))==1
 assert d.select_one('meta[name="robots"]')['content']=='noindex,nofollow'
 assert not d.select('script[src^="http"],link[href^="http"]')
assert not re.search(r'non generata dall[\'’]AI|Ogni luce ha un significato|EXPERIMENTAL LAB|Progetto Esperimenti, §', ' '.join([p.read_text() for p in [ROOT/'index.html',ROOT/'banco-di-prova.html',ROOT/'assets/app.js']]),flags=re.I)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=__import__('shutil').which('chromium') or __import__('shutil').which('google-chrome') or None,args=['--no-sandbox','--disable-dev-shm-usage'])
 for width in [375,390,768,1440]:
  context=browser.new_context(viewport={'width':width,'height':870},device_scale_factor=1)
  page=context.new_page();page.set_default_timeout(5000);errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  render(page,'index.html')
  page.locator('.palace-accessible-title').wait_for(state='visible')
  assert page.locator('.palace-click-target').count()==0
  assert page.locator('.room-card').count()==3
  assert page.locator('video').count()==1
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 3'),('portal overflow',width,page.evaluate('document.documentElement.scrollWidth'),page.evaluate('innerWidth'))
  page.screenshot(path=str(DEST/f'palazzo-{width}.png'),full_page=width==1440)
  render(page,'banco-di-prova.html')
  assert page.locator('.learning-step').count()==6
  assert page.locator('#source-document').inner_text().startswith('PREVENTIVO N. 2026/047')
  assert page.locator('.claim-card').count()==8
  assert page.locator('#network-description').inner_text().startswith('0 relazioni dichiarate')
  assert page.locator('#models-summary').inner_text()==''
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 3'),('banco overflow',width,page.evaluate('document.documentElement.scrollWidth'),page.evaluate('innerWidth'))
  page.screenshot(path=str(DEST/f'banco-{width}.png'),full_page=width==1440)
  # No-JS fallback is verified from complete static HTML (no scripts required).
  if width==375:
   raw=BeautifulSoup((ROOT/'banco-di-prova.html').read_text(),'html.parser')
   assert len(raw.select_one('#source-document').get_text())>600
   assert raw.select_one('#prompt-a').get_text().startswith('Riassumi questo preventivo')
   assert raw.select_one('#prompt-b').get_text().startswith('Riassumi questo preventivo')
   assert len(raw.select('#answer-list .answer-row'))==8
   assert 'Per selezionare, confrontare e registrare' in raw.select_one('noscript').get_text()
  if width==1440:
   page.locator('a[href="#lacune"].stage-nav-link').click()
   for target in ['L1','L2','L3','L4','L5','L6','L7','L8']:
    page.locator(f'#gap-options input[value="{target}"]').check()
   page.locator('#reveal-evaluation').click()
   assert '8 lacune' in page.locator('#evaluation-feedback').inner_text()
   page.locator('a[href="#riassunto"].stage-nav-link').click()
   expect={ 'R1':('supported','Lavori compresi'),'R2':('supported','Importo'), 'R3':('unsupported',''), 'R4':('supported','Tempi'), 'R5':('unsupported',''), 'R6':('partial','Pagamento'), 'R7':('unsupported',''),'R8':('supported','Validità') }
   for k,(status,source) in expect.items():
    page.locator(f'[data-claim="{k}"] input[value="{status}"]').check()
    if source:page.locator(f'[data-claim="{k}"] select').select_option(source)
   assert '8 / 8 relazioni' in page.locator('#network-counter').inner_text()
   assert page.locator('#evidence-network .net-connection').count()==8
   page.locator('.network-evidence-shell').screenshot(path=str(DEST/'rete-reale-1440.png'))
   page.locator('#freeze-claims').click()
   assert page.locator('#decision-review').is_visible()
   assert 'Nessuna risposta modificata' in page.locator('#changed-count').inner_text()
   page.locator('[data-claim="R3"] input[value="supported"]').check()
   page.locator('[data-claim="R3"] select').select_option('Importo')
   assert '1 risposta modificata' in page.locator('#changed-count').inner_text()
   page.locator('#decision-review').screenshot(path=str(DEST/'prima-dopo-1440.png'))
   assert 'Supportata · Importo' in page.locator('#decision-rows tr:nth-child(3)').inner_text()
   page.locator('#change-reason').fill('Ho letto la voce Importo: l’aliquota non compare')
   # Part 2, two models (case and whitespace normalization), result must stay separated
   page.locator('a[href="#registro"].stage-nav-link').click()
   for model in ['Demo Uno','demo  uno','Altro Modello']:
    prompt='A' if model=='Demo Uno' else ('B' if model=='demo  uno' else 'A')
    page.locator('input[name="model"]').fill(model)
    page.locator('input[name="version"]').fill('v-test')
    page.locator('input[name="date"]').fill('2026-11-20')
    page.locator('select[name="prompt"]').select_option(prompt)
    page.locator('input[name="found-gap"][value="L1"]').check()
    page.locator('input[name="found-gap"][value="L2"]').check()
    for metric in ['inventions','omissions','generalisations','inferences','falseAlarms']:
     page.locator(f'input[name="{metric}"]').fill('0')
    page.locator('#trial-form button[type="submit"]').click()
   assert page.locator('#models-summary .model-summary').count()==2
   assert page.locator('#run-history .run-row').count()==3
   assert '3 prove' in page.locator('#run-progress').inner_text()
   page.locator('a[href="#verdetto"].stage-nav-link').click()
   page.locator('#corrective-rule').fill('Quando manca una cifra, allora chiedo la fonte prima di usarla')
   # copy may be blocked in headless; enforce content through static generator/runtime test separately
   assert not re.search(r'(?:localStorage|sessionStorage)\s*\.|document\.cookie\s*=|fetch\s*\(|XMLHttpRequest\s*\(', APP)
  assert not errors,(width,errors)
  print('PASS',width,'portal + banco responsive',flush=True)
  context.close()
 browser.close()

print('PASS HTML + JS-off + logic + responsive + source',flush=True)
