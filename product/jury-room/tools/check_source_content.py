#!/usr/bin/env python3
"""Read-only content contract for MANZO AI private jurors' room, v0.2.
Verifies exact verbatim document, prompts, answer rows, example claims and classes.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import re, json, sys
ROOT=Path(__file__).resolve().parents[1]
ORG=(ROOT/'sources/MANZO_AI_Progetto_Esperimenti.md').read_text(encoding='utf-8')
BRIEF=(ROOT/'sources/MANZO_AI_Brief_Correzione_Prototipo_Stanza_dei_giurati.md').read_text(encoding='utf-8')
html=(ROOT/'banco-di-prova.html').read_text(encoding='utf-8')
soup=BeautifulSoup(html,'html.parser')

def extract(s,regex):
 m=re.search(regex,s,re.S)
 assert m is not None,regex
 return m.group(1).strip('\n')
def check(label,a,b):
 if a!=b:
  print('FAIL',label,'expected',repr(a[:150]),'actual',repr(b[:150]));sys.exit(1)
 print('PASS',label)

doc=extract(ORG,r'```text\s*\n(\s*PREVENTIVO N\. 2026/047.*?)(?=\n```)')
A=extract(ORG,r'\*\*Richiesta A \(generica\):\*\*\s*```text\s*\n(.*?)\n```')
B=extract(ORG,r'\*\*Richiesta B \(vincolata\):\*\*\s*```text\s*\n(.*?)\n```')
check('Preventivo integrale',doc,soup.select_one('#source-document').get_text())
check('Prompt A integrale',A,soup.select_one('#prompt-a').get_text())
check('Prompt B integrale',B,soup.select_one('#prompt-b').get_text())
key=extract(ORG,r'#### Chiave di risposta \(nota in anticipo, non mostrarla al modello\)\n\n(.*?)\n\n\*\*Controllo:')
expected=[]
for line in key.splitlines():
 m=re.match(r'\| (L[1-8]) \| (.*?) \| (Alta|Media|Bassa) \|',line)
 if m:expected.append(m.groups())
actual=[tuple(el.get_text(' ',strip=True).split(' ',1)) for el in soup.select('#answer-list .answer-row')]
assert len(expected)==8 and len(actual)==8
for ix,(row,(id,rest)) in enumerate(zip(expected,actual)):
 check('Chiave '+id,(row[0],row[1],row[2]),(id,rest.rsplit(' ',1)[0],rest.rsplit(' ',1)[-1]))
claims=extract(BRIEF,r'\*\*Il riassunto di esempio \(8 affermazioni, testi da usare così come sono\):\*\*\n\n(.*?)\n\n\*\*Interazione')
expected_claims=[]
for line in claims.splitlines():
 m=re.match(r'\| (R[1-8]) \| (.*?) \|',line)
 if m:expected_claims.append(m.groups())
assert len(expected_claims)==8
for ix,(id,txt) in enumerate(expected_claims):
 check('Affermazione '+id,txt,soup.select(f'.claim-card[data-claim="{id}"] .claim-title p')[0].get_text())
classes=extract(ORG,r'\| Classe \| Definizione \| Esempio sul documento di prova \|\n\|[-| ]+\|\n(.*?)\n\n\*\*Rischio:')
expected_cl=[]
for line in classes.splitlines():
 m=re.match(r'\| (.*?) \| (.*?) \| (.*?) \|',line)
 if m:expected_cl.append(m.groups())
assert len(expected_cl)==4
actual_cl=[tuple(td.get_text(' ',strip=True) for td in tr.select('th, td')) for tr in soup.select('#classi-errori tbody tr')]
check('Definizioni originali delle classi di errore',expected_cl,actual_cl)
assert len(soup.select('h1'))==1
assert soup.select_one('noscript') and 'Il documento, le richieste e la chiave restano leggibili' in soup.select_one('noscript').get_text()
assert soup.select_one('meta[name=robots]')['content']=='noindex,nofollow'
assert len(soup.select('.record-gap input[name=found-gap]'))==8
assert len(soup.select('script[src]'))==2
assert 'Non è la risposta di un modello AI' in soup.select_one('.storyteller-alert').get_text()
assert soup.select_one('#models-summary').get_text().strip()==''
assert not re.search(r'non generata dall[\'’]AI|Ogni luce ha un significato|Progetto Esperimenti, §|EXPERIMENTAL LAB',html,flags=re.I)
js=(ROOT/'assets/app.js').read_text(encoding='utf-8')
assert not re.search(r'(?<![a-zA-Z])(?:fetch\s*\(|XMLHttpRequest|localStorage\s*\.|sessionStorage\s*\.|document\.cookie\s*=)',js)
print('PASS Fonte unica per testi originali, static fallback, privacy, noindex')
