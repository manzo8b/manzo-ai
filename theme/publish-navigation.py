#!/usr/bin/env python3
"""Add mobile navigation assets to the final MANZO AI GitHub Pages build.
The original ZIP remains immutable; work after editorial and SEO overlays.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import shutil

CLOSE = re.compile(r"</head\s*>", re.IGNORECASE)
MARKER = 'data-manzo-nav-overlay="1"'

def publish(site: Path, theme: Path, verify_only: bool = False):
    assets = site / 'assets'
    css = theme / 'mobile-nav.css'
    js = theme / 'mobile-nav.js'
    if not css.is_file() or not js.is_file():
        raise RuntimeError('Missing navigation assets')
    if not verify_only:
        assets.mkdir(parents=True, exist_ok=True)
        shutil.copy2(css, assets/css.name)
        shutil.copy2(js, assets/js.name)
    for filename, source in [('mobile-nav.css',css),('mobile-nav.js',js)]:
        dest=assets/filename
        if not dest.is_file() or dest.read_bytes()!=source.read_bytes():
            raise RuntimeError(f'Navigation asset mismatch: {filename}')
    revision=hashlib.sha256(css.read_bytes()+js.read_bytes()).hexdigest()[:12]
    tag=(f'<link data-manzo-nav-overlay="1" rel="stylesheet" '
         f'href="/manzo-ai/assets/mobile-nav.css?v={revision}">'
         f'<script src="/manzo-ai/assets/mobile-nav.js?v={revision}" defer></script>')
    pages=sorted(site.rglob('index.html'))
    if len(pages)<82:
        raise RuntimeError(f'Incomplete MANZO AI site: {len(pages)} HTML pages')
    for page in pages:
        html=page.read_text(encoding='utf-8')
        if verify_only:
            if html.count(MARKER)!=1 or f'mobile-nav.js?v={revision}' not in html:
                raise RuntimeError(f'Mobile navigation missing/duplicated: {page}')
            continue
        if MARKER in html:
            raise RuntimeError(f'Duplicate mobile enhancement: {page}')
        closing=CLOSE.search(html)
        if not closing:
            raise RuntimeError(f'HTML head missing: {page}')
        html=html[:closing.start()]+tag+html[closing.start():]
        page.write_text(html,encoding='utf-8')
    for rel in ('index.html','it/index.html','es/index.html','en/index.html',
                'it/academy/index.html','it/risorse/index.html',
                'it/video-e-slide/prompt-engineering/index.html'):
        if not (site/rel).is_file():
            raise RuntimeError('Required navigation page missing: '+rel)
    print(f'MANZO AI navigation: {len(pages)} HTML pages, portal /manzo-ai/, IT/ES/EN, verified={verify_only}')

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--site',required=True,type=Path)
    p.add_argument('--theme',default=Path(__file__).resolve().parent,type=Path)
    p.add_argument('--verify-only',action='store_true')
    a=p.parse_args()
    publish(a.site,a.theme,a.verify_only)
