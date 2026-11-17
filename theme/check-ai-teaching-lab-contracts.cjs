#!/usr/bin/env node
/**
 * AI Teaching Lab: zero-dependency source and rendered-site contract tests.
 * Scope: structure, JavaScript syntax, provenance disclosure and links.
 * Does not replace physical browser, accessibility or pedagogical testing.
 */
"use strict";
const fs=require("node:fs");
const path=require("node:path");
const vm=require("node:vm");
const assert=require("node:assert/strict");
const root=path.resolve(__dirname,"..");
const route="it/formazione/ia-per-la-didattica";
const sources={
 image:"tools/ai-teaching-image-studio/index.html",
 voice:"tools/ai-teaching-voice-studio/index.html",
 video:"tools/ai-teaching-video-studio/index.html",
 workspace:"tools/ai-teaching-workspace/index.html"
};
const routes={image:"studio-immagini",voice:"studio-voce",video:"studio-video",workspace:"workspace-multimediale"};
const schemas={
 image:"ai-teaching-lab-image-v0.1",
 voice:"ai-teaching-lab-voice-v0.1",
 video:"ai-teaching-lab-video-v0.1",
 workspace:"ai-teaching-lab-multimedia-kit-v0.1"
};
function load(file){
 const full=path.join(root,file);
 assert.ok(fs.existsSync(full),"Missing "+file);
 const value=fs.readFileSync(full,"utf8");
 assert.ok(value.length>5000,"Suspiciously short "+file);
 return value;
}
function checkHtml(name,html){
 const scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script\s*>/gi)];
 assert.ok(scripts.length>=2,name+": missing application or guided demo scripts");
 scripts.forEach((m,i)=>new vm.Script(m[1],{filename:name+"-inline-"+i+".js"}));
 const bare=html.replace(/<script(?:\s[^>]*)?>[\s\S]*?<\/script\s*>/gi,"");
 const ids=[...bare.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
 assert.equal(new Set(ids).size,ids.length,name+": duplicate static ID");
 assert.ok(ids.includes("approve"),name+": missing approval");
 assert.ok(html.includes(schemas[name]),name+": missing export schema");
 assert.ok(html.includes("esempio")||html.includes("Esempio"),name+": missing beginner guidance");
 assert.ok(html.includes("docente"),name+": missing teacher authority");
 assert.ok(html.includes("#205beb")||html.includes("#205BEB"),name+": missing palette");
 return {scripts:scripts.length,ids:ids.length};
}
const htmls=Object.fromEntries(Object.entries(sources).map(([k,v])=>[k,load(v)]));
const stats=Object.fromEntries(Object.entries(htmls).map(([k,v])=>[k,checkHtml(k,v)]));
const workspace=htmls.workspace;
for(const schema of Object.values(schemas))assert.ok(workspace.includes(schema),"Workspace misses "+schema);
for(const studio of ["image","voice","video"]){
 assert.ok(htmls[studio].includes("../workspace-multimediale/"),studio+": missing handoff");
 assert.ok(workspace.includes("../"+routes[studio]+"/"),"Workspace: missing "+studio+" link");
}
for(const id of ["kitfile","restorestatus","sample-brief","wk-all","wk1","wk5","jsonfile","exportJSON","exportHTML"]){
 assert.ok(workspace.includes('id="'+id+'"'),"Workspace: missing "+id);
}
assert.ok(workspace.includes("validateStudyFile(raw)"),"Missing import validation");
assert.ok(workspace.includes("imageName:get(s.imageName)"),"Video per-scene provenance dropped");
assert.ok(workspace.includes("Provenienza e file — "),"HTML delivery must include declared asset provenance");
assert.ok(workspace.includes("className=\"provenance-details\""),"Workspace UI must expose provenance");
assert.ok(workspace.includes("approvazione finale verrà azzerata"),"Missing restoration disclaimer");
assert.ok(workspace.includes("approved=false;approvedAt=null;changed=true"),"Restored kit needs a fresh review");
assert.ok(workspace.includes(".layout>main{order:0!important"),"Mobile must show task before status");
assert.ok(workspace.includes('class="example-detail"'),"Missing compact contextual examples");
assert.ok(workspace.includes("data-atl-workspace"),"Missing mobile scope marker");
for(const studio of ["image","voice","video"]){
 assert.ok(htmls[studio].includes('id="guided-demo"'),studio+": missing demo");
 assert.ok(htmls[studio].includes('class="learn-next"'),studio+": missing workspace CTA");
 assert.ok(htmls[studio].includes("field-guide"),studio+": missing field guidance");
 assert.ok(htmls[studio].includes("learn-flow-mobile"),studio+": missing compact mobile learning guide");
 assert.ok(htmls[studio].includes("field-example"),studio+": missing expandable examples");
}
assert.ok(htmls.video.includes("silenzioso"),"Video silent-only disclosure missing");
assert.ok(htmls.voice.includes("non genera voci IA"),"Voice non-AI disclosure missing");
assert.ok(htmls.image.includes("Non genera immagini con IA"),"Image non-AI disclosure missing");

/* Import/export boundary: exercise real normalization and validation logic,
   without loading any UI, account data or user files. */
const begin=workspace.indexOf("function safeValue");
const end=workspace.indexOf("function render(){",begin);
assert.ok(begin!==-1 && end>begin,"Import normalization source missing");
const normalizedFunctions=workspace.slice(begin,end);
const validators=vm.runInNewContext(
  "(function(){const types="+JSON.stringify({[schemas.image]:"image",[schemas.voice]:"voice",[schemas.video]:"video"})+";"+
  normalizedFunctions+"return {clean,validateStudyFile};})()",
  {},{timeout:1000}
);
const sampleVideo={
 schema:schemas.video,exportedAt:"2026-11-17T18:00:00Z",
 fields:{title:"Evaporazione",objective:"Spiegare il ciclo"},
 approval:{approved:true,approvedAt:"2026-11-17",reviewer:"Docente"},
 review:{c1:true,c2:true,c3:true,c4:true},
 scenes:[{title:"Acqua",goal:"Individuare cambiamento",caption:"L'acqua evapora",seconds:5,origin:"ai_external",source:"Fonte e licenza controllate",imageName:"acqua.png"}],
 audioReference:"voce.wav"
};
assert.equal(validators.validateStudyFile(sampleVideo),"video");
const normalizedVideo=validators.clean(sampleVideo);
assert.equal(normalizedVideo.media.scenes[0].source,"Fonte e licenza controllate");
assert.equal(normalizedVideo.media.scenes[0].imageName,"acqua.png");
assert.equal(normalizedVideo.review,4);
assert.equal(validators.clean(normalizedVideo).review,4,"Review count must survive kit reopen");
const corruptVideo={...sampleVideo,scenes:[]};
assert.throws(()=>validators.validateStudyFile(corruptVideo),/scene/,"Approved video without scenes must fail");
const falseApproval={...sampleVideo,review:{c1:true,c2:true,c3:false,c4:true}};
assert.throws(()=>validators.validateStudyFile(falseApproval),/controlli/,"Incomplete reviews must not pass");
const nonBooleanApproval={...sampleVideo,review:{c1:"yes",c2:"yes",c3:"yes",c4:"yes"}};
assert.throws(()=>validators.validateStudyFile(nonBooleanApproval),/controlli/,"Non-boolean checks must fail");
assert.throws(()=>validators.validateStudyFile({schema:"invalid"}),/Formato/,"Unknown import schema must fail");

const siteArg=process.argv.indexOf("--site");
if(siteArg!==-1){
 const site=process.argv[siteArg+1];
 assert.ok(site,"--site requires a directory");
 for(const [name,dest] of Object.entries(routes)){
  const index=path.join(root,site,route,dest,"index.html");
  assert.ok(fs.existsSync(index),"Missing rendered "+index);
  const rendered=fs.readFileSync(index,"utf8");
  assert.ok(rendered.includes(schemas[name]),"Rendered "+name+" missing schema");
  assert.ok(rendered.length>=htmls[name].length*0.9,"Truncated rendered "+name);
 }
 const landing=fs.readFileSync(path.join(root,site,route,"index.html"),"utf8");
 for(const slug of Object.values(routes))assert.ok(landing.includes("./"+slug+"/"),"Landing lacks "+slug);
}
console.log("AI Teaching Lab contracts PASS",JSON.stringify(stats));
