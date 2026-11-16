#!/usr/bin/env python3
"""MANZO AI My Learning: browser E2E against an isolated fake SDK/API.

NO real Supabase network, no actual invitations, no database writes.
The production feature flag is OFF; this tests both honest pending state
and the future read-only UI after a separately authorized backend rollout.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json

REF="https://bjydnaejpxwubmxpnpnv.supabase.co/functions/v1/learning-api/"
ORGS=[
 {"organizationId":"aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa","name":"Team A — QA only","role":"learner"},
 {"organizationId":"bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb","name":"Team B — QA only","role":"learner"},
]
COURSE_A="cccccccc-cccc-4ccc-8ccc-cccccccccccc"
COURSE_B="dddddddd-dddd-4ddd-8ddd-dddddddddddd"
LOCALES={
 "it":"it/prodotto/learning-b2b/mio-percorso",
 "en":"en/product/learning-b2b/my-learning",
 "es":"es/producto/learning-b2b/mi-aprendizaje",
}
OUT=Path("auth-review-screenshots")
def reply(route,body,status=200):
 route.fulfill(status=status,content_type="application/json",body=json.dumps(body))
def backend(route):
 url=route.request.url
 assert route.request.headers.get("authorization")=="Bearer test-jwt-isolated-only"
 assert route.request.headers.get("apikey","").startswith("sb_publishable_")
 if url.endswith("/v1/learning/organizations"):
  return reply(route,{"organizations":ORGS})
 if "/aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa/" in url:
  course=COURSE_A
  if url.endswith("/courses"):
   return reply(route,{"courses":[{"id":course,"title":"Engineering Assurance nel coding","status":"published"}]})
  if url.endswith("/enrollments"):
   return reply(route,{"enrollments":[{"courseId":course,"status":"active"}]})
  if url.endswith("/progress"):
   return reply(route,{"progress":[{"courseId":course,"moduleKey":"intro"},{"courseId":course,"moduleKey":"intro"},{"courseId":course,"moduleKey":"practice"}]})
 if "/bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb/" in url:
  course=COURSE_B
  if url.endswith("/courses"):
   return reply(route,{"courses":[{"id":course,"title":"<img src=x onerror=alert(1)>","status":"published"}]})
  if url.endswith("/enrollments"):
   return reply(route,{"enrollments":[{"courseId":course,"status":"active"}]})
  if url.endswith("/progress"):
   return reply(route,{"progress":[]})
 return reply(route,{"code":"not_found"},404)

def verify_page(page,locale,route,width):
 page.set_viewport_size({"width":width,"height":860 if width<500 else 900})
 errors=[]
 page.on("pageerror",lambda error:errors.append(str(error)))
 page.route(REF+"**",backend)
 response=page.goto("http://127.0.0.1:8769/manzo-ai/"+route+"/",wait_until="networkidle")
 assert response and response.status==200
 assert page.locator('[data-manzo-workspace="v1"]').count()==1
 assert page.locator("#mw-courses article").count()==1
 assert page.locator("#mw-courses h3").inner_text()=="Engineering Assurance nel coding"
 assert "2" in page.locator("#mw-courses .mw-course-progress").inner_text()
 assert len(page.locator("#mw-organizations button").all())==2
 assert page.locator('[aria-pressed="true"]').count()==1
 # Selecting another real organization changes the data, not an invented metric.
 page.locator("#mw-organizations button").nth(1).click()
 page.wait_for_function('document.querySelector("#mw-courses h3")?.textContent.includes("<img src=x")')
 assert page.locator("#mw-courses img").count()==0, "Untrusted title executed as HTML"
 assert page.locator("#mw-courses h3").inner_text()=="<img src=x onerror=alert(1)>"
 assert page.locator("#mw-courses .mw-course-progress").inner_text().startswith("0 ")
 assert not page.evaluate("document.documentElement.scrollWidth > innerWidth + 3")
 assert not errors,errors
 OUT.mkdir(exist_ok=True)
 page.screenshot(path=str(OUT/f"my-learning-{locale}-{width}.png"),full_page=True)

def main():
 with sync_playwright() as p:
  browser=p.chromium.launch()
  for loc,route in LOCALES.items():
   # The actual published workspace is deliberately fail-closed: no API.
   page=browser.new_page(viewport={"width":1440,"height":900})
   calls=[]
   page.on("request",lambda req: calls.append(req.url) if "/functions/v1/learning-api/" in req.url else None)
   page.goto("http://127.0.0.1:8768/manzo-ai/"+route+"/",wait_until="networkidle")
   assert page.locator("#mw-courses article").count()==0
   assert not calls,"Disabled pilot must never call the Learning API"
   page.close()
   for width in (1440,390):
    page=browser.new_page()
    verify_page(page,loc,route,width)
    page.close()
  browser.close()
 print("PASS: My Learning IT/EN/ES, 2 sizes, real-response UX, tenant switch, no XSS, no fake metrics, production API flag OFF")
if __name__=="__main__":main()
