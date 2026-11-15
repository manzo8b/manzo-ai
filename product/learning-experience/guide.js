/* MANZO AI Guided Learning — local-only module self-check.
   Derived from existing course headings. No login, grades, localStorage,
   analytics, cookies, network requests, or changes to existing quizzes. */
(()=>{
 'use strict';
 const root=document.querySelector('[data-ma-learning-guide="v1"]');
 if(!root)return;
 const dictionary=document.getElementById('ma-learning-labels');
 if(!dictionary)return;
 const t=JSON.parse(dictionary.textContent);
 const items=[...root.querySelectorAll('[data-ma-unit]')];
 const buttons=[...root.querySelectorAll('[data-ma-mark]')];
 const counter=root.querySelector('#ma-progress-current');
 const bar=root.querySelector('.ma-progress-track');
 const fill=root.querySelector('#ma-progress-fill');
 const next=root.querySelector('#ma-continue');
 const reset=root.querySelector('#ma-reset');
 const seen=new Set();
 const getAnchor=(index)=>{
   const selector=root.dataset.maGuideKind==='coding'
     ? 'hc-section-'+String(index).padStart(2,'0')
     : 'ma-learn-unit-'+index;
   return '#'+selector;
 };
 function update(){
  const total=items.length,completed=seen.size;
  counter.textContent=String(completed);
  fill.style.width=(completed/total*100).toFixed(1)+'%';
  bar.setAttribute('aria-valuenow',String(completed));
  for(const item of items){
   const number=Number(item.dataset.maUnit);
   const btn=item.querySelector('[data-ma-mark]');
   const active=seen.has(number);
   item.classList.toggle('ma-studied',active);
   btn.setAttribute('aria-pressed',String(active));
   btn.replaceChildren();
   const symbol=document.createElement('span');
   symbol.setAttribute('aria-hidden','true');symbol.textContent=active?'✓':'○';
   btn.append(symbol,document.createTextNode(active?t.done:t.mark));
   const title=item.querySelector('.ma-unit-copy strong')?.textContent||'';
   btn.setAttribute('aria-label',(active?t.unmark:t.mark)+': '+title);
  }
  const firstOpen=items.find(item=>!seen.has(Number(item.dataset.maUnit)));
  if(firstOpen){
   next.href=getAnchor(Number(firstOpen.dataset.maUnit));
   next.firstChild.textContent=t.continue;
   next.classList.remove('ma-all-done');
  }else{
   next.removeAttribute('href');
   next.firstChild.textContent=t.allDone;
   next.classList.add('ma-all-done');
  }
 }
 root.addEventListener('click',event=>{
  const button=event.target.closest('button[data-ma-mark]');
  if(button&&root.contains(button)){
   const i=Number(button.dataset.maMark);
   if(seen.has(i))seen.delete(i);
   else seen.add(i);
   update();
  }
 });
 reset.addEventListener('click',()=>{seen.clear();update()});
 update();
})();
/* Academy discovery — actual archive routes, client-side filter only.
   No search requests, analytics, login, certificates or persistent data. */
(()=>{
 'use strict';
 const root=document.querySelector('[data-ma-pathways="v1"]');
 if(!root)return;
 const cards=[...root.querySelectorAll('[data-ma-course-card]')];
 const filters=[...root.querySelectorAll('[data-ma-filter]')];
 const input=root.querySelector('#ma-course-search');
 const count=root.querySelector('[data-ma-count]');
 const empty=root.querySelector('[data-ma-empty]');
 const clear=root.querySelector('[data-ma-clear]');
 if(!input||!count||cards.length!==6)return;
 let active='all';
 const plain=value=>(value||'').toLocaleLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').trim();
 function update(){
  const query=plain(input.value);
  let visible=0;
  cards.forEach(card=>{
   const matchCategory=active==='all'||card.dataset.maCategory===active;
   const matchText=!query||plain(card.dataset.maSearch).includes(query);
   const show=matchCategory&&matchText;
   card.hidden=!show;
   if(show)visible++;
  });
  filters.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.maFilter===active)));
  count.textContent=String(visible);
  empty.hidden=visible!==0;
 }
 filters.forEach(button=>button.addEventListener('click',()=>{
  active=button.dataset.maFilter;
  update();
 }));
 input.addEventListener('input',update);
 clear.addEventListener('click',()=>{
  input.value='';
  active='all';
  update();
  input.focus();
 });
 update();
})();
