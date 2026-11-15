# MANZO AI · Design System

**Direction:** Precision & Motion  
**Version:** 1.0 · 15 November 2026  
**Scope:** Public website, learning, research, Product Lab, Learning B2B preview, navigation and responsive treatments  
**Languages:** IT / EN / ES

## Product thesis

MANZO AI is a professional product-in-progress connecting **Studio**, **Verify** and **Learning**, with research and education as foundations. The visual system must help an enterprise buyer, student and working practitioner understand what the platform currently does, what requires human verification and what is still in development.

**Visual concept:** from an unverified AI output to a professionally inspected result. The visual narrative is not generic AI magic. Editorial reading establishes knowledge; the Product Lab demonstrates measurable operations; the Learning console reveals workflow and accountability.

## Source skills

The visual system applies the guidance in the three user-supplied documents:
- `SKILL apple-design(4).md`: prompt response, direct manipulation, interruptible feeling, reduced motion, material hierarchy, optical typography and accessibility.
- `SKILL design-taste-frontend(4).md`: subject-specific art direction, substantive content, no generic stacked icon cards, flat visual fields, clear titles, disciplined type and real interface fragments rather than fabricated products.
- `SKILL impeccable)(2).md`: scope-aware Persuade / Read / Operate modes, design-context discipline, accessible feedback and responsive polish.

The attached skill **text** was available, but its referenced executable `draw.mjs`, `inspect.mjs` and `impeccable` launchers were not bundled. Do not claim these tools were run. Verification uses the project's own Playwright/GitHub Actions checks instead.

## Brand system

Retain the approved MANZO AI bull-mark, project name and public content. The existing GitHub source archive is not edited.

| Design token | Colour | Meaning |
|---|---|---|
| `--ma-paper` | `#FFFFFF` | Main background |
| `--ma-ink` | `#172E44` | Primary running text and headlines |
| `--ma-blue` | `#1B609B` | Navigation, links and primary actions |
| `--ma-teal` | `#086A64` | Verification, progress and academic accents |
| `--ma-coral` | `#B95839` | Sparing warnings and editorial differentiation |
| `--ma-soft-blue` | `#EEF5FA` | Studio + informative scenes |
| `--ma-soft-teal` | `#ECF8F4` | Learning / verified progress |
| `--ma-soft-orange` | `#FFF1E8` | Important notices and transitions |
| `--ma-stroke` | `#CBDCE7` | Functional control borders and tables |

No ivory paper backgrounds, dark full-page dashboards, rainbow card palette or decorative gradients. Use **whole flat colour fields**, not colour effects behind every component. Readable contrast is more important than brand saturation.

### Typography

One system font stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Inter, system-ui, sans-serif`. Use optical sizing when available; large headings have negative tracking and tight leading; body copy stays at or above the working baseline of ~16px, with generous line spacing. Monospace remains legitimate inside code examples and JSON exports.

### Composition by user task

**Persuade · Home and Product Lab**
- Large, clear product proposition; one priority action leading to actual existing product demonstrations
- Avoid a uniform row of identical cards: content regions vary in span and occupy distinct, flat-colour fields
- Show genuine Studio/Verify/Learning preview, never invented user numbers or customer logos
- The bull logo and existing orbital artifact remain part of the identity; do not introduce decorative 3D stock art

**Read · Course, dossier, technical articles**
- High-contrast full ink text, calm margins, spacious headings and distinguishable references
- Dossier and advanced exercise content are preserved verbatim
- A minimal reading-progress line provides orientation without changing navigation
- Answers, code blocks, crosswords, quizzes and source citations are not rewritten or replaced

**Operate · Learning B2B console**
- Compact, purposeful controls with functional borders and predictable feedback
- Tables, role state, progress and revoked-seat states are prioritized over decorative effects
- The current console remains an explicitly simulated browser-only demonstration
- No checkout, SaaS or live accounts may be implied by the design

## Motion and accessibility

- Interaction feedback starts at press; buttons remain interruptible.
- Progressive reveal is limited to nonessential sections. Content is always present in HTML without JS, and an escape hatch removes any lingering hidden state.
- Motion is fully reduced when requested; readability never depends on animation.
- Keep focus-visible indicators, real labels, touch-size controls, expected keyboard order, and stable paths back to locale homepage and Product Lab.
- No new trackers, local/session storage, third-party analytics or network calls.
- The user's existing language routes, navigation, coursework, downloads, legal links and search indices must survive.

## Implementation

- `theme/design-system.css`: late-loaded, surface-scoped CSS design tokens and per-mode styles
- `theme/design-motion.js`: nontracking progressive motion and reading progress
- `theme/publish-design-system.py`: classifies every final HTML page into portal, landing, learning, research, product, console or general
- `theme/design-browser-smoke.py`: Playwright tests for 11 representative surfaces at 1440/768/390px, motion policy, content visibility and screenshots
- `.github/workflows/deploy-pages.yml`: adds the final design overlay after all publishers and navigation
- `.github/workflows/theme-qa.yml`: ensures that every page receives exactly one style/script link, validates original interactions and archives screenshot evidence

The source `site-v0.7.zip` and all editorial content are left unmodified. The overlay is reversible: omit the final publisher and its CSS/JS to restore the earlier design.

## Evidence and limits

The GitHub workflow's reported PASS validates technical rendering, baseline colour, page presence, basic overflow, JavaScript errors and representative interactions. It **does not** by itself establish award-level visual quality, a complete WCAG audit or Core Web Vitals performance. Review the screenshot evidence attached to the Chromatic QA run before treating the design as final.

The full editorial archive has many page-specific exceptions. Future visual refinements should be incremental, documented with screenshots and cross-checked against mobile learning functionality. No content changes were authorized as part of this redesign.

## Visual-review notes from the first screenshot pass

The CI screenshot evidence from the initial implementation was inspected directly for the Italian homepage at 1440/390, the ACR scientific dossier at 768, Product Lab at 1440 and the Learning console at 390.

The visual review identified three shortcomings and corresponding fixes:
1. **Homepage**: original centered search composition remained generic. Added a real, localized Studio / Verify / Learning navigation narrative beside the original search on wide screens, stacking below it on phones.
2. **Product Lab**: desktop headline wrapped unnecessarily over three lines. Broadened its reading measure while keeping the existing copy, hero focus and actual functional links.
3. **Learning B2B mobile**: the portal-level mobile bar duplicated the console's native responsive header. Product Lab and Learning now use their built-in headers instead of the archive navigation overlay. A follow-up screenshot revealed the old navigation stylesheet still overwrote their `.shell` display/width; this was also restored on the standalone mobile surfaces and is now asserted in QA.

The ACR dossier's research-specific diagrams remain visually distinctive. Its original content, labels and scientific caveats are preserved, even when its deliberate visual treatments differ from the general marketing-site rules.

**Remaining visual validation:** examine the final refreshed screenshots, especially narrow-screen console hierarchy and the homepage's first viewport after the navigation fix. Chromatic QA artifacts are diagnostic, not an independent accessibility certification.


## Regole non negoziabili — aggiornamento Home / Academy

Queste regole derivano dal feedback diretto di approvazione e correzione dell'identità visiva e sono **criteri permanenti di accettazione**, non consigli facoltativi:

1. **Tutte le card del sito devono essere moderne e avere una risposta visiva misurabile.** Su desktop si usano movimento moderato, elevazione e ombra profonda al passaggio del mouse; sul focus tastiera si garantisce la stessa evidenza funzionale. Su mobile gli effetti non devono ostacolare i controlli e si rispettano le preferenze di movimento ridotto.
2. **Mai un punto finale nei titoli di sezione** (H1–H6), in nessuna lingua. Questo è verificato dalla pipeline su tutto il sito tramite \`theme/publish-title-cleanup.py\`, senza manipolare il testo didattico.
3. **Niente palette debole, smorta o carta avorio.** Il bianco rimane il piano di lettura, mentre i blocchi funzionali e le card principali possono essere saturi e riconoscibili, con adeguato contrasto tra testo e sfondo.
4. **Non stravolgere l'architettura approvata.** La Home mantiene ricerca reale, contenuti, menu e percorsi; cambiano soprattutto la gerarchia cromatica, le card, gli stati interattivi e la definizione degli accenti.
5. **Non copiare Coursera.** Adottare il catalogo filtrabile e la didattica modulare, con card originali e informazioni reali. Nessun rating, certificato o contenuto inventato.

### Home v1.3 — valori visivi verificabili

| Superficie | Colore previsto | Testo |
|---|---|---|
| Hero | Bianco \`#FFFFFF\`, accent line cobalto | Blu profondo |
| Prima card | Cobalto \`#204EE5\` | Bianco |
| Seconda card | Verde petrolio \`#006F68\` | Bianco |
| Terza card | Arancio corallo \`#FF8F52\` | Blu profondo |
| Scena prodotto | Blu \`#2158ED\` | Bianco |
| Banner commerciale | Blu profondo \`#183B9A\` | Bianco, CTA oro tenue |

Il test \`theme/design-browser-smoke.py\` verifica i valori CSS applicati dal browser alle prime tre card, la presenza delle ombre, l'elevazione hover e la larghezza mobile; la QA salva screenshot reali desktop e mobile.

**La PR resta in attesa di approvazione visiva.** Nessuna modifica in questa iterazione dà per attivati login, corso commerciale, pagamenti o progressi persistenti.
