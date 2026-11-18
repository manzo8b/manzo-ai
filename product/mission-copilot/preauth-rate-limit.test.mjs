import test from "node:test";
import assert from "node:assert/strict";
import { checkPreAuthRateLimit, PRE_AUTH_LIMIT_KEY, PRE_AUTH_POLICY } from "./preauth-rate-limit.mjs";

test("P5.12 local pre-auth binding policy is fixed, content-free, and conservative", () => {
  assert.deepEqual(PRE_AUTH_POLICY, { limit: 12, periodSeconds: 60 });
  assert.equal(PRE_AUTH_LIMIT_KEY, "mission-copilot:preview:supabase:preauth:v1");
  assert.ok(Object.isFrozen(PRE_AUTH_POLICY));
});

test("P5.12 available limiter allows a request without leaking any user input", async () => {
  let calls = 0;
  const bound = { PRE_AUTH_LIMITER: {
    async limit(arg) {
      calls++;
      assert.deepEqual(arg, { key: PRE_AUTH_LIMIT_KEY });
      return { success: true };
    }
  }};
  assert.equal(await checkPreAuthRateLimit(bound), null);
  assert.equal(calls, 1);
});

test("P5.12 blocked limiter returns rate-limit code", async () => {
  const bound = { PRE_AUTH_LIMITER: { async limit() { return { success: false }; } } };
  assert.equal(await checkPreAuthRateLimit(bound), "PRE_AUTH_RATE_LIMIT");
});

test("P5.12 missing, throwing, or malformed limiter fails closed", async () => {
  const cases = [
    undefined,
    {},
    { PRE_AUTH_LIMITER: null },
    { PRE_AUTH_LIMITER: {} },
    { PRE_AUTH_LIMITER: { limit: "not-a-function" } },
    { PRE_AUTH_LIMITER: { limit: () => { throw Error("unavailable"); } } },
    { PRE_AUTH_LIMITER: { async limit() { throw Error("backend down"); } } },
    { PRE_AUTH_LIMITER: { async limit() { return {}; } } },
    { PRE_AUTH_LIMITER: { async limit() { return { success: "true" }; } } },
    { PRE_AUTH_LIMITER: { async limit() { return undefined; } } }
  ];
  for (const candidate of cases)
    assert.equal(await checkPreAuthRateLimit(candidate), "PRE_AUTH_RATE_LIMIT_UNAVAILABLE");
});
