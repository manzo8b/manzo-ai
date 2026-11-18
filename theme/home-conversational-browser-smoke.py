#!/usr/bin/env python3
"""Optional Playwright QA for the MANZO AI trilingual conversational home.

Run after building _site and serving it at http://127.0.0.1:8000/manzo-ai/.
Requires playwright and an installed Chromium browser. Not a CI claim.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

LOCALES=("it","en","es")

def inspect(page,base,locale,width,out=None):
 errors=[]
 page.on("pageerror",lambda e:errors.append(str(e)))
 response=page.goto(f"{base}/{locale}/",wait_until="domcontentloaded")
 assert response and response.ok,f"Page not available: {locale}"
 hero=page.locator(".home-hero")
 panel=page.locator('[data-ma-home-discovery="v1"]')
 assert hero.count()==1 and panel.count()==1,f"Home hero/discovery missing: {locale}"
 assert hero.locator(".searchbox input").count()>=1,"Existing search was displaced"
 assert page.locator(".ma-product-scene").count()==1,"Product scene unexpectedly missing"
 assert page.locator(".ma-home-showcase .ma-course-card").count()==6,"Real Academy catalog changed"
 choices=panel.locator("[data-ma-intent]")
 assert choices.count()==4,f"Expected four real goals in {locale}"
 action=panel.locator("[data-ma-discovery-action]")
 initial=action.get_attribute("href")
 assert initial and "ia-per-la-didattica/inizia/" in initial,initial
 expected=choices.nth(2).get_attribute("href")
 choices.nth(2).click()
 assert action.get_attribute("href")==expected,"Goal did not update the recommended route"
 assert choices.nth(2).get_attribute("aria-current")=="true","Active goal not exposed"
 assert action.is_visible(),"Recommended action is hidden"
 assert page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 2") is False,\
  f"Horizontal overflow {locale} at {width}"
 assert not errors,f"JavaScript errors {locale}: {errors}"
 if width<600:
  goal=choices.first.bounding_box()
  scene=page.locator(".ma-product-scene").bounding_box()
  assert goal and scene and goal["y"]<scene["y"],"Mobile goal must precede decorative scene"
 if out:
  Path(out).mkdir(parents=True,exist_ok=True)
  page.screenshot(path=str(Path(out)/f"home-{locale}-{width}.png"),full_page=True)
 print(f"PASS {locale} · {width}px · four goals, existing search, Academy, no overflow")

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument("--base",default="http://127.0.0.1:8000/manzo-ai")
 parser.add_argument("--screenshots",default=None)
 args=parser.parse_args()
 with sync_playwright() as p:
  browser=p.chromium.launch()
  for locale in LOCALES:
   for width,height in ((1440,900),(390,844),(320,750)):
    page=browser.new_page(viewport={"width":width,"height":height})
    inspect(page,args.base.rstrip("/"),locale,width,args.screenshots)
    page.close()
  browser.close()
 print("Home conversational browser smoke PASS")
if __name__=="__main__":main()
