"use strict";
/* MANZO AI / Build Safely. Native, local-only teaching interactions.
   No file uploads, network calls, persistence, tracking or AI model calls.
   The words, answers and interface are authored and translated server-side. */
(() => {
  const root=document.querySelector('[data-ma-safe="v1"]');
  if(!root) return;
  const $=(q)=>root.querySelector(q);
  const $$=(q)=>Array.from(root.querySelectorAll(q));
  let payload={};
  try{payload=JSON.parse($("#safe-data")?.textContent||"{}");}catch(_e){return;}
  const ui=payload.ui||{};
  const live=(selector,text)=>{const el=$(selector);if(el)el.textContent=text;};

  const readingProgress=()=>{
    live("#safe-reading-progress",$$(".ps-read-check:checked").length+" / 6 "+ui.readingsDone);
  };
  $$(".ps-read-check").forEach(input=>input.addEventListener("change",readingProgress));
  readingProgress();
  function openReading(hash){
    const section=document.getElementById(hash);
    if(section){const detail=section.querySelector("details");if(detail)detail.open=true;}
  }
  $$("[data-open-reading]").forEach(anchor=>{
    anchor.addEventListener("click",()=>openReading(anchor.getAttribute("data-open-reading")));
  });
  if(location.hash && /^#safe-reading-[1-6]$/.test(location.hash))openReading(location.hash.substring(1));

  const scoreSelects=$$(".safe-data-card select");
  $("#safe-data-check")?.addEventListener("click",()=>{
    let n=0,answered=0;
    $$(".safe-data-card").forEach((card,index)=>{
      const select=card.querySelector("select");
      const feedback=card.querySelector(".safe-feedback");
      const item=payload.dataItems[index];
      if(!select||!item)return;
      if(select.value)answered++;
      if(select.value===item.level)n++;
      feedback.textContent=(select.value===item.level?ui.correct+": ":ui.review+": ")+item.why;
    });
    live("#safe-data-status",answered+" / "+scoreSelects.length+" "+ui.answered+" · "+n+" / "+scoreSelects.length+" "+ui.correct.toLowerCase()+". "+ui.trafficNote);
  });

  const gate=$("#safe-gate-choice");
  if(gate){
    gate.addEventListener("change",()=>{
      const answer=gate.value;
      if(!answer){live("#safe-gate-status",ui.gateIdle);return;}
      live("#safe-gate-status",answer==="check"?ui.gateChecked:ui.gateUnsafe);
    });
  }
  const injection=$("#safe-injection-choice");
  if(injection){
    injection.addEventListener("change",()=>{
      const answer=injection.value;
      live("#safe-injection-status",answer==="layers"?ui.injectionGood:ui.injectionBad);
    });
  }
  const rubric=$$(".safe-rubric select");
  $("#safe-score")?.addEventListener("click",()=>{
    if(rubric.some(sel=>!sel.value)){
      live("#safe-rubric-status",ui.missingScores);return;
    }
    const n=rubric.reduce((sum,sel)=>sum+Number(sel.value),0);
    const critical=rubric.filter(sel=>sel.dataset.critical==="true" && sel.value==="0").length;
    live("#safe-rubric-status",ui.score+": "+n+" / "+rubric.length*2+". "+(critical?ui.stop:ui.scoreWarning));
  });

  const wordInputs=$$(".safe-word-cell input");
  wordInputs.forEach((input,i)=>{
    input.addEventListener("input",()=>{
      input.value=input.value.normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[^A-Za-z]/g,"").slice(0,1).toUpperCase();
      if(input.value&&i<wordInputs.length-1)wordInputs[i+1].focus();
    });
    input.addEventListener("keydown",e=>{
      if(e.key==="Backspace"&&!input.value&&i>0)wordInputs[i-1].focus();
    });
  });
  $("#safe-cross-check")?.addEventListener("click",()=>{
    let good=0;
    wordInputs.forEach(el=>{
      const match=el.value===el.dataset.letter;
      if(match)good++;
      el.style.backgroundColor=match?"#dbf5e5":"#ffeade";
    });
    live("#safe-cross-result",good+" / "+wordInputs.length+" "+ui.wordCells+". "+(good===wordInputs.length?ui.crossSuccess:ui.crossTryAgain));
  });
  $("#safe-cross-clear")?.addEventListener("click",()=>{
    wordInputs.forEach(el=>{el.value="";el.style.backgroundColor="";});
    live("#safe-cross-result",ui.crossCleared);
    wordInputs[0]?.focus();
  });

  const host=$("#safe-quiz-host");
  if(host && Array.isArray(payload.quiz)){
    const form=document.createElement("form");form.noValidate=true;
    payload.quiz.forEach((q,i)=>{
      const field=document.createElement("fieldset");field.className="safe-quiz-field";
      const legend=document.createElement("legend");legend.textContent=(i+1)+". "+q.q;
      field.append(legend);
      q.options.forEach((option,j)=>{
        const label=document.createElement("label");
        const radio=document.createElement("input");
        radio.type="radio";radio.name="safe-q-"+i;radio.value=String(j);
        label.append(radio,document.createTextNode(option));field.append(label);
      });
      const why=document.createElement("p");why.className="safe-quiz-explain";field.append(why);form.append(field);
    });
    const submit=document.createElement("button");submit.className="safe-action";submit.type="submit";submit.textContent=ui.quizSubmit;
    const feedback=document.createElement("p");feedback.className="safe-status";feedback.setAttribute("role","status");feedback.setAttribute("aria-live","polite");feedback.hidden=true;
    form.append(submit,feedback);
    form.addEventListener("submit",event=>{
      event.preventDefault();let right=0,done=0;
      Array.from(form.querySelectorAll(".safe-quiz-field")).forEach((field,i)=>{
        const checked=field.querySelector("input:checked");
        const good=!!checked&&Number(checked.value)===payload.quiz[i].answer;
        if(checked)done++;
        if(good)right++;
        field.dataset.reviewed="true";field.dataset.correct=String(good);
        field.querySelector(".safe-quiz-explain").textContent=(good?ui.correct+": ":ui.review+": ")+payload.quiz[i].why+" "+ui.correctAnswer+": "+payload.quiz[i].options[payload.quiz[i].answer]+".";
      });
      feedback.hidden=false;
      feedback.textContent=ui.answered+": "+done+"/"+payload.quiz.length+". "+ui.score+": "+right+"/"+payload.quiz.length+". "+ui.quizAdvice;
      feedback.scrollIntoView({behavior:"smooth",block:"nearest"});
    });
    host.replaceChildren(form);
  }
})();
