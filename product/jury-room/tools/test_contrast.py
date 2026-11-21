"""WCAG AA text pair checks of important UI foregrounds and actual solid surfaces.
Image overlays and CSS gradients still need visual review; audit is not a WCAG certificate.
"""
from pathlib import Path
import re,base64,collections
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];styles='\n'.join((R/'assets'/n).read_text() for n in ('styles.css','rooms.css'))
js=r'''()=>{const rgba=s=>{const a=(s.match(/[\d.]+/g)||[]).map(Number);return a.length===4?a:[...a.slice(0,3),1]};
const lum=a=>a.slice(0,3).map(x=>x/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4).reduce((p,v,i)=>p+v*[.2126,.7152,.0722][i],0);
const ratio=(a,b)=>{let x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
const bg=el=>{let a=[];while(el){a.unshift(el);el=el.parentElement}let b=[255,255,255,1];for(let n of a){let s=getComputedStyle(n).backgroundColor;if(s.startsWith('rgb')){const q=rgba(s);b=[0,1,2].map(i=>q[i]*q[3]+b[i]*(1-q[3]));b.push(1)}}return b};
return [...document.querySelectorAll('.room-top>span:first-child,.room-kicker,.room-card h3,.room-card>p,.lead-index span,.method-steps small,.sidebar-eyebrow,.prompt-card-head div span,.video-concept>summary span,.form-disclosure,.verdict-note,.verdict-work label small,.result-caution,.form-title span,.results-heading span,.room-chapter>p,.room-callout p,.room-output,.room-action')].filter(x=>x.getBoundingClientRect().width>0).map(x=>({text:x.textContent.trim().slice(0,35),selector:x.className||x.tagName,color:getComputedStyle(x).color,ratio:+ratio(rgba(getComputedStyle(x).color),bg(x)).toFixed(2)}))}'''
from collections import defaultdict
problems=[];measure=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 for name in ('index.html','banco-di-prova.html','officina-locale.html','sala-dei-confini.html'):
  d=BeautifulSoup((R/name).read_text(),'html.parser')
  for t in d.select('script[src],link[rel="stylesheet"]'):t.decompose()
  for t in d.select('img[src]'):
   src=t['src'];f=R/src
   if f.is_file():t['src']='data:'+('image/svg+xml' if src.endswith('.svg') else 'image/webp')+';base64,'+base64.b64encode(f.read_bytes()).decode()
  for width in (375,768,1440):
   pg=b.new_page(viewport={'width':width,'height':900})
   pg.set_content(str(d),wait_until='domcontentloaded');pg.add_style_tag(content=styles)
   data=pg.evaluate(js)
   bad=[v for v in data if v['ratio']<4.5 and not (v['text'].startswith('→'))]
   problems.extend((name,width,v) for v in bad);measure.extend((name,width,v) for v in data)
   assert pg.evaluate('document.documentElement.scrollWidth <= innerWidth+3'),(name,width)
   pg.close()
 b.close()
print('Audited',len(measure),'critical text samples at three viewports')
if problems:
 for n,w,v in problems[:30]:print('LOW',n,w,v)
 raise SystemExit(f'{len(problems)} pair(s) below 4.5:1')
print('PASS: all selected normal-text pairs >= 4.5:1 across 375/768/1440')
