#!/usr/bin/env python3
"""MANZO AI Learning B2B client-side simulation browser QA.

Tests actual browser behavior; this is NOT a test of production identity,
billing, durable student records or SaaS access.
"""
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin

BASE='http://127.0.0.1:8765/manzo-ai/'
ROUTES={
 'it':'it/prodotto/learning-b2b/',
 'en':'en/product/learning-b2b/',
 'es':'es/producto/learning-b2b/'
}
PARENTS={'it':'it/prodotto/','en':'en/product/','es':'es/producto/'}

def check(page,locale,mobile):
 errors=[]
 page.on('pageerror',lambda error:errors.append(str(error)))
 page.goto(urljoin(BASE,ROUTES[locale]),wait_until='load',timeout=30000)
 assert page.locator('html').get_attribute('lang')==locale
 assert page.locator('meta[name=robots]').get_attribute('content')=='noindex,follow'
 assert page.locator('h1').count()==1
 assert page.locator('#lc-members tr').count()==4
 assert page.locator('#lc-metric-0').inner_text()=='2 / 3'
 assert page.locator('#lc-metric-1').inner_text()=='3'
 assert page.locator('#lc-tab-admin').get_attribute('aria-selected')=='true'
 assert page.locator('#lc-student-view-panel').is_hidden()
 assert page.locator('link[rel=alternate][hreflang=it]').count()==1
 # Allocate the third and last available seat.
 page.locator('button[data-seat-member="u3"]').click()
 assert page.locator('#lc-metric-0').inner_text()=='3 / 3'
 assert page.locator('button[data-seat-member="u4"]').is_disabled()
 # Enroll the newly licensed learner in a published sample course.
 page.locator('#lc-student-admin').select_option('u3')
 page.locator('#lc-course-admin').select_option('coding')
 page.locator('#lc-enroll').click()
 assert page.locator('#lc-metric-1').inner_text()=='4'
 # View progress as a SIMULATED student; selecting a profile is not login.
 page.locator('#lc-tab-student').click()
 assert page.locator('#lc-tab-student').get_attribute('aria-selected')=='true'
 page.locator('#lc-student-view').select_option('u3')
 assert page.locator('#lc-student-courses .course-card').count()==1
 assert page.locator('#lc-student-courses [role=progressbar]').get_attribute('aria-valuenow')=='0'
 page.locator('button[data-complete-user="u3"]').click()
 assert page.locator('#lc-student-courses [role=progressbar]').get_attribute('aria-valuenow')=='17'
 # Release seat: enrollment becomes revoked, paid course inaccessible.
 page.locator('#lc-tab-admin').click()
 page.locator('button[data-seat-member="u3"]').click()
 assert page.locator('#lc-metric-0').inner_text()=='2 / 3'
 page.locator('#lc-tab-student').click()
 page.locator('#lc-student-view').select_option('u3')
 assert page.locator('#lc-student-courses .course-card').count()==0
 assert page.locator('#lc-student-access').is_visible()
 # Released seat can be reassigned, enrollment stays revoked until new approval.
 page.locator('#lc-tab-admin').click()
 page.locator('button[data-seat-member="u3"]').click()
 page.locator('#lc-tab-student').click()
 page.locator('#lc-student-view').select_option('u3')
 assert page.locator('#lc-student-courses .course-card').count()==0
 # Reset all sample state. No persistent data or test credentials.
 page.locator('#lc-tab-admin').click()
 page.locator('#lc-reset').click()
 assert page.locator('#lc-metric-0').inner_text()=='2 / 3'
 assert page.locator('#lc-metric-1').inner_text()=='3'
 assert page.locator('#lc-events li').count()==1
 assert page.evaluate('localStorage.length')==0
 assert page.evaluate('sessionStorage.length')==0
 assert page.locator('input[type=password]').count()==0
 assert page.locator('form[action]').count()==0
 width=page.evaluate('document.documentElement.scrollWidth')
 viewport=page.evaluate('window.innerWidth')
 assert width<=viewport+2, f'{locale}: overflow {width}>{viewport}, mobile={mobile}'
 assert not errors, f'Browser errors in {locale}: {errors}'
 page.goto(urljoin(BASE,PARENTS[locale]),wait_until='load')
 assert page.locator('[data-learning-b2b-console]').count()==1

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,args=['--no-sandbox'])
 for locale in ROUTES:
  for mobile in (False,True):
   page=browser.new_page(
       viewport={'width':390 if mobile else 1366,'height':844},
       is_mobile=mobile,device_scale_factor=2 if mobile else 1
   )
   check(page,locale,mobile)
   page.close()
 browser.close()
print('PASS: IT/EN/ES B2B simulation; 3 seats, 4 learners, enrollment, progress, license revocation, reset, mobile and no storage.')
