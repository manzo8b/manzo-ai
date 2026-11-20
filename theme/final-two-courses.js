"use strict";
/* MANZO AI | Last two Academy courses
 * Interactive, trilingual, synthetic exercises without external API requests,
 * local storage, remote submissions or collection of personal information.
 */
(() => {
  const root=document.querySelector('[data-ma-final-course]');
  if(!root)return;
  const $=(sel)=>root.querySelector(sel);
  const $$=(sel)=>Array.from(root.querySelectorAll(sel));
  let data={};
  try{data=JSON.parse($("#ft-payload")?.textContent||"{}");}
  catch(_error){return;}
  const kind=data.kind,ui=data.ui||{},questions=data.quiz||[];
  const el=(tag,text,className)=>{
    const x=document.createElement(tag);
    if(text!==undefined&&text!==null)x.textContent=text;
    if(className)x.className=className;
    return x;
  };
  const status=(id,message,tone)=>{
    const x=$(id);if(!x)return;
    x.textContent=message;
    x.dataset.tone=tone||"info";
  };
  let evaluated=false;
  function invalidate(){
    const x=$("#ft-decision");
    if(x){x.hidden=true;x.textContent="";}
    evaluated=false;
  }

  function updateReadings(){
    status("#ft-progress",$$(".ps-read-check:checked").length+" / 6 "+ui.progress,"info");
  }
  function openReading(id){
    const panel=document.getElementById(id);
    const details=panel?.querySelector("details");
    if(details)details.open=true;
  }
  $$(".ps-read-check").forEach(input=>input.addEventListener("change",updateReadings));
  $$("[data-open-reading]").forEach(anchor=>anchor.addEventListener("click",()=>openReading(anchor.dataset.openReading)));
  if(/^#ft-reading-[1-6]$/.test(location.hash))openReading(location.hash.slice(1));
  updateReadings();

  function setExplanation(select,match,why){
    const row=select.closest(".ft-lab-row");
    const explain=row?.querySelector(".ft-explanation");
    if(explain){
      explain.textContent=(match?ui.correct:ui.review)+". "+why;
      explain.dataset.tone=match?"success":"warning";
    }
  }
  const toolSelectors=$$(".ft-tool-choice"),caseSelectors=$$(".ft-case-choice");
  const taskSelectors=$$(".ft-task-choice"),workSelectors=$$(".ft-workslop-choice");
  const rubricSelectors=$$(".ft-rubric-choice");
  const userFields=$$(".ft-station input, .ft-station textarea");
  [...toolSelectors,...caseSelectors,...taskSelectors,...workSelectors,
   ...rubricSelectors,...userFields].forEach(input=>{
    input.addEventListener("change",invalidate);
    input.addEventListener("input",invalidate);
  });

  const getVal=id=>($("#"+id)?.value||"").trim();
  const scoreChoice=(selector,answer,why)=>{
    const match=selector.value!==""&&selector.value===String(answer);
    setExplanation(selector,match,why);
    return match;
  };
  const allFilled=(selectors)=>selectors.every(select=>select.value!=="");
  const allInputsFilled=(selectors)=>selectors.every(input=>input.value.trim().length>0);
  function assessCompliance(){
    let tools=0,cases=0;
    toolSelectors.forEach(select=>{
      const correct=select.value==="yes";
      if(correct)tools++;
      setExplanation(select,correct,ui.toolFeedback);
    });
    caseSelectors.forEach((select,i)=>{
      const entry=ui.cases[i];
      if(scoreChoice(select,entry[3],entry[4]))cases++;
    });
    const owner=getVal("ft-owner");
    const metrics=$$(".ft-metric-input");
    const triggers=$$(".ft-trigger-input");
    const full=toolSelectors.length===8&&caseSelectors.length===4&&
       allFilled(toolSelectors)&&allFilled(caseSelectors)&&owner.length>=3&&
       metrics.length===9&&triggers.length===9&&allInputsFilled(metrics)&&allInputsFilled(triggers);
    const critical=owner.length<3||
       (caseSelectors[0]?.value!==""&&caseSelectors[0]?.value!==String(ui.cases[0][3]));
    return {count:tools+cases,total:12,full,critical};
  }
  function assessAugmented(){
    let tasks=0,checks=0;let critical=false;
    taskSelectors.forEach((select,i)=>{
      const entry=ui.tasks[i],match=select.value===entry[1];
      if(match)tasks++;
      setExplanation(select,match,entry[2]);
      if((entry[1]==="human"||entry[1]==="verify")&&select.value==="delegate")critical=true;
    });
    workSelectors.forEach((select,i)=>{
      const item=ui.checkQuestions[i];
      const match=scoreChoice(select,item[2],item[3]);
      if(match)checks++;
    });
    const rules=Array.from({length:5},(_,i)=>getVal("ft-rule-"+i));
    const humanCriteria=getVal("ft-prior"),rewrite=getVal("ft-rewrite"),
       protectedData=getVal("ft-data-rule");
    if(rules[4].length<12)critical=true;
    if(workSelectors[1]?.value!==""&&workSelectors[1]?.value!==String(ui.checkQuestions[1][2]))critical=true;
    const full=taskSelectors.length===8&&workSelectors.length===4&&
       allFilled(taskSelectors)&&allFilled(workSelectors)&&
       rules.every(x=>x.length>=12)&&humanCriteria.length>=24&&rewrite.length>=24&&protectedData.length>=10;
    return {count:tasks+checks,total:12,full,critical};
  }
  function getRubric(){
    const complete=rubricSelectors.length===5&&rubricSelectors.every(x=>x.value!=="");
    const sum=complete?rubricSelectors.reduce((n,x)=>n+Number(x.value),0):0;
    const hasZero=complete&&rubricSelectors.some(x=>x.value==="0");
    return {complete,sum,hasZero};
  }
  function decision(){
    const a=kind==="compliance"?assessCompliance():assessAugmented();
    const rub=getRubric();
    if(a.critical||rub.hasZero)return{type:"stop",text:ui.stop,value:rub.sum};
    if(!a.full||a.count<a.total||!rub.complete||rub.sum<10)
      return{type:"revise",text:ui.revise,value:rub.sum};
    return{type:"go",text:ui.go,value:rub.sum};
  }
  $("#ft-release")?.addEventListener("click",()=>{
    const state=decision();const message=state.text+" · "+state.value+"/10. "+ui.notCertificate;
    const x=$("#ft-decision");if(x){x.hidden=false;x.dataset.tone=state.type;x.textContent=message;}
    evaluated=true;
  });
  $("#ft-copy")?.addEventListener("click",async()=>{
    const lines=[
      "MANZO AI · "+ui.copyTitle,
      ui.title+" — "+ui.subtitle,
      ui.notCertificate,
      "",
      ui.stages[0]
    ];
    if(kind==="compliance"){
      ui.tools.forEach((item,i)=>lines.push(item+" → "+(toolSelectors[i]?.selectedOptions[0]?.textContent||"—")));
      lines.push(ui.owner+": "+getVal("ft-owner"),"",ui.stages[1]);
      ui.cases.forEach((item,i)=>lines.push(item[0]+" → "+(caseSelectors[i]?.selectedOptions[0]?.textContent||"—")));
      lines.push("",ui.stages[2]);
      $$(".ft-metric-input").forEach((x,i)=>lines.push("Metric "+(i+1)+": "+x.value));
      $$(".ft-trigger-input").forEach((x,i)=>lines.push("Trigger "+(i+1)+": "+x.value));
    }else{
      ui.tasks.forEach((item,i)=>lines.push(item[0]+" → "+(taskSelectors[i]?.selectedOptions[0]?.textContent||"—")));
      lines.push("",ui.stages[1]);
      ui.checkQuestions.forEach((q,i)=>lines.push(q[0]+" → "+(workSelectors[i]?.selectedOptions[0]?.textContent||"—")));
      lines.push(ui.prior+": "+getVal("ft-prior"),ui.rewrite+": "+getVal("ft-rewrite"));
      ui.charterRules.forEach((label,i)=>lines.push(label+": "+getVal("ft-rule-"+i)));
      lines.push(ui.dataRule+": "+getVal("ft-data-rule"));
    }
    lines.push("",ui.stages[3]);
    ui.rubric.forEach((item,i)=>lines.push(item+": "+(rubricSelectors[i]?.value||"—")));
    lines.push(ui.release+": "+decision().text);
    try{
      if(!navigator.clipboard?.writeText)throw Error("Clipboard unavailable");
      await navigator.clipboard.writeText(lines.join("\n"));
      status("#ft-copy-status",ui.copied,"success");
    }catch(_){status("#ft-copy-status",ui.copyUnavailable,"warning");}
  });

  const squares=$$(".ft-cross-cell input");
  squares.forEach((input,index)=>{
    input.addEventListener("input",()=>{
      input.value=input.value.normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[^a-zA-Z]/g,"").slice(0,1).toUpperCase();
      if(input.value&&index+1<squares.length)squares[index+1].focus();
    });
    input.addEventListener("keydown",e=>{
      if(e.key==="Backspace"&&!input.value&&index>0)squares[index-1].focus();
    });
  });
  $("#ft-cross-check")?.addEventListener("click",()=>{
    let n=0;
    squares.forEach(input=>{
      const correct=input.value===input.dataset.answer;
      if(correct)n++;
      input.closest(".ft-cross-cell").dataset.state=correct?"ok":"fix";
    });
    status("#ft-cross-result",n+" / "+squares.length+" "+ui.cells+" · "+(n===squares.length?ui.crossGood:ui.crossRetry),n===squares.length?"success":"warning");
  });
  $("#ft-cross-clear")?.addEventListener("click",()=>{
    squares.forEach(input=>{
      input.value="";
      delete input.closest(".ft-cross-cell").dataset.state;
    });
    status("#ft-cross-result",ui.crossEmpty,"info");
    squares[0]?.focus();
  });

  const quizHost=$("#ft-quiz-host");
  if(quizHost&&questions.length===10){
    const form=el("form");form.noValidate=true;
    questions.forEach((entry,index)=>{
      const field=el("fieldset",null,"ft-question");
      const legend=el("legend",(index+1)+". "+entry.q);
      field.append(legend);
      entry.options.forEach((choice,j)=>{
        const label=el("label",null,"ft-option");
        const radio=el("input");radio.type="radio";radio.name="ft-q-"+index;radio.value=String(j);
        label.append(radio,document.createTextNode(choice));field.append(label);
      });
      const msg=el("p",null,"ft-question-why");field.append(msg);
      form.append(field);
    });
    const submit=el("button",ui.quizCheck,"ft-button");submit.type="submit";
    const result=el("p",null,"ft-result");result.setAttribute("role","status");
    result.setAttribute("aria-live","polite");result.hidden=true;
    form.append(submit,result);
    form.addEventListener("submit",event=>{
      event.preventDefault();let right=0,answered=0;
      form.querySelectorAll("fieldset").forEach((field,index)=>{
        const item=questions[index],checked=field.querySelector('input[type="radio"]:checked');
        const good=Boolean(checked)&&Number(checked.value)===item.answer;
        if(checked)answered++;if(good)right++;
        field.dataset.reviewed="1";field.dataset.correct=good?"1":"0";
        const x=field.querySelector(".ft-question-why");
        x.textContent=(good?ui.correct:ui.review)+". "+item.why+" "+ui.expected+": "+item.options[item.answer]+".";
      });
      result.hidden=false;
      result.textContent=ui.answered+": "+answered+"/10 · "+ui.score+": "+right+"/10. "+ui.quizNote;
    });
    quizHost.replaceChildren(form);
  }
})();
