#!/usr/bin/env python3
"""Install the exact owner-reviewed v0.5 package onto a non-deploy Git branch.

Never pushes, merges, deploys, modifies the MANZO AI Home, or overwrites files.
Usage: python3 theme/install-jury-v05.py --zip /path/to/MANZO_AI_Stanza_dei_Giurati_v05_Brief_2_Corretto.zip
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile

EXPECTED_SHA256 = "0d74c2832cb296a22d15aaa6aef0791d7f60536bfefc3b7d37d47a427e52ace7"
SOURCE_PREFIX = "MANZO_AI_Stanza_dei_Giurati_v05/"
REQUIRED = {
    "index.html", "banco-di-prova.html", "officina-locale.html", "sala-dei-confini.html",
    "assets/app.js", "assets/experiment-data.js", "assets/rooms.css",
    "assets/room-practices.js", "assets/styles.css", "assets/manzo-mark.svg",
    "assets/palazzo-stendardi-manzo.webp", "assets/filmato-concept.mp4",
    "tools/build_for_manzo_ai.py", "tools/test_brief_v05.py",
    "sources/MANZO_AI_Progetto_Esperimenti.md",
    "sources/MANZO_AI_Esperimento_02_Governo.md",
    "sources/MANZO_AI_Esperimento_03_Officina.md",
}
ALLOWED_DIRS = {"assets", "tools", "sources"}
EXCLUDED = {"QA"}

def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], check=True,
                            capture_output=True, text=True)
    return result.stdout.strip()

def install(repo: Path, archive: Path, dry_run: bool = False) -> list[str]:
    repo = Path(git(repo, "rev-parse", "--show-toplevel")).resolve()
    branch = git(repo, "branch", "--show-current")
    if branch in {"main", "master", "gh-pages"} or not branch.startswith("feat/jury-room-"):
        raise RuntimeError(f"Refusing branch {branch!r}: use a feat/jury-room-* staging branch")
    if git(repo, "status", "--porcelain"):
        raise RuntimeError("Worktree must be clean before importing; commit or stash other work")
    if not archive.is_file():
        raise FileNotFoundError(archive)
    actual_sha = hashlib.sha256(archive.read_bytes()).hexdigest()
    if actual_sha != EXPECTED_SHA256:
        raise RuntimeError("Archive SHA256 differs from the visually approved v0.5 package")
    destination = repo / "product" / "jury-room"
    pending: list[tuple[Path, bytes]] = []
    with zipfile.ZipFile(archive) as z:
        files = {info.filename: info for info in z.infolist() if not info.is_dir()}
        paths = {name.removeprefix(SOURCE_PREFIX) for name in files if name.startswith(SOURCE_PREFIX)}
        missing = REQUIRED - paths
        if missing:
            raise RuntimeError("The approved archive is incomplete: " + ", ".join(sorted(missing)))
        for name, info in files.items():
            if not name.startswith(SOURCE_PREFIX):
                raise RuntimeError(f"Unexpected archive member: {name}")
            rel = PurePosixPath(name.removeprefix(SOURCE_PREFIX))
            if not rel.parts or rel.is_absolute() or ".." in rel.parts:
                raise RuntimeError(f"Unsafe path: {name}")
            if rel.parts[0] in EXCLUDED or "__pycache__" in rel.parts:
                continue
            if len(rel.parts) > 1 and rel.parts[0] not in ALLOWED_DIRS:
                raise RuntimeError(f"Unexpected nested path: {name}")
            if (info.external_attr >> 16) & 0o170000 == 0o120000:
                raise RuntimeError(f"Archive contains symbolic link: {name}")
            out = destination.joinpath(*rel.parts)
            if out.exists():
                raise RuntimeError(f"Refusing overwrite of {out}")
            pending.append((out, z.read(info)))
    if not dry_run:
        for out, blob in pending:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(blob)
    return [str(out.relative_to(repo)) for out, _ in pending]

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--zip", type=Path, required=True, help="Exact approved v0.5 ZIP")
    p.add_argument("--repo", type=Path, default=Path.cwd(), help="Local Git clone")
    p.add_argument("--dry-run", action="store_true", help="Validate but do not write")
    args = p.parse_args()
    try:
        paths = install(args.repo, args.zip.expanduser().resolve(), args.dry_run)
        print(f"PASS: {'validated' if args.dry_run else 'installed'} {len(paths)} files on staging branch")
        print("No git push, merge, deployment or Home change was performed.")
        print("Next: run source/interaction QA, then stage & push only after review.")
    except (RuntimeError, FileNotFoundError, subprocess.CalledProcessError, zipfile.BadZipFile) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
