/* MANZO AI · Engineering Assurance. Self-contained training UI. No external requests. */
(()=>{"use strict";
const root=document.querySelector('[data-hc-module]');if(!root)return;
const labels=JSON.parse(document.getElementById('hc-labels').textContent);
const cases=[...root.querySelectorAll('[data-hc-case]')];
cases.forEach(card=>{
  const input=card.querySelector('textarea'),button=card.querySelector('[data-hc-review]'),
        answer=card.querySelector('[data-hc-solution]'),help=card.querySelector('[data-hc-help]');
  const refresh=()=>{button.disabled=input.value.trim().length<30;help.textContent=button.disabled?labels.min:labels.ready};
  input.addEventListener('input',refresh);refresh();
  button.addEventListener('click',()=>{if(button.disabled)return;
    answer.hidden=!answer.hidden;button.textContent=answer.hidden?labels.reveal:labels.hide;
  });
});
const gateChecks=[...root.querySelectorAll('[data-hc-gate]')];
const gateStatus=root.querySelector('[data-hc-gate-status]');
function refreshGate(){const n=gateChecks.filter(c=>c.checked).length;gateStatus.textContent=n+' / '+gateChecks.length+' · '+labels.gateReminder}
gateChecks.forEach(el=>el.addEventListener('change',refreshGate));refreshGate();
const data=JSON.parse(document.getElementById('hc-quiz-data').textContent),
      host=root.querySelector('[data-hc-question]'),bar=root.querySelector('[data-hc-bar]'),
      pos=root.querySelector('[data-hc-position]'),submit=root.querySelector('[data-hc-submit]'),
      next=root.querySelector('[data-hc-next]'),feedback=root.querySelector('[data-hc-feedback]'),
      result=root.querySelector('[data-hc-result]');
let index=0,points=0,locked=false;
function render(){
  if(index===data.length){
    host.hidden=true;submit.hidden=true;next.hidden=true;feedback.hidden=true;result.hidden=false;
    result.replaceChildren();
    const title=document.createElement('h3');title.textContent=labels.results+': '+points+' / '+data.length;
    const p=document.createElement('p');p.textContent=labels.completed;
    const restart=document.createElement('button');restart.type='button';restart.className='hx-btn hx-btn-primary';restart.textContent=labels.restart;
    restart.addEventListener('click',()=>{index=0;points=0;host.hidden=false;result.hidden=true;render()});
    result.append(title,p,restart);bar.style.width='100%';return;
  }
  locked=false;feedback.hidden=true;submit.hidden=false;submit.disabled=false;next.hidden=true;
  const q=data[index];pos.textContent=(index+1)+' / '+data.length;bar.style.width=(index/data.length*100)+'%';
  host.replaceChildren();
  const h=document.createElement('h3');h.className='hc-quiz-title';h.textContent=q.question;
  const opts=document.createElement('div');opts.className='hc-quiz-options';
  q.options.forEach((label,i)=>{
    const row=document.createElement('label'),input=document.createElement('input'),span=document.createElement('span');
    input.type='radio';input.name='hc-answer';input.value=String(i);span.textContent=label;row.append(input,span);opts.append(row);
  });
  host.append(h,opts);
}
submit.addEventListener('click',()=>{
  if(locked)return;
  const el=host.querySelector('input:checked');if(!el){feedback.textContent=labels.choose;feedback.hidden=false;return}
  const q=data[index],right=Number(el.value)===q.answer;
  if(right)points++;locked=true;host.querySelectorAll('input').forEach(x=>x.disabled=true);
  feedback.textContent=(right?labels.correct:labels.wrong)+' — '+q.why;
  feedback.hidden=false;submit.hidden=true;next.hidden=false;next.textContent=index===data.length-1?labels.results:labels.next;
});
next.addEventListener('click',()=>{if(locked){index++;render()}});
render();
})();