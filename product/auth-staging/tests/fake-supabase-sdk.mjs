/**
 * QA-ONLY fake Supabase Auth adapter used by the *separate* interaction
 * test bundle. Never imported by source/app.js nor by production build.
 * This test double deliberately performs zero network requests.
 */
const user=Object.freeze({
  id:"11111111-1111-4111-8111-111111111111",
  email:"student@example.invalid",
  email_confirmed_at:"2026-11-16T00:00:00Z"
});
export function createClient(){
  let callback=()=>{};
  let signedIn=false;
  return {
    auth:{
      onAuthStateChange(fn){
        callback=fn;
        queueMicrotask(()=>callback("INITIAL_SESSION",null));
        return {data:{subscription:{unsubscribe(){}}}};
      },
      async getUser(){
        if(!signedIn)return {data:{user:null},error:{code:"session_not_found"}};
        return {data:{user},error:null};
      },
      async signInWithPassword({email,password}){
        if(email!=="student@example.invalid"||password!=="demo-password")
          return {data:{},error:{code:"invalid_credentials",status:400}};
        signedIn=true;
        callback("SIGNED_IN",{user});
        return {data:{user},error:null};
      },
      async resetPasswordForEmail(email,options){
        if(!email||!options?.redirectTo)return {data:{},error:{code:"invalid_request",status:400}};
        return {data:{},error:null};
      },
      async updateUser({password}){
        if(!signedIn)return {data:{},error:{code:"session_not_found",status:401}};
        if(password==="bad-password!")return {data:{},error:{code:"weak_password",status:422}};
        if(password!=="safe-password-2026!")return {data:{},error:{code:"same_password",status:422}};
        return {data:{user},error:null};
      },
      async signOut(){
        signedIn=false;
        callback("SIGNED_OUT",null);
        return {error:null};
      }
    }
  };
}
