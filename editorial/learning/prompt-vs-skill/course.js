"use strict";
(() => {
  const root=document.querySelector('[data-ma-prompt-skill="course-v1"]');
  if(!root) return;
  const $=(s)=>root.querySelector(s);
  const $$=(s)=>Array.from(root.querySelectorAll(s));

  function openReading(id){
    const section=document.getElementById(id);
    if(!section) return;
    const details=section.querySelector("details");
    if(details) details.open=true;
  }
  $$("[data-open-reading]").forEach(link=>{
    link.addEventListener("click",()=>openReading(link.getAttribute("data-open-reading")));
  });
  if(location.hash && /^#lettura-[1-6]$/.test(location.hash)){
    openReading(location.hash.slice(1));
  }

  function updateProgress(){
    const n=$$(".ps-read-check:checked").length;
    const counter=$("#ps-progress");
    if(counter) counter.textContent=n+" di 6 letture segnate come completate in questa sessione";
  }
  $$(".ps-read-check").forEach(x=>x.addEventListener("change",updateProgress));
  updateProgress();

  const quizData=document.getElementById("ps-quiz-data");
  const quizHost=$("#ps-quiz-form");
  if(quizData && quizHost){
    let questions=[];
    try{questions=JSON.parse(quizData.textContent);}catch(_err){questions=[];}
    if(questions.length){
      quizHost.innerHTML="";
      const form=document.createElement("form");
      form.className="ps-quiz-form";
      form.noValidate=true;
      questions.forEach((item,index)=>{
        const field=document.createElement("fieldset");
        field.className="ps-question";
        const legend=document.createElement("legend");
        legend.textContent=(index+1)+". "+item.q;
        field.append(legend);
        item.o.forEach((option,opt)=>{
          const label=document.createElement("label");
          label.className="ps-option";
          const radio=document.createElement("input");
          radio.type="radio";
          radio.name="ps-q-"+index;
          radio.value=String(opt);
          label.append(radio,document.createTextNode(option));
          field.append(label);
        });
        const explanation=document.createElement("p");
        explanation.className="ps-answer-explanation";
        field.append(explanation);
        form.append(field);
      });
      const submit=document.createElement("button");
      submit.type="submit";
      submit.textContent="Correggi il quiz e leggi le spiegazioni";
      submit.className="ps-quiz-submit";
      const feedback=document.createElement("p");
      feedback.id="ps-quiz-feedback";
      feedback.setAttribute("role","status");
      feedback.setAttribute("aria-live","polite");
      feedback.hidden=true;
      form.append(submit,feedback);
      form.addEventListener("submit",(event)=>{
        event.preventDefault();
        let correct=0,answered=0;
        $$(".ps-question").forEach((field,index)=>{
          const item=questions[index];
          const checked=field.querySelector('input[type="radio"]:checked');
          if(checked) answered++;
          const match=checked && Number(checked.value)===item.a;
          if(match) correct++;
          field.dataset.reviewed="1";
          field.dataset.correct=match?"1":"0";
          const explanation=field.querySelector(".ps-answer-explanation");
          explanation.textContent=(match?"Risposta corretta. ":"Da rivedere. ")+item.e+" Risposta prevista: "+item.o[item.a]+".";
        });
        feedback.hidden=false;
        feedback.textContent="Hai risposto a "+answered+" domande su "+questions.length+". Risposte corrette: "+correct+" su "+questions.length+". Leggi il commento sotto ogni domanda e riprova quando vuoi.";
        feedback.scrollIntoView({behavior:"smooth",block:"nearest"});
      });
      quizHost.append(form);
    }
  }

  const crossInputs=$$(".ps-cross-square input");
  const crossCheck=$("#ps-check-cross");
  const crossClear=$("#ps-clear-cross");
  const crossResult=$("#ps-cross-result");
  crossInputs.forEach((input,i)=>{
    input.addEventListener("input",()=>{
      input.value=input.value.replace(/[^A-Za-zÀ-ÿ]/g,"").slice(0,1).toLocaleUpperCase("it-IT");
      if(input.value && i+1<crossInputs.length) crossInputs[i+1].focus();
    });
    input.addEventListener("keydown",(event)=>{
      if(event.key==="Backspace" && !input.value && i>0){
        crossInputs[i-1].focus();
      }
    });
  });
  if(crossCheck && crossResult){
    crossCheck.addEventListener("click",()=>{
      let right=0;
      crossInputs.forEach(input=>{
        const pass=input.value.toLocaleUpperCase("it-IT")===input.dataset.answer;
        if(pass) right++;
        input.style.backgroundColor=pass?"#e6f7ef":"#fff2ea";
      });
      crossResult.textContent=right+" caselle corrette su "+crossInputs.length+". "+(right===crossInputs.length?"Cruciverba completato!":"Rivedi quelle evidenziate e riprova.");
    });
  }
  if(crossClear){
    crossClear.addEventListener("click",()=>{
      crossInputs.forEach(input=>{input.value="";input.style.backgroundColor="";});
      if(crossResult) crossResult.textContent="Cruciverba azzerato. Puoi riprovare.";
      if(crossInputs.length) crossInputs[0].focus();
    });
  }
})();
