/* MANZO AI My Learning — pure, no-side-effects data contract.
   Accept ONLY fields returned by the authenticated Learning API.
   Do not create invented completion percentages or missing course records.
*/
const UUID=/^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
export const isUuid=value=>typeof value==="string"&&UUID.test(value);
export function safeText(value,limit=180){
  return typeof value==="string" ? value.trim().slice(0,limit) : "";
}
export function organizationsFrom(data){
  if(!data||!Array.isArray(data.organizations)||data.organizations.length>25)throw Error("invalid_organizations");
  const ids=new Set();
  return data.organizations.map(item=>{
    if(!item||!isUuid(item.organizationId)||ids.has(item.organizationId)
      ||!safeText(item.name,140)
      ||!["owner","admin","instructor","learner"].includes(item.role)){
      throw Error("invalid_organizations");
    }
    ids.add(item.organizationId);
    return {id:item.organizationId,name:safeText(item.name,140),role:item.role};
  });
}
export function studySnapshot(courseResponse,enrollmentResponse,progressResponse){
  if(!Array.isArray(courseResponse?.courses)||courseResponse.courses.length>100
    ||!Array.isArray(enrollmentResponse?.enrollments)||enrollmentResponse.enrollments.length>100
    ||!Array.isArray(progressResponse?.progress)||progressResponse.progress.length>200)
    throw Error("invalid_learning_data");
  const courses=new Map();
  for(const c of courseResponse.courses){
    if(!c||!isUuid(c.id)||!safeText(c.title)||!["published","draft","archived"].includes(c.status)
      ||courses.has(c.id))throw Error("invalid_learning_data");
    courses.set(c.id,{title:safeText(c.title),status:c.status});
  }
  const completed=new Map();
  const dedupe=new Set();
  for(const progress of progressResponse.progress){
    if(!progress||!isUuid(progress.courseId)||!safeText(progress.moduleKey,100))throw Error("invalid_learning_data");
    const key=progress.courseId+":"+progress.moduleKey;
    if(!dedupe.has(key)){
      dedupe.add(key);
      completed.set(progress.courseId,(completed.get(progress.courseId)||0)+1);
    }
  }
  const result=[];
  const unique=new Set();
  for(const enrollment of enrollmentResponse.enrollments){
    if(!enrollment||!isUuid(enrollment.courseId)
      ||!["active","completed","revoked"].includes(enrollment.status)
      ||unique.has(enrollment.courseId))throw Error("invalid_learning_data");
    unique.add(enrollment.courseId);
    if(enrollment.status==="revoked")continue;
    const course=courses.get(enrollment.courseId);
    // No courses/versions shown if RLS hides their material.
    if(!course||course.status!=="published")continue;
    result.push({
      id:enrollment.courseId,
      title:course.title,
      enrollmentStatus:enrollment.status,
      modulesCompleted:completed.get(enrollment.courseId)||0,
    });
  }
  return result;
}
