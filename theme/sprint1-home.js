"use strict";
/* MANZO AI Sprint 1 — progressive disclosure of the existing Academy cards.
 * With JavaScript unavailable, every card remains visible.
 * No analytics, storage, external requests, or changes to language UI.
 */
(() => {
  const showcase=document.querySelector('body[data-ma-surface="landing"] .ma-home-showcase[data-ma-home-showcase="v1"]');
  if(!showcase)return;
  const grid=showcase.querySelector('.ma-home-course-grid');
  const toggle=showcase.querySelector('[data-ma-s1-toggle="v1"]');
  const status=showcase.querySelector('[data-ma-s1-status]');
  if(!grid || !toggle || !status)return;
  const cards=Array.from(grid.children).filter(child=>child.matches('article'));
  const count=cards.length;
  if(count<=4)return;
  const n=4;
  let expanded=false;
  const word=(key,fallback)=>toggle.dataset[key] || fallback;
  const update=()=>{
    cards.forEach((card,i)=>{card.hidden=!expanded && i>=n;});
    toggle.hidden=false;
    toggle.setAttribute('aria-expanded',String(expanded));
    const label=expanded
      ?word('less','Show selection')
      :word('more','Show all')+' '+count+' '+word('unit','courses');
    toggle.textContent=label;
    status.textContent=(expanded?count:n)+' / '+count+' '+(status.dataset.count||'visible');
  };
  toggle.addEventListener('click',()=>{
    expanded=!expanded;
    update();
    if(!expanded)toggle.scrollIntoView({block:'nearest'});
  });
  update();
})();
