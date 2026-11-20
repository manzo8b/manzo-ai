#!/usr/bin/env python3
"""End-to-end browser checks for the MANZO AI coding assurance module."""
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin

BASE='http://127.0.0.1:8765/manzo-ai/'
ROUTES={
 'it':'it/impara/allucinazioni-ai-verificabilita/coding/',
 'en':'en/learn/ai-hallucinations-verification/coding/',
 'es':'es/aprende/alucinaciones-ia-verificacion/coding/'
}
PARENTS={
 'it':'it/impara/allucinazioni-ai-verificabilita/',
 'en':'en/learn/ai-hallucinations-verification/',
 'es':'es/aprende/alucinaciones-ia-verificacion/'
}
def inspect(page,loc,mobile=False):
 page.goto(urljoin(BASE,ROUTES[loc]),wait_until='load',timeout=35000)
 assert page.locator('h1').count()==1,loc
 assert page.locator('.hc-section').count()==6,loc
 assert page.locator('[data-hc-case]').count()==4,loc
 assert page.locator('[data-hc-gate]').count()==8,loc
 assert page.locator('.hc-ref').count()==4,loc
 assert page.locator('pre code').count()==2,loc
 assert page.locator('link[href*="coding.css?v="]').count()==1,(loc,'cache-safe stylesheet missing')
 # Compute the real browser colors, not merely CSS source declarations.
 ratios=page.evaluate("""() => {
   const rgb=value=>(value.match(/\\d+/g)||[]).slice(0,3).map(Number);
   const lum=value=>{
     const c=rgb(value).map(n=>n/255).map(v=>v<=0.04045?v/12.92:Math.pow((v+0.055)/1.055,2.4));
     return c[0]*0.2126+c[1]*0.7152+c[2]*0.0722;
   };
   const ratio=(fg,bg)=>{const a=lum(fg),b=lum(bg);return (Math.max(a,b)+0.05)/(Math.min(a,b)+0.05)};
   const color=sel=>getComputedStyle(document.querySelector(sel)).color;
   const bg=sel=>getComputedStyle(document.querySelector(sel)).backgroundColor;
   return {
     title:ratio(color('.hc-banner h2'),bg('.hc-banner')),
     introduction:ratio(color('.hc-banner > p:not(.hc-eyebrow)'),bg('.hc-banner')),
     stageTitle:ratio(color('.hc-banner .hc-stage strong'),bg('.hc-banner .hc-stage')),
     stageBody:ratio(color('.hc-banner .hc-stage p'),bg('.hc-banner .hc-stage')),
     stageIndex:ratio(color('.hc-banner .hc-stage small'),bg('.hc-banner .hc-stage'))
   };
 }""")
 assert all(value>=4.5 for value in ratios.values()),(loc,mobile,'Engineering banner WCAG AA contrast failure',ratios)
 assert ratios['title']>=7.0 and ratios['stageBody']>=7.0,(loc,mobile,'Core contrast under AAA',ratios)
 assert page.locator('.hc-quiz-options label').count()==4,loc
 assert page.locator('[data-hc-position]').inner_text().strip()=='1 / 4',loc
 assert page.locator('.hc-section p').count()>=24,loc
 assert page.locator('link[rel=alternate][hreflang=it]').count()==1,loc
 page.locator('[data-hc-gate]').first.check()
 assert page.locator('[data-hc-gate-status]').inner_text().startswith('1 / 8'),loc
 case=page.locator('[data-hc-case]').first
 assert case.locator('button[data-hc-review]').is_disabled()
 case.locator('textarea').fill('This documentation cannot establish the existence of the claimed SDK method.')
 assert case.locator('button[data-hc-review]').is_enabled()
 case.locator('button[data-hc-review]').click()
 assert case.locator('[data-hc-solution]').is_visible(),loc
 page.locator('.hc-quiz-options input').nth(1).check()
 page.locator('[data-hc-submit]').click()
 assert page.locator('[data-hc-feedback]').is_visible(),loc
 page.locator('[data-hc-next]').click()
 assert page.locator('[data-hc-position]').inner_text().strip()=='2 / 4',loc
 width=page.evaluate('document.documentElement.scrollWidth')
 vp=page.evaluate('window.innerWidth')
 assert width<=vp+2,f'{loc}: horizontal overflow width={width}, viewport={vp} mobile={mobile}'

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,args=['--no-sandbox'])
 for loc in ROUTES:
  for ismobile in (False,True):
   page=browser.new_page(viewport={'width':390 if ismobile else 1366,'height':845},device_scale_factor=2 if ismobile else 1,is_mobile=ismobile)
   inspect(page,loc,ismobile)
   page.goto(urljoin(BASE,PARENTS[loc]),wait_until='load')
   assert page.locator('[data-hc-coding-chapter]').count()==1
   assert page.locator('.hx-module').count()==6
   page.close()
 browser.close()
print('PASS: Engineering Assurance in IT/EN/ES: 6 editorial sections, 4 cases, 8 gates, quiz interactions, course links, desktop and mobile.')
