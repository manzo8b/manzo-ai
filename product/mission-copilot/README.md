# Mission Studio — AI Copilot · P2 private architecture

**Status: private Worker source only / not deployed / not connected to a real model.** The P1 browser-side adapter is wired to Mission Studio **only as a local, offline simulation behind `?copilot=preview`**; no API request is made.

This is a security and architecture prototype, not a public chatbot or a feature to advertise on the website.

## Budget commitment

- **Maximum authorized cost: €0.**
- Existing MANZO AI hosting stays on GitHub Pages; **no extra hosting purchase**.
- Candidate: **Cloudflare Workers AI on the Workers Free plan** (10,000 Neurons/day as of 18 November 2026, subject to provider conditions). The Free allocation stops processing after the quota. **Never switch to Workers Paid, prepaid credits, a paid-only model, or auto-upgrade.**
- Proposed model for future testing: `@cf/google/gemma-4-26b-a4b-it`, from the official Workers AI catalog, *subject to a fresh Free-plan availability check*.
- Do not use the deprecated-on-2026-11-20 Llama 3.1 FP8 model by default.
- This repository **does not create a Cloudflare account, activate inference, deploy a Worker, obtain a payment method or install external services**.

Sources: [Cloudflare Workers AI pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/), [Gemma 4 model](https://developers.cloudflare.com/workers-ai/models/gemma-4-26b-a4b-it/), [model deprecations](https://developers.cloudflare.com/changelog/post/2026-11-05-planned-model-deprecations/).

## Technical boundaries

- `worker.mjs`: Cloudflare Workers module supporting `POST /api/plan` only after Cloudflare Access, Free-plan consent and atomic daily quota are verified. Not deployed.
- `wrangler.toml`: AI binding, SQLite Durable Object `GLOBAL_QUOTA`; `COPILOT_ENABLED=false`, `FREE_PLAN_CONFIRMED=false`, `MODEL_FREE_CONFIRMED=false`, `workers_dev=false`; no public routes.
- `worker.test.mjs`: offline tests for Access identity, HMAC, global/per-user limits, concurrency and failure handling. All model responses are local fixtures.
- No environment or API keys are committed. Access credentials are **not** browser Bearer tokens. A trusted Access audience (`ACCESS_AUD`) and pseudonymization secret (`QUOTA_HASH_SALT`) must be supplied server-side by the owner before any opt-in activation.
- If disabled, missing an Access-authenticated context, Free-plan confirmations, HMAC secret, AI binding or atomic Durable Object quota, the Worker refuses every generation. No request can bypass the quota.
- **No CORS header, public frontend connection or login UI.** Future identity would come from Cloudflare Access; a single SQLite-backed Durable Object stores only hashed identity counters for the current UTC day. No educational text is persisted.
- Limited JSON input (4 KiB), predictable audience/duration/resource fields, bounded output, explicit **teacherApproval: false**.
- Heuristic exclusion of contact details; **not a proven PII filter**. Test with invented subjects, never student names or records.
- Strict output checks fail closed. A generated suggestion is **not a verified scientific claim**.

## Offline test

```bash
node --check product/mission-copilot/worker.mjs
node --test product/mission-copilot/worker.test.mjs
```

No npm install, payment, Cloudflare account or API key is required for these tests.

## Why we are not launching publicly yet

A secret shared with a browser cannot protect a public service. Before any opt-in public release, we need authenticated access, **account-wide distributed usage quotas**, monitoring, cost controls, abuse protection, data-governance review and a separate acceptance gate. A per-request token cap is **not** an account-wide cost limit.

**Do not enable / deploy until the project owner approves the external connection and account is confirmed to remain Free.**

## Future pedagogical integration

Once separate safeguards exist: select a teaching objective in Mission Studio → make a bounded, authorized request → receive a structured **unapproved** lesson draft → teacher edits and validates → save a local draft → export to the appropriate Studio. No raw student data, no automatic approval.

## P2 — Authenticated Free-only private backend (source only)

- Cloudflare Access identity is required from the runtime (`ctx.access`) with an exact audience match; arbitrary request headers or browser tokens cannot forge it.
- User identity is HMAC-SHA256 pseudonymized with a server-only salt before use as the quota key.
- One SQLite-backed Durable Object provides **atomic shared limits**: 20 requests total/UTC day, 3/user/day, 60 seconds between requests. Failed provider calls still consume a reservation.
- The backend fails closed whenever the quota store or authentication is missing. **Nothing is live or deployed to Cloudflare.**
- This is a count-based safety ceiling, **not a precise Neurons billing cap**. Remaining on Workers Free is mandatory; Cloudflare will reject requests once its own free allowance runs out.
- Local automated tests use mocked identities/storage/AI only: no live model calls and no real user data.
- Authoritative technical scope: [P2 Access, quota and €0 release gates](../../docs/MANZO_AI_COPILOT_P2_AUTH_QUOTA_ZERO_EURO_2026-11-18.md).

## P1 — Local UI integration, still €0

- `tools/ai-teaching-launchpad/mission-adapter.mjs` maps the existing unapproved `ai-teaching-lab-mission-v0.1` brief to the P0 Worker input: `tema`, `destinatari`, `durataMinuti`, `tipoRisorsa`, `obiettivo`. Only whitelisted fields can be passed.
- `tools/ai-teaching-launchpad/copilot-preview.mjs` contains the **local demo controller**: structured sample, explicit provenance and opt-in application of *only* the suggested objective to the existing brief. A later edit invalidates the suggestion.
- The public page only imports the demo module when a user opens `/it/formazione/ia-per-la-didattica/inizia/?copilot=preview`. Without this opt-in it remains hidden and does not load the modules.
- Publisher copies both modules next to the Mission Studio page; GitHub Actions confirms their presence and runs `node --test tools/ai-teaching-launchpad/mission-adapter.test.mjs`.
- The local simulation is **not an AI result**. In particular, tests use mocked/static data and no Cloudflare inference; the Worker remains disabled, without public route, credentials or browser-facing endpoint.

The existing application continues working without the preview and keeps local draft export/reimport; no online data is stored, transmitted or approved. Privacy checks are heuristic and are not a substitute for data-protection controls.


## P3 — Account readiness, real billing and privacy (still OFF)

- **Account is not connected or inspected**. The code cannot establish which Cloudflare plan, charges, card requirements or Neurons usage applies to the owner's account.
- `zero-euro-preflight.mjs` is a **zero-network read-only source audit**. It checks config guards and produces a planning projection; `safeToEnablePublicInference=false` by design.
- `zero-euro-preflight.test.mjs` tests cost assumptions, settings that must remain OFF, privacy gates and no network access.
- `DATA_PROTECTION_CONFIRMED=false` is a new independent server-side blocker. The Worker rejects all inference without the explicit review of data-protection responsibilities and provider terms.
- `[observability]` and invocation logging are disabled in the prospective Worker configuration. **Separate provider and account-level logging settings need inspection** before activation.
- Full evidence, Cloudflare Free/Zero Trust onboarding payment-detail caveat and Italian school privacy requirements: [P3 report](../../docs/MANZO_AI_COPILOT_P3_PREFLIGHT_PRIVACY_COSTI_0EUR_2026-11-18.md).

**No live model call, Worker deployment, API key or payment has been initiated.**
