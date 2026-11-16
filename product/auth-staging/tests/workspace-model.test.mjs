import test from "node:test";
import assert from "node:assert/strict";
import {isUuid,organizationsFrom,studySnapshot,safeText} from "../src/workspace-model.mjs";
const org="aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa";
const course="bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb";
const other="cccccccc-cccc-4ccc-8ccc-cccccccccccc";
test("organization discovery rejects forged IDs, duplicate organizations and unknown roles",()=>{
 assert.equal(isUuid(org),true);
 assert.equal(isUuid("../secret"),false);
 assert.deepEqual(organizationsFrom({organizations:[]}),[]);
 assert.deepEqual(organizationsFrom({organizations:[{organizationId:org,name:"Team AI",role:"learner"}]}),
  [{id:org,name:"Team AI",role:"learner"}]);
 assert.throws(()=>organizationsFrom({organizations:[{organizationId:"bad",name:"A",role:"owner"}]}));
 assert.throws(()=>organizationsFrom({organizations:[{organizationId:org,name:"A",role:"admin"},{organizationId:org,name:"B",role:"admin"}]}));
 assert.throws(()=>organizationsFrom({organizations:[{organizationId:org,name:"Team",role:"superadmin"}]}));
 assert.throws(()=>organizationsFrom({organizations:{value:"wrong type"}}));
});
test("My Learning renders only actual published and assigned courses",()=>{
 const courses={courses:[
  {id:course,title:"Engineering Assurance",status:"published"},
  {id:other,title:"Private Draft",status:"draft"},
 ]};
 const enrollments={enrollments:[
  {courseId:course,status:"active"},
  {courseId:other,status:"active"}
 ]};
 const progress={progress:[
  {courseId:course,moduleKey:"intro"},
  {courseId:course,moduleKey:"intro"},
  {courseId:course,moduleKey:"practice"},
  {courseId:other,moduleKey:"unpublished"}
 ]};
 assert.deepEqual(studySnapshot(courses,enrollments,progress),[{
  id:course,title:"Engineering Assurance",enrollmentStatus:"active",modulesCompleted:2
 }]);
});
test("An empty real backend response produces no phantom percentages, courses or progress",()=>{
 assert.deepEqual(studySnapshot({courses:[]},{enrollments:[]},{progress:[]}),[]);
 assert.deepEqual(studySnapshot({courses:[{id:course,title:"A course",status:"published"}]},
   {enrollments:[]},{progress:[]}),[]);
 assert.equal(safeText('<img src=x onerror=alert(1)>'),'<img src=x onerror=alert(1)>');
 // Only textContent is used by the renderer. No dynamic innerHTML is allowed.
});
test("Revoked enrollments are excluded even when existing progress remains",()=>{
 assert.deepEqual(studySnapshot({courses:[{id:course,title:"AI Verification",status:"published"}]},
  {enrollments:[{courseId:course,status:"revoked"}]},{progress:[{courseId:course,moduleKey:"m1"}]}),[]);
});
test("Untrusted response shape, unknown status and duplicate rows are rejected",()=>{
 assert.throws(()=>studySnapshot({courses:{}},{enrollments:[]},{progress:[]}));
 assert.throws(()=>studySnapshot({courses:[{id:course,title:"Valid",status:"unknown"}]},
  {enrollments:[]},{progress:[]}));
 assert.throws(()=>studySnapshot({courses:[]},{enrollments:[{courseId:course,status:"active"},{courseId:course,status:"active"}]},{progress:[]}));
 assert.throws(()=>studySnapshot({courses:[]},{enrollments:[]},{progress:[{courseId:"bad",moduleKey:"intro"}]}));
});
