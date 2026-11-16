/**
 * MANZO AI · Learning API Edge adapter — NOT DEPLOYED.
 * Auth derives actor ONLY from Supabase verified ctx.userClaims.id.
 * Reads: RLS-scoped database role; writes: private server functions.
 * No client-side SQL, credential, score, billing or entitlement updates.
 */
import { withSupabase } from "npm:@supabase/server@1";
import postgres from "npm:postgres@3.4.7";
import { dispatchLearning, MAX_BODY_BYTES } from "./router.mjs";

const ORIGIN=Deno.env.get("MANZO_ALLOWED_ORIGIN")||"";
const DATABASE_URL=Deno.env.get("MANZO_DB_POOLER_URL")||"";
let connection:ReturnType<typeof postgres>|undefined;
const db=()=>{
 if(!DATABASE_URL)throw Error("missing_backend_configuration");
 if(!connection)connection=postgres(DATABASE_URL,{max:1,prepare:false,ssl:"require",connect_timeout:5,idle_timeout:5,max_lifetime:60});
 return connection;
};
const allowed=(origin:string|null):Record<string,string>|null=>!origin?{}:(origin===ORIGIN&&ORIGIN?{"Access-Control-Allow-Origin":origin,Vary:"Origin"}:null);
const response=(status:number,body:unknown,origin:string|null)=>Response.json(body,{status,headers:{"Cache-Control":"no-store",...(allowed(origin)||{})}});
const adapt=()=>{
 const sql=db();
 return {
  // Session-scoped RLS on every SELECT; no global trusted client can return
  // foreign-tenant records merely because the request guessed an org ID.
  listCourses:({actor,organizationId}:{actor:string,organizationId:string})=>sql.begin(async tx=>{
   await tx`SET LOCAL ROLE authenticated`;
   await tx`SELECT set_config('request.jwt.claim.sub',${actor},true)`;
   return await tx`SELECT id,organization_id AS "organizationId",slug,title,status FROM app.courses
     WHERE organization_id=${organizationId}::uuid ORDER BY created_at DESC LIMIT 100`;
  }),
  listProgress:({actor,organizationId}:{actor:string,organizationId:string})=>sql.begin(async tx=>{
   await tx`SET LOCAL ROLE authenticated`;
   await tx`SELECT set_config('request.jwt.claim.sub',${actor},true)`;
   return await tx`SELECT id,course_id AS "courseId",version_id AS "versionId",
      user_id AS "userId",module_key AS "moduleKey",completed_at AS "completedAt"
      FROM app.learning_progress WHERE organization_id=${organizationId}::uuid
      ORDER BY completed_at DESC LIMIT 200`;
  }),
  assignSeat:async ({actor,organizationId,memberUserId}:{actor:string,organizationId:string,memberUserId:string})=>{
   const [row]=await sql`SELECT app_private.assign_learning_seat(
     ${actor}::uuid,${organizationId}::uuid,${memberUserId}::uuid) AS state`;
   return row.state;
  },
  releaseSeat:async ({actor,organizationId,memberUserId}:{actor:string,organizationId:string,memberUserId:string})=>{
   const [row]=await sql`SELECT app_private.release_learning_seat(
     ${actor}::uuid,${organizationId}::uuid,${memberUserId}::uuid) AS state`;
   return row.state;
  },
  enroll:async ({actor,organizationId,memberUserId,courseId}:{actor:string,organizationId:string,memberUserId:string,courseId:string})=>{
   const [row]=await sql`SELECT app_private.enroll_learning_student(
     ${actor}::uuid,${organizationId}::uuid,
     ${memberUserId}::uuid,${courseId}::uuid) AS id`;
   return row.id;
  },
  completeModule:async ({actor,organizationId,courseId,versionId,moduleKey}:{actor:string,organizationId:string,courseId:string,versionId:string,moduleKey:string})=>{
   const [row]=await sql`SELECT app_private.complete_learning_module(
     ${actor}::uuid,${organizationId}::uuid,${courseId}::uuid,
     ${versionId}::uuid,${moduleKey}) AS id`;
   return row.id;
  },
  gradeAssessment:async ({actor,organizationId,courseId,versionId,assessmentId,answers}:{actor:string,organizationId:string,courseId:string,versionId:string,assessmentId:string,answers:Record<string,string>})=>{
   const [row]=await sql`SELECT app_private.record_learning_assessment(
     ${actor}::uuid,${organizationId}::uuid,${courseId}::uuid,
     ${versionId}::uuid,${assessmentId},${JSON.stringify(answers)}::jsonb) AS id`;
   return row.id;
  }
 };
};
const protectedHandler=withSupabase({auth:"user"},async(req:Request,ctx)=>{
 const origin=req.headers.get("Origin");
 if(origin&&allowed(origin)===null)return response(403,{code:"origin_not_allowed"},null);
 const actor=ctx.userClaims?.id;
 if(typeof actor!=="string"||!actor)return response(401,{code:"authentication_required"},origin);
 const url=new URL(req.url);
 if(url.search||url.pathname.length>400)return response(400,{code:"invalid_request_url"},origin);
 const route=url.pathname.replace(/^\/functions\/v1\/learning-api(?=\/|$)/,"")
    .replace(/^\/learning-api(?=\/|$)/,"");
 if(!route.startsWith("/v1/organizations/"))return response(404,{code:"not_found"},origin);
 let body:unknown=undefined;
 if(req.method==="POST"){
  if(req.headers.get("Content-Type")?.split(";")[0].trim().toLowerCase()!=="application/json")
   return response(415,{code:"unsupported_media_type"},origin);
  const declared=Number(req.headers.get("Content-Length")||0);
  if(!Number.isFinite(declared)||declared>MAX_BODY_BYTES)return response(413,{code:"payload_too_large"},origin);
  const raw=await req.text();
  if(new TextEncoder().encode(raw).byteLength>MAX_BODY_BYTES)return response(413,{code:"payload_too_large"},origin);
  try{body=JSON.parse(raw)}catch{return response(400,{code:"invalid_json"},origin)}
 }
 if(!DATABASE_URL)return response(503,{code:"service_not_configured"},origin);
 const outcome=await dispatchLearning({actor,method:req.method,path:route,body,data:adapt()});
 return response(outcome.status,outcome.body,origin);
});
export default {
 fetch(req:Request):Promise<Response>|Response{
  const origin=req.headers.get("Origin");
  if(req.method==="OPTIONS"){
   const headers=allowed(origin);
   if(!origin||!headers)return response(403,{code:"origin_not_allowed"},null);
   return new Response(null,{status:204,headers:{...headers,
     "Access-Control-Allow-Methods":"GET, POST, DELETE, OPTIONS",
     "Access-Control-Allow-Headers":"Authorization, apikey, Content-Type",
     "Access-Control-Max-Age":"300"}});
  }
  return protectedHandler(req);
 }
};
