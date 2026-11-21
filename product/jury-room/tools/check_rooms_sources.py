from pathlib import Path
import re, html
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]

def normalize(text):
 return re.sub(r'\s+',' ',re.sub(r'\*','',html.unescape(text))).strip()
for filename,source,expected_table,expected_count,anchors in [
 ('officina-locale.html','MANZO_AI_Esperimento_03_Officina.md','data-test',6,['Forno Esempio','Pane casareccio','Non c’è consegna a domicilio','celiaca']),
 ('sala-dei-confini.html','MANZO_AI_Esperimento_02_Governo.md','data-action',12,['Centro Formazione Aurora','foglio degli iscritti','A12','Regola cambiata'])
]:
 doc=BeautifulSoup((ROOT/filename).read_text(encoding='utf-8'),'html.parser')
 source_text=(ROOT/'sources'/source).read_text(encoding='utf-8')
 original=normalize(source_text)
 rendered=normalize(doc.select_one('.room-source-body').get_text(' ',strip=True))
 for term in anchors:
  assert normalize(term).lower() in rendered.lower(),(filename,'Missing source term',term)
 for fragment in ['In preparazione','[da definire]']:
  assert normalize(fragment).lower() in original.lower(),(source,fragment)
 assert len(doc.select('['+expected_table+']'))==expected_count,filename
 if filename.startswith('officina'):
  for line in source_text.splitlines():
   if re.match(r'^\| T[1-6] \|',line):
    msg=line.strip('|').split('|')[2].strip().strip('*')
    assert normalize(msg) in rendered,('Test message missing from full dossier',msg)
 else:
  assert 'Fonti normative da completare' in doc.get_text(' ',strip=True)
  for line in source_text.splitlines():
   if re.match(r'^\| A\d+ \|',line) and len(line.strip('|').split('|'))==2:
    action=line.strip('|').split('|')[1].strip()
    assert normalize(action) in rendered,(filename,action)
 print('PASS',filename,'source text and required exercise structure')
