#!/usr/bin/env python3
"""Live PILOT page browser smoke, with no users, credentials or remote Auth calls.

Exercise only the rendered sign-in and privacy UI. Real invitation and recovery
must be verified by the owner with a preauthorized email and client acceptance.
"""
from pathlib import Path
from urllib.parse import urljoin
import json
from playwright.sync_api import sync_playwright

BASE="http://127.0.0.1:8766/manzo-ai/"
ROUTES={
 "it":("it/prodotto/learning-b2b/accesso/","it/prodotto/learning-b2b/privacy/"),
 "en":("en/product/learning-b2b/sign-in/","en/product/learning-b2b/privacy/"),
 "es":("es/producto/learning-b2b/acceso/","es/producto/learning-b2b/privacidad/"),
}
COUNT=0
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,args=["--no-sandbox"])
 for locale,(access,privacy) in ROUTES.items():
  for width in (1440,390):
   page=browser.new_page(viewport={"width":width,"height":900 if width==1440 else 844},is_mobile=(width==390))
   errors=[]
   remote=[]
   page.on("pageerror",lambda err:errors.append(str(err)))
   page.on("request",lambda req:remote.append(req.url) if "supabase.co" in req.url else None)
   page.route("**/*.supabase.co/**",lambda request:request.abort())
   page.goto(urljoin(BASE,access),wait_until="load",timeout=35000)
   try:
    page.locator("#auth-signin").wait_for(state="visible",timeout=9000)
   except Exception:
    print("AUTH_DIAGNOSTIC",{
      "locale":locale,"width":width,
      "view":page.locator('body').get_attribute('data-view'),
      "messages":page.locator('#auth-status').inner_text(),
      "config_enabled":json.loads(page.locator('#auth-config').text_content()).get("enabled"),
      "script_present":page.locator('script[src*="auth-app"]').count(),
      "errors":errors,
      "console_problems":page.evaluate("window.__AUTH_TEST_ERRORS || []"),
    },flush=True)
    raise
   assert page.locator("#auth-disabled").is_hidden(),(locale,width,"disabled")
   cfg=json.loads(page.locator("#auth-config").text_content())
   assert cfg["enabled"] is True and cfg["authMode"]=="invite-only"
   assert cfg["requireEmailVerification"] is True
   assert page.locator("#auth-signin-form input[name=email]").is_visible()
   assert page.locator("#auth-signin-form input[name=password]").is_visible()
   assert page.locator('a[href="/manzo-ai/'+privacy+'"]').count()==1
   # There must be NO public sign-up UI or buttons.
   assert page.locator('[data-auth-signup],#auth-signup-form').count()==0
   page.locator("#auth-forgot").click()
   assert page.locator("#auth-recover").is_visible()
   page.locator('[data-auth-back]').first.click()
   assert page.locator("#auth-signin").is_visible()
   assert page.evaluate('sessionStorage.length')==0
   assert not remote,(locale,width,"unexpected live Supabase request",remote)
   assert not errors,(locale,width,errors)
   response=page.goto(urljoin(BASE,privacy),wait_until="load")
   assert response.status==200,(locale,width,response.status)
   assert page.locator('body[data-manzo-auth-privacy="v1"]').count()==1
   assert page.locator('meta[name=robots]').get_attribute('content').startswith('noindex')
   assert page.locator('a[href="mailto:marcelo2020.it@gmail.com"]').count()==1
   assert page.locator('.privacy-section').count()>=7
   for h in page.locator('h1,h2,h3').all():
    assert not h.inner_text().strip().endswith('.'),(locale,width,h.inner_text())
   assert page.evaluate('document.documentElement.scrollWidth-window.innerWidth')<=4
   if locale=="it":
    folder=Path('auth-review-screenshots')
    folder.mkdir(exist_ok=True)
    page.goto(urljoin(BASE,access),wait_until="load")
    page.locator("#auth-signin").wait_for(state="visible")
    page.screenshot(path=str(folder/f"live-invite-only-signin-{width}.png"),full_page=False,animations="disabled")
   page.close()
   COUNT+=1
 browser.close()
assert COUNT==6
print(f"PASS MANZO AI invite-only pilot: {COUNT} IT/EN/ES desktop+mobile, usable login forms, privacy notices and zero external Auth calls")
