#!/usr/bin/env node
/* DOM-less behavioral test: prove goals update REAL navigation, not chatbot answers. */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const vm=require("node:vm");
const path=require("node:path");
const source=fs.readFileSync(path.resolve(__dirname,"../home-conversational.js"),"utf8");
const pathFor=i=>"/manzo-ai/it/learn/goal-"+i+"/";
function element(extra={}){
 return Object.assign({
  textContent:"",dataset:{},attrs:{},handlers:{},href:"",
  setAttribute(k,v){this.attrs[k]=v},
  getAttribute(k){return k==="href"?this.href:this.attrs[k]},
  addEventListener(k,v){this.handlers[k]=v},
  focus(){this.focused=true},
 },extra);
}
const choices=[0,1,2].map(i=>element({
 dataset:{maTitle:"Title "+i,maDescription:"Description "+i,maAction:"Open "+i},
 href:pathFor(i),
}));
const title=element(),summary=element(),action=element(),announce=element(),search=element({value:""});
const root={
 closest(){return null},
 querySelectorAll(s){return s==="[data-ma-intent]"?choices:[]},
 querySelector(s){return ({
  "[data-ma-discovery-title]":title,
  "[data-ma-discovery-summary]":summary,
  "[data-ma-discovery-action]":action,
  "[data-ma-discovery-live]":announce
 })[s]||null}
};
const context={
 document:{querySelector(s){return s==='[data-ma-home-discovery="v1"]'?root:
  s===".home-hero .searchbox input"?search:null}},
};
vm.runInNewContext(source,context,{timeout:1000});
assert.equal(title.textContent,"Title 0");
assert.equal(action.href,pathFor(0));
assert.equal(choices[0].attrs["aria-current"],"true");
assert.equal(choices[1].attrs["aria-current"],"false");
let prevented=false;
choices[2].handlers.click({
 button:0,metaKey:false,ctrlKey:false,shiftKey:false,altKey:false,
 preventDefault(){prevented=true}
});
assert.equal(prevented,true);
assert.equal(title.textContent,"Title 2");
assert.equal(summary.textContent,"Description 2");
assert.equal(action.href,pathFor(2));
assert.equal(choices[2].attrs["aria-current"],"true");
assert.equal(choices[0].attrs["aria-current"],"false");
assert.equal(action.focused,true);
assert.ok(announce.textContent.includes("Title 2"));
search.value="verificare una fonte";
search.handlers.input();
assert.equal(action.href,pathFor(2),"Search should map to available verification learning resources");
let modifiedClick=false;
choices[1].handlers.click({button:0,metaKey:true,ctrlKey:false,shiftKey:false,altKey:false,preventDefault(){modifiedClick=true}});
assert.equal(modifiedClick,false,"Meta-click must preserve native link opening");
assert.equal(action.href,pathFor(2),"Modified click must not overwrite prior selected result");
assert.ok(!/\bfetch\s*\(|XMLHttpRequest|sendBeacon|localStorage|sessionStorage/.test(source),
  "Discovery must not transmit or store user input");
console.log("PASS MANZO AI guided home discovery: initial, selection, search mapping, native link behavior");
