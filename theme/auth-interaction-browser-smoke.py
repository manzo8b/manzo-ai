#!/usr/bin/env python3
"""QA-only end-to-end form interaction regression.

The served bundle replaces only the Supabase SDK with a deterministic test
double. This never sends a request to the live Supabase project. The test
must catch the browser bug where SubmitEvent.currentTarget is null AFTER await.
"""
from pathlib import Path
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

BASE="http://127.0.0.1:8767/manzo-ai/"
ROUTES={
 "it":"it/prodotto/learning-b2b/accesso/",
 "en":"en/product/learning-b2b/sign-in/",
 "es":"es/producto/learning-b2b/acceso/",
}

def visible(page,selector):
 assert page.locator(selector).is_visible(),(page.url,selector,page.locator("body").get_attribute("data-view"))

with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,args=["--no-sandbox"])
 count=0
 for lang,path in ROUTES.items():
  for width in (1440,390):
   ctx=browser.new_context(viewport={"width":width,"height":900 if width==1440 else 844})
   page=ctx.new_page()
   errors=[]
   remotes=[]
   page.on("pageerror",lambda err:errors.append(str(err)))
   page.on("request",lambda req:remotes.append(req.url) if "supabase.co" in req.url else None)
   page.goto(urljoin(BASE,path),wait_until="load")
   page.locator("#auth-signin").wait_for(state="visible")
   # Recovery success: exercise an actual async handler and confirm form.clear.
   page.locator("#auth-forgot").click()
   visible(page,"#auth-recover")
   page.locator("#auth-recover-email").fill("student@example.invalid")
   page.locator('#auth-recover-form button[type=submit]').click()
   page.wait_for_function('document.querySelector("#auth-recover-email").value === ""',timeout=4000)
   status=page.locator("#auth-status")
   assert status.get_attribute("data-level")=="info",(lang,width,"recovery failed",status.inner_text())
   assert status.inner_text().strip() and "Operazione non riuscita" not in status.inner_text()
   page.locator("[data-auth-back]").first.click()
   visible(page,"#auth-signin")
   # Sign-in success must NOT throw while attempting to reset the old form.
   page.locator("#auth-email").fill("student@example.invalid")
   page.locator("#auth-password").fill("demo-password")
   page.locator('#auth-signin-form button[type=submit]').click()
   page.locator("#auth-verified").wait_for(state="visible",timeout=4000)
   assert page.locator("#auth-email").input_value()=="",(lang,width,"login form not cleared")
   assert status.get_attribute("data-level")=="info",(lang,width,"sign-in failure",status.inner_text())
   assert page.locator("#auth-user-email").inner_text()=="student@example.invalid"
   # Known rejection: retain verified screen on weak password (no false success).
   page.locator("#auth-open-update").click()
   visible(page,"#auth-update")
   page.locator("#auth-new-password").fill("bad-password!")
   page.locator('#auth-update-form button[type=submit]').click()
   page.wait_for_function('document.querySelector("#auth-status").dataset.level==="error"',timeout=4000)
   assert page.locator("#auth-update").is_visible()
   # Success must clear the field, show success and keep the session valid.
   page.locator("#auth-new-password").fill("safe-password-2026!")
   page.locator('#auth-update-form button[type=submit]').click()
   page.locator("#auth-verified").wait_for(state="visible",timeout=4000)
   assert page.locator("#auth-new-password").input_value()=="",(lang,width,"password form not cleared")
   assert status.get_attribute("data-level")=="info",(lang,width,"update failure",status.inner_text())
   assert status.inner_text().strip()
   # Logout must not be conflated with a successful password change.
   page.locator("#auth-signout").click()
   page.locator("#auth-signin").wait_for(state="visible",timeout=4000)
   assert status.get_attribute("data-level")=="info"
   assert not remotes,(lang,width,"unexpected Supabase network call",remotes)
   assert not errors,(lang,width,"JS runtime errors",errors)
   count+=1
   print(f"PASS Auth E2E mocked {lang}/{width}: reset, sign-in, weak password, update and sign-out")
   ctx.close()
 browser.close()
assert count==6
print(f"PASS: {count} end-to-end browser tests with mocked Auth, zero production API calls")
