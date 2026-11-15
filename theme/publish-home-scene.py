#!/usr/bin/env python3
"""Add a truthful, locale-specific product-flow scene to existing home heroes.

This is a layout affordance linking to REAL current Product Lab functionality.
Existing headings, copy, forms, links, JS and search are not edited.
"""
from __future__ import annotations
import argparse
from html import escape
from pathlib import Path
import re

MARKER='data-ma-home-scene="1"'
COPY={
 'it':{
  'label':'Dal primo brief alla verifica',
  'studio':'Studio','studio_desc':'Definisci il progetto',
  'verify':'Verify','verify_desc':'Individua i claim da controllare',
  'learning':'Learning','learning_desc':'Configura il percorso aziendale',
  'action':'Esplora il Product Lab',
  'status':'Anteprima interattiva · Nessun account necessario'
 },
 'en':{
  'label':'From the first brief to review',
  'studio':'Studio','studio_desc':'Structure the project',
  'verify':'Verify','verify_desc':'Flag claims that need evidence',
  'learning':'Learning','learning_desc':'Configure enterprise learning',
  'action':'Explore Product Lab',
  'status':'Interactive preview · No account required'
 },
 'es':{
  'label':'Del primer brief a la verificación',
  'studio':'Studio','studio_desc':'Estructura el proyecto',
  'verify':'Verify','verify_desc':'Señala afirmaciones sin comprobar',
  'learning':'Learning','learning_desc':'Configura la formación empresarial',
  'action':'Explorar Product Lab',
  'status':'Vista previa interactiva · Sin cuentas'
 }
}
ROUTE={'it':'it/prodotto','en':'en/product','es':'es/producto'}

def e(x):return escape(str(x),quote=True)

def find_hero_end(doc):
 m=re.search(r'<(?P<tag>section|div)\b[^>]*class=["\x27][^"\x27]*\bhome-hero\b[^"\x27]*["\x27][^>]*>',doc,re.I|re.S)
 if not m:raise RuntimeError('No home-hero tag found')
 tag=m.group('tag').lower()
 token=re.compile(r'</?'+re.escape(tag)+r'\b[^>]*>',re.I|re.S)
 depth=1
 for match in token.finditer(doc,m.end()):
  if match.group(0).startswith('</'):depth-=1
  else:depth+=1
  if depth==0:return match.start()
 raise RuntimeError('Unbalanced home hero markup')

def block(lang):
 c=COPY[lang]
 rows=''.join(
  '<div class="ma-stage"><span>'+e(c[key])+'</span><strong>'+e(c[key+'_desc'])+'</strong></div>'
  for key in ('studio','verify','learning')
 )
 return (
  '<aside '+MARKER+' class="ma-product-scene" aria-label="'+e(c['label'])+'">'
  '<p class="ma-scene-title">'+e(c['label'])+'</p>'
  '<div class="ma-stages">'+rows+'</div>'
  '<a class="ma-scene-link" href="/manzo-ai/'+ROUTE[lang]+'/">'+e(c['action'])+' <span aria-hidden="true">↗</span></a>'
  '<p class="ma-scene-note">'+e(c['status'])+'</p></aside>'
 )

def publish(site,verify_only=False):
 for lang in COPY:
  target=site/lang/'index.html'
  if not target.is_file():raise RuntimeError('Missing homepage: '+str(target))
  content=target.read_text(encoding='utf-8')
  if verify_only:
   if content.count(MARKER)!=1:raise RuntimeError('Missing scene '+lang)
   assert '/manzo-ai/'+ROUTE[lang]+'/' in content
   assert content.count('home-hero')>=1
   continue
  if MARKER in content:raise RuntimeError('Duplicate scene '+lang)
  idx=find_hero_end(content)
  content=content[:idx]+block(lang)+content[idx:]
  target.write_text(content,encoding='utf-8')
 print(f'MANZO AI homepage product scene: IT/EN/ES; 3 actual product paths; verified={verify_only}')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--site',type=Path,required=True)
 p.add_argument('--verify-only',action='store_true')
 a=p.parse_args();publish(a.site,a.verify_only)
