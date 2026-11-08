#!/usr/bin/env python3
"""Rewrite public MANZO AI URLs in the built Pages artifact after an owner rename.

The authoritative release ZIP and integrity verification remain untouched.
No rewrite occurs for the original account owner.
"""
from __future__ import annotations

import argparse
from pathlib import Path

TEXT_EXTENSIONS = {".html", ".css", ".js", ".mjs", ".json", ".xml", ".txt", ".svg", ".webmanifest"}
TEXT_NAMES = {"robots.txt", "sitemap.xml", "CNAME"}
MAX_BYTES = 5_000_000


def rewrite(site: Path, old_owner: str, new_owner: str) -> tuple[int, int]:
    if not site.is_dir():
        raise ValueError(f"Missing built site: {site}")
    if not old_owner or not new_owner or "/" in old_owner + new_owner:
        raise ValueError("Invalid account name")
    if old_owner == new_owner:
        print("MANZO AI owner unchanged: URL rewrite not required.")
        return (0, 0)
    replacements = [
        (f"https://{old_owner}.github.io", f"https://{new_owner}.github.io"),
        (f"http://{old_owner}.github.io", f"https://{new_owner}.github.io"),
        (f"https://raw.githubusercontent.com/{old_owner}/", f"https://raw.githubusercontent.com/{new_owner}/"),
        (f"https://api.github.com/repos/{old_owner}/", f"https://api.github.com/repos/{new_owner}/"),
        (f"git@github.com:{old_owner}/", f"git@github.com:{new_owner}/"),
        (f"https://github.com/{old_owner}", f"https://github.com/{new_owner}"),
        (f"http://github.com/{old_owner}", f"https://github.com/{new_owner}"),
    ]
    changed, references = 0, 0
    for path in sorted(site.rglob("*")):
        if not path.is_file() or (path.suffix.lower() not in TEXT_EXTENSIONS and path.name not in TEXT_NAMES):
            continue
        if path.stat().st_size > MAX_BYTES:
            raise ValueError(f"Unexpected large text asset: {path}")
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = original
        for before, after in replacements:
            references += updated.count(before)
            updated = updated.replace(before, after)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"MANZO AI account migration: {changed} files, {references} old-owner URL references updated.")
    return changed, references


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, required=True)
    parser.add_argument("--old-owner", default="manzo8b")
    parser.add_argument("--new-owner", required=True)
    args = parser.parse_args()
    rewrite(args.site, args.old_owner, args.new_owner)
