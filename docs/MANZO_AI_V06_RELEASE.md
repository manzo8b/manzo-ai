# MANZO AI v0.6 — Critical Thinking Edition

**Product Owner decision:** Approved 27 October 2026.
**Delivery status:** Built and validated locally; binary publication archive has not yet been uploaded to GitHub. Do not mark v0.6 as live without successful deployment.

## Scope (IT / ES / EN)

- AI Brain Challenge: 3 demanding crosswords per locale, 12 clues per grid, all crossings verified, 9 grids / 108 original localized clues total; keyboard and button controls, grading and voluntary solution reveal.
- AI Radar: 3 source-grounded, dated editorial briefs per locale; 9 news pages, each explicitly linked to the primary institutional source, no auto-refresh.
- AI Dilemma: hiring automation and AI-supported learning, 2 cases per locale / 6 exercises; three response paths, explanations, unpersisted reflection.
- One critical-thinking hub per locale: 3 navigation pages. 27 pages added; **79 index.html pages total**.
- Existing M01–M06 lesson materials and the 11 original M01 slide assets preserved unmodified.

## Verified primary sources (accessed 27 October 2026)

1. European Commission, DG CONNECT, “The enforcement framework of the AI Act”; last updated 20 October 2026: https://digital-strategy.ec.europa.eu/en/policies/enforcement-ai-act
2. European Education Area, “New reports examine how AI and digital technologies are shaping education in Europe”, 22 September 2026: https://education.ec.europa.eu/whats-new/news/new-reports-examine-how-ai-and-digital-technologies-are-shaping-education-in-europe
3. UNESCO IITE, “Teacher AI Competency Frameworks”, 28 September 2026: https://iite.unesco.org/news/unesco-iite-has-released-the-analytical-report-teacher-ai-competency-frameworks/

All three are dated editorial digests, not continuous real-time news. The regulatory brief is educational, not legal advice.

## Local QA evidence

- Python build succeeded (79 HTML pages, 76 sitemap entries).
- Valid local hyperlink targets, schema JSON, localized routes.
- 9 generated crosswords each have 12 unique answers and form a connected crossing structure; all 108 word/clue pairs checked.
- 9 dated news pages, 6 interactive dilemma pages, 3 hubs.
- M01 graphic slides / PDF / PPTX / teacher guide byte-for-byte identical to v0.5.
- `node --check` of `app.js` passed.
- The browser smoke test could **not** run due to local Chromium administrative networking block (`ERR_BLOCKED_BY_ADMINISTRATOR`); interaction on real devices remains to be accepted.

## Publishing procedure

1. Download binary archive `site-v0.6.zip` from ChatGPT delivery; keep compressed.
2. Upload via https://github.com/manzo8b/manzo-ai/upload/main in repository root; confirm commit.
3. The workflow now recognizes the v0.6 filename, selects it over v0.5, and requires the 27 new pages, crossword and dilemma scripts, 79 page count, and M01 downloads.
4. Confirm a successful GitHub Actions run, then manually test crossword typing/keyboard/solutions and dilemmas on desktop and mobile.

Launch routes:
- IT https://manzo8b.github.io/manzo-ai/it/pensiero-critico/
- ES https://manzo8b.github.io/manzo-ai/es/pensamiento-critico/
- EN https://manzo8b.github.io/manzo-ai/en/critical-thinking/

**Release discipline:** This is the last proposed scope expansion before the planned pause; follow-ups should be limited to fixes and QA, subject to the owner's choices.
