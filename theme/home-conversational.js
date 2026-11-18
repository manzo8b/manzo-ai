/* MANZO AI · Conversational Learning Gateway v1
 * Guided goal discovery only; never simulates an AI chat or writes to storage.
 * Searchbox belongs to existing site search: this controller does not intercept submit.
 */
(()=>{
 "use strict";
 const root=document.querySelector('[data-ma-home-discovery="v1"]');
 if(!root)return;
 const goals=[...root.querySelectorAll('[data-ma-intent]')];
 const title=root.querySelector('[data-ma-discovery-title]');
 const summary=root.querySelector('[data-ma-discovery-summary]');
 const action=root.querySelector('[data-ma-discovery-action]');
 const announce=root.querySelector('[data-ma-discovery-live]');
 if(!title||!summary||!action||goals.length!==4)return;
 let active=null;
 function choose(choice,notify=true){
  if(!choice)return;
  active=choice;
  goals.forEach(g=>g.setAttribute('aria-current',String(g===choice)));
  title.textContent=choice.dataset.maTitle||choice.textContent.trim();
  summary.textContent=choice.dataset.maDescription||"";
  action.textContent=choice.dataset.maAction||"";
  action.href=choice.getAttribute('href');
  if(notify&&announce)announce.textContent=title.textContent+" — "+summary.textContent;
 }
 goals.forEach(goal=>goal.addEventListener('click',e=>{
  // Selecting a suggestion updates the recommended path; the separate action opens it.
  if(e.metaKey||e.ctrlKey||e.shiftKey||e.altKey||e.button!==0)return;
  e.preventDefault();choose(goal);action.focus({preventScroll:true});
 }));
 const search=document.querySelector('.home-hero .searchbox input');
 const terms=[
  /(?:che cos|cosa (?:è|e) l|capir|imparar|fondament|basi|begin|basic|fundament|entender|comprend)/i,
  /(?:prompt|istruzion|instrucci|instruction|redact)/i,
  /(?:allucin|hallucin|alucin|fals|fak|invent|verif|fact|fuente|source|font)/i,
  /(?:crea|progett|codic|coding|code|web|design|build|crear|desarroll)/i
 ];
 if(search){
  search.addEventListener('input',()=>{
   const q=search.value.trim();
   if(q.length<3)return;
   const index=terms.findIndex(re=>re.test(q));
   if(index>=0&&goals[index]!==active)choose(goals[index],false);
  });
 }

 // Legacy sidebar groups 14+ mixed audiences and contained repeated destinations.
 // Curated links are produced from verified, published course routes by the publisher.
 const curated=root.querySelector('[data-ma-home-primary-nav="v2"]');
 const rail=document.querySelector(".rail");
 if(curated&&rail){
  const bottom=rail.querySelector(".rail-bottom");
  rail.querySelectorAll(".nav-title,.nav-link").forEach(el=>el.remove());
  if(bottom)rail.insertBefore(curated,bottom);
  else rail.append(curated);
  rail.classList.add("ma-home-rail-curated");
 }
 // Old hero shortcuts mixed unrelated labels and sent distinct intents
 // to the same lesson. Remove the duplicated shortcuts, not the search.
 const hero=root.closest(".home-hero");
 if(hero){
  const redundant=new Set([
   "studio","lavoro","vita quotidiana","aula del docente","prompt mastery",
   "work","everyday life","teacher classroom","trabajo","vida cotidiana","aula del docente"
  ]);
  hero.querySelectorAll("a,button").forEach(el=>{
   if(el.closest(".ma-discovery")||el.closest(".searchbox"))return;
   const label=(el.textContent||"").replace(/^[^\p{L}\p{N}]+/gu,"").trim().replace(/\s*[↗→]+\s*$/u,"").replace(/\s+/g," ").toLocaleLowerCase();
   if(!redundant.has(label))return;
   const parent=el.parentElement;
   el.remove();
   if(parent&&parent!==hero&&parent.childElementCount===0&&!parent.textContent.trim()){
    parent.remove();
   }
  });
 }

 choose(goals[0],false);
})();
