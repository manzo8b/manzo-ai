#!/usr/bin/env python3
"""Chromium QA for MANZO AI Academy's three guided routes (IT/EN/ES)."""
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE="http://127.0.0.1:8765/manzo-ai"
LANG={"it":"academy","en":"academy","es":"academia"}
DEST=Path("design-review-screenshots")

def test(page,lang,route,width):
 page.set_viewport_size({"width":width,"height":844 if width<500 else 900})
 errors=[]
 page.on("pageerror",lambda err:errors.append(str(err)))
 resp=page.goto(f"{BASE}/{lang}/{route}/",wait_until="domcontentloaded")
 assert resp and resp.status==200
 section=page.locator('[data-ma-journeys="v1"]')
 assert section.count()==1
 assert section.locator("h2").count()==1
 assert not section.locator("h2").inner_text().strip().endswith(".")
 options=section.locator("[data-ma-journey-choice]")
 panels=section.locator("[data-ma-journey-panel]")
 assert options.count()==3 and panels.count()==3
 assert page.locator("[data-ma-course-card='1']").count()==6, "Original catalog changed"
 for i in range(3):
  options.nth(i).click()
  assert options.nth(i).get_attribute("aria-pressed")=="true"
  assert panels.nth(i).is_visible()
  assert sum(panel.is_visible() for panel in panels.all())==1
  links=panels.nth(i).locator("ol a.ma-journey-step-title")
  assert links.count()==3
  for link in links.all():
   url=link.get_attribute("href")
   assert url and url.startswith(f"/manzo-ai/{lang}/")
   assert link.is_visible()
 assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 3"),f"Overflow {lang}/{width}"
 options.first.click()
 options.first.press("ArrowRight")
 assert options.nth(1).get_attribute("aria-pressed")=="true"
 options.nth(1).press("End")
 assert options.last.get_attribute("aria-pressed")=="true"
 options.last.press("Home")
 assert options.first.get_attribute("aria-pressed")=="true"
 page.evaluate("window.__maPrinted=false;window.print=()=>{window.__maPrinted=true}")
 section.locator("[data-ma-journey-print]").click()
 assert page.evaluate("window.__maPrinted")
 assert not errors,errors
 DEST.mkdir(parents=True,exist_ok=True)
 page.screenshot(path=str(DEST/f"academy-journeys-{lang}-{width}.png"),full_page=True)

def main():
 with sync_playwright() as p:
  browser=p.chromium.launch()
  for lang,route in LANG.items():
   for width in (1440,390):
    page=browser.new_page()
    test(page,lang,route,width)
    page.close()
  page=browser.new_page(reduced_motion="reduce")
  page.goto(f"{BASE}/it/academy/",wait_until="domcontentloaded")
  first=page.locator('[data-ma-journey-choice="0"]')
  first.hover()
  assert first.evaluate("(x)=>getComputedStyle(x).transitionDuration") in ("0s","0s, 0s, 0s, 0s")
  page.close()
  browser.close()
 print("PASS: 3 guided journeys × IT/EN/ES, choices, steps, print, mobile, focus, reduced motion")

if __name__=="__main__":main()
