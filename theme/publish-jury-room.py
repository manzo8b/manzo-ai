#!/usr/bin/env python3
"""Staging-only publisher for MANZO AI jury-room pages.

This publisher is NOT wired to deploy-pages.yml. It refuses missing source
files and existing routes. Do not merge or activate until complete v0.4
sources and approved two-banner illustration are committed to the branch.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"product"/"jury-room"
ASSETS=SOURCE/"assets"
BASE="/manzo-ai/"
ENTRY=BASE+"it/laboratorio/stanza-dei-giurati/"
ROUTES={
    "index.html":ENTRY,
    "banco-di-prova.html":ENTRY+"banco-di-prova/",
    "officina-locale.html":ENTRY+"officina-locale/",
    "sala-dei-confini.html":ENTRY+"sala-dei-confini/",
}
SUFFIXES={".css",".js",".svg",".webp",".mp4"}
MARKER='content="noindex,nofollow"'

def transform(filename:str)->str:
    doc=(SOURCE/filename).read_text(encoding="utf-8")
    if MARKER not in doc:raise ValueError(f"Noindex missing in {filename}")
    if doc.lower().count("<h1")!=1:
        raise ValueError(f"Expected one H1 in {filename}")
    def rewrite(m:re.Match)->str:
        key,value=m.group(1),m.group(2)
        if value.startswith("assets/"):
            asset=ASSETS/value.removeprefix("assets/")
            if not asset.is_file():
                raise FileNotFoundError(f"Missing asset: {asset}")
            sha=hashlib.sha256(asset.read_bytes()).hexdigest()[:12]
            value=BASE+"assets/jury-room/"+asset.name+"?v="+sha
        else:
            for source,target in ROUTES.items():
                if value.startswith(source):
                    value=target+value[len(source):]
                    break
        return key+'="'+value+'"'
    doc=re.sub(r'(href|src)="([^"]+)"',rewrite,doc)
    if "<head>" not in doc:
        raise ValueError("No head: "+filename)
    image="https://manzo8b.github.io/manzo-ai/assets/jury-room/palazzo-stendardi-manzo.webp"
    meta=(
        '<link rel="canonical" href="https://manzo8b.github.io'+ROUTES[filename]+'">'
        '<meta property="og:type" content="website">'
        '<meta property="og:image" content="'+image+'">'
    )
    doc=doc.replace("</head>",meta+"</head>",1)
    return doc

def publish(site:Path,verify_only:bool=False)->None:
    required=[SOURCE/name for name in ROUTES]
    required += [ASSETS/name for name in (
        "styles.css","rooms.css","app.js","room-practices.js",
        "experiment-data.js","manzo-mark.svg",
        "palazzo-stendardi-manzo.webp","filmato-concept.mp4"
    )]
    missing=[str(f) for f in required if not f.is_file()]
    if missing:
        raise FileNotFoundError("Staging sources have not been uploaded: "+", ".join(missing))
    dst_assets=site/"assets"/"jury-room"
    if not verify_only:
        dst_assets.mkdir(parents=True,exist_ok=True)
        for asset in ASSETS.iterdir():
            if asset.is_file() and asset.suffix in SUFFIXES:
                shutil.copyfile(asset,dst_assets/asset.name)
    for filename,url in ROUTES.items():
        destination=site/url.removeprefix(BASE)/"index.html"
        expected=transform(filename)
        if verify_only:
            if not destination.is_file():
                raise FileNotFoundError(destination)
            if expected!=destination.read_text(encoding="utf-8"):
                raise RuntimeError("Staging page drift: "+str(destination))
            continue
        if destination.exists():
            raise RuntimeError("Refusing to overwrite an existing MANZO AI page: "+str(destination))
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_text(expected,encoding="utf-8")
        print("STAGED",url)
    if verify_only:
        print("PASS jury-room v0.4: four pages, published assets and noindex")

def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--site",type=Path,required=True)
    p.add_argument("--verify-only",action="store_true")
    a=p.parse_args()
    publish(a.site,a.verify_only)
if __name__=="__main__":
    main()
