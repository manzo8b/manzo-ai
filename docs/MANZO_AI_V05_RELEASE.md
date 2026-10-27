# MANZO AI v0.5 — M02–M06 complete multilingual lessons

**Date:** 27 October 2026  
**Product Owner decision:** Approved M02–M06 IT / ES / EN.  
**Status:** Static release package built and tested locally; **not yet uploaded/published on GitHub Pages**.

## Changes

- Full approved M02–M06 lesson text in Italian, Spanish and English (15 additional lesson pages).
- Total 52 HTML pages; 49 sitemap entries, excluding privacy pages.
- AI Academy catalogue: all six modules link to actual lesson pages, not editorial placeholders.
- Includes learning goals, complete didactic text, examples, exercise and worked solution, questions with expandable answers, rubrics and source links.
- Direct navigation among modules, alternate-language links, internal search entries, metadata and responsive styling.
- Preserves the full M01 text and eight Italian slide graphics/PDF/PowerPoint from v0.4 unmodified.

## Evidence from local build

- 52 HTML pages present, one H1 and valid JSON-LD for each.
- All internal local links valid and 15 new pages include source links and three revealable quiz answer sections each.
- All 11 M01 slide assets (8 WebP, PDF, PPTX, Markdown guide) binary-identical to v0.4.
- JavaScript syntax check successful.
- No old 'DRAFT for owner', 'BOZZA per revisione' or 'BORRADOR para revisión' labels appear on new public lessons.
- No learner data collected or sent to a backend in the site source.

**Important:** Local checks are not live deployment or hands-on desktop/mobile acceptance tests. The original lesson sources keep their historical v0.2 editorial provenance for traceability; owner approval is recorded separately. External linked references were preserved from the original materials, not independently live-validated in this release.

## Publishing gate

The repository workflow now recognizes `site-v0.5.zip` and checks presence of all 15 lesson pages, quiz answer blocks, M01 slide assets and total HTML page count before deploying.

The complete binary ZIP and complete source ZIP have been prepared for owner download. Publish by uploading **`site-v0.5.zip`** (without extracting) in the root of `manzo8b/manzo-ai` and committing. The GitHub Actions workflow will then automatically select it.

Do not describe v0.5 as live before the GitHub Actions deployment reports success and the public pages have been checked.
