"use strict";
/* MANZO AI Prompt vs Skill — bilingual interactive learning.
   All questions, clues, button text and feedback are locale-specific.
   No network calls, storage or tracking. */
(() => {
  const root=document.querySelector('[data-ma-prompt-skill-i18n="v1"]');
  if(!root)return;
  const $=(q)=>root.querySelector(q);
  const $$=(q)=>Array.from(root.querySelectorAll(q));
  let payload;
  try{payload=JSON.parse($("#ps-quiz-data")?.textContent||"{}");}
  catch(_error){return;}
  const ui=payload.ui||{};
  const questions=payload.quiz||[];

  const openReading=(id)=>{
    const section=document.getElementById(id);
    const details=section?.querySelector("details");
    if(details)details.open=true;
  };
  $$("[data-open-reading]").forEach(a=>{
    a.addEventListener("click",()=>openReading(a.getAttribute("data-open-reading")));
  });
  if(/^#lettura-[1-6]$/.test(location.hash))openReading(location.hash.slice(1));

  function updateProgress(){
    const p=$("#ps-progress");
    if(p)p.textContent=$$(".ps-read-check:checked").length+" / 6 "+ui.progress;
  }
  $$(".ps-read-check").forEach(c=>c.addEventListener("change",updateProgress));
  updateProgress();

  const host=$("#ps-quiz-form");
  if(host && questions.length===10){
    const form=document.createElement("form");
    form.className="ps-quiz-form";form.noValidate=true;
    questions.forEach((item,index)=>{
      const field=document.createElement("fieldset");field.className="ps-question";
      const legend=document.createElement("legend");legend.textContent=(index+1)+". "+item.q;
      field.append(legend);
      item.o.forEach((option,i)=>{
        const label=document.createElement("label");label.className="ps-option";
        const radio=document.createElement("input");radio.type="radio";radio.name="ps-q-"+index;radio.value=String(i);
        label.append(radio,document.createTextNode(option));field.append(label);
      });
      const explanation=document.createElement("p");explanation.className="ps-answer-explanation";field.append(explanation);
      form.append(field);
    });
    const submit=document.createElement("button");submit.type="submit";submit.textContent=ui.quizSubmit;submit.className="ps-quiz-submit";
    const status=document.createElement("p");status.id="ps-quiz-feedback";status.hidden=true;
    status.setAttribute("role","status");status.setAttribute("aria-live","polite");
    form.append(submit,status);
    form.addEventListener("submit",event=>{
      event.preventDefault();let correct=0,answered=0;
      form.querySelectorAll(".ps-question").forEach((field,index)=>{
        const item=questions[index],checked=field.querySelector('input[type="radio"]:checked');
        const match=!!checked && Number(checked.value)===item.a;
        if(checked)answered++;if(match)correct++;
        field.dataset.reviewed="1";field.dataset.correct=match?"1":"0";
        field.querySelector(".ps-answer-explanation").textContent=(match?ui.correct:ui.review)+". "+item.e+" "+ui.expected+": "+item.o[item.a]+".";
      });
      status.hidden=false;
      status.textContent=ui.quizProgress+": "+answered+"/"+questions.length+". "+ui.quizScore+": "+correct+"/"+questions.length+". "+ui.quizComment;
      status.scrollIntoView({behavior:"smooth",block:"nearest"});
    });
    host.replaceChildren(form);
  }

  const cells=$$(".ps-cross-square input");
  cells.forEach((input,index)=>{
    input.addEventListener("input",()=>{
      input.value=input.value.normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[^A-Za-z]/g,"").slice(0,1).toUpperCase();
      if(input.value&&index<cells.length-1)cells[index+1].focus();
    });
    input.addEventListener("keydown",e=>{
      if(e.key==="Backspace"&&!input.value&&index>0)cells[index-1].focus();
    });
  });
  $("#ps-check-cross")?.addEventListener("click",()=>{
    let correct=0;
    cells.forEach(input=>{
      const match=input.value===input.dataset.answer;
      if(match)correct++;
      input.style.backgroundColor=match?"#e6f7ef":"#fff2ea";
    });
    const p=$("#ps-cross-result");
    if(p)p.textContent=correct+" "+ui.crossCells+" "+cells.length+". "+(correct===cells.length?ui.crossGood:ui.crossBad);
  });
  $("#ps-clear-cross")?.addEventListener("click",()=>{
    cells.forEach(input=>{input.value="";input.style.backgroundColor="";});
    const p=$("#ps-cross-result");if(p)p.textContent=ui.crossCleared;
    cells[0]?.focus();
  });
})();
