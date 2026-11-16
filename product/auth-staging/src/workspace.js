/* MANZO AI — My Learning read-only pilot
 * The browser never accepts org IDs, scores or progress from user input.
 * Real Supabase Auth + verified Learning Edge API only. No sample learners.
 * Backend feature remains OFF until the authenticated API is deployment-tested.
 */
import {createClient} from "@supabase/supabase-js";
import {isUuid,organizationsFrom,studySnapshot} from "./workspace-model.mjs";
const root=document.querySelector("[data-manzo-workspace]");
if(root){
 const cfg=JSON.parse(document.getElementById("workspace-config").textContent);
 const words=JSON.parse(document.getElementById("workspace-i18n").textContent);
 const $=id=>document.getElementById(id);
 const api=String(cfg.url||"").replace(/\/$/,"")+"/functions/v1/learning-api";
 const info=$("mw-status"),intro=$("mw-identity"),orgs=$("mw-organizations"),cards=$("mw-courses");
 const orgLabel=$("mw-org-label");
 let client=null;
 let epoch=0;
 const controller={current:null};
 const state=(message,type="info")=>{
   info.textContent=message;
   info.dataset.level=type;
   info.setAttribute("role",type==="error"?"alert":"status");
 };
 const element=(tag,className,text)=>{
   const node=document.createElement(tag);
   if(className)node.className=className;
   if(text!==undefined)node.textContent=String(text);
   return node;
 };
 const clear=(container)=>container.replaceChildren();
 const restrict=()=>{clear(orgs);clear(cards);orgLabel.textContent="";};
 function disabled(){
   restrict();
   state(words.pending,"notice");
 }
 function loggedOut(){
   restrict();
   intro.textContent="";
   $("mw-signout").hidden=true;
   $("mw-signin").hidden=false;
   state(words.signInRequired,"error");
 }
 async function getAuth(){
   const {data:{user}={},error}=await client.auth.getUser();
   if(error||!user||!user.email_confirmed_at)return null;
   const {data:{session}={},error:sessionError}=await client.auth.getSession();
   if(sessionError||!session?.access_token||session.user?.id!==user.id)return null;
   return {user,token:session.access_token};
 }
 async function call(path,token,signal){
   const res=await fetch(api+path,{
     method:"GET",mode:"cors",credentials:"omit",cache:"no-store",
     referrerPolicy:"no-referrer",signal,
     headers:{Authorization:"Bearer "+token,apikey:cfg.publishableKey,Accept:"application/json"}
   });
   if(!res.ok){
     if(res.status===401)throw Error("session");
     if(res.status===403)throw Error("forbidden");
     if(res.status===429)throw Error("rate_limited");
     if(res.status===503)throw Error("unavailable");
     throw Error("service");
   }
   const type=res.headers.get("content-type")||"";
   if(!type.includes("application/json"))throw Error("invalid_response");
   return res.json();
 }
 const messageFor=err=>{
   if(err?.name==="AbortError")return "";
   switch(err?.message){
     case "session":return words.sessionExpired;
     case "forbidden":return words.accessDenied;
     case "rate_limited":return words.rateLimited;
     case "unavailable":return words.unavailable;
     default:return words.error;
   }
 };
 async function selectOrganization(org,token){
   if(!isUuid(org.id))return;
   const current=++epoch;
   controller.current?.abort();
   const abort=new AbortController();
   controller.current=abort;
   clear(cards);
   orgLabel.textContent=org.name;
   state(words.loadingCourses);
   for(const button of orgs.querySelectorAll("button[data-org]")){
     button.setAttribute("aria-pressed",String(button.dataset.org===org.id));
   }
   const prefix="/v1/organizations/"+encodeURIComponent(org.id)+"/learning";
   try{
     const [courses,enrollments,progress]=await Promise.all([
       call(prefix+"/courses",token,abort.signal),
       call(prefix+"/enrollments",token,abort.signal),
       call(prefix+"/progress",token,abort.signal)
     ]);
     if(current!==epoch)return;
     const records=studySnapshot(courses,enrollments,progress);
     if(records.length===0){state(words.noCourses);return}
     for(const course of records){
       const card=element("article","mw-course");
       const head=element("div","mw-course-head");
       head.append(element("span","mw-course-eyebrow",words.assignedCourse));
       head.append(element("span","mw-course-badge",course.enrollmentStatus==="completed"?words.completed:words.active));
       card.append(head,element("h3","mw-course-title",course.title));
       card.append(element("p","mw-course-progress",course.modulesCompleted+" "+words.modulesCompleted));
       card.append(element("p","mw-course-footnote",words.noCertificate));
       cards.append(card);
     }
     state(words.coursesLoaded);
   }catch(err){
     if(current!==epoch||err?.name==="AbortError")return;
     state(messageFor(err),"error");
   }
 }
 async function start(){
   state(words.verifying);
   if(!cfg.enabled||cfg.authMode!=="invite-only"||!cfg.publishableKey||!cfg.url){
     disabled();return;
   }
   try{
     client=createClient(cfg.url,cfg.publishableKey,{
       auth:{
         flowType:"implicit",persistSession:true,autoRefreshToken:true,
         storage:window.sessionStorage,storageKey:"manzo-learning-b2b-session",
         detectSessionInUrl:false
       }
     });
     // getUser() validates identity with Auth; never trust cached user claims.
     const auth=await getAuth();
     if(!auth){loggedOut();return}
     intro.textContent=words.verifiedAccount+": "+String(auth.user.email||"");
     $("mw-signout").hidden=false;
     $("mw-signin").hidden=true;
     if(cfg.workspaceApiEnabled!==true){disabled();return}
     state(words.loadingOrganizations);
     const list=organizationsFrom(await call("/v1/learning/organizations",auth.token));
     if(list.length===0){state(words.noOrganization);return}
     for(const org of list){
       const button=element("button","mw-org-button",org.name);
       button.type="button";
       button.dataset.org=org.id;
       button.setAttribute("aria-pressed","false");
       button.addEventListener("click",()=>{void selectOrganization(org,auth.token)});
       orgs.append(button);
     }
     await selectOrganization(list[0],auth.token);
   }catch(err){state(messageFor(err),"error")}
 }
 $("mw-signout").addEventListener("click",async()=>{
   ++epoch; controller.current?.abort();
   if(!client)return;
   try{await client.auth.signOut()}catch{}
   loggedOut();
 });
 void start();
}
