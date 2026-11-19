"use strict";
/* Centroni City — AI Product Builder. Everything runs locally in the browser.
   No submissions, tracking, accounts, database, or user-generated publication.
   The civic demo and all its cases are explicitly simulated. */
(() => {
  const root=document.querySelector('[data-ma-centroni="course-v1"]');
  if(!root) return;
  const $=(q)=>root.querySelector(q);
  const $$=(q)=>Array.from(root.querySelectorAll(q));

  const progress=()=>{
    const count=$$(".ps-read-check:checked").length;
    const el=$("#cc-progress");
    if(el) el.textContent=count+" di 6 letture completate (solo durante questa visita)";
  };
  $$(".ps-read-check").forEach(x=>x.addEventListener("change",progress));
  progress();
  function openReading(id){
    const section=document.getElementById(id);
    if(section){const details=section.querySelector("details");if(details)details.open=true;}
  }
  $$("[data-open-reading]").forEach(a=>a.addEventListener("click",()=>openReading(a.dataset.openReading)));
  if(/^#cc-lettura-[1-6]$/.test(location.hash)) openReading(location.hash.slice(1));

  const fields=["project","problem","target","input","process","output","limits","measure"];
  const value=(id)=>($("#cc-"+id)?.value||"").trim();
  const blueprint=()=>[
    "AI PRODUCT BUILDER — BLUEPRINT DIDATTICO",
    "PROGETTO: "+(value("project")||"Centroni City"),
    "PROBLEMA: "+(value("problem")||"[DA DEFINIRE]"),
    "DESTINATARI: "+(value("target")||"[DA DEFINIRE]"),
    "INPUT: "+(value("input")||"[DA DEFINIRE]"),
    "PROCESSO / REGOLE: "+(value("process")||"[DA DEFINIRE]"),
    "OUTPUT: "+(value("output")||"[DA DEFINIRE]"),
    "VINCOLI E RISCHI: "+(value("limits")||"[DA DEFINIRE]"),
    "METRICA DI UTILITÀ: "+(value("measure")||"[DA DEFINIRE]"),
    "",
    "Nota di progetto: non inserire segnalazioni identificative, dati personali o accuse nel prototipo. La demo non è uno sportello istituzionale."
  ].join("\n");
  async function copyText(content,feedback){
    try{
      await navigator.clipboard.writeText(content);
      if(feedback)feedback.textContent="Testo copiato. Contiene solo ciò che hai scritto e informazioni didattiche.";
    }catch(e){
      if(feedback)feedback.textContent="Copia non disponibile nel browser. Puoi selezionare i contenuti e copiarli manualmente.";
    }
  }
  $("#cc-copy-blueprint")?.addEventListener("click",()=>copyText(blueprint(),$("#cc-studio-status")));
  $("#cc-copy-coach")?.addEventListener("click",()=>copyText(
    "Sei un tutor socratico di progettazione digitale, non il costruttore che esegue subito.\n"+
    "Il mio progetto è: "+(value("project")||"Centroni City")+".\n"+
    "Poni una sola domanda alla volta per aiutarmi a distinguere bisogno, utenti, input, processo, output, vincoli e test.\n"+
    "Non inventare dati o servizi pubblici. Non generare codice finché non ho definito il blueprint.\n"+
    "Quando hai abbastanza informazioni, individua tre casi limite e spiegami come collaudarli.\n"+
    "Il prodotto non deve ricevere denunce formali, accuse o dati personali in questa V1.",
    $("#cc-studio-status")
  ));

  const official="https://www.comune.roma.it/web/it/suggerimenti-segnalazioni-e-reclami-urp-uffici-relazioni-con-il-pubblico.page";
  const municipality="https://www.comune.roma.it/web/it/i-quartieri-di-roma-mun7.page";
  const committee="https://www.comune.roma.it/web/it/attivita-progetto.page?contentId=PRG1506858";
  const views={
    info:{
      title:"Informazioni e fonti",
      lead:"Una buona scheda civica distingue i dati documentati dalle informazioni che richiedono un controllo.",
      items:[
        {title:"Centroni nel Municipio VII",desc:"Informazione istituzionale: Roma Capitale include Centroni tra i quartieri del Municipio VII.",href:municipality,label:"Consulta la fonte ufficiale"},
        {title:"Avviso simulato — lavori in quartiere",desc:"ESEMPIO FITTIZIO, non pubblicabile: non abbiamo una comunicazione verificata, una data o un riferimento ufficiale. Stato: IN VERIFICA.",href:null,label:""}
      ]},
    servizi:{
      title:"Servizi e partecipazione",
      lead:"La piattaforma deve rendere i percorsi comprensibili e collegare i cittadini alle informazioni ufficiali.",
      items:[
        {title:"Suggerimenti, segnalazioni e reclami",desc:"Guida ufficiale ai canali di relazione con Roma Capitale, incluso ChiamaRoma 060606.",href:official,label:"Vai al servizio istituzionale"},
        {title:"Comitati di quartiere",desc:"Roma Capitale descrive i comitati del Municipio VII, fra cui Centroni–Villa Senni–Valle Marciana.",href:committee,label:"Consulta l'elenco istituzionale"}
      ]},
    segnalazioni:{
      title:"Dove indirizzare una segnalazione?",
      lead:"La demo non raccoglie né invia dati. Scegli una situazione fittizia per conoscere il percorso appropriato.",
      items:[]
    }
  };
  const pathData={
    guasto:{title:"Guasto o disservizio urbano",text:"Consulta i canali ufficiali di Roma Capitale per individuare quello competente. Non considerare il problema preso in carico finché non ricevi conferma dal servizio istituzionale.",href:official,link:"Apri la guida ufficiale"},
    reclamo:{title:"Reclamo relativo a un servizio",text:"Un reclamo segue le procedure dell'ente o dell'azienda responsabile. Centroni City può aiutare a trovare i riferimenti, ma non invia il reclamo.",href:official,link:"Consulta i canali di Roma Capitale"},
    denuncia:{title:"Possibile reato o denuncia formale",text:"Non inviare accuse, nominativi o prove tramite questa demo. Per una denuncia rivolgiti direttamente alle autorità competenti secondo le procedure applicabili. Centroni City non è un ufficio di polizia e non protocolla denunce.",href:null,link:""},
    emergenza:{title:"Situazione di pericolo immediato",text:"Non usare questo portale per chiedere soccorso. In Italia, in caso di emergenza, contatta il numero unico 112 e segui le indicazioni degli operatori.",href:null,link:""}
  };
  function buildElement(tag,content,klass){
    const e=document.createElement(tag);
    if(klass)e.className=klass;
    if(content!==undefined)e.textContent=content;
    return e;
  }
  function renderPath(key){
    $$(".cc-path-buttons button").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.path===key)));
    const target=$("#cc-path-output");
    if(!target)return;
    target.replaceChildren();
    const item=pathData[key]||pathData.guasto;
    target.append(buildElement("strong",item.title),buildElement("p",item.text));
    if(item.href){
      const link=buildElement("a",item.link);
      link.href=item.href;link.target="_blank";link.rel="noopener noreferrer";
      target.append(link);
    }
  }
  function renderTab(name){
    const panel=$("#cc-sim-content");
    const data=views[name];
    if(!panel||!data)return;
    $$(".cc-sim-tabs button").forEach(b=>{
      const active=b.dataset.tab===name;
      b.setAttribute("aria-selected",String(active));
      b.tabIndex=active?0:-1;
    });
    panel.replaceChildren();
    panel.append(buildElement("h3",data.title),buildElement("p",data.lead));
    if(name==="segnalazioni"){
      const controls=buildElement("div",undefined,"cc-path-buttons");
      controls.setAttribute("role","group");
      controls.setAttribute("aria-label","Tipologie di richiesta simulata");
      for(const [k,label] of [["guasto","Guasto"],["reclamo","Reclamo"],["denuncia","Denuncia"],["emergenza","Emergenza"]]){
        const b=buildElement("button",label);b.type="button";b.dataset.path=k;
        b.addEventListener("click",()=>renderPath(k));
        controls.append(b);
      }
      panel.append(controls);
      const output=buildElement("div",undefined,"cc-path-output");
      output.id="cc-path-output";output.setAttribute("role","status");output.setAttribute("aria-live","polite");
      panel.append(output);
      renderPath("guasto");
    }else{
      const cards=buildElement("div",undefined,"cc-sim-cards");
      data.items.forEach(item=>{
        const c=buildElement("article",undefined,"cc-sim-box");
        c.append(buildElement("strong",item.title),buildElement("small",item.desc));
        if(item.href){
          const link=buildElement("a",item.label);
          link.href=item.href;link.target="_blank";link.rel="noopener noreferrer";
          c.append(link);
        }
        cards.append(c);
      });
      panel.append(cards);
    }
    panel.append(buildElement("p","SIMULAZIONE FORMATIVA · Nessun dato viene raccolto o trasmesso; non è un servizio istituzionale.","cc-sim-disclaimer"));
  }
  $$(".cc-sim-tabs button").forEach(button=>button.addEventListener("click",()=>renderTab(button.dataset.tab)));
  renderTab("info");

  const checks=$$(".cc-check-list input[type=checkbox]");
  const checkStatus=$("#cc-check-status");
  function updateChecks(){
    const total=checks.filter(x=>x.checked).length;
    if(checkStatus)checkStatus.textContent=total+" di "+checks.length+" verifiche di progetto dichiarate come completate. Questa checklist non certifica la conformità del sito.";
  }
  checks.forEach(x=>x.addEventListener("change",updateChecks));
  updateChecks();

  const questionsEl=$("#cc-quiz-data"),rootQuiz=$("#cc-quiz-root");
  if(questionsEl&&rootQuiz){
    let questions=[];
    try{questions=JSON.parse(questionsEl.textContent);}catch(e){}
    if(questions.length){
      const form=buildElement("form");form.noValidate=true;
      questions.forEach((item,index)=>{
        const field=buildElement("fieldset",undefined,"cc-quiz-field");
        const legend=buildElement("legend",(index+1)+". "+item.q);
        field.append(legend);
        item.options.forEach((option,j)=>{
          const label=buildElement("label");
          const inp=document.createElement("input");
          inp.type="radio";inp.name="cc-q-"+index;inp.value=String(j);
          label.append(inp,document.createTextNode(option));
          field.append(label);
        });
        field.append(buildElement("p",undefined,"cc-quiz-explain"));
        form.append(field);
      });
      const button=buildElement("button","Correggi e leggi il feedback","cc-btn");
      button.type="submit";
      const output=buildElement("p",undefined,"cc-quiz-status");
      output.id="cc-quiz-result";output.hidden=true;output.setAttribute("role","status");output.setAttribute("aria-live","polite");
      form.append(button,output);
      form.addEventListener("submit",e=>{
        e.preventDefault();
        let correct=0,answered=0;
        form.querySelectorAll(".cc-quiz-field").forEach((field,index)=>{
          const picked=field.querySelector("input:checked");
          if(picked)answered++;
          const ok=!!picked&&Number(picked.value)===questions[index].answer;
          if(ok)correct++;
          field.dataset.reviewed="1";field.dataset.correct=ok?"1":"0";
          field.querySelector(".cc-quiz-explain").textContent=(ok?"Corretto. ":"Da rivedere. ")+questions[index].why+" Risposta attesa: "+questions[index].options[questions[index].answer]+".";
        });
        output.hidden=false;
        output.textContent="Hai risposto a "+answered+" domande su "+questions.length+". Risposte corrette: "+correct+"/"+questions.length+". Leggi le spiegazioni sotto ogni quesito.";
      });
      rootQuiz.replaceChildren(form);
    }
  }
})();
