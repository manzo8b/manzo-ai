/*
 * MANZO AI Learning B2B · invite-only client AUTH shell.
 * SOURCE ONLY. Publisher intentionally disabled in production.
 *
 * Authentication: Supabase Auth email/password + verified email.
 * Authorization: NOT in this module. An approved server must check grants.
 * The module never loads team data or makes payments.
 */
import {createClient} from "@supabase/supabase-js";
import {safetyConfig,validEmail,validPassword,confirmedUser} from "./auth-policy.mjs";

const root=document.querySelector("[data-manzo-auth]");
if(root){
  const t=JSON.parse(document.getElementById("auth-locales").textContent);
  const cfg=JSON.parse(document.getElementById("auth-config").textContent);
  const locale=root.dataset.locale;
  const byId=id=>document.getElementById(id);
  const views=["disabled","signin","recover","update","verified","pending"];
  const status=byId("auth-status");
  const submitButtons=[...root.querySelectorAll('button[type="submit"]')];
  let client=null,originMode="login",busy=false,recoveryEvent=false;
  const title=byId("auth-view-title");

  function feedback(msg,error=false){
    status.textContent=String(msg);
    status.dataset.level=error?"error":"info";
  }
  function show(view){
    for(const key of views){
      const el=byId("auth-"+key);
      if(el)el.hidden=key!==view;
    }
    root.dataset.view=view;
    // The browser can tab through only the currently visible form.
    const heading=byId("auth-"+view+"-title");
    if(heading){title.textContent=heading.textContent; }
  }
  function lock(value){
    busy=value;
    submitButtons.forEach(button=>{button.disabled=value});
    root.setAttribute("aria-busy",String(value));
  }
  async function verifiedSession(){
    if(!client)return;
    // Do not accept local session.user as identity: getUser verifies with Auth server.
    const {data,error}=await client.auth.getUser();
    if(error||!confirmedUser(data?.user)){
      show("pending");
      feedback(t.unauthorized,true);
      return;
    }
    byId("auth-user-email").textContent=data.user.email||"";
    show("verified");
    feedback(t.verified);
  }
  function openSignIn(){
    show("signin");
    feedback("");
  }
  if(!safetyConfig(cfg,locale)){
    show("disabled");
    feedback(t.disabled);
  }else{
    client=createClient(cfg.url,cfg.publishableKey,{
      auth:{
        flowType:"pkce",
        autoRefreshToken:true,
        persistSession:true,
        detectSessionInUrl:true,
      },
    });
    show("pending");
    feedback(t.loading);
    // Supabase invokes auth event callbacks synchronously; defer client calls.
    client.auth.onAuthStateChange((event)=>{
      if(event==="PASSWORD_RECOVERY"){
        recoveryEvent=true;
        show("update");
        feedback(t.newPasswordHelp);
      }else if(event==="SIGNED_OUT"){
        recoveryEvent=false;
        openSignIn();
      }else if(event==="SIGNED_IN"||event==="TOKEN_REFRESHED"||event==="INITIAL_SESSION"){
        if(!recoveryEvent)queueMicrotask(()=>{void verifiedSession()});
      }
    });
    // Some providers do not emit INITIAL_SESSION until after storage discovery.
    Promise.resolve().then(async()=>{
      const {data,error}=await client.auth.getSession();
      if(error||!data?.session){openSignIn();return;}
      if(!recoveryEvent)await verifiedSession();
    }).catch(()=>{openSignIn();feedback(t.errorGeneric,true)});
  }

  root.querySelector("#auth-forgot").addEventListener("click",()=>{
    show("recover");feedback("");
  });
  for(const button of root.querySelectorAll("[data-auth-back]")){
    button.addEventListener("click",openSignIn);
  }
  root.querySelector("#auth-open-update").addEventListener("click",()=>{
    show("update");feedback(t.newPasswordHelp);
  });
  root.querySelector("#auth-signin-form").addEventListener("submit",async event=>{
    event.preventDefault();
    if(!client||busy)return;
    const data=new FormData(event.currentTarget);
    const email=String(data.get("email")||"").trim();
    const password=String(data.get("password")||"");
    if(!validEmail(email)||!password){feedback(t.errorValidation,true);return}
    lock(true);
    try{
      const result=await client.auth.signInWithPassword({email,password});
      if(result.error){feedback(t.errorCredentials,true);return}
      await verifiedSession();
      event.currentTarget.reset();
    }catch{feedback(t.errorGeneric,true)}
    finally{lock(false)}
  });
  root.querySelector("#auth-recover-form").addEventListener("submit",async event=>{
    event.preventDefault();
    if(!client||busy)return;
    const email=String(new FormData(event.currentTarget).get("email")||"").trim();
    if(!validEmail(email)){feedback(t.errorValidation,true);return}
    lock(true);
    try{
      // Use one exact, audited redirect path. Never accept a next URL from input.
      await client.auth.resetPasswordForEmail(email,{redirectTo:cfg.callback});
      feedback(t.sent);
      event.currentTarget.reset();
    }catch{feedback(t.errorGeneric,true)}
    finally{lock(false)}
  });
  root.querySelector("#auth-update-form").addEventListener("submit",async event=>{
    event.preventDefault();
    if(!client||busy)return;
    const password=String(new FormData(event.currentTarget).get("password")||"");
    if(!validPassword(password)){feedback(t.errorValidation,true);return}
    lock(true);
    try{
      const result=await client.auth.updateUser({password});
      if(result.error){feedback(t.errorGeneric,true);return}
      event.currentTarget.reset();
      recoveryEvent=false;
      await client.auth.signOut({scope:"local"});
      openSignIn();
      feedback(t.passwordUpdated);
    }catch{feedback(t.errorGeneric,true)}
    finally{lock(false)}
  });
  root.querySelector("#auth-signout").addEventListener("click",async()=>{
    if(!client||busy)return;
    lock(true);
    try{
      const {error}=await client.auth.signOut();
      if(error){feedback(t.errorGeneric,true);return}
      openSignIn();
      byId("auth-user-email").textContent="";
      feedback(t.signedOut);
    }catch{feedback(t.errorGeneric,true)}
    finally{lock(false)}
  });
}
