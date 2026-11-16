#!/usr/bin/env python3
"""Publish MANZO AI My Learning behind verified invite-only Auth.

The workspace is read-only and truly data-backed ONLY after a separate
authenticated Edge API release gate. No fake students, courses, progress,
certificates, database writes, or untrusted redirects.
Runs after publish-auth-staging.py (which is already the private pilot).
"""
from __future__ import annotations
import argparse
from html import escape
import json
import os
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parent.parent
SOURCE=ROOT/"product"/"auth-staging"
BASE="/manzo-ai/"
API_PROJECT="https://bjydnaejpxwubmxpnpnv.supabase.co"
ROUTES={
 "it":"it/prodotto/learning-b2b/mio-percorso",
 "en":"en/product/learning-b2b/my-learning",
 "es":"es/producto/learning-b2b/mi-aprendizaje",
}
ACCESS={
 "it":"it/prodotto/learning-b2b/accesso",
 "en":"en/product/learning-b2b/sign-in",
 "es":"es/producto/learning-b2b/acceso",
}
LANG={
 "it":{
  "title":"Il mio percorso","hero":"La formazione prende forma",
  "lead":"Corsi assegnati, attività realmente completate e un ambiente di studio che rispetta la tua identità",
  "pilot":"SPAZIO PERSONALE / PILOTA","login":"Accedi con il tuo account",
  "back":"Esplora l’Academy","signout":"Esci","assigned":"I miei corsi",
  "assignedLead":"Contenuti e attività disponibili soltanto in base alle iscrizioni effettive e alle autorizzazioni del tuo account",
  "verifiedAccount":"Account verificato","signInRequired":"Accedi con un account invitato e verificato per visualizzare i corsi",
  "pending":"La lettura dei progressi è in preparazione: l'API protetta non è ancora attiva. Nessun corso o risultato è simulato",
  "verifying":"Verifica della sessione Supabase","loadingOrganizations":"Ricerca delle tue organizzazioni",
  "noOrganization":"Non risulti ancora assegnato a un'organizzazione di formazione",
  "loadingCourses":"Caricamento dei corsi effettivamente assegnati",
  "noCourses":"Non risultano corsi pubblicati e assegnati al tuo account",
  "coursesLoaded":"Dati aggiornati dalla piattaforma di apprendimento",
  "sessionExpired":"La sessione non è valida o è scaduta. Accedi nuovamente",
  "accessDenied":"Non sei autorizzato a consultare questi dati",
  "rateLimited":"Troppe richieste. Riprova più tardi",
  "unavailable":"L'API Learning non è disponibile",
  "error":"I dati non possono essere caricati. Non è stato mostrato alcun progresso fittizio",
  "assignedCourse":"Corso assegnato","active":"In corso","completed":"Completato",
  "modulesCompleted":"moduli completati","noCertificate":"Non è prevista alcuna certificazione accreditata",
  "how1":"Accesso verificato","how1Text":"I dati appartengono soltanto all'account autenticato",
  "how2":"Progressi documentati","how2Text":"Le unità vengono mostrate soltanto quando registrate nel backend",
  "how3":"Controllo degli accessi","how3Text":"Ruoli, organizzazioni e iscrizioni vengono verificati dal server",
 },
 "en":{
  "title":"My Learning","hero":"Make your learning count",
  "lead":"Assigned courses, actually completed activities and a learning environment linked to your verified account",
  "pilot":"PERSONAL WORKSPACE / PILOT","login":"Sign in to your account",
  "back":"Explore the Academy","signout":"Sign out","assigned":"My courses",
  "assignedLead":"Content and learning activity are available only when backed by a real enrollment and verified access",
  "verifiedAccount":"Verified account","signInRequired":"Sign in with a verified invited account to view assigned courses",
  "pending":"Progress tracking is being prepared: the protected API is not active yet. No courses or outcomes are simulated",
  "verifying":"Verifying your Supabase session","loadingOrganizations":"Loading your organizations",
  "noOrganization":"You have not yet been assigned to a learning organization",
  "loadingCourses":"Loading courses actually assigned to you",
  "noCourses":"No published courses are currently assigned to your account",
  "coursesLoaded":"Data refreshed from the Learning platform",
  "sessionExpired":"Your session has expired or is invalid. Sign in again",
  "accessDenied":"You are not authorized to access these records",
  "rateLimited":"Too many requests. Try again later",
  "unavailable":"The Learning API is unavailable",
  "error":"Learning data could not be loaded. No fictional progress has been displayed",
  "assignedCourse":"Assigned course","active":"In progress","completed":"Completed",
  "modulesCompleted":"modules completed","noCertificate":"No accredited certification is provided",
  "how1":"Verified access","how1Text":"Records belong only to the authenticated account",
  "how2":"Evidence-backed progress","how2Text":"Completed units appear only after a backend record exists",
  "how3":"Protected records","how3Text":"Roles, organizations and enrollments are checked by the server",
 },
 "es":{
  "title":"Mi aprendizaje","hero":"Tu aprendizaje cobra forma",
  "lead":"Cursos asignados, actividades realmente completadas y un entorno vinculado a tu cuenta verificada",
  "pilot":"ESPACIO PERSONAL / PILOTO","login":"Accede con tu cuenta",
  "back":"Explorar la Academia","signout":"Cerrar sesión","assigned":"Mis cursos",
  "assignedLead":"Los contenidos y resultados dependen exclusivamente de inscripciones y permisos reales de tu cuenta",
  "verifiedAccount":"Cuenta verificada","signInRequired":"Accede con una cuenta invitada y verificada para ver tus cursos",
  "pending":"El seguimiento de progresos se está preparando: la API protegida aún no está activa. No se simulan cursos ni resultados",
  "verifying":"Verificando tu sesión Supabase","loadingOrganizations":"Cargando tus organizaciones",
  "noOrganization":"Todavía no estás asignado a una organización formativa",
  "loadingCourses":"Cargando los cursos realmente asignados",
  "noCourses":"No hay cursos publicados asignados a tu cuenta",
  "coursesLoaded":"Información actualizada desde la plataforma",
  "sessionExpired":"La sesión ha caducado o no es válida. Accede de nuevo",
  "accessDenied":"No tienes autorización para consultar estos datos",
  "rateLimited":"Demasiadas solicitudes. Inténtalo más tarde",
  "unavailable":"La API Learning no está disponible",
  "error":"No se pueden cargar los datos. No se muestran progresos simulados",
  "assignedCourse":"Curso asignado","active":"En curso","completed":"Completado",
  "modulesCompleted":"módulos completados","noCertificate":"No se ofrece certificación acreditada",
  "how1":"Acceso verificado","how1Text":"Los datos corresponden únicamente a la cuenta autenticada",
  "how2":"Progresos con evidencia","how2Text":"Las unidades aparecen al registrarse realmente en el backend",
  "how3":"Datos protegidos","how3Text":"Los roles, organizaciones y matrículas se verifican en el servidor",
 }
}
ACADEMY={"it":"it/academy","en":"en/academy","es":"es/academia"}
def e(s):return escape(str(s),quote=True)
def safe_json(v):return json.dumps(v,ensure_ascii=False,separators=(",",":")).replace("<","\\u003c").replace(">","\\u003e").replace("&","\\u0026")
def render(loc,enabled,api_enabled):
 t=LANG[loc]
 config=json.loads((SOURCE/"config.json").read_text(encoding="utf-8"))
 config={key:value for key,value in config.items() if key!="note"}
 config["enabled"]=bool(enabled)
 config["workspaceApiEnabled"]=bool(api_enabled)
 links="".join('<a href="'+BASE+ROUTES[lang]+'/" hreflang="'+lang+'" lang="'+lang+'"'
  +(' aria-current="page"' if lang==loc else '')+'>'+lang.upper()+'</a>' for lang in LANG)
 csp=("default-src 'none';base-uri 'none';form-action 'none';script-src 'self';"
      "style-src 'self';img-src 'self' data:;"
      "connect-src "+API_PROJECT+";"
      "object-src 'none';upgrade-insecure-requests")
 signin=BASE+ACCESS[loc]+"/"
 return f'''<!doctype html><html lang="{loc}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive">
<meta name="referrer" content="no-referrer">
<meta http-equiv="Content-Security-Policy" content="{e(csp)}">
<meta name="theme-color" content="#ffffff">
<title>MANZO AI | {e(t["title"])}</title>
<link rel="stylesheet" href="{BASE}assets/auth/workspace.css">
<script defer src="{BASE}assets/auth/workspace.js"></script></head>
<body data-manzo-workspace="v1" data-locale="{loc}">
<a class="mw-skip" href="#mw-main">{e(t["assigned"])}</a>
<header class="mw-header"><div class="mw-shell mw-header-inner">
<a class="mw-logo" href="{BASE}{loc}/">MANZO <strong>AI</strong><span>LEARNING</span></a>
<nav class="mw-langs" aria-label="Languages">{links}</nav></div></header>
<main id="mw-main" class="mw-main"><div class="mw-shell">
<section class="mw-hero" aria-labelledby="mw-title">
<p class="mw-overline">{e(t["pilot"])}</p>
<h1 id="mw-title">{e(t["hero"])}</h1>
<p class="mw-lead">{e(t["lead"])}</p>
<div class="mw-hero-actions">
<a class="mw-button mw-button-primary" id="mw-signin" href="{signin}">{e(t["login"])} ↗</a>
<button class="mw-button" id="mw-signout" type="button" hidden>{e(t["signout"])}</button>
<a class="mw-button" href="{BASE}{ACADEMY[loc]}/">{e(t["back"])} ↗</a>
</div>
<p id="mw-identity" class="mw-identity"></p>
</section>
<section class="mw-data-panel" aria-labelledby="mw-section-title">
<div class="mw-data-header">
<small>MANZO AI / LEARNING B2B</small>
<h2 id="mw-section-title">{e(t["assigned"])}</h2>
<p>{e(t["assignedLead"])}</p>
</div>
<div class="mw-panel-content">
<div id="mw-organizations" class="mw-organizations" role="group" aria-label="Organization"></div>
<p id="mw-org-label" class="mw-identity"></p>
<div id="mw-status" class="mw-status" role="status" aria-live="polite">{e(t["verifying"])}</div>
<div id="mw-courses" class="mw-course-grid" aria-live="polite"></div>
</div></section>
<section class="mw-method">
<article><strong>{e(t["how1"])}</strong><p>{e(t["how1Text"])}</p></article>
<article><strong>{e(t["how2"])}</strong><p>{e(t["how2Text"])}</p></article>
<article><strong>{e(t["how3"])}</strong><p>{e(t["how3Text"])}</p></article>
</section></div></main>
<footer class="mw-footer"><div class="mw-shell">
MANZO AI · Learning B2B · {e(t["pilot"])}
</div></footer>
<script type="application/json" id="workspace-i18n">{safe_json(t)}</script>
<script type="application/json" id="workspace-config">{safe_json(config)}</script>
</body></html>'''
def publish(site,verify_only=False,live_auth=False,qa_api=False):
 if live_auth and os.getenv("MANZO_AUTH_PILOT_RELEASE")!="restricted-invite-only":
  raise RuntimeError("Live workspace requires restricted Auth staging gate")
 if qa_api and (os.getenv("MANZO_WORKSPACE_QA_MODE")!="isolated-test-only" or not live_auth):
  raise RuntimeError("API simulation may run only in isolated Auth QA")
 if not verify_only:
  assets=site/"assets"/"auth"
  assets.mkdir(parents=True,exist_ok=True)
  for name in ("workspace.css","workspace.js"):
   src=(SOURCE/name if name.endswith("css") else SOURCE/"dist"/name)
   if not src.is_file():raise RuntimeError("Build Auth workspace bundle first: "+name)
   shutil.copyfile(src,assets/name)
  for loc,route in ROUTES.items():
   target=site/route/"index.html"
   target.parent.mkdir(parents=True,exist_ok=True)
   target.write_text(render(loc,live_auth,qa_api),encoding="utf-8")
   auth_page=site/ACCESS[loc]/"index.html"
   source=auth_page.read_text(encoding="utf-8")
   marker='data-manzo-workspace-link="v1"'
   if marker in source:raise RuntimeError("Duplicate workspace CTA")
   anchor='<button type="button" class="button" id="auth-signout">'
   if anchor not in source:raise RuntimeError("Missing authorized signout area")
   cta=(f'<a {marker} class="button" href="{BASE}{route}/">'
         f'{e(LANG[loc]["title"])} ↗</a>')
   auth_page.write_text(source.replace(anchor,cta+"\n    "+anchor,1),encoding="utf-8")
 for loc,route in ROUTES.items():
  page=site/route/"index.html"
  html=page.read_text(encoding="utf-8")
  if html.count('data-manzo-workspace="v1"')!=1:raise RuntimeError("Workspace page absent")
  if html.count('noindex,nofollow,noarchive')!=1:raise RuntimeError("Workspace indexed")
  if '"workspaceApiEnabled":'+("true" if qa_api else "false") not in html:
   raise RuntimeError("Backend gate unexpectedly enabled")
  if '"enabled":'+("true" if live_auth else "false") not in html:
   raise RuntimeError("Auth pilot mode mismatch")
  for id_ in ("mw-signout","mw-status","mw-courses","mw-organizations","workspace-config"):
   if id_ not in html:raise RuntimeError("Missing component "+id_)
  auth=site/ACCESS[loc]/"index.html"
  if auth.read_text(encoding="utf-8").count('data-manzo-workspace-link="v1"')!=1:
   raise RuntimeError("Authorized CTA absent")
 for name in ("workspace.css","workspace.js"):
  if not (site/"assets"/"auth"/name).is_file():raise RuntimeError("Workspace asset missing")
 print("PASS: 3 private read-only My Learning pages; API="+str(qa_api)+"; Auth="+str(live_auth)+", verified="+str(verify_only))
if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("--site",required=True,type=Path)
 p.add_argument("--verify-only",action="store_true")
 p.add_argument("--live-auth",action="store_true")
 p.add_argument("--qa-api-only",action="store_true")
 a=p.parse_args()
 publish(a.site,a.verify_only,a.live_auth,a.qa_api_only)
