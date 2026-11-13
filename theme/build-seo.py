#!/usr/bin/env python3
"""Deterministic post-build SEO for MANZO AI GitHub Pages project site.
Runs AFTER all editorial overlays; never modifies the authoritative release ZIP.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from html import escape, unescape
from pathlib import Path
import re
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

XML_NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('', XML_NS)
LOCALES = {'it': ('Mappa del sito', 'Tutte le risorse educative'),
           'es': ('Mapa del sitio', 'Todos los recursos educativos'),
           'en': ('Site map', 'All educational resources')}
GROUP_NAMES = {
 'it': {'academy':'Impara e Academy', 'prompt':'Prompt Mastery e laboratorio', 'critical':'Pensiero critico', 'media':'Risorse e media', 'other':'Altri percorsi'},
 'es': {'academy':'Aprende y Academia', 'prompt':'Prompt Mastery y laboratorio', 'critical':'Pensamiento crítico', 'media':'Recursos y medios', 'other':'Otros itinerarios'},
 'en': {'academy':'Learn and Academy', 'prompt':'Prompt Mastery and labs', 'critical':'Critical thinking', 'media':'Resources and media', 'other':'Other pathways'},
}
NAV = {
 'it': [('AI Academy','academy/'), ('Prompt Mastery','prompt-mastery/'), ('Laboratorio tecnico','prompt-mastery/laboratorio-tecnico/'), ('AI Brain Challenge','pensiero-critico/'), ('Risorse','risorse/'), ('Video e podcast','video-e-slide/')],
 'es': [('AI Academia','academia/'), ('Prompt Mastery','prompt-mastery/'), ('Laboratorio técnico','prompt-mastery/laboratorio-tecnico/'), ('AI Brain Challenge','pensamiento-critico/'), ('Recursos','recursos/'), ('Vídeos y podcast','videos-y-diapositivas/')],
 'en': [('AI Academy','academy/'), ('Prompt Mastery','prompt-mastery/'), ('Technical lab','prompt-mastery/technical-lab/'), ('AI Brain Challenge','critical-thinking/'), ('Resources','resources/'), ('Videos and podcast','videos-and-slides/')],
}

def url_for(path: Path, site: Path, base: str) -> str:
    rel = path.parent.relative_to(site).as_posix()
    return base + (rel + '/' if rel != '.' else '')

def page_title(text: str, fallback: str) -> str:
    match = re.search(r'<title\b[^>]*>(.*?)</title\s*>', text, re.I | re.S)
    if not match: return fallback
    label = re.sub(r'<[^>]*>', '', unescape(match.group(1)))
    label = re.sub(r'\s*[|—–]\s*MANZO AI\s*$', '', label, flags=re.I).strip()
    return label[:110] or fallback

def group_for(rel: str) -> str:
    if any(segment in rel for segment in ('/academy/', '/academia/', '/impara/', '/aprende/', '/learn/')): return 'academy'
    if '/prompt-mastery/' in rel: return 'prompt'
    if any(segment in rel for segment in ('/pensiero-critico/', '/pensamiento-critico/', '/critical-thinking/')): return 'critical'
    if any(segment in rel for segment in ('/risorse/', '/recursos/', '/resources/', '/video-e-slide/', '/videos-y-diapositivas/', '/videos-and-slides/', '/podcast/', '/slides/', '/diapositivas/')): return 'media'
    return 'other'

def sitemap_page(site: Path, base: str, locale: str) -> None:
    heading, intro = LOCALES[locale]
    pages = sorted((site / locale).rglob('index.html'))
    sections: dict[str, list[tuple[str,str]]] = defaultdict(list)
    for page in pages:
        if page.parent == site / locale: continue
        text = page.read_text(encoding='utf-8')
        if re.search(r'<meta\b[^>]*name=["\x27]robots["\x27][^>]*noindex', text, re.I): continue
        rel = page.relative_to(site).as_posix()
        sections[group_for('/'+rel)].append((page_title(text, page.parent.name), url_for(page, site, base)))
    css = 'body{margin:0;background:white;color:#18212b;font:16px/1.65 system-ui,sans-serif}header,main,footer{max-width:1080px;margin:auto;padding:24px}h1{font-size:clamp(2rem,5vw,3.4rem);letter-spacing:-.04em}h2{font-size:1.35rem;margin:32px 0 12px}a{color:#17578b}a:focus-visible{outline:3px solid #b13f28;outline-offset:3px}ul{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:10px}li a{display:block;padding:12px 14px;border:1px solid #cbd8df;border-radius:12px;text-decoration:none;background:#f5f8fb}li a:hover{background:#e7f1fc}p{color:#4f5c68}'
    parts = [f'<!doctype html><html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(heading)} | MANZO AI</title><meta name="description" content="{escape(intro)}: MANZO AI Knowledge &amp; Prompt Lab."><style>{css}</style></head><body>',
             f'<header><a href="{base}{locale}/">MANZO AI · {locale.upper()}</a></header><main><h1>{escape(heading)}</h1><p>{escape(intro)}</p>']
    for group in ('academy','prompt','critical','media','other'):
        entries = sections.get(group, [])
        if entries:
            parts.append(f'<section><h2>{escape(GROUP_NAMES[locale][group])}</h2><ul>')
            parts.extend(f'<li><a href="{escape(link,quote=True)}">{escape(title)}</a></li>' for title,link in entries)
            parts.append('</ul></section>')
    parts.append(f'</main><footer><a href="{base}{locale}/">MANZO AI</a></footer></body></html>')
    output = site / locale / {'it':'mappa-del-sito','es':'mapa-del-sitio','en':'site-map'}[locale] / 'index.html'
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(''.join(parts),encoding='utf-8')

def update_page(page: Path, site: Path, base: str) -> None:
    html = page.read_text(encoding='utf-8')
    url = url_for(page,site,base)
    canonical = f'<link rel="canonical" href="{escape(url,quote=True)}">'
    html = re.sub(r'<link\b(?=[^>]*\brel\s*=\s*["\x27]canonical["\x27])[^>]*>\s*','',html,flags=re.I)
    insert = canonical
    if not re.search(r'<meta\b(?=[^>]*\bproperty\s*=\s*["\x27]og:site_name["\x27])[^>]*>',html,re.I):
        insert += '<meta property="og:site_name" content="MANZO AI">'
    if page == site/'index.html' or page in [site/loc/'index.html' for loc in LOCALES]:
        html = re.sub(r'<link\b(?=[^>]*\bhreflang\s*=)[^>]*>\s*','',html,flags=re.I)
        insert += ''.join(f'<link rel="alternate" hreflang="{loc}" href="{base}{loc}/">' for loc in LOCALES)
        insert += f'<link rel="alternate" hreflang="x-default" href="{base}">'
    if page in [site/loc/'index.html' for loc in LOCALES]:
        loc = page.parent.name
        navlinks = [(label,base+loc+'/'+route) for label,route in NAV[loc] if (site/loc/route/'index.html').is_file()]
        sm = {'it':'Mappa del sito','es':'Mapa del sitio','en':'Site map'}[loc]
        smpath = {'it':'mappa-del-sito','es':'mapa-del-sitio','en':'site-map'}[loc]
        navlinks.append((sm,base+loc+'/'+smpath+'/'))
        if 'data-manzo-seo-nav="1"' not in html and navlinks:
            nav = f'<nav data-manzo-seo-nav="1" aria-label="{escape(sm)}" style="margin:3rem auto;max-width:1100px;padding:1.5rem;border:1px solid #cbd8df;border-radius:18px;background:#f5f8fb"><h2 style="margin:0 0 1rem;font-size:1.35rem;color:#1b334c">{escape(sm)}</h2><div style="display:flex;gap:.7rem;flex-wrap:wrap">'
            nav += ''.join(f'<a href="{escape(link,quote=True)}" style="display:inline-block;border:1px solid #b9c9d8;border-radius:9px;background:white;color:#1a5275;padding:.65rem .9rem;text-decoration:none;font-weight:600">{escape(label)}</a>' for label,link in navlinks)
            nav += '</div></nav>'
            match = re.search(r'</main\s*>',html,re.I)
            if match: html = html[:match.start()]+nav+html[match.start():]
            else: raise RuntimeError(f'No main in locale home: {page}')
    match = re.search(r'</head\s*>',html,re.I)
    if not match: raise RuntimeError(f'Missing head close: {page}')
    html = html[:match.start()]+insert+html[match.start():]
    page.write_text(html,encoding='utf-8')

def publish(site: Path, base: str) -> int:
    if not (site/'index.html').is_file(): raise RuntimeError('Missing site landing page')
    base = base.rstrip('/')+'/'
    if urlparse(base).scheme != 'https' or not urlparse(base).path.endswith('/manzo-ai/'):
        raise ValueError('Provide the HTTPS GitHub Pages project root ending /manzo-ai/')
    for locale in LOCALES:
        if not (site/locale/'index.html').is_file(): raise RuntimeError('Missing locale: '+locale)
        sitemap_page(site,base,locale)
    pages = sorted(site.rglob('index.html'))
    for page in pages: update_page(page,site,base)
    root = ET.Element(f'{{{XML_NS}}}urlset')
    urls = []
    for page in pages:
        html = page.read_text(encoding='utf-8')
        if re.search(r'<meta\b[^>]*name=["\x27]robots["\x27][^>]*noindex',html,re.I): continue
        url = url_for(page,site,base)
        ET.SubElement(ET.SubElement(root,f'{{{XML_NS}}}url'),f'{{{XML_NS}}}loc').text = url
        urls.append(url)
    assert len(set(urls)) == len(urls), 'Duplicate URLs in sitemap'
    tree = ET.ElementTree(root)
    ET.indent(tree,space='  ')
    tree.write(site/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    parsed = ET.parse(site/'sitemap.xml')
    got = [node.text for node in parsed.findall('.//{'+XML_NS+'}loc')]
    assert got == urls and all(x.startswith(base) for x in got)
    for locale in LOCALES:
        home = (site/locale/'index.html').read_text(encoding='utf-8')
        assert 'data-manzo-seo-nav="1"' in home
        assert 'hreflang="x-default"' in home
    print(f'MANZO AI SEO: {len(urls)} canonical URLs; 3 human-readable sitemaps; 3 linked locale homepages; XML validated.')
    print('Note: a robots.txt under /manzo-ai/ is not a host-root robots.txt. Configure the host root separately if needed.')
    return len(urls)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--site',type=Path,required=True)
    parser.add_argument('--base-url',required=True)
    args = parser.parse_args()
    publish(args.site,args.base_url)
