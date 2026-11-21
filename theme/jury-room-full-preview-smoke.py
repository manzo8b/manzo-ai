#!/usr/bin/env python3
"""Review the real MANZO AI Home v2 with Jury Room v0.5, without deployment.

Requires a local HTTP server exposing the generated _site at
http://127.0.0.1:8765/manzo-ai/ (same layout as the Home Magic v2 preview).
Screenshots and a small factual QA record are written to jury-room-full-preview-qa/.
"""
from __future__ import annotations
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE="http://127.0.0.1:8765/manzo-ai"
OUT=Path("jury-room-full-preview-qa")
ROOMS=[
 "it/laboratorio/stanza-dei-giurati/",
 "it/laboratorio/stanza-dei-giurati/banco-di-prova/",
 "it/laboratorio/stanza-dei-giurati/officina-locale/",
 "it/laboratorio/stanza-dei-giurati/sala-dei-confini/",
]
WIDTHS=(375,390,768,1440)
OUT.mkdir(exist_ok=True)
observations=[]

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 for width in WIDTHS:
  context=browser.new_context(
   viewport={'width':width,'height':900},
   reduced_motion='reduce',
   device_scale_factor=1,
  )
  page=context.new_page()
  page.set_default_timeout(18000)
  errors=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
  response=page.goto(f"{BASE}/it/",wait_until="networkidle")
  assert response and response.status==200,("IT Home HTTP status",width)
  assert page.locator('section[data-ma-v2-section]').count()==5,("Home section contract",width)
  assert page.locator('[data-ma-v2-card]').count()==6,("Home card contract",width)
  assert page.locator('h1').count()==1,("Home h1 contract",width)
  assert page.locator('.ma-v2-magic-stage').count()==1,("original Magic Box missing",width)
  badge=page.locator('.ma-jury-top-notice')
  teaser=page.locator('section[data-ma-v2-section="hero"] .ma-jury-hero-feature')
  artwork=teaser.locator('img.ma-jury-feature-image')
  cta=teaser.locator('a.ma-jury-feature-action')
  assert badge.count()==1 and badge.is_visible(),("Home badge missing",width)
  assert teaser.count()==1 and teaser.is_visible(),("full-width feature missing",width)
  assert artwork.count()==1 and artwork.is_visible() and artwork.evaluate(
   "(el)=>el.complete&&el.naturalWidth>1000&&el.naturalHeight>500"
  ),("original approved palace artwork not loaded",width)
  assert 'palazzo-stendardi-manzo.webp' in artwork.get_attribute('src')
  assert 'Nuovo esperimento' in badge.inner_text().capitalize(),("badge wording",width)
  assert cta.count()==1 and cta.is_visible(),("experiment CTA missing",width)
  assert cta.get_attribute('href')=="/manzo-ai/it/laboratorio/stanza-dei-giurati/"
  rect=teaser.bounding_box()
  hero=page.locator('section[data-ma-v2-section="hero"]').bounding_box()
  assert rect and hero and rect['width']>=hero['width']*.8,("not a prominent full-width feature",width,rect,hero)
  assert page.evaluate("document.documentElement.scrollWidth<=innerWidth+3"),("horizontal scrolling",width)
  assert not errors,("JavaScript errors in IT Home",width,errors)
  badge_rect=badge.bounding_box()
  assert badge_rect and badge_rect['y']<900,("badge not visible in first viewport",width)
  cta.focus()
  assert cta.evaluate("(el)=>document.activeElement===el"),("CTA keyboard focus",width)
  # A click must open a functioning Italian experience, not a 404.
  with page.expect_navigation(wait_until="domcontentloaded"):
   cta.click()
  assert page.url.rstrip('/').endswith('/it/laboratorio/stanza-dei-giurati')
  assert page.locator('h1').count()==1,("experiment landing heading",width)
  assert page.locator('meta[name=robots]').get_attribute('content')=="noindex,nofollow",width
  assert page.locator('a[href*="banco-di-prova"],a[href*="officina-locale"],a[href*="sala-dei-confini"]').count()>0
  assert page.evaluate("document.documentElement.scrollWidth<=innerWidth+3"),("experiment landing overflow",width)
  page.goto(f"{BASE}/it/",wait_until="networkidle")
  page.locator('.ma-jury-hero-feature').scroll_into_view_if_needed()
  page.screenshot(path=str(OUT/f"home-jury-{width}px.png"),full_page=True,animations='disabled')
  observations.append({'viewport':width,'home_sections':5,'home_cards':6,
                       'palace_loaded':True,'badge_in_initial_view':True,
                       'cta_opens_experiment':True})
  context.close()
 # Exact four pages reachable and not accidentally indexed
 page=browser.new_page(viewport={'width':1440,'height':900})
 for path in ROOMS:
  response=page.goto(f'{BASE}/{path}',wait_until='domcontentloaded')
  assert response and response.status==200,(path,"HTTP error")
  assert page.locator('meta[name=robots]').get_attribute('content')=="noindex,nofollow"
  assert page.locator('h1').count()==1
  assert page.evaluate("document.documentElement.scrollWidth<=innerWidth+3"),(path,"overflow")
  assert page.locator('script[src^="/manzo-ai/assets/jury-room/"]').count()>=1,(path,"missing rewritten JS")
 for loc in ("en","es"):
  response=page.goto(f'{BASE}/{loc}/',wait_until="domcontentloaded")
  assert response and response.status==200
  assert page.locator('[data-ma-jury-home-preview]').count()==0,(loc,"teaser should be IT-only")
  assert page.locator('[data-ma-jury-top-badge]').count()==0,(loc,"no unpublished translations")
  assert page.locator('[data-ma-v2-card]').count()==6
 browser.close()

(OUT/'QA.json').write_text(json.dumps({
 'scope':'real full Home staging + Jury Room v0.5',
 'production_deploy':False,'screenshots':[f'home-jury-{w}px.png' for w in WIDTHS],
 'observations':observations,'noindex_routes':ROOMS
},indent=2,ensure_ascii=False),encoding='utf-8')
print('PASS: full Home integrated with prominent experiment Hero, four live staging paths, EN/ES unchanged.')
