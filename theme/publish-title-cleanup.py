#!/usr/bin/env python3
"""MANZO AI editorial invariant: never terminate a visible H1–H6 with a dot.

Normalize ONLY terminal full stops in rendered section headings.
Do not modify paragraph copy, site archive, course answers, prices, links,
source citations, meta descriptions or other punctuation.
Works on final built HTML after all article/course/SEO publishers.
"""
from __future__ import annotations

import argparse
from html import unescape
from pathlib import Path
import re

HEADING=re.compile(r'<h(?P<level>[1-6])\b[^>]*>.*?</h(?P=level)\s*>',re.I|re.S)
OPEN=re.compile(r'^<h[1-6]\b[^>]*>',re.I|re.S)
CLOSE=re.compile(r'</h[1-6]\s*>$',re.I)
TRAILING_DOT=re.compile(r'\.+(?=\s*(?:</[a-z][^>]*>\s*)*$)',re.I|re.S)
TAG=re.compile(r'<[^>]*>')
SCRIPT=re.compile(r'<script\b.*?</script\s*>|<style\b.*?</style\s*>',re.I|re.S)

def visible(html:str)->str:
 return unescape(TAG.sub('',html)).strip()

def amend(match:re.Match)->str:
 raw=match.group(0)
 start=OPEN.search(raw)
 end=CLOSE.search(raw)
 if start is None or end is None:return raw
 internal=raw[start.end():end.start()]
 if not visible(internal).endswith('.'):return raw
 fixed=TRAILING_DOT.sub('',internal)
 if fixed==internal:
  raise ValueError('Heading punctuation cannot safely be normalized: '+raw[:100])
 return raw[:start.end()]+fixed+raw[end.start():]

def headings(html:str):
 # Script/style elements are not user-visible headings and may contain HTML
 # examples. Ignore those while reporting issues.
 sanitized=SCRIPT.sub('',html)
 return [match.group(0) for match in HEADING.finditer(sanitized)]

def normalize(doc:str)->str:
 # Split code-bearing script/style ranges; only process real markup outside.
 pieces=SCRIPT.split(doc)
 hidden=SCRIPT.findall(doc)
 out=[]
 for i,part in enumerate(pieces):
  out.append(HEADING.sub(amend,part))
  if i<len(hidden):out.append(hidden[i])
 return ''.join(out)

def selftest():
 cases={
  '<h2>Programma.</h2>':'<h2>Programma</h2>',
  '<h2><span>Il programma.</span></h2>':'<h2><span>Il programma</span></h2>',
  '<h3>1. Il metodo.</h3>':'<h3>1. Il metodo</h3>',
  '<h2>Why? </h2>':'<h2>Why? </h2>',
  '<h2>IA <em>responsabile.</em></h2>':'<h2>IA <em>responsabile</em></h2>',
  '<h2>Dr. Rossi</h2>':'<h2>Dr. Rossi</h2>',
 }
 for start,expected in cases.items():
  assert normalize(start)==expected,(start,normalize(start),expected)
 assert normalize('<script>const html="<h2>Test.</h2>";</script>')=='<script>const html="<h2>Test.</h2>";</script>'
 assert normalize('<p>La frase termina.</p>')=='<p>La frase termina.</p>'

def build(site:Path,verify_only=False):
 pages=sorted(site.rglob('index.html'))
 if len(pages)<90:raise RuntimeError(f'Incomplete site: only {len(pages)} pages')
 fixed_pages=0;fixed_headings=0;tested=0
 for page in pages:
  original=page.read_text(encoding='utf-8')
  issues=[h for h in headings(original) if visible(h).endswith('.')]
  if verify_only:
   if issues:raise RuntimeError(f'Heading has final period: {page}: '+repr(issues[:2]))
   tested+=len(headings(original))
   continue
  updated=normalize(original)
  new_issues=[h for h in headings(updated) if visible(h).endswith('.')]
  if new_issues:raise RuntimeError(f'Unresolved heading full stops: {page}: '+repr(new_issues[:2]))
  if updated!=original:
   page.write_text(updated,encoding='utf-8')
   fixed_pages+=1
   fixed_headings+=len(issues)
  tested+=len(headings(updated))
 print(f'PASS heading editorial contract: {len(pages)} pages, {tested} H1–H6 titles, {fixed_headings} terminal periods removed on {fixed_pages} pages, verified={verify_only}')

if __name__=='__main__':
 selftest()
 parser=argparse.ArgumentParser()
 parser.add_argument('--site',type=Path,required=True)
 parser.add_argument('--verify-only',action='store_true')
 args=parser.parse_args()
 build(args.site,args.verify_only)
