# MANZO AI · Learning UX 1.1 — Coursera-informed, independently designed

**Date:** 2026-11-15  
**Status:** design proposal and functional demonstration on a feature branch; not a commercial LMS.  
**Scope:** Academy discovery (IT/EN/ES), professional hallucinations course, specialist coding module, visual contrast refinement.

## Evidence and design decisions

Coursera is an external benchmark. We adapt **educational principles, not Coursera's source code, branding, copy, proprietary content or pixel-level layout**.

1. **Learning objectives → activities → evidence.** Coursera's learning-design materials recommend specific outcomes linked to practice and authentic evaluation. MANZO AI now displays three explicit outcomes above the existing syllabus, grounded in course content. [Source](https://blog.coursera.org/courseras-commitment-to-learning-how-we-support-skill-development/)
2. **Transparent syllabus and workload.** Coursera's public course pages display module counts, content types and indicative effort. MANZO AI now provides a chapter-by-chapter anchor index and shows estimated time **only where already supplied by MANZO AI course data**. [Example](https://www.coursera.org/learn/generative-ai-for-everyone)
3. **Low-stakes practice distinct from assessments.** Coursera distinguishes practice assignments from graded assessments. MANZO AI keeps its existing scenario practice, formative quiz and optional crossword, clearly linking to each without claiming exam accreditation. [Source](https://www.coursera.support/s/article/learner-000001563?language=en_US)
4. **Small actionable units and feedback.** Coursera research identifies smaller frequent assessments, hands-on projects and prompt feedback as practices associated with learning persistence in its studied population. These are **not guaranteed outcomes for MANZO AI**. [Source](https://www.coursera.org/about/press/wp-content/uploads/2022/05/Courseras-Drivers-of-Retention-in-Online-Degree-Programs-Report-1.pdf)
5. **Progress feedback.** Six optional chapter checkmarks update an in-page counter and a next-chapter link. These represent **self-reported reading progress during the current visit only**, not graded or independently verified course completion. Nothing is stored or transmitted.
6. **Professional application.** Existing MANZO AI content addresses finance, AML, legal and AI-generated coding. The UI provides a learning sequence without rewriting or expanding the substantive lessons.

## Interaction & privacy

- Chapter controls are buttons with correct `aria-pressed`; a reset clears the current in-memory selection.
- A link moves to the first still-unmarked chapter, while native chapter anchors remain available.
- Existing assessment scoring, reviews, detailed coding gate, crosswords, bibliographies and legal notices remain in place.
- No account creation, grade recording, access control, badges claiming certification, cookie, `localStorage`, `sessionStorage`, analytics, external JavaScript or third-party call is introduced by this enhancement.
- Real B2B progress will require verified account identity, backend scoring and PostgreSQL RLS; it is separate from this preview.

## Experience & design

The latest public redesign was judged too muted. This branch therefore **strengthens colour contrast without rearranging the site wholesale**: clean white background, saturated cobalt for primary navigation and functional CTAs, meaningful green for progress, coral for practice, and stronger light-blue/green section fields. An existing asymmetric homepage scene is preserved and changed from muted pale inset to a high-contrast cobalt field; content remains unchanged.

Course reader guidance deliberately sits as an inserted panel before the existing syllabus. It does not replace the original course hero, article, lesson component or workbook.

## Test gates

- All three Academy hubs link to the existing full course and specialist coding chapter.
- Three language routes × two lesson types contain exactly six anchored existing chapters.
- Buttons toggle reversible in-memory status; counter and next link update correctly; reset restores original state.
- Existing 10 cases, 10-question quiz and crossword in the core course survive.
- Existing 4 coding cases and specialist quiz survive.
- Chromium confirms no JS errors or horizontal overflow on mobile and no persistence.
- Full site-wide regression suite remains successful.
- Inspect actual desktop/mobile screenshots before acceptance. The fact that CI passes is **not** evidence that the user approves the aesthetic.

## Delivery process

This branch should undergo CI and visual review before merging. **Do not automatically publish** without explicit design approval, following the user's stated dissatisfaction with the previously published redesign.

## Sources

- Coursera [Generative AI for Everyone](https://www.coursera.org/learn/generative-ai-for-everyone), course page and module pattern
- Coursera Teaching & Learning Team, [Commitment to Learning](https://blog.coursera.org/courseras-commitment-to-learning-how-we-support-skill-development/)
- Coursera Help Center, [Taking assignments](https://www.coursera.support/s/article/learner-000001563?language=en_US)
- Coursera Research, [Drivers of Retention in Online Degree Programs](https://www.coursera.org/about/press/wp-content/uploads/2022/05/Courseras-Drivers-of-Retention-in-Online-Degree-Programs-Report-1.pdf)
