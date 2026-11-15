/* MANZO AI Learning B2B · In-memory interactive DEMO only.
   No network requests, credentials, cookies, storage, accounts or real grading. */
(()=>{
"use strict";
const host=document.querySelector("[data-learning-console]");
if(!host)return;
const t=JSON.parse(document.getElementById("lc-content").textContent);
const $=id=>document.getElementById(id);
const maxSeats=3;
const allCourses=[{id:"hallucinations",total:6,title:t.courses[0]},
                  {id:"coding",total:6,title:t.courses[1]}];
const sample=()=>[
 {id:"u1",name:t.personNames[0],seat:true,enrollments:[{courseId:"hallucinations",done:2,status:"active"},{courseId:"coding",done:0,status:"active"}]},
 {id:"u2",name:t.personNames[1],seat:true,enrollments:[{courseId:"hallucinations",done:1,status:"active"}]},
 {id:"u3",name:t.personNames[2],seat:false,enrollments:[]},
 {id:"u4",name:t.personNames[3],seat:false,enrollments:[]}
];
let members=sample();
let events=[];
let activeTab="admin";
let selectedStudent="u1";
const percent=(done,total)=>Math.round(100*done/total);
const countSeats=()=>members.filter(x=>x.seat).length;
const enrl=(m)=>m.enrollments.filter(x=>x.status==="active");
const allEnrollments=()=>members.flatMap(m=>m.seat?enrl(m).map(e=>({...e,userId:m.id})):[]);
const catalogue=id=>allCourses.find(c=>c.id===id);

function node(tag,cls,text){
 const element=document.createElement(tag);
 if(cls)element.className=cls;
 if(text!==undefined)element.textContent=String(text);
 return element;
}
function tell(message,warning=false){
 const e=$("lc-feedback");
 e.textContent=message;
 e.classList.toggle("warn",warning);
}
function log(event){
 events.unshift(event);
 if(events.length>8)events=events.slice(0,8);
 renderEvents();
}
function renderEvents(){
 const list=$("lc-events");list.replaceChildren();
 if(!events.length){
  const li=node("li","",t.eventsEmpty);list.append(li);return;
 }
 events.forEach(event=>list.append(node("li","",event)));
}
function makeTag(active){
 return node("span","tag"+(active?"":" off"),active?t.seatActive:t.seatMissing);
}
function setMetrics(){
 const used=countSeats();
 const active=allEnrollments();
 const average=active.length?Math.round(active.reduce((sum,e)=>sum+percent(e.done,catalogue(e.courseId).total),0)/active.length):0;
 const metrics=[used+" / "+maxSeats,active.length,allCourses.length,average+"%"];
 for(let i=0;i<4;i++)$("lc-metric-"+i).textContent=metrics[i];
 $("lc-seats-progress").style.width=(used/maxSeats*100)+"%";
 $("lc-seats-progress").setAttribute("aria-valuenow",String(used));
}
function renderAdmin(){
 setMetrics();
 const tbody=$("lc-members");tbody.replaceChildren();
 members.forEach(m=>{
  const tr=node("tr");
  const person=node("td","",m.name);
  const seatCell=node("td");seatCell.append(makeTag(m.seat));
  const courseCell=node("td","",enrl(m).length);
  const done=enrl(m);
  const avg=done.length?Math.round(done.reduce((sum,e)=>sum+percent(e.done,catalogue(e.courseId).total),0)/done.length):0;
  const progress=node("td","",avg+"%");
  const control=node("td");
  const button=node("button","small-btn",m.seat?t.release:t.assign);
  button.type="button";button.dataset.seatMember=m.id;
  if(!m.seat&&countSeats()>=maxSeats){button.disabled=true;button.title=t.noSeat;}
  control.append(button);
  tr.append(person,seatCell,courseCell,progress,control);
  tbody.append(tr);
 });
 $("lc-student-admin").replaceChildren();
 members.forEach(m=>{
  const option=node("option","",m.name);option.value=m.id;$("lc-student-admin").append(option);
 });
 // Keep selection stable on rerenders.
 $("lc-student-admin").value=selectedStudent;
 renderEvents();
}
function renderStudent(){
 const sel=$("lc-student-view");sel.replaceChildren();
 members.forEach(m=>{
  const option=node("option","",m.name);option.value=m.id;sel.append(option);
 });
 sel.value=selectedStudent;
 const current=members.find(x=>x.id===selectedStudent)||members[0];
 const list=$("lc-student-courses");list.replaceChildren();
 $("lc-student-access").textContent=t.noLogin+(current.seat?"":(" · "+t.unlicensed));
 const filtered=enrl(current);
 if(!current.seat||!filtered.length){
  list.append(node("p","notice",current.seat?t.noCourses:t.unlicensed));
  return;
 }
 filtered.forEach(e=>{
  const course=catalogue(e.courseId);
  const card=node("article","course-card");
  card.append(node("h3","",course.title));
  card.append(node("p","course-progress",e.done+" / "+course.total+" "+t.courseModules));
  const meter=node("div","bar");
  meter.setAttribute("role","progressbar");meter.setAttribute("aria-label",course.title);
  meter.setAttribute("aria-valuemin","0");meter.setAttribute("aria-valuemax","100");
  meter.setAttribute("aria-valuenow",String(percent(e.done,course.total)));
  const fill=node("span");fill.style.width=percent(e.done,course.total)+"%";
  meter.append(fill);card.append(meter);
  const btn=node("button","button",e.done>=course.total?t.finished:t.complete);
  btn.type="button";btn.disabled=e.done>=course.total;
  btn.dataset.completeUser=current.id;btn.dataset.completeCourse=course.id;
  card.append(btn);
  list.append(card);
 });
}
function render(){
 renderAdmin();renderStudent();
}
function setTab(tab){
 activeTab=tab;
 const admin=tab==="admin";
 $("lc-admin-view").hidden=!admin;
 $("lc-student-view-panel").hidden=admin;
 $("lc-tab-admin").setAttribute("aria-selected",String(admin));
 $("lc-tab-student").setAttribute("aria-selected",String(!admin));
 $("lc-tab-admin").tabIndex=admin?0:-1;
 $("lc-tab-student").tabIndex=admin?-1:0;
}
$("lc-tab-admin").addEventListener("click",()=>setTab("admin"));
$("lc-tab-student").addEventListener("click",()=>setTab("student"));
$("lc-members").addEventListener("click",e=>{
 const button=e.target.closest("button[data-seat-member]");if(!button)return;
 const m=members.find(item=>item.id===button.dataset.seatMember);if(!m)return;
 if(m.seat){
  m.seat=false;m.enrollments.forEach(en=>{if(en.status==="active")en.status="revoked"});
  const event=t.seatReleased+" "+m.name;log(event);tell(event);
 }else if(countSeats()<maxSeats){
  m.seat=true;const event=t.seatAdded+" "+m.name;log(event);tell(event);
 }else{tell(t.noSeat,true)}
 render();
});
$("lc-student-admin").addEventListener("change",e=>{selectedStudent=e.target.value;renderStudent()});
$("lc-student-view").addEventListener("change",e=>{selectedStudent=e.target.value;renderAdmin();renderStudent()});
$("lc-enroll").addEventListener("click",()=>{
 const id=$("lc-student-admin").value;
 const courseId=$("lc-course-admin").value;
 const m=members.find(item=>item.id===id);if(!m)return;
 if(!m.seat){tell(t.enrollNoSeat,true);return}
 const current=m.enrollments.find(en=>en.courseId===courseId);
 if(current&&current.status==="active"){tell(t.enrollAlready,true);return}
 if(current){current.status="active"}else{m.enrollments.push({courseId,done:0,status:"active"})}
 const event=t.enrolled+" "+m.name+" · "+catalogue(courseId).title;
 log(event);tell(event);render();
});
$("lc-student-courses").addEventListener("click",e=>{
 const button=e.target.closest("button[data-complete-user]");if(!button)return;
 const m=members.find(x=>x.id===button.dataset.completeUser);
 if(!m||!m.seat)return;
 const enrollment=m.enrollments.find(x=>x.courseId===button.dataset.completeCourse);
 const course=catalogue(button.dataset.completeCourse);
 if(!enrollment||enrollment.status!=="active"||enrollment.done>=course.total)return;
 enrollment.done++;
 const event=t.moduleLogged+" "+m.name+" · "+course.title;
 log(event);tell(event);render();
});
$("lc-reset").addEventListener("click",()=>{
 members=sample();events=[];selectedStudent="u1";render();setTab("admin");tell(t.simReset);
});
function init(){
 render();setTab("admin");tell(t.demo);
}
init();
})();