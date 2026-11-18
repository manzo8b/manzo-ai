#!/usr/bin/env node
/* Mission Studio v0.1 state regressions against its real inline application.
   The deterministic DOM fixture does not replace browser/mobile QA. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const assert=require('node:assert/strict');
const {test}=require('node:test');
const root=path.resolve(__dirname,'../../../..');
function harness(search=''){
 const html=fs.readFileSync(path.join(root,'tools/ai-teaching-launchpad/index.html'),'utf8');
 let script=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)][0][1];
 const nodes=new Map(),controls=[],events=new Map(),downloads=[],urls=new Map(),dialogs=[];
 let serial=0,answer=true;
 class Element{
  constructor(tag='div'){this.tagName=tag.toUpperCase();this._value='';this.options=[];this.selectedIndex=0;this.textContent='';this.dataset={};this.children=[];this.attributes={};this.events=new Map();this.files=[]}
  get value(){return this.tagName==='SELECT'?(this.options[this.selectedIndex]?.value||''):this._value}
  set value(value){if(this.tagName==='SELECT')this.selectedIndex=this.options.findIndex(o=>o.value===value);else this._value=value}
  addEventListener(type,fn){if(!this.events.has(type))this.events.set(type,[]);this.events.get(type).push(fn)}
  async emit(type){for(const fn of this.events.get(type)||[])await fn({currentTarget:this,target:this})}
  setAttribute(name,value){this.attributes[name]=String(value)}
  append(...children){this.children.push(...children)} replaceChildren(...children){this.children=[...children]}
  focus(){} scrollIntoView(){} remove(){}
  click(){if(this.tagName==='A')downloads.push({name:this.download,blob:urls.get(this.href)});else return this.emit('click')}
 }
 // Only instantiate controls that actually exist in the source document.
 for(const match of html.matchAll(/<([a-z][a-z0-9]*)\b([^>]*\bid="([^"]+)"[^>]*)>/gi)){
  const el=new Element(match[1]);el.id=match[3];el._value=match[2].match(/\bvalue="([^"]*)"/)?.[1]||'';nodes.set(el.id,el);
 }
 const $=id=>{assert.ok(nodes.has(id),'Real element exists: '+id);return nodes.get(id)};
 const selectSource=html.match(/<select\b[^>]*id="audience"[^>]*>([\s\S]*?)<\/select>/)[1];
 $('audience').options=[...selectSource.matchAll(/<option([^>]*)>([^<]*)<\/option>/g)].map((match,index)=>{if(/\bselected\b/.test(match[1]))$('audience').selectedIndex=index;return {value:match[2]}});
 for(const match of html.matchAll(/<button\b([^>]*\bdata-(kind|topic|minutes)="([^"]+)"[^>]*)>/g)){const el=new Element('button');el.dataset[match[2]]=match[3];controls.push(el)}
 const document={body:new Element('body'),getElementById:$,querySelectorAll(selector){const attribute=selector.match(/^\[data-(kind|topic|minutes)\]$/)?.[1];return attribute?controls.filter(el=>Object.hasOwn(el.dataset,attribute)):[]},createElement:tag=>new Element(tag),createTextNode:text=>({textContent:text})};
 const window={matchMedia:()=>({matches:true}),addEventListener(type,fn){if(!events.has(type))events.set(type,[]);events.get(type).push(fn)}};
 const context={document,window,Blob,URLSearchParams,location:{search},navigator:{clipboard:{writeText:async()=>{}}},confirm:message=>{dialogs.push(message);return answer},URL:{createObjectURL(blob){const id='blob:mission-'+(++serial);urls.set(id,blob);return id},revokeObjectURL:id=>urls.delete(id)},setTimeout:()=>++serial};
 const end=script.lastIndexOf('})();');script=script.slice(0,end)+'globalThis.app={state,validateDraft,flags:()=>({unsaved,restoreRequest})};\n'+script.slice(end);
 vm.createContext(context);vm.runInContext(script,context,{timeout:1000,filename:'mission-inline.js'});
 return {app:context.app,$,controls,downloads,dialogs,answer:value=>{answer=value},async event(type){const event={preventDefault(){this.prevented=true},returnValue:undefined};for(const fn of events.get(type)||[])await fn(event);return event},async restore(data,{size,text}={}){const body=text??JSON.stringify(data);$('restore').files=[{size:size??body.length,text:async()=>body}];await $('restore').emit('change')}};
}
const snapshot=h=>JSON.stringify({state:h.app.state(),topic:h.$('topic').value,audience:h.$('audience').value,objective:h.$('objective').value},(key,value)=>key==='createdAt'?undefined:value);
function draft(h,changes={}){return {...h.app.state(),topic:'Tema sintetico',objective:'Ordinare tre elementi\ne motivare  due relazioni',...changes}}

test('Mission reset requires confirmation and cancellation retains the current draft',async()=>{
 const h=harness();h.$('topic').value='Da conservare';await h.$('topic').emit('input');const before=snapshot(h);
 h.answer(false);await h.$('reset').emit('click');assert.equal(snapshot(h),before);assert.match(h.dialogs.at(-1),/Scaricalo prima/);
 h.answer(true);await h.$('reset').emit('click');assert.equal(h.$('topic').value,"Il ciclo dell'acqua");assert.equal(h.$('objective').value,'');assert.equal(h.app.state().approval,false);
});
test('Mission changes warn before leaving; JSON export clears the warning and copying does not',async()=>{
 const h=harness();assert.equal((await h.event('beforeunload')).prevented,undefined);
 for(const field of ['topic','audience','objective']){await h.$(field).emit('change');assert.equal((await h.event('beforeunload')).prevented,true);await h.$('export').emit('click');assert.equal((await h.event('beforeunload')).prevented,undefined)}
 for(const key of ['kind','topic','minutes']){const control=h.controls.find(el=>Object.hasOwn(el.dataset,key));await control.emit('click');assert.equal((await h.event('beforeunload')).prevented,true);await h.$('export').emit('click')}
 h.$('objective').value='Spiegare';await h.$('objective').emit('input');await h.$('copy').emit('click');assert.equal((await h.event('beforeunload')).prevented,true);
});
test('Mission imports preserve editable text exactly and remain unapproved',async()=>{
 const h=harness(),data=draft(h,{topic:'T'.repeat(110),objective:'Obiettivo  con  spazi\ne righe distinte'});
 await h.restore(data);assert.equal(h.$('topic').value,data.topic);assert.equal(h.$('objective').value,data.objective);assert.equal(h.app.state().approval,false);assert.equal((await h.event('beforeunload')).prevented,true);
 await h.$('export').emit('click');const record=JSON.parse(await h.downloads.at(-1).blob.text());assert.equal(record.schema,'ai-teaching-lab-mission-v0.1');assert.equal(record.topic,data.topic);assert.equal(record.objective,data.objective);assert.equal(record.approval,false);assert.match(h.$('form-status').textContent,/suggerimenti sono ricostruiti/);
});
test('Mission rejects overlength, incompatible and invalid data atomically instead of truncating',async()=>{
 const h=harness();h.$('topic').value='Brief corrente';await h.$('topic').emit('input');const before=snapshot(h);
 const cases=[{topic:'x'.repeat(111)},{objective:'x'.repeat(601)},{topic:'Tema\nnon valido'},{objective:'Testo\r\nnon standard'},{minutes:60},{minutes:'30'},{audience:'Destinatari sconosciuti'},{mission:'unknown'},{mission:'toString'},{schema:'ai-teaching-lab-multimedia-kit-v0.1'},{approval:true},{topic:[]},{objective:null}];
 for(const changes of cases){await h.restore(draft(h,changes));assert.equal(snapshot(h),before,JSON.stringify(changes));assert.match(h.$('form-status').textContent,/non è stato sostituito/)}
});
test('Mission cancelled replacement retains all current input values',async()=>{
 const h=harness();h.$('topic').value='Conservare';await h.$('topic').emit('input');const before=snapshot(h);h.answer(false);await h.restore(draft(h));assert.equal(snapshot(h),before);
});
test('Mission stale file reads cannot overwrite a later import or new editing',async()=>{
 const h=harness();let resolve;const first=draft(h,{topic:'Prima richiesta'}),second=draft(h,{topic:'Richiesta più recente'});
 h.$('restore').files=[{size:100,text:()=>new Promise(r=>{resolve=r})}];const pending=h.$('restore').emit('change');await h.restore(second);resolve(JSON.stringify(first));await pending;assert.equal(h.$('topic').value,second.topic);
 let resolveEdit;h.$('restore').files=[{size:100,text:()=>new Promise(r=>{resolveEdit=r})}];const pendingEdit=h.$('restore').emit('change');h.$('topic').value='Nuova modifica';await h.$('topic').emit('input');resolveEdit(JSON.stringify(first));await pendingEdit;assert.equal(h.$('topic').value,'Nuova modifica');
});
test('Mission reset invalidates pending restore while malformed and oversized files preserve state',async()=>{
 const h=harness();let resolve;h.$('restore').files=[{size:100,text:()=>new Promise(r=>{resolve=r})}];const pending=h.$('restore').emit('change');await h.$('reset').emit('click');resolve(JSON.stringify(draft(h)));await pending;assert.equal(h.$('topic').value,"Il ciclo dell'acqua");
 const before=snapshot(h);await h.restore(null,{text:'{'});assert.equal(snapshot(h),before);await h.restore(null,{size:0});assert.equal(snapshot(h),before);assert.match(h.$('form-status').textContent,/1 MB/);
 let read=false;h.$('restore').files=[{size:1024*1024+1,text:async()=>{read=true;return '{}'}}];await h.$('restore').emit('change');assert.equal(read,false);assert.equal(snapshot(h),before);
});
test('Mission query parameters select only an existing local mission',()=>{
 assert.equal(harness('?mission=video').app.state().mission,'video');assert.equal(harness('?mission=unknown').app.state().mission,'image');assert.equal(harness('?mission=toString').app.state().mission,'image');
});
