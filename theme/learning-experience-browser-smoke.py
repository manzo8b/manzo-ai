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
     # Six native details: outcomes and references to ORIGINAL case/quiz sections.
     checks=root.locator('.ma-unit-evidence')
     assert checks.count()==6,(locale,width,'missing unit competency disclosures')
     assert checks.locator('summary').count()==6
     assert all(not box.get_attribute('open') for box in checks.all())
     first_check=checks.first
     first_check.locator('summary').click()
     assert first_check.get_attribute('open') is not None,(locale,width,'details cannot be opened')
     assert first_check.get_attribute('data-ma-core-case')=='2'
     assert first_check.get_attribute('data-ma-core-quiz')=='1'
     assert [a.get_attribute('href') for a in first_check.locator('.ma-unit-evidence-links a').all()]==['#hx-lab','#hx-quiz']
     first_check.locator('summary').click()
     assert first_check.get_attribute('open') is None
     assert page.locator('.hx-module').count()==6
     assert page.locator('.hx-case').count()==10
     assert page.locator('#hx-quiz-data').count()==1
     assert page.locator('#hx-quiz-check').is_enabled()
     assert page.locator('#hx-cross-grid').count()==1
    else:
     checks=root.locator('.ma-unit-evidence')
     assert checks.count()==6,(locale,width,'six coding competency disclosures missing')
     assert checks.locator('summary').count()==6
     assert all(not box.get_attribute('open') for box in checks.all())
     first_check=checks.first
     first_check.locator('summary').click()
     assert first_check.get_attribute('open') is not None,(locale,width,'coding disclosure cannot open')
     assert first_check.get_attribute('data-ma-coding-case')=='2'
     assert first_check.get_attribute('data-ma-coding-quiz')=='2'
     assert [a.get_attribute('href') for a in first_check.locator('.ma-unit-evidence-links a').all()]==['#hc-lab','#hc-quiz']
     first_check.locator('summary').click()
     assert first_check.get_attribute('open') is None
     assert checks.last.locator('.ma-unit-evidence-limit').count()==1,(locale,width,'business-value evidence limit absent')
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
   errors=[]
   page.on('pageerror',lambda exception:errors.append(str(exception)))
   page.goto(urljoin(BASE,hub),wait_until='load',timeout=40000)
   block=page.locator('[data-ma-pathways="v1"]')
   assert block.count()==1,(locale,'missing Academy catalog')
   assert page.locator('link[data-ma-pathways-css]').count()==1,(locale,'missing CSS')
   assert page.locator('script[data-ma-pathways-js]').count()==1,(locale,'missing search JS')
   cards=block.locator('[data-ma-course-card]')
   assert cards.count()==6,(locale,'catalog item count')
   assert cards.locator('[data-ma-course-orientation="1"]').count()==6,(locale,'missing positioning cues')
   assert all(len(hint.inner_text().strip())>18 for hint in cards.locator('.ma-course-orientation').all()),(locale,'empty path guidance')
   assert block.locator('[data-ma-count]').inner_text()=='6'
   color=block.locator('.ma-catalog-hero').evaluate('(el)=>getComputedStyle(el).backgroundColor')
   assert color=='rgb(29, 80, 221)',(locale,'weak/unloaded Academy design',color)
   first_card=cards.first
   art=first_card.locator('.ma-course-art').evaluate('(el)=>getComputedStyle(el).backgroundColor')
   assert art=='rgb(33, 88, 237)',(locale,'unstyled card',art)
   shadow=first_card.evaluate('(el)=>getComputedStyle(el).boxShadow')
   assert shadow!='none',(locale,'modern card effect missing')
   for anchor in cards.locator('.ma-course-link').all():
    link=anchor.get_attribute('href')
    assert link and link.startswith('/manzo-ai/'),(locale,'external or nonexistent catalog link',link)
    response=page.request.get(urljoin('http://127.0.0.1:8765',link),timeout=10000)
    assert response.status==200,(locale,'broken course link',link,response.status)
   # Subject filters: two verification resources, one specialist coding resource.
   block.locator('[data-ma-filter="verify"]').click()
   assert block.locator('[data-ma-count]').inner_text()=='2'
   assert block.locator('[data-ma-course-card]:visible').count()==2
   block.locator('[data-ma-filter="coding"]').click()
   assert block.locator('[data-ma-count]').inner_text()=='1'
   assert block.locator('[data-ma-course-card]:visible').count()==1
   # Search and no-match reset, with aria-live count.
   query=block.locator('#ma-course-search')
   block.locator('[data-ma-filter="all"]').click()
   query.fill('Engineering')
   matched=block.locator('[data-ma-count]').inner_text()
   assert matched=='1',(locale,'keyword search should match specialist module',matched,[x.get_attribute('data-ma-search')[:70] for x in cards.all()])
   query.fill('manzo-nonexistent-search')
   assert block.locator('[data-ma-count]').inner_text()=='0'
   assert block.locator('[data-ma-empty]').is_visible()
   block.locator('[data-ma-clear]').click()
   assert block.locator('[data-ma-count]').inner_text()=='6'
   assert block.locator('[data-ma-empty]').is_hidden()
   if width==1440:
    first_card.hover()
    page.wait_for_timeout(380)
    transform=first_card.evaluate('(el)=>getComputedStyle(el).transform')
    assert transform!='none',(locale,'hover elevation not applied')
   if width==390:
    overflow=page.evaluate('document.documentElement.scrollWidth-window.innerWidth')
    assert overflow<=4,(locale,'Academy mobile overflow',overflow)
   if locale=='it':
    folder=Path('design-review-screenshots');folder.mkdir(exist_ok=True)
    block.locator('.ma-catalog-hero').scroll_into_view_if_needed()
    page.wait_for_timeout(90)
    page.screenshot(path=str(folder/f'academy-hero-{width}.png'),full_page=False,animations='disabled')
    block.locator('.ma-course-grid').scroll_into_view_if_needed()
    page.wait_for_timeout(90)
    page.screenshot(path=str(folder/f'academy-modern-cards-{width}.png'),full_page=False,animations='disabled')
   assert not errors,(locale,errors)
   page.close()
 browser.close()
print(f'PASS Guided Learning: {for_review} course views + 6 Academy catalog views, 6 live routes per locale, filters/search, card motion, module controls and unchanged assessment logic')
