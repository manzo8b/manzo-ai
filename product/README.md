# MANZO AI · Product Platform (pre-commercial foundation)

**Status:** functional local preview and unit-tested policy contracts; **NOT** an operating SaaS, hosted billing service or multi-tenant application.

## Product purpose

A transferable platform composed of three separately marketable tracks:

- **Studio** — professional briefs and, later, AI-assisted website creation with controlled exports
- **Verify** — claim identification followed by source verification, approval and audit trail
- **Learning** — enterprise learning, assessments and team licensing

The demo is intentionally honest about what it can do *now*.

## Files

- `preview/content.json` — editorial interface copy for IT, EN and ES
- `preview/preview.css` and `preview/preview.js` — dependency-free front-end
- `theme/publish-product-preview.py` — deterministic static pages and homepage links
- `core/entitlements.py` — reference policy engine for tenant/feature/quota decisions
- `core/tests/test_entitlements.py` — tests for missing/suspended/expired/foreign-tenant grants
- `theme/product-preview-browser-smoke.py` — browser QA for real interactions and input handling

## Current capabilities, actually implemented

| Component | Real behavior | Limit |
|---|---|---|
| Studio | builds and exports JSON requirements brief locally | not an AI generator |
| Verify | uses documented text heuristics to flag potentially checkable claims | does not determine truth or hallucination |
| Learning | configures a team license request profile locally | not a quote, enrolment or subscription |
| SaaS policy contract | tests authorization decisions for tenant, validity and quota | no auth, trusted data source or database yet |
| Locale + responsive | IT, EN, ES and small/large viewport browser checks | physical device & accessibility audit remain |

**Privacy:** preview fields and results exist only in current-page memory. The preview has no network requests in application JavaScript, no cookies, no analytics and no local/session storage. Users are explicitly warned not to paste confidential data.

**Search:** preview pages are `noindex,follow` during pre-commercial testing. Their homepage links are informational, not purchase links.

## Hard go-live gates

A genuine MANZO AI SaaS needs:
1. commercial hosting and domain (not GitHub Pages as primary SaaS store)
2. dedicated, region-selected backend with secure identity management
3. database enforced organization isolation; tests against unauthorized access
4. signed provider webhooks and server-controlled feature entitlements
5. server-only AI credentials, metered costs, rate limits and human approval
6. legal documents and verified data processing scope
7. operational monitoring, backups, incident response and recovery rehearsal
8. paying customer discovery, validated product claims and a buyer-ready service agreement

**Do not implement fake authentication, client-only subscription checks or faux AI responses.** Any new feature must be honest about functional status.

## Deployment and migration

The GitHub Pages site is a non-transactional preview only. Once the market and technical gates are ready, deploy the actual SaaS app to a suitable provider. Keep the versioned editorial assets and this preview independent of backend choice. The existing source ZIP is preserved.

See:
- [SaaS Architecture ADR-001](../../docs/MANZO_AI_SAAS_ARCHITECTURE_ADR001_2026-11-15.md)
- [Buyer Research](../../docs/MANZO_AI_BUYER_RESEARCH_2026-11-15.md)
- [Product Release Gate](../../docs/MANZO_AI_PRODUCT_RELEASE_GATE_2026-11-15.md)
