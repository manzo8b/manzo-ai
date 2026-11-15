/* MANZO AI · Product Preview. Real local utilities, no AI calls, network, storage or tracking. */
(()=>{
"use strict";
const root=document.querySelector("[data-product-preview]");if(!root)return;
const words=JSON.parse(document.getElementById("product-dictionary").textContent);
const lang=root.getAttribute("lang")||"it";
const $=id=>document.getElementById(id);
const announce=$("announce");
const clean=v=>String(v||"").trim();
const valueOrEmpty=v=>clean(v)||words.empty;
let lastBrief={};
function updateBrief(){
 const option=$("project-type");
 lastBrief={
  product:"MANZO AI Studio · client-side brief preview",
  locale:lang,
  type:option.options[option.selectedIndex].text,
  goal:clean($("project-goal").value)||null,
  audience:clean($("project-audience").value)||null,
  constraints:clean($("project-constraints").value)||null,
  workflow:"Draft requires human validation; no website or AI task was executed.",
  dataPolicy:"Generated only in browser memory; not transmitted"
 };
 $("brief-json").textContent=JSON.stringify(lastBrief,null,2);
 announce.textContent=words.previewDesc;
}
["project-type","project-goal","project-audience","project-constraints"].forEach(id=>$(id).addEventListener("change",updateBrief));
$("project-update").addEventListener("click",updateBrief);
$("project-export").addEventListener("click",()=>{
 updateBrief();
 const blob=new Blob([JSON.stringify(lastBrief,null,2)+"\n"],{type:"application/json;charset=utf-8"});
 const url=URL.createObjectURL(blob);
 const anchor=document.createElement("a");
 anchor.href=url;anchor.download="manzo-ai-project-brief.json";anchor.rel="noopener";
 anchor.click();
 URL.revokeObjectURL(url);
});
updateBrief();
function candidateStatements(raw){
 const normalized=clean(raw).slice(0,6000).replace(/\r/g,"");
 // Deliberately heuristic: not a fact checker and not a hallucination detector.
 // Respect ordinary decimal separators while splitting on sentence punctuation.
 const statements=normalized.split(/(?:[!?;]\s*|\n+|\.(?!\d)\s+)/g).map(s=>s.trim()).filter(s=>s.length>=12);
 const patterns=[
  /\d(?:[\d.,%€$ ]*)/u,
  /\b(?:legge|normativa|regolamento|obblig|vietat|decreto|sanzion|direttiva|article|law|regulation|mandatory|required|prohibit|compliance|ley|normativa|reglamento|obligatori|prohib|artículo|articolo)\w*\b/iu,
  /\b(?:sempre|mai|tutti|nessuno|garantit|certament|always|never|every|all companies|guaranteed|todos|nunca|siempre|garantiz)\w*\b/iu
 ];
 const seen=new Set();
 return statements.filter(s=>{
  if(!patterns.some(p=>p.test(s)))return false;
  const key=s.toLocaleLowerCase();
  if(seen.has(key))return false;seen.add(key);return true;
 }).slice(0,16);
}
$("inspect-text").addEventListener("click",()=>{
 const text=clean($("inspect-input").value);
 const host=$("claim-list");host.replaceChildren();
 const claims=text?candidateStatements(text):[];
 $("claim-count").textContent=claims.length+" · "+words.claimCount;
 if(!text||!claims.length){
  const p=document.createElement("p");p.textContent=text?words.noClaims:words.noInput;
  p.className="notice";host.append(p);return;
 }
 claims.forEach((claim,index)=>{
  const article=document.createElement("article");article.className="claim";
  const badge=document.createElement("span");badge.textContent="#"+String(index+1).padStart(2,"0")+" · "+words.verified;
  const p=document.createElement("p");p.textContent=claim;
  article.append(badge,p);host.append(article);
 });
});
const seats=$("team-seats"),seatNumber=$("team-seats-label");
const org=$("org-type"),mod=$("team-module"),summary=$("team-summary");
function updateTeam(){
 seatNumber.textContent=seats.value;
 const selectedOrg=org.options[org.selectedIndex].text;
 const selectedMod=mod.options[mod.selectedIndex].text;
 summary.textContent=selectedOrg+" · "+seats.value+" "+(lang==="it"?"utenti":lang==="es"?"usuarios":"users")+" · "+selectedMod;
}
seats.addEventListener("input",updateTeam);
org.addEventListener("change",updateTeam);
mod.addEventListener("change",updateTeam);
updateTeam();
$("copy-proposal").addEventListener("click",async()=>{
 const text=words.licenseTitle+" — MANZO AI Learning\n"+summary.textContent+"\n"+words.licenseDisclaimer;
 try{if(!navigator.clipboard||!navigator.clipboard.writeText)throw Error("clipboard unavailable");await navigator.clipboard.writeText(text);announce.textContent=words.copied;}
 catch(e){announce.textContent=words.copyFail;}
});
})();