#!/usr/bin/env python3
"""Publish a self-hosted Prompt Engineering lesson when its real MP4 is available.
The source release ZIP is never modified. Cards are added only for playable media.
"""
from __future__ import annotations
from html import escape
from pathlib import Path
import argparse
import json
import re
import shutil
import subprocess

ROUTE = '/manzo-ai/it/video-e-slide/prompt-engineering/'
ORIGIN = 'https://manzo8b.github.io'
PUBLIC = ORIGIN + ROUTE
ASSETS = '/manzo-ai/assets/media/prompt-engineering/'
FILE = 'Prompt_Engineering.mp4'
SUBTITLE = 'Prompt_Engineering.it.vtt'

HUBS = {
    'it/video-e-slide/index.html': ('VIDEO LEZIONE · 7 MIN 54 SEC', 'Prompt Engineering: dalla domanda al metodo', 'Come progettare prompt più precisi, verificare le risposte e migliorare i risultati con esercizi concreti.', 'Guarda la video lezione'),
    'it/risorse/index.html': ('NUOVA RISORSA · VIDEO', 'Prompt Engineering: una guida video in italiano', 'Una lezione visuale di circa otto minuti, dalle prime domande fino alla verifica dei risultati.', 'Apri la risorsa'),
    'it/prompt-mastery/index.html': ('APPROFONDIMENTO · VIDEO', 'Prompt Engineering: esempi e metodo', 'Dal prompt generico a istruzioni con obiettivi, contesto e criteri di valutazione.', 'Guarda il video'),
    'es/videos-y-diapositivas/index.html': ('VÍDEO · AUDIO EN ITALIANO', 'Prompt Engineering: del primer mensaje al método', 'Lección de unos ocho minutos sobre instrucciones, ejemplos y verificación. Audio original en italiano.', 'Ver vídeo en italiano'),
    'es/recursos/index.html': ('RECURSO · VÍDEO EN ITALIANO', 'Prompt Engineering: guía visual', 'Un vídeo práctico con audio en italiano sobre cómo diseñar mejores instrucciones para la IA.', 'Abrir recurso'),
    'en/videos-and-slides/index.html': ('VIDEO · ITALIAN AUDIO', 'Prompt Engineering: from a question to a method', 'An eight-minute visual lesson on instructions, examples and verification. Original Italian audio.', 'Watch Italian video'),
    'en/resources/index.html': ('RESOURCE · ITALIAN VIDEO', 'Prompt Engineering: a visual introduction', 'Learn how to structure, test and improve instructions. Italian spoken audio.', 'Open resource'),
}

def patch_hub(page: Path, text: tuple[str,str,str,str]) -> bool:
    if not page.exists():
        print('Video hub not found, skipped:', page)
        return False
    html = page.read_text(encoding='utf-8')
    if 'data-manzo-prompt-video="1"' in html:
        return False
    kicker, title, description, label = map(escape,text)
    card = f'''
<section data-manzo-prompt-video="1" aria-label="{title}" style="margin:2.2rem auto;max-width:1100px;padding:clamp(1.1rem,3vw,2rem);background:#fff;border:2px solid #c5d8e8;border-top:5px solid #d95328;border-radius:19px;box-shadow:0 13px 38px #16304516;color:#172332">
  <p style="margin:0 0 .6rem;color:#9c3b1d;letter-spacing:.09em;text-transform:uppercase;font-size:.8rem;font-weight:800">{kicker}</p>
  <h2 style="color:#132941;line-height:1.2;letter-spacing:-.025em;font-size:clamp(1.4rem,3vw,2rem);margin:.3rem 0 .7rem">{title}</h2>
  <p style="color:#33465a;line-height:1.7;margin:0 0 1rem">{description}</p>
  <a href="{ROUTE}" style="display:inline-block;padding:.85rem 1.15rem;border-radius:10px;background:#1a5381;color:#fff;font-weight:750;text-decoration:none">{label} →</a>
</section>
'''
    close = re.search(r'</main\s*>',html,re.I)
    if not close:
        raise RuntimeError('No closing main element in '+str(page))
    page.write_text(html[:close.start()]+card+html[close.start():],encoding='utf-8')
    return True

def video_page(has_subtitles:bool, has_cover:bool, upload_date: str | None = None) -> str:
    title = 'Prompt Engineering: dalla domanda al metodo professionale | MANZO AI'
    description = 'Una lezione video di 7 minuti e 54 secondi per imparare a progettare prompt chiari, valutare le risposte dell’intelligenza artificiale e migliorare il proprio metodo.'
    cover_url = ORIGIN + ASSETS + 'copertina.jpg'
    media_url = ORIGIN + ASSETS + FILE
    graph = {
        '@context':'https://schema.org',
        '@type':'VideoObject',
        'name':'Prompt Engineering: dalla domanda al metodo professionale',
        'description':description,
        'inLanguage':'it-IT',
        'duration':'PT7M54S',
        'contentUrl':media_url,
        'embedUrl':PUBLIC,
        'thumbnailUrl':cover_url if has_cover else ORIGIN+'/manzo-ai/logo.svg',
        'publisher':{'@type':'Organization','name':'MANZO AI','url':ORIGIN+'/manzo-ai/'}
    }
    if upload_date:
        graph['uploadDate'] = upload_date
    subs = ('<track kind="captions" src="'+ASSETS+SUBTITLE+'" srclang="it" label="Italiano" default>' if has_subtitles else '')
    poster = (' poster="'+ASSETS+'copertina.jpg"' if has_cover else '')
    return f'''<!doctype html>
<html lang="it"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description,quote=True)}">
<link rel="canonical" href="{PUBLIC}">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="video.other"><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:url" content="{PUBLIC}">
''' + (f'<meta property="og:image" content="{cover_url}">' if has_cover else '') + f'''
<meta property="og:video" content="{media_url}">
<script type="application/ld+json">{json.dumps(graph,ensure_ascii=False)}</script>
<link rel="stylesheet" href="/manzo-ai/style.css">
<style>
:root{{color-scheme:light}}body{{margin:0;background:#fff;color:#172331;font-family:system-ui,-apple-system,"Segoe UI",sans-serif;line-height:1.65}}
header,main,footer{{max-width:1100px;margin:auto;padding:24px clamp(18px,4vw,48px)}}
header{{display:flex;justify-content:space-between;gap:14px;align-items:center;border-bottom:1px solid #dce6ee}}
header a,footer a{{color:#205981;text-decoration:none;font-weight:650}}
header img{{width:42px;height:42px}}
.brand{{display:flex;gap:12px;align-items:center;font-weight:850}}
.eyebrow{{font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;color:#ae4323;font-weight:800}}
h1{{font-size:clamp(2.1rem,5.4vw,4rem);line-height:1.08;letter-spacing:-.055em;max-width:880px;margin:.5rem 0 1.2rem}}
.lead{{font-size:clamp(1.05rem,2.1vw,1.3rem);color:#3c5266;max-width:780px}}
.badges{{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0 24px}}
.badges span{{font-size:.85rem;font-weight:650;border-radius:18px;padding:5px 12px;background:#eaf3fb;color:#1f5274}}
figure{{margin:0 0 25px}}video{{display:block;width:100%;height:auto;aspect-ratio:16/9;background:#102238;border-radius:16px;box-shadow:0 22px 52px #16273922}}
section{{border:1px solid #cddde9;border-top:4px solid #1f628e;border-radius:16px;padding:clamp(16px,3vw,26px);margin:20px 0;background:#fff}}
h2{{font-size:1.45rem;letter-spacing:-.025em;margin:0 0 12px}}ul{{padding-left:1.3rem}}li{{margin:.4rem 0}}
.actions{{display:flex;gap:12px;flex-wrap:wrap;margin-top:15px}}.btn{{display:inline-block;border-radius:10px;padding:12px 18px;background:#1d5881;color:white;text-decoration:none;font-weight:700}}.btn-alt{{background:#edf4fb;color:#1d5881}}
.small{{color:#52667b;font-size:.93rem}}
a:focus-visible{{outline:3px solid #d95328;outline-offset:4px}}
footer{{padding-bottom:40px;border-top:1px solid #dce6ee}}
@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important;animation:none!important}}}}
</style></head>
<body>
<header><div class="brand"><img src="/manzo-ai/assets/manzo-mark.svg" alt=""><span>MANZO AI</span></div><a href="/manzo-ai/it/video-e-slide/">← Video e slide</a></header>
<main>
<p class="eyebrow">MANZO AI · VIDEO LEZIONE 01</p>
<h1>Prompt Engineering.<br>Dalla domanda al metodo.</h1>
<p class="lead">Non basta chiedere all’AI: bisogna saper definire il compito, stabilire i criteri di qualità e verificare il risultato. Questo video introduce un percorso pratico per cominciare.</p>
<div class="badges"><span>7 min 54 s</span><span>Livello: base → intermedio</span><span>Lingua: italiano</span><span>Formato: video 16:9</span></div>
<figure>
<video controls playsinline preload="metadata"{poster} aria-label="Video lezione MANZO AI sul Prompt Engineering">
<source src="{ASSETS}{FILE}" type="video/mp4">{subs}
Il browser non supporta la riproduzione video. Puoi scaricare il file MP4 dal collegamento sottostante.
</video>
<figcaption class="small">Video didattico realizzato con NotebookLM e curatela editoriale del progetto MANZO AI.</figcaption>
<div class="actions"><a class="btn" href="{ASSETS}{FILE}" download>Scarica il video MP4</a><a class="btn btn-alt" href="/manzo-ai/it/prompt-mastery/">Approfondisci Prompt Mastery</a></div>
</figure>
<section><h2>Che cosa imparerai</h2>
<ul><li>Come distinguere un prompt generico da un’istruzione utile e valutabile.</li><li>Le cinque domande essenziali: obiettivo, contesto, destinatario, formato e qualità.</li><li>Come usare esempi e strutture più precise per guidare la risposta.</li><li>Perché una risposta convincente non è necessariamente corretta.</li><li>Il ciclo professionale: definizione, generazione, verifica, miglioramento e iterazione.</li></ul>
</section>
<section><h2>Continua a imparare</h2>
<p>Il video è un punto di partenza. Usa il laboratorio e le risorse della piattaforma per sperimentare il metodo su problemi reali.</p>
<div class="actions"><a class="btn btn-alt" href="/manzo-ai/it/risorse/">Esplora le risorse</a><a class="btn btn-alt" href="/manzo-ai/it/prompt-mastery/laboratorio-tecnico/">Apri il laboratorio tecnico</a><a class="btn btn-alt" href="/manzo-ai/it/">Torna alla Academy</a></div>
</section>
<section><h2>Prometeus Marcelus e la Biblioteca</h2>
<p>Per passare dalle tecniche introduttive a un metodo operativo, puoi esplorare Prometeus Marcelus: un percorso che parte dalla comprensione del problema, organizza la richiesta e introduce criteri di verifica. La Biblioteca raccoglie esempi storici da studiare e adattare criticamente; la loro presenza non equivale a una validazione automatica.</p>
<div class="actions"><a class="btn btn-alt" href="https://manzo8b.github.io/marcelus-v-v01/it/library/" target="_blank" rel="noopener noreferrer">Esplora la Biblioteca Prometeus Marcelus ↗</a></div>
</section>
<section><h2>Produzione, fonti e trasparenza</h2>
<p>Video generato attraverso Google NotebookLM a partire da materiali didattici preparati per MANZO AI. Le spiegazioni hanno finalità formative; esempi e risposte di AI devono essere verificati rispetto al contesto e alle fonti appropriate.</p>
<p class="small">La produzione sintetica del video non equivale a una validazione scientifica autonoma dei suoi contenuti.</p>
</section>
</main>
<footer>© MANZO AI · MARCELUS AI LAB · <a href="/manzo-ai/it/">Home</a></footer>
</body></html>'''

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--site',required=True,type=Path)
    p.add_argument('--edition',required=True,type=Path)
    args = p.parse_args()
    src = args.edition / FILE
    if not src.is_file():
        print('MANZO AI Prompt Engineering: MP4 not yet committed; no empty player or broken links published.')
        return
    if src.stat().st_size < 1_000_000:
        raise RuntimeError('Prompt video MP4 is unexpectedly small: '+str(src))
    site = args.site
    if not (site/'it/risorse/index.html').is_file():
        raise RuntimeError('Expected MANZO AI resources page not found')
    dest = site/'assets/media/prompt-engineering'
    dest.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src,dest/FILE)
    has_subs = (args.edition/SUBTITLE).is_file()
    if has_subs:
        shutil.copy2(args.edition/SUBTITLE,dest/SUBTITLE)
    cover = dest/'copertina.jpg'
    ffmpeg = shutil.which('ffmpeg')
    if ffmpeg:
        run = subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-y','-ss','4','-i',str(src),'-frames:v','1','-q:v','3',str(cover)],capture_output=True,text=True)
        if run.returncode or not cover.exists() or cover.stat().st_size < 1000:
            print('Warning: thumbnail extraction skipped:',run.stderr[-300:])
            cover.unlink(missing_ok=True)
    target = site/'it/video-e-slide/prompt-engineering/index.html'
    target.parent.mkdir(parents=True,exist_ok=True)
    # Read the media file's actual most recent Git commit date for video-rich metadata.
    # Full history is fetched by the publishing workflow; never invent a date.
    rel_src = src.relative_to(Path.cwd()) if src.is_relative_to(Path.cwd()) else src
    git_date = subprocess.run(['git','log','-1','--format=%cI','--',str(rel_src)],capture_output=True,text=True)
    upload_date = git_date.stdout.strip() if git_date.returncode == 0 and re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T.*',git_date.stdout.strip()) else None
    target.write_text(video_page(has_subs,cover.is_file(),upload_date),encoding='utf-8')
    updated = []
    for rel,titles in HUBS.items():
        if patch_hub(site/rel,titles):updated.append(rel)
    assert (dest/FILE).stat().st_size == src.stat().st_size
    assert 'VideoObject' in target.read_text(encoding='utf-8')
    print('MANZO AI Prompt Engineering: video published, page created, cards added to',len(updated),'hub pages.')
    print('Video size:',(dest/FILE).stat().st_size,'thumbnail:',cover.exists(),'captions:',has_subs)

if __name__=='__main__':
    main()
