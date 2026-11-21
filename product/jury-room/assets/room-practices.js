/* MANZO AI v0.5 — Officina locale / Sala dei confini.
   Only deterministic arithmetic and manual learner entries. No AI, network, persistence, analytics. */
(() => {
 'use strict';
 const room=document.body.dataset.room;
 const $=(sel,root=document)=>root.querySelector(sel);
 const $$=(sel,root=document)=>Array.from(root.querySelectorAll(sel));
 const write=(tag,value)=>{const el=document.createElement(tag);el.textContent=value;return el;};
 const label=(map,key)=>map[key]||'Non compilato';
 const announce=message=>{const status=$('#announce');if(status)status.textContent=message;};
 async function copyText(text){
  if(!text.trim())return announce('Non ci sono dati da copiare');
  if(navigator.clipboard&&window.isSecureContext){try{await navigator.clipboard.writeText(text);announce('Testo copiato; nessun dato inviato al sito');return;}catch{}}
  const el=write('textarea',text);el.style.position='fixed';el.style.left='-9999px';document.body.append(el);el.select();
  let ok=false;try{ok=document.execCommand('copy');}catch{}el.remove();
  announce(ok?'Testo copiato; nessun dato inviato al sito':'Copia non disponibile: seleziona manualmente il testo');
 }
 if(room==='officina'){
  const expected={C1:'regole',C2:'regole',C3:'regole',C4:'linguaggio',C5:'linguaggio',C6:'linguaggio',C7:'persona',C8:'persona'};
  const types={regole:'Regole fisse',linguaggio:'Modello linguistico',persona:'Persona'};
  const tasks=$$('tr[data-task]');
  const current=()=>tasks.map(row=>({id:row.dataset.task,choice:$('select',row).value}));
  function progress(){$('#diagnosis-progress').textContent=`${current().filter(x=>x.choice).length} di 8 compiti classificati`;}
  tasks.forEach(row=>$('select',row).addEventListener('change',()=>{progress();$('#diagnosis-comparison').hidden=true;}));
  $('#compare-diagnosis').addEventListener('click',()=>{
   const out=$('#diagnosis-comparison');out.replaceChildren(write('strong','Confronto con la chiave proposta'));
   const list=write('ul','');
   for(const item of current()){
    const status=item.choice===expected[item.id]?'Coincide con la proposta':item.choice?'Scelta differente: motiva la scelta':'Da classificare';
    list.append(write('li',`${item.id} · Scelta: ${label(types,item.choice)} · Ipotesi di partenza: ${types[expected[item.id]]} · ${status}`));
   }
   out.append(list,write('p','Questa chiave è un’ipotesi didattica, non la valutazione di un modello AI. Non assegna voti.'));
   out.hidden=false;announce('Confronto di diagnosi visibile');
  });
  const skillKeys=[['role','Ruolo'],['context','Contesto e dati ammessi'],['forbidden','Divieti'],['format','Formato'],['clarification','Chiarimenti'],['human','Passaggio a una persona']];
  const skillText=()=>skillKeys.map(([key,title])=>`${title}:\n${$(`[data-skill="${key}"]`).value.trim()||'[da definire]'}`).join('\n\n');
  $('#copy-skill').addEventListener('click',()=>{
   if(!$$('[data-skill]').some(x=>x.value.trim()))return announce('Compila almeno una parte della skill');
   copyText('MANZO AI · Officina locale · Skill v1 su dati fittizi\n\n'+skillText());
  });
  // Deterministic, entirely in-browser: prices and order constraints are in the original source document.
  const money=value=>new Intl.NumberFormat('it-IT',{style:'currency',currency:'EUR'}).format(value);
  const minute=time=>/^\d{2}:\d{2}$/.test(time)?Number(time.slice(0,2))*60+Number(time.slice(3)):NaN;
  function simStatus(ok){return ok?'Rispettata':'Non rispettata';}
  function simulate(){
   const products=$$('[data-sim-product]').map(el=>({key:el.dataset.simProduct,quantity:Math.min(99,Math.max(0,Math.floor(Number(el.value)||0))),price:Number(el.dataset.price)}));
   const total=products.reduce((acc,item)=>acc+item.quantity*item.price,0);
   const days=Number($('#sim-days').value);
   const orderTime=minute($('#sim-order-time').value),pickTime=minute($('#sim-pickup-time').value);
   const okOrder=days>=2||(days===1&&orderTime<=18*60);
   const okPickup=$('#sim-weekday').value!=='lun'&&pickTime>=7*60+30&&pickTime<=13*60;
   const hasCake=products.some(x=>x.key==='torta'&&x.quantity>0);
   const okCake=!hasCake||days>=2;
   const out=$('#sim-results');out.replaceChildren(write('h4','Risultato delle regole fisse'));
   const list=write('ul','');
   list.append(write('li',`Totale calcolato: ${money(total)} · ${products.reduce((sum,x)=>sum+x.quantity,0)} articoli`));
   list.append(write('li',`Regola 1 · Ordine entro le 18:00 del giorno prima: ${Number.isFinite(orderTime)?simStatus(okOrder):'Orario da indicare'}`));
   list.append(write('li',`Regola 2 · Ritiro tra le 7:30 e le 13:00, escluso lunedì: ${Number.isFinite(pickTime)?simStatus(okPickup):'Orario da indicare'}`));
   list.append(write('li',`Regola 3 · Torte con due giorni di calendario: ${simStatus(okCake)}${hasCake?'':' (nessuna torta ordinata: regola non applicabile)'}`));
   out.append(list,write('p','Il simulatore non interpreta messaggi né verifica disponibilità, allergeni o ordini reali. Non sostituisce un addetto.'));
  }
  $$('[data-sim-product],#sim-days,#sim-order-time,#sim-weekday,#sim-pickup-time').forEach(el=>el.addEventListener(el.tagName==='SELECT'?'change':'input',simulate));
  simulate();
  const tests=$$('[data-test]');
  const trialEntries=()=>tests.map(box=>({id:box.dataset.test,v1:$$('[data-run="v1"]',box).map(sel=>sel.value),v2:$$('[data-run="v2"]',box).map(sel=>sel.value),note:$('[data-trial-note]',box).value.trim()}));
  const show=value=>value==='ok'?'Senza errori':value==='fail'?'Con errore':'Non provata';
  function trialSummary(){
   const entries=trialEntries();const count=v=>entries.reduce((n,item)=>n+item[v].filter(Boolean).length,0);
   const out=$('#trial-summary');out.replaceChildren(write('strong',`${count('v1')} / 18 prove registrate per v1 · ${count('v2')} / 18 prove registrate per v2`));
   for(const version of ['v1','v2']){
    const safety=entries.find(x=>x.id==='T6')[version];
    const verdict=safety.some(x=>x==='fail')?'Almeno un errore registrato':safety.some(Boolean)?'Nessun errore registrato':'Nessuna prova T6 registrata';
    out.append(write('p',`T6 · ${version}: ${verdict} (${safety.filter(Boolean).length}/3 osservazioni manuali)`));
   }
   out.append(write('p','Sono appunti di prove eventualmente condotte altrove: nessun test viene eseguito o dichiarato superato dalla pagina.'));
  }
  $$('[data-run],[data-trial-note]').forEach(el=>el.addEventListener(el.tagName==='SELECT'?'change':'input',trialSummary));
  $('#copy-officina').addEventListener('click',()=>{
   const lines=['MANZO AI · Officina locale · Scheda con dati fittizi','La pagina NON ha eseguito alcun modello AI','DIAGNOSI',...current().map(x=>`${x.id}: ${label(types,x.choice)}`),'','SKILL V1',skillText(),'','TEST OSSERVATI MANUALMENTE'];
   for(const entry of trialEntries()){
    for(const v of ['v1','v2'])lines.push(`${entry.id} ${v}: ${entry[v].map((value,i)=>`Prova ${i+1}: ${show(value)}`).join(' · ')}`);
    if(entry.note)lines.push(`Nota ${entry.id}: ${entry.note}`);
   }
   lines.push('','CORREZIONI V2',$('#skill-revision').value.trim()||'[non compilate]','LIMITI: dati fittizi; esiti non verificati; nessuna certificazione o consulenza.');
   copyText(lines.join('\n'));
  });
  $('#reset-officina').addEventListener('click',()=>{
   tasks.forEach(row=>$('select',row).value='');$('#diagnosis-comparison').hidden=true;progress();
   announce('Diagnosi ripristinata. Gli appunti delle prove non sono stati cancellati');
  });
  progress();trialSummary();
 }
 if(room==='confini'){
  const types={autonomo:'Autonomo',conferma:'Con conferma',umano:'Solo umano'};
  const actions=$$('tr[data-action]');
  const traits={A3:['effetto esterno','difficile da annullare'],A5:['difficile da annullare'],A7:['effetto esterno','difficile da annullare'],A8:['effetto esterno','difficile da annullare'],A9:['denaro'],A10:['denaro'],A11:['effetto esterno','denaro']};
  const data=()=>actions.map(row=>({id:row.dataset.action,action:row.children[1].textContent.trim(),level:$('[data-autonomy]',row).value,owner:$('[data-owner]',row).value.trim()}));
  const described=level=>label(types,level);
  let before=null;
  let showFinal=false;
  const incidents=$$('[data-incident]');
  for(const card of incidents){
   const select=$('[data-incident-action]',card);
   for(const action of actions){const option=write('option',`${action.dataset.action} · ${action.children[1].textContent.trim()}`);option.value=action.dataset.action;select.append(option);}
   const apply=()=>{
    const id=select.value,level=$('[data-incident-level]',card).value;
    if(id&&level){const target=actions.find(el=>el.dataset.action===id);$('[data-autonomy]',target).value=level;refresh();announce(`Livello aggiornato per ${id}; il giudizio Prima rimane invariato`);}
   };
   select.addEventListener('change',apply);$('[data-incident-level]',card).addEventListener('change',apply);
  }
  function warnings(rows){
   const list=[];
   for(const x of rows){
    if((x.level==='conferma'||x.level==='umano')&&!x.owner)list.push(`${x.id} · Manca chi decide: indica il responsabile di ${described(x.level).toLowerCase()}.`);
    if(x.level==='autonomo'&&traits[x.id])list.push(`${x.id} · Attenzione: ${traits[x.id].join(', ')}. Secondo la regola didattica di partenza di solito richiede conferma o è solo umana. Se mantieni «Autonomo», scrivi perché.`);
   }
   return list;
  }
  function renderWarnings(target,rows){
   const items=warnings(rows);
   target.append(write('p','Avvisi di coerenza, non punteggi. Caratteristiche e regola di partenza sono ipotesi didattiche da validare, non soluzioni automatiche.'));
   if(items.length){const ul=write('ul','');for(const item of items)ul.append(write('li',item));target.append(ul);}
   else target.append(write('p','Nessun avviso con le condizioni attuali. Le scelte restano da valutare da una persona.'));
  }
  function renderPreliminary(){
   const out=$('#autonomy-map');out.replaceChildren(write('strong',before?'La mappa Prima è stata congelata':'Mappa provvisoria delle tue decisioni'));
   const list=write('ul','');for(const x of (before||data()))list.append(write('li',`${x.id} · ${described(x.level)} · Responsabile: ${x.owner||'non indicato'}`));out.append(list);
   renderWarnings(out,before||data());out.append(write('p','Non è un giudizio legale o una verifica automatica. Prosegui con gli incidenti per rivedere le scelte.'));
   out.hidden=false;
  }
  function renderFinal(){
   if(!showFinal)return;
   const out=$('#final-autonomy-map');out.replaceChildren();
   if(!before){out.append(write('p','Mostra prima la mappa provvisoria al passo 02 per fissare il giudizio «Prima».'));out.hidden=false;return;}
   const after=data();let changed=0;
   const wrap=write('div','');wrap.className='room-table-scroll';
   const table=document.createElement('table');table.className='room-before-after';
   const thead=document.createElement('thead'),head=document.createElement('tr');
   for(const name of ['Azione','Prima','Dopo','Cambiato'])head.append(write('th',name));thead.append(head);table.append(thead);
   const body=document.createElement('tbody');
   for(const a of after){
    const previous=before.find(item=>item.id===a.id);
    const difference=previous.level!==a.level||previous.owner!==a.owner;if(difference)changed++;
    const row=document.createElement('tr');
    const th=write('th',a.id);th.scope='row';row.append(th);
    row.append(write('td',`${described(previous.level)} · Responsabile: ${previous.owner||'non indicato'}`));
    row.append(write('td',`${described(a.level)} · Responsabile: ${a.owner||'non indicato'}`));
    row.append(write('td',difference?'Sì · Cambiato':'No · Invariato'));body.append(row);
   }
   table.append(body);wrap.append(table);
   out.append(write('strong',changed?`${changed} ${changed===1?'azione modificata':'azioni modificate'}`:'Nessuna azione modificata'),wrap);
   renderWarnings(out,after);out.hidden=false;
  }
  function refresh(){
   $('#autonomy-progress').textContent=`${data().filter(a=>a.level).length} di 12 azioni classificate`;
   if(!$('#autonomy-map').hidden)renderPreliminary();
   renderFinal();
  }
  actions.forEach(row=>$$('select,input',row).forEach(input=>input.addEventListener(input.tagName==='SELECT'?'change':'input',refresh)));
  $('#show-autonomy-map').addEventListener('click',()=>{
   if(!before)before=data().map(a=>({...a}));
   renderPreliminary();renderFinal();announce('Giudizio Prima congelato nella memoria della pagina');
  });
  $('#show-final-map').addEventListener('click',()=>{showFinal=true;renderFinal();announce('Mappa Prima / Dopo aggiornata senza punteggi');});
  $('#copy-confini').addEventListener('click',()=>{
   const now=data();const out=['MANZO AI · Sala dei confini · Studio con dati fittizi','Non è una consulenza legale, non contiene test AI.',...now.map(x=>{
    const old=before?.find(a=>a.id===x.id);
    return `${x.id} · ${x.action} · Prima: ${old?described(old.level):'Non acquisito'} · Dopo: ${described(x.level)} · Responsabile: ${x.owner||'non indicato'}`;
   }),'','AVVISI',...warnings(now),'','INCIDENTI'];
   for(const card of incidents){out.push(`Incidente ${card.dataset.incident}: azione ${$('[data-incident-action]',card).value||'[non scelta]'}, livello ${described($('[data-incident-level]',card).value)} · ${$('[data-incident-response]',card).value.trim()||'[senza nota]'}`);}
   out.push('','Protocollo umano:', $('#autonomy-protocol').value.trim()||'[non compilato]','Motivo del cambiamento:', $('#change-confini').value.trim()||'[non compilato]');
   copyText(out.join('\n'));
  });
  $('#reset-confini').addEventListener('click',()=>{
   before=null;showFinal=false;
   actions.forEach(row=>{$('[data-autonomy]',row).value='';$('[data-owner]',row).value='';});
   incidents.forEach(card=>{$('[data-incident-action]',card).value='';$('[data-incident-level]',card).value='';});
   $('#autonomy-map').hidden=true;$('#final-autonomy-map').hidden=true;$('#change-confini').value='';
   refresh();announce('Mappa e classificazioni ripristinate; le note narrative restano in pagina');
  });
  refresh();
 }
})();
