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
import os
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
PRIVACY={'it':'it/prodotto/learning-b2b/privacy',
         'en':'en/product/learning-b2b/privacy',
         'es':'es/producto/learning-b2b/privacidad'}
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
 assert type(config['enabled']) is bool
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
   <p class="privacy">{e(text['privacy'])} <a href="{BASE}{PRIVACY[loc]}/">{e(text['privacyLink'])}</a></p>
  </div>
 </div>
</div></main>
<footer class="footer"><div class="shell"><strong>MANZO AI · {e(text['brand'])}</strong>
 <span>{e(text['footer'])}</span></div></footer>
<script type="application/json" id="auth-locales">{safe_json(text)}</script>
<script type="application/json" id="auth-config">{safe_json(config)}</script>
</body></html>'''

def render_privacy(loc: str, text: dict, source: dict)->str:
    """Account-only pilot notice; no generated legal assertions or scripts."""
    access=f'{BASE}{ROUTES[loc]}/'
    sections=''.join(
      f'<section class="privacy-section"><h2>{e(title.rstrip(". "))}</h2>'
      f'<p>{e(paragraph)}</p></section>'
      for title,paragraph in source['sections']
    )
    return f'''<!doctype html><html lang="{loc}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive">
<meta name="referrer" content="no-referrer">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'self'; base-uri 'none'; form-action 'none'; object-src 'none'">
<title>MANZO AI | {e(source['title'])}</title>
<link rel="stylesheet" href="{BASE}assets/auth/auth.css">
</head><body data-manzo-auth-privacy="v1">
<header class="masthead"><div class="shell">
<a class="logo" href="{BASE}{loc}/">MANZO <span>AI</span><small>LEARNING B2B</small></a>
<a class="back" href="{access}">{e(source['back'])} <span aria-hidden="true">↗</span></a>
</div></header>
<main class="main"><div class="shell">
<article class="privacy-document">
<p class="eyebrow">MANZO AI / LEARNING B2B</p>
<h1>{e(source['title'].rstrip('. '))}</h1>
<p class="lead">{e(source['lead'])}</p>
<p class="privacy-review">{e(source['review'])}</p>
{sections}
<p class="privacy-contact"><a href="mailto:marcelo2020.it@gmail.com">{e(source['contact'])}</a></p>
<p class="privacy-updated">{e(source['updated'])}</p>
<a class="back" href="{access}">{e(source['back'])} ↗</a>
</article></div></main>
<footer class="footer"><div class="shell">
<a href="{BASE}{loc}/">{e(source['home'])}</a><strong>MANZO AI · LEARNING B2B</strong>
</div></footer>
</body></html>'''

def publish(site:Path,verify_only:bool,enabled:bool,live_auth:bool=False):
 if not enabled:raise RuntimeError('Auth publisher requires explicit --enable')
 if live_auth and os.getenv('MANZO_AUTH_PILOT_RELEASE')!='restricted-invite-only':
  raise RuntimeError('Live Auth publication requires explicit staging release flag')
 content=json.loads((SOURCE/'content.json').read_text(encoding='utf-8'))
 config=json.loads((SOURCE/'config.json').read_text(encoding='utf-8'))
 notices=json.loads((SOURCE/'privacy.json').read_text(encoding='utf-8'))
 config['enabled']=bool(live_auth)
 if config.get('authMode')!='invite-only' or config.get('requireEmailVerification') is not True:
  raise RuntimeError('Incorrect Auth mode; do not publish')
 if set(content)!=set(ROUTES) or set(notices)!=set(ROUTES):
  raise RuntimeError('Three locales and privacy notices required')
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
   privacy_page=site/PRIVACY[locale]/'index.html'
   privacy_page.parent.mkdir(parents=True,exist_ok=True)
   privacy_page.write_text(render_privacy(locale,content[locale],notices[locale]),encoding='utf-8')
 for locale,path in ROUTES.items():
  page=site/path/'index.html'
  if not page.is_file():raise RuntimeError('Missing route '+path)
  html=page.read_text(encoding='utf-8')
  if html.count(MARKER)!=1:raise RuntimeError('Duplicate/missing auth app '+path)
  if html.count('noindex,nofollow')!=1:raise RuntimeError('Auth page indexed '+path)
  expected='"enabled":true' if live_auth else '"enabled":false'
  if html.count(expected)!=1:raise RuntimeError('Unexpected auth activation '+path)
  privacy_path=site/PRIVACY[locale]/'index.html'
  if not privacy_path.is_file():raise RuntimeError('Missing privacy notice '+locale)
  privacy_html=privacy_path.read_text(encoding='utf-8')
  if privacy_html.count('data-manzo-auth-privacy="v1"')!=1 or 'marcelo2020.it@gmail.com' not in privacy_html:
   raise RuntimeError('Invalid account privacy page '+locale)
  if html.count(f'href="{BASE}{PRIVACY[locale]}/"')!=1:
   raise RuntimeError('Access page lacks account privacy link '+locale)
  for required in ('auth-signin-form','auth-update-form','auth-recover-form','auth-status',
                   'auth-config','auth-locales','auth-signout','auth-pending'):
   if required not in html:raise RuntimeError('Auth UX missing '+required)
  if html.count('auth-app.js')!=1:raise RuntimeError('Duplicate app bundle '+path)
 for name in ('auth.css','auth-app.js'):
  if not (assets/name).is_file():raise RuntimeError('Missing asset '+name)
 print(f'PASS: 3 invite-only Auth pages, 3 privacy notices, noindex; live_auth={live_auth}, verified={verify_only}')

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--site',required=True,type=Path)
 p.add_argument('--enable',action='store_true')
 p.add_argument('--verify-only',action='store_true')
 p.add_argument('--live-auth',action='store_true')
 a=p.parse_args()
 publish(a.site,a.verify_only,a.enable,a.live_auth)
