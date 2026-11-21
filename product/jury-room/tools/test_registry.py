from pathlib import Path
import sys
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path=__import__('shutil').which('chromium') or __import__('shutil').which('google-chrome') or None,args=['--no-sandbox','--disable-dev-shm-usage'])
 page=b.new_page();s=BeautifulSoup((ROOT/'banco-di-prova.html').read_text(),'html.parser')
 for tag in list(s.select('script[src],link[rel=stylesheet]')):tag.decompose()
 page.set_content(str(s));page.add_style_tag(content=(ROOT/'assets/styles.css').read_text())
 page.add_script_tag(content=(ROOT/'assets/experiment-data.js').read_text());page.add_script_tag(content=(ROOT/'assets/app.js').read_text())
 page.evaluate('''() => {window.addRun=(model,prompt)=>{
   const form=document.getElementById('trial-form');
   form.querySelector('[name=model]').value=model;
   form.querySelector('[name=version]').value='v1';
   form.querySelector('[name=date]').value='2026-11-20';
   form.querySelector('[name=prompt]').value=prompt;
   form.querySelector('input[name="found-gap"][value="L1"]').checked=true;
   for(const key of ['inventions','omissions','generalisations','inferences','falseAlarms'])form.querySelector(`[name=${key}]`).value='0';
   form.requestSubmit();
 };}''')
 for i in range(5):page.evaluate('window.addRun("Demo Uno", "A")')
 assert page.locator('#run-history .run-row').count()==5
 page.evaluate('window.addRun("demo  uno", "A")')
 assert page.locator('#run-history .run-row').count()==5,'over 5 per prompt'
 for i in range(5):page.evaluate('window.addRun(" DE MO Uno ", "B")')
 # different spelling is not same normalized name by definition; another model
 assert page.locator('#models-summary .model-summary').count()==2
 for i in range(5):page.evaluate('window.addRun("demo uno", "B")')
 assert page.locator('#models-summary .model-summary').count()==2
 assert page.locator('#run-history .run-row').count()==15
 for i in range(3):page.evaluate('window.addRun("Altro modello", "A")')
 assert page.locator('#models-summary .model-summary').count()==3
 page.evaluate('window.addRun("Quarto modello", "A")')
 assert page.locator('#models-summary .model-summary').count()==3
 assert page.locator('#run-history .run-row').count()==18
 # reset form does NOT delete records
 page.evaluate('document.getElementById("trial-form").reset()')
 assert page.locator('#run-history .run-row').count()==18
 assert page.locator('#record-gap-count').inner_text()=='0 / 8'
 assert not page.locator('#result-caution').inner_text().lower().startswith('la richiesta b è')
 print('PASS 3-model ceiling, normalized grouping, 5 each model/prompt, separate summary, reset without data deletion')
 b.close()
