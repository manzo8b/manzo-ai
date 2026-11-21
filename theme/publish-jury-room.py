#!/usr/bin/env python3
"""Guarded MANZO AI jury-room staging publisher.

The implementation is the versioned v0.5 builder shipped with the approved
prototype. Keeping a single source of truth prevents divergence between
local QA and GitHub staging. This file is NOT wired to deploy-pages.yml.

Usage: python3 theme/publish-jury-room.py --site _site [--verify-only]
"""
from __future__ import annotations
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / 'product' / 'jury-room' / 'tools' / 'build_for_manzo_ai.py'
if not BUILDER.is_file():
    raise SystemExit('BLOCKED: v0.5 prototype files are missing from product/jury-room. Do not deploy.')
if __name__ == '__main__':
    runpy.run_path(str(BUILDER), run_name='__main__')
