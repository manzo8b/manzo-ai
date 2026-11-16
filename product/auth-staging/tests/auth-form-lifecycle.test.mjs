import test from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import vm from "node:vm";
import {classifyRecoveryError} from "../src/auth-policy.mjs";

// Run the actual browser module with a tiny DOM/Auth double. The simulated
// dispatch clears event.currentTarget immediately after the synchronous handler
// returns, just as browsers do before async Auth calls have finished.
const original=readFileSync(new URL("../src/app.js",import.meta.url),"utf8");
const script=original.replace(/^import .+;\r?$/gm,"");
if(script.includes('from "@supabase/'))throw Error("Auth imports not isolated");

function createHarness(authOverrides={}){
  const nodes=new Map();
  const node=id=>{
    if(!nodes.has(id)){
      nodes.set(id,{
        textContent:"",dataset:{},hidden:false,disabled:false,fields:{},
        resetCount:0,listeners:{},addEventListener(name,fn){this.listeners[name]=fn},
        reset(){this.resetCount++}
      });
    }
    return nodes.get(id);
  };
  const root={
    dataset:{locale:"it"},attrs:{},
    setAttribute(name,value){this.attrs[name]=value},
    querySelector(selector){return node(selector.slice(1))},
    querySelectorAll(selector){
      if(selector==='button[type="submit"]')return [node("signin-submit"),node("recover-submit"),node("update-submit")];
      if(selector==="[data-auth-back]")return [node("go-back")];
      return [];
    }
  };
  const translations={
    loading:"LOADING",verified:"VERIFIED",sent:"SENT",
    passwordUpdated:"UPDATED",errorGeneric:"ERROR",
    errorCredentials:"CREDENTIALS",errorValidation:"VALIDATION",
    newPasswordHelp:"PASSWORD HELP",unauthorized:"NOT VERIFIED",
    linkExpired:"EXPIRED",passwordRejected:"REJECTED",
    recoveryEmailLimit:"EMAIL QUOTA",recoveryRestrictedEmail:"RECIPIENT RESTRICTED",
    recoveryRateLimit:"RATE LIMIT",recoveryUnavailable:"UNAVAILABLE"
  };
  const document={
    querySelector(selector){return selector==="[data-manzo-auth]"?root:null},
    getElementById(id){
      if(id==="auth-locales")return {textContent:JSON.stringify(translations)};
      if(id==="auth-config")return {textContent:JSON.stringify({enabled:true,callback:"https://example.test"})};
      return node(id);
    }
  };
  const user={id:"test-id",email:"tester@example.test",email_confirmed_at:"2026-01-01T00:00:00Z"};
  const auth={
    onAuthStateChange(){return {data:{subscription:{unsubscribe(){}}}}},
    async getUser(){return {data:{user},error:null}},
    async signInWithPassword(){return {data:{user},error:null}},
    async resetPasswordForEmail(){return {data:{},error:null}},
    async updateUser(){return {data:{user},error:null}},
    async signOut(){return {error:null}},
    ...authOverrides
  };
  class TestFormData {
    constructor(form){assert.ok(form,"the form must exist during dispatch");this.fields=form.fields}
    get(name){return this.fields[name]??null}
  }
  vm.runInNewContext(script,{
    document,window:{location:{search:""},sessionStorage:{}},
    URLSearchParams,FormData:TestFormData,queueMicrotask,
    createClient:()=>({auth}),
    safetyConfig:()=>true,validEmail:()=>true,validPassword:()=>true,
    confirmedUser:()=>true,classifyPasswordError:()=> "rejected",classifyRecoveryError
  },{filename:"auth-app.js"});
  async function submit(formId,fields){
    const form=node(formId);
    form.fields=fields;
    const event={currentTarget:form,preventDefault(){}};
    const promise=form.listeners.submit(event);
    // Simulates the event dispatch boundary before the awaited API settles.
    event.currentTarget=null;
    await promise;
    return {form,status:node("auth-status"),view:root.dataset.view};
  }
  return {submit};
}

test("sign-in never turns an accepted authentication into a stale-event error",async()=>{
  const {submit}=createHarness();
  const result=await submit("auth-signin-form",{email:"tester@example.test",password:"example-password"});
  assert.equal(result.view,"verified");
  assert.equal(result.status.textContent,"VERIFIED");
  assert.equal(result.status.dataset.level,"info");
  assert.equal(result.form.resetCount,1);
});

test("password recovery retains the form after a successful async request",async()=>{
  const {submit}=createHarness();
  const result=await submit("auth-recover-form",{email:"tester@example.test"});
  assert.equal(result.status.textContent,"SENT");
  assert.equal(result.status.dataset.level,"info");
  assert.equal(result.form.resetCount,1);
});

test("password change stays successful when event.currentTarget becomes null",async()=>{
  const {submit}=createHarness();
  const result=await submit("auth-update-form",{password:"a-new-secure-password"});
  assert.equal(result.view,"verified");
  assert.equal(result.status.textContent,"UPDATED");
  assert.equal(result.status.dataset.level,"info");
  assert.equal(result.form.resetCount,1);
});

test("recovery API rejection cannot display a false success notice",async()=>{
  const {submit}=createHarness({async resetPasswordForEmail(){return {error:{status:429,code:"over_email_send_rate_limit"}}}});
  const result=await submit("auth-recover-form",{email:"tester@example.test"});
  assert.equal(result.status.textContent,"EMAIL QUOTA");
  assert.equal(result.status.dataset.level,"error");
  assert.equal(result.form.resetCount,0);
});

test("unauthorized trial email recipients receive an actionable failure",async()=>{
  const {submit}=createHarness({async resetPasswordForEmail(){return {error:{status:400,code:"email_address_not_authorized"}}}});
  const result=await submit("auth-recover-form",{email:"tester@example.test"});
  assert.equal(result.status.textContent,"RECIPIENT RESTRICTED");
  assert.equal(result.status.dataset.level,"error");
  assert.equal(result.form.resetCount,0);
});

test("all three published locales explain recovery email delivery failures",()=>{
  const translations=JSON.parse(readFileSync(new URL("../content.json",import.meta.url),"utf8"));
  for(const locale of ["it","en","es"]){
    for(const key of ["recoveryEmailLimit","recoveryRestrictedEmail","recoveryRateLimit","recoveryUnavailable"]){
      assert.ok(translations[locale][key]?.length>30,locale+" missing "+key);
    }
  }
});
