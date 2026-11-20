"use strict";
/* MANZO AI / magical box — purely presentational progressive enhancement.
 * No timers or network requests; animation is in CSS and can be paused.
 * Never touches the language selector, routing, search, sidebar or footer.
 */
(() => {
  const root=document.querySelector('[data-ma-v2-section="hero"] .ma-v2-magic');
  if(!root)return;
  const pause=root.querySelector('[data-ma-v2-motion-control]');
  if(!pause)return;
  const reduced=window.matchMedia?.('(prefers-reduced-motion: reduce)');
  if(reduced?.matches)return; // CSS displays the meaningful open-box frame.
  pause.hidden=false;
  function update(paused){
    root.classList.toggle('ma-v2-motion-paused',paused);
    pause.setAttribute('aria-pressed',String(paused));
    pause.textContent=paused?pause.dataset.play:pause.dataset.pause;
  }
  pause.addEventListener('click',()=>update(!root.classList.contains('ma-v2-motion-paused')));
  // Pause offscreen animations to avoid unnecessary animation work.
  if('IntersectionObserver' in window){
    const observer=new IntersectionObserver(entries=>{
      if(!entries[0]?.isIntersecting){
        root.dataset.offscreen="1";
      } else {
        delete root.dataset.offscreen;
      }
    },{threshold:0.05});
    observer.observe(root);
  }
  if(reduced?.addEventListener)reduced.addEventListener('change',e=>{
    if(e.matches){pause.hidden=true;root.classList.remove('ma-v2-motion-paused');}
    else{pause.hidden=false;update(false);}
  });
})();
