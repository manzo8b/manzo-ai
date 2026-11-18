/**
 * P5.12 — BEFORE remote Supabase Auth validation (not before Cloudflare Access).
 * The binding is Cloudflare Workers' approximate, per-location rate limiter.
 * One shared key is deliberate for this single-tester beta: no client IP,
 * bearer token, email, or student data enters the limiter.
 * This is not a strict global quota and never replaces CopilotQuota.
 */
export const PRE_AUTH_LIMIT_KEY = "mission-copilot:preview:supabase:preauth:v1";
export const PRE_AUTH_POLICY = Object.freeze({ limit: 12, periodSeconds: 60 });

/** @returns {Promise<null | "PRE_AUTH_RATE_LIMIT" | "PRE_AUTH_RATE_LIMIT_UNAVAILABLE">} */
export async function checkPreAuthRateLimit(env) {
  if (typeof env?.PRE_AUTH_LIMITER?.limit !== "function")
    return "PRE_AUTH_RATE_LIMIT_UNAVAILABLE";
  try {
    const result = await env.PRE_AUTH_LIMITER.limit({ key: PRE_AUTH_LIMIT_KEY });
    if (result?.success === true) return null;
    if (result?.success === false) return "PRE_AUTH_RATE_LIMIT";
  } catch {
    // Reject all auth/inference when the limiter is unavailable or throws.
  }
  return "PRE_AUTH_RATE_LIMIT_UNAVAILABLE";
}
