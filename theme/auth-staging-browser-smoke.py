#!/usr/bin/env python3
"""Auth preview browser regression: UI rendered, disabled, no real traffic.

The preview is NOT the live auth app. It must remain unlinked and disabled
until Supabase Auth settings, privacy, invitation and role tests are complete.
"""
from __future__ import annotations
from pathlib import Path
from urllib.parse import urljoin
import json

from playwright.sync_api import sync_playwright

BASE="http://127.0.0.1:8765/manzo-ai/"
ROUTES={
 "it":"it/prodotto/learning-b2b/accesso/",
 "en":"en/product/learning-b2b/sign-in/",
 "es":"es/producto/learning-b2b/acceso/",
}
OUT=Path("auth-review-screenshots")
OUT.mkdir(exist_ok=True)
done=0

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,args=["--no-sandbox"])
 for locale,route in ROUTES.items():
  for width in (1440,390):
   page=browser.new_page(viewport={"width":width,"height":900 if width>390 else 844},
                         is_mobile=width==390,
                         reduced_motion="reduce" if width==390 else "no-preference")
   runtime_errors=[]
   requests=[]
   page.on("pageerror",lambda exc:runtime_errors.append(str(exc)))
   page.on("request",lambda req:requests.append(req.url))
   page.goto(urljoin(BASE,route),wait_until="load",timeout=35000)
   page.wait_for_timeout(250)
   assert page.locator('body[data-manzo-auth="v1"]').count()==1
   assert page.locator("html").get_attribute("lang")==locale
   assert page.locator("meta[name=robots]").get_attribute("content").startswith("noindex,nofollow")
   assert page.locator("#auth-status").inner_text().strip()
   assert page.locator("#auth-disabled").is_visible()
   for view in ("signin","recover","update","verified","pending"):
    assert page.locator("#auth-"+view).is_hidden(),(locale,width,view)
   assert page.locator(".feature").count()==2
   left=page.locator(".feature").first
   assert left.evaluate("(el)=>getComputedStyle(el).backgroundColor")=="rgb(32, 78, 229)"
   assert page.locator(".feature").nth(1).evaluate(
    "(el)=>getComputedStyle(el).backgroundColor")=="rgb(0, 111, 104)"
   assert page.locator(".logo").is_visible()
   cfg=json.loads(page.locator("#auth-config").text_content())
   assert cfg["enabled"] is False
   assert cfg["authMode"]=="invite-only"
   assert cfg["requireEmailVerification"] is True
   assert cfg["callback"].startswith("https://manzo8b.github.io/manzo-ai/")
   assert cfg["publishableKey"].startswith("sb_publishable_")
   assert cfg["projectRef"]=="bjydnaejpxwubmxpnpnv"
   for h in page.locator("h1,h2,h3,h4,h5,h6").all():
    assert not h.inner_text().strip().endswith("."),(locale,width,h.inner_text())
   assert not any("bjydnaejpxwubmxpnpnv.supabase.co" in url for url in requests),(
     locale,width,"unexpected Supabase network request")
   assert not runtime_errors,(locale,width,"JS errors",runtime_errors)
   assert page.evaluate("document.documentElement.scrollWidth-window.innerWidth")<=4,(
     locale,width,"mobile/desktop overflow")
   if width==1440:
    first=left.bounding_box()
    left.hover()
    page.wait_for_timeout(350)
    assert left.evaluate("(el)=>getComputedStyle(el).transform")!="none"
    assert first
   if locale=="it":
    page.screenshot(path=str(OUT/f"login-preview-{width}.png"),full_page=False,animations="disabled")
   print(f"PASS AUTH STAGING {locale}/{width}: no live requests, disabled, 2 vivid cards, verified copy, no title periods.")
   page.close()
   done+=1
 browser.close()
assert done==6
print("PASS Auth staging: six viewport/locale combinations, zero sessions and zero account creation.")
