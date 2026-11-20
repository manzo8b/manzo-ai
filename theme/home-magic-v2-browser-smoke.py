#!/usr/bin/env python3
"""Trilingual magic-box Home smoke on a STAGED site, never public production."""
from __future__ import annotations
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE="http://127.0.0.1:8765/manzo-ai"
OUT=Path("home-magic-v2-qa")
TITLE={
"it":"L’IA ti ha risposto con sicurezza. Ma è vero?",
"en":"AI answered confidently. But is it true?",
"es":"La IA respondió con seguridad. ¿Pero es verdad?"
}
COURSE={"it":"academy","en":"academy","es":"academia"}

def test_page(page,loc,width):
 url=f"{BASE}/{loc}/"
 response=page.goto(url,wait_until="domcontentloaded")
 assert response and response.status==200,(loc,width,response.status if response else None)
 assert page.locator("html").get_attribute("lang").lower().startswith(loc),loc
 assert page.locator("h1").count()==1,(loc,"h1 count")
 assert page.locator("h1").inner_text()==TITLE[loc]
 assert page.locator("[data-ma-v2-section]").count()==6
 assert page.locator('[data-ma-v2-section="hero"] .ma-v2-magic').count()==1
 assert page.locator('.ma-v2-question').count()==4
 assert page.locator('.ma-v2-course').count()==6
 assert page.locator('.ma-v2-course > .ma-v2-art svg[aria-hidden="true"]').count()==6
 assert page.locator('.ma-v2-course .ma-v2-kind').count()==6
 assert page.locator('.ma-v2-course .ma-v2-tags span').count()==12
 assert page.locator(".rail").count()==1 and page.locator(".topbar").count()==1
 assert page.locator("footer.site-footer").count()==1
 assert page.locator('h1').evaluate("(el)=>getComputedStyle(el).visibility")=="visible"
 assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth+2"),(loc,width,"horizontal overflow")
 assert page.locator('.ma-v2-course').first.evaluate("(el)=>getComputedStyle(el).display")!="none"
 links=page.locator('[data-ma-v2-section] a[href^="/manzo-ai/"]')
 assert links.count()>=18, (loc,"too few direct course links")
 for link in links.all():
  assert link.get_attribute("href").endswith('/'),(loc,"malformed local route")
 assert page.locator('meta[name="description"]').get_attribute("content")
 toggle=page.locator('[data-ma-v2-motion-control]')
 assert toggle.count()==1 and toggle.is_visible()
 assert toggle.get_attribute('aria-pressed')=="false"
 toggle.click()
 assert toggle.get_attribute("aria-pressed")=="true"
 assert page.locator('.ma-v2-magic').evaluate("(el)=>el.classList.contains('ma-v2-motion-paused')")
 toggle.click()
 assert toggle.get_attribute("aria-pressed")=="false"
 OUT.mkdir(exist_ok=True)
 page.screenshot(path=str(OUT/f"home-v2-{loc}-{width}.png"),full_page=True)
 academy=page.goto(BASE+"/"+loc+"/"+COURSE[loc]+"/",wait_until="domcontentloaded")
 assert academy and academy.status==200
 assert page.locator('[data-ma-v2-academy="preview"] .ma-v2-extra-link').count()==7
 assert page.locator('[data-ma-course-card="1"]').count()==6

def main():
 with sync_playwright() as p:
  browser=p.chromium.launch()
  for lang in TITLE:
   for width,height in ((1440,900),(768,950),(375,812)):
    page=browser.new_page(viewport={"width":width,"height":height})
    test_page(page,lang,width)
    page.close()
   page=browser.new_page(viewport={"width":375,"height":812},reduced_motion="reduce")
   page.goto(BASE+"/"+lang+"/",wait_until="domcontentloaded")
   assert page.locator('[data-ma-v2-motion-control]').is_hidden()
   lid=page.locator('.ma-v2-lid')
   assert lid.evaluate("(el)=>getComputedStyle(el).animationName")=="none"
   page.close()
   # The entire static page is navigable if JavaScript is unavailable.
   page=browser.new_page(viewport={"width":375,"height":812},java_script_enabled=False)
   page.goto(BASE+"/"+lang+"/",wait_until="domcontentloaded")
   assert page.locator('[data-ma-v2-section]').count()==6
   assert page.locator('.ma-v2-motion-toggle').is_hidden()
   assert page.locator('.ma-v2-course').count()==6
   page.close()
  browser.close()
 print("PASS staged MANZO Home V2: 3 locales × 3 widths + reduced-motion, pause/resume, 6+7 course destinations, no-JS fallback, no overflow")

if __name__=="__main__":
 main()
