/* MANZO AI · La stanza dei giurati · Prototipo esperienziale v0.2
   NO API · NO storage · NO simulated model responses · NO analytics.
   Source document, prompts and answer key are HTML, readable without JS.
*/
(()=>{
 'use strict';
 const $=(sel,root=document)=>root.querySelector(sel);
 const $$=(sel,root=document)=>[...root.querySelectorAll(sel)];
 const alertText=text=>{const node=$('#announce');if(node)node.textContent=text};
 if(!$('#source-document'))return;
 const KEY=window.MANZO_EVAL_01;
 if(!KEY||KEY.statements.length!==8)throw Error('Missing original experiment answer map');
 const statements=KEY.statements;
 const byId=new Map(statements.map(s=>[s.id,s]));
 const selected=new Set();
 const runs=[];
 let before=null;
 const responseNames={supported:'Supportata',partial:'In parte',unsupported:'Non supportata'};
 const sources=['Oggetto','Lavori compresi','Importo','Materiali','Tempi','Pagamento','Garanzia','Validità'];
 const reduced=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
 const doc=$('#source-document').textContent;
 const expandPrompt=which=>$('#prompt-'+which.toLowerCase()).textContent.replace('[incolla il documento di prova]',doc);
 async function copyText(value){
  if(navigator.clipboard&&isSecureContext){try{await navigator.clipboard.writeText(value);return true}catch(e){/* local file fallback */}}
  const copy=document.createElement('textarea');copy.value=value;copy.style.position='fixed';copy.style.left='-99999px';document.body.append(copy);copy.select();
  let ok=false;try{ok=document.execCommand('copy')}catch(e){}copy.remove();return ok;
 }
 $$('[data-copy]').forEach(button=>button.addEventListener('click',async()=>{
  const which=button.dataset.copy;
  const ok=await copyText(which==='document'?doc:expandPrompt(which));
  alertText(ok?'Testo copiato. Nessun dato trasmesso a server':'Copia non riuscita: seleziona il testo e copialo manualmente');
  if(ok){const previous=button.textContent;button.textContent='Copiato ✓';setTimeout(()=>button.textContent=previous,1600)}
 }));

 // Part 1: learner's own diagnosis; source answer key is HTML, not an API response.
 const gapInputs=$$('#gap-options input[type="checkbox"]');
 let gapKeyUnlocked=false;
 const unlockGaps=()=>{
  gapKeyUnlocked=true;
  $('#record-gap-locked').hidden=true;
  $('#record-gap-unlocked').hidden=false;
  $$('.gap-id[data-answer-label]').forEach(el=>{el.textContent=el.dataset.answerLabel==='FA'?'Falso allarme':el.dataset.answerLabel});
 };
 const resetGapUnlock=()=>{
  gapKeyUnlocked=false;
  $('#record-gap-locked').hidden=false;
  $('#record-gap-unlocked').hidden=true;
  $$('.gap-id[data-answer-label]').forEach((el,i)=>el.textContent=String(i+1));
  $('#skip-diagnosis').disabled=false;
 };
 $('#skip-diagnosis').addEventListener('click',()=>{
  unlockGaps();alertText('Lista delle lacune sbloccata senza svolgere la prima indagine');
 });

 function updateGapSelections(){
  selected.clear();gapInputs.forEach(input=>{if(input.checked)selected.add(input.value)});
  $('#selection-count').textContent=`${selected.size} ${selected.size===1?'selezione':'selezioni'}`;
 }
 gapInputs.forEach(input=>input.addEventListener('change',updateGapSelections));
 $('#reveal-evaluation').addEventListener('click',()=>{
  const matches=KEY.gaps.filter(id=>selected.has(id)).length;
  const falseAlarms=selected.has(KEY.falseAlarm)?1:0;
  const node=$('#evaluation-feedback');node.replaceChildren();
  const lead=document.createElement('strong');lead.textContent=`Hai individuato ${matches} delle 8 lacune della chiave`;
  const p=document.createElement('p');p.textContent=`Lacune ancora da individuare: ${8-matches}. Falsi allarmi selezionati: ${falseAlarms}. È il confronto della tua lettura con la chiave, non un risultato di un modello AI.`;
  node.append(lead,p);node.hidden=false;$('#answer-key').open=true;unlockGaps();
  node.scrollIntoView({block:'nearest',behavior:reduced()?'instant':'smooth'});
  alertText('Chiave di riferimento aperta, '+matches+' lacune individuate');
 });
 $('#reset-selection').addEventListener('click',()=>{
  gapInputs.forEach(input=>input.checked=false);updateGapSelections();
  $('#evaluation-feedback').hidden=true;$('#answer-key').open=false;
  alertText('Prima diagnosi ripristinata');
 });
 updateGapSelections();

 // Learner must connect actual statements to document sections. No artificial neural links.
 const cards=$$('[data-claim]');
 function readClaim(id){
  const card=$(`[data-claim="${id}"]`);
  const checked=$('input[type="radio"]:checked',card);
  return {status:checked?.value||'',source:checked?.value==='unsupported'?'':($('select',card).value||'')};
 }
 function isComplete(response){return response.status&&(response.status==='unsupported'||Boolean(response.source))}
 function statusCorrect(actual,expected){return Boolean(actual.status===expected.status&&actual.source===expected.source)}
 function refreshClaimStatus(){
  cards.forEach(card=>{
   const answer=readClaim(card.dataset.claim);
   const source=$('.claim-source',card);
   source.hidden=!answer.status||answer.status==='unsupported';
  });
  const current=statements.filter(s=>isComplete(readClaim(s.id))).length;
  $('#claim-progress').textContent=`${current} di 8 affermazioni classificate`;
  drawNetwork();
  if(before)updateReview();
 }
 cards.forEach(card=>{
  $$('input,select',card).forEach(input=>input.addEventListener('change',refreshClaimStatus));
 });
 const ns='http://www.w3.org/2000/svg';
 function SVG(name,attributes={},content=''){
  const el=document.createElementNS(ns,name);
  Object.entries(attributes).forEach(([key,val])=>el.setAttribute(key,String(val)));
  if(content)el.textContent=content;
  return el;
 }
 function drawNetwork(){
  const root=$('#evidence-network');root.replaceChildren();
  // Every one of these nodes is a real target for a question; no decorative connections.
  root.append(SVG('text',{x:50,y:25,class:'net-head'},'LE 8 AFFERMAZIONI'),SVG('text',{x:666,y:25,class:'net-head'},'SEZIONI DEL DOCUMENTO'));
  const positions=new Map(sources.map((source,index)=>[source,63+index*50]));
  sources.forEach((source,index)=>{
   const y=positions.get(source);
   const node=SVG('g',{class:'net-source','data-source':source});
   node.append(SVG('rect',{x:622,y:y-19,width:210,height:38,rx:12}),SVG('text',{x:638,y:y+5},source));
   root.append(node);
  });
  let linked=0,without=0,correct=0;
  statements.forEach((item,index)=>{
   const y=63+index*50;
   const chosen=readClaim(item.id);
   const node=SVG('g',{class:'net-claim', 'data-id':item.id});
   node.append(SVG('rect',{x:25,y:y-19,width:99,height:38,rx:12}),SVG('text',{x:48,y:y+5},item.id));
   root.append(node);
   if(!isComplete(chosen))return;
   const isRight=before&&statusCorrect(chosen,item);
   let edge;
   if(chosen.status==='unsupported'){
    without++;
    edge=SVG('path',{d:`M124 ${y} C280 ${y} 315 ${y} 410 ${y}`,class:`net-connection net-unsupported ${before?(isRight?'net-correct':'net-wrong'):''}`});
    const end=SVG('text',{x:415,y:y+4,class:'net-label'},before?(isRight?'NON SUPPORTATA ✓':'DA RIVEDERE'):'NESSUNA FONTE');
    root.append(edge,end);
   } else {
    linked++;
    const end=positions.get(chosen.source);
    edge=SVG('path',{d:`M124 ${y} C365 ${y} 388 ${end} 622 ${end}`,class:`net-connection ${before?(isRight?'net-correct':'net-wrong'):''}`});
    root.insertBefore(edge,root.firstChild);
   }
   if(isRight)correct++;
  });
  const total=linked+without;
  $('#network-counter').textContent=`${total} / 8 relazioni dichiarate`;
  const info=before?`Dopo il confronto: ${correct} relazioni coerenti con la chiave, ${total-correct} da rivedere. ${without} frasi dichiarate prive di fonte.`:
   `${total} relazioni dichiarate: ${linked} collegate a sezioni, ${without} dichiarate senza fonte. Nessuna relazione generata automaticamente.`;
  $('#network-description').textContent=info;
 }
 function describe(response){return response?.status?`${responseNames[response.status]}${response.source?' · '+response.source:''}`:'Non scelta'}
 function updateReview(){
  if(!before)return;
  let changed=0;
  const body=$('#decision-rows');body.replaceChildren();
  statements.forEach(item=>{
   const previous=before[item.id],current=readClaim(item.id);
   const diff=previous.status!==current.status||previous.source!==current.source;
   if(diff)changed++;
   const tr=document.createElement('tr');
   const id=document.createElement('th');id.scope='row';id.textContent=item.id;
   const t1=document.createElement('td');t1.textContent=describe(previous);
   const t2=document.createElement('td');t2.textContent=describe(current);
   const t3=document.createElement('td');t3.textContent=describe(item);t3.className=statusCorrect(current,item)?'review-accurate':'review-unresolved';
   tr.append(id,t1,t2,t3);body.append(tr);
  });
  $('#changed-count').textContent=changed?`${changed} ${changed===1?'risposta modificata':'risposte modificate'} dopo il confronto`:'Nessuna risposta modificata';
 }
 $('#freeze-claims').addEventListener('click',()=>{
  for(const item of statements){
   const ans=readClaim(item.id);
   if(!isComplete(ans)){
    alertText(`Completa ${item.id}: seleziona una valutazione e, se necessario, la fonte`);
    const card=$(`[data-claim="${item.id}"]`);
    card.scrollIntoView({block:'center',behavior:reduced()?'instant':'smooth'});
    (ans.status&&ans.status!=='unsupported'?$('select',card):$('input[type="radio"]',card)).focus();
    return;
   }
  }
  if(!before){before=Object.fromEntries(statements.map(s=>[s.id,{...readClaim(s.id)}]));}
  $('#summary-key').open=true;
  cards.forEach(card=>{$('[data-claim-explanation]',card).hidden=false});
  $('#decision-review').hidden=false;
  $('#freeze-claims').textContent='Aggiorna il confronto';
  refreshClaimStatus();
  $('#decision-review').scrollIntoView({block:'start',behavior:reduced()?'instant':'smooth'});
  alertText('Giudizio iniziale conservato: ora puoi modificarlo e spiegare che cosa ti ha fatto cambiare idea');
 });
 refreshClaimStatus();

 // Part 2: optional real-model entries; never invent a value or merge distinct models.
 const form=$('#trial-form');
 const normalize=name=>name.trim().replace(/\s+/g,' ').toLocaleLowerCase('it');
 const gapCheck=$$('input[name="found-gap"]',form);
 const gapCounter=$('#record-gap-count');
 const updateRecordCount=()=>{gapCounter.textContent=`${gapCheck.filter(el=>el.checked).length} / 8`};
 gapCheck.forEach(input=>input.addEventListener('change',updateRecordCount));
 form.addEventListener('reset',()=>setTimeout(updateRecordCount,0));
 updateRecordCount();
 $$('[data-step]',form).forEach(button=>button.addEventListener('click',()=>{
  const code=button.dataset.step;const sign=code.startsWith('+')?1:-1;
  const input=$(`[name="${code.slice(1)}"]`,form);
  const current=input.value===''?0:Number(input.value);
  input.value=String(Math.min(99,Math.max(0,current+sign)));
  input.dispatchEvent(new Event('change',{bubbles:true}));
 }));
 const metrics=['inventions','omissions','generalisations','inferences','falseAlarms'];
 const groupRuns=()=>{
  const groups=new Map();
  runs.forEach(run=>{
   if(!groups.has(run.key))groups.set(run.key,{name:run.model,rows:[]});
   groups.get(run.key).rows.push(run);
  });
  return groups;
 };
 const aggregates=(rows,property)=>rows.reduce((sum,row)=>sum+row[property],0);
 function renderRuns(){
  $('#run-progress').textContent=runs.length?`${runs.length} prove osservate · ${groupRuns().size} modelli`:'Nessuna prova registrata';
  const wrapper=$('#models-summary');wrapper.replaceChildren();
  for(const [key,group] of groupRuns()){
   const section=document.createElement('section');section.className='model-summary';
   const h=document.createElement('h4');h.textContent=group.name;
   const versions=[...new Set(group.rows.map(r=>r.version||'Versione non dichiarata'))];
   const meta=document.createElement('p');meta.textContent=`Versioni registrate: ${versions.join(', ')}. Confronta preferibilmente risultati della stessa versione.`;
   const columns=document.createElement('div');columns.className='results-columns';
   for(const prompt of ['A','B']){
    const entries=group.rows.filter(r=>r.prompt===prompt);
    const col=document.createElement('div');col.className='result-column';
    const letter=document.createElement('span');letter.className='result-letter';letter.textContent=`${prompt} / ${prompt==='A'?'GENERICA':'VINCOLATA'}`;
    const avg=document.createElement('strong');avg.textContent=entries.length?`${(aggregates(entries,'gaps')/entries.length).toFixed(1)} / 8`:'—';
    const sub=document.createElement('small');sub.textContent=entries.length?`${entries.length}/5 prove · lacune individuate medie`:'Nessuna prova per questa richiesta';
    const details=document.createElement('p');details.textContent=entries.length?`Lacune segnalate: ${[...new Set(entries.flatMap(r=>r.foundGaps))].sort().join(', ')||'nessuna'} · Invenzioni: ${aggregates(entries,'inventions')} · Omissioni: ${aggregates(entries,'omissions')}`:'Risultati in arrivo';
    col.append(letter,avg,sub,details);columns.append(col);
   }
   const completion=document.createElement('p');completion.className='model-caution';
   completion.textContent=group.rows.length===10&&group.rows.filter(r=>r.prompt==='A').length===5&&group.rows.filter(r=>r.prompt==='B').length===5?
    'Protocollo A/B completo per questo modello: interpreta i risultati manualmente e annota i limiti.':'Protocollo incompleto: nessuna conclusione affidabile sul confronto A/B.';
   section.append(h,meta,columns,completion);wrapper.append(section);
  }
  const history=$('#run-history');history.replaceChildren();
  runs.forEach((r,index)=>{
   const row=document.createElement('div');row.className='run-row';
   const description=document.createElement('div');
   const h=document.createElement('strong');h.textContent=`Prova ${index+1} · ${r.model} · ${r.prompt}`;
   const info=document.createElement('span');info.textContent=`${r.date} · Versione ${r.version||'non dichiarata'} · Lacune ${r.foundGaps.join(', ')||'nessuna'} (${r.gaps}/8) · Inventati ${r.inventions} · Omissioni ${r.omissions} · Generalizzazioni ${r.generalisations} · Inferenze ${r.inferences} · Falsi allarmi ${r.falseAlarms}`;
   description.append(h,document.createElement('br'),info);
   const remove=document.createElement('button');remove.type='button';remove.textContent='Rimuovi';remove.setAttribute('aria-label',`Rimuovi prova ${index+1}`);
   remove.addEventListener('click',()=>{runs.splice(index,1);renderRuns();alertText('Prova rimossa')});
   row.append(description,remove);history.append(row);
  });
  $('#clear-runs').hidden=!runs.length;
 }
 form.addEventListener('submit',event=>{
  event.preventDefault();if(!form.reportValidity())return;
  const fields=new FormData(form);
  const model=String(fields.get('model')||'').trim().replace(/\s+/g,' ');
  const key=normalize(model);
  if(!key)return;
  const prompt=fields.get('prompt');
  const groups=groupRuns();
  if(!groups.has(key)&&groups.size>=3){alertText('Il registro ammette al massimo tre modelli: rimuovi prove di un modello per aggiungerne un altro');return}
  const current=runs.filter(r=>r.key===key&&r.prompt===prompt).length;
  if(current>=5){alertText(`Hai già registrato cinque prove della richiesta ${prompt} per ${model}`);return}
  const run={key,model,version:String(fields.get('version')||'').trim(),date:fields.get('date'),prompt};
  run.foundGaps=gapCheck.filter(el=>el.checked).map(el=>el.value);
  run.gaps=run.foundGaps.length;
  for(const field of metrics){
   const raw=String(fields.get(field)||'');
   if(raw.trim()===''){alertText('Compila tutti i contatori dopo aver verificato la risposta');$(`[name="${field}"]`,form).focus();return}
   const n=Number(raw);if(!Number.isInteger(n)||n<0||n>99){alertText('Inserisci solo conteggi interi da 0 a 99');return}
   run[field]=n;
  }
  runs.push(run);
  renderRuns();
  form.reset();$('[name="model"]',form).value=model;$('[name="version"]',form).value=run.version;$('[name="prompt"]',form).value=prompt;
  updateRecordCount();
  alertText(`Prova reale ${current+1} di cinque per ${model}, richiesta ${prompt} registrata localmente`);
 });
 $('#clear-runs').addEventListener('click',()=>{
  if(!confirm('Eliminare tutte le prove inserite?'))return;
  runs.length=0;renderRuns();alertText('Registro delle prove svuotato');
 });
 renderRuns();
 $('#copy-audit').addEventListener('click',async()=>{
  const chosen=KEY.gaps.filter(id=>selected.has(id));
  const lines=[
   'MANZO AI · LA STANZA DEI GIURATI · SCHEDA DI AUDIT — Prototipo privato',
   'Documento fittizio: PREVENTIVO N. 2026/047',
   `Lacune selezionate nella prima diagnosi: ${chosen.join(', ')||'nessuna'} (${chosen.length}/8)`,
   `Falso allarme selezionato: ${selected.has('FA')?'sì':'no'}`,
   'PARTE 1 · ESEMPIO SCRITTO PER L’ESPERIMENTO (non è una risposta AI)',
   ...statements.map(item=>{
    const now=readClaim(item.id);
    const old=before?.[item.id];
    return `${item.id} | Prima ${old?describe(old):'non registrato'} | Dopo ${describe(now)} | Chiave ${describe(item)}`;
   }),
   'Perché ho cambiato idea: '+($('#change-reason').value.trim()||'[non compilato]'),
   'PARTE 2 · TEST ESTERNI REALI (solo risultati inseriti manualmente)',
   ...(!runs.length?['Nessuna prova esterna registrata']:runs.map((r,i)=>`${i+1}. ${r.model} | v.${r.version||'non dichiarata'} | ${r.date} | ${r.prompt} | lacune: ${r.foundGaps.join(', ')||'nessuna'} | inventati: ${r.inventions} | omissioni: ${r.omissions} | generalizzazioni: ${r.generalisations} | inferenze: ${r.inferences} | falsi allarmi: ${r.falseAlarms}`)),
   'Regola correttiva: '+($('#corrective-rule').value.trim()||'[da scrivere]'),
   'LIMITI: documento e riassunto di esempio fittizi, nessun risultato generato automaticamente; risultati dei test reali registrati dall’utente e non generalizzabili. Non è consulenza legale.'
  ];
  const ok=await copyText(lines.join('\n'));
  alertText(ok?'Scheda di audit copiata':'Copia non riuscita: seleziona manualmente i dati');
 });

 // Guided stepper, but basic source text remains fully readable when JavaScript is off.
 const phases=$$('.learning-step[id]');
 let activePhase=0;
 const setPhase=(index,{scroll=true}={})=>{
  if(index<0||index>=phases.length)return;
  activePhase=index;
  phases.forEach((section,n)=>section.hidden=n!==index);
  $$('.stage-nav-link').forEach(link=>{
   const active=link.hash==='#'+phases[index].id;
   link.classList.toggle('is-current',active);
   if(active)link.setAttribute('aria-current','step');else link.removeAttribute('aria-current');
  });
  $('#stage-meter').textContent=`${String(index+1).padStart(2,'0')} / ${String(phases.length).padStart(2,'0')} · ${$('h2',phases[index]).textContent}`;
  if(scroll){
   phases[index].scrollIntoView({block:'start',behavior:reduced()?'instant':'smooth'});
   const heading=$('h2',phases[index]);heading.setAttribute('tabindex','-1');heading.focus({preventScroll:true});
  }
 };
 const meter=document.createElement('p');meter.className='stage-meter';meter.id='stage-meter';meter.setAttribute('aria-live','polite');$('.method-mini').after(meter);
 phases.forEach((section,i)=>{
  const controls=document.createElement('div');controls.className='flow-step-actions';
  const prev=document.createElement('button');prev.type='button';prev.className='flow-back';prev.dataset.phasePrev='';prev.textContent='← Fase precedente';prev.hidden=i===0;
  prev.addEventListener('click',()=>setPhase(i-1));
  const next=document.createElement('button');next.type='button';next.className='flow-forward';next.dataset.phaseNext='';next.textContent=i===2?'Passa alla prova esterna (facoltativa) →':i===4?'Vai al verdetto →':'Prossima fase →';next.hidden=i===phases.length-1;
  next.addEventListener('click',()=>setPhase(i+1));
  controls.append(prev,next);section.append(controls);
 });
 $$('a[href^="#"]').forEach(link=>{
  const id=link.getAttribute('href').slice(1);
  const idx=phases.findIndex(section=>section.id===id);
  if(idx<0)return;
  link.addEventListener('click',event=>{
   event.preventDefault();setPhase(idx);
   try{history.replaceState(null,'','#'+id)}catch(e){}
  });
 });
 document.body.classList.add('stepper-ready');
 const initial=phases.findIndex(section=>location.hash==='#'+section.id);
 setPhase(initial<0?0:initial,{scroll:false});
 $('#reset-all').addEventListener('click',()=>{
  if(!confirm('Ricominciare da capo? Le selezioni e le prove della visita saranno cancellate'))return;
  before=null;runs.length=0;cards.forEach(card=>{
   $$('input[type=radio]',card).forEach(input=>input.checked=false);
   $('select',card).value='';
   $('[data-claim-explanation]',card).hidden=true;
  });
  gapInputs.forEach(input=>input.checked=false);updateGapSelections();resetGapUnlock();
  $('#evaluation-feedback').hidden=true;$('#answer-key').open=false;
  $('#summary-key').open=false;$('#decision-review').hidden=true;
  $('#change-reason').value='';$('#corrective-rule').value='';
  $('#freeze-claims').textContent='Confronta le prove e scopri la chiave';
  form.reset();renderRuns();refreshClaimStatus();setPhase(0);alertText('Esperimento ripristinato');
 });
})();
