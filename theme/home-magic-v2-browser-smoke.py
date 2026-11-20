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
 # SVG uses painter order: symbols must be after the box/lid so the rising
 # question/method/evidence cards cannot disappear behind the open lid.
 assert page.locator(".ma-v2-box-svg").evaluate("""svg=>{
   const box=svg.querySelector('.ma-v2-box');
   const lid=svg.querySelector('.ma-v2-lid');
   const symbols=svg.querySelector('.ma-v2-artifacts');
   return Boolean(box&&lid&&symbols&&box.contains(lid)&&
     (box.compareDocumentPosition(symbols)&Node.DOCUMENT_POSITION_FOLLOWING));
 }"""),(loc,"animated symbols incorrectly layered behind the lid")
 # The closed pose is only the start of the animation. Freeze all keyframes
 # in the OPEN phase and prove that the two flaps move outward while the three
 # distinct learning symbols rise above the rim and remain fully opaque.
 assert page.locator(".ma-v2-flap").count()==2,(loc,"missing left/right flaps")
 assert page.locator(".ma-v2-artifact").count()==3,(loc,"three symbols expected")
 assert page.locator(".ma-v2-beam").count()==1,(loc,"missing luminous inner beam")
 page.evaluate("""()=>{
   const selectors=['.ma-v2-box-svg','.ma-v2-lid','.ma-v2-orbit',
     '.ma-v2-beam','.ma-v2-flap','.ma-v2-artifacts','.ma-v2-artifact'];
   for(const selector of selectors){
     for(const el of document.querySelectorAll(selector)){
       for(const animation of el.getAnimations({subtree:false})){
         const timing=animation.effect.getTiming();
         if(timing.duration && typeof timing.duration==='number' && timing.duration<15000){
           animation.pause();
           animation.currentTime=6200;
         }
       }
     }
   }
 }""")
 assert page.locator(".ma-v2-artifacts").evaluate(
  "(e)=>Number(getComputedStyle(e).opacity)>.95"),(loc,"symbols invisible in open pose")
 assert page.locator(".ma-v2-flap-left").evaluate(
  "(e)=>new DOMMatrix(getComputedStyle(e).transform).m41 < -85"),(loc,"left flap fails to clear opening")
 assert page.locator(".ma-v2-flap-right").evaluate(
  "(e)=>new DOMMatrix(getComputedStyle(e).transform).m41 > 85"),(loc,"right flap fails to clear opening")
 assert page.locator(".ma-v2-artifact.ma-v2-b").evaluate(
  "(e)=>new DOMMatrix(getComputedStyle(e).transform).m42 < -45"),(loc,"central symbol fails to rise")
 assert page.locator(".ma-v2-artifact.ma-v2-a").evaluate(
  "(e)=>new DOMMatrix(getComputedStyle(e).transform).m42 < -28"),(loc,"question symbol fails to rise")
 if width==1440 and loc=="it":
  OUT.mkdir(exist_ok=True)
  page.locator(".ma-v2-magic-stage").screenshot(path=str(OUT/"magic-box-open-3d-it.png"))
 # Resume CSS animations for subsequent interaction checks.
 page.evaluate("""()=>{
   for(const el of document.querySelectorAll(
      '.ma-v2-box-svg,.ma-v2-orbit,.ma-v2-beam,.ma-v2-flap,.ma-v2-artifacts,.ma-v2-artifact'))
     for(const animation of el.getAnimations({subtree:false}))animation.play();
 }""")

 # Exact Academy components — not a similar Home-specific card template.
 native=page.locator(".ma-v2-courses .ma-course-card")
 assert native.count()==6,(loc,"six native Academy cards expected")
 assert page.locator(".ma-v2-courses .ma-course-grid").count()==1
 assert page.locator(".ma-v2-courses .ma-course-link").count()==6
 assert page.locator(".ma-v2-courses .ma-course-art").count()==6
 assert page.locator(".ma-v2-courses .ma-course-info h3").count()==6
 assert page.locator(".ma-v2-courses .ma-course-cta b").count()==6
 assert page.locator(".ma-v2-courses .ma-v2-course").count()==0,(loc,"old card system survived")
 assert page.locator('link[href*="learning-experience/guide.css"]').count()>=1
 home_cards=[(c.locator("h3").inner_text(),c.locator("a.ma-course-link").get_attribute("href")) for c in native.all()]
 assert len(set(x[1] for x in home_cards))==6,(loc,"duplicate card destination")
 # Academy provides the source of both actual HTML and interaction styles.
 if width==1440:
  first=native.first
  first.hover()
  page.wait_for_timeout(400)
  assert first.evaluate("(el)=>getComputedStyle(el).transform")!="none",(loc,"Academy hover lift missing")
  shine=first.locator(".ma-course-art")
  assert shine.evaluate("(el)=>getComputedStyle(el,'::after').backgroundImage")!="none",(loc,"Academy shine missing")
 assert page.locator(".rail").count()==1 and page.locator(".topbar").count()==1
 assert page.locator("footer.site-footer").count()==1
 assert page.locator(".topbar .top-label").inner_text()==LABEL[loc]
 assert page.locator("h1").evaluate("(el)=>getComputedStyle(el).visibility")=="visible"
 assert page.evaluate("document.documentElement.scrollWidth<=window.innerWidth+2"),(loc,width,"horizontal overflow")
 assert page.locator(".ma-v2-courses .ma-course-card").first.evaluate("(el)=>getComputedStyle(el).display")!="none"
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
 if width==1440:
  academy_cards=[(c.locator("h3").inner_text(),c.locator("a.ma-course-link").get_attribute("href"))
    for c in page.locator('[data-ma-course-card="1"]').all()]
  assert academy_cards==home_cards,(loc,"Home and Academy no longer share the same six titles and routes")

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
   assert page.locator(".ma-v2-flap-left").evaluate(
    "(e)=>getComputedStyle(e).animationName")=="none"
   assert page.locator(".ma-v2-artifacts").evaluate(
    "(e)=>Number(getComputedStyle(e).opacity)>.95"),(lang,"reduced-motion symbols must remain visible")
   assert page.locator(".ma-v2-flap-left").evaluate(
    "(e)=>new DOMMatrix(getComputedStyle(e).transform).m41 < -85"),(lang,"reduced-motion lid not open")
   page.close()
   page=browser.new_page(viewport={"width":375,"height":812},java_script_enabled=False)
   page.goto(BASE+"/"+lang+"/",wait_until="domcontentloaded")
   assert page.locator('[data-ma-v2-section]').count()==5
   assert page.locator(".ma-v2-motion-toggle").is_hidden()
   assert page.locator(".ma-v2-courses .ma-course-card").count()==6
   page.close()
  browser.close()
 print("PASS staged Home V2: five sections x three locales x three widths, tablet/mobile, motion and no-JS")

if __name__=="__main__":
 main()
