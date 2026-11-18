#!/usr/bin/env node
/* Deterministic regressions against the real inline Studio applications.
   A small DOM/media harness exercises state and file boundaries; it does not
   claim to emulate Safari, a real microphone, or browser media decoding. */
'use strict';
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const assert=require('node:assert/strict');
const {test}=require('node:test');
const root=path.resolve(__dirname,'../../../..');
const clone=x=>JSON.parse(JSON.stringify(x));
function harness(kind){
  const file=path.join(root,`tools/ai-teaching-${kind==='workspace'?'workspace':kind+'-studio'}/index.html`);
  const html=fs.readFileSync(file,'utf8');
  let code=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)][0][1];
  const nodes=new Map(),windowEvents=new Map(),downloads=[],urls=new Map(),revoked=[],images=[],timers=new Map(),media=[],drawn=[],alerts=[],scrolls=[];
  let serial=0,now=0,confirmation=true;
  const options={voices:[],recorderThrows:false,supported:true};
  class Element{
    constructor(tag='div'){this.tagName=tag.toUpperCase();this.value='';this.textContent='';this.checked=false;this.hidden=false;this.disabled=false;this.files=[];this.dataset={};this.style={};this.children=[];this.attributes={};this.events=new Map()}
    addEventListener(name,fn){if(!this.events.has(name))this.events.set(name,[]);this.events.get(name).push(fn)}
    async emit(name){const event={target:this,preventDefault(){this.prevented=true},returnValue:undefined};for(const fn of this.events.get(name)||[])await fn(event);if(this['on'+name])await this['on'+name](event);return event}
    setAttribute(k,v){this.attributes[k]=String(v)} removeAttribute(k){delete this.attributes[k]}
    append(...values){this.children.push(...values)} replaceChildren(...values){this.children=[...values]}
    focus(){document.activeElement=this} select(){} scrollIntoView(arg){scrolls.push({id:this.id||this.tagName,arg})}
    click(){if(this.tagName==='A'){downloads.push({name:this.download,blob:urls.get(this.href)});return}return this.emit('click')}
  }
  const $=id=>{if(!nodes.has(id)){const el=new Element();el.id=id;nodes.set(id,el)}return nodes.get(id)};
  for(const match of html.matchAll(/\bid="([^"]+)"/g))$(match[1]);
  const tabs=/<nav\b[^>]*\brole="tablist"/.test(html)?new Element('nav'):null;if(tabs)tabs.id='tabs';
  const context={fillRect(){},drawImage(image){drawn.push({image})},measureText:t=>({width:t.length*10}),fillText(text){drawn.push({text})}};
  const document={activeElement:null,getElementById:$,querySelectorAll:()=>[],querySelector:s=>s==='[role=tablist]'?tabs:null,createElement(tag){const el=new Element(tag);if(tag==='canvas'){el.getContext=()=>context;el.captureStream=()=>{const track={stopped:false,stop(){this.stopped=true}};const stream={track,getTracks:()=>[track]};media.push(stream);return stream}}return el}};
  class Image extends Element{constructor(){super('img');this.naturalWidth=4;this.naturalHeight=4;images.push(this)}}
  class MediaRecorder{
    static isTypeSupported(){return options.supported}
    constructor(stream,{mimeType}={}){if(options.recorderThrows)throw Error('Fixture recorder failure');this.stream=stream;this.mimeType=mimeType||'audio/webm';this.state='inactive';media.push(this)}
    start(){this.state='recording'}
    stop(){this.state='inactive';this.ondataavailable?.({data:new Blob(['fixture'],{type:this.mimeType})});this.onstop?.()}
  }
  const speechSynthesis={getVoices:()=>options.voices,cancel(){},speak(utterance){options.spoken=utterance}};
  const window={addEventListener(name,fn){if(!windowEvents.has(name))windowEvents.set(name,[]);windowEvents.get(name).push(fn)},matchMedia:()=>({matches:false}),speechSynthesis,SpeechSynthesisUtterance:function(text){this.text=text}};
  const api={image:'state:()=>({approved,unsaved,imageInfo,objectUrl}),show',voice:'state:()=>({approved,unsaved,recording,requesting,blob,fileName}),setAudio,show',video:'state:()=>({approval,unsaved,rendering,audioReferenceName}),getScenes:()=>scenes,setScenes:value=>{scenes=value},exportSilent,show',workspace:'state:()=>({approved,unsaved,approvedAt}),assets,clean,validateStudyFile,manifest'}[kind];
  const end=code.lastIndexOf('})();');assert.ok(end>0,'Application closure found');
  code=code.slice(0,end)+`globalThis.app={${api}};\n`+code.slice(end);
  const sandbox={document,window,Image,MediaRecorder,Blob,console,performance:{now:()=>now},navigator:{mediaDevices:{getUserMedia:async()=>({getTracks:()=>[]})}},URL:{createObjectURL(blob){const u='blob:fixture-'+(++serial);urls.set(u,blob);return u},revokeObjectURL(u){revoked.push(u);urls.delete(u)}},alert:message=>alerts.push(message),confirm:()=>confirmation,setTimeout:()=>++serial,clearTimeout(){},setInterval(fn){const id=++serial;timers.set(id,fn);return id},clearInterval:id=>timers.delete(id),speechSynthesis,SpeechSynthesisUtterance:window.SpeechSynthesisUtterance};
  vm.createContext(sandbox);vm.runInContext(code,sandbox,{filename:file,timeout:1000});
  return {app:sandbox.app,$,options,images,downloads,urls,revoked,media,alerts,scrolls,drawn,sandbox,confirm:value=>{confirmation=value},async file(id,data,size){$(id).files=[{size:size??JSON.stringify(data).length,text:async()=>JSON.stringify(data)}];await $(id).emit('change')},async event(name){const e={preventDefault(){this.prevented=true},returnValue:undefined};for(const fn of windowEvents.get(name)||[])await fn(e);return e},tick(ms){now=ms;for(const fn of [...timers.values()])fn()}};
}
function study(kind){
  const common={schema:`ai-teaching-lab-${kind}-v0.1`,exportedAt:'2026-11-17T10:00:00Z',fields:{title:'Ciclo dell’acqua',objective:'Spiegare il processo',audience:'Classe sintetica',origin:'local',source:'Materiale sintetico autorizzato'},review:{c1:true,c2:true,c3:true,c4:true},approval:{approved:true,approvedAt:'2026-11-17',reviewer:'Docente sintetico'}};
  if(kind==='image'){common.fields.alt='Tre fasi con frecce';common.fields.evidence='Ordina e spiega';common.image={name:'fixture.png',type:'image/png',size:100,width:4,height:4}}
  if(kind==='voice'){common.fields.origin='recorded';common.fields.transcript='La sequenza';common.fields.script='La sequenza';common.fields.audioDescription='Testo disponibile';common.audio={name:'fixture.wav',mimeType:'audio/wav',size:100}}
  if(kind==='video'){common.fields.captions='La sequenza';common.scenes=[{id:'scene-synthetic',title:'Evaporazione',goal:'Spiegare',caption:'L’acqua evapora',seconds:2,origin:'ai_external',source:'Modello e licenza sintetici dichiarati',imageName:'fixture.png'}];common.audioReference='fixture.wav'}
  return common;
}
function kit(assets){return {schema:'ai-teaching-lab-multimedia-kit-v0.1',title:'Kit sintetico',audience:'Classe sintetica',learningObjective:'Spiegare',assessment:'Riordinare',teachingSequence:'Osservare, spiegare',accessibility:'Testi alternativi',rightsAndPrivacy:'Solo fixture',assets,review:{reviewer:'Docente sintetico',reviewDate:'2026-11-17',notes:'Fixture'},approval:{approved:true,approvedAt:'2026-11-17'}}}
function fill(h,values){for(const [id,value]of Object.entries(values))h.$(id).value=value}
function checks(h,ids=['c1','c2','c3','c4']){for(const id of ids)h.$(id).checked=true}
function videoScene(){return {id:'scene-fixture',title:'Originale',goal:'Spiegare',caption:'Didascalia originale',seconds:2,origin:'local',source:'',imageName:'fixture.png',image:{naturalWidth:4,naturalHeight:4},imageUrl:'blob:original',imageRequest:0}}
async function approveVideo(h){fill(h,{title:'Fixture',audience:'Classe',objective:'Spiegare',why:'Sequenza',assessment:'Ordina',captions:'Didascalia originale',access:'Testo alternativo',reviewer:'Docente'});h.app.setScenes([videoScene()]);checks(h);await h.$('approve').emit('click');assert.equal(h.app.state().approval,true)}

test('Workspace rejects false approval both at direct import and legacy restoration',async()=>{
  const h=harness('workspace');
  for(const kind of ['image','voice','video']){
    const raw=study(kind);raw.review.c3=false;
    assert.throws(()=>h.app.validateStudyFile(raw),/controlli/);
    const malicious=kit({[kind]:raw});
    h.$('title').value='Lavoro da conservare';await h.file('kitfile',malicious);
    assert.equal(h.$('title').value,'Lavoro da conservare');assert.equal(h.app.assets[kind],null);assert.match(h.$('restorestatus').textContent,/non riuscito/);
  }
});
test('Workspace preserves source fields, complete scene provenance and legacy numeric reviews',async()=>{
  const h=harness('workspace'),assets={};
  for(const kind of ['image','voice','video']){
    const raw=study(kind);raw.fields.extended='x'.repeat(9000);
    const normalized=h.app.clean(raw),legacy=clone(normalized);delete legacy.reviewChecks;
    assert.equal(normalized.fields.extended,raw.fields.extended);
    assert.equal(h.app.clean(legacy).review,4);
    assets[kind]=legacy;
  }
  assert.equal(assets.video.media.scenes[0].id,'scene-synthetic');assert.equal(assets.video.media.scenes[0].source,'Modello e licenza sintetici dichiarati');
  assert.equal(assets.voice.fields.audioDescription,'Testo disponibile');
  checks(h);await h.file('kitfile',kit(assets));
  assert.equal(h.$('title').value,'Kit sintetico');assert.equal(h.app.state().approved,false);
  assert.equal(h.$('c1').checked,false);assert.equal(h.app.assets.video.media.audioReference,'fixture.wav');
  const repeated=h.app.clean(h.app.assets.video);assert.equal(repeated.review,4);assert.equal(repeated.media.scenes[0].imageName,'fixture.png');
});
test('Workspace restoration is atomic when a later field or asset is invalid',async()=>{
  const h=harness('workspace');await h.file('jsonfile',study('image'));h.$('title').value='Originale';
  const before=JSON.stringify(h.app.assets),m=kit({image:study('image'),voice:study('voice')});m.review.notes='x'.repeat(50001);
  await h.file('kitfile',m);assert.equal(h.$('title').value,'Originale');assert.equal(JSON.stringify(h.app.assets),before);
  const incompatible=kit({image:study('voice')});await h.file('kitfile',incompatible);assert.equal(h.$('title').value,'Originale');assert.equal(JSON.stringify(h.app.assets),before);
});
test('Workspace rejects unknown schemas, malformed review counts and oversized files',async()=>{
  const h=harness('workspace');assert.throws(()=>h.app.clean({schema:'unknown'}),/Formato/);
  const f=study('image');f.fields.title={malformed:true};assert.throws(()=>h.app.clean(f),/Testo/);
  const legacy=h.app.clean(study('video'));legacy.review=3;assert.throws(()=>h.app.clean(legacy),/coerenti/);delete legacy.reviewChecks;assert.throws(()=>h.app.clean(legacy),/controlli/);
  await h.file('jsonfile',study('image'),2*1024*1024+1);assert.equal(h.app.assets.image,null);assert.match(h.$('importstatus').textContent,/2 MB/);
});
test('Workspace cancel and stale reads preserve the current asset',async()=>{
  const h=harness('workspace');await h.file('jsonfile',study('image'));const first=JSON.stringify(h.app.assets.image);
  const replacement=study('image');replacement.fields.title='Sostituzione';h.confirm(false);await h.file('jsonfile',replacement);assert.equal(JSON.stringify(h.app.assets.image),first);
  h.confirm(true);let resolve;h.$('jsonfile').files=[{size:100,text:()=>new Promise(r=>{resolve=r})}];const pending=h.$('jsonfile').emit('change');
  await h.file('jsonfile',replacement);resolve(JSON.stringify(study('image')));await pending;assert.equal(h.app.assets.image.fields.title,'Sostituzione');
});
test('All four tools warn on unsaved editing and clear the warning after JSON export',async()=>{
  for(const kind of ['image','voice','video','workspace']){
    const h=harness(kind);assert.equal((await h.event('beforeunload')).prevented,undefined);
    h.$('title').value='Bozza';await h.$('title').emit('input');assert.equal((await h.event('beforeunload')).prevented,true,kind);
    await h.$(kind==='workspace'?'exportJSON':'export').emit('click');assert.equal((await h.event('beforeunload')).prevented,undefined,kind);
    await h.$('title').emit('input');assert.equal((await h.event('beforeunload')).prevented,true,kind);
  }
});
test('Image decode race keeps the latest file and preserves it on rejected replacement',async()=>{
  const h=harness('image'),file=name=>({name,type:'image/png',size:10});
  h.$('upload').files=[file('first.png')];await h.$('upload').emit('change');
  h.$('upload').files=[file('latest.png')];await h.$('upload').emit('change');
  h.images[1].onload();h.images[0].onload();assert.equal(h.app.state().imageInfo.name,'latest.png');assert.ok(h.revoked.includes('blob:fixture-1'));
  h.$('upload').files=[{name:'invalid.png',type:'image/png',size:0}];await h.$('upload').emit('change');assert.equal(h.app.state().imageInfo.name,'latest.png');
  h.confirm(false);h.$('upload').files=[file('cancelled.png')];await h.$('upload').emit('change');assert.equal(h.app.state().imageInfo.name,'latest.png');
});
test('Image and voice origin changes revoke approval and require fresh checks',async()=>{
  const image=harness('image');fill(image,{title:'Fixture',objective:'Spiegare',audience:'Classe',evidence:'Ordina',origin:'local',alt:'Descrizione',teacher:'Docente'});
  image.$('upload').files=[{name:'fixture.png',type:'image/png',size:10}];await image.$('upload').emit('change');image.images[0].onload();checks(image,['r1','r2','r3','r4']);await image.$('approve').emit('click');assert.equal(image.app.state().approved,true);
  image.$('origin').value='other';await image.$('origin').emit('change');assert.equal(image.app.state().approved,false);assert.equal(image.$('r1').checked,false);
  const voice=harness('voice');voice.app.setAudio(new Blob(['fixture'],{type:'audio/wav'}),'fixture.wav');fill(voice,{title:'Fixture',audience:'Classe',objective:'Spiegare',assessment:'Ordina',script:'Copione',origin:'recorded',transcript:'Copione',reviewer:'Docente'});checks(voice);await voice.$('approve').emit('click');assert.equal(voice.app.state().approved,true);
  voice.$('origin').value='ai_external';await voice.$('origin').emit('change');assert.equal(voice.app.state().approved,false);assert.equal(voice.$('c1').checked,false);
});
test('Voice synthesis never falls back to a remote service',async()=>{
  const h=harness('voice');fill(h,{script:'Testo sintetico',language:'it-IT'});h.options.voices=[{lang:'it-IT',localService:false}];await h.$('tts').emit('click');assert.equal(h.options.spoken,undefined);assert.match(h.$('ttsnote').textContent,/Nessuna voce locale/);
  const local={lang:'it-IT',localService:true};h.options.voices.push(local);await h.$('tts').emit('click');assert.equal(h.options.spoken.voice,local);
});
test('Voice pending permission is cancelled safely on pagehide',async()=>{
  const h=harness('voice');let resolve,stopped=false;h.sandbox.navigator.mediaDevices.getUserMedia=()=>new Promise(r=>{resolve=r});const pending=h.$('record').emit('click');assert.equal(h.app.state().requesting,true);await h.event('pagehide');resolve({getTracks:()=>[{stop(){stopped=true}}]});await pending;assert.equal(stopped,true);assert.equal(h.app.state().recording,false);assert.equal(h.app.state().requesting,false);
});
test('Video export uses an immutable scene snapshot and releases every track',async()=>{
  const h=harness('video'),scene=videoScene();h.app.setScenes([scene]);await h.app.exportSilent();assert.equal(h.app.state().rendering,true);scene.caption='Modifica successiva';h.app.setScenes([]);h.tick(1000);assert.ok(h.drawn.some(x=>x.text==='Didascalia originale'));assert.ok(!h.drawn.some(x=>x.text==='Modifica successiva'));h.tick(2100);assert.equal(h.app.state().rendering,false);assert.equal(h.$('render').disabled,false);assert.equal(h.media[0].track.stopped,true);assert.equal(h.downloads[0].name,'studio-video-silenzioso.webm');
});
test('Video recorder failures, pagehide and unsupported WebM clean up predictably',async()=>{
  const failed=harness('video');failed.options.recorderThrows=true;failed.app.setScenes([videoScene()]);await failed.app.exportSilent();assert.equal(failed.app.state().rendering,false);assert.equal(failed.media[0].track.stopped,true);assert.match(failed.$('renderStatus').textContent,/Impossibile avviare/);
  const cancelled=harness('video');cancelled.app.setScenes([videoScene()]);await cancelled.app.exportSilent();await cancelled.event('pagehide');assert.equal(cancelled.app.state().rendering,false);assert.equal(cancelled.media[0].track.stopped,true);assert.equal(cancelled.downloads.length,0);
  const fallback=harness('video');fallback.options.supported=false;fallback.app.setScenes([videoScene()]);await fallback.app.exportSilent();assert.equal(fallback.app.state().rendering,false);assert.equal(fallback.media.length,0);assert.match(fallback.$('renderStatus').textContent,/storyboard e VTT/);
});
test('Rejected video audio invalidates approval and preserves the previous reference',async()=>{
  const h=harness('video');h.$('audio').files=[{name:'original.wav',type:'audio/wav',size:100}];await h.$('audio').emit('change');await approveVideo(h);
  h.$('audio').files=[{name:'invalid.txt',type:'text/plain',size:2}];await h.$('audio').emit('change');assert.equal(h.app.state().approval,false);assert.equal(h.app.state().audioReferenceName,'original.wav');assert.equal(h.$('c1').checked,false);
  await h.$('export').emit('click');const record=JSON.parse(await h.downloads.at(-1).blob.text());assert.equal(record.audioReference,'original.wav');assert.equal(record.approval.approved,false);
});
test('Studio step navigation focuses and scrolls the selected tab into view',()=>{
  for(const kind of ['image','voice','video']){const h=harness(kind);h.app.show(5);assert.equal(h.$('p5').hidden,false);assert.equal(h.$('p1').hidden,true);assert.equal(h.$('t5').tabIndex,0);assert.equal(h.scrolls.at(-1).id,'t5');assert.equal(h.scrolls.at(-1).arg.inline,'nearest')}
});
