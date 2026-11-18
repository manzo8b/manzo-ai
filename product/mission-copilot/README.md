# Mission Studio — AI Copilot · P0 private prototype

**Status: source-only / not deployed / not connected to Mission Studio.**

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

- `worker.mjs`: Cloudflare Workers module supporting `POST /api/plan`, strictly private preview.
- `wrangler.toml`: AI binding present; `COPILOT_ENABLED=false` and `workers_dev=false`; no public routes.
- `worker.test.mjs`: eight automated tests without actual IA or network. All model responses are local fixtures.
- No environment or API keys are committed. `PREVIEW_ACCESS_TOKEN` would have to be set by an authorized person in Cloudflare as a **secret**, never in GitHub Pages or front-end code.
- If disabled, missing an adequate secret, or missing the AI binding, the Worker refuses any generation. Even when enabled for a private test, an authorization token is required.
- **No CORS header**, login system, user tracking, database or file storage. The GitHub Pages frontend is intentionally not connected.
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
