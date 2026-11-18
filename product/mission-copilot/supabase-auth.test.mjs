import test from "node:test";
import assert from "node:assert/strict";
import { authenticatedSupabasePrincipal } from "./supabase-auth.mjs";

const ID_A = "11111111-1111-4111-8111-111111111111";
const ID_B = "22222222-2222-4222-8222-222222222222";
const TOKEN = "header.payload.signature"; // shape only: fixture is NOT a real JWT
const KEY = "sb_publishable_offline_fixture_not_an_actual_key_123";
const SALT = "fictitious-private-test-only-audit-salt-66dd99aa";
const goodUser = Object.freeze({
  id: ID_A, role: "authenticated", is_anonymous: false,
  email_confirmed_at: "2026-11-18T11:00:00.000Z"
});
const safeEnv = () => ({
  SUPABASE_AUTH_CONFIRMED: "true",
  SUPABASE_PUBLISHABLE_KEY: KEY,
  SUPABASE_ALLOWED_TESTER_IDS: JSON.stringify([ID_A]),
  QUOTA_HASH_SALT: SALT
});
const request = (authorization = `Bearer ${TOKEN}`) => new Request(
  "https://private-worker.example.invalid/api/plan", {
    method: "POST",
    headers: authorization ? { authorization } : {}
  }
);
const trustedAuth = (user = goodUser, status = 200) => async (url, options) => {
  assert.equal(url, "https://bjydnaejpxwubmxpnpnv.supabase.co/auth/v1/user");
  assert.equal(options.method, "GET");
  assert.equal(options.redirect, "error");
  assert.equal(options.headers.authorization, `Bearer ${TOKEN}`);
  assert.equal(options.headers.apikey, KEY);
  assert.equal(options.cache, "no-store");
  assert.equal(options.headers["cache-control"], "no-store");
  return new Response(JSON.stringify(user), {
    status, headers: { "content-type": "application/json" }
  });
};

test("P5.7 confirmed user in explicit allowlist gets only pseudonymous HMAC identity", async () => {
  const a = await authenticatedSupabasePrincipal(request(), safeEnv(), trustedAuth());
  const b = await authenticatedSupabasePrincipal(request(), safeEnv(), trustedAuth());
  assert.match(a, /^[a-f0-9]{64}$/);
  assert.equal(a, b);
  assert.ok(!a.includes(ID_A));
  assert.ok(!a.includes(TOKEN));
  const different = await authenticatedSupabasePrincipal(request(), {
    ...safeEnv(), SUPABASE_ALLOWED_TESTER_IDS: JSON.stringify([ID_B])
  }, trustedAuth({ ...goodUser, id: ID_B }));
  assert.match(different, /^[a-f0-9]{64}$/);
  assert.notEqual(a, different);
});

test("P5.7 disabled/misconfigured auth and invalid bearer never reach the Auth endpoint", async () => {
  let calls = 0;
  const mock = async () => { calls++; throw Error("Unexpected auth call"); };
  const e = safeEnv();
  const cases = [
    [request(), { ...e, SUPABASE_AUTH_CONFIRMED: "false" }],
    [request(), { ...e, SUPABASE_AUTH_CONFIRMED: undefined }],
    [request(), { ...e, SUPABASE_PUBLISHABLE_KEY: "" }],
    [request(), { ...e, SUPABASE_PUBLISHABLE_KEY: "service-role-not-allowed" }],
    [request(), { ...e, QUOTA_HASH_SALT: "short" }],
    [request(), { ...e, SUPABASE_ALLOWED_TESTER_IDS: "[]" }],
    [request(), { ...e, SUPABASE_ALLOWED_TESTER_IDS: "not json" }],
    [request(), { ...e, SUPABASE_ALLOWED_TESTER_IDS: JSON.stringify(["not-uuid"]) }],
    [request(), { ...e, SUPABASE_ALLOWED_TESTER_IDS: JSON.stringify(Array.from({length: 6}, () => ID_A)) }],
    [request(""), e],
    [request("Bearer forged"), e],
    [request("Bearer x.y.z extra"), e],
    [request("Basic a.b.c"), e]
  ];
  for (const [req, config] of cases)
    assert.equal(await authenticatedSupabasePrincipal(req, config, mock), null);
  assert.equal(calls, 0);
});

test("P5.7 only confirmed, permitted, non-anonymous Auth users can reach quota reservation", async () => {
  const failCases = [
    [{ ...goodUser, id: ID_B }, 200],
    [{ ...goodUser, id: "malformed" }, 200],
    [{ ...goodUser, role: "anon" }, 200],
    [{ ...goodUser, role: "service_role" }, 200],
    [{ ...goodUser, is_anonymous: true }, 200],
    [{ ...goodUser, email_confirmed_at: null }, 200],
    [{ ...goodUser, email_confirmed_at: "not-a-date" }, 200],
    [goodUser, 401],
    [goodUser, 403],
    [{}, 200]
  ];
  for (const [user, status] of failCases)
    assert.equal(await authenticatedSupabasePrincipal(request(), safeEnv(), trustedAuth(user, status)), null);
  assert.equal(await authenticatedSupabasePrincipal(request(), safeEnv(),
    async () => { throw Error("Auth service offline"); }), null);
  assert.equal(await authenticatedSupabasePrincipal(request(), safeEnv(),
    async () => new Response("not-json", { status: 200 })), null);
});

test("P5.7 spoofed browser headers cannot replace a verified Supabase session", async () => {
  let calls = 0;
  const spoof = new Request("https://private-worker.example.invalid/api/plan", {
    method: "POST",
    headers: {
      "x-user-id": ID_A,
      "x-supabase-user": ID_A,
      "cf-access-jwt-assertion": "faked",
      "x-user-email": "teacher@example.test"
    }
  });
  const result = await authenticatedSupabasePrincipal(spoof, safeEnv(), async () => {
    calls++; return new Response(JSON.stringify(goodUser), { status: 200 });
  });
  assert.equal(result, null);
  assert.equal(calls, 0);
});
