/* Test-only Supabase Auth dependency for isolated My Learning browser smoke.
   NEVER import into production source, deploy or bundle.
*/
const user=Object.freeze({
 id:"11111111-1111-4111-8111-111111111111",
 email:"workspace-qa@example.invalid",
 email_confirmed_at:"2026-11-16T00:00:00Z",
});
export function createClient(){
 return {auth:{
  async getUser(){return {data:{user},error:null}},
  async getSession(){return {data:{session:{user,access_token:"test-jwt-isolated-only"}},error:null}},
  async signOut(){return {error:null}}
 }};
}
