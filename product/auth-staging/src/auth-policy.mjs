/**
 * MANZO AI Learning B2B · pure authentication boundary rules
 * No remote calls, no storage, no user passwords or token handling.
 */
export const AUTH_ROUTES=Object.freeze({
  it:"/manzo-ai/it/prodotto/learning-b2b/accesso/",
  en:"/manzo-ai/en/product/learning-b2b/sign-in/",
  es:"/manzo-ai/es/producto/learning-b2b/acceso/"
});
export const ORIGIN="https://manzo8b.github.io";
export const MIN_PASSWORD_LENGTH=12;
const EMAIL=/^[^\s@]+@[^\s@]+\.[^\s@]+$/u;

/** Never derive auth callback from user-controlled URL query parameters. */
export function exactCallback(locale,origin=ORIGIN){
  if(!Object.prototype.hasOwnProperty.call(AUTH_ROUTES,locale))throw Error("invalid_locale");
  if(origin!==ORIGIN)throw Error("invalid_origin");
  return origin+AUTH_ROUTES[locale];
}
export function validEmail(value){
  return typeof value==="string" && value.length<=254
    && value.length>=5 && EMAIL.test(value.trim());
}
export function validPassword(value){
  return typeof value==="string" && value.length>=MIN_PASSWORD_LENGTH && value.length<=128;
}
export function confirmedUser(user){
  return Boolean(user && typeof user.id==="string" && typeof user.email==="string"
    && user.email_confirmed_at);
}
/** Never accept a client-side identity as proof of membership/entitlement. */
export function authState(user,serverMemberships=[]){
  if(!confirmedUser(user))return "unverified";
  return "verified_no_access"; // Access requires a verified future backend API.
}
export function safetyConfig(config,locale){
  if(!config || config.enabled!==true)return false;
  if(config.authMode!=="invite-only"||config.requireEmailVerification!==true)return false;
  if(config.projectRef!=="bjydnaejpxwubmxpnpnv")return false;
  if(config.url!=="https://bjydnaejpxwubmxpnpnv.supabase.co")return false;
  if(typeof config.publishableKey!=="string"||!config.publishableKey.startsWith("sb_publishable_"))return false;
  if(config.callback!==exactCallback(locale))return false;
  return true;
}
