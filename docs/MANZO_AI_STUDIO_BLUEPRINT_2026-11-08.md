# MANZO AI Studio — Product blueprint (concept v0.1)

**Date:** 8 November 2026  
**Status:** owner-approved cinematic visual direction, **prototype built and tested locally**. **Not yet published on MANZO AI**, not an active AI website-generation SaaS.

## 1. Strategic architecture

- **MARCELUS AI LAB:** central portfolio; project methods and verifiable case studies.
- **MANZO AI Academy:** existing public IT/ES/EN educational portal, technical prompt lab, podcast and editorial assets; keep **all 82 source pages** and routes untouched.
- **MANZO AI Studio:** new, visually ambitious sector-adaptive website design experience. Brand identity black/dark aubergine, crimson, magenta, refined violet, original MANZO bull emblem.
- **MARCELUS WebFoundry:** independently prototyped Python/Agent Skill site generator. Future integration requires explicit schema/CLI compatibility tests; **not connected yet**.

**Promise:** premium visual experiences + structured sector-specific blueprints + verifiable QA, with human control before publication.

## 2. Audience and verticals

| Sector | User need | Page concepts | Must review |
| --- | --- | --- | --- |
| Education | Digital classroom and training | Programs, method, resources, contacts | Pedagogy, accessibility |
| Hospitality | Clear digital guest journey | Services, experiences, gallery, contact | Current services / mobile UX |
| Compliance | Evidence-first professional presentation | Services, method, transparency, contact | Sources, legal specialist review |
| Tourism | Local discovery and editorial content | Explore, routes, stories, updates | Places, dates, multilingual facts |
| Creators / Music | Original creative identity | Work, catalogue, press kit, contact | Ownership, credits, official links |

## 3. Proposed website / navigation

**Homepage:** hero and value proposition; design/blueprint/quality capabilities; five industry cards; interactive blueprint laboratory; method timeline; MARCELUS identity and Academy link.

**Future routes only (not deployed):**
`/studio/`, `/studio/soluzioni/`, `/studio/settori/` and 5 vertical child routes, `/studio/laboratorio/`, `/studio/metodo/`, `/studio/casi/`, `/studio/chi-siamo/`, `/studio/contatti/`.

## 4. Prototype v0.1 — what works

- Standalone HTML/CSS/JavaScript with approved MANZO visual direction; no external framework, tracking, payment, login or server requests.
- Five interactive sectors and a structured form (project name, sector, visual direction, objective).
- Live visual preview and JSON blueprint download/copy.
- Export clearly flags `ai_model_used: false` and `production_ready: false`. **This is a deterministic brief composer, not a full AI site generator.**
- Source, visual previews, data schema, six design/product/technical documents and test scripts are delivered as a local downloadable package in the project conversation. Full prototype source has **not yet been committed to this repository**.

**Local test evidence, 08/11/2026:** 12 dependency-free structure tests, Node JS syntax check, Chromium desktop 1440×900 and mobile 390×844 smoke flows passed (navigation, sector selection, submission, JSON download, no page JS exceptions or document horizontal overflow). The sample JSON also passed JSON Schema validation.

**Not tested:** Safari on actual iPhone, real Android, Lighthouse, full WCAG 2.2 audit, authentication/data security, actual AI generation, backend deployment or payments.

## 5. Technical trajectory

```text
Sector brief -> validation -> deterministic blueprint -> visual preview + JSON
                                              |
                                              v (future, NOT implemented)
                                  WebFoundry Python generator
                                              |
                                    Generated static website
                                              |
                               Automated QA + browser review
                                              |
                                   HUMAN PUBLICATION GATE
```

Future optional LLM adapter must keep secrets on a server, validate untrusted outputs, have bounded costs, quotas, access controls and explicit approval gates. Use OWASP LLM Top 10 guidance; never execute instructions from generated code or retrieved material unchecked.

## 6. Visual system

- Base: `#090710`; main text `#FFF8FC`; accents `#FF375F`, `#DA3D98`, `#8250BC`.
- Logo: existing original MANZO geometric bull emblem.
- UI: cinematic graphic core, glass-like feature cards, rounded controlled CTAs, real content hierarchy.
- Accessibility target: WCAG 2.2 AA, focus-visible, semantic markup, responsive reflow and reduced motion; **no certification claim**.
- The Dribbble reference informed the desired sophistication, **not reused as source artwork**.

## 7. Release and business gates

1. **Vision/prototype:** owner visual approval and local technical prototype (DONE).
2. **Visual QA:** real mobile/browser, accessibility, copy and legal/IP review (PENDING).
3. **WebFoundry integration:** validated generation of five actual sector sites with repeatable QA (PENDING).
4. **Portfolio case:** show concept, implementation, source, test evidence and limitations (PENDING).
5. **Commercial deployment:** hosting, privacy, legal terms, service delivery and cost model — **separate decision**. GitHub Pages may serve a non-commercial static showcase, not a hosted commercial SaaS.

No changes to `site-v0.7.zip`, release/deploy workflows, current live pages, podcast or Oracle City are part of this change.

## 8. References

- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/
- OWASP LLM 2025: https://genai.owasp.org/llm-top-10/
- GitHub Pages terms: https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features
- MARCELUS WebFoundry roadmap: https://github.com/manzo8b/marcelus/issues/31
