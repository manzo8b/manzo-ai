/* MANZO AI · learning interactions · offline, zero analytics, no data transfer */
(()=>{'use strict';
const root=document.querySelector('[data-hx-course]');if(!root)return;
const labels=JSON.parse(document.getElementById('hx-ui-labels').textContent);
const exerciseCards=[...document.querySelectorAll('.hx-case')];
let examined=0;
exerciseCards.forEach(card=>{
 const note=card.querySelector('textarea'),button=card.querySelector('.hx-reveal'),feedback=card.querySelector('.hx-case-feedback'),status=card.querySelector('.hx-case-status');
 const update=()=>{button.disabled=note.value.trim().length<20;status.textContent=button.disabled?labels.exInput:labels.exReady};
 note.addEventListener('input',update);update();
 button.addEventListener('click',()=>{
   if(button.disabled)return;
   feedback.hidden=!feedback.hidden;
   button.textContent=feedback.hidden?labels.compare:labels.hide;
   if(!feedback.hidden&&!card.dataset.reviewed){card.dataset.reviewed='1';examined++;const out=document.getElementById('hx-case-progress');if(out)out.textContent=examined+' / '+exerciseCards.length;}
 });
});
const questions=JSON.parse(document.getElementById('hx-quiz-data').textContent);
const qhost=document.getElementById('hx-question'),progress=document.getElementById('hx-quiz-bar'),position=document.getElementById('hx-quiz-position');
const next=document.getElementById('hx-quiz-next'),check=document.getElementById('hx-quiz-check'),qfeedback=document.getElementById('hx-quiz-feedback'),qresult=document.getElementById('hx-quiz-result');
let at=0,score=0,reviewed=false,history=[];
function renderQuestion(){
 reviewed=false;
 if(at>=questions.length){qhost.hidden=true;check.hidden=true;next.hidden=true;qfeedback.hidden=true;qresult.hidden=false;const total=questions.length;const percent=Math.round(score/total*100);qresult.innerHTML='<strong>'+labels.score+': '+score+' / '+total+' ('+percent+'%)</strong><p>'+labels.quizEnd+'</p><button type="button" class="hx-btn hx-btn-primary" id="hx-quiz-restart">'+labels.restart+'</button>';document.getElementById('hx-quiz-restart').addEventListener('click',()=>{at=0;score=0;history=[];qresult.hidden=true;qhost.hidden=false;renderQuestion()});return;}
 const q=questions[at];position.textContent=(at+1)+' / '+questions.length;progress.style.width=(at/questions.length*100)+'%';
 const multi=q.correct.length>1; qhost.innerHTML='';
 const heading=document.createElement('h3');heading.className='hx-q-heading';heading.textContent=q.prompt;qhost.append(heading);
 const opts=document.createElement('div');opts.className='hx-q-options';
 q.options.forEach((value,i)=>{const label=document.createElement('label');label.className='hx-q-option';
 const input=document.createElement('input');input.type=multi?'checkbox':'radio';input.name='hx-answer';input.value=String(i);
 const span=document.createElement('span');span.textContent=value;label.append(input,span);opts.append(label)});
 qhost.append(opts);qfeedback.hidden=true;qfeedback.textContent='';check.hidden=false;check.disabled=false;next.hidden=true;
}
check.addEventListener('click',()=>{
 const q=questions[at];const selected=[...qhost.querySelectorAll('input:checked')].map(el=>Number(el.value)).sort();
 if(!selected.length){qfeedback.textContent=labels.select; qfeedback.hidden=false;return}
 const correct=[...q.correct].sort();const yes=selected.length===correct.length&&selected.every((v,i)=>v===correct[i]);if(yes)score++;
 history.push({question:q.prompt,correct:yes});reviewed=true;
 qhost.querySelectorAll('input').forEach(el=>el.disabled=true);
 qfeedback.replaceChildren();
 const strong=document.createElement('strong');strong.textContent=(yes?labels.correct:labels.incorrect)+' — '+q.explain;
 qfeedback.append(strong);qfeedback.hidden=false;check.hidden=true;next.hidden=false;next.textContent=at===questions.length-1?labels.finish:labels.next;
});
next.addEventListener('click',()=>{if(!reviewed)return;at++;renderQuestion()});
renderQuestion();
const grid=document.getElementById('hx-cross-grid'),crossFeedback=document.getElementById('hx-cross-status');
const placements=[
 {id:1,word:'PROVENIENZA',r:0,c:5,dir:'h'},
 {id:2,word:'VERIFICABILITA',r:0,c:8,dir:'v'},
 {id:3,word:'RISCHIO',r:2,c:8,dir:'h'},
 {id:4,word:'FONTE',r:4,c:8,dir:'h'},
 {id:5,word:'TRACCIABILITA',r:6,c:5,dir:'h'},
 {id:6,word:'PROBATORIO',r:8,c:5,dir:'h'},
 {id:7,word:'CONTROLLO',r:10,c:2,dir:'h'},
 {id:8,word:'CONTESTO',r:12,c:5,dir:'h'}
];
const answer=new Map(),ids=new Map();
placements.forEach(p=>[...p.word].forEach((letter,i)=>{
 const r=p.r+(p.dir==='v'?i:0),c=p.c+(p.dir==='h'?i:0),key=r+':'+c;
 if(answer.has(key)&&answer.get(key)!==letter)throw Error('Crossword mismatch at '+key);
 answer.set(key,letter);
 if(i===0&&!ids.has(key))ids.set(key,p.id);
}));
let direction='h';const cells=new Map();
for(let r=0;r<14;r++){for(let c=0;c<18;c++){const key=r+':'+c,el=document.createElement('div');el.className='hx-cell';
 if(!answer.has(key)){el.classList.add('hx-void');el.setAttribute('aria-hidden','true');grid.append(el);continue}
 if(ids.has(key)){const n=document.createElement('span');n.className='hx-cell-number';n.textContent=ids.get(key);el.append(n)}
 const inp=document.createElement('input');inp.type='text';inp.maxLength=1;inp.autocomplete='off';inp.spellcheck=false;inp.setAttribute('aria-label',labels.cell+' '+(r+1)+', '+(c+1));inp.dataset.r=r;inp.dataset.c=c;
 inp.addEventListener('focus',()=>{const h=placements.some(p=>p.dir==='h'&&r===p.r&&c>=p.c&&c<p.c+p.word.length),v=placements.some(p=>p.dir==='v'&&c===p.c&&r>=p.r&&r<p.r+p.word.length);if(!h&&v)direction='v'});
 inp.addEventListener('input',()=>{inp.value=inp.value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-zA-Z]/g,'').toUpperCase().slice(-1);el.classList.remove('hx-wrong','hx-right');if(inp.value)move(r,c,direction==='h'?0:1,direction==='h'?1:0)});
 inp.addEventListener('keydown',ev=>{const moves={ArrowRight:[0,1,'h'],ArrowLeft:[0,-1,'h'],ArrowDown:[1,0,'v'],ArrowUp:[-1,0,'v']};if(moves[ev.key]){ev.preventDefault();const [dr,dc,dir]=moves[ev.key];direction=dir;move(r,c,dr,dc);return}if(ev.key==='Backspace'&&!inp.value){move(r,c,direction==='h'?0:-1,direction==='h'?-1:0)}});
 el.append(inp);cells.set(key,{el,inp});grid.append(el);
}}
function move(r,c,dr,dc){let nr=r+dr,nc=c+dc;while(nr>=0&&nr<14&&nc>=0&&nc<18){const target=cells.get(nr+':'+nc);if(target){target.inp.focus();break}nr+=dr;nc+=dc}}
document.getElementById('hx-cross-check').addEventListener('click',()=>{let right=0,filled=0;answer.forEach((letter,key)=>{const {el,inp}=cells.get(key);const value=inp.value.toUpperCase();if(value)filled++;const pass=value===letter;if(pass)right++;el.classList.toggle('hx-right',pass);el.classList.toggle('hx-wrong',Boolean(value)&&!pass)});crossFeedback.textContent=right===answer.size?labels.crossSuccess:labels.crossResult.replace('{correct}',right).replace('{total}',answer.size).replace('{filled}',filled)});
document.getElementById('hx-cross-reset').addEventListener('click',()=>{cells.forEach(({el,inp})=>{inp.value='';el.classList.remove('hx-right','hx-wrong')});crossFeedback.textContent=labels.crossReset});
})();