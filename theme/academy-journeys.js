/* MANZO AI — guided learning choices.
   No tracking, cookies, storage, accounts or network requests.
   With JS disabled all three routes remain visible and navigable.
*/
(()=>{
 "use strict";
 const sections=[...document.querySelectorAll('[data-ma-journeys="v1"]')];
 for(const section of sections){
  const choices=[...section.querySelectorAll('[data-ma-journey-choice]')];
  const panels=[...section.querySelectorAll('[data-ma-journey-panel]')];
  if(choices.length!==3 || panels.length!==3)return;
  function select(index,focus=false){
   choices.forEach((button,i)=>{
    button.setAttribute("aria-pressed",String(i===index));
    if(focus&&i===index)button.focus();
   });
   panels.forEach((panel,i)=>{panel.hidden=i!==index});
   section.dataset.ready="1";
  }
  choices.forEach((button,index)=>{
   button.addEventListener("click",()=>select(index));
   button.addEventListener("keydown",event=>{
    if(!["ArrowRight","ArrowLeft","Home","End"].includes(event.key))return;
    event.preventDefault();
    const next=event.key==="Home"?0:event.key==="End"?choices.length-1:
      (index+(event.key==="ArrowRight"?1:-1)+choices.length)%choices.length;
    select(next,true);
   });
  });
  const print=section.querySelector("[data-ma-journey-print]");
  if(print)print.addEventListener("click",()=>{
   document.body.classList.add("ma-print-journey-mode");
   window.print();
  });
  window.addEventListener("afterprint",()=>document.body.classList.remove("ma-print-journey-mode"));
  select(0);
 }
})();
