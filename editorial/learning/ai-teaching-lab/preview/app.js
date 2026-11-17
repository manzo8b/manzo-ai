"use strict";
/* MANZO AI / AI Teaching Lab — isolated educational preview
 * Source content: ../it/course.json and ../it/assessment-bank.json
 * No cookies, API credentials, analytics, localStorage, or student data.
 * Quiz solutions live in a PUBLIC JSON: formative only, never an exam engine.
 */
(function () {
  const $ = (id) => document.getElementById(id);
  const accent = {cobalt:"#1159ea",violet:"#7547cb",coral:"#d84d30",emerald:"#077c61",teal:"#007a8b"};
  const state = {course:null,bank:null,scenarios:null,index:0};
  function el(tag, cls, text) {
    const x=document.createElement(tag);
    if (cls) x.className=cls;
    if (text!==undefined && text!==null) x.textContent=String(text);
    return x;
  }
  function add(parent,...children){children.flat().forEach(c=>{if(c!==undefined&&c!==null)parent.append(c)});return parent}
  function heading(tag,text){return el(tag,"",text)}
  function paragraph(s,klass){return el("p",klass||"",s)}
  function list(items, ordered) {const node=el(ordered?"ol":"ul");items.forEach(s=>add(node,el("li","",s)));return node}
  function control(text,cb,variant) {const b=el("button","button"+(variant?" "+variant:""),text);b.type="button";b.addEventListener("click",cb);return b}
  function feedback(where,body,ok) {
    const old=where.querySelector(".result");if(old)old.remove();
    const n=el("div","result "+(ok===true?"success":ok===false?"warning":""),body);
    n.setAttribute("role","status");n.setAttribute("aria-live","polite");where.append(n);
  }
  function section(kicker,title) {
    const x=el("section","panel");
    add(x,el("div","section-kicker",kicker),heading("h3",title));
    return x;
  }
  function external(url,name) {
    const a=el("a","",name);a.href=url;a.target="_blank";a.rel="noopener noreferrer";return a;
  }
  function singleChoice(item,n) {
    const block=el("fieldset","assessment-block");
    add(block,el("legend","",n+". "+item.question));
    const name="q-"+item.id;
    item.options.forEach((opt,i)=>{
      const label=el("label","choice");
      const inp=el("input");inp.type="radio";inp.name=name;inp.value=String(i);
      add(label,inp,el("span","",opt));add(block,label);
    });
    add(block,control("Verifica la risposta",()=>{
      const selected=block.querySelector("input:checked");
      if (!selected) {feedback(block,"Seleziona una risposta prima di controllare.");return}
      const ok=Number(selected.value)===item.correct_index;
      feedback(block,(ok?"Corretto. ":"Da rivedere. ")+item.feedback,ok);
    }));
    return block;
  }
  function multiChoice(item) {
    const block=el("fieldset","assessment-block");
    add(block,el("legend","",item.stem));
    item.choices.forEach((opt,i)=>{
      const label=el("label","choice");
      const inp=el("input");inp.type="checkbox";inp.value=String(i);
      add(label,inp,el("span","",opt));add(block,label);
    });
    add(block,control("Controlla la selezione",()=>{
      const chosen=Array.from(block.querySelectorAll("input:checked")).map(x=>Number(x.value)).sort((a,b)=>a-b);
      if (chosen.length===0) {feedback(block,"Scegli almeno una risposta.");return}
      const expected=[...item.correct].sort((a,b)=>a-b);
      const ok=JSON.stringify(chosen)===JSON.stringify(expected);
      feedback(block,(ok?"Corretto. ":"Riesamina entrambe le condizioni. ")+item.rationale,ok);
    }));
    return block;
  }
  function scenario(item) {
    const block=el("fieldset","assessment-block");
    add(block,el("legend","",item.stem));
    item.options.forEach((opt,i)=>{
      const label=el("label","choice");const radio=el("input");radio.type="radio";radio.name="scenario";radio.value=String(i);
      add(label,radio,el("span","",opt));add(block,label);
    });
    const label=el("label","", "Spiega con almeno 20 caratteri perché hai scelto questa risposta");
    label.htmlFor="decision-reason";
    const reason=el("textarea","text-reason");reason.id="decision-reason";reason.rows=3;
    add(block,label,reason,control("Confronta la tua decisione",()=>{
      const checked=block.querySelector("input:checked");
      if(!checked||reason.value.trim().length<20){
        feedback(block,"Seleziona un'opzione e motiva la decisione prima di leggere il feedback.");return;
      }
      const selected=Number(checked.value),ok=selected===item.correct_index;
      feedback(block,(ok?"Decisione coerente. ":"La scelta comporta un problema. ")+item.feedback[selected],ok);
    }));
    return block;
  }
  function matching(item) {
    const block=el("div","assessment-block");
    add(block,heading("h4","Associazioni — collega termini ed esempi"),paragraph(item.prompt,"subtle"));
    const all=item.pairs.map(p=>p.description).reverse();
    const selects=[];
    item.pairs.forEach((p,i)=>{
      const row=el("div","match-row");const title=el("label","",p.term);
      const sel=el("select");sel.id="match-"+i;title.htmlFor=sel.id;
      const placeholder=el("option","", "Scegli la definizione");placeholder.value="";add(sel,placeholder);
      all.forEach((d,j)=>{const opt=el("option","",d);opt.value=d;add(sel,opt)});
      add(row,title,sel);add(block,row);selects.push({sel,expected:p.description});
    });
    add(block,control("Controlla le associazioni",()=>{
      const count=selects.filter(s=>s.sel.value===s.expected).length;
      feedback(block,count+" associazioni corrette su "+selects.length+". Rivedi le altre e spiega una coppia usando un caso.",count===selects.length);
    }));
    return block;
  }
  function crossword(item) {
    const block=el("section","assessment-block");
    add(block,heading("h4","Cruciverba professionale"),paragraph("Compila la griglia oppure scegli la modalità testuale accessibile. Le caselle scure non vanno riempite.","subtle"));
    const toggles=el("div","toggle-row");
    const gridButton=control("Griglia",()=>switchMode("grid"),"secondary");
    const textButton=control("Elenco accessibile",()=>switchMode("text"),"secondary");
    add(toggles,gridButton,textButton);add(block,toggles);
    const gridWrap=el("div","crossword-wrap");
    const grid=el("div","crossword");grid.style.setProperty("--grid-cols",String(item.width));
    const startNums={};
    item.entries.forEach(e=>{startNums[e.row+","+e.col]=String(e.number)});
    const cells={};
    item.pattern.forEach((row,y)=>[...row].forEach((ch,x)=>{
      if(ch==="#"){add(grid,el("div","cross-cell cross-block"));return}
      const box=el("div","cross-cell"),input=el("input");
      input.type="text";input.maxLength=1;input.autocomplete="off";input.spellcheck=false;
      input.setAttribute("aria-label","Riga "+(y+1)+", colonna "+(x+1));
      input.dataset.row=String(y);input.dataset.col=String(x);
      input.addEventListener("input",()=>{input.value=input.value.slice(-1).toUpperCase().replace(/[^A-Z]/g,"")});
      input.addEventListener("keydown",ev=>{
        const moves={ArrowLeft:[0,-1],ArrowRight:[0,1],ArrowUp:[-1,0],ArrowDown:[1,0]};
        if(!moves[ev.key])return;
        ev.preventDefault();const d=moves[ev.key];
        let ry=y+d[0],cx=x+d[1];
        while(ry>=0&&ry<item.height&&cx>=0&&cx<item.width){
          if(cells[ry+","+cx]){cells[ry+","+cx].focus();return}
          ry+=d[0];cx+=d[1];
        }
      });
      cells[y+","+x]=input;add(box,input);
      if(startNums[y+","+x])add(box,el("span","cell-num",startNums[y+","+x]));
      add(grid,box);
    }));
    add(gridWrap,grid);
    const clues=el("div","clue-list");
    const clueList=el("ol");
    item.entries.forEach(e=>add(clueList,el("li","",e.number+" "+(e.direction==="across"?"Orizzontale":"Verticale")+" · "+e.clue+" ("+e.answer.length+" lettere)")));
    add(clues,clueList);add(gridWrap,clues);
    const accessible=el("div","accessible-words");accessible.hidden=true;
    const words=[];
    item.entries.forEach(e=>{
      const row=el("div","word-field"),label=el("label","",e.number+" "+e.clue+" ("+e.answer.length+" lettere)");
      const input=el("input");input.type="text";input.maxLength=e.answer.length+3;input.autocomplete="off";input.spellcheck=false;
      input.id="word-"+e.number+"-"+e.direction;label.htmlFor=input.id;
      add(row,label,input);add(accessible,row);words.push({answer:e.answer,input});
    });
    let mode="grid";
    function switchMode(next){
      mode=next;gridWrap.hidden=next!=="grid";accessible.hidden=next!=="text";
      gridButton.setAttribute("aria-pressed",String(next==="grid"));
      textButton.setAttribute("aria-pressed",String(next==="text"));
      const prev=block.querySelector(".result");if(prev)prev.remove();
    }
    switchMode("grid");
    add(block,gridWrap,accessible);
    const normalize=v=>String(v).toUpperCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[^A-Z]/g,"");
    const exp={};
    item.entries.forEach(e=>{
      [...e.answer].forEach((ch,i)=>{
        const y=e.row+(e.direction==="down"?i:0),x=e.col+(e.direction==="across"?i:0);
        exp[y+","+x]=ch;
      });
    });
    add(block,control("Verifica il cruciverba",()=>{
      if(mode==="grid"){
        const keys=Object.keys(exp),correct=keys.filter(k=>normalize(cells[k].value)===exp[k]).length;
        feedback(block,correct+" caselle corrette su "+keys.length+". Controlla gli incroci e riprova.",correct===keys.length);
      }else{
        const correct=words.filter(w=>normalize(w.input.value)===w.answer).length;
        feedback(block,correct+" parole corrette su "+words.length+". Rivedi gli indizi non risolti.",correct===words.length);
      }
    }));
    return block;
  }
  function conceptProbe(module) {
    const block=section("PRIMA DI LEGGERE","Che cosa decideresti oggi?");
    const q=module.mini_theory;
    add(block,paragraph(q.probe));
    const field=el("fieldset","assessment-block");
    add(field,el("legend","","Seleziona un'ipotesi prima di aprire la teoria"));
    q.options.forEach((opt,i)=>{
      const label=el("label","choice"),inp=el("input");
      inp.type="radio";inp.name="theory-probe";inp.value=String(i);
      add(label,inp,el("span","",opt));add(field,label);
    });
    add(field,control("Confronta la mia ipotesi",()=>{
      const selected=field.querySelector("input:checked");
      if(!selected){feedback(field,"Scegli un'ipotesi per confrontarla con la teoria.");return}
      const good=Number(selected.value)===q.correct;
      feedback(field,(good?"Hai individuato il principio. ":"Quale premessa manca? ")+q.feedback,good);
    }));
    add(block,field,paragraph("Questa previsione è solo un esercizio formativo. Nessuna risposta viene registrata.","subtle"));
    return block;
  }
  function branchingSimulation(s) {
    const block=section("DECISION LAB / SIMULAZIONE","Una scelta cambia il problema");
    add(block,paragraph("Due decisioni consecutive, tre strategie iniziali e sei esiti possibili. Nessun punteggio: valuta il ragionamento e la responsabilità." ,"subtle"));
    const view=el("div","branch-stage"),head=el("h4"),lead=el("p"),choices=el("div","branch-choices"),after=el("div","branch-feedback"),actions=el("div","branch-actions");
    add(view,head,lead,choices,after,actions);add(block,view);
    function chooseFirst(selected) {
      const p=s.first[selected];choices.replaceChildren();after.replaceChildren();actions.replaceChildren();
      head.textContent="Conseguenza della prima scelta";
      lead.textContent=p.challenge;
      const note=el("div","branch-note",p.note);
      add(after,note);
      p.routes.forEach((route,i)=>{
        add(choices,control(String.fromCharCode(65+i)+" · "+route.label,()=>finish(p,route),"secondary"));
      });
      const back=control("Cambia la prima scelta",start,"secondary");add(actions,back);
      choices.querySelector("button")?.focus();
    }
    function finish(p,route){
      choices.replaceChildren();after.replaceChildren();actions.replaceChildren();
      head.textContent=route.good?"Decisione responsabile — e ora?":"Scelta problematica — come correggerla?";
      lead.textContent=route.why;
      const consequence=el("div","branch-outcome");
      add(consequence,el("strong","",route.good?"Passaggio utilizzabile":"Intervento correttivo"),paragraph(route.result));
      const reflection=el("div","branch-reflection");
      add(reflection,heading("h4","Trasferisci nella tua classe"),paragraph(route.transfer),
        paragraph(s.reflection,"subtle"));
      const label=el("label","", "La mia revisione motivata (solo su questa pagina)");
      label.htmlFor="branch-reason";
      const text=el("textarea","text-reason");text.id="branch-reason";text.rows=4;
      const confirm=control("Ho definito una revisione",()=>{
        if(text.value.trim().length<30){feedback(after,"Formula una revisione concreta di almeno 30 caratteri.");return}
        feedback(after,"Revisione formulata. Trasferiscila nel tuo portfolio personale: questo prototipo non la salva.",true);
      });
      add(after,consequence,reflection,label,text,confirm);
      add(actions,control("Esplora una scelta diversa",start,"secondary"));
    }
    function start(){
      head.textContent=s.title;
      lead.textContent=s.setting+" "+s.key_question;
      choices.replaceChildren();after.replaceChildren();actions.replaceChildren();
      s.first.forEach((p,i)=>add(choices,control(String.fromCharCode(65+i)+" · "+p.label,()=>chooseFirst(i),"secondary")));
    }
    start();
    return block;
  }
  function render() {
    const m=state.course.modules[state.index],a=state.bank.modules.find(q=>q.module_id===m.id),scenario=state.scenarios.modules.find(q=>q.module_id===m.id);
    document.documentElement.style.setProperty("--accent",accent[m.accent]||"#1159ea");
    Array.from($("module-nav").children).forEach((b,i)=>b.setAttribute("aria-current",String(i===state.index)));
    const root=$("module-content");root.replaceChildren();
    const hero=el("header","module-hero");
    add(hero,el("div","kicker","MODULO "+String(state.index+1).padStart(2,"0")+" / 05"),
      heading("h2",m.title),paragraph(m.question),add(el("div","module-meta"),el("span","","4 ore previste"),el("span","","2 laboratori"),el("span","","Verifica interattiva")));
    add(root,hero);
    const outcomes=section("LEARNING OUTCOMES","Quello che saprai fare");
    add(outcomes,list(m.outcomes));add(root,outcomes,conceptProbe(scenario));
    const theory=section("TEORIA DOCUMENTATA","Capire prima di applicare");
    add(theory,paragraph(m.urgent_teacher_challenge,"subtle"));
    m.theory.paragraphs.forEach((p,i)=>{
      const details=el("details","theory-accordion");
      const summary=el("summary","",["Il concetto chiave","Quale rischio affrontiamo","Che cosa cambia nella lezione"][i]||"Approfondimento");
      add(details,summary,paragraph(p));add(theory,details);
    });
    const quote=el("div","quote");
    add(quote,el("b","",m.theory.pedagogical_reference.name+" — insegnamento applicato"),paragraph(m.theory.pedagogical_reference.insight),paragraph("Parafrasi contestualizzata MANZO AI, non citazione letterale.","subtle"),external(m.theory.pedagogical_reference.source,"Apri la fonte del riferimento pedagogico"));
    add(theory,quote);add(root,theory);
    const method=section("METODOLOGIA MANZO AI","Sette passaggi, una decisione responsabile");
    const grid=el("div","method-steps");
    state.course.methodology.seven_steps.forEach((s,i)=>{
      const step=el("div","method-step");
      add(step,el("span","",String(i+1).padStart(2,"0")),el("b","",s.label),el("small","",s.deliverable));add(grid,step);
    });
    add(method,grid,paragraph("Questo modello operativo non è una certificazione scientifica esterna; serve a documentare ogni scelta professionale.","subtle"));add(root,method);
    const labs=section("LABORATORI AUTENTICI","I problemi di oggi, affrontati in pratica");
    const cards=el("div","case-grid");
    m.professional_cases.forEach((c,i)=>{
      const p=el("div","case-card");
      add(p,el("div","section-kicker","LABORATORIO "+(i+1)),heading("h4",c.title),paragraph(c.situation),paragraph(c.task),el("p","case-foot","Output · "+c.artifact),paragraph("Condizione di sicurezza: "+c.redline,"subtle"));add(cards,p);
    });
    add(labs,cards);
    const link=el("a","full-lesson-link","Leggi il modulo completo con esercizi e soluzioni");
    const moduleNumber=String(state.index+1).padStart(2,"0");
    link.href=document.body.dataset.moduleBase ? document.body.dataset.moduleBase+moduleNumber+"/" : "../it/module-"+moduleNumber+".md";
    link.target="_blank";link.rel="noopener noreferrer";
    add(labs,paragraph("Il documento contiene consegne passo passo, esempi guidati, prompt e una guida di correzione.", "subtle"),link);add(root,labs,branchingSimulation(scenario));
    const assess=section("VERIFICA FORMATIVA","Metti alla prova il tuo giudizio");
    add(assess,paragraph("Le risposte rimangono solo in questa pagina durante la visita. Non c'è voto, salvataggio o attestato.","subtle"));
    m.checkpoint.forEach((q,i)=>add(assess,singleChoice(q,i+1)));
    add(assess,multiChoice(a.multi_select),scenario(a.decision_scenario),matching(a.matching),crossword(a.crossword));
    const performance=el("div","assessment-block");
    add(performance,heading("h4","Compito autentico"),paragraph(a.authentic_task.portfolio_artifact),
      paragraph("Produci l'artefatto su un documento tuo, usando solo casi sintetici. La valutazione finale richiede un revisore umano.","subtle"),
      heading("h4","Exit ticket"),paragraph(a.exit_ticket.question));
    add(assess,performance);add(root,assess);
    const sources=section("RIFERIMENTI VERIFICABILI","Le fonti di questa unità");
    const links=el("div","source-list");
    m.theory.sources.forEach((s,i)=>add(links,external(s.url,(i+1)+". "+s.title)));
    add(sources,links,paragraph("Riferimenti datati e soggetti a verifica editoriale prima di ogni erogazione.","subtle"));add(root,sources);
    root.focus({preventScroll:true});
  }
  function init(course,bank,scenarios) {
    if(!course||!bank||course.modules.length!==5||bank.modules.length!==5)throw Error("Contenuti formativi incompleti");
    const isEditorial=course.published===false&&course.status==="editorial_draft";
    const isPublic=course.published===true&&course.status==="public_beta"&&document.body.dataset.courseDataBase;
    if(!isEditorial&&!isPublic)throw Error("Stato di pubblicazione non riconosciuto");
    if(!scenarios||scenarios.modules.length!==5)throw Error("Simulazioni didattiche incomplete");
    state.course=course;state.bank=bank;state.scenarios=scenarios;
    const nav=$("module-nav");
    course.modules.forEach((m,i)=>{
      const b=el("button","nav-button");b.type="button";
      add(b,el("span","nav-number",String(i+1).padStart(2,"0")),el("span","nav-text",m.title));
      b.addEventListener("click",()=>{state.index=i;render();$("module-content").scrollIntoView({block:"start",behavior:"auto"})});
      add(nav,b);
    });
    $("experience").hidden=false;$("notice").hidden=true;render();
  }
  const dataBase=document.body.dataset.courseDataBase||"../it/";
  Promise.all([
    fetch(dataBase+"course.json").then(r=>{if(!r.ok)throw Error("corso HTTP "+r.status);return r.json()}),
    fetch(dataBase+"assessment-bank.json").then(r=>{if(!r.ok)throw Error("verifiche HTTP "+r.status);return r.json()}),
    fetch(dataBase+"scenarios.json").then(r=>{if(!r.ok)throw Error("simulazioni HTTP "+r.status);return r.json()})
  ]).then(d=>init(d[0],d[1],d[2])).catch(err=>{
    $("notice").textContent="Anteprima non disponibile: "+err.message+". Apri con un server HTTP locale dalla radice del repository; non usare file://.";
    $("notice").className="wrap notice";
  });
})();
