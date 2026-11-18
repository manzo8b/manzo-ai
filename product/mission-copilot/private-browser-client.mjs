/**
 * P5.13 source-only private browser transport.
 * NOT imported by the public Mission Studio page. This intentionally does
 * not handle sign-in, store tokens, or create accounts. The client-side SDK
 * only supplies the short-lived access token; authorization is always server-side.
 */
import { BETA_CASE_IDS } from "./beta-scenarios.mjs";
import { validateCopilotProposal } from "../../tools/ai-teaching-launchpad/mission-adapter.mjs";

export const PRIVATE_BROWSER_CONFIG = Object.freeze({
  enabled: false,
  endpoint: null // No Worker hostname or public route authorized yet.
});
const MAX_RESPONSE_CHARS = 10_000;
const JWT = /^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/;

function privateEndpoint(value) {
  if (typeof value !== "string" || value.length > 300) return null;
  try {
    const url = new URL(value);
    if (url.protocol !== "https:" ||
        url.username || url.password || url.search || url.hash ||
        url.pathname !== "/api/plan" || url.port ||
        !url.hostname || url.hostname === "localhost" ||
        url.hostname.endsWith(".github.io") ||
        url.hostname.endsWith(".supabase.co")) return null;
    return url.href;
  } catch { return null; }
}

export class PrivateCopilotError extends Error {
  constructor(code) { super(code); this.name = "PrivateCopilotError"; this.code = code; }
}

/**
 * The only permissible input is one server-owned, synthetic scenario ID.
 * The endpoint is code configuration, never a URL from query parameters
 * or browser storage. This candidate remains disabled until reviewed.
 */
export async function requestPrivateSyntheticProposal({
  config = PRIVATE_BROWSER_CONFIG,
  supabase,
  scenarioId,
  fetchImpl = globalThis.fetch
}) {
  if (config?.enabled !== true) throw new PrivateCopilotError("PRIVATE_BETA_DISABLED");
  if (!BETA_CASE_IDS.includes(scenarioId))
    throw new PrivateCopilotError("SYNTHETIC_SCENARIO_REQUIRED");
  const endpoint = privateEndpoint(config.endpoint);
  if (!endpoint) throw new PrivateCopilotError("PRIVATE_ENDPOINT_UNCONFIGURED");
  if (typeof supabase?.auth?.getSession !== "function" ||
      typeof fetchImpl !== "function")
    throw new PrivateCopilotError("AUTH_CLIENT_NOT_CONFIGURED");

  // The browser SDK session supplies ONLY the token. Ignore any cached user
  // claims: Supabase Auth must verify identity and server allowlist on each call.
  let token;
  try {
    const { data, error } = await supabase.auth.getSession();
    if (error) throw error;
    token = data?.session?.access_token;
  } catch {
    throw new PrivateCopilotError("SESSION_REQUIRED");
  }
  if (typeof token !== "string" || token.length > 4096 || !JWT.test(token))
    throw new PrivateCopilotError("SESSION_REQUIRED");

  let response;
  try {
    response = await fetchImpl(endpoint, {
      method: "POST",
      mode: "cors",
      credentials: "omit",
      redirect: "error",
      cache: "no-store",
      headers: {
        authorization: `Bearer ${token}`,
        "content-type": "application/json"
      },
      body: JSON.stringify({ scenarioId })
    });
  } catch {
    // Error details may contain credentials or provider internals.
    throw new PrivateCopilotError("PRIVATE_NETWORK_UNAVAILABLE");
  }

  if (!response || typeof response.text !== "function" ||
      !/^application\/json(?:\s*;|$)/i.test(response.headers?.get("content-type") || ""))
    throw new PrivateCopilotError("UNEXPECTED_SERVER_REPLY");

  const raw = await response.text();
  if (raw.length > MAX_RESPONSE_CHARS)
    throw new PrivateCopilotError("UNEXPECTED_SERVER_REPLY");
  let data;
  try { data = JSON.parse(raw); }
  catch { throw new PrivateCopilotError("UNEXPECTED_SERVER_REPLY"); }

  if (!response.ok) {
    // Only expose known server error categories; never show arbitrary payload.
    const mapped = {
      401: "SESSION_REQUIRED",
      403: "ORIGIN_NOT_ALLOWED",
      429: "PREVIEW_RATE_LIMIT",
      503: "PREVIEW_TEMPORARILY_UNAVAILABLE"
    };
    throw new PrivateCopilotError(mapped[response.status] || "PREVIEW_REQUEST_FAILED");
  }
  try {
    return validateCopilotProposal(data);
  } catch {
    throw new PrivateCopilotError("UNVERIFIED_DRAFT");
  }
}
