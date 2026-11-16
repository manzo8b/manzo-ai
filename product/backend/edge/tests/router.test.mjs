import test from "node:test";
import assert from "node:assert/strict";
import {dispatchLearning,ENDPOINTS,MAX_BODY_BYTES} from "../learning-api/router.mjs";

const actor="11111111-1111-4111-8111-111111111111";
const student="22222222-2222-4222-8222-222222222222";
const foreign="33333333-3333-4333-8333-333333333333";
const org="aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa";
const otherOrg="bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb";
const course="cccccccc-cccc-4ccc-8ccc-ccccccccccca";
const version="dddddddd-dddd-4ddd-8ddd-ddddddddddda";
const base=`/v1/organizations/${org}/learning`;
const called=[];
const data={
 listOrganizations:async args=>{called.push(["organizations",args]);return [{organizationId:org,name:"Enterprise Test",role:"learner"}]},
 listEnrollments:async args=>{called.push(["enrollments",args]);return [{courseId:course,status:"active"}]},
 listCourses:async args=>{called.push(["courses",args]);return [{id:course,title:"Demo",status:"published"}]},
 listProgress:async args=>{called.push(["progress",args]);return [{module_key:"intro",user_id:student}]},
 assignSeat:async args=>{called.push(["seat",args]);return "assigned"},
 releaseSeat:async args=>{called.push(["release",args]);return "released"},
 enroll:async args=>{called.push(["enroll",args]);return "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee"},
 completeModule:async args=>{called.push(["complete",args]);return "ffffffff-ffff-4fff-8fff-ffffffffffff"},
 gradeAssessment:async args=>{called.push(["grade",args]);return "abababab-abab-4bab-8bab-abababababab"}
};
async function run(method,route,body,as=actor,provider=data){
 called.length=0;
 return dispatchLearning({method,path:route,body,actor:as,data:provider});
}
test("API routes exactly match the defined Learning vertical",()=>{
 assert.equal(ENDPOINTS.length,9);
 assert.equal(new Set(ENDPOINTS).size,9);
 assert.equal(MAX_BODY_BYTES,8192);
});
test("identity missing or forged is rejected before touching DB",async()=>{
 assert.deepEqual(await run("GET",base+"/courses",undefined,""),{status:401,body:{code:"authentication_required",status:401}});
 assert.equal(called.length,0);
 assert.equal((await run("GET",base+"/courses",null,"not-a-uuid")).status,401);
 assert.equal(called.length,0);
});
test("tenant and member route IDs must be canonical UUIDs",async()=>{
 assert.equal((await run("GET","/v1/organizations/other/learning/courses")).status,404);
 assert.equal((await run("DELETE",base+"/seats/../../etc/passwd")).status,404);
 assert.equal((await run("DELETE",base+"/seats/not-a-user")).status,404);
});
test("strict seat request: actor is supplied by VERIFIED adapter only",async()=>{
 const result=await run("POST",base+"/seats",{memberUserId:student});
 assert.equal(result.status,200);
 assert.deepEqual(called[0],[ "seat",{actor,organizationId:org,memberUserId:student} ]);
 assert.equal((await run("POST",base+"/seats",{memberUserId:student,actor:foreign})).status,422);
 assert.equal(called.length,0);
 assert.equal((await run("POST",base+"/seats",{memberUserId:student,price:0})).status,422);
});
test("server-scoped seat release and enrollment",async()=>{
 let result=await run("DELETE",base+"/seats/"+student);
 assert.equal(result.body.result,"released");
 assert.equal(called[0][1].actor,actor);
 result=await run("POST",base+"/enrollments",{memberUserId:student,courseId:course});
 assert.equal(result.status,200);
 assert.equal(result.body.state,"active");
 assert.equal(called[0][1].organizationId,org);
 assert.equal((await run("POST",base+"/enrollments",{memberUserId:student,courseId:course,score:100})).status,422);
});
test("student completion rejects fabricated actor, score or unknown module",async()=>{
 const good={courseId:course,versionId:version,moduleKey:"intro"};
 const result=await run("POST",base+"/progress",good);
 assert.equal(result.status,200);
 assert.deepEqual(called[0][1],{actor,organizationId:org,...good});
 assert.equal((await run("POST",base+"/progress",{...good,userId:student})).status,422);
 assert.equal((await run("POST",base+"/progress",{...good,scorePercent:100})).status,422);
 assert.equal((await run("POST",base+"/progress",{...good,moduleKey:"../bad-module"})).status,422);
});
test("assessment accepts only answer choices and never client scores",async()=>{
 const good={courseId:course,versionId:version,assessmentId:"quiz",answers:{q1:"a",q2:"c"}};
 const result=await run("POST",base+"/attempts",good);
 assert.equal(result.status,200);
 assert.equal(result.body.state,"recorded");
 assert.deepEqual(called[0][1],{actor,organizationId:org,...good});
 assert.equal((await run("POST",base+"/attempts",{...good,scorePercent:100})).status,422);
 assert.equal((await run("POST",base+"/attempts",{...good,answers:{q1:{correct:true}}})).status,422);
 assert.equal((await run("POST",base+"/attempts",{...good,answers:{}})).status,422);
 assert.equal(called.length,0);
});
test("reads remain delegated to DB-backed authenticated RLS scope",async()=>{
 const courses=await run("GET",base+"/courses");
 assert.equal(courses.status,200);
 assert.deepEqual(called[0],["courses",{actor,organizationId:org}]);
 const progress=await run("GET",base+"/progress");
 assert.equal(progress.body.progress.length,1);
 assert.deepEqual(called[0],["progress",{actor,organizationId:org}]);
});
test("same actor with foreign tenant never bypasses database checks",async()=>{
 const guarded={assignSeat:async()=>{throw new Error("LEARNING_NOT_ADMIN")}};
 const result=await run("POST",`/v1/organizations/${otherOrg}/learning/seats`,{memberUserId:student},actor,guarded);
 assert.equal(result.status,403);
 assert.equal(result.body.code,"not_authorized");
});
test("business error codes are sanitized; unexpected SQL exceptions are private",async()=>{
 const denied={assignSeat:async()=>{throw Error("LEARNING_NO_SEATS")}};
 const res=await run("POST",base+"/seats",{memberUserId:student},actor,denied);
 assert.equal(res.status,409);
 assert.equal(res.body.code,"seat_limit_reached");
 const unknown={assignSeat:async()=>{throw Error("password: secret-db-connection")}};
 const err=await run("POST",base+"/seats",{memberUserId:student},actor,unknown);
 assert.equal(err.status,500);
 assert.deepEqual(err.body,{status:500,code:"internal_error"});
 assert.equal(JSON.stringify(err).includes("secret-db-connection"),false);
});
test("wrong method is rejected without invoking DB",async()=>{
 const response=await run("PUT",base+"/seats",{memberUserId:student});
 assert.equal(response.status,405);
 assert.equal(called.length,0);
});
test("unknown resource and path traversal cannot select fallback route",async()=>{
 const response=await run("GET",base+"/private-answer-keys");
 assert.equal(response.status,404);
 assert.equal(called.length,0);
});

test("My Learning organization list derives member identity only from verified Auth",async()=>{
 const result=await run("GET","/v1/learning/organizations");
 assert.equal(result.status,200);
 assert.deepEqual(called[0],["organizations",{actor}]);
 assert.equal(result.body.organizations[0].organizationId,org);
 assert.equal((await run("POST","/v1/learning/organizations",{userId:foreign})).status,405);
 assert.equal(called.length,0);
});
test("My Learning enrollments are queried with a verified actor AND org",async()=>{
 const result=await run("GET",base+"/enrollments");
 assert.equal(result.status,200);
 assert.deepEqual(called[0],["enrollments",{actor,organizationId:org}]);
 assert.equal(result.body.enrollments[0].status,"active");
 const unauthorized=await run("GET",`/v1/organizations/${otherOrg}/learning/enrollments`,undefined,actor,{
   listEnrollments:async()=>{throw Error("LEARNING_NOT_ADMIN")}
 });
 assert.equal(unauthorized.status,403);
 assert.equal(unauthorized.body.code,"not_authorized");
});
