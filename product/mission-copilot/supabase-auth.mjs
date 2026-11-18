/**
 * P5.7 candidate auth adapter (OFF until an explicitly approved private trial).
 *
 * Trust boundary: a raw bearer token is NEVER trusted as identity. The trusted
 * Supabase Auth /auth/v1/user endpoint checks it on every candidate request.
 * Unlike direct JWKS validation, this also works with legacy HS256 signing keys.
 *
 * No service_role key, no JWT secret, no user-supplied URL and no user_metadata
 * can grant access. An additional small server-side UUID allowlist is required.
 * This module never sends student content to Supabase and stores no emails.
 */
const AUTH_USER_URL = "https://bjydnaejpxwubmxpnpnv.supabase.co/auth/v1/user";
const JWT = /^Bearer ([A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)$/i;
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

function allowedTesterIds(raw) {
  if (typeof raw !== "string" || raw.length > 600) return null;
  try {
    const ids = JSON.parse(raw);
    if (!Array.isArray(ids) || ids.length < 1 || ids.length > 5 ||
        !ids.every(id => typeof id === "string" && UUID.test(id))) return null;
    return new Set(ids.map(id => id.toLowerCase()));
  } catch {
    return null;
  }
}

export async function authenticatedSupabasePrincipal(request, env, authFetch = globalThis.fetch) {
  // Additional explicit server-only gate, independent of billing/privacy gates.
  if (env?.SUPABASE_AUTH_CONFIRMED !== "true" ||
      typeof env?.SUPABASE_PUBLISHABLE_KEY !== "string" ||
      !/^sb_publishable_[A-Za-z0-9_-]{15,}$/.test(env.SUPABASE_PUBLISHABLE_KEY) ||
      typeof env?.QUOTA_HASH_SALT !== "string" ||
      env.QUOTA_HASH_SALT.length < 32) return null;
  const testers = allowedTesterIds(env?.SUPABASE_ALLOWED_TESTER_IDS);
  if (!testers) return null;

  const authorization = request?.headers?.get("authorization") || "";
  const token = JWT.exec(authorization)?.[1];
  if (!token || token.length > 4096 || typeof authFetch !== "function") return null;

  try {
    // Response is trusted ONLY from the fixed MANZO AI Supabase Auth endpoint.
    // Never follow redirects to another host or forward an unverified user URL.
    const response = await authFetch(AUTH_USER_URL, {
      method: "GET",
      headers: {
        apikey: env.SUPABASE_PUBLISHABLE_KEY,
        authorization: `Bearer ${token}`,
        accept: "application/json",
        "cache-control": "no-store"
      },
      redirect: "error",
      cache: "no-store"
    });
    if (response?.status !== 200) return null;

    const user = await response.json();
    const id = typeof user?.id === "string" ? user.id.toLowerCase() : "";
    if (!UUID.test(id) || !testers.has(id) ||
        user?.role !== "authenticated" ||
        user?.is_anonymous === true ||
        typeof user?.email_confirmed_at !== "string" ||
        !Number.isFinite(Date.parse(user.email_confirmed_at))) return null;

    // The email and bearer are never persisted or forwarded to Workers AI.
    // Prefix avoids collisions with Access identities under the same salt.
    const key = await crypto.subtle.importKey(
      "raw", new TextEncoder().encode(env.QUOTA_HASH_SALT),
      { name: "HMAC", hash: "SHA-256" }, false, ["sign"]
    );
    const digest = await crypto.subtle.sign(
      "HMAC", key, new TextEncoder().encode("supabase-user:" + id)
    );
    return Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, "0")).join("");
  } catch {
    // Auth unavailable, bad JWT, invalid payload, network failure: no inference.
    return null;
  }
}
