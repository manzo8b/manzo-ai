#!/usr/bin/env node
/* DOM-level regression for the simplified HOME menu and decorative legacy shortcuts. */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const vm=require("node:vm");
const path=require("node:path");
const source=fs.readFileSync(path.resolve(__dirname,"../home-conversational.js"),"utf8");
function el(text=""){
 return {textContent:text,href:"/manzo-ai/it/",dataset:{maTitle:"Title",maDescription:"Description",maAction:"Apri"},
 attrs:{},handlers:{},setAttribute(k,v){this.attrs[k]=v},
 getAttribute(k){return k==="href"?this.href:this.attrs[k]},
 addEventListener(k,fn){this.handlers[k]=fn},focus(){this.focused=true},
 remove(){this.removed=true},closest(){return null},
 parentElement:{childElementCount:2,textContent:"notempty"}};
}
const shortcuts=[el("◈ Studio ↗"),el("◈ Vita quotidiana ↗"),el("◈ Lavoro")];
const oldLinks=[el("Studio"),el("Vita quotidiana")];
const nav=el("Short menu");
const goals=[0,1,2,3].map(i=>el("Goal "+i));
const title=el(),summary=el(),action=el(),announce=el(),search=el();
search.value="";
const rail={classList:{add(s){this.label=s}},querySelector(){return null},
 querySelectorAll(){return oldLinks},append(node){this.moved=node}};
const hero={querySelectorAll(){return shortcuts}};
const root={closest(){return hero},querySelectorAll(){return goals},
 querySelector(k){return ({
 "[data-ma-discovery-title]":title,
 "[data-ma-discovery-summary]":summary,
 "[data-ma-discovery-action]":action,
 "[data-ma-discovery-live]":announce,
 '[data-ma-home-primary-nav="v2"]':nav
 })[k]||null}};
const document={querySelector(k){return k==='[data-ma-home-discovery="v1"]'?root:
 k===".rail"?rail:k===".home-hero .searchbox input"?search:null}};
vm.runInNewContext(source,{document},{timeout:1000});
assert.equal(rail.moved,nav,"Curated navigation was not promoted");
assert.equal(rail.classList.label,"ma-home-rail-curated");
assert.ok(oldLinks.every(x=>x.removed),"Old grouped rail links remain");
assert.ok(shortcuts.every(x=>x.removed),"Decorated shortcut labels were not normalized");
assert.equal(goals[0].attrs["aria-current"],"true");
console.log("PASS HOME: curated menu promoted; 14+ legacy entries and redundant decorated shortcuts removed");
