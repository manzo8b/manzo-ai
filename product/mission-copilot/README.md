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

## P4 — Private synthetic-only beta readiness (not deployed)

- The first real private experiment is restricted to **four fixed fictional cases** in product/mission-copilot/beta-scenarios.mjs. Clients may send ONLY a scenarioId; no free-text lesson brief, student details or additional request fields may reach inference. All future expansions require new explicit review.
- BETA_SYNTHETIC_ONLY=true is mandatory in Wrangler and the Worker. The CI preflight fails if either side stops enforcing it.
- The Durable Object schedules a best-effort cleanup alarm shortly after UTC midnight to remove expired HMAC quota counters. Platform backup/point-in-time recovery and Access identity retention are separate Cloudflare matters.
- 20 offline backend tests + 9 cost/privacy preflight tests + 10 Mission Studio adapter tests all passed in GitHub Pages run 44307897878. **Mock tests do not constitute a real model request.**
- Privacy, Free-plan status, payment-method requirements and actual Neuron consumption of the owner's Cloudflare account are still **unverified**.
- Complete decision protocol: [P4 private beta](../../docs/MANZO_AI_COPILOT_P4_BETA_PRIVATA_ZERO_EURO_2026-11-18.md).
- Do not set flags to true, deploy to Cloudflare, create a public hostname, or edit Access/billing settings without the owner's separate approval.


## P5.5 — Offline reliability audit (branch only; still OFF)

- Worker now asks Gemma 4 for `chat_template_kwargs: { enable_thinking: false }`, following Cloudflare's own model example while preserving the 650-token output cap.
- Handles both text `response` and chat-completion `choices[0].message.content`, rejecting incomplete, filtered or refused chat results even if the body appears to contain valid JSON.
- Regression tests and static preflight verify these rules; a dedicated offline GitHub Actions workflow checks a branch/pull request without Worker deployment, Cloudflare credentials or inference.
- Do **not** assume Gemma 4 JSON Mode compatibility from the generic JSON Mode guide; preserve strict JSON parsing and validate support separately in the future.
- P5.5 is source-only: real Access, model invocation, account Neurons and privacy/billing acceptance remain unverified.

[Audit and release gates](../../docs/MANZO_AI_COPILOT_P5_5_AUDIT_RELIABILITY_2026-11-18.md).

**No API has been connected to public Mission Studio and no paid service has been activated.**

## P5.6 — Access Free onboarding and offline identity verification (still OFF)

- The owner's screenshots confirm a Workers Free ($0) account, but the Cloudflare Zero Trust organization was not configured. **Workers Free and Zero Trust Free are separate plans.**
- Cloudflare's current Zero Trust Free onboarding docs explicitly request payment details even though the plan itself is free. Do not submit card information, select a paid plan or change billing without separate owner authorization.
- Cloudflare now supports protecting a single Worker by identity (rather than just one hostname). Once an Access organization is legitimately configured, prefer a Worker-wide, narrowly scoped account-member policy and test an authenticated direct invocation before any route is exposed.
- **Local `wrangler dev` Access simulation is not production authentication.** Added P5.6 mock regression tests for audience matching, distinct pseudonymous identities, missing Access, forged browser headers, and identity service failures. No secrets, network inference or deploy are involved.
- **Important:** Cloudflare Workers AI's actual model binding can still incur Neurons usage in local development. Mock tests are the approved cost-free method until the account and privacy gate are cleared.
- Without verified Access, the Worker must remain unreachable and disabled, and public Mission Studio must remain a local, non-generative preview.

[Access readiness dossier](../../docs/MANZO_AI_COPILOT_P5_6_ACCESS_FREE_ONBOARDING_2026-11-18.md).

## P5.7 — Alternative Supabase Free authentication (source-only, NOT activated)

- Confirmed the existing MANZO AI Supabase organization is on the **Free** tier and its project is healthy. The repository's `product/auth-staging/config.json` remains `enabled: false`; no invitation, login, card or project was created.
- `supabase-auth.mjs` validates a short-lived bearer session by contacting only the pinned MANZO AI Supabase `/auth/v1/user` endpoint. It requires server-side publishable credentials, a verified non-anonymous `authenticated` user, an explicit UUID allowlist (up to five testers) and a server-only HMAC secret. This does **not** rely on unverified frontend claims or a JWT decoded without signature verification.
- Existing Cloudflare Access remains the Worker default, and the new server-side `AUTH_PROVIDER = "access"` and `SUPABASE_AUTH_CONFIRMED = "false"` switches prevent alternative authentication until a separate owner-controlled release.
- All existing zero-euro, privacy and synthetic-only gates continue to block inference by default. No Worker, route, public CORS, user invite, signing-key migration or Supabase provider call has been deployed.
- Before even a private live test, block pre-auth abuse against Supabase, review GitHub Pages CORS, user session expiration, DPA/retention, and the full Free-plan usage limits.

[Complete P5.7 technical dossier](../../docs/MANZO_AI_COPILOT_P5_7_SUPABASE_AUTH_FREE_2026-11-18.md).

**Release status: OFF. Offline tests with simulated users only.**

## P5.12 — Anti-abuse gate BEFORE Supabase Auth (offline, OFF)

- P5.12 adds a Cloudflare Workers Rate Limiting binding (`PRE_AUTH_LIMITER`) with **12 requests per 60 seconds per Cloudflare location**, checked *before* any attempt to validate a Supabase bearer token. A single fixed key shared by all preview requests avoids collecting IPs/tokens and limits traffic across different source IPs at the same location; it may also block a legitimate tester under attack.
- The limiter is **approximate and per-location**; do not rely on it for global counting or billing. The existing SQLite Durable Object is still the strict authority for AI usage reservations (20/day globally, 3/day per tester, 60-second minimum separation).
- Missing, throwing, or malformed limiter → **503** `PRE_AUTH_RATE_LIMIT_UNAVAILABLE`. Exhaustion → **429** `PRE_AUTH_RATE_LIMIT`. Neither reaches Supabase Auth or Workers AI.
- New mocks validate denial paths and the permitted sequence `rate-limit → Supabase Auth → quota reservation → AI`, without external calls. Static preflight asserts the binding and invocation order.
- The namespace `51218` is a **provisional account-local identifier**, to be checked for uniqueness before a live deploy. All flags remain disabled, `workers_dev=false`, no routes, no CORS, no credentials, no live inference and no merge.

[Read the P5.12 audit](../../docs/MANZO_AI_COPILOT_P5_12_PREAUTH_ABUSE_PROTECTION_2026-11-18.md).

## P5.13 — Browser origin + dormant Supabase session bridge (source only)

- Exact browser origin for later tests: `https://manzo8b.github.io`. CORS is **not authentication** and cannot distinguish different repositories sharing the same GitHub Pages host. Supabase verified identity, server UUID allowlist and durable atomic quota remain mandatory.
- New `BROWSER_CONNECTION_CONFIRMED = "false"` gate is independent of Auth/plan/privacy flags. The Worker handles `OPTIONS` only with correct origin, method and requested headers, without calling Supabase, Durable Objects or AI. Authenticated `POST` retains explicit origin verification **before** rate-limiting and auth.
- Candidate `private-browser-client.mjs` uses only synthetic scenario IDs and a Supabase SDK access token, validates unapproved replies and sanitizes error categories. **It is not imported by the public site**, contains no live API URL and defaults to `enabled:false`.
- CI includes no-network browser/CORS tests and confirms browser approval stays OFF, with `workers_dev=false` and no routes.
- Release remains **blocked** until manual account Free validation, approved endpoint and Rate Limiting namespace, exact tester allowlist, privacy/data-retention review, and a small real synthetic-only test.

[Read P5.13 dossier](../../docs/MANZO_AI_COPILOT_P5_13_BROWSER_CORS_AUTH_OFFLINE_2026-11-18.md).

## P5.14 — Release handoff and diagnostics hardening

- Removed the unauthenticated `/health` endpoint before any future public Worker routing; non-API requests return a generic 404.
- Current release decision: **GO for mocked offline QA only / NO-GO for Worker deployment, session activation or any real inference**.
- Manual owner gates and exact order of account/billing, secret allowlist, namespace, privacy and one synthetic live test are described in the [19 November handoff](../../docs/MISSION_STUDIO_RIPRESA_2026-11-19.md).
- The main GitHub Pages site and the Learning B2B Supabase redirect/auth settings were not modified.

