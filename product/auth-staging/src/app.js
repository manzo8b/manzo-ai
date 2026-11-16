/*
 * MANZO AI Learning B2B · invite-only client AUTH shell.
 * SOURCE ONLY. Publisher intentionally disabled in production.
 *
 * Authentication: Supabase Auth email/password + verified email.
 * Authorization: NOT in this module. An approved server must check grants.
 * The module never loads team data or makes payments.
 */
import {createClient} from "@supabase/supabase-js";
import {safetyConfig,validEmail,validPassword,confirmedUser,classifyPasswordError} from "./auth-policy.mjs";

const root=document.querySelector("[data-manzo-auth]");
if(root){
  const t=JSON.parse(document.getElementById("auth-locales").textContent);
  const cfg=JSON.parse(document.getElementById("auth-config").textContent);
  const locale=root.dataset.locale;
  const byId=id=>document.getElementById(id);
  const views=["disabled","signin","recover","update","verified","pending"];
  const status=byId("auth-status");
  const submitButtons=[...root.querySelectorAll('button[type="submit"]')];
  let client=null,busy=false,recoveryEvent=false;
  // Supabase redirects with ?error_code=otp_expired when the one-time
  // invitation is expired/already consumed. This is NOT proof that the
  // current authenticated session is invalid.
  let expiredInvite=new URLSearchParams(window.location.search).get("error_code")==="otp_expired";
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
    feedback(expiredInvite?t.linkExpired:t.verified,Boolean(expiredInvite));
  }
  function openSignIn(){
    show("signin");
    feedback(expiredInvite?t.linkExpired:"",Boolean(expiredInvite));
  }
  if(!safetyConfig(cfg,locale)){
    show("disabled");
    feedback("");
  }else{
    client=createClient(cfg.url,cfg.publishableKey,{
      auth:{
        // For an admin-initiated invitation on a static client, use the
        // token-bearing redirect handled by Supabase JS's implicit flow.
        // PKCE needs a verifier generated in the same client session and
        // cannot be assumed for server-initiated invite links.
        flowType:"implicit",
        autoRefreshToken:true,
        persistSession:true,
        storage:window.sessionStorage, // short-lived pilot; not localStorage
        storageKey:"manzo-learning-b2b-session",
        detectSessionInUrl:true,
      },
    });
    show("pending");
    feedback(t.loading);
    // Supabase invokes auth event callbacks synchronously; defer client calls.
    client.auth.onAuthStateChange((event,session)=>{
      if(event==="PASSWORD_RECOVERY"){
        recoveryEvent=true;
        show("update");
        feedback(t.newPasswordHelp);
      }else if(event==="SIGNED_OUT"){
        recoveryEvent=false;
        openSignIn();
      }else if(event==="INITIAL_SESSION"){
        // A missing session is NOT an unverified account. Show the normal
        // sign-in form, rather than leaving users stuck in a warning state.
        if(!session){openSignIn();return}
        if(!recoveryEvent)queueMicrotask(()=>{void verifiedSession()});
      }else if(event==="SIGNED_IN"||event==="TOKEN_REFRESHED"){
        if(session&&!recoveryEvent)queueMicrotask(()=>{void verifiedSession()});
      }
    });
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
      expiredInvite=false;
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
      // Supabase returns a specific AuthApiError (often HTTP 422); never
      // hide it under "Operation failed", and never echo a password to logs.
      const result=await client.auth.updateUser({password});
      if(result.error){
        const type=classifyPasswordError(result.error);
        const messages={
          same:t.passwordSame,
          weak:t.passwordWeak,
          reauth:t.passwordReauth,
          session:t.passwordSession,
          expired:t.passwordExpired,
          rejected:t.passwordRejected,
          generic:t.errorGeneric
        };
        feedback(messages[type]||t.errorGeneric,true);
        return;
      }
      // Password is ALREADY updated. Signing out can fail independently
      // (e.g. network/token issue) and must never turn success into a
      // false "Operation failed" message. Keep the verified session;
      // users may sign out explicitly to test a fresh login.
      event.currentTarget.reset();
      recoveryEvent=false;
      expiredInvite=false;
      show("verified");
      feedback(t.passwordUpdated,false);
    }catch{
      feedback(t.errorGeneric,true);
    }finally{lock(false)}
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
