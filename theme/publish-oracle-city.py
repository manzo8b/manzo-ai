#!/usr/bin/env python3
"""Publish the approved Oracle City compact comic as an additive overlay to MANZO AI."""
from pathlib import Path
from html import escape
import argparse, shutil, re, xml.etree.ElementTree as ET

ROUTE='/manzo-ai/it/risorse/oracle-city/numero-01/'
SUFFIX='it/risorse/oracle-city/numero-01'
EXPECTED=['index.html','copertina.jpg','copertina.webp','ORACLE_CITY_Numero_01_La_Risposta_Perfetta.pdf']+[f'pagina-{n:02d}.webp' for n in range(1,10)]

CARD={
 'it/risorse/index.html': ('ORACLE CITY · Fumetto digitale', 'La risposta perfetta · Numero 01', 'Una risposta per ogni domanda. Ma chi verifica la risposta? Leggi il fumetto originale a colori, con Lia, Manzo e Glitch.', 'Leggi il fumetto'),
 'es/recursos/index.html': ('ORACLE CITY · Cómic digital', 'La risposta perfetta · Número 01', 'Un cómic original de MANZO AI. Primera edición disponible en italiano.', 'Leer en italiano'),
 'en/resources/index.html': ('ORACLE CITY · Digital comic', 'La risposta perfetta · Issue 01', 'An original MANZO AI comic. First edition currently available in Italian.', 'Read in Italian')
}

def patch_card(root: Path, rel: str, entry):
    f=root/rel
    if not f.is_file():
        raise RuntimeError(f'Missing resources hub {rel}')
    html=f.read_text(encoding='utf-8')
    if ROUTE in html:
        print(f'Skip duplicate link: {rel}')
        return
    heading,sub,description,button=map(escape,entry)
    block=f'''\n<section aria-label="{heading}" class="oracle-city-feature" style="margin:2rem auto;max-width:1050px;padding:1rem 1.1rem;border:1px solid #bea8d9;border-radius:16px;background:linear-gradient(120deg,#f5f0ff,#fdfaf4);color:#19233b;display:flex;flex-wrap:wrap;align-items:center;gap:1.3rem;box-shadow:0 8px 30px #21213b18">\n <a href="{ROUTE}" aria-label="{button}: Oracle City" style="flex:0 0 140px;max-width:32%;"><img src="{ROUTE}copertina.webp" alt="Copertina Oracle City numero 01" width="140" height="198" loading="lazy" style="width:100%;height:auto;border-radius:7px;box-shadow:0 8px 16px #0003"></a>\n <div style="flex:1 1 220px"><p style="color:#67439A;font-weight:850;font-size:.82rem;letter-spacing:.08em;text-transform:uppercase;margin:.3rem 0">{heading}</p><h2 style="color:#172444;font-size:clamp(1.35rem,3vw,1.8rem);line-height:1.22;margin:0 0 .35rem">{sub}</h2><p style="font-size:1rem;line-height:1.5;margin:.5rem 0 1rem;color:#34405d">{description}</p><a href="{ROUTE}" style="display:inline-block;background:#41347b;color:white;text-decoration:none;font-weight:750;padding:.78rem 1.15rem;border-radius:9px;min-height:44px">{button}</a></div>\n</section>\n'''
    match=re.search(r'</main\s*>',html,re.IGNORECASE)
    if not match:
        raise RuntimeError(f'No closing main found in {rel}; refusing risky patch')
    html=html[:match.start()]+block+html[match.start():]
    f.write_text(html,encoding='utf-8')


def patch_sitemap(root: Path):
    f=root/'sitemap.xml'
    text=f.read_text(encoding='utf-8')
    url='https://manzo8b.github.io'+ROUTE
    if url in text:
        return
    m=re.search(r'</urlset\s*>',text,re.I)
    if not m:
        raise RuntimeError('Unexpected sitemap format: no closing urlset')
    text=text[:m.start()]+f'<url><loc>{url}</loc></url>\n'+text[m.start():]
    ET.fromstring(text)
    f.write_text(text,encoding='utf-8')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--site',required=True)
    parser.add_argument('--edition',required=True)
    a=parser.parse_args()
    site=Path(a.site); edition=Path(a.edition)
    if not all((edition/n).is_file() and (edition/n).stat().st_size>500 for n in EXPECTED):
        missing=[n for n in EXPECTED if not (edition/n).is_file() or (edition/n).stat().st_size<=500]
        raise RuntimeError('Comic assets missing or too small: '+', '.join(missing))
    target=site/SUFFIX
    target.mkdir(parents=True,exist_ok=True)
    for n in EXPECTED:
        shutil.copy2(edition/n,target/n)
    for rel,card in CARD.items():
        patch_card(site,rel,card)
    patch_sitemap(site)
    assert (target/'index.html').is_file()
    assert sum((target/f'pagina-{i:02d}.webp').is_file() for i in range(1,10))==9
    print('ORACLE CITY NUMERO 01 published to static artifact, 10 illustrated pages, PDF and 3 resource links')

if __name__=='__main__': main()