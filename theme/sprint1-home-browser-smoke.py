#!/usr/bin/env python3
"""MANZO AI Sprint 1 Home visual QA across locales, widths and JS fallback."""
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE="http://127.0.0.1:8765/manzo-ai"
DEST=Path("design-review-screenshots")
EXPECT={
 "it":("L'AI si impara facendo",["Comprendi","Sperimenta","Verifica","Costruisci"]),
 "en":("Learn AI by building understanding",["Understand","Experiment","Verify","Build"]),
 "es":("Aprende IA construyendo criterio",["Comprender","Experimentar","Verificar","Construir"])
}

def test_page(page,loc,width):
 response=page.goto(BASE+"/"+loc+"/",wait_until="domcontentloaded")
 assert response and response.status==200,(loc,width)
 page.wait_for_function(
  """() => document.querySelector('[data-ma-s1-toggle]') &&
           !document.querySelector('[data-ma-s1-toggle]').hidden""",timeout=10000)
 assert page.locator(".home-hero h1").inner_text()==EXPECT[loc][0]
 assert page.locator(".home-hero input").count()>=1,loc+" search lost"
 assert page.locator('[data-ma-home-primary-nav="v2"]').count()==1
 assert page.locator('[data-ma-home-discovery="v1"]').count()==1
 assert page.locator('.ma-s1-step').count()==4
 for i,label in enumerate(EXPECT[loc][1],1):
  card=page.locator('.ma-s1-step[data-ma-s1-step="'+str(i)+'"]')
  assert card.locator('strong').inner_text()==label
  href=card.get_attribute("href")
  assert href and href.startswith("/manzo-ai/") and href.endswith("/")
 toggle=page.locator('[data-ma-s1-toggle="v1"]')
 grid=page.locator('.ma-home-course-grid')
 assert grid.locator('> article').count()==13
 assert grid.locator('> article:visible').count()==4,(loc,width,"initial preview")
 assert toggle.get_attribute("aria-expanded")=="false"
 assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2"),(loc,width,"overflow")
 assert page.locator('.ma-s1-hero-primary').is_visible()
 assert page.locator('.ma-s1-hero-secondary').is_visible()
 DEST.mkdir(parents=True,exist_ok=True)
 page.screenshot(path=str(DEST/("sprint1-home-"+loc+"-"+str(width)+".png")),full_page=True)
 toggle.click()
 assert toggle.get_attribute("aria-expanded")=="true"
 assert grid.locator('> article:visible').count()==13
 toggle.click()
 assert toggle.get_attribute("aria-expanded")=="false"
 assert grid.locator('> article:visible').count()==4
 assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2"),(loc,width,"overflow-expanded")

def main():
 with sync_playwright() as p:
  browser=p.chromium.launch()
  for locale in EXPECT:
   for width,height in ((1440,900),(390,844)):
    page=browser.new_page(viewport={"width":width,"height":height})
    test_page(page,locale,width)
    page.close()
  # HTML itself must be usable if script execution is blocked or unavailable.
  for locale in EXPECT:
   page=browser.new_page(viewport={"width":390,"height":844},java_script_enabled=False)
   resp=page.goto(BASE+"/"+locale+"/",wait_until="domcontentloaded")
   assert resp and resp.status==200
   assert page.locator(".ma-home-course-grid > article:visible").count()==13
   assert page.locator('[data-ma-s1-toggle="v1"]').is_hidden()
   page.close()
  page=browser.new_page(viewport={"width":1440,"height":900},reduced_motion="reduce")
  page.goto(BASE+"/it/",wait_until="domcontentloaded")
  card=page.locator('.ma-s1-step').first
  card.hover()
  assert card.evaluate("(el)=>getComputedStyle(el).transform")=="none"
  page.close()
  browser.close()
 print("PASS: MANZO AI Sprint 1 Home / IT EN ES / 1440 390 / 4→13 cards / no-JS fallback / reduced motion / preserved search")

if __name__=="__main__":
 main()
