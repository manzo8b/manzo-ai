/* MANZO AI — progressive logo assembly. Navigation never waits for the animation. */
(()=>{'use strict';
 const stage=document.querySelector('body > main');
 if(!stage||!stage.querySelector('h1'))return;
 const heading=stage.querySelector('h1'),logo=stage.querySelector('img');
 if(!logo)return;
 const reduce=matchMedia('(prefers-reduced-motion: reduce)');
 const animations=[];let active=false;
 stage.classList.add('assembly-stage');
 const emblem=document.createElement('div');emblem.className='assembly-emblem';logo.before(emblem);emblem.append(logo);
 const replay=document.createElement('button');replay.className='assembly-replay';replay.type='button';replay.textContent='↻ Replay';replay.setAttribute('aria-label','Ripeti animazione / Replay animation');stage.append(replay);
 function clear(){animations.forEach(a=>a.cancel());animations.length=0;stage.querySelectorAll('.assembly-fragment,.assembly-title-layer,.assembly-ring').forEach(e=>e.remove());logo.style.opacity='';heading.style.color='';stage.dataset.assembly='complete';active=false;replay.disabled=false}
 function run(){
  clear();if(reduce.matches)return;active=true;replay.disabled=true;stage.dataset.assembly='running';
  const ring=document.createElement('div');ring.className='assembly-ring';ring.setAttribute('aria-hidden','true');emblem.append(ring);
  animations.push(ring.animate([{opacity:0,transform:'scale(1.6) rotate(-60deg)'},{opacity:.8,offset:.25},{opacity:0,transform:'scale(.8) rotate(80deg)'}],{duration:1800,easing:'ease-out'}));
  function launch(el,index,total,delay,duration,distance){
   const angle=(index*137.5)*Math.PI/180;const x=Math.cos(angle)*distance,y=Math.sin(angle)*distance*.6;
   const a=el.animate([{opacity:0,transform:`translate3d(${x}px,${y}px,0) rotate(${index%2?150:-150}deg) scale(.3)`},{opacity:1,offset:.16},{opacity:1,transform:'translate3d(0,0,0) rotate(0) scale(1)'}],{duration,delay:delay+(index%5)*42,easing:'cubic-bezier(.22,.72,.12,1)',fill:'both'});animations.push(a);return a;
  }
  logo.style.opacity='0';
  for(let i=0;i<24;i++){
   const piece=document.createElement('span');piece.className='assembly-fragment';piece.setAttribute('aria-hidden','true');piece.style.backgroundImage=`url("${logo.src}")`;
   const c=Math.floor(i/2)%4,r=Math.floor(i/8),x=c*25,y=r*100/3,w=25,h=100/3;
   piece.style.clipPath=i%2?`polygon(${x+w}% ${y}%,${x+w}% ${y+h}%,${x}% ${y+h}%)`:`polygon(${x}% ${y}%,${x+w}% ${y}%,${x}% ${y+h}%)`;
   emblem.append(piece);launch(piece,i,24,80,1300,Math.min(innerWidth*.65,520));
  }
  const layer=document.createElement('span');layer.className='assembly-title-layer';layer.setAttribute('aria-hidden','true');heading.append(layer);
  const title=heading.firstChild.textContent.trim();heading.style.color='transparent';
  for(let i=0;i<12;i++){
   const piece=document.createElement('span');piece.className='assembly-fragment assembly-type';piece.textContent=title;piece.setAttribute('aria-hidden','true');const c=i%6,r=Math.floor(i/6);piece.style.clipPath=`inset(${r*50}% ${100-(c+1)*100/6}% ${50-r*50}% ${c*100/6}%)`;layer.append(piece);launch(piece,i,12,1000,1500,Math.min(innerWidth*.6,460));
  }
  const settle=emblem.animate([{transform:'scale(1)'},{transform:'scale(1.045)'},{transform:'scale(1)'}],{duration:350,delay:1450,easing:'ease-out'});animations.push(settle);
  Promise.allSettled(animations.map(a=>a.finished)).then(()=>{if(active)clear()});
 }
 replay.addEventListener('click',run);reduce.addEventListener('change',()=>{if(reduce.matches)clear();replay.hidden=reduce.matches});replay.hidden=reduce.matches;
 if(typeof emblem.animate==='function')run();
})();
