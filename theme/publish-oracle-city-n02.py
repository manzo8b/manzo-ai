#!/usr/bin/env python3
"""ORACLE CITY N02. Non-destructive, reproducible MANZO AI digital edition."""
from pathlib import Path
from html import escape
from io import BytesIO
import argparse, base64, hashlib, math, random, re, textwrap
from PIL import Image
import cairosvg
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4

BASE="it/risorse/oracle-city/numero-02"
ROUTE="/manzo-ai/"+BASE+"/"
SITE_URL="https://manzo8b.github.io"+ROUTE
PAGE_W,PAGE_H=1000,1500
PALETTE={"LIA":"#c43b36","MANZO":"#355c7d","GLITCH":"#7445a4","PASSANTE":"#566075","LIBRAIO":"#ac7e4c","DIDASCALIA":"#d9b879"}
# scene, people, speech/caption: every frame is one independently typeset vignette.
PAGES=[
("Trecento non è un numero piccolo",[
 ("papers","lia",[("LIA","Trecento fogli?!")]),
 ("counter","glitch",[("GLITCH","Potrei contarli due volte.")]),
 ("papers","manzo",[("MANZO","Meglio capire da dove arrivano.")])]),
("I fogli tornano",[
 ("library","lia,manzo,glitch",[("DIDASCALIA","Lunedì. La biblioteca comunale ha riaperto.")]),
 ("screens","",[("DIDASCALIA","La vecchia notizia continua a viaggiare su schermi diversi.")]),
 ("paper","",[("DIDASCALIA","Una notizia corre anche quando è stata smentita.")])]),
("Le trecento ombre",[
 ("city","",[("DIDASCALIA","La piazza si illumina di centinaia di schermi.")]),
 ("screens","",[("DIDASCALIA","La stessa frase. Perfino lo stesso errore.")]),
 ("papers","",[("DIDASCALIA","Sembravano trecento testimoni.")])]),
("Il dubbio non fa notizia",[
 ("library","lia,passante",[("PASSANTE","Ma online dicono ancora che è chiusa.")]),
 ("counter","lia,glitch",[("LIA","Da dove arriva tutta questa roba?"),("GLITCH","Rilevo trecento pubblicazioni.")]),
 ("screens","manzo",[("MANZO","Pubblicazioni. Non trecento verifiche.")]),
 ("papers","lia",[("LIA","Quindi copiare non è testimoniare.")])]),
("Il dettaglio minuscolo",[
 ("paper","manzo",[("MANZO","Guarda questa virgola.")]),
 ("paper","lia",[("LIA","Davvero stiamo seguendo una virgola?")]),
 ("comparison","glitch",[("GLITCH","Coincidono anche gli errori.")]),
 ("papers","manzo",[("MANZO","Anche l'errore è stato copiato.")])]),
("Un clic non fa un testimone",[
 ("screens","lia",[("LIA","Trovata la prima fonte!")]),
 ("comparison","manzo",[("MANZO","C'è scritto «ripubblicato».")]),
 ("loop","lia,glitch",[("LIA","Il primo link non è il primo autore.")])]),
("La sala degli specchi",[
 ("screens","glitch",[("GLITCH","Tre canali replicano lo stesso testo.")]),
 ("screens","lia",[("LIA","Tre canali. Tre fonti?")]),
 ("mirrors","manzo",[("MANZO","Una sola immagine. Molti riflessi.")]),
 ("mystery","lia,glitch",[])]),
("La diramazione",[
 ("flow","",[("DIDASCALIA","Bollettino 42 → Sintesi civica → Tre canali → Trecento copie.")]),
 ("document","lia",[("LIA","Una frase ha fatto tutto questo giro?")]),
 ("flow","glitch",[("GLITCH","Trecento copie. Una sola sintesi.")])]),
("Chi ha scritto la prima riga?",[
 ("terminal","",[("DIDASCALIA","Nel registro, il campo «Autore della sintesi» è vuoto.")]),
 ("terminal","lia,glitch",[("LIA","Dimmi chi l'ha scritta."),("GLITCH","Non lo so ancora.")]),
 ("terminal","manzo",[("MANZO","Un campo vuoto non è una firma nascosta.")]),
 ("mystery","lia",[])]),
("La persona dall'altra parte",[
 ("bookshop","bookseller",[("LIBRAIO","Per me la correzione è arrivata dopo.")]),
 ("bookshop","lia",[("LIA","Pensavo bastasse dire che era falsa.")]),
 ("bookshop","lia,manzo,glitch",[])]),
("Piccola rettifica, grande strada",[
 ("correction","glitch",[("GLITCH","Posso collegare la rettifica alle copie raggiungibili.")]),
 ("correction","lia",[("LIA","E quelle che non raggiungi?")]),
 ("correction","glitch",[("GLITCH","Non posso promettere di correggerle tutte.")]),
 ("correction","glitch",[("GLITCH","Non so chi ha iniziato. So cosa posso correggere.")])]),
("Il nome dietro il nome",[
 ("terminal","lia",[("LIA","È questo il responsabile?")]),
 ("terminal","manzo",[("MANZO","È il nome di un servizio. Non di una persona.")]),
 ("mystery","glitch",[("GLITCH","Per sapere chi lo gestisce serve un'altra domanda.")])]),
("Il corridoio",[
 ("library","",[("DIDASCALIA","La biblioteca è di nuovo piena di vita.")]),
 ("notebook","lia",[("DIDASCALIA","QUANTE FONTI SONO DAVVERO INDIPENDENTI?")]),
 ("door","manzo",[("MANZO","Qui iniziano le revisioni.")]),
 ("door","lia,glitch",[("LIA","E chi decide cosa possiamo vedere?")])])
]
assert len(PAGES)==13
assert sum(len(p[1]) for p in PAGES)==45
all_speech=" ".join(t for _,frames in PAGES for _,_,speech in frames for _,t in speech)
assert not re.search(r"(?i)\b(?:amo|amò)\b",all_speech)
def E(s):return escape(str(s),quote=True)
def t(x,y,s,sz=28,fill="#fff",weight=700,anchor="start",extra=""):
 return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{sz}" font-family="DejaVu Sans,Arial,sans-serif" font-weight="{weight}" text-anchor="{anchor}" {extra}>{E(s)}</text>'
def rect(x,y,w,h,fill,rx=0,stroke="none",sw=0):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def path(d,fill,stroke="none",sw=0,extra=""):
 return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def circle(x,y,r,fill,stroke="none",sw=0):
 return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def defs():
 return """<defs>
  <linearGradient id="night" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0a1021"/><stop offset=".52" stop-color="#19294f"/><stop offset="1" stop-color="#7d3867"/></linearGradient>
  <linearGradient id="dusk" x1="0" y1="0" x2=".6" y2="1"><stop stop-color="#0d1732"/><stop offset=".5" stop-color="#3e4578"/><stop offset="1" stop-color="#da7560"/></linearGradient>
  <linearGradient id="ink" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#11142a"/><stop offset="1" stop-color="#253c60"/></linearGradient>
  <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fff0aa"/><stop offset="1" stop-color="#e9a75d"/></linearGradient>
  <linearGradient id="violet" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#e0b3ff"/><stop offset="1" stop-color="#7c38dc"/></linearGradient>
  <pattern id="windows" patternUnits="userSpaceOnUse" width="31" height="35"><rect width="31" height="35" fill="#18213b"/><rect x="8" y="9" width="9" height="14" fill="#f0b56f" opacity=".5"/></pattern>
 </defs>"""
def city_art(w,h,seed):
 rng=random.Random(seed)
 a=[rect(0,0,w,h,"url(#dusk)")]
 a.append(circle(int(w*.76),int(h*.20),min(w,h)//7,"#f6bb8d"))
 for i in range(20):
  px=int(i*w/19-20); hh=rng.randint(int(h*.26),int(h*.73))
  a.append(rect(px,h-hh,54,hh,"#18213b",0,"#090d1e",2))
  for wy in range(int(h-hh+14),int(h-18),30):
   for wx in range(px+10,px+47,18):
    if rng.random()<.55:a.append(rect(wx,wy,7,13,"#eaaa69"))
 a.append(path(f"M0,{h-36} Q{w//2},{h-94} {w},{h-28} L{w},{h} H0 Z","#101427"))
 return "".join(a)
def papers_art(w,h,seed):
 rng=random.Random(seed); a=[]
 for i in range(16):
  x=rng.randint(50,w-130); y=rng.randint(15,int(h-80))
  rot=rng.randint(-21,21)
  a.append(f'<g transform="translate({x} {y}) rotate({rot})">'+rect(0,0,80,105,"#f2e6d4",3,"#142037",2)+rect(10,14,55,4,"#8791a7")+rect(10,28,48,3,"#a9b1bd")+rect(10,41,57,3,"#a9b1bd")+rect(10,54,43,3,"#a9b1bd")+'</g>')
 return "".join(a)
def library_art(w,h):
 a=[rect(w*.43,h*.03,w*.48,h*.91,"#3a3449",0,"#a78175",5),rect(w*.46,h*.08,w*.43,h*.09,"#bf9e81"),rect(w*.50,h*.28,w*.32,h*.61,"#d4a871",150,"#e4c49e",10),rect(w*.53,h*.34,w*.26,h*.54,"#241928",115,"#fbd088",7)]
 for x in (int(w*.46),int(w*.86)):
  a.append(rect(x,h*.16,28,h*.73,"#d6a994",0,"#3c3347",4))
 a.append(path(f"M{w*.43},{h*.17} L{w*.67},{h*.02} L{w*.94},{h*.17} Z","#f2cba5","#493f4c",5))
 a.append(t(int(w*.68),int(h*.14),"BIBLIOTECA",20,"#302944",800,"middle"))
 for k in range(6):
  x=w*.5+k*45
  a.append(rect(x,h*.41,8,h*.42,"#d0a365"))
 return "".join(a)
def screens_art(w,h):
 a=[]
 for i,(label,col) in enumerate([("SCHERMI PUBBLICI","#54a8f0"),("NEWSLETTER","#ca84fb"),("QUARTIERI","#ed8c7b")]):
  x=20+i*w/3
  a.append(rect(x,30,w/3-28,h*.66,"#131e34",14,col,6))
  a.append(rect(x+14,43,w/3-56,32,col,5))
  a.append(t(x+23,68,label,14,"#07101e",800))
  a.append(rect(x+18,100,w/3-67,7,"#d1d2e3",2))
  for yy in (122,147,172,197):
   a.append(rect(x+18,yy,w/3-65,5,"#a3aac3",2))
  a.append(rect(x+18,232,w/3-65,10,"#d66c72",2))
 return "".join(a)
def map_art(w,h,mode):
 a=[rect(30,25,w-60,h*.78,"#111a31",22,"#8a66d4",5)]
 if mode=="flow":
  labels=["BOLLETTINO 42","SINTESI CIVICA","TRE CANALI","300 COPIE"]
  for i,lab in enumerate(labels):
   x=65+i*(w-145)/4
   a.append(rect(x,85,(w-165)/4,105,("#d9bb8d" if i==0 else "#6549a0" if i in (1,2) else "#315a80"),9,"#e8dbea",3))
   a.append(t(x+(w-165)/8,122,lab.split(" ")[0],16,"#fff",800,"middle"))
   a.append(t(x+(w-165)/8,151,lab.split(" ")[-1],18,"#fff",800,"middle"))
   if i<3: a.append(path(f"M{x+(w-165)/4+4},135 l18,-12 v24 Z","#f3c98c"))
 else:
  for i in range(3):
   a.append(rect(90+i*190,55,150,92,"#402f72",13,"#9873ef",3))
   a.append(circle(165+i*190,95,13,"#f1c4ff"))
  a.append(path("M165,147 Q365,200 355,270 M355,147 Q355,205 355,270 M545,147 Q350,210 355,270","none","#ae8cf1",6))
  a.append(rect(265,268,180,70,"#161a35",13,"#f1bf97",4))
 return "".join(a)
def terminal_art(w,h,kind):
 a=[rect(95,24,w-195,h*.84,"#111e36",18,"#8b6ad5",7)]
 if kind=="terminal":
  headings=[("REGISTRO SINTESI",55),("DATA / VERSIONE",120),("SERVIZIO: SINTESI CIVICA",173),("AUTORE DELLA SINTESI: —",226)]
 elif kind=="correction":
  headings=[("RETTIFICA UFFICIALE",55),("BIBLIOTECA APERTA",120),("PROPOSTA NON APPROVATA",173),("COPIE NON RAGGIUNGIBILI",226)]
 else:
  headings=[("SINTESI CIVICA",55),("SERVIZIO AUTOMATICO",120),("REGISTRO REVISIONI",173),("ACCESSO LIMITATO",226)]
 for label,yy in headings:
  a.append(rect(120,yy-25,w-245,40,"#284363" if yy<200 else "#443455",4))
  a.append(t(140,yy+2,label,22,"#f4ebfb",750))
 return "".join(a)
def bookshop_art(w,h):
 a=[]
 for x in range(55,w-25,132):
  a.append(rect(x,45,113,h*.74,"#432f32",2,"#b28b62",5))
  for y in range(68,int(h*.70),48):
   a.append(rect(x+9,y,100,5,"#b78b5f"))
   for b in range(6):
    a.append(rect(x+11+14*b,y-29,9,26,("#de8a65" if b%3==0 else "#6b8baa" if b%3==1 else "#caba7a")))
 return "".join(a)
def scene_art(kind,w,h,seed):
 a=[city_art(w,h,seed)]
 if kind=="library": a.append(library_art(w,h))
 elif kind in ("papers","paper","comparison"): a.append(papers_art(w,h,seed+20))
 elif kind=="screens": a.append(screens_art(w,h))
 elif kind=="counter":
  a.append(rect(w*.45,30,w*.42,h*.65,"#191431",20,"#8e6fd2",5))
  for x,y in ((.55,.3),(.71,.22),(.61,.48)):a.append(t(int(w*x),int(h*y),"300",45,"#c59eff",900))
 elif kind in ("flow","loop","mystery"):
  a.append(map_art(w,h,"flow" if kind=="flow" else "mystery"))
 elif kind in ("terminal","correction"):a.append(terminal_art(w,h,kind))
 elif kind=="bookshop":a.append(bookshop_art(w,h))
 elif kind=="door":
  a.append(rect(int(w*.44),10,int(w*.48),int(h*.92),"#322c38",6,"#d0a27d",12))
  a.append(rect(int(w*.57),20,int(w*.20),int(h*.71),"#1c1d2f",40,"#b28b6b",7))
  a.append(rect(int(w*.48),int(h*.57),int(w*.38),58,"#d6c7a9",4))
  a.append(t(int(w*.67),int(h*.63),"ACCESSO LIMITATO",19,"#1a1b25",900,"middle"))
 elif kind=="mirrors":
  for i in range(3):
   x=40+i*w/3
   a.append(rect(x,24,w/3-45,h*.72,"#17294b",80,"#dfb3a1",9))
   a.append(path(f"M{x+50},50 Q{x+120},130 {x+100},{h*.7}","none","#c09ffc",11))
 elif kind=="notebook":
  a.append(rect(w*.32,30,w*.61,h*.75,"#eee2d0",8,"#885b4d",6))
  a.append(t(int(w*.63),int(h*.35),"QUANTE FONTI",33,"#2a3045",900,"middle"))
  a.append(t(int(w*.63),int(h*.48),"SONO DAVVERO",33,"#2a3045",900,"middle"))
  a.append(t(int(w*.63),int(h*.61),"INDIPENDENTI?",33,"#2a3045",900,"middle"))
 return "".join(a)
def lia(x,y,s=1):
 body=rect(15,128,138,170,"#c43b36",40,"#18213b",8)+path("M15,180 L-22,268 L10,280 L43,190 Z","#f4e9df","#18213b",5)+path("M143,186 L188,268 L169,282 L118,197 Z","#e8ded8","#18213b",5)
 hair=path("M1,111 C-6,17 36,-15 105,8 C180,-2 181,88 166,126 L145,108 C173,49 130,20 90,31 C20,14 5,89 19,116 Z","#ebbe64","#251c32",8)
 head=circle(90,92,70,"#ffd9bd","#2a1e32",7)
 bang=path("M22,66 Q70,-12 145,49 Q106,35 80,65 Q56,41 22,66 Z","#ebbf63","#523a3c",6)
 eyes=circle(68,99,8,"#231a2a")+circle(117,97,8,"#231a2a")+circle(70,96,2,"white")+circle(119,94,2,"white")
 mouth=path("M83,132 Q101,142 115,129","none","#ab5363",4)
 return f'<g transform="translate({x},{y}) scale({s})">'+body+hair+head+bang+eyes+mouth+'</g>'
def manzo(x,y,s=1):
 horns=path("M29,43 Q-45,10 -24,-57 Q-20,12 50,15 Z","#eedbb0","#182139",7)+path("M129,25 Q196,6 191,-58 Q220,15 164,47 Z","#ead7b3","#172039",7)
 body=path("M7,150 L156,146 L191,321 L-23,321 Z","#253c5c","#11182b",9)+path("M62,153 L106,151 L110,302 L66,304 Z","#e9e5dc","#101422",4)+path("M83,154 L95,201 L78,252 L71,198 Z","#151825")
 head=path("M4,39 Q47,-25 125,8 Q171,22 161,102 Q133,161 43,160 Q-15,131 4,39 Z","#895a37","#172037",9)
 muzzle=path("M37,83 Q91,49 159,94 Q182,131 127,149 Q66,153 29,131 Z","#c99a69","#29202d",6)
 eyes=circle(57,74,7,"#141a23")+path("M44,63 L73,58","none","#171522",6)+circle(148,126,5,"#69482e")
 return f'<g transform="translate({x},{y}) scale({s})">'+horns+body+head+muzzle+eyes+'</g>'
def glitch(x,y,s=1):
 a=circle(96,99,103,"#7033b7")
 a+=rect(12,14,170,152,"#16142e",25,"#ad65ef",12)
 a+=rect(22,23,150,133,"#100e22",19,"#2b3358",5)
 a+=f'<ellipse cx="73" cy="86" rx="10" ry="24" fill="#f6f3ff"/><ellipse cx="119" cy="86" rx="10" ry="24" fill="#f6f3ff"/>'
 a+=rect(-5,67,22,54,"#6636bd",9,"#e5a8ff",4)+rect(178,67,22,54,"#6636bd",9,"#e5a8ff",4)
 a+=path("M7,183 l-23,28 l28,-6 M180,181 l30,30 l-40,-7","#9045d9","#e3b3ff",4)
 return f'<g transform="translate({x},{y}) scale({s})">'+a+'</g>'
def bookseller(x,y,s=1):
 a=rect(13,122,137,176,"#6b5551",30,"#1b2030",7)+circle(85,68,63,"#e1b78d","#1e2130",6)
 a+=path("M19,53 Q30,-20 115,10 Q154,33 148,69 Q105,24 45,38 Z","#51413e","#191a29",6)
 a+=rect(33,70,48,29,"none",9,"#252f3c",5)+rect(90,70,49,29,"none",9,"#252f3c",5)+path("M79,82 L89,82","none","#232936",5)
 a+=path("M45,125 Q88,165 132,121","none","#59423a",10)
 return f'<g transform="translate({x},{y}) scale({s})">'+a+'</g>'
def cast(scene,people,w,h,seed):
 if not people:return ""
 who=people.split(",")
 if scene in ("screens","terminal","flow","correction","notebook","comparison"):
  xs=[80,450,770]
 else: xs=[75,390,720]
 a=[]
 for i,name in enumerate(who):
  x=xs[min(i,len(xs)-1)]
  if name=="lia":a.append(lia(x,max(22,int(h*.28)),.72))
  elif name=="manzo":a.append(manzo(x,max(22,int(h*.25)),.78))
  elif name=="glitch":a.append(glitch(x,max(32,int(h*.30)),.65))
  elif name=="passante":a.append(bookseller(x,max(25,int(h*.26)),.7))
  elif name=="bookseller":a.append(bookseller(x,max(15,int(h*.20)),.9))
 return "".join(a)
def bubble(y,h,speech,frame_idx):
 if not speech:return ""
 a=[]
 bH=120 if len(speech)>1 else 112
 gap=14; available=PAGE_W-55
 cols=len(speech); box_w=(available-gap*(cols-1))/cols
 for j,(speaker,words) in enumerate(speech):
  x=28+j*(box_w+gap)
  a.append(rect(x,y+h-bH-15,box_w,bH,"#fbf6e9",19,"#161c2c",4))
  col=PALETTE.get(speaker,"#c8a56d")
  a.append(rect(x+8,y+h-bH-7,min(193,box_w-16),25,col,4))
  a.append(t(x+20,y+h-bH+13,speaker,15,"#fff" if speaker!="DIDASCALIA" else "#1c2437",900))
  max_chars=26 if cols==2 else 53
  lines=textwrap.wrap(words,max_chars,break_long_words=False,break_on_hyphens=False)
  font=28 if cols==1 else 25
  if len(lines)>3:
   font=22
   lines=textwrap.wrap(words,32 if cols==1 else 25,break_long_words=False)
  for k,line in enumerate(lines[:4]):
   a.append(t(x+21,y+h-bH+48+k*(font+2),line,font,"#171a27",680))
 return "".join(a)
def svg_page(index,title,frames):
 W,H=PAGE_W,PAGE_H
 top=94; bottom=41; gap=12
 ph=(H-top-bottom-gap*(len(frames)-1))/len(frames)
 a=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',defs(),rect(0,0,W,H,"#101221"),rect(0,0,W,94,"#12182d")]
 a += [t(28,56,"ORACLE",53,"#ffffff",950),t(290,56,"CITY",53,"#dc3e48",950),t(690,39,"NUMERO 02",24,"#c9afe6",850),t(690,72,title.upper(),22,"#fff",850)]
 for i,(scene,people,speech) in enumerate(frames):
  y=top+i*(ph+gap)
  a.append(f'<g clip-path="url(#cut{i})"><defs><clipPath id="cut{i}"><rect x="9" y="{y}" width="{W-18}" height="{ph}" rx="4"/></clipPath></defs>')
  a.append(f'<g transform="translate(9 {y})">{scene_art(scene,W-18,ph,100*index+i)}{cast(scene,people,W-18,ph,100*index+i)}</g>')
  a.append('</g>'+rect(9,y,W-18,ph,"none",3,"#060a18",9))
  a.append(bubble(y,ph,speech,i))
 a.append(rect(0,H-bottom,W,bottom,"#13192a"))
 a.append(t(23,H-13,"MANZO · ORACLE CITY · DOMANDA / VERIFICA / RESPONSABILITÀ",14,"#d8d5e4",680))
 a.append(t(W-25,H-12,str(index).zfill(2),24,"#fff",950,"end"))
 a.append('</svg>')
 return ''.join(a)
def logo_data():
 p=Path("theme/manzo-mark.svg")
 return base64.b64encode(p.read_bytes()).decode() if p.exists() else ""
def svg_cover():
 logo=logo_data()
 a=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{PAGE_W}" height="{PAGE_H}" viewBox="0 0 {PAGE_W} {PAGE_H}">',defs(),city_art(PAGE_W,PAGE_H,447),rect(0,0,PAGE_W,PAGE_H,"#050811",0,sw=0)]
 # Cover backdrop: purple / sunset atmospheric windows and city
 a.append('<path d="M0 0H1000V1500H0Z" fill="url(#night)"/>')
 a.append(city_art(PAGE_W,PAGE_H,44))
 a.append(rect(24,24,952,145,"#0a0d20",0,"#e5d4ed",5))
 if logo:a.append(f'<image x="47" y="43" width="95" height="96" href="data:image/svg+xml;base64,{logo}"/>')
 a += [t(165,119,"ORACLE",104,"#faf9f5",950),t(635,119,"CITY",104,"#aa60f2",950)]
 a.append(t(503,198,"UNA CITTÀ TUTT'ALTRO CHE SEMPLICE",30,"#ffffff",850,"middle"))
 a.append(lia(65,620,2.3))
 a.append(manzo(365,595,2.35))
 a.append(glitch(723,747,1.4))
 a.append(papers_art(PAGE_W,PAGE_H,874))
 a.append(rect(0,1100,PAGE_W,400,"#0b0f20"))
 a.append(rect(43,1137,135,120,"#ad66ed",8))
 a.append(t(111,1184,"N.",38,"white",850,"middle"))
 a.append(t(111,1241,"02",80,"white",950,"middle"))
 a.append(t(205,1210,"TRECENTO",95,"#fff",950))
 a.append(t(205,1319,"COPIE",103,"#b16cf2",950))
 a.append(t(55,1444,"FONTI  ·  VERIFICA  ·  CONTESTO  ·  REALTÀ",24,"#ddd7df",750))
 a.append('</svg>')
 return ''.join(a)
HTML_TEMPLATE="""<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ORACLE CITY — Trecento copie | Numero 02 · MANZO AI</title><meta name="description" content="Leggi il Numero 02 del fumetto ORACLE CITY: Trecento copie. Lia, Manzo e Glitch indagano sulle notizie copiate."><link rel="canonical" href="__URL__"><meta property="og:type" content="article"><meta property="og:title" content="ORACLE CITY — Trecento copie"><meta property="og:image" content="__URL__copertina.webp"><style>
:root{color-scheme:dark;--bg:#0b1020;--accent:#ab69ec;--line:#494c68}*{box-sizing:border-box}body{margin:0;background:linear-gradient(#0b1124,#171b30);color:#f8f5fb;font:16px/1.55 system-ui,-apple-system,Segoe UI,sans-serif}a{color:#dbc4ff}header,footer{max-width:1140px;margin:auto;padding:18px;display:flex;flex-wrap:wrap;gap:12px;justify-content:space-between;align-items:center}header a{text-decoration:none;font-weight:700}main{max-width:1040px;margin:auto;padding:12px 18px 50px}.intro{text-align:center;max-width:800px;margin:0 auto 25px}.intro .eyebrow{color:#ceb4f5;text-transform:uppercase;letter-spacing:.14em;font-size:.8rem;font-weight:850}h1{font-size:clamp(2rem,7vw,4.5rem);margin:0;line-height:1.13}h2{color:#e8d6ff;margin:.5rem}.actions{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin:20px auto}.actions a,.actions button{background:#42336f;border:1px solid #9877db;color:#fff;text-decoration:none;padding:12px 16px;border-radius:10px;min-height:44px;font-weight:750;cursor:pointer}.reader{max-width:770px;margin:auto}.reader img{width:100%;height:auto;display:block;background:#10182c;border:2px solid #5c527d;box-shadow:0 16px 44px #0008}.controls{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:15px 0}.controls button,.controls select{border:1px solid #7b7195;background:#222540;color:#fff;border-radius:10px;padding:13px;min-height:44px;font-weight:650}.controls button:disabled{opacity:.35}.controls button{flex:1}.controls select{max-width:155px}details{max-width:770px;margin:24px auto;border:1px solid #51526f;border-radius:12px;padding:18px}details summary{cursor:pointer;font-weight:800}#transcript{white-space:pre-wrap;line-height:1.8;padding:15px 0;color:#e8e6f3}footer{color:#c3bdce;font-size:.84rem;border-top:1px solid #33394d}@media(max-width:500px){.controls select{max-width:105px}.controls button{padding:9px 7px}.actions a{width:100%}}@media print{header,.intro,.controls,details,footer{display:none!important}main{padding:0}.reader{max-width:none}.reader img{border:0;box-shadow:none;width:100%;max-height:98vh;object-fit:contain}}
</style></head><body><header><a href="/manzo-ai/it/risorse/">MANZO AI · Risorse</a><nav><a href="/manzo-ai/it/risorse/oracle-city/">Collana ORACLE CITY</a> · <a href="/manzo-ai/it/risorse/oracle-city/numero-01/">Numero 01</a></nav></header><main><div class="intro"><div class="eyebrow">Fumetto originale · Numero 02</div><h1>ORACLE <span style="color:#c27dff">CITY</span></h1><h2>Trecento copie</h2><p>La biblioteca ha riaperto, ma una notizia falsa continua a circolare. Trecento voci o un'unica origine? Lia, Manzo e Glitch seguono la traccia.</p><div class="actions"><a href="ORACLE_CITY_Numero_02_Trecento_Copie.pdf" download>Scarica il PDF completo</a><a href="#lettore">Leggi online</a><button type="button" onclick="navigator.share?navigator.share({title:'ORACLE CITY — Trecento copie',url:location.href}):navigator.clipboard?.writeText(location.href)">Condividi</button></div></div><section id="lettore" class="reader" aria-label="Lettore fumetto numero 02"><img id="art" src="copertina.webp" alt="Copertina del Numero 02" width="1000" height="1500" fetchpriority="high"><div class="controls"><button id="prev">← Indietro</button><select id="jump" aria-label="Seleziona tavola"></select><button id="next">Avanti →</button></div><p id="position" aria-live="polite"></p></section><details><summary>Trascrizione accessibile della tavola</summary><div id="transcript"></div></details><p style="text-align:center"><a href="/manzo-ai/it/risorse/oracle-city/numero-01/">Rileggi il Numero 01: La risposta perfetta</a></p></main><footer><span>© 2026 MANZO AI · Testo e direzione editoriale umana, illustrazioni realizzate con supporto AI.</span><span>Finzione narrativa · Nessun tracciamento nel lettore</span></footer><script>
const pages=['copertina.webp',...Array.from({length:13},(_,i)=>'pagina-'+String(i).padStart(2,'0')+'.webp')];const texts=__TEXTS__;let pos=0;const img=document.querySelector('#art'),jump=document.querySelector('#jump');pages.forEach((p,i)=>{let o=document.createElement('option');o.value=i;o.textContent=i?'Tavola '+String(i-1).padStart(2,'0'):'Copertina';jump.append(o)});function show(n){pos=Math.max(0,Math.min(pages.length-1,n));img.src=pages[pos];img.alt=pos?'Tavola '+(pos-1)+' di Trecento copie':'Copertina di Trecento copie';jump.value=pos;document.querySelector('#position').textContent=(pos+1)+' di '+pages.length;document.querySelector('#transcript').textContent=pos?texts[pos-1]:'ORACLE CITY — Numero 02: Trecento copie';document.querySelector('#prev').disabled=pos===0;document.querySelector('#next').disabled=pos===pages.length-1;if(pos+1<pages.length){let n=new Image();n.src=pages[pos+1]}}document.querySelector('#prev').onclick=()=>show(pos-1);document.querySelector('#next').onclick=()=>show(pos+1);jump.onchange=()=>show(+jump.value);document.onkeydown=e=>{if(e.target?.matches('input,select,textarea'))return;if(e.key==='ArrowRight')show(pos+1);if(e.key==='ArrowLeft')show(pos-1)};let tx=0;img.addEventListener('touchstart',e=>{tx=e.changedTouches[0].screenX},{passive:true});img.addEventListener('touchend',e=>{let dx=e.changedTouches[0].screenX-tx;if(Math.abs(dx)>65)show(pos+(dx<0?1:-1))},{passive:true});show(0);
</script></body></html>"""
def patch_site(site):
 # Add new issue link to existing first issue without tampering with its artwork.
 f=site/"it/risorse/oracle-city/numero-01/index.html"
 html=f.read_text(encoding="utf-8")
 needle="</main>"
 addition='<p style="text-align:center;padding:15px"><a href="/manzo-ai/it/risorse/oracle-city/numero-02/" style="display:inline-block;background:#573d8d;color:white;border-radius:12px;padding:15px;font-weight:850;text-decoration:none">Continua la storia: Numero 02 · Trecento copie →</a></p>'
 if ROUTE not in html:
  assert needle in html
  html=html.replace(needle,addition+needle)
  f.write_text(html,encoding="utf-8")
 # Resources: new block, all three language hubs.
 for loc,heading,desc in [
  ("it/risorse/index.html","ORACLE CITY · NUMERO 02","Trecento copie — La notizia è stata corretta, ma continua a circolare."),
  ("es/recursos/index.html","ORACLE CITY · NÚMERO 02","Trecento copie — Segunda entrega disponible en italiano."),
  ("en/resources/index.html","ORACLE CITY · ISSUE 02","Trecento copie — Second issue available in Italian.")]:
  f=site/loc
  text=f.read_text(encoding="utf-8")
  if ROUTE not in text:
   block=f'<section aria-label="{E(heading)}" style="max-width:1050px;margin:1.3rem auto;padding:1.1rem;background:#f6f0ff;color:#1c2240;border:1px solid #bb9ae4;border-radius:16px;display:flex;gap:1rem;align-items:center;flex-wrap:wrap"><a href="{ROUTE}"><img src="{ROUTE}copertina.webp" width="94" height="141" alt="Copertina Oracle City Numero 02" style="border-radius:7px;box-shadow:0 5px 12px #0003"></a><div style="flex:1 1 220px"><strong style="color:#654393">{E(heading)}</strong><p>{E(desc)}</p><a href="{ROUTE}" style="display:inline-block;background:#513583;color:white;border-radius:10px;padding:.7rem 1.1rem;text-decoration:none;font-weight:700">Leggi il Numero 02 →</a></div></section>'
   assert "</main>" in text
   f.write_text(text.replace("</main>",block+"</main>"),encoding="utf-8")
 sitemap=site/"sitemap.xml"
 xml=sitemap.read_text(encoding="utf-8")
 for route in ("/manzo-ai/it/risorse/oracle-city/","/manzo-ai/"+BASE+"/"):
  url="https://manzo8b.github.io"+route
  if url not in xml:
   assert "</urlset>" in xml
   xml=xml.replace("</urlset>",f'<url><loc>{url}</loc></url></urlset>')
 sitemap.write_text(xml,encoding="utf-8")
def main():
 p=argparse.ArgumentParser();p.add_argument("--site",required=True);p.add_argument("--edition",required=False)
 args=p.parse_args()
 site=Path(args.site);target=site/BASE;target.mkdir(parents=True,exist_ok=True)
 chapter_svg=[svg_cover()]+[svg_page(i,title,frames) for i,(title,frames) in enumerate(PAGES)]
 out_names=["copertina"]+[f"pagina-{i:02d}" for i in range(13)]
 rendered=[]
 for name,svg in zip(out_names,chapter_svg):
  (target/(name+".svg")).write_text(svg,encoding="utf-8")
  png=cairosvg.svg2png(bytestring=svg.encode("utf-8"),output_width=PAGE_W,output_height=PAGE_H)
  im=Image.open(BytesIO(png)).convert("RGB")
  im.save(target/(name+".webp"),"WEBP",quality=88,method=5)
  rendered.append(im)
 pdf=target/"ORACLE_CITY_Numero_02_Trecento_Copie.pdf"
 c=canvas.Canvas(str(pdf),pagesize=A4)
 for im in rendered:
  im.thumbnail((1488,2105))
  buff=BytesIO();im.save(buff,format="JPEG",quality=92,optimize=True);buff.seek(0)
  c.drawImage(ImageReader(buff),0,0,width=A4[0],height=A4[1])
  c.showPage()
 c.setTitle("ORACLE CITY — Numero 02: Trecento copie");c.setAuthor("MANZO AI");c.save()
 transcripts=[]
 for title,frames in PAGES:
  s=[title]
  for _,_,speech in frames:
   for who,line in speech:s.append(who+": "+line)
  transcripts.append("\n".join(s))
 import json
 (target/"index.html").write_text(HTML_TEMPLATE.replace("__URL__",SITE_URL).replace("__TEXTS__",json.dumps(transcripts,ensure_ascii=False)),encoding="utf-8")
 hub=site/"it/risorse/oracle-city/index.html"
 hub.parent.mkdir(parents=True,exist_ok=True)
 hub.write_text(f'<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ORACLE CITY · Collana digitale MANZO AI</title><style>body{{background:#10172a;color:white;font:18px/1.6 system-ui;margin:0}}main{{max-width:900px;margin:auto;padding:35px}}a{{color:#dfc2ff}}.issues{{display:flex;gap:20px;flex-wrap:wrap}}article{{width:min(340px,100%);border:1px solid #575272;border-radius:15px;padding:18px}}img{{width:100%;height:auto;border-radius:9px}}</style><main><a href="/manzo-ai/it/risorse/">← Risorse MANZO AI</a><h1>ORACLE CITY</h1><p>Una città tutt’altro che semplice · In questa città, altro che storie</p><div class="issues"><article><a href="/manzo-ai/it/risorse/oracle-city/numero-01/"><img src="numero-01/copertina.webp" alt="Copertina Numero 01"></a><h2>01 — La risposta perfetta</h2><a href="numero-01/">Leggi il fumetto</a></article><article><a href="numero-02/"><img src="numero-02/copertina.webp" alt="Copertina Numero 02"></a><h2>02 — Trecento copie</h2><a href="numero-02/">Leggi il fumetto</a></article></div><p>Realizzato con supporto AI e revisione editoriale umana.</p></main></html>',encoding="utf-8")
 patch_site(site)
 assert len(list(target.glob("pagina-??.webp")))==13
 assert len(rendered)==14 and pdf.stat().st_size>1000000
 print(f"ORACLE CITY 02 READY: 14 illustrated pages, {pdf.stat().st_size} PDF bytes")
if __name__=="__main__":main()
