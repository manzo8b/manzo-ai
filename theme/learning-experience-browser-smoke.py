#!/usr/bin/env python3
"""Browser regression: trilingual learning compass with existing original quizzes.

No simulated credentials, no storage, no fake certificate. Paths are from the
actual previously published courses, not invented course URLs.
"""
from __future__ import annotations
from urllib.parse import urljoin
from pathlib import Path
import base64
from playwright.sync_api import sync_playwright

BASE='http://127.0.0.1:8765/manzo-ai/'
ROUTES={
 'it':('it/impara/allucinazioni-ai-verificabilita/','it/impara/allucinazioni-ai-verificabilita/coding/'),
 'en':('en/learn/ai-hallucinations-verification/','en/learn/ai-hallucinations-verification/coding/'),
 'es':('es/aprende/alucinaciones-ia-verificacion/','es/aprende/alucinaciones-ia-verificacion/coding/'),
}
for_review=0
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,args=['--no-sandbox'])
 for locale,paths in ROUTES.items():
  for kind,route in zip(('core','coding'),paths):
   for width in (1440,390):
    page=browser.new_page(
      viewport={'width':width,'height':844 if width==390 else 900},
      is_mobile=(width==390),
      reduced_motion='reduce' if width==390 else 'no-preference'
    )
    errors=[]
    page.on('pageerror',lambda exception:errors.append(str(exception)))
    page.goto(urljoin(BASE,route),wait_until='load',timeout=40000)
    root=page.locator('[data-ma-learning-guide="v1"]')
    assert root.count()==1,(locale,kind,'missing guide')
    assert root.get_attribute('data-ma-guide-kind')==kind
    assert page.locator('[data-ma-unit]').count()==6
    assert page.locator('[data-ma-mark]').count()==6
    assert page.locator('#ma-progress-current').inner_text()=='0'
    assert page.locator('.ma-progress-track').get_attribute('aria-valuenow')=='0'
    assert page.locator('link[data-ma-learning-assets]').count()==1
    assert page.locator('script[src*="learning-experience/guide.js"]').count()==1
    assert page.locator('html').get_attribute('lang')==locale
    first=page.locator('[data-ma-mark="1"]')
    first.click()
    assert first.get_attribute('aria-pressed')=='true'
    assert page.locator('#ma-progress-current').inner_text()=='1'
    assert page.locator('#ma-continue').get_attribute('href')==('#hc-section-02' if kind=='coding' else '#ma-learn-unit-2')
    for i in (2,3,4,5,6):
     page.locator(f'[data-ma-mark="{i}"]').click()
    assert page.locator('#ma-progress-current').inner_text()=='6'
    assert page.locator('.ma-progress-track').get_attribute('aria-valuenow')=='6'
    assert page.locator('#ma-continue').get_attribute('href') is None
    page.locator('#ma-reset').click()
    assert page.locator('#ma-progress-current').inner_text()=='0'
    assert first.get_attribute('aria-pressed')=='false'
    # Existing exercises and quiz rendering must not be altered.
    if kind=='core':
     assert page.locator('.hx-module').count()==6
     assert page.locator('.hx-case').count()==10
     assert page.locator('#hx-quiz-data').count()==1
     assert page.locator('#hx-quiz-check').is_enabled()
     assert page.locator('#hx-cross-grid').count()==1
    else:
     assert page.locator('.hc-section').count()==6
     assert page.locator('[data-hc-case]').count()==4
     assert page.locator('#hc-quiz-data').count()==1
     assert page.locator('[data-hc-submit]').is_enabled()
    if width==390:
     number=page.locator('.ma-guide-key>strong').bounding_box()
     explanation=page.locator('.ma-guide-key>small').bounding_box()
     assert number and explanation and number['x']+number['width']<=explanation['x']+2,(locale,kind,'module label overlap',number,explanation)
    assert page.evaluate('localStorage.length')==0
    assert page.evaluate('sessionStorage.length')==0
    if width==390:
     overflow=page.evaluate('document.documentElement.scrollWidth-window.innerWidth')
     assert overflow<=4,(locale,kind,'horizontal overflow',overflow)
    assert not errors,(locale,kind,errors)
    if locale=='it' and kind=='core':
     folder=Path('design-review-screenshots')
     folder.mkdir(exist_ok=True)
     page.locator('.ma-guide-head').scroll_into_view_if_needed()
     page.evaluate("window.scrollBy(0,-70)")
     page.wait_for_timeout(80)
     page.screenshot(path=str(folder/f'guided-learning-head-{width}.png'),full_page=False,animations='disabled')
     img=page.screenshot(type='jpeg',quality=43,full_page=False,animations='disabled')
     print('MA_LEARN_VISUAL|'+str(width)+'|'+base64.b64encode(img).decode('ascii'),flush=True)
    page.close()
    for_review+=1
 for locale,hub in (('it','it/academy/'),('en','en/academy/'),('es','es/academia/')):
  for width in (1440,390):
   page=browser.new_page(viewport={'width':width,'height':900 if width>390 else 844},is_mobile=width==390)
   page.goto(urljoin(BASE,hub),wait_until='load',timeout=40000)
   block=page.locator('[data-ma-pathways="v1"]')
   assert block.count()==1,(locale,'missing Academy pathways')
   assert page.locator('link[data-ma-pathways-css]').count()==1,(locale,'missing css asset')
   assert block.locator('a.ma-pathway-option').count()==2,(locale,'missing tracks')
   color=block.locator('.ma-pathway-primary').evaluate('(el)=>getComputedStyle(el).backgroundColor')
   assert color=='rgb(33, 88, 237)',(locale,'unstyled Academy',color)
   if width==390:
    overflow=page.evaluate('document.documentElement.scrollWidth-window.innerWidth')
    assert overflow<=4,(locale,'Academy mobile overflow',overflow)
   if locale=='it':
    folder=Path('design-review-screenshots');folder.mkdir(exist_ok=True)
    block.scroll_into_view_if_needed()
    page.screenshot(path=str(folder/f'academy-pathways-{width}.png'),full_page=False,animations='disabled')
   page.close()
 browser.close()
print(f'PASS Guided Learning: {for_review} page/viewport combinations, six lesson controls, reset, courses and existing quiz/crossword preserved')
