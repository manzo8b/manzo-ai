/**
 * P5.13 candidate CORS policy. Only the MANZO AI GitHub Pages ORIGIN can
 * read the beta endpoint. An origin includes scheme/host/port, NOT path.
 * GitHub Pages projects share an origin: this is NOT an authorization barrier.
 * Session proof, exact UUID allowlist and global quota remain mandatory.
 *
 * Default OFF even in a deployed Worker. No public routes in Wrangler.
 */
export const MISSION_BROWSER_ORIGIN = "https://manzo8b.github.io";
const API_PATH = "/api/plan";
const ALLOWED_REQUEST_HEADERS = new Set(["authorization", "content-type"]);

export function browserBetaReady(env) {
  return env?.COPILOT_ENABLED === "true" &&
    env?.FREE_PLAN_CONFIRMED === "true" &&
    env?.MODEL_FREE_CONFIRMED === "true" &&
    env?.DATA_PROTECTION_CONFIRMED === "true" &&
    env?.BETA_SYNTHETIC_ONLY === "true" &&
    env?.AUTH_PROVIDER === "supabase" &&
    env?.SUPABASE_AUTH_CONFIRMED === "true" &&
    env?.BROWSER_CONNECTION_CONFIRMED === "true";
}

export function exactApprovedOrigin(request) {
  return request?.headers?.get("origin") === MISSION_BROWSER_ORIGIN;
}

function privateHeaders() {
  return {
    "cache-control": "no-store",
    "x-content-type-options": "nosniff",
    "referrer-policy": "no-referrer",
    "vary": "Origin"
  };
}

function noAccess(status, code) {
  return new Response(JSON.stringify({ ok: false, code }), {
    status,
    headers: {
      ...privateHeaders(),
      "content-type": "application/json; charset=utf-8"
    }
  });
}

/**
 * OPTIONS is a browser negotiation without a token, never a model call.
 * The browser setting must be explicitly approved; otherwise no CORS.
 */
export function preflightResponse(request, env) {
  if (new URL(request.url).pathname !== API_PATH || request.method !== "OPTIONS")
    return noAccess(404, "NOT_FOUND");
  if (!browserBetaReady(env)) return noAccess(503, "BROWSER_CONNECTION_DISABLED");
  if (!exactApprovedOrigin(request)) return noAccess(403, "ORIGIN_NOT_ALLOWED");
  if (request.headers.get("access-control-request-method") !== "POST")
    return noAccess(405, "PREFLIGHT_METHOD_NOT_ALLOWED");
  const requested = request.headers.get("access-control-request-headers");
  if (!requested) return noAccess(400, "PREFLIGHT_HEADERS_REQUIRED");
  const names = requested.split(",").map(n => n.trim().toLowerCase());
  if (names.length < 1 || names.length > 2 || new Set(names).size !== names.length ||
      !names.every(n => ALLOWED_REQUEST_HEADERS.has(n)) ||
      !names.includes("authorization") || !names.includes("content-type"))
    return noAccess(403, "PREFLIGHT_HEADERS_NOT_ALLOWED");
  return new Response(null, {
    status: 204,
    headers: {
      ...privateHeaders(),
      "access-control-allow-origin": MISSION_BROWSER_ORIGIN,
      "access-control-allow-methods": "POST, OPTIONS",
      "access-control-allow-headers": "authorization, content-type",
      "access-control-max-age": "300"
    }
  });
}

/** Attach readable CORS metadata to *all* responses for an approved browser. */
export function withApprovedCors(response, request, env) {
  if (!browserBetaReady(env) || !exactApprovedOrigin(request)) return response;
  const headers = new Headers(response.headers);
  headers.set("access-control-allow-origin", MISSION_BROWSER_ORIGIN);
  headers.set("vary", "Origin");
  headers.set("cache-control", "no-store");
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers
  });
}

export function unauthorizedOriginResponse() {
  return noAccess(403, "ORIGIN_NOT_ALLOWED");
}

export function disabledBrowserResponse() {
  return noAccess(503, "BROWSER_CONNECTION_DISABLED");
}
