# MANZO AI · Learning B2B Edge API

**Status: SOURCE-ONLY STAGING ADAPTER. NO ENDPOINTS DEPLOYED.**

**My Learning read-only increment:** the verified-user organization list and personally assigned enrollments are now in the source adapter. Existing progress read is explicitly filtered to the actor, including for admins. These are not remotely available until the Edge Function is deployed and security-tested. The separate My Learning frontend is published with API feature flag **OFF**.  
Do not connect the existing public Academy or students to this directory until a dedicated MANZO AI Supabase project exists, has been security-tested, and has appropriate privacy notice and support procedures.

## What this adds

- \`learning-api/router.mjs\`: pure, portable Learning HTTP request policy, validated by Node tests.
- \`learning-api/index.ts\`: Supabase Edge Functions TypeScript adapter, type-checked by Deno in GitHub CI.
- \`tests/router.test.mjs\`: privileged actor, foreign tenant, forbidden payload fields, score isolation, idempotent-response and safe error tests.
- PostgreSQL schema/migrations 0001/0002 (existing): private stored procedures, RLS, seat quotas and server-grade assessment keys.
- OpenAPI v0.4 source-only contract (existing, updated).

### Endpoints represented in the source

\`\`\`text
GET    /v1/learning/organizations
GET    /v1/organizations/:organizationId/learning/courses
GET    /v1/organizations/:organizationId/learning/enrollments
GET    /v1/organizations/:organizationId/learning/progress
POST   /v1/organizations/:organizationId/learning/seats
DELETE /v1/organizations/:organizationId/learning/seats/:memberId
POST   /v1/organizations/:organizationId/learning/enrollments
POST   /v1/organizations/:organizationId/learning/progress
POST   /v1/organizations/:organizationId/learning/attempts
\`\`\`

Real Supabase Edge Function routing is prefixed with \`/functions/v1/learning-api\`. These paths are internal to a **future** managed API, not accessible at the current GitHub Pages domain.

## Credential / authorization model

1. The browser sends a **real Supabase Auth user access JWT** in \`Authorization\` (not a publishable API key masquerading as a user).
2. \`@supabase/server\` verifies the token using \`withSupabase({auth:'user',cors:'disabled'})\`. The normalized identity is \`ctx.userClaims.id\`, not a user ID supplied by the browser.
3. API operations validate UUIDs and strictly reject unrecognized request fields. Scores and progress subject IDs are not client-supplied.
4. Read queries explicitly switch to \`authenticated\` role and set the verified user context inside a transaction. PostgreSQL RLS must constrain both organization and individual records. The backend's elevated PostgreSQL connection is **never** used to return arbitrary records.
5. Write queries call the \`app_private\` routines which recheck tenant membership, role and license (and lock the seat-grant row for quota enforcement).
6. The backend holds the direct/pooler database URL in an encrypted server-side secret. **Never** put this string, Stripe credentials or an AI provider key in a GitHub Pages asset, commit, PR comment, client config or image.

### Required environment settings before a staging deploy

| Variable | Example | Storage |
|---|---|---|
| \`MANZO_DB_POOLER_URL\` | PostgreSQL server-side pooler URI for **new MANZO AI project only** | Supabase Edge Functions secret, not GitHub |
| \`MANZO_ALLOWED_ORIGIN\` | \`https://staging.your-domain.example\` | Supabase environment configuration |
| \`SUPABASE_URL\`, \`SUPABASE_JWKS\`, publishable/secret keys | Injected by the future Supabase project | Supabase-managed, not copied into source |

The origin shown above is a placeholder, **not** a live site or a URL to visit. The backend deliberately rejects unknown origins and does not enable wildcard CORS. \`@supabase/server\`'s default CORS handler must remain **disabled** so it cannot overwrite the strict policy.

### Deployment checklist — do not skip

- [ ] Operator creates a **separate Supabase organization** named MANZO AI and a new EU-region project; Oiko is never reused
- [ ] Operator reviews the actual Supabase subscription cost and approves any nonzero charge
- [ ] Apply migrations in staging after version and grants audit; never run \`000_auth_fixture.sql\` against a managed project
- [ ] Keep \`app_private\` excluded from exposed Data API schemas; review public/default privileges and function roles
- [ ] Verify the exact issuer, audience, JWT signing keys, account confirmation, expiration/revocation, CORS and refresh behavior of the new project
- [ ] Provision a **secret** backend pooler URL; verify TLS and database role permission; never leak it to browser or logs
- [ ] Create at least two verified organizations and test same-tenant success, cross-tenant denial, revocation and concurrent seat assignment with *real* test identities
- [ ] Deploy Edge Function to staging only and perform authenticated HTTP integration tests
- [ ] Configure separate rate limiting, abuse controls, monitoring and alerts (not implemented in this adapter)
- [ ] Complete email invitation, reset password, deletion/export, backup/restore and DPA/privacy work before using customer information
- [ ] Complete paid-plan/Stripe test-mode validation and accounting/tax review before enabling any checkout
- [ ] Only after sign-off, connect Learning UI without disrupting the publicly approved static site

## Automated checks (no real Supabase resources)

\`\`\`bash
node --test product/backend/edge/tests/router.test.mjs
deno check product/backend/edge/learning-api/index.ts
python3 -m unittest discover -s product/backend/tests -p 'test_*.py' -v
\`\`\`

GitHub Actions additionally creates an ephemeral PostgreSQL 16 database to run tenant isolation and seat-concurrency assertions.

## Known limitations

- Not an HTTP deployment, so there is **no tested email sign-in**, active student session, provider secret, public API URL, real report or functioning subscription.
- User-mode JWT verification and typing are validated in the SDK contract, **not yet on a project with real session tokens**.
- API token use is not rate-limited and lacks per-tenant request quotas. Do not expose to the public internet until those controls exist.
- Direct private stored procedure calls use a privileged database connection. Carefully audit failure handling, database user privileges, read-time RLS role switching and DNS/TLS prior to production.
- Reading progress as an admin is allowed by existing RLS policies, but instructor/team reports are not implemented as a separate authorized workflow.
- The module progress mark on the static Academy is **in-memory only** and must never be represented as equivalent to authenticated, server-persisted learning progress.
- The existing assessment SQL supports **single-choice** answers, not unvalidated multiple-choice score calculations. The OpenAPI v0.4 contract was corrected to agree with this.

Useful official references:
- https://supabase.com/docs/guides/functions/auth
- https://supabase.com/docs/guides/functions/auth-headers
- https://supabase.com/docs/guides/functions/connect-to-postgres
- https://supabase.com/docs/guides/functions/secrets
- https://supabase.github.io/server/interfaces/index.UserClaims.html

## My Learning API production boundary

- `GET /v1/learning/organizations` derives active organizations from verified Auth actor using RLS; rejects client-supplied identities.
- `GET /v1/organizations/{id}/learning/enrollments` returns **only the authenticated actor's enrollments**, never the organization roster.
- `GET .../progress` similarly filters by verified `user_id` in addition to RLS; no team scores in this student endpoint.
- UI shows server-backed module completion **counts only**; no inferred percentages, certifications, or course links without approved content versions.
- Published pilot uses `"workspaceApiEnabled":false` and does **not** call the API. Enabling requires real JWT, CORS, RLS, tenant A/B, rate limit and backup/DR tests.
- Never publish a direct pooler URL or privileged key. `app_private` remains an unexposed schema.
