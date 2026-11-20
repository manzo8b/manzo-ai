"use strict";
/* MANZO AI | Reliability + Centroni legacy course localisation
 * Native EN/ES strings are embedded in the course page's reviewed assessment
 * payload. Fictional exercises are entirely local: no network or storage.
 */
(() => {
  const page=document.querySelector('[data-ma-legacy-course]');
  if(!page)return;
  const $=(selector)=>page.querySelector(selector);
  const $$=(selector)=>Array.from(page.querySelectorAll(selector));
  const x=$("#lgi-payload");if(!x)return;
  let data;
  try{data=JSON.parse(x.textContent||"{}");}catch(_error){return;}
  const kind=data.type,ui=data.ui||{},quiz=data.quiz||[];
  const element=(tag,text,cls)=>{
    const n=document.createElement(tag);if(typeof text==="string")n.textContent=text;
    if(cls)n.className=cls;return n;
  };
  const mark=(node,message,tone)=>{
    if(!node)return;node.textContent=message;node.dataset.tone=tone||"info";
    node.hidden=false;
  };
  const val=id=>($("#"+id)?.value||"").trim();
  const finished=()=>{
    const n=$$(".ps-read-check:checked").length;
    mark($("#lgi-progress"),n+" / 6 "+ui.progress,"info");
  };
  $$(".ps-read-check").forEach(c=>c.addEventListener("change",finished));
  $$("[data-open-reading]").forEach(link=>link.addEventListener("click",()=>{
    document.getElementById(link.dataset.openReading)?.querySelector("details")?.setAttribute("open","");
  }));
  if(/^#lgi-reading-[1-6]$/.test(location.hash)){
    document.getElementById(location.hash.slice(1))?.querySelector("details")?.setAttribute("open","");
  }
  finished();
  let touchedScenario=false;
  const invalidate=()=>{
    const output=$("#lgi-decision");
    if(output){output.textContent="";output.hidden=true;}
  };
  $$("#lgi-lab input, #lgi-lab textarea, #lgi-lab select").forEach(n=>{
    n.addEventListener("input",invalidate);n.addEventListener("change",invalidate);
  });
  $$(".lgi-scenario").forEach(button=>button.addEventListener("click",()=>{
    const index=Number(button.dataset.scenario),entry=ui.scenarios?.[index];
    if(!entry)return;
    touchedScenario=true;
    mark($("#lgi-scenario-output"),entry[1]+" · "+entry[2],"info");
    $$(".lgi-scenario").forEach(btn=>{
      btn.setAttribute("aria-pressed",String(btn===button));
    });
    invalidate();
  }));
  function evaluateReliability(){
    const selectors=$$(".lgi-score select");
    let sum=0,zero=0,missing=0,critical=false;
    selectors.forEach((node,index)=>{
      if(node.value==="")missing++;
      else{
        const score=Number(node.value);sum+=score;
        if(score===0)zero++;
        // A zero in source fidelity for any test is a hard learning STOP.
        if(score===0&&index%3===0)critical=true;
      }
    });
    const full=selectors.length===12&&missing===0&&val("lgi-owner").length>=3&&
      val("lgi-source").length>=4&&val("lgi-review").length>=24;
    if(critical)return{type:"stop",message:ui.stop,score:sum,total:24};
    if(!full||zero>0||sum<20)return{type:"revise",message:ui.revise,score:sum,total:24};
    return{type:"go",message:ui.go,score:sum,total:24};
  }
  function evaluateCentroni(){
    const fields=ui.fields||[];
    const complete=fields.length===8&&fields.every(item=>val("lgi-"+item[0]).length>=4);
    const qa=$$(".lgi-check");
    const passed=qa.filter(c=>c.checked).length;
    const critical=qa.length===5&&(!qa[2].checked||!qa[3].checked);
    if(critical)return{type:"stop",message:ui.stop,score:passed,total:5};
    if(!complete||qa.length!==5||passed<5||!touchedScenario||val("lgi-owner").length<3)
      return{type:"revise",message:ui.revise,score:passed,total:5};
    return{type:"go",message:ui.go,score:passed,total:5};
  }
  function evaluate(){
    return kind==="reliability"?evaluateReliability():evaluateCentroni();
  }
  $("#lgi-evaluate")?.addEventListener("click",()=>{
    const score=evaluate();
    mark($("#lgi-decision"),score.message+" · "+score.score+"/"+score.total+". "+ui.noCert,score.type);
  });
  $("#lgi-copy")?.addEventListener("click",async()=>{
    const result=evaluate();
    const items=["MANZO AI · "+ui.copyTitle,ui.title+" — "+ui.subtitle,ui.noCert,""];
    if(kind==="reliability"){
      items.push(ui.source+": "+val("lgi-source"),ui.role+": "+val("lgi-owner"),"");
      const selectors=$$(".lgi-score select");
      (ui.cases||[]).forEach((entry,i)=>{
        items.push(entry[0]+": "+entry[2]);
        (ui.rubric||[]).forEach((criterion,j)=>{
          items.push("  "+criterion+": "+(selectors[i*3+j]?.value||"—"));
        });
      });
      items.push(ui.review+": "+val("lgi-review"));
    }else{
      (ui.fields||[]).forEach(item=>items.push(item[1]+": "+val("lgi-"+item[0])));
      items.push(ui.staff+": "+val("lgi-owner"),ui.test);
      $$(".lgi-check").forEach((c,i)=>items.push((c.checked?"✓ ":"✗ ")+(ui.checks?.[i]||"")));
      items.push(ui.noOfficial);
    }
    items.push(ui.status+": "+result.message+" · "+result.score+"/"+result.total);
    try{
      if(!navigator.clipboard?.writeText)throw Error("Clipboard unsupported");
      await navigator.clipboard.writeText(items.join("\n"));
      mark($("#lgi-copy-status"),ui.copyOk,"success");
    }catch(_){mark($("#lgi-copy-status"),ui.copyError,"warning");}
  });
  const host=$("#lgi-quiz-host");
  if(host&&quiz.length===10){
    const form=element("form");
    quiz.forEach((q,i)=>{
      const field=element("fieldset",null,"ft-question");
      field.append(element("legend",(i+1)+". "+q.q));
      q.options.forEach((choice,j)=>{
        const label=element("label",null,"ft-option");
        const input=element("input");
        input.type="radio";input.name="lgi-q-"+i;input.value=String(j);
        label.append(input,document.createTextNode(choice));
        field.append(label);
      });
      field.append(element("p",null,"ft-question-why"));
      form.append(field);
    });
    const submit=element("button",ui.verify,"ft-button");submit.type="submit";
    const result=element("p",null,"ft-result");result.setAttribute("role","status");
    result.setAttribute("aria-live","polite");result.hidden=true;
    form.append(submit,result);
    form.addEventListener("submit",event=>{
      event.preventDefault();
      let good=0,answered=0;
      form.querySelectorAll("fieldset").forEach((field,i)=>{
        const chosen=field.querySelector('input[type="radio"]:checked');
        const ok=Boolean(chosen)&&Number(chosen.value)===quiz[i].answer;
        if(chosen)answered++;if(ok)good++;
        field.dataset.reviewed="1";field.dataset.correct=ok?"1":"0";
        const why=field.querySelector(".ft-question-why");
        why.textContent=(ok?ui.correct:ui.review)+". "+quiz[i].why+
          " "+ui.expected+": "+quiz[i].options[quiz[i].answer]+".";
      });
      mark(result,ui.answered+": "+answered+"/10 · "+ui.right+": "+good+"/10. "+ui.noCert,good===10?"success":"info");
    });
    host.replaceChildren(form);
  }
})();
