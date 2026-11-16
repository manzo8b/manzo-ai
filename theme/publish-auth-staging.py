#!/usr/bin/env python3
"""MANZO AI Learning B2B · private, unlinked Auth preview.

Build only by explicitly passing --enable on a QA-only site directory.
Never called in GitHub Pages public deployment until Auth, redirects,
privacy, real verified invitations and the backend's tenant gates pass.
"""
from __future__ import annotations
import argparse
from html import escape
import json
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parent.parent
SOURCE=ROOT/'product'/'auth-staging'
BASE='/manzo-ai/'
ORIGIN='https://manzo8b.github.io'
ROUTES={
 'it':'it/prodotto/learning-b2b/accesso',
 'en':'en/product/learning-b2b/sign-in',
 'es':'es/producto/learning-b2b/acceso',
}
PRODUCT={'it':'it/prodotto','en':'en/product','es':'es/producto'}
MARKER='data-manzo-auth="v1"'

def e(value):return escape(str(value),quote=True)
def safe_json(value):
 return json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')

def view_header(view,heading):
 return f'<h2 id="auth-{view}-title">{e(str(heading).rstrip(". "))}</h2>'

def render(loc,text,settings):
 route=ROUTES[loc]+'/'
 parent=BASE+PRODUCT[loc]+'/'
 config={key:value for key,value in settings.items() if key!='note'}
 config['callback']=ORIGIN+BASE+route
 assert config['enabled'] is False,'No live authentication without explicit release gate'
 assert config['authMode']=='invite-only' and config['requireEmailVerification'] is True
 links=''.join(f'<a href="{BASE}{p}/" hreflang="{l}" lang="{l}"'
               +(' aria-current="page"' if l==loc else '')+f'>{l.upper()}</a>'
               for l,p in ROUTES.items())
 csp=("default-src 'none'; base-uri 'none'; form-action 'self'; "
      "script-src 'self'; style-src 'self'; img-src 'self' data:; "
      "connect-src https://bjydnaejpxwubmxpnpnv.supabase.co; "
      "object-src 'none'; upgrade-insecure-requests")
 return f'''<!doctype html>
<html lang="{loc}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive">
<meta name="referrer" content="no-referrer">
<meta http-equiv="Content-Security-Policy" content="{e(csp)}">
<meta name="theme-color" content="#ffffff">
<title>MANZO AI | {e(text['pageTitle'])}</title>
<link rel="stylesheet" href="{BASE}assets/auth/auth.css">
<script defer src="{BASE}assets/auth/auth-app.js"></script>
</head>
<body {MARKER} data-locale="{loc}" data-view="disabled">
<a class="skip" href="#auth-main">Skip to content / Vai al contenuto</a>
<header class="masthead"><div class="shell">
 <a class="logo" href="{parent}">MANZO <span>AI</span><small>{e(text['brand'])}</small></a>
 <nav class="langs" aria-label="Languages">{links}</nav>
</div></header>
<main id="auth-main" class="main"><div class="shell">
 <div class="grid">
  <div class="intro">
   <p class="eyebrow">{e(text['kicker'])}</p>
   <h1>{e(text['hero'])}</h1>
   <p class="lead">{e(text['subtitle'])}</p>
   <a class="back" href="{parent}">{e(text['back'])} <span aria-hidden="true">↗</span></a>
   <div class="features">
    <article class="feature"><strong>{e(text['private'])}</strong><p>{e(text['privateText'])}</p></article>
    <article class="feature"><strong>{e(text['clear'])}</strong><p>{e(text['clearText'])}</p></article>
   </div>
  </div>
  <div class="card">
   <div class="card-top"><span class="card-brand">MANZO AI / {e(text['brand'])}</span>
    <span class="tag">{e(text['private'])}</span></div>
   <p id="auth-view-title" class="auth-title-fallback"></p>
   <section class="view" id="auth-disabled">
    {view_header('disabled',text['disabledTitle'])}
    <p class="auth-info">{e(text['disabled'])}</p>
   </section>
   <section class="view" id="auth-pending" hidden>
    {view_header('pending',text['loading'])}
    <p class="auth-info">{e(text['loading'])}</p>
   </section>
   <section class="view" id="auth-signin" hidden>
    {view_header('signin',text['pageTitle'])}
    <p class="view-lead">{e(text['privateText'])}</p>
    <form id="auth-signin-form" autocomplete="on">
     <div class="field"><label for="auth-email">{e(text['email'])}</label>
      <input id="auth-email" name="email" type="email" autocomplete="username"
      spellcheck="false" inputmode="email" required maxlength="254"></div>
     <div class="field"><label for="auth-password">{e(text['password'])}</label>
      <input id="auth-password" name="password" type="password" autocomplete="current-password" required></div>
     <button class="button full" type="submit">{e(text['signIn'])} <span aria-hidden="true">↗</span></button>
    </form>
    <button id="auth-forgot" class="link-button" type="button">{e(text['forgot'])}</button>
   </section>
   <section class="view" id="auth-recover" hidden>
    {view_header('recover',text['resetTitle'])}
    <p class="view-lead">{e(text['resetExplanation'])}</p>
    <form id="auth-recover-form">
     <div class="field"><label for="auth-recover-email">{e(text['email'])}</label>
      <input id="auth-recover-email" name="email" type="email" autocomplete="email"
      spellcheck="false" inputmode="email" required maxlength="254"></div>
     <button class="button full" type="submit">{e(text['sendRecovery'])} <span aria-hidden="true">↗</span></button>
    </form>
    <button class="link-button" data-auth-back="1" type="button">{e(text['backToLogin'])}</button>
   </section>
   <section class="view" id="auth-update" hidden>
    {view_header('update',text['newPasswordTitle'])}
    <p class="view-lead">{e(text['newPasswordHelp'])}</p>
    <form id="auth-update-form">
     <div class="field"><label for="auth-new-password">{e(text['newPassword'])}</label>
      <input id="auth-new-password" name="password" type="password"
      minlength="12" maxlength="128" autocomplete="new-password" required>
      <small>{e(text['passwordHint'])}</small></div>
     <button class="button full" type="submit">{e(text['savePassword'])} <span aria-hidden="true">↗</span></button>
    </form>
    <button class="link-button" data-auth-back="1" type="button">{e(text['backToLogin'])}</button>
   </section>
   <section class="view" id="auth-verified" hidden>
    {view_header('verified',text['waiting'])}
    <div class="identity"><small>{e(text['verified'])}</small>
     <strong id="auth-user-email"></strong></div>
    <p class="view-lead">{e(text['waitingText'])}</p>
    <button type="button" class="button" id="auth-signout">{e(text['signOut'])} <span aria-hidden="true">↗</span></button>
    <button id="auth-open-update" type="button" class="link-button">{e(text['newPasswordTitle'])}</button>
   </section>
   <p id="auth-status" class="message" aria-live="polite" role="status" data-level="info"></p>
   <p class="privacy">{e(text['privacy'])}</p>
  </div>
 </div>
</div></main>
<footer class="footer"><div class="shell"><strong>MANZO AI · {e(text['brand'])}</strong>
 <span>{e(text['footer'])}</span></div></footer>
<script type="application/json" id="auth-locales">{safe_json(text)}</script>
<script type="application/json" id="auth-config">{safe_json(config)}</script>
</body></html>'''

def publish(site:Path,verify_only:bool,enabled:bool):
 if not enabled:raise RuntimeError('Auth publisher requires explicit --enable; public deployment must NOT call it')
 content=json.loads((SOURCE/'content.json').read_text(encoding='utf-8'))
 config=json.loads((SOURCE/'config.json').read_text(encoding='utf-8'))
 if set(content)!=set(ROUTES):raise RuntimeError('Three locales required')
 assets=site/'assets'/'auth'
 if not verify_only:
  assets.mkdir(parents=True,exist_ok=True)
  shutil.copyfile(SOURCE/'auth.css',assets/'auth.css')
  bundle=SOURCE/'dist'/'auth-app.js'
  if not bundle.is_file():raise RuntimeError('Run npm run build in product/auth-staging first')
  shutil.copyfile(bundle,assets/'auth-app.js')
  for locale,path in ROUTES.items():
   page=site/path/'index.html'
   page.parent.mkdir(parents=True,exist_ok=True)
   page.write_text(render(locale,content[locale],config),encoding='utf-8')
 for locale,path in ROUTES.items():
  page=site/path/'index.html'
  if not page.is_file():raise RuntimeError('Missing route '+path)
  html=page.read_text(encoding='utf-8')
  if html.count(MARKER)!=1:raise RuntimeError('Duplicate/missing auth app '+path)
  if html.count('noindex,nofollow')!=1:raise RuntimeError('Auth page indexed '+path)
  if html.count('"enabled":false')!=1:raise RuntimeError('Unexpectedly enabled auth '+path)
  for required in ('auth-signin-form','auth-update-form','auth-recover-form','auth-status',
                   'auth-config','auth-locales','auth-signout','auth-pending'):
   if required not in html:raise RuntimeError('Auth UX missing '+required)
  if html.count('auth-app.js')!=1:raise RuntimeError('Duplicate app bundle '+path)
 for name in ('auth.css','auth-app.js'):
  if not (assets/name).is_file():raise RuntimeError('Missing asset '+name)
 print(f'PASS: 3 unlinked invite-only Auth staging pages, all disabled, all noindex; verify_only={verify_only}')

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--site',required=True,type=Path)
 p.add_argument('--enable',action='store_true')
 p.add_argument('--verify-only',action='store_true')
 a=p.parse_args()
 publish(a.site,a.verify_only,a.enable)
