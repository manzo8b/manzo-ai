/**
 * MANZO AI Learning B2B — provider-neutral, tested HTTP request policy.
 * Actor MUST be a verified Supabase Auth user ID supplied by a trusted adapter.
 * No direct client access, public tokens, licenses, scores or JWT decoding.
 * This pure module deliberately does not initiate DB connections.
 */
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const MODULE = /^[A-Za-z0-9_.-]{1,100}$/;
const ASSESSMENT = /^[A-Za-z0-9_.:-]{1,160}$/;
const ROUTE = /^\/v1\/organizations\/([^/]+)\/learning\/(courses|enrollments|progress|seats|attempts)(?:\/([^/]+))?$/;

const result = (status, data) => ({ status, body: data });
const issue = (status, code) => result(status, { code, status });
function assertBody(body, keys, required=keys) {
  if (!body || typeof body !== "object" || Array.isArray(body)) return false;
  const present = Object.keys(body);
  return present.length <= keys.length
    && present.every(k => keys.includes(k))
    && required.every(k => Object.prototype.hasOwnProperty.call(body, k));
}
function isId(s) { return typeof s === "string" && UUID.test(s); }
const safeError = (error) => {
  // Never expose SQL messages, keys, schema names, or error stack to the user.
  const msg=String(error?.message || "");
  if (msg === "LEARNING_NO_SEATS") return issue(409, "seat_limit_reached");
  if (msg === "LEARNING_LICENSE_INACTIVE" || msg === "LEARNING_LICENSE_MISSING")
    return issue(403, "license_not_active");
  if (msg === "LEARNING_NOT_ADMIN" || msg === "LEARNING_NOT_INSTRUCTOR")
    return issue(403, "not_authorized");
  if (msg === "LEARNING_STUDENT_NOT_MEMBER" || msg === "LEARNING_STUDENT_UNLICENSED")
    return issue(403, "member_not_eligible");
  if (msg === "LEARNING_COURSE_UNAVAILABLE" || msg === "LEARNING_MODULE_UNAVAILABLE")
    return issue(404, "learning_resource_not_available");
  if (msg === "LEARNING_INVALID_ANSWERS") return issue(422,"invalid_assessment_answers");
  if (msg === "LEARNING_NOT_ENROLLED") return issue(403,"enrollment_required");
  return issue(500,"internal_error");
};
function checkAnswers(answers) {
  if (!answers || typeof answers !== "object" || Array.isArray(answers)) return false;
  const values=Object.entries(answers);
  if (values.length < 1 || values.length > 40) return false;
  return values.every(([key,value])=>
    ASSESSMENT.test(key) && typeof value === "string" && value.length >= 1 && value.length <= 80
  );
}
export const MAX_BODY_BYTES = 8192;
export const ENDPOINTS = Object.freeze([
  "GET /v1/organizations/{organizationId}/learning/courses",
  "GET /v1/organizations/{organizationId}/learning/progress",
  "POST /v1/organizations/{organizationId}/learning/seats",
  "DELETE /v1/organizations/{organizationId}/learning/seats/{memberId}",
  "POST /v1/organizations/{organizationId}/learning/enrollments",
  "POST /v1/organizations/{organizationId}/learning/progress",
  "POST /v1/organizations/{organizationId}/learning/attempts"
]);

/**
 * @param {{method:string,path:string,body?:unknown,actor:string,data:object}} args
 * @returns {Promise<{status:number,body:object}>}
 */
export async function dispatchLearning({method,path,body,actor,data}) {
  if (!isId(actor)) return issue(401,"authentication_required");
  if (!data || typeof data !== "object") return issue(503,"service_not_configured");
  const match = ROUTE.exec(path);
  if (!match) return issue(404,"not_found");
  const [,organizationId,operation,memberId]=match;
  if (!isId(organizationId)) return issue(404,"not_found");
  if (memberId !== undefined && (!isId(memberId)||operation!=="seats"))
    return issue(404,"not_found");
  try {
    if (operation === "courses" && method === "GET" && !memberId)
      return result(200,{ courses: await data.listCourses({actor,organizationId}) });
    if (operation === "progress" && method === "GET" && !memberId)
      return result(200,{ progress: await data.listProgress({actor,organizationId}) });
    if (operation === "seats" && method === "POST" && !memberId) {
      if (!assertBody(body,["memberUserId"]) || !isId(body.memberUserId))
        return issue(422,"invalid_seat_request");
      const state=await data.assignSeat({actor,organizationId,memberUserId:body.memberUserId});
      return result(200,{result:state,memberUserId:body.memberUserId});
    }
    if (operation === "seats" && method === "DELETE" && memberId) {
      const state=await data.releaseSeat({actor,organizationId,memberUserId:memberId});
      return result(200,{result:state,memberUserId:memberId});
    }
    if (operation === "enrollments" && method === "POST" && !memberId) {
      if (!assertBody(body,["memberUserId","courseId"])
        || !isId(body.memberUserId) || !isId(body.courseId))
        return issue(422,"invalid_enrollment_request");
      const enrollmentId=await data.enroll({actor,organizationId,memberUserId:body.memberUserId,courseId:body.courseId});
      return result(200,{enrollmentId,state:"active"});
    }
    if (operation === "progress" && method === "POST" && !memberId) {
      if (!assertBody(body,["courseId","versionId","moduleKey"])
        || !isId(body.courseId) || !isId(body.versionId)
        || typeof body.moduleKey !== "string" || !MODULE.test(body.moduleKey))
        return issue(422,"invalid_progress_request");
      const progressId=await data.completeModule({actor,organizationId,...body});
      return result(200,{progressId,moduleKey:body.moduleKey,state:"completed"});
    }
    if (operation === "attempts" && method === "POST" && !memberId) {
      if (!assertBody(body,["courseId","versionId","assessmentId","answers"])
        || !isId(body.courseId) || !isId(body.versionId)
        || typeof body.assessmentId !== "string" || !ASSESSMENT.test(body.assessmentId)
        || !checkAnswers(body.answers))
        return issue(422,"invalid_assessment_request");
      const attemptId=await data.gradeAssessment({actor,organizationId,...body});
      return result(200,{attemptId,state:"recorded"});
    }
    return issue(405,"method_not_allowed");
  } catch(error) {
    return safeError(error);
  }
}
