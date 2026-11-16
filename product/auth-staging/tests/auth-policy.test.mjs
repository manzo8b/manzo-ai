import test from "node:test";
import assert from "node:assert/strict";
import {AUTH_ROUTES,ORIGIN,MIN_PASSWORD_LENGTH,exactCallback,validEmail,
  validPassword,confirmedUser,authState,safetyConfig,classifyPasswordError} from "../src/auth-policy.mjs";

const good={
 enabled:true, authMode:"invite-only", requireEmailVerification:true,
 projectRef:"bjydnaejpxwubmxpnpnv",
 url:"https://bjydnaejpxwubmxpnpnv.supabase.co",
 publishableKey:"sb_publishable_test_nonsecret",
 callback:ORIGIN+AUTH_ROUTES.it,
};
test("all redirect paths have fixed, distinct locale routes",()=>{
 assert.deepEqual(Object.keys(AUTH_ROUTES),["it","en","es"]);
 assert.equal(new Set(Object.values(AUTH_ROUTES)).size,3);
 for(const locale of Object.keys(AUTH_ROUTES)){
  assert.equal(exactCallback(locale),ORIGIN+AUTH_ROUTES[locale]);
  assert.ok(exactCallback(locale).startsWith("https://manzo8b.github.io/manzo-ai/"));
  assert.throws(()=>exactCallback(locale,"https://evil.test"),/invalid_origin/);
 }
 assert.throws(()=>exactCallback("fr"),/invalid_locale/);
});
test("correct project and explicit activated invite-only policy required",()=>{
 assert.equal(safetyConfig({...good,enabled:false},"it"),false);
 assert.equal(safetyConfig(good,"it"),true);
 assert.equal(safetyConfig({...good,authMode:"public"},"it"),false);
 assert.equal(safetyConfig({...good,requireEmailVerification:false},"it"),false);
 assert.equal(safetyConfig({...good,projectRef:"alvvadydotkvyipatvxz"},"it"),false);
 assert.equal(safetyConfig({...good,publishableKey:"sb_secret_test"},"it"),false);
 assert.equal(safetyConfig({...good,url:"https://example.supabase.co"},"it"),false);
 assert.equal(safetyConfig({...good,callback:"https://evil.test"},"it"),false);
 assert.equal(safetyConfig(good,"en"),false);
 assert.equal(safetyConfig(null,"it"),false);
});
test("only conventional bounded email accepted",()=>{
 assert.equal(validEmail("person@example.test"),true);
 assert.equal(validEmail(" not-email "),false);
 assert.equal(validEmail("not@localhost"),false);
 assert.equal(validEmail({address:"person@example.test"}),false);
 assert.equal(validEmail("a".repeat(255)+"@example.com"),false);
});
test("new password length hardened, no password logging",()=>{
 assert.equal(MIN_PASSWORD_LENGTH,12);
 assert.equal(validPassword("12_characters"),true);
 assert.equal(validPassword("short"),false);
 assert.equal(validPassword("x".repeat(129)),false);
 assert.equal(validPassword(null),false);
});
test("email confirmation is mandatory for recognized identity",()=>{
 const user={id:"11111111-1111-4111-8111-111111111111",email:"student@example.test",email_confirmed_at:null};
 assert.equal(confirmedUser(user),false);
 assert.equal(authState(user), "unverified");
 assert.equal(confirmedUser({...user,email_confirmed_at:"2026-11-16T10:00:00Z"}),true);
});
test("a verified login never implies tenant membership or license",()=>{
 const user={id:"11111111-1111-4111-8111-111111111111",email:"student@example.test",email_confirmed_at:"2026-11-16T10:00:00Z"};
 assert.equal(authState(user),"verified_no_access");
 assert.equal(authState(user,[{role:"owner",grant:"paid"}]),"verified_no_access");
});

test("password changes map Supabase Auth codes into non-sensitive actionable states",()=>{
  assert.equal(classifyPasswordError({code:"same_password",status:422}),"same");
  assert.equal(classifyPasswordError({code:"weak_password",status:422}),"weak");
  assert.equal(classifyPasswordError({code:"reauthentication_needed",status:422}),"reauth");
  assert.equal(classifyPasswordError({code:"session_not_found",status:401}),"session");
  assert.equal(classifyPasswordError({code:"otp_expired",status:403}),"expired");
  assert.equal(classifyPasswordError({code:"unknown_422",status:422}),"rejected");
  assert.equal(classifyPasswordError({message:"password: SECRET-PASSWORD"}),"generic");
  assert.equal(classifyPasswordError(null),"generic");
});
