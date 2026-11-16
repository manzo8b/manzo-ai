#!/usr/bin/env python3
"""Read-only audit of the FINAL MANZO AI rendered site (_site).

This script NEVER uploads files, edits pages or calls Supabase. Run it only
AFTER all GitHub Pages publisher/SEO/design/auth steps have completed.
JSON is generated outside _site by default so it cannot leak to production.
"""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import posixpath
from urllib.parse import unquote, urlsplit

PREFIX = "/manzo-ai/"
AUTH_SEGMENTS = (
    "it/prodotto/learning-b2b/accesso/",
    "en/product/learning-b2b/sign-in/",
    "es/producto/learning-b2b/acceso/",
    "it/prodotto/learning-b2b/privacy/",
    "en/product/learning-b2b/privacy/",
    "es/producto/learning-b2b/privacidad/",
)


class HeadAudit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.title = ""
        self._in_title = False
        self.robots = ""
        self.canonical = ""
        self.alternates = {}
        self.references = []
        self.headings_with_terminal_period = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang", "")
        if tag == "title":
            self._in_title = True
        if tag == "meta" and a.get("name", "").lower() == "robots":
            self.robots = a.get("content", "")
        if tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonical = a.get("href", "")
        if tag == "link" and "alternate" in a.get("rel", "").lower().split() and a.get("hreflang"):
            self.alternates[a["hreflang"]] = a.get("href", "")
        if tag in {"a", "link", "script", "img", "source", "video", "audio"}:
            value = a.get("href") or a.get("src")
            if value:
                self.references.append(value)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, value):
        if self._in_title:
            self.title += value


def file_digest(path):
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def internal_reference(ref, document):
    if ref.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
        return None
    url = urlsplit(ref)
    if url.scheme or url.netloc:
        return None
    raw = unquote(url.path)
    if not raw:
        return None
    if raw.startswith("/"):
        if not raw.startswith(PREFIX):
            return None  # other sites hosted at this GitHub Pages origin
        local = raw[len(PREFIX):]
    else:
        local = posixpath.join(posixpath.dirname(document), raw)
    result = posixpath.normpath(local)
    if result.startswith("../") or result == "..":
        return None
    if raw.endswith("/") or not posixpath.splitext(result)[1]:
        return posixpath.join(result, "index.html") if result != "." else "index.html"
    return result


def scan(site):
    site = Path(site).resolve()
    if not site.is_dir():
        raise ValueError("site root is missing")
    pages, assets, missing = [], [], []
    all_files = sorted(p for p in site.rglob("*") if p.is_file())
    known = {p.relative_to(site).as_posix() for p in all_files}
    for file in all_files:
        if file.is_symlink() and not file.resolve().is_relative_to(site):
            raise ValueError("external symlink in site: " + str(file))
        route = file.relative_to(site).as_posix()
        size = file.stat().st_size
        if file.suffix.lower() not in {".html", ".htm"}:
            assets.append({"path": route, "bytes": size, "sha256": file_digest(file)})
            continue
        reader = HeadAudit()
        reader.feed(file.read_text(encoding="utf-8", errors="replace"))
        is_private = any(route.startswith(segment) for segment in AUTH_SEGMENTS)
        refs = set()
        for ref in reader.references:
            internal = internal_reference(ref, route)
            if internal is not None:
                refs.add(internal)
        missing_here = sorted(ref for ref in refs if ref not in known)
        if missing_here:
            missing.append({"page": route, "paths": missing_here})
        pages.append({
            "path": route,
            "locale": reader.lang,
            "title": reader.title.strip(),
            "canonical": reader.canonical,
            "robots": reader.robots,
            "hreflang": reader.alternates,
            "auth_private": is_private,
            "private_noindex_ok": not is_private or "noindex" in reader.robots.lower(),
            "bytes": size,
            "sha256": file_digest(file),
            "internal_refs": len(refs),
            "missing_internal_refs": missing_here,
        })
    noindex = sum("noindex" in p["robots"].lower() for p in pages)
    violation = [p["path"] for p in pages if not p["private_noindex_ok"]]
    locales = sorted({p["locale"] for p in pages if p["locale"]})
    return {
        "schema_version": "1.0",
        "scope": "built-release-site",
        "root_url_prefix": PREFIX,
        "site": "_site",
        "summary": {
            "html_pages": len(pages),
            "asset_files": len(assets),
            "indexed_candidates": len(pages) - noindex,
            "noindex_pages": noindex,
            "locales": locales,
            "bytes_total": sum(p["bytes"] for p in pages + assets),
            "missing_reference_pages": len(missing),
            "auth_noindex_violations": len(violation),
        },
        "pages": pages,
        "assets": assets,
        "missing_internal_references": missing,
        "auth_noindex_violations": violation,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", default="_site", help="Final built site directory")
    parser.add_argument("--output", required=True, help="Write JSON outside site root")
    parser.add_argument("--minimum-pages", type=int, default=82)
    parser.add_argument("--strict", action="store_true", help="Fail on broken refs and auth indexability")
    args = parser.parse_args()
    root = Path(args.site).resolve()
    output = Path(args.output).resolve()
    if output.is_relative_to(root):
        parser.error("refusing to publish inventory inside the public site")
    result = scan(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], sort_keys=True))
    if result["summary"]["html_pages"] < args.minimum_pages:
        parser.error("incomplete site: fewer pages than the required baseline")
    if args.strict and (result["summary"]["missing_reference_pages"] or
                        result["summary"]["auth_noindex_violations"]):
        parser.error("rendered-site release gate failed")


if __name__ == "__main__":
    main()
