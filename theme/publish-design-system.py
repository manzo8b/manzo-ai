#!/usr/bin/env python3
"""MANZO AI Precision & Motion: final-layer site-wide design system.

Runs after *all* editorial publishers, SEO and navigation.
Writes only CSS/JS and safe attributes in index.html opening body tags.
Does not change text, SEO, learning activities, data, links or media.
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import re
import shutil
from collections import Counter

ROOT=Path(__file__).resolve().parent
ASSETS=(('design-system.css',ROOT/'design-system.css'),('design-motion.js',ROOT/'design-motion.js'))
HEAD_CLOSE=re.compile(r'</head\s*>',re.I)
BODY_OPEN=re.compile(r'<body\b[^>]*>',re.I|re.S)
MARKER='data-manzo-design="precision-motion-v1"'
PRODUCT={'prodotto','product','producto'}
LEARNING={'academy','academia','impara','learn','aprende','prompt-mastery','slides','diapositivas'}
RESEARCH={'ricerca','research','investigacion','pensiero-critico','critical-thinking','pensamiento-critico','risorse','resources','recursos'}

def surface(page:Path,site:Path)->str:
 parts=page.relative_to(site).parts[:-1]
 if not parts:return 'portal'
 if len(parts)==1 and parts[0] in ('it','en','es'):return 'landing'
 if len(parts)>=2:
  second=parts[1]
  if second in PRODUCT:
   return 'console' if len(parts)>=3 and parts[2]=='learning-b2b' else 'product'
  if second in LEARNING:return 'learning'
  if second in RESEARCH:return 'research'
 return 'general'

def apply(site:Path,verify_only:bool=False)->dict:
 pages=sorted(site.rglob('index.html'))
 if len(pages)<90:
  raise RuntimeError(f'Incomplete MANZO AI site: only {len(pages)} pages')
 assets=site/'assets'
 if not verify_only:
  assets.mkdir(parents=True,exist_ok=True)
  for name,src in ASSETS:
   if not src.is_file():raise RuntimeError('Missing source: '+str(src))
   shutil.copyfile(src,assets/name)
 for name,src in ASSETS:
  dest=assets/name
  if not dest.is_file() or dest.read_bytes()!=src.read_bytes():
   raise RuntimeError(f'Design asset mismatch: {name}')
 rev=hashlib.sha256(b''.join(src.read_bytes() for _,src in ASSETS)).hexdigest()[:12]
 link=(f'<link {MARKER} rel="stylesheet" '
       f'href="/manzo-ai/assets/design-system.css?v={rev}">'
       f'<script defer src="/manzo-ai/assets/design-motion.js?v={rev}"></script>')
 distribution=Counter()
 for page in pages:
  label=surface(page,site)
  distribution[label]+=1
  doc=page.read_text(encoding='utf-8')
  if verify_only:
   if doc.count(MARKER)!=1:
    raise RuntimeError(f'Design stylesheet missing/duplicated: {page}')
   if doc.count(f'design-motion.js?v={rev}')!=1:
    raise RuntimeError(f'Design JS missing/duplicated: {page}')
   if f'data-ma-surface="{label}"' not in doc:
    raise RuntimeError(f'Incorrect page surface classification: {page} ({label})')
   if label=='product' and 'data-product-preview' not in doc:
    raise RuntimeError(f'Product scope missing: {page}')
   if label=='console' and 'data-learning-console' not in doc:
    raise RuntimeError(f'Learning B2B scope missing: {page}')
   continue
  if MARKER in doc or 'data-ma-surface=' in doc:
   raise RuntimeError(f'Non-idempotent duplicate injection: {page}')
  m=BODY_OPEN.search(doc)
  if not m:raise RuntimeError(f'No opening body tag: {page}')
  extra=f' data-ma-surface="{label}"'
  if label=='product':extra+=' data-product-preview'
  if label=='console':extra+=' data-learning-console'
  new_body=m.group(0)[:-1]+extra+'>'
  doc=doc[:m.start()]+new_body+doc[m.end():]
  close=HEAD_CLOSE.search(doc)
  if not close:raise RuntimeError(f'Head tag missing: {page}')
  doc=doc[:close.start()]+link+doc[close.start():]
  page.write_text(doc,encoding='utf-8')
 if distribution['landing']!=3 or distribution['portal']!=1:
  raise RuntimeError(f'Unexpected homepage coverage: {distribution}')
 if distribution['product']!=3 or distribution['console']!=3:
  raise RuntimeError(f'Incomplete Product Lab / Learning B2B: {distribution}')
 print(f'MANZO AI design: {len(pages)} pages / {dict(distribution)} / rev={rev} / verified={verify_only}')
 return dict(distribution)

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--site',type=Path,required=True)
 p.add_argument('--verify-only',action='store_true')
 a=p.parse_args()
 apply(a.site,a.verify_only)
