/* MANZO AI Precision & Motion. Interaction enhancement only.
   No tracking, storage, network, gesture hijacking or changes to teaching logic. */
(()=>{
'use strict';
const body=document.body;
if(!body||!body.hasAttribute('data-ma-surface'))return;
const kind=body.getAttribute('data-ma-surface');
const reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* Reading progress is informative, not interactive or a replacement for links. */
if(kind==='learning'||kind==='research'){
  const progress=document.createElement('div');
  progress.className='ma-reading-meter';
  progress.setAttribute('aria-hidden','true');
  body.append(progress);
  let scheduled=false;
  function updateReading(){
    scheduled=false;
    const root=document.documentElement;
    const max=Math.max(1,root.scrollHeight-window.innerHeight);
    const pct=Math.min(100,Math.max(0,(window.scrollY/max)*100));
    progress.style.width=pct.toFixed(2)+'%';
  }
  function requestUpdate(){
    if(scheduled)return;
    scheduled=true;
    window.requestAnimationFrame(updateReading);
  }
  window.addEventListener('scroll',requestUpdate,{passive:true});
  window.addEventListener('resize',requestUpdate,{passive:true});
  updateReading();
}

/* Each element is visible in plain HTML; a short progressive treatment is
   added only when supported and when the visitor allows motion. Never apply
   to quizzes, form controls, active tabs, crosswords, editable areas, or data. */
if(reduce||!('IntersectionObserver' in window))return;
const selector={
  landing:'.home-hero, .grid-3>.feature, .activity-strip, [data-manzo-product-preview]',
  portal:'.home-hero, .grid-3>.feature',
  learning:'.page-intro, .module-card',
  research:'.page-intro',
  product:'.product-card, .section-head',
  console:'.panel-heading, .metric',
  general:'.page-intro, .module-card'
}[kind]||'.page-intro';

const nodes=Array.from(document.querySelectorAll(selector))
  .filter(el=>!el.closest('form,dialog,details,[role=tablist],.cross-scroll'))
  .slice(0,30);
if(!nodes.length)return;
nodes.forEach((el,i)=>{
  el.classList.add('ma-reveal');
  el.style.setProperty('--ma-order',String(i%3));
});
const observer=new IntersectionObserver((entries)=>{
  for(const entry of entries){
    if(!entry.isIntersecting)continue;
    entry.target.classList.add('ma-inview');
    observer.unobserve(entry.target);
  }
},{rootMargin:'0px 0px 45px 0px',threshold:.045});
nodes.forEach(node=>observer.observe(node));
body.classList.add('ma-motion-ready');
/* A robust escape hatch: no stale hidden content after viewport changes,
   tab updates, a browser in a restricted state or third-party interference. */
window.setTimeout(()=>{
  for(const node of nodes)node.classList.add('ma-inview');
  observer.disconnect();
},1800);
})();