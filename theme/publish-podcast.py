#!/usr/bin/env python3
"""Additive MANZO AI podcast publication overlay. Never rewrites the release ZIP."""
from pathlib import Path
from html import escape
import argparse
import re
import shutil
import xml.etree.ElementTree as ET

ROUTE = "/manzo-ai/it/podcast/episodio-00/"
PUBLIC = "https://manzo8b.github.io" + ROUTE
MEDIA_ROUTE = "/manzo-ai/assets/podcast/ep00/"
VIDEO_NAME = "manzo-ai-ep00.mp4"
AUDIO_DURATION = "PT3M21S"

HUBS = {
    "it/video-e-slide/index.html": (
        "MANZO AI · PODCAST", "Episodio 00 — L'intelligenza artificiale serve davvero?",
        "La prima puntata: che cosa può fare l'IA, come formulare una buona domanda e perché serve il giudizio umano.",
        "Apri l'episodio"
    ),
    "es/videos-y-diapositivas/index.html": (
        "MANZO AI · PODCAST", "Episodio 00 — ¿Para qué sirve realmente la IA?",
        "Presentación educativa sobre preguntas, respuestas y criterio humano. Audio original en italiano, con transcripción y subtítulos en italiano.",
        "Ver episodio en italiano"
    ),
    "en/videos-and-slides/index.html": (
        "MANZO AI · PODCAST", "Episode 00 — What is AI really useful for?",
        "An introduction to effective prompting, verification, and human judgment. Spoken in Italian, with Italian transcript and captions.",
        "View Italian episode"
    )
}

def patch_hub(site: Path, rel: str, labels: tuple, has_video: bool):
    path = site / rel
    if not path.is_file():
        raise RuntimeError(f"Expected video hub is missing: {rel}")
    html = path.read_text(encoding="utf-8")
    if ROUTE in html:
        return
    kicker, title, description, call = map(escape, labels)
    status = (
        '<span style="color:#166c53;font-weight:700">Video disponibile</span>'
        if has_video else
        '<span style="color:#8b5619;font-weight:700">Scheda editoriale online · video in caricamento</span>'
    )
    card = f'''
<section aria-label="Podcast MANZO AI episodio 00" class="manzo-podcast-feature" style="margin:2rem auto;max-width:1050px;padding:clamp(1rem,3vw,1.7rem);border:1px solid #cbd0d5;border-radius:17px;background:linear-gradient(110deg,#f5f6f7,#fff);color:#15202b;box-shadow:0 10px 30px #18243012">
  <p style="font-size:.8rem;color:#b02232;font-weight:850;letter-spacing:.11em;text-transform:uppercase;margin:0 0 .4rem">{kicker}</p>
  <h2 style="color:#17212b;font-size:clamp(1.35rem,3vw,1.9rem);line-height:1.23;margin:.3rem 0 .55rem">{title}</h2>
  <p style="line-height:1.6;color:#384351;margin:.5rem 0">{description}</p>
  <p style="font-size:.87rem;margin:.5rem 0 1rem">{status} · 3 min 21 s</p>
  <a href="{ROUTE}" style="display:inline-flex;align-items:center;background:#b72235;color:white;font-weight:750;min-height:44px;padding:.8rem 1.1rem;border-radius:10px;text-decoration:none">{call}</a>
</section>
'''
    closing = re.search(r"</main\s*>", html, re.I)
    if not closing:
        raise RuntimeError(f"Expected closing main not found: {rel}")
    path.write_text(html[:closing.start()] + card + html[closing.start():], encoding="utf-8")

def render_page(has_video: bool) -> str:
    video = (f'''
    <video controls playsinline preload="metadata" width="1280" height="720" poster="{MEDIA_ROUTE}copertina.svg" aria-label="MANZO AI episodio 00, voce sintetica Stefano Gal">
        <source src="{MEDIA_ROUTE}{VIDEO_NAME}" type="video/mp4">
        <track src="{MEDIA_ROUTE}ep00-it.vtt" kind="captions" srclang="it" label="Italiano" default>
        Il browser non supporta la riproduzione video.
    </video>
    <p class="download"><a href="{MEDIA_ROUTE}{VIDEO_NAME}" download>Scarica il video MP4</a> · <a href="{MEDIA_ROUTE}ep00-it.srt" download>Scarica i sottotitoli SRT</a></p>''' if has_video else '''
    <div class="pending" role="status"><strong>Scheda dell'episodio pubblicata</strong><p>Il file MP4 definitivo non è ancora disponibile sul sito. La riproduzione sarà attivata quando il master corretto sarà caricato nel repository ufficiale.</p></div>''')
    ldjson = (f'''<script type="application/ld+json">{{"@context":"https://schema.org","@type":"VideoObject","name":"MANZO AI — Episodio 00: L'intelligenza artificiale serve davvero?","description":"Podcast educativo italiano sull'intelligenza artificiale, i prompt e il giudizio umano.","duration":"{AUDIO_DURATION}","inLanguage":"it-IT","uploadDate":"2026-11-05","thumbnailUrl":"https://manzo8b.github.io{MEDIA_ROUTE}copertina.svg","contentUrl":"https://manzo8b.github.io{MEDIA_ROUTE}{VIDEO_NAME}"}}</script>''' if has_video else "")
    return f'''<!doctype html>
<html lang="it"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Podcast · Episodio 00 — L'intelligenza artificiale serve davvero? | MANZO AI</title>
<meta name="description" content="Il podcast MANZO AI: scopri che cosa può fare l'intelligenza artificiale, come formulare prompt efficaci e perché il giudizio umano resta fondamentale.">
<link rel="canonical" href="{PUBLIC}"><meta property="og:type" content="article">
<meta property="og:title" content="MANZO AI · Episodio 00 — L'intelligenza artificiale serve davvero?">
<meta property="og:description" content="3 minuti e 21 secondi per cominciare a capire l'IA con curiosità e spirito critico.">
<meta property="og:image" content="https://manzo8b.github.io{MEDIA_ROUTE}copertina.svg">
<meta property="og:url" content="{PUBLIC}">
<meta name="theme-color" content="#11161c">
<link rel="stylesheet" href="/manzo-ai/style.css">
<style>
:root{{color-scheme:light}}
body{{margin:0;background:#f7f8fa;color:#17212a;font-family:system-ui,-apple-system,'Segoe UI',sans-serif;line-height:1.6}}
header,main,footer{{max-width:1000px;margin:auto;padding:1.1rem max(1.1rem,3vw)}}
header{{display:flex;align-items:center;gap:1rem;padding-top:1.5rem}}
header img{{width:46px;height:46px;object-fit:contain}}
header a{{font-size:.95rem;color:#1d2835}}
.eyebrow{{color:#a91d31;font-size:.83rem;font-weight:850;letter-spacing:.1em;text-transform:uppercase}}
h1{{font-size:clamp(2rem,5vw,3.8rem);line-height:1.09;letter-spacing:-.04em;margin:.4rem 0 1rem}}
.lead{{font-size:clamp(1.02rem,2vw,1.3rem);max-width:760px;color:#46515c}}
.hero{{padding:2rem 0 1rem}}
figure{{margin:1.5rem 0}}
video{{width:100%;height:auto;display:block;border-radius:14px;background:#14181e;box-shadow:0 14px 35px #1115}}
.cover{{width:100%;display:block;border-radius:14px;box-shadow:0 12px 28px #1112}}
section{{margin:2rem 0;padding:1.2rem clamp(1rem,3vw,1.8rem);background:white;border:1px solid #dfe3e6;border-radius:14px}}
h2{{font-size:1.4rem;line-height:1.25}}
a{{color:#a3152e}}
a:focus-visible{{outline:3px solid #e53d50;outline-offset:3px}}
.pending{{background:#fbf3e7;border:1px solid #e6c9a5;border-radius:12px;padding:1.2rem}}
.download{{font-size:.95rem}}
.meta{{color:#55616e;font-size:.95rem}}
.notice{{font-size:.9rem;color:#455360}}
footer{{padding-bottom:3rem;color:#55616e}}
</style>
{ldjson}
</head>
<body>
<header><img src="/manzo-ai/assets/manzo-mark.svg" alt="Emblema MANZO"><a href="/manzo-ai/it/video-e-slide/">← Video e slide</a><a href="/manzo-ai/it/" style="margin-left:auto">MANZO AI</a></header>
<main>
<div class="hero">
<p class="eyebrow">MANZO AI · PODCAST · EPISODIO 00</p>
<h1>L'intelligenza artificiale serve davvero?</h1>
<p class="lead">Che cosa possiamo fare con l'IA nella vita e nel lavoro? Da una buona domanda alla verifica delle risposte, senza perdere il giudizio umano.</p>
<p class="meta">Durata: 3 min 21 s · Lingua: italiano · Voce narrante sintetica: Stefano Gal · Progetto editoriale MANZO AI</p>
</div>
<figure><img class="cover" src="{MEDIA_ROUTE}copertina.svg" width="1280" height="720" alt="Copertina grafica MANZO AI Episodio 00, senza persone"></figure>
{video}
<section><h2>In questo episodio</h2>
<p>Partiamo dalla domanda più comune: a cosa serve davvero l'intelligenza artificiale? Un esempio legato alla formazione mostra perché è importante formulare una richiesta precisa, verificare il risultato e decidere con il proprio giudizio.</p>
<p>Si introduce inoltre il significato di <strong>prompt</strong>: l'istruzione, la richiesta o il contesto che diamo a un sistema di IA.</p>
</section>
<section><h2>Trascrizione e accessibilità</h2>
<p>La puntata è in italiano. Il file dei sottotitoli è disponibile in formato <a href="{MEDIA_ROUTE}ep00-it.srt" download>SRT</a>, e per la riproduzione web anche in formato <a href="{MEDIA_ROUTE}ep00-it.vtt">WebVTT</a>.</p>
</section>
<section><h2>Crediti e trasparenza</h2>
<p>Un progetto editoriale MANZO AI, parte di MARCELUS AI LAB. La voce narrante è <strong>Stefano Gal, voce sintetica della libreria Descript</strong>, scelta e approvata dalla direzione editoriale. Il contenuto nasce da un copione e da una revisione umana. La musica di sottofondo è una composizione strumentale originale realizzata per il progetto. Nessuna persona reale appare nel video.</p>
<p class="notice">Questo contenuto è introduttivo e non sostituisce una verifica delle informazioni presso fonti autorevoli.</p>
</section>
</main><footer>© MANZO AI · <a href="/manzo-ai/it/">Torna al portale educativo</a></footer>
</body></html>'''

def sitemap_add(site: Path):
    p = site / "sitemap.xml"
    xml = p.read_text(encoding="utf-8")
    if PUBLIC in xml:
        return
    end = re.search(r"</urlset\s*>", xml, re.I)
    if not end:
        raise RuntimeError("Unexpected sitemap: no urlset closing tag")
    xml = xml[:end.start()] + f"<url><loc>{escape(PUBLIC)}</loc></url>\n" + xml[end.start():]
    ET.fromstring(xml)
    p.write_text(xml, encoding="utf-8")

def main():
    a = argparse.ArgumentParser()
    a.add_argument("--site", required=True)
    a.add_argument("--edition", required=True)
    options = a.parse_args()
    site = Path(options.site)
    edition = Path(options.edition)
    for required in ("ep00-it.srt", "ep00-it.vtt", "copertina.svg"):
        if not (edition / required).is_file():
            raise RuntimeError(f"Podcast edition missing: {required}")
    dest = site / "assets/podcast/ep00"
    dest.mkdir(parents=True, exist_ok=True)
    for name in ("ep00-it.srt", "ep00-it.vtt", "copertina.svg"):
        shutil.copy2(edition/name, dest/name)
    source_video = edition / VIDEO_NAME
    has_video = source_video.is_file() and source_video.stat().st_size > 1000000
    if has_video:
        shutil.copy2(source_video, dest / VIDEO_NAME)
    page = site / "it/podcast/episodio-00/index.html"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(render_page(has_video), encoding="utf-8")
    for path,labels in HUBS.items():
        patch_hub(site, path, labels, has_video)
    sitemap_add(site)
    assert page.stat().st_size > 2000
    print("MANZO AI podcast: episode page, IT/ES/EN hub cards, metadata and captions ready.")
    print("Published media video:", has_video)

if __name__ == "__main__":
    main()
