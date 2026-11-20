"use strict";
/* MANZO AI — Governing Autonomy · Mission Control learning simulator
 * Entirely client-side, synthetic data only. No APIs, file uploads, accounts,
 * email sending, payments, persistence, storage or external execution.
 */
(() => {
  const scope=document.querySelector('[data-ga-course="v1"]');
  if(!scope)return;
  const $=selector=>scope.querySelector(selector);
  const $$=selector=>Array.from(scope.querySelectorAll(selector));
  let data={};
  try{data=JSON.parse($("#ga-data")?.textContent||"{}");}catch(_err){return;}
  const t=data.ui||{}, actions=data.actions||[], incidents=data.incidents||[], questions=data.quiz||[];
  const make=(tag,txt,klass)=>{
    const el=document.createElement(tag);
    if(txt!==undefined && txt!==null)el.textContent=txt;
    if(klass)el.className=klass;
    return el;
  };
  const feedback=(selector,value,status)=>{
    const el=$(selector);if(!el)return;
    el.textContent=value;el.dataset.status=status||"info";
  };
  const settings=(id)=>$("#ga-"+id);
  const actionChoices=[], incidentChoices=[];
  let actionsChecked=false,limitsChecked=false,incidentsChecked=false;
  let actionCorrect=0,incidentCorrect=0,limitsValid=false,dangerous=false;

  function readingProgress(){
    feedback("#ga-reading-progress",$$(".ps-read-check:checked").length+" / 6 "+t.progress);
  }
  $$(".ps-read-check").forEach(i=>i.addEventListener("change",readingProgress));
  readingProgress();
  function openReading(id){const section=document.getElementById(id);const details=section?.querySelector("details");if(details)details.open=true;}
  $$("[data-open-reading]").forEach(a=>a.addEventListener("click",()=>openReading(a.dataset.openReading)));
  if(/^#ga-reading-[1-6]$/.test(location.hash))openReading(location.hash.slice(1));

  const actionsTarget=$("#ga-actions");
  if(actionsTarget){
    actions.forEach((entry,i)=>{
      const row=make("div",null,"ga-action-row"),label=make("label",entry.label);
      const select=make("select");
      select.id="ga-action-"+i;
      select.setAttribute("aria-label",entry.label);
      t.choices.forEach(([value,text])=>{const option=make("option",text);option.value=value;select.append(option);});
      const why=make("p",null,"ga-feedback");
      why.setAttribute("aria-live","polite");
      row.append(label,select,why);actionsTarget.append(row);
      actionChoices.push(select);
      select.addEventListener("change",()=>{actionsChecked=false;recompute();});
    });
  }
  $("#ga-actions-check")?.addEventListener("click",()=>{
    actionCorrect=0;dangerous=false;actionsChecked=true;
    actionChoices.forEach((select,i)=>{
      const item=actions[i];
      const ok=select.value===item.expected;
      if(ok)actionCorrect++;
      if(select.value==="allow"&&["review","block"].includes(item.expected))dangerous=true;
      const why=select.parentElement.querySelector(".ga-feedback");
      why.dataset.status=ok?"success":"warning";why.textContent=(ok?t.incidentGood:t.incidentBad)+": "+item.why;
    });
    feedback("#ga-actions-status",t.actionCorrect+": "+actionCorrect+" / "+actions.length+". "+(dangerous?t.actionWarning:""),dangerous?"stop":"info");
    recompute();
  });

  const numericNames=["minute","records","budget","messages"];
  const recomputeLimits=()=>{
    limitsChecked=false;limitsValid=false;recompute();
  };
  numericNames.forEach(n=>settings(n)?.addEventListener("input",recomputeLimits));
  settings("owner")?.addEventListener("input",recomputeLimits);
  settings("enforcer")?.addEventListener("change",recomputeLimits);
  $("#ga-limits-check")?.addEventListener("click",()=>{
    const values=numericNames.map(n=>Number(settings(n)?.value));
    const validInput=numericNames.every((n,i)=>{
      const input=settings(n);
      return input && input.value.trim()!=="" && Number.isFinite(values[i]) && values[i]>=0 && values[i]<=1000000
        && (n==="minute"||n==="records"?values[i]>0:true);
    });
    limitsChecked=true;
    limitsValid=Boolean(validInput&&settings("owner")?.value.trim()&&settings("enforcer")?.value==="gateway");
    feedback("#ga-limits-status",limitsValid?t.limitGood:t.limitBad,limitsValid?"success":"stop");
    recompute();
  });

  const incidentsTarget=$("#ga-incidents");
  if(incidentsTarget){
    incidents.forEach((entry,i)=>{
      const row=make("div",null,"ga-incident-card");
      const title=make("h4",(i+1)+". "+entry.title),lead=make("p",entry.setup);
      const select=make("select");
      select.id="ga-incident-"+i;select.setAttribute("aria-label",entry.title);
      const blank=make("option",t.incidentSelect);blank.value="";select.append(blank);
      entry.options.forEach((option,j)=>{const o=make("option",option);o.value=String(j);select.append(o);});
      const msg=make("p",null,"ga-feedback");msg.setAttribute("aria-live","polite");
      row.append(title,lead,select,msg);incidentsTarget.append(row);
      incidentChoices.push(select);
      select.addEventListener("change",()=>{incidentsChecked=false;recompute();});
    });
  }
  $("#ga-incidents-check")?.addEventListener("click",()=>{
    incidentCorrect=0;incidentsChecked=true;
    incidentChoices.forEach((select,i)=>{
      const match=select.value!==""&&Number(select.value)===incidents[i].answer;
      if(match)incidentCorrect++;
      const explanation=select.parentElement.querySelector(".ga-feedback");
      explanation.textContent=(match?t.incidentGood:t.incidentBad)+": "+incidents[i].why;
      explanation.dataset.status=match?"success":"warning";
    });
    feedback("#ga-incidents-status",incidentCorrect+" / "+incidents.length+" "+t.incidentGood.toLowerCase(),incidentCorrect===incidents.length?"success":"warning");
    recompute();
  });

  const rubricTarget=$("#ga-rubric");
  if(rubricTarget){
    t.rubricCriteria.forEach((criterion,i)=>{
      const row=make("div",null,"ga-rubric-row");
      const label=make("label",criterion);label.htmlFor="ga-rubric-"+i;
      const select=make("select");select.id="ga-rubric-"+i;
      t.rubricOptions.forEach(([value,text])=>{const option=make("option",text);option.value=value;select.append(option);});
      row.append(label,select);rubricTarget.append(row);
      select.addEventListener("change",recompute);
    });
  }

  function computeRelease(){
    const rubric=$$("#ga-rubric select").map(x=>x.value);
    const filled=rubric.length===4&&rubric.every(x=>x!=="");
    const score=filled?rubric.reduce((sum,value)=>sum+Number(value),0):0;
    const critical=actionsChecked&&dangerous
       ||limitsChecked&&!limitsValid
       ||incidentsChecked&&incidentCorrect<incidents.length
       ||filled&&rubric.some(x=>x==="0");
    if(critical)return{type:"stop",text:t.stop,score};
    if(!filled||!actionsChecked||!limitsChecked||!incidentsChecked||actionCorrect<actions.length||!limitsValid||incidentCorrect<incidents.length||score<8){
      return{type:"revise",text:t.revise,score};
    }
    return{type:"go",text:t.go,score};
  }
  function recompute(){
    const current=$("#ga-release");
    if(current){current.hidden=true;current.textContent="";}
  }
  $("#ga-release-check")?.addEventListener("click",()=>{
    const result=computeRelease();
    const el=$("#ga-release");
    if(el){el.hidden=false;el.dataset.status=result.type;el.textContent=result.text+" · "+result.score+"/8. "+t.releaseDesc;}
  });

  $("#ga-copy")?.addEventListener("click",async()=>{
    const rubric=$$("#ga-rubric select").map(x=>x.value||"—");
    const lines=[
      "MANZO AI · "+t.boundaryTitle,
      "",
      t.stations[0],
      ...actions.map((action,i)=>action.label+" → "+(actionChoices[i]?.selectedOptions[0]?.textContent||"—")),
      "",
      t.stations[1],
      ...t.limits.map(([id,label,unit])=>label+": "+(settings(id)?.value||"—")+" "+unit),
      t.enforcement+": "+(settings("enforcer")?.selectedOptions[0]?.textContent||"—"),
      t.owner+": "+(settings("owner")?.value||"—"),
      "",
      t.stations[2],
      ...incidents.map((entry,i)=>entry.title+" → "+(incidentChoices[i]?.selectedOptions[0]?.textContent||"—")),
      "",
      t.stations[3],
      ...t.rubricCriteria.map((name,i)=>name+": "+rubric[i]),
      t.releaseCheck+": "+computeRelease().text,
      t.releaseDesc
    ];
    try{await navigator.clipboard.writeText(lines.join("\n"));feedback("#ga-copy-status",t.copyOk,"success");}
    catch(_){feedback("#ga-copy-status",t.copyFail,"warning");}
  });

  const boardInputs=$$(".ga-cross-cell input");
  boardInputs.forEach((input,index)=>{
    input.addEventListener("input",()=>{
      input.value=input.value.normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[^A-Za-z]/g,"").slice(0,1).toUpperCase();
      if(input.value&&index<boardInputs.length-1)boardInputs[index+1].focus();
    });
    input.addEventListener("keydown",event=>{
      if(event.key==="Backspace"&&!input.value&&index>0)boardInputs[index-1].focus();
    });
  });
  $("#ga-cross-check")?.addEventListener("click",()=>{
    let n=0;boardInputs.forEach(cell=>{
      const valid=cell.value===cell.dataset.answer;
      if(valid)n++;
      cell.parentElement.dataset.valid=valid?"1":"0";
    });
    feedback("#ga-cross-status",n+"/"+boardInputs.length+" "+t.crossCells+". "+(n===boardInputs.length?t.crossGood:t.crossBad),n===boardInputs.length?"success":"warning");
  });
  $("#ga-cross-reset")?.addEventListener("click",()=>{
    boardInputs.forEach(input=>{input.value="";delete input.parentElement.dataset.valid;});
    feedback("#ga-cross-status",t.crossCleared,"info");
    boardInputs[0]?.focus();
  });

  const quizHost=$("#ga-quiz");
  if(quizHost&&questions.length===10){
    const form=make("form");form.noValidate=true;
    questions.forEach((q,i)=>{
      const field=make("fieldset",null,"ga-question");
      const legend=make("legend",(i+1)+". "+q.q);field.append(legend);
      q.options.forEach((option,j)=>{
        const label=make("label");const radio=make("input");
        radio.type="radio";radio.name="ga-q-"+i;radio.value=String(j);
        label.append(radio,document.createTextNode(option));field.append(label);
      });
      const explanation=make("p",null,"ga-why");
      field.append(explanation);form.append(field);
    });
    const submit=make("button",t.quizSubmit,"ga-button");submit.type="submit";
    const outcome=make("p",null,"ga-status");outcome.hidden=true;outcome.setAttribute("role","status");outcome.setAttribute("aria-live","polite");
    form.append(submit,outcome);
    form.addEventListener("submit",e=>{
      e.preventDefault();let right=0,answered=0;
      form.querySelectorAll("fieldset").forEach((field,i)=>{
        const selected=field.querySelector('input[type="radio"]:checked');
        const good=!!selected&&Number(selected.value)===questions[i].answer;
        if(selected)answered++;if(good)right++;
        field.dataset.reviewed="1";field.dataset.correct=good?"1":"0";
        field.querySelector(".ga-why").textContent=(good?t.quizCorrect:t.quizReview)+". "+questions[i].why+" "+t.quizExpected+": "+questions[i].options[questions[i].answer]+".";
      });
      outcome.hidden=false;outcome.textContent=t.quizAnswered+": "+answered+"/10 · "+t.quizResult+": "+right+"/10. "+t.quizEnd;
    });
    quizHost.replaceChildren(form);
  }
})();
