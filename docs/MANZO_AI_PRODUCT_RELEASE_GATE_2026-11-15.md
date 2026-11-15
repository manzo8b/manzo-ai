# MANZO AI — Product release gates, portability and acquisition readiness

**Decision date:** 2026-11-15
**Status:** v0.1 functional proof-of-concept / pre-commercial, NOT live SaaS
**Owner:** MANZO AI project
**Repository:** `manzo8b/manzo-ai`

## Product thesis

MANZO AI is not only a content website. It is a potential set of enterprise products under a single brand:

**MANZO AI Studio** — build/review digital projects;
**MANZO AI Verify** — structure verification of professional AI output;
**MANZO AI Learning** — deliver AI competency learning to organizations.

The core differentiator to validate is **verifiable professional workflows with human oversight**, not unlimited content generation or an AI model claimed to be infallible.

## What is now real

- Three localized, responsive nontransactional product previews produced by the existing static build:
  - IT: `/manzo-ai/it/prodotto/`
  - EN: `/manzo-ai/en/product/`
  - ES: `/manzo-ai/es/producto/`
- Studio's project brief generation and JSON export, entirely client-side
- Verify's deterministic candidate-claim extraction, without claiming fact verification
- Learning's enterprise request profile configuration, not a real license/quote
- A fail-closed, deterministic entitlement-policy proof-of-concept with unit tests, not connected to users or Stripe
- Source and QA scripts committed to GitHub

### Explicitly NOT available

- Production AI agent calls
- Authentication or accounts
- Database or customer data storage
- Client-company isolation enforced by a live backend
- Stripe Checkout or subscription provisioning
- Automatic site deployment, WordPress/Wix publishing, or binding quotations
- Independently audited enterprise compliance or security certification

## Definition of done for Product MVP (not the static preview)

| Gate | Required proof | Status |
|---|---|---|
| Buyer discovery | 10–15 relevant interviews, problem/offer evidence | NOT STARTED |
| Value proposition | one priority vertical and 2 scoped pilot offers | PROPOSED |
| Commercial hosting | functioning deployment on permitted host/domain | NOT STARTED |
| Identity | email verification, sessions, invitation, password recovery, admin | NOT STARTED |
| Multi-tenancy | database RLS plus cross-tenant tests and authorization review | NOT STARTED |
| Billing | test-mode Checkout, signed webhook, expiry/cancellation/refunds | NOT STARTED |
| AI run | server-only API, prompts/log policy, resource caps and tool allowlist | NOT STARTED |
| Operational safety | logs/monitoring, backup & restore, incident playbook | NOT STARTED |
| Legal | terms, privacy, DPA where needed, tax and invoice checks | NOT STARTED |
| Enterprise pilot | explicit service scope, acceptance criteria, QA and trained users | NOT STARTED |

The prototype tests demonstrate code behavior only. They do not replace penetration tests, accessibility testing, real user research or security review.

## Portable architecture criteria

- Content, presentation and backend contracts remain separable.
- No direct payment provider credentials or personal data in public repository.
- Entitlement policies are evaluated on the server with authenticated session identity and transactional usage metering; UI may only display derived state.
- Data export must be designed for tenant-scoped portability (course results, project artifacts, billing records where legally permitted), with deletion/retention controls.
- Source/asset inventory with SPDX license metadata and third-party permissions before commercial licensing.
- Open standards where possible: JSON, SQL migrations, REST/OpenAPI, WCAG/ARIA, tested CI.
- Build must be reproducible from tagged commit, not from an opaque manually prepared ZIP alone.

## Phased delivery

**P0 (this PR).** Working trilingual product preview, honest capability states, unit-testable authorization policy, CI smoke tests. No recurring cost.

**P1.** Move source-of-truth site out of archive-only workflows; stabilize component and content versions, conduct accessible/visual QA and validate one paying buyer vertical.

**P2.** Provision a separate commercial environment when operating costs are approved; implement server-side login, tenant schema and audit log with fail-closed policies. Existing Supabase project Oiko MUST NOT be reused.

**P3.** Add single end-to-end functional vertical. If buyer = training provider: enrollments, learning attempts and team admin. If buyer = software firm: reviewed workspace and source export with a metered agent. Do not build both at once.

**P4.** Test-mode billing with provider-signed webhook validation, idempotency and cancellation, then legal and security approval for live billing.

**P5.** Customer pilots, reliable metrics, audit and options for corporate licenses or full acquisition.

## Acquisition due diligence worklist

Future buyers will require verified facts, not deck narratives:

- Transferable IP and licences for source, design, copy, images and AI-generated assets
- Trademark/domain ownership and clean legal identity of the contracting entity
- Versioned repositories, branch protection, reproducible builds and deployment instructions
- Test results, unresolved vulnerabilities and third-party dependencies
- Service infrastructure, vendor agreements, data protection and recovery policy
- Revenue proof, costs, churn/retention, enterprise contracts and obligations (when present)
- Product roadmap linked to requests and actual business results
- Support agreements, assignment clauses and migration handover documentation

**Not yet available:** customers, revenue, signed deals, live subscriptions. Do not invent them or imply a valuation based on income.

## Budget guardrails

As of this release:
- GitHub preview adds no backend or AI model usage fees.
- Backend, domain, email and managed provider selection require explicit cost comparison and separate decision.
- No resources that could create non-zero bills should be provisioned until approved.
- A production service needs margin calculation: acquisition cost + support + platform costs + model/API inference + taxes/fees.

## Decision for the product owner

Approve a **single lead vertical** for P2. Recommended order based on current editorial and operational state: Learning team licences (lower initial complexity) or Verify evidence workflow (more differentiated), then Studio AI generation after reliable isolation, resource controls and human approval.
