import test from "node:test";
import assert from "node:assert/strict";
import worker, {
  MODEL, SCHEMA, QUOTA_POLICY, CopilotQuota, authenticatedPrincipal,
  validateInput, validateModelOutput
} from "./worker.mjs";

const AUD = "access-audience-preview-test-v1";
const SALT = "b8da6b77e3a12fbdefb48b1c18a19898-private-test-hmac-salt";
const payload = {
  tema: "Il ciclo dell'acqua", destinatari: "secondaria_primo_grado",
  durataMinuti: 30, tipoRisorsa: "immagini",
  obiettivo: "Ordinare e spiegare tre fasi del ciclo dell'acqua"
};
const answer = {
  obiettivo: "Ordinare le fasi del ciclo dell'acqua e spiegarne i collegamenti.",
  attivita: [
    "Gli studenti osservano una rappresentazione corretta del ciclo dell'acqua.",
    "In piccoli gruppi spiegano con parole proprie le relazioni principali."
  ],
  criteriDiVerifica: "Ogni studente dispone le fasi in sequenza e motiva almeno una relazione.",
  adattamenti: "Prevedere una descrizione testuale della figura e parole-chiave accessibili."
};
function request(body, headers = {}, method = "POST") {
  return new Request("https://preview.example.test/api/plan", {
    method,
    ...(method === "POST" ? { body: typeof body === "string" ? body : JSON.stringify(body) } : {}),
    headers: { "content-type": "application/json", ...headers }
  });
}
const ctx = (email = "teacher@example.test", aud = AUD) => ({
  access: { aud, getIdentity: async () => ({ email }) }
});
function quotaFixture() {
  const values = new Map();
  let clock = Date.now();
  let queue = Promise.resolve();
  const state = { storage: { transaction(fn) {
    // Emulate serialized/atomic SQLite Durable Object transactions.
    const p = queue.then(() => fn({
      get: async key => structuredClone(values.get(key)),
      put: async (key, value) => { values.set(key, structuredClone(value)); }
    }));
    queue = p.catch(() => {});
    return p;
  } } };
  const instance = new CopilotQuota(state);
  instance.clock = () => clock;
  const binding = {
    idFromName(name) { assert.equal(name,"mission-copilot-global-v1"); return name; },
    get() { return { fetch: req => instance.fetch(req) }; }
  };
  return {
    binding,
    values,
    setNow(value) { clock=value; },
    advance(ms) { clock+=ms; }
  };
}
const env = (mockAI = async () => ({ response: JSON.stringify(answer) }), q = quotaFixture()) => ({
  COPILOT_ENABLED: "true",
  FREE_PLAN_CONFIRMED: "true",
  MODEL_FREE_CONFIRMED: "true",
  DATA_PROTECTION_CONFIRMED: "true",
  ACCESS_AUD: AUD,
  QUOTA_HASH_SALT: SALT,
  GLOBAL_QUOTA: q.binding,
  AI: { run: mockAI }
});
async function read(response) { return { status: response.status, data: await response.json() }; }
async function reserve(q, subject = "a".repeat(64)) {
  const result = await q.binding.get().fetch(new Request("https://quota.internal/reserve", {
    method:"POST", headers:{"content-type":"application/json"},
    body:JSON.stringify({subject})
  }));
  return read(result);
}

test("P2 is disabled by default: neither account nor model gets called", async () => {
  let calls=0;
  const out=await read(await worker.fetch(request(payload), {
    AI: { run: () => {calls++;} }
  }, ctx()));
  assert.equal(out.status, 503);
  assert.equal(out.data.code, "COPILOT_DISABLED");
  assert.equal(calls,0);
});
test("P2 zero-euro consent flags BOTH required and model binding mandatory", async () => {
  let calls=0; const fake=async()=>{calls++; return {response:JSON.stringify(answer)};};
  const standard=env(fake);
  for(const update of [
    {FREE_PLAN_CONFIRMED:"false"},{MODEL_FREE_CONFIRMED:"false"},
    {AI:null}
  ]){
    const out=await read(await worker.fetch(request(payload),{...standard,...update},ctx()));
    assert.equal(out.status,503);
    assert.equal(out.data.code,"ZERO_EURO_POLICY_NOT_CONFIRMED");
  }
  assert.equal(calls,0);
});
test("P3 privacy approval is independent of Free-plan approval and blocks all AI calls", async () => {
  let calls = 0;
  const fake = async () => { calls++; return { response: JSON.stringify(answer) }; };
  for (const value of ["false", undefined, "", "approved"]) {
    const out = await read(await worker.fetch(
      request(payload),
      { ...env(fake), DATA_PROTECTION_CONFIRMED: value },
      ctx()
    ));
    assert.equal(out.status, 503);
    assert.equal(out.data.code, "DATA_PROTECTION_NOT_CONFIRMED");
  }
  assert.equal(calls, 0);
});
test("P2 Cloudflare Access context is mandatory; browser headers cannot spoof it", async () => {
  let calls=0; const standard=env(async()=>{calls++;});
  for(const context of [
    undefined, {}, {access:{aud:AUD}}, ctx("teacher@example.test","wrong-audience"),
    ctx("not-an-address"), ctx("")
  ]){
    const out=await read(await worker.fetch(request(payload,{
      "Cf-Access-Jwt-Assertion":"fake-token",
      "authorization":"Bearer forged-browser-token"
    }),standard,context));
    assert.equal(out.status,401);
    assert.equal(out.data.code,"CLOUDFLARE_ACCESS_REQUIRED");
  }
  assert.equal(calls,0);
});
test("P2 HMAC principal is stable, non-identifying and fails without secret", async () => {
  const standard=env();
  const first=await authenticatedPrincipal(ctx("TEACHER@EXAMPLE.TEST"),standard);
  const second=await authenticatedPrincipal(ctx("teacher@example.test"),standard);
  assert.match(first,/^[0-9a-f]{64}$/);
  assert.equal(first,second);
  assert.ok(!first.includes("teacher"));
  assert.equal(await authenticatedPrincipal(ctx(),{...standard,QUOTA_HASH_SALT:"short"}),null);
});
test("P2 one authorized request uses atomic quota before IA and remains unapproved", async()=>{
  let invoked=null;
  const q=quotaFixture();
  const standard=env(async(model, options)=>{
    invoked={model,options};
    const saved=q.values.get("daily-ledger");
    assert.equal(saved?.total,1,"Must reserve BEFORE calling model");
    return {response:JSON.stringify(answer)};
  },q);
  const response=await worker.fetch(request(payload),standard,ctx());
  const out=await read(response);
  assert.equal(out.status,200);
  assert.equal(out.data.schema,SCHEMA);
  assert.equal(out.data.teacherApproval,false);
  assert.equal(out.data.status,"bozza_non_approvata");
  assert.equal(out.data.model,MODEL);
  assert.ok(invoked && invoked.options.max_completion_tokens<=650);
  assert.equal(response.headers.get("access-control-allow-origin"),null);
  assert.equal(response.headers.get("cache-control"),"no-store");
  assert.ok(!JSON.stringify(out).includes("teacher@example.test"));
  assert.ok(!JSON.stringify(q.values.get("daily-ledger")).includes("teacher@example.test"));
});
test("P2 identity and global quota binding failures fail closed",async()=>{
  let invoked=0;
  const standard=env(async()=>{invoked++;return {response:JSON.stringify(answer)};});
  for(const update of [
    {GLOBAL_QUOTA:null},
    {GLOBAL_QUOTA:{idFromName(){return "x"},get(){throw Error("storage offline")}}},
    {QUOTA_HASH_SALT:""},
    {ACCESS_AUD:"another-app-audience"}
  ]){
    const out=await read(await worker.fetch(request(payload),{...standard,...update},ctx()));
    assert.ok(out.status===503||out.status===401);
  }
  assert.equal(invoked,0);
});
test("P2 malformed JSON, too-large input and unsupported media type fail without quota",async()=>{
  const q=quotaFixture();let calls=0;
  const standard=env(async()=>{calls++;},q);
  for(const [body, headers, code] of [
    ["{",{},"INVALID_JSON"],
    ["x".repeat(5000),{},"INPUT_TOO_LARGE"],
    [payload,{"content-type":"text/plain"},"JSON_REQUIRED"],
    [{...payload,tema:"contact student@example.test"},{},"INVALID_OR_PERSONAL_DATA"],
    [{...payload,durataMinuti:90},{},"INVALID_OR_PERSONAL_DATA"]
  ]){
    const out=await read(await worker.fetch(request(body,headers),standard,ctx()));
    assert.ok(out.status>=400);
    assert.equal(out.data.code,code);
  }
  assert.equal(q.values.size,0);
  assert.equal(calls,0);
});
test("P2 per-identity interval and per-day ceiling are enforced atomically",async()=>{
  const q=quotaFixture();const subject="a".repeat(64);
  const a=await reserve(q,subject);
  const b=await reserve(q,subject);
  assert.equal(a.status,200);
  assert.equal(b.status,429);
  assert.equal(b.data.code,"TOO_FREQUENT");
  q.advance(QUOTA_POLICY.minimumIntervalMs+1);
  const c=await reserve(q,subject);
  assert.equal(c.status,200);
  q.advance(QUOTA_POLICY.minimumIntervalMs+1);
  const d=await reserve(q,subject);
  assert.equal(d.status,200);
  q.advance(QUOTA_POLICY.minimumIntervalMs+1);
  const e=await reserve(q,subject);
  assert.equal(e.status,429);
  assert.equal(e.data.code,"USER_DAILY_LIMIT");
  assert.equal(q.values.get("daily-ledger").total,3);
});
test("P2 absolute global cap across identities and concurrent reservations",async()=>{
  const q=quotaFixture();
  const subjects=Array.from({length:80},(_,i)=>i.toString(16).padStart(64,"0"));
  const results=await Promise.all(subjects.map(s=>reserve(q,s)));
  assert.equal(results.filter(r=>r.status===200).length,QUOTA_POLICY.globalDaily);
  assert.equal(results.filter(r=>r.status===429).length,80-QUOTA_POLICY.globalDaily);
  assert.equal(q.values.get("daily-ledger").total,QUOTA_POLICY.globalDaily);
  assert.ok(results.filter(r=>r.status===429).every(r=>r.data.code==="GLOBAL_DAILY_LIMIT"));
});
test("P2 global counters reset at UTC day boundary, no historical email records",async()=>{
  const q=quotaFixture();
  q.setNow(Date.parse("2026-11-18T23:58:00.000Z"));
  assert.equal((await reserve(q)).status,200);
  q.setNow(Date.parse("2026-11-19T00:01:00.000Z"));
  assert.equal((await reserve(q)).status,200);
  const ledger=q.values.get("daily-ledger");
  assert.equal(ledger.day,"2026-11-19");
  assert.equal(ledger.total,1);
  assert.deepEqual(Object.keys(ledger.people),["a".repeat(64)]);
});
test("P2 failed inference still consumes reservation, no bypass via retry",async()=>{
  const q=quotaFixture(); let calls=0;
  const standard=env(async()=>{calls++;throw Error("provider quota exhausted")},q);
  const a=await read(await worker.fetch(request(payload),standard,ctx()));
  const b=await read(await worker.fetch(request(payload),standard,ctx()));
  assert.equal(a.status,503);
  assert.equal(a.data.code,"PROVIDER_UNAVAILABLE_OR_QUOTA_EXCEEDED");
  assert.equal(b.status,429);
  assert.equal(b.data.code,"TOO_FREQUENT");
  assert.equal(calls,1);
  assert.equal(q.values.get("daily-ledger").total,1);
});
test("P2 invalid model replies never signal approval, yet consume quota",async()=>{
  const q=quotaFixture();
  const standard=env(async()=>({response:"Not JSON"}),q);
  const out=await read(await worker.fetch(request(payload),standard,ctx()));
  assert.equal(out.status,502);
  assert.equal(out.data.code,"MODEL_OUTPUT_UNVERIFIED");
  assert.equal(out.data.teacherApproval,undefined);
  assert.equal(q.values.get("daily-ledger").total,1);
});
test("P2 private only: no open API and health does not call model",async()=>{
  const info=await read(await worker.fetch(new Request("https://preview.example.test/health"),{}));
  assert.equal(info.status,200);
  assert.equal(info.data.enabled,false);
  const missing=await read(await worker.fetch(new Request("https://preview.example.test/open"),{}));
  assert.equal(missing.status,404);
  const get=await read(await worker.fetch(new Request("https://preview.example.test/api/plan"),{}));
  assert.equal(get.status,405);
  assert.equal(missing.data.schema,SCHEMA);
});
test("P2 validators preserve only the five approved inputs",()=>{
  const cleaned=validateInput({...payload,hiddenSecret:"not forwarded"});
  assert.deepEqual(Object.keys(cleaned),
    ["tema","destinatari","durataMinuti","tipoRisorsa","obiettivo"]);
  assert.deepEqual(validateModelOutput(JSON.stringify(answer)),answer);
  assert.equal(validateModelOutput("{not-json}"),null);
});
