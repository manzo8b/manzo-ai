#!/usr/bin/env python3
"""MANZO AI Precision & Motion visual and interaction smoke tests.

Uses browser rendering, three widths, three locales and all product surfaces.
Captures production-built screenshot evidence, not a mockup.
This is not a human visual review or a full WCAG/axe audit.
"""
from __future__ import annotations
from pathlib import Path
import base64
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

BASE='http://127.0.0.1:8765/manzo-ai/'
SCREENS={
 'portal':('', 'portal'),
 'it-home':('it/','landing'),
 'en-home':('en/','landing'),
 'es-home':('es/','landing'),
 'it-learning':('it/academy/','learning'),
 'it-course':('it/impara/allucinazioni-ai-verificabilita/','learning'),
 'it-research':('it/ricerca/acr/','research'),
 'it-product':('it/prodotto/','product'),
 'it-console':('it/prodotto/learning-b2b/','console'),
 'en-product':('en/product/','product'),
 'es-console':('es/producto/learning-b2b/','console'),
}
WIDTHS=(1440,768,390)
DEST=Path('design-review-screenshots')
DEST.mkdir(parents=True,exist_ok=True)

def test(page,route,expected_kind,screen,width):
 errors=[]
 page.on('pageerror',lambda exc:errors.append(str(exc)))
 page.goto(urljoin(BASE,route),wait_until='load',timeout=40000)
 actual=page.locator('body').get_attribute('data-ma-surface')
 assert actual==expected_kind,(screen,width,'kind',actual)
 assert page.locator('link[data-manzo-design="precision-motion-v1"]').count()==1
 assert page.locator('script[src*="design-motion.js"]').count()==1
 assert page.locator('h1').count()>=1,(screen,'missing h1')
 body_color=page.evaluate('getComputedStyle(document.body).backgroundColor')
 assert body_color=='rgb(255, 255, 255)',(screen,width,'paper',body_color)
 ink=page.evaluate("getComputedStyle(document.body).getPropertyValue('--ma-ink').trim()")
 assert ink=='#172e44',(screen,width,'ink',ink)
 if expected_kind=='landing':
  assert page.locator('[data-ma-home-scene="1"]').count()==1
  assert page.locator('.ma-product-scene a[href*="/prodotto/"],.ma-product-scene a[href*="/product/"],.ma-product-scene a[href*="/producto/"]').count()==1
 if screen.endswith('product'):
  assert page.locator('.product-card').count()==3
  assert page.locator('.btn-primary').first.is_enabled()
 if width==390 and expected_kind in ('product','console'):
  assert page.locator('.manzo-mobile-bar').count()==0,(screen,'duplicate global nav')
  assert page.locator('header').first.is_visible(),(screen,'own header missing')
 if screen.endswith('console'):
  assert page.locator('#lc-metric-0').inner_text()=='2 / 3'
  assert page.locator('#lc-tab-student').is_enabled()
 if width==390 and expected_kind in ('landing','product','console'):
  overflow=page.evaluate('document.documentElement.scrollWidth-window.innerWidth')
  assert overflow<=4,(screen,'mobile overflow',overflow)
 if errors:
  raise AssertionError((screen,width,'browser errors',errors))
 # Allow non-blocking reveal to settle before a full-page capture.
 page.wait_for_timeout(2100)
 page.screenshot(path=str(DEST/f'{screen}-{width}.png'),full_page=True,animations='disabled')
 # Small first-viewport previews can be inspected from the CI job log.
 # Full-page captures remain in the 7-day GitHub Actions artifact.
 if (screen,width) in {
    ('it-home',1440),('it-home',390),('it-product',1440),('it-console',390),('it-research',768)
 }:
  raw=page.screenshot(type='jpeg',quality=45,full_page=False,animations='disabled')
  print('MA_VISUAL_JPEG|'+screen+'|'+str(width)+'|'+base64.b64encode(raw).decode('ascii'),flush=True)
 print(f'PASS DESIGN {screen} {width}px: {actual}; paper {body_color}; h1 OK; screenshot captured.')

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,args=['--no-sandbox'])
 for name,(route,kind) in SCREENS.items():
  for width in WIDTHS:
   page=browser.new_page(
    viewport={'width':width,'height':900 if width>390 else 844},
    device_scale_factor=1,
    is_mobile=width==390,
    reduced_motion='reduce' if width==390 else 'no-preference',
   )
   test(page,route,kind,name,width)
   page.close()
 # Reduced motion should never hide content.
 page=browser.new_page(viewport={'width':390,'height':844},reduced_motion='reduce',is_mobile=True)
 page.goto(urljoin(BASE,'it/prodotto/'),wait_until='load')
 assert page.locator('body').evaluate("(el)=>getComputedStyle(el).getPropertyValue('--ma-paper').trim()")=='#ffffff'
 assert page.locator('.product-card').first.is_visible()
 # Functional smoke tests of underlying site still run separately.
 browser.close()
print('PASS DESIGN SYSTEM: 11 real surfaces x 3 widths, plus reduced-motion visibility.')
