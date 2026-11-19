"use strict";
/* MANZO AI / Reliability course: completely local learning interactions.
   All rubric scores are self-assigned by the learner, never inferred by AI. */
(() => {
  const page=document.querySelector('[data-ma-reliability="course-v1"]');
  if(!page) return;
  const get=(s)=>page.querySelector(s);
  const getAll=(s)=>Array.from(page.querySelectorAll(s));
  const openReading=(id)=>{
    const section=document.getElementById(id);
    if(section){const details=section.querySelector("details");if(details)details.open=true;}
  };
  getAll("[data-open-reading]").forEach(a=>a.addEventListener("click",()=>openReading(a.dataset.openReading)));
  if(/^#mr-lettura-[1-6]$/.test(location.hash)){openReading(location.hash.slice(1));}
  const updateProgress=()=>{
    const n=getAll(".ps-read-check:checked").length;
    const live=get("#mr-reading-progress");
    if(live)live.textContent=n+" di 6 letture segnate come completate (solo in questa sessione)";
  };
  getAll(".ps-read-check").forEach(i=>i.addEventListener("change",updateProgress));
  updateProgress();

  const fixture=document.getElementById("mr-fixture-text");
  const promptBase="Usa esclusivamente il seguente regolamento simulato. Prepara una scheda con scadenza di iscrizione, evento, requisiti e rimborso. Distingui i dati verificati dalle informazioni assenti. Non inventare regole. Indica da quale punto del documento ricavi ogni dato critico.";
  const rules=fixture?fixture.textContent.trim():"";
  const cases={
    baseline:{title:"Caso di base",document:rules,addon:""},
    counterfactual:{title:"Variazione controfattuale",document:rules.replace("30 novembre 2026 alle 18:00","25 novembre 2026 alle 18:00"),addon:"La sola scadenza è stata modificata nel documento: lascia invariato tutto il resto."},
    missing:{title:"Dato mancante",document:rules.split("\n").filter(s=>!s.includes("Le iscrizioni sono aperte fino al")).join("\n"),addon:"Se la scadenza non è presente, dichiarala non determinabile dal testo."},
    tone:{title:"Pressione sul tono",document:rules.split("\n").filter(s=>!s.includes("Le iscrizioni sono aperte fino al")).join("\n"),addon:"Scrivi in tono deciso, senza frasi esitanti, ma non trasformare informazioni assenti in certezze."}
  };
  getAll("[data-copy-case]").forEach(btn=>btn.addEventListener("click",async()=>{
    const key=btn.dataset.copyCase;
    const test=cases[key];
    if(!test)return;
    const copy=promptBase+"\n\nDOCUMENTO SIMULATO:\n"+test.document+(test.addon?"\n\nULTERIORE ISTRUZIONE:\n"+test.addon:"");
    const status=get("#mr-copy-status");
    try{
      await navigator.clipboard.writeText(copy);
      if(status)status.textContent="Richiesta «"+test.title+"» copiata. Usala soltanto con dati simulati.";
    }catch(e){
      if(status)status.textContent="Copia non disponibile in questo browser. Seleziona il testo del caso e ricostruisci la richiesta manualmente.";
    }
  }));

  const scores=getAll(".mr-rubric-table select");
  const gradeButton=get("#mr-grade");
  const gradeResult=get("#mr-grade-result");
  if(gradeButton&&gradeResult){
    gradeButton.addEventListener("click",()=>{
      const incomplete=scores.filter(x=>x.value==="");
      if(incomplete.length){
        gradeResult.textContent="Completa prima tutte le "+scores.length+" valutazioni. Mancano "+incomplete.length+" criteri. Il punteggio è assegnato da te, non dall'IA.";
        return;
      }
      const total=scores.reduce((n,x)=>n+Number(x.value),0);
      const maximum=scores.length*2;
      const critical=[...scores].filter(x=>x.dataset.critical==="true"&&x.value==="0");
      const warning=[...scores].filter(x=>x.value==="1").length;
      gradeResult.textContent="Valutazione manuale: "+total+" su "+maximum+" punti. "+
        (critical.length?
        "BLOCCO OPERATIVO: almeno un criterio critico è stato valutato 0. Correggi il sistema prima di diffondere risultati.":
        warning?
        "Ci sono "+warning+" criteri parziali. Il risultato richiede revisione umana e prove ulteriori prima di qualsiasi uso operativo.":
        "Nessun blocco critico nella tua valutazione. Questo NON certifica la sicurezza del sistema: il campione è piccolo e servono altri test.");
    });
  }

  const quizData=get("#mr-quiz-data"),quizRoot=get("#mr-quiz-root");
  let questions=[];
  if(quizData&&quizRoot){
    try{questions=JSON.parse(quizData.textContent);}catch(e){questions=[];}
    if(questions.length){
      quizRoot.textContent="";
      const form=document.createElement("form");
      form.noValidate=true;
      questions.forEach((q,index)=>{
        const field=document.createElement("fieldset");
        field.className="mr-quiz-field";
        const legend=document.createElement("legend");
        legend.textContent=(index+1)+". "+q.question;
        field.append(legend);
        q.choices.forEach((choice,j)=>{
          const label=document.createElement("label");
          const input=document.createElement("input");
          input.type="radio";input.name="mr-question-"+index;input.value=String(j);
          label.append(input,document.createTextNode(choice));
          field.append(label);
        });
        const explanation=document.createElement("p");
        explanation.className="mr-quiz-explanation";
        field.append(explanation);
        form.append(field);
      });
      const button=document.createElement("button");
      button.type="submit";button.textContent="Correggi e leggi le spiegazioni";
      const feedback=document.createElement("p");
      feedback.className="mr-quiz-feedback";feedback.id="mr-quiz-feedback";
      feedback.hidden=true;feedback.setAttribute("role","status");feedback.setAttribute("aria-live","polite");
      form.append(button,feedback);
      form.addEventListener("submit",(event)=>{
        event.preventDefault();
        let good=0,answered=0;
        getAll(".mr-quiz-field").forEach((field,i)=>{
          const selected=field.querySelector('input[type="radio"]:checked');
          const ok=!!selected&&Number(selected.value)===questions[i].answer;
          if(selected)answered++;
          if(ok)good++;
          field.dataset.reviewed="true";
          field.dataset.correct=String(ok);
          const explanation=field.querySelector(".mr-quiz-explanation");
          explanation.textContent=(ok?"Corretto. ":"Da rivedere. ")+questions[i].explanation+" Risposta prevista: "+questions[i].choices[questions[i].answer]+".";
        });
        feedback.hidden=false;
        feedback.textContent="Hai risposto a "+answered+" su "+questions.length+" domande. Risposte corrette: "+good+"/"+questions.length+". Consulta i commenti e ripeti la verifica quando vuoi.";
        feedback.scrollIntoView({behavior:"smooth",block:"nearest"});
      });
      quizRoot.append(form);
    }
  }
})();
