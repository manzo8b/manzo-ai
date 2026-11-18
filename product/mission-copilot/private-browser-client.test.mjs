import test from "node:test";
import assert from "node:assert/strict";
import {
  PRIVATE_BROWSER_CONFIG, PrivateCopilotError,
  requestPrivateSyntheticProposal
} from "./private-browser-client.mjs";

const URL = "https://private-beta.example.invalid/api/plan";
const TOKEN = "header.payload.signature"; // deliberately NOT a valid session
const config = Object.freeze({ enabled: true, endpoint: URL });
const sessionClient = (token = TOKEN) => ({
  auth: { async getSession() { return { data: { session: { access_token: token } }, error: null }; } }
});
const validDraft = {
  schema: "mission-copilot-v0.1",
  status: "bozza_non_approvata",
  teacherApproval: false,
  obiettivo: "Distinguere le tre fasi del ciclo dell'acqua e rappresentarle con ordine.",
  attivita: [
    "Ordinare tre figure illustrate in una sequenza e motivare la scelta.",
    "Descrivere con parole proprie un passaggio del ciclo usando un esempio."
  ],
  criteriDiVerifica: "Ogni partecipante riconosce la sequenza e spiega almeno una relazione.",
  adattamenti: "Predisporre la descrizione testuale delle immagini e un esempio guidato."
};
const response = (body, status = 200, contentType = "application/json") =>
  new Response(typeof body === "string" ? body : JSON.stringify(body), {
    status, headers: { "content-type": contentType }
  });
async function rejectsCode(fn, code) {
  await assert.rejects(fn, error =>
    error instanceof PrivateCopilotError && error.code === code);
}

test("P5.13 default private client cannot reach auth or network", async () => {
  let authCalls = 0, networkCalls = 0;
  assert.deepEqual(PRIVATE_BROWSER_CONFIG, { enabled: false, endpoint: null });
  assert.equal(Object.isFrozen(PRIVATE_BROWSER_CONFIG), true);
  await rejectsCode(() => requestPrivateSyntheticProposal({
    scenarioId: "water_cycle",
    supabase: { auth: { getSession: async () => { authCalls++; } } },
    fetchImpl: async () => { networkCalls++; }
  }), "PRIVATE_BETA_DISABLED");
  assert.equal(authCalls, 0);
  assert.equal(networkCalls, 0);
});

test("P5.13 sends only fixed synthetic ID and temporary JWT, never a raw student brief", async () => {
  let received;
  const result = await requestPrivateSyntheticProposal({
    config, supabase: sessionClient(), scenarioId: "water_cycle",
    fetchImpl: async (url, options) => {
      received = { url, ...options };
      return response(validDraft);
    }
  });
  assert.equal(received.url, URL);
  assert.equal(received.method, "POST");
  assert.equal(received.mode, "cors");
  assert.equal(received.credentials, "omit");
  assert.equal(received.cache, "no-store");
  assert.equal(received.redirect, "error");
  assert.equal(received.headers.authorization, `Bearer ${TOKEN}`);
  assert.equal(received.headers["content-type"], "application/json");
  assert.deepEqual(JSON.parse(received.body), { scenarioId: "water_cycle" });
  assert.equal(result.teacherApproval, false);
  assert.equal(result.status, "bozza_non_approvata");
  assert.equal(result.schema, undefined); // validated, minimal proposal only
});

test("P5.13 malformed/unknown scenario or invalid endpoint never reads a session", async () => {
  let authCalls = 0, networkCalls = 0;
  const client = { auth: { getSession: async () => { authCalls++; } } };
  const network = async () => { networkCalls++; };
  for (const scenarioId of [
    "", null, "unknown", { scenarioId: "water_cycle" }, "admin_dashboard",
    "../../secrets", "studentName=Example"
  ]) await rejectsCode(() => requestPrivateSyntheticProposal({
    config, supabase: client, scenarioId, fetchImpl: network
  }), "SYNTHETIC_SCENARIO_REQUIRED");
  const endpoints = [
    null, "", "http://private.example.invalid/api/plan",
    "https://manzo8b.github.io/api/plan",
    "https://bjydnaejpxwubmxpnpnv.supabase.co/api/plan",
    "https://user:secret@example.invalid/api/plan",
    "https://example.invalid/api/plan?token=secret",
    "https://example.invalid/api/plan#secret",
    "https://example.invalid/api/not-approved",
    "https://localhost/api/plan"
  ];
  for (const endpoint of endpoints)
    await rejectsCode(() => requestPrivateSyntheticProposal({
      config: { enabled: true, endpoint }, scenarioId: "water_cycle",
      supabase: client, fetchImpl: network
    }), "PRIVATE_ENDPOINT_UNCONFIGURED");
  assert.equal(authCalls, 0);
  assert.equal(networkCalls, 0);
});

test("P5.13 missing or malformed session fails before request", async () => {
  let calls = 0;
  for (const token of [undefined, "", "a.b", "Bearer a.b.c", "notjwt", "x".repeat(4097)]) {
    await rejectsCode(() => requestPrivateSyntheticProposal({
      config, scenarioId: "water_cycle",
      supabase: sessionClient(token), fetchImpl: async () => { calls++; }
    }), "SESSION_REQUIRED");
  }
  await rejectsCode(() => requestPrivateSyntheticProposal({
    config, scenarioId: "water_cycle",
    supabase: { auth: { getSession: async () => { throw Error("TOKEN SECRET"); } } },
    fetchImpl: async () => { calls++; }
  }), "SESSION_REQUIRED");
  assert.equal(calls, 0);
});

test("P5.13 HTTP rate limit, failed auth and provider outages only expose safe codes", async () => {
  const mapping = [
    [401, "SESSION_REQUIRED"], [403, "ORIGIN_NOT_ALLOWED"],
    [429, "PREVIEW_RATE_LIMIT"], [503, "PREVIEW_TEMPORARILY_UNAVAILABLE"],
    [502, "PREVIEW_REQUEST_FAILED"]
  ];
  for (const [status, code] of mapping)
    await rejectsCode(() => requestPrivateSyntheticProposal({
      config, supabase: sessionClient(), scenarioId: "water_cycle",
      fetchImpl: async () => response({ secret: "do-not-display", code: "BACKEND_STACK" }, status)
    }), code);
  await rejectsCode(() => requestPrivateSyntheticProposal({
    config, supabase: sessionClient(), scenarioId: "water_cycle",
    fetchImpl: async () => { throw Error("Bearer header.payload.signature"); }
  }), "PRIVATE_NETWORK_UNAVAILABLE");
});

test("P5.13 invalid/oversized/approved AI replies are rejected", async () => {
  const cases = [
    [response({ ...validDraft, teacherApproval: true }), "UNVERIFIED_DRAFT"],
    [response({ ...validDraft, schema: "other" }), "UNVERIFIED_DRAFT"],
    [response("<!doctype html>", 200, "text/html"), "UNEXPECTED_SERVER_REPLY"],
    [response("not-json"), "UNEXPECTED_SERVER_REPLY"],
    [response("x".repeat(10001)), "UNEXPECTED_SERVER_REPLY"],
    [response({ ...validDraft, attivita: [] }), "UNVERIFIED_DRAFT"]
  ];
  for (const [resp, code] of cases)
    await rejectsCode(() => requestPrivateSyntheticProposal({
      config, supabase: sessionClient(), scenarioId: "water_cycle",
      fetchImpl: async () => resp
    }), code);
});
