import test from "node:test";
import assert from "node:assert/strict";
import {
  MISSION_BROWSER_ORIGIN, browserBetaReady, exactApprovedOrigin,
  preflightResponse, withApprovedCors
} from "./browser-origin.mjs";

const enabled = () => ({
  COPILOT_ENABLED: "true",
  FREE_PLAN_CONFIRMED: "true",
  MODEL_FREE_CONFIRMED: "true",
  DATA_PROTECTION_CONFIRMED: "true",
  BETA_SYNTHETIC_ONLY: "true",
  AUTH_PROVIDER: "supabase",
  SUPABASE_AUTH_CONFIRMED: "true",
  BROWSER_CONNECTION_CONFIRMED: "true"
});
const request = (origin, method = "OPTIONS", headers = {}) =>
  new Request("https://private.example.invalid/api/plan", {
    method, headers: {
      ...(origin === null ? {} : { origin }),
      ...(method === "OPTIONS" ? {
        "access-control-request-method": "POST",
        "access-control-request-headers": "authorization, content-type"
      } : {}),
      ...headers
    }
  });

test("P5.13 dedicated browser access is OFF unless every server release flag is true", () => {
  assert.equal(MISSION_BROWSER_ORIGIN, "https://manzo8b.github.io");
  assert.equal(browserBetaReady(enabled()), true);
  for (const key of Object.keys(enabled()))
    assert.equal(browserBetaReady({ ...enabled(), [key]: "false" }), false, key);
  assert.equal(browserBetaReady({}), false);
});

test("P5.13 permitted preflight returns exact CORS without cookies or credentials", async () => {
  const response = preflightResponse(request(MISSION_BROWSER_ORIGIN), enabled());
  assert.equal(response.status, 204);
  assert.equal(response.headers.get("access-control-allow-origin"), MISSION_BROWSER_ORIGIN);
  assert.equal(response.headers.get("access-control-allow-methods"), "POST, OPTIONS");
  assert.equal(response.headers.get("access-control-allow-headers"), "authorization, content-type");
  assert.equal(response.headers.get("access-control-max-age"), "300");
  assert.equal(response.headers.get("access-control-allow-credentials"), null);
  assert.equal(response.headers.get("vary"), "Origin");
  assert.equal(response.headers.get("cache-control"), "no-store");
});

test("P5.13 disabled config and forged/sibling/null origins fail with no CORS", async () => {
  const forbidden = [
    null, "null", "", "http://manzo8b.github.io",
    "https://manzo8b.github.io.evil.example",
    "https://evil.example", "https://manzo8b.github.io:443",
    "https://manzo8b.github.io/manzo-ai", "HTTPS://manzo8b.github.io"
  ];
  for (const origin of forbidden) {
    const req = request(origin);
    assert.equal(exactApprovedOrigin(req), false);
    const response = preflightResponse(req, enabled());
    assert.equal(response.status, 403, String(origin));
    assert.equal(response.headers.get("access-control-allow-origin"), null);
  }
  const off = preflightResponse(request(MISSION_BROWSER_ORIGIN), {
    ...enabled(), BROWSER_CONNECTION_CONFIRMED: "false"
  });
  assert.equal(off.status, 503);
  assert.equal(off.headers.get("access-control-allow-origin"), null);
});

test("P5.13 reject unsafe preflight methods, requested headers and wrong routes", async () => {
  for (const headers of [
    { "access-control-request-method": "GET" },
    { "access-control-request-method": "DELETE" },
    { "access-control-request-headers": "authorization, cookie" },
    { "access-control-request-headers": "x-admin-token, content-type" },
    { "access-control-request-headers": "authorization, authorization" },
    { "access-control-request-headers": "authorization" },
    { "access-control-request-headers": "content-type" },
    { "access-control-request-headers": "" }
  ]) {
    const response = preflightResponse(request(MISSION_BROWSER_ORIGIN, "OPTIONS", headers), enabled());
    assert.ok(response.status === 403 || response.status === 400 ||
      response.status === 405);
    assert.equal(response.headers.get("access-control-allow-origin"), null);
  }
  const wrongPath = new Request("https://private.example.invalid/private", {
    method: "OPTIONS", headers: { origin: MISSION_BROWSER_ORIGIN }
  });
  assert.equal(preflightResponse(wrongPath, enabled()).status, 404);
});

test("P5.13 CORS errors are readable only with matching origin AND approved flags", async () => {
  for (const status of [200, 401, 429, 502, 503]) {
    const raw = new Response(JSON.stringify({ ok: false }), {
      status, headers: { "content-type": "application/json" }
    });
    const approved = withApprovedCors(raw, request(MISSION_BROWSER_ORIGIN, "POST"), enabled());
    assert.equal(approved.status, status);
    assert.equal(approved.headers.get("access-control-allow-origin"), MISSION_BROWSER_ORIGIN);
    assert.equal(approved.headers.get("cache-control"), "no-store");
    assert.equal(approved.headers.get("access-control-allow-credentials"), null);
    assert.deepEqual(await approved.json(), { ok: false });
  }
  for (const origin of [null, "https://evil.example"]) {
    const denied = withApprovedCors(
      new Response("blocked", { status: 401 }), request(origin, "POST"), enabled()
    );
    assert.equal(denied.headers.get("access-control-allow-origin"), null);
  }
  const disabled = withApprovedCors(
    new Response("disabled", { status: 503 }),
    request(MISSION_BROWSER_ORIGIN, "POST"),
    { ...enabled(), BROWSER_CONNECTION_CONFIRMED: "false" }
  );
  assert.equal(disabled.headers.get("access-control-allow-origin"), null);
});
