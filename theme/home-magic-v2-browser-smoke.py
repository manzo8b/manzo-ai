#!/usr/bin/env python3
"""Trilingual MANZO Home staging checks, without publishing to production."""
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
LABEL={
 "it":"Conoscenza e prompt",
 "en":"Knowledge & Prompt Lab",
 "es":"Conocimiento y prompts",
}
COURSE={"it":"academy","en":"academy","es":"academia"}

def test_page(page,loc,width):
 response=page.goto(f"{BASE}/{loc}/",wait_until="domcontentloaded")
 assert response and response.status==200,(loc,width,response.status if response else None)
 assert page.locator("html").get_attribute("lang").lower().startswith(loc)
 assert page.locator("h1").count()==1 and page.locator("h1").inner_text()==TITLE[loc]
 assert page.locator("[data-ma-v2-section]").count()==5
 assert page.locator('.ma-v2-questions').count()==0,(loc,"duplicate questions still visible")
 assert page.locator('[data-ma-v2-section="hero"] .ma-v2-magic').count()==1
 assert page.locator(".ma-v2-course").count()==6
 assert page.locator(".ma-v2-tone-rose").count()==1
 assert page.locator('.ma-v2-course > .ma-v2-art svg[aria-hidden="true"]').count()==6
 assert page.locator(".ma-v2-course .ma-v2-kind").count()==6
 assert page.locator(".ma-v2-course .ma-v2-tags span").count()==12
 assert page.locator(".rail").count()==1 and page.locator(".topbar").count()==1
 assert page.locator("footer.site-footer").count()==1
 assert page.locator(".topbar .top-label").inner_text()==LABEL[loc]
 assert page.locator("h1").evaluate("(el)=>getComputedStyle(el).visibility")=="visible"
 assert page.evaluate("document.documentElement.scrollWidth<=window.innerWidth+2"),(loc,width,"horizontal overflow")
 assert page.locator(".ma-v2-course").first.evaluate("(el)=>getComputedStyle(el).display")!="none"
 links=page.locator('[data-ma-v2-section] a[href^="/manzo-ai/"]')
 assert links.count()>=14,(loc,"too few working links")
 for link in links.all():
  assert link.get_attribute("href").endswith('/'),(loc,"malformed local route")
 assert page.locator('meta[name="description"]').get_attribute("content")
 if width==768:
  copy=page.locator(".ma-v2-hero-copy").bounding_box()
  art=page.locator(".ma-v2-magic").bounding_box()
  assert copy and art and art["y"]>=copy["y"]+copy["height"]-2,(loc,"tablet hero must be stacked")
  for action in page.locator(".ma-v2-actions a").all():
   assert action.bounding_box()["height"]<110,(loc,"tablet CTA too tall")
  assert page.locator(".ma-v2-hero h1").evaluate(
   "(el)=>getComputedStyle(el).hyphens")=="none",(loc,"title hyphenated")
 if width==375:
  nav=page.locator(".manzo-mobile-bar").bounding_box()
  menu=page.locator(".manzo-mobile-toggle").bounding_box()
  assert nav and menu,(loc,"mobile navigation missing")
  assert nav["x"]>=-1 and nav["x"]+nav["width"]<=width+1,(loc,"bar clipped")
  assert menu["x"]>=-1 and menu["x"]+menu["width"]<=width+1,(loc,"menu clipped")
  visible=page.locator(".ma-v2-actions a").first.evaluate("""el=>{
    const r=el.getBoundingClientRect(),x=r.left+r.width/2,y=r.top+r.height/2;
    if(y<0||y>=innerHeight)return true;
    return el.contains(document.elementFromPoint(x,y));
  }""")
  assert visible,(loc,"primary hero CTA obscured at initial scroll")
 toggle=page.locator("[data-ma-v2-motion-control]")
 assert toggle.count()==1 and toggle.is_visible()
 assert toggle.get_attribute("aria-pressed")=="false"
 toggle.click()
 assert toggle.get_attribute("aria-pressed")=="true"
 assert toggle.get_attribute("aria-label")
 assert page.locator(".ma-v2-magic").evaluate("(el)=>el.classList.contains('ma-v2-motion-paused')")
 toggle.click()
 assert toggle.get_attribute("aria-pressed")=="false"
 OUT.mkdir(exist_ok=True)
 page.evaluate("window.scrollTo(0,0)")
 page.wait_for_timeout(150)
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
   assert page.locator(".ma-v2-lid").evaluate("(el)=>getComputedStyle(el).animationName")=="none"
   page.close()
   page=browser.new_page(viewport={"width":375,"height":812},java_script_enabled=False)
   page.goto(BASE+"/"+lang+"/",wait_until="domcontentloaded")
   assert page.locator('[data-ma-v2-section]').count()==5
   assert page.locator(".ma-v2-motion-toggle").is_hidden()
   assert page.locator(".ma-v2-course").count()==6
   page.close()
  browser.close()
 print("PASS staged Home V2: five sections x three locales x three widths, tablet/mobile, motion and no-JS")

if __name__=="__main__":
 main()
