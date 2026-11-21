#!/usr/bin/env python3
"""Regenerate embedded integral source cards; do not hand-edit the quoted documents.

Requires: beautifulsoup4, mistune. Heading levels are offset by one so the
container page retains its single visible H1; text and tables are preserved.
"""
from pathlib import Path
from bs4 import BeautifulSoup as BS
import mistune, re
ROOT=Path(__file__).resolve().parents[1]
CONTRACT=(('officina-locale.html','MANZO_AI_Esperimento_03_Officina.md'),('sala-dei-confini.html','MANZO_AI_Esperimento_02_Governo.md'))
render=mistune.create_markdown(plugins=['table','strikethrough','task_lists'])
for page,source in CONTRACT:
 doc=BS((ROOT/page).read_text(encoding='utf-8'),'html.parser')
 src=BS(render((ROOT/'sources'/source).read_text(encoding='utf-8')),'html.parser')
 for title in src.find_all(re.compile(r'^h[1-5]$')):title.name='h'+str(min(6,int(title.name[1])+1))
 root=doc.select_one('.room-source-body')
 if not root:raise ValueError(f'No source container in {page}')
 root.clear()
 for element in list(src.contents):root.append(element)
 output=str(doc)
 if not output.lstrip().lower().startswith('<!doctype'):output='<!DOCTYPE html>\n'+output
 (ROOT/page).write_text(output,encoding='utf-8')
 print('REGENERATED',page,'from',source)
