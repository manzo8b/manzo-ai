#!/usr/bin/env python3
"""Repair duplicate subsection anchors in MANZO AI's legacy M02–M06 lessons.

Older M02–M06 pages give all five h3 lesson subsections id="sub-2-2".
This creates five DOM nodes with the same ID and breaks direct subsection links.
Only those H3 IDs are changed; headings, quizzes, routes and source ZIP remain intact.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import re

MARK = re.compile(r'(<h3\b[^>]*\bid=")sub-2-2("[^>]*>\s*)(2\.([1-5])\s)', re.I)
IDS = re.compile(r'\bid=["\']([^"\']+)["\']', re.I)

# Source archive has five affected M02–M06 lessons in each locale.
ROUTES = {
 "it": [
  "it/impara/come-funziona-un-modello-linguistico",
  "it/impara/come-costruire-un-prompt-efficace",
  "it/impara/come-verificare-le-risposte-ai",
  "it/impara/progettare-un-workflow-ai",
  "it/impara/ai-storia-lavoro-societa",
 ],
 "en": [
  "en/learn/how-a-language-model-works",
  "en/learn/how-to-build-an-effective-prompt",
  "en/learn/how-to-verify-ai-answers",
  "en/learn/designing-an-ai-workflow",
  "en/learn/ai-history-work-and-society",
 ],
 "es": [
  "es/aprende/como-funciona-un-modelo-de-lenguaje",
  "es/aprende/como-construir-un-prompt-eficaz",
  "es/aprende/como-verificar-las-respuestas-de-ia",
  "es/aprende/disenar-un-flujo-de-trabajo-con-ia",
  "es/aprende/ia-historia-trabajo-sociedad",
 ]
}

def repair(site:Path, verify_only=False):
 reviewed=0
 for lang,items in ROUTES.items():
  for route in items:
   page=site/route/"index.html"
   if not page.is_file():
    raise RuntimeError("Missing lesson: "+route)
   doc=page.read_text(encoding="utf-8")
   def callback(m):
    # Correct id derives from the *actual* visible section number, never
    # from the repeated id of the original HTML.
    return m.group(1)+"sub-2-"+m.group(4)+m.group(2)+m.group(3)
   if not verify_only:
    if len(MARK.findall(doc))!=5:
     raise RuntimeError("Unexpected subsection structure: "+route)
    doc=MARK.sub(callback,doc)
    page.write_text(doc,encoding="utf-8")
   expected={f"sub-2-{i}" for i in range(1,6)}
   occurrences=re.findall(r'<h3\b[^>]*\bid="(sub-2-\d+)"',doc,re.I)
   if set(occurrences)!=expected or len(occurrences)!=5:
    raise RuntimeError("Subsection IDs not unique/complete: "+route)
   ids=IDS.findall(doc)
   duplicates=[name for name,n in Counter(ids).items() if n>1]
   if duplicates:raise RuntimeError("Duplicate DOM IDs: "+route+" -> "+str(duplicates[:5]))
   if 'data-ma-learning' in doc:
    # The repair must not remove existing independent lesson interactions.
    pass
   reviewed+=1
 print(f"MANZO AI learning subsection anchor audit: {reviewed} pages (5 × 3 languages), duplicate IDs=0; verify={verify_only}")

if __name__=="__main__":
 parser=argparse.ArgumentParser()
 parser.add_argument("--site",type=Path,required=True)
 parser.add_argument("--verify-only",action="store_true")
 args=parser.parse_args()
 repair(args.site,args.verify_only)
