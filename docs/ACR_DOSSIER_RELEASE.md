# MANZO AI — Scientific ACR dossier launch

**Editorial release:** 14 November 2026 · **Publication status:** added to the MANZO AI GitHub Pages build pipeline.

## Routes

- Italiano: `/manzo-ai/it/ricerca/acr/`
- English: `/manzo-ai/en/research/acr/`
- Español: `/manzo-ai/es/investigacion/acr/`

## What the dossier publishes

- A professionally designed, three-language editorial dossier with an animated geometric hero and an accessible interactive memory-lifecycle explainer.
- A scientific overview of experiments **A** (verified memory), **B** (Fibonacci checkpoint schedule) and **C** (prompt structure ratios).
- Real, appropriately qualified **offline replay** figures: **2/16** eligible regressions for both C2 and C3 in each of two fixture scenarios. Those figures DO NOT prove efficacy.
- Prototype software test state reported as **48/48** local tests passed in v0.9; **zero** completed causal LLM comparisons.
- Primary research references, stable link to the full source tree, independent caveats on memory poisoning, and explicit non-peer-reviewed disclosure.

## Architecture

`theme/publish-acr-dossier.py` copies three localized HTML pages and static CSS/JS into the deployed `_site/` after unpacking `site-v0.7.zip`; it then adds localized entry cards to six existing entry pages. All additions happen in CI, before `theme/build-seo.py` regenerates sitemap/canonical URLs and before `theme/publish-navigation.py` adds the shared mobile navigation. The v0.7 release archive is not modified.

The dossier itself is a **public scientific communication interface**, not an LLM evaluation runner or a visitor-data collection system. No cookies, analytics, remote fonts or trackers are used by the dossier.

## Validation and accuracy limits

- Validate Python compilation, JavaScript syntax, three translations, publisher idempotency, browser layout and demo interactions.
- Test the full GitHub Actions deployment and live links before claiming publication is live.
- A passing deploy does not imply scientific peer review or indexation by Google.
- Follow-up revisions must never turn the 12.5% offline replay metric into an effectiveness finding.

## GitHub research material

The full lab v0.9 is pinned to commit `1a61fdb665f6ec9b7fe384abbe23e9a913d941f9` under `research/acr-lab/`. Its scientific conclusions are still open.
