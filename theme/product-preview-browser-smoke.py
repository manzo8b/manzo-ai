#!/usr/bin/env python3
"""Functional and responsive QA of nontransactional MANZO AI Product Lab."""
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin

BASE='http://127.0.0.1:8765/manzo-ai/'
ROUTES={'it':'it/prodotto/','en':'en/product/','es':'es/producto/'}
def test_locale(page,locale,mobile=False):
 page.goto(urljoin(BASE,ROUTES[locale]),wait_until='load',timeout=35000)
 assert page.locator('html').get_attribute('lang')==locale
 assert page.locator('meta[name=robots]').get_attribute('content')=='noindex,follow'
 assert page.locator('h1').count()==1
 assert page.locator('.product-card').count()==3
 assert page.locator('.readiness-item').count()==6
 assert page.locator('link[rel=alternate][hreflang=it]').count()==1
 assert page.locator('#project-export').is_enabled()
 page.locator('#project-goal').fill('A multilingual business website for enterprise customers')
 page.locator('#project-audience').fill('Operations teams and technology buyers')
 page.locator('#project-update').click()
 assert 'A multilingual business website' in page.locator('#brief-json').inner_text()
 with page.expect_download() as d:
  page.locator('#project-export').click()
 assert d.value.suggested_filename=='manzo-ai-project-brief.json'
 assert page.locator('#claim-list .claim').count()==0
 page.locator('#inspect-input').fill('Revenue grew by 28% in 2025. All companies must use this AI. The package is fully compliant.')
 page.locator('#inspect-text').click()
 assert page.locator('#claim-list .claim').count()>=1
 assert '28%' in page.locator('#claim-list').inner_text()
 # Text is inserted only via textContent; no user HTML execution.
 page.locator('#inspect-input').fill('<img src=x onerror="window.__unsafe=true"> The law requires all firms to do this.')
 page.locator('#inspect-text').click()
 assert page.evaluate('window.__unsafe') is None
 page.locator('#team-seats').evaluate("(el) => {el.value='45';el.dispatchEvent(new Event('input',{bubbles:true}));}")
 assert page.locator('#team-seats-label').inner_text()=='45'
 assert '45' in page.locator('#team-summary').inner_text()
 assert page.locator('input[type=password]').count()==0
 # Non transactional: no checkout link, no credential collection, no persistent storage.
 assert page.locator('form[action]').count()==0
 assert page.evaluate('localStorage.length')==0
 width=page.evaluate('document.documentElement.scrollWidth')
 vp=page.evaluate('window.innerWidth')
 assert width<=vp+2, f'{locale} mobile={mobile} overflow {width}>{vp}'
 assert page.locator('#studio').is_visible()
 assert page.locator('#verify').is_visible()
 assert page.locator('#learning').is_visible()

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,args=['--no-sandbox'])
 for loc in ROUTES:
  for mobile in (False,True):
   page=browser.new_page(viewport={'width':390 if mobile else 1366,'height':844},accept_downloads=True,is_mobile=mobile)
   test_locale(page,loc,mobile)
   page.goto(urljoin(BASE,loc+'/'),wait_until='load')
   assert page.locator('[data-manzo-product-preview]').count()==1
   page.close()
 browser.close()
print('PASS Product Lab: 3 locales, 2 viewports, functional brief JSON download, claim analysis, team configurator, XSS and no-storage checks.')
