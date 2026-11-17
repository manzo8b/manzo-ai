"use strict";
/* Original presentation text + accessible controls; no cookies, analytics or persistence */
(function(){
 const $=id=>document.getElementById(id);
 const base=document.body.dataset.slidesBase||"../../it/";
 function make(tag,cls,text){const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=String(text);return e}
 function put(node,...children){for(const c of children)if(c)node.append(c);return node}
 const state={slides:[],index:0};
 const slide=$("atl-present-slide"),next=$("atl-present-next"),prev=$("atl-present-prev"),index=$("atl-present-index"),select=$("atl-present-select");
 function render(){
   const s=state.slides[state.index];if(!s)return;
   slide.replaceChildren();
   slide.className="atl-slide-page atl-slide-page-"+String(state.index+1).padStart(2,"0");
   const originalBase=document.body.dataset.originalSlideBase;
   if(originalBase){
     const image=make("img","atl-original-slide");
     image.src=originalBase+"slide-"+String(state.index+1).padStart(2,"0")+".webp";
     image.alt="Slide originale NotebookLM "+(state.index+1)+": "+s.title;
     image.width=1376;image.height=768;image.decoding="async";
     const wrap=make("figure","atl-original-slide-wrap");
     put(wrap,image,make("figcaption","","Slide originale "+(state.index+1)+" di 15 · Presentazione dell'autore"));
     put(slide,wrap);
     const details=make("details","atl-slide-transcription");
     put(details,make("summary","","Leggi il contenuto in formato accessibile"));
     const prose=make("div","atl-slide-reading");
     put(prose,make("h2","",s.title),make("p","",s.lead));
     const points=make("ul");
     for(const item of s.points)put(points,make("li","",item));
     put(prose,points,make("p","atl-slide-remember",s.takeaway));
     put(details,prose);put(slide,details);
   }else{
     // No artwork has been uploaded to the repo. Don't misrepresent this text
     // adaptation as the authentic NotebookLM presentation.
     put(slide,make("p","atl-slide-fallback-notice",
       "Questa è una trasposizione testuale: il PDF originale non è ancora stato caricato nella piattaforma."),
       make("span","atl-slide-kicker",s.eyebrow),
       make("h2","",s.title),
       make("p","atl-slide-lead",s.lead));
     const points=make("ul","atl-slide-points");
     for(const entry of s.points)put(points,make("li","",entry));
     put(slide,points);
     const takeaway=make("div","atl-slide-takeaway");
     put(takeaway,make("span","","DA RICORDARE"),make("p","",s.takeaway));
     put(slide,takeaway);
   }
   $("atl-present-counter").textContent=String(state.index+1).padStart(2,"0")+" / "+String(state.slides.length).padStart(2,"0");
   $("atl-present-progress").style.width=((state.index+1)/state.slides.length*100)+"%";
   select.value=String(state.index);
   [...index.querySelectorAll("button")].forEach((b,i)=>b.setAttribute("aria-current",String(i===state.index)));
   prev.disabled=state.index===0;
   next.disabled=state.index===state.slides.length-1;
   history.replaceState(null,"","#slide-"+String(state.index+1).padStart(2,"0"));
 }
 function goto(i){if(i<0||i>=state.slides.length)return;state.index=i;render();}
 function init(data){
   if(!data||data.slides.length!==15)throw new Error("Presentazione incompleta");
   state.slides=data.slides;select.replaceChildren();index.replaceChildren();
   data.slides.forEach((s,i)=>{
     const opt=make("option","",(i+1)+". "+s.title);opt.value=String(i);put(select,opt);
     const b=make("button","atl-present-index-button",String(i+1).padStart(2,"0")+" · "+s.title);
     b.type="button";b.addEventListener("click",()=>goto(i));put(index,b);
   });
   const match=window.location.hash.match(/^#slide-(\d{2})$/);
   state.index=match?Math.max(0,Math.min(14,Number(match[1])-1)):0;
   render();
 }
 next.addEventListener("click",()=>goto(state.index+1));
 prev.addEventListener("click",()=>goto(state.index-1));
 select.addEventListener("change",()=>goto(Number(select.value)));
 document.addEventListener("keydown",e=>{
   if(e.altKey||e.ctrlKey||e.metaKey||["INPUT","TEXTAREA","SELECT"].includes(document.activeElement.tagName))return;
   if(e.key==="ArrowLeft"){e.preventDefault();goto(state.index-1)}
   if(e.key==="ArrowRight"){e.preventDefault();goto(state.index+1)}
 });
 fetch(base+"presentation.json").then(r=>{if(!r.ok)throw new Error("HTTP "+r.status);return r.json()}).then(init).catch(error=>{
   slide.replaceChildren(make("p","atl-slide-load-error","Impossibile caricare la versione web: "+error.message));
 });
})();
