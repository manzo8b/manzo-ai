import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import {
  toCopilotRequest, makeLocalSimulation, validateCopilotProposal, possiblyIdentifying
} from "./mission-adapter.mjs";
import { validateInput, validateModelOutput } from "../../product/mission-copilot/worker.mjs";
import { initializeCopilotPreview } from "./copilot-preview.mjs";

const here=dirname(fileURLToPath(import.meta.url));
function brief(override={}) {
  return {
    schema:"ai-teaching-lab-mission-v0.1", approval:false, topic:"Il ciclo dell'acqua",
    audience:"Secondaria di primo grado", minutes:30, mission:"image",
    objective:"Ordinare tre fasi del ciclo dell'acqua e spiegarne una relazione",
    ...override
  };
}
test("Adapter maps existing Mission Studio fields to private Worker, no extras", () => {
  const input=toCopilotRequest(brief({secret:"do not forward",teacherReview:"private"}));
  assert.deepEqual(input,{
    tema:"Il ciclo dell'acqua", destinatari:"secondaria_primo_grado",
    durataMinuti:30,tipoRisorsa:"immagini",
    obiettivo:"Ordinare tre fasi del ciclo dell'acqua e spiegarne una relazione"
  });
  assert.deepEqual(validateInput(input),input,"Worker must accept exact frontend schema");
});
test("All four resources and audiences use accepted Worker vocabulary", () => {
  const missions=["image","voice","video","verify"];
  const targets=["immagini","voce","video","verifica"];
  const audiences=["Scuola primaria","Secondaria di primo grado",
    "Secondaria di secondo grado","Formazione adulti"];
  for(let i=0;i<4;i++){
    const input=toCopilotRequest(brief({
      mission:missions[i],audience:audiences[i],minutes:[15,30,45,15][i]
    }));
    assert.equal(input.tipoRisorsa,targets[i]);
    assert.deepEqual(validateInput(input),input);
  }
});
test("Reject schema mismatch, approved drafts, unknown choices and long input", () => {
  for(const invalid of [
    brief({approval:true}),brief({schema:"mission-copilot-v0.1"}),
    brief({audience:"Bambino nominato"}),
    brief({minutes:60}),brief({mission:"unbounded"}),
    brief({objective:"x".repeat(351)}),brief({topic:"x"}),
    null, []
  ])assert.throws(()=>toCopilotRequest(invalid),Error);
});
test("Reject obvious identifying patterns; keep no claim of perfect data detection", () => {
  assert.equal(possiblyIdentifying("email: mario@example.com"),true);
  assert.equal(possiblyIdentifying("Cellulare +39 333 456 7890"),true);
  for(const topic of ["studente mario@example.com","tel. 3334567890"]){
    assert.throws(()=>toCopilotRequest(brief({topic})),/identificabili/);
  }
});
test("Offline simulation is NOT inference, NEVER approved and matches Worker proposal", () => {
  for(const mission of ["image","voice","video","verify"]){
    const simulation=makeLocalSimulation(brief({mission}));
    assert.equal(simulation.modelUsed,false);
    assert.equal(simulation.status,"simulazione_locale");
    assert.equal(simulation.teacherApproval,false);
    const clean=validateCopilotProposal(simulation,"simulazione_locale");
    assert.equal(clean.teacherApproval,false);
    assert.deepEqual(validateModelOutput(JSON.stringify(clean)),{
      obiettivo:clean.obiettivo,attivita:clean.attivita,
      criteriDiVerifica:clean.criteriDiVerifica,adattamenti:clean.adattamenti
    });
  }
});
test("Never accept forged approvals, wrong status or unstructured model replies",()=>{
  const valid=makeLocalSimulation(brief());
  for(const change of [
    {teacherApproval:true},{status:"bozza_non_approvata"},
    {obiettivo:"Too short"},{attivita:[]},{criteriDiVerifica:4},
    {schema:"other"}
  ])assert.throws(()=>validateCopilotProposal({...valid,...change},"simulazione_locale"));
});
function node(){
  return {
    hidden:true,disabled:false,value:"",textContent:"",handlers:{},children:[],
    addEventListener(e,fn){(this.handlers[e]??=[]).push(fn)},
    click(){for(const fn of (this.handlers.click??[]))fn({})},
    dispatchEvent(e){for(const fn of (this.handlers[e.type]??[]))fn(e)},
    replaceChildren(){this.children=[]},
    append(el){this.children.push(el)},
    focus(){this.focused=true}
  };
}
function setup(){
  const ids=[
    "copilot-preview","copilot-simulate","copilot-apply",
    "copilot-status","copilot-results","copilot-goal","copilot-activities",
    "copilot-criteria","copilot-access","topic","audience","objective","reset","restore"
  ];
  const map=Object.fromEntries(ids.map(id=>[id,node()]));
  let input=brief();
  const document={
    getElementById(id){return map[id]},
    querySelectorAll(){return []},
    createElement(){return node()}
  };
  const window={
    confirm(){return true},
    Event:class {constructor(type){this.type=type}}
  };
  initializeCopilotPreview({getBrief:()=>input,document,window});
  return { map, replaceBrief(next){input=next} };
}
test("Optional preview starts unapproved, hidden result, no action until explicit click",()=>{
  const {map}=setup();
  assert.equal(map["copilot-preview"].hidden,false);
  assert.equal(map["copilot-results"].hidden,true);
  assert.equal(map["copilot-apply"].disabled,true);
  assert.match(map["copilot-access"].textContent,/nessuna chiamata IA/);
});
test("Explicit simulation is visible with valid activities; human action modifies objective only",()=>{
  const {map}=setup();
  map["copilot-simulate"].click();
  assert.equal(map["copilot-results"].hidden,false);
  assert.equal(map["copilot-apply"].disabled,false);
  assert.equal(map["copilot-activities"].children.length,2);
  map["copilot-apply"].click();
  assert.match(map.objective.value,/Riconoscere e spiegare/);
  assert.equal(map["copilot-results"].hidden,true,"Any form change invalidates prior suggestion");
  assert.equal(map["copilot-apply"].disabled,true);
});
test("Changing a field invalidates stale suggestions before application",()=>{
  const {map,replaceBrief}=setup();
  map["copilot-simulate"].click();
  replaceBrief(brief({topic:"Argomento diverso"}));
  map["copilot-apply"].click();
  assert.equal(map.objective.value,"");
  assert.equal(map["copilot-apply"].disabled,true);
});
test("No secrets, external request, endpoint or token is present in public preview code",()=>{
  const controller=fs.readFileSync(resolve(here,"copilot-preview.mjs"),"utf8");
  const adapter=fs.readFileSync(resolve(here,"mission-adapter.mjs"),"utf8");
  const html=fs.readFileSync(resolve(here,"index.html"),"utf8");
  assert.doesNotMatch(controller+adapter,/\bfetch\s*\(|XMLHttpRequest|localStorage|sessionStorage|Bearer /);
  assert.match(html,/id="copilot-preview" hidden/);
  assert.match(html,/pilotQuery==="preview"/);
  assert.match(html,/import\("\.\/copilot-preview\.mjs"\)/);
  assert.doesNotMatch(html,/https:\/\/.*workers\.dev\/api/);
});
