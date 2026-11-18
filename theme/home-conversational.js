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
  /(?:lezion|docen|didatt|teach|lesson|aula|clase|profesor)/i,
  /(?:prompt|istruzion|instruction|instrucci)/i,
  /(?:verif|font|fact|claim|source|fuente|allucin|hallucin)/i,
  /(?:sit[oi]|web|design|studio|progett|creat)/i
 ];
 if(search){
  search.addEventListener('input',()=>{
   const q=search.value.trim();
   if(q.length<3)return;
   const index=terms.findIndex(re=>re.test(q));
   if(index>=0&&goals[index]!==active)choose(goals[index],false);
  });
 }
 choose(goals[0],false);
})();
