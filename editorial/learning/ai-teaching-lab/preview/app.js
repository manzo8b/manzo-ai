"use strict";
/* MANZO AI / AI Teaching Lab — isolated educational preview
 * Source content: ../it/course.json and ../it/assessment-bank.json
 * No cookies, API credentials, analytics, localStorage, or student data.
 * Quiz solutions live in a PUBLIC JSON: formative only, never an exam engine.
 */
(function () {
  const $ = (id) => document.getElementById(id);
  const accent = {cobalt:"#1159ea",violet:"#7547cb",coral:"#d84d30",emerald:"#077c61",teal:"#007a8b"};
  const state = {course:null,bank:null,scenarios:null,narrative:null,glossary:null,index:0};
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
    const block=el("section","assessment-block crossword-card");
    add(block,el("div","section-kicker","ALLENAMENTO DEL LESSICO"),heading("h4","Cruciverba delle competenze"),
      paragraph("Un vero cruciverba, con sette parole che si incrociano. Seleziona un indizio per evidenziare le caselle, scrivi una lettera per volta e controlla la soluzione. Su telefono puoi usare la modalità per parole.","subtle"));
    const status=el("p","crossword-status","Nessuna casella compilata");
    status.setAttribute("role","status");status.setAttribute("aria-live","polite");
    const toggles=el("div","toggle-row crossword-modes");
    const gridButton=control("Griglia",()=>switchMode("grid"),"secondary");
    const textButton=control("Elenco accessibile",()=>switchMode("text"),"secondary");
    add(toggles,gridButton,textButton);
    const gridLayout=el("div","crossword-grid-layout");
    const gridWrap=el("div","crossword-wrap");
    const hint=el("p","crossword-scroll-hint","La griglia scorre orizzontalmente se lo schermo è stretto");
    const grid=el("div","crossword");
    grid.style.setProperty("--grid-cols",String(item.width));
    const clues=el("div","crossword-clue-panel");
    add(clues,heading("h5","Indizi"),paragraph("Tocca un indizio per selezionare una parola","subtle"));
    const clueList=el("div","crossword-clues");
    add(clues,clueList);
    const cells={}, startNums={}, expected={};
    item.entries.forEach(e=>{
      startNums[e.row+","+e.col]=e.number;
      for(let i=0;i<e.answer.length;i++){
        const y=e.row+(e.direction==="down"?i:0),x=e.col+(e.direction==="across"?i:0);
        expected[y+","+x]=e.answer[i];
      }
    });
    let active=null,mode="grid";
    const normalize=s=>String(s||"").toUpperCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[^A-Z]/g,"");
    const keys=Object.keys(expected);
    function positions(entry){
      return [...entry.answer].map((_,i)=>entry.row+(entry.direction==="down"?i:0)+","+(entry.col+(entry.direction==="across"?i:0)));
    }
    function updateProgress(){
      const count=keys.filter(k=>Boolean(normalize(cells[k]?.value))).length;
      status.textContent=count+" caselle compilate su "+keys.length+" · "+item.entries.length+" indizi";
    }
    function selectEntry(entry,focus){
      active=entry;
      grid.querySelectorAll(".cross-cell.active").forEach(x=>x.classList.remove("active"));
      const coords=positions(entry);
      coords.forEach(k=>cells[k]?.parentElement?.classList.add("active"));
      clueList.querySelectorAll("button").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.word===entry.answer)));
      const first=coords.find(k=>!cells[k]?.value)||coords[0];
      if(focus!==false)cells[first]?.focus();
    }
    function advance(cellKey,delta){
      const entry=active||item.entries.find(e=>positions(e).includes(cellKey));
      if(!entry)return;
      const ps=positions(entry),at=ps.indexOf(cellKey),next=at+delta;
      if(next>=0&&next<ps.length)cells[ps[next]]?.focus();
    }
    item.pattern.forEach((row,y)=>[...row].forEach((ch,x)=>{
      if(ch==="#"){const wall=el("div","cross-cell cross-block");wall.setAttribute("aria-hidden","true");add(grid,wall);return}
      const k=y+","+x,box=el("div","cross-cell"),input=el("input","cross-input");
      input.type="text";input.inputMode="text";input.maxLength=1;input.autocomplete="off";input.spellcheck=false;
      input.setAttribute("aria-label","Riga "+(y+1)+", colonna "+(x+1)+(startNums[k]?", inizio parola "+startNums[k]:""));
      input.addEventListener("focus",()=>{
        if(!active||!positions(active).includes(k)){
          const first=item.entries.find(e=>positions(e).includes(k));if(first)selectEntry(first,false);
        }
      });
      input.addEventListener("click",()=>{
        const inCell=item.entries.filter(e=>positions(e).includes(k));
        if(inCell.length>1){
          const other=inCell.find(e=>e!==active)||inCell[0];selectEntry(other,false);
        }
      });
      input.addEventListener("input",()=>{
        input.value=normalize(input.value).slice(-1);
        updateProgress();
        if(input.value)advance(k,1);
      });
      input.addEventListener("keydown",ev=>{
        const directions={ArrowLeft:[0,-1],ArrowRight:[0,1],ArrowUp:[-1,0],ArrowDown:[1,0]};
        if(ev.key==="Backspace"&&!input.value){ev.preventDefault();advance(k,-1);return}
        if(!directions[ev.key])return;
        ev.preventDefault();const delta=directions[ev.key];
        let ny=y+delta[0],nx=x+delta[1];
        while(ny>=0&&ny<item.height&&nx>=0&&nx<item.width){
          if(cells[ny+","+nx]){cells[ny+","+nx].focus();return}
          ny+=delta[0];nx+=delta[1];
        }
      });
      if(startNums[k]!==undefined)add(box,el("span","cell-num",String(startNums[k])));
      cells[k]=input;add(box,input);add(grid,box);
    }));
    const textWrap=el("div","accessible-words");textWrap.hidden=true;
    const words=[];
    item.entries.forEach(entry=>{
      const btn=control(entry.number+" · "+(entry.direction==="across"?"Orizzontale":"Verticale")+" · "+entry.clue+" · "+entry.answer.length+" lettere",
        ()=>selectEntry(entry),"secondary");
      btn.className="crossword-clue";
      btn.dataset.word=entry.answer;btn.setAttribute("aria-pressed","false");
      add(clueList,btn);
      const row=el("div","word-field"),label=el("label","",
        entry.number+" "+(entry.direction==="across"?"orizzontale":"verticale")+" · "+entry.clue+" ("+entry.answer.length+" lettere)");
      const input=el("input","crossword-word-input");
      input.type="text";input.autocomplete="off";input.spellcheck=false;input.maxLength=entry.answer.length;
      input.id="word-"+entry.number+"-"+entry.direction;label.htmlFor=input.id;
      input.addEventListener("input",()=>{
        const letters=normalize(input.value).slice(0,entry.answer.length);
        input.value=letters;
        positions(entry).forEach((k,i)=>{if(letters[i]!==undefined)cells[k].value=letters[i]});
        updateProgress();
      });
      add(row,label,input);add(textWrap,row);words.push({answer:entry.answer,input});
    });
    add(gridWrap,grid,hint);add(gridLayout,gridWrap,clues);
    const actions=el("div","crossword-actions");
    const check=control("Controlla le risposte",()=>{
      if(mode==="grid"){
        const done=keys.filter(k=>normalize(cells[k].value)===expected[k]).length;
        feedback(block,done+" caselle corrette su "+keys.length+". Puoi correggere le altre senza ricominciare.",done===keys.length);
      }else{
        const count=words.filter(w=>normalize(w.input.value)===w.answer).length;
        feedback(block,count+" parole corrette su "+words.length+". Rileggi gli indizi e riprova.",count===words.length);
      }
    });
    // Maintain familiar named control for existing technical regressions.
    check.textContent="Verifica il cruciverba";
    const reset=control("Ricomincia",()=>{
      Object.values(cells).forEach(x=>{x.value="";x.parentElement.classList.remove("active")});
      words.forEach(w=>w.input.value="");
      const prior=block.querySelector(".result");if(prior)prior.remove();
      active=null;updateProgress();selectEntry(item.entries[0],false);
    },"secondary");
    add(actions,check,reset);
    function switchMode(next){
      mode=next;gridLayout.hidden=next!=="grid";textWrap.hidden=next!=="text";
      gridButton.setAttribute("aria-pressed",String(next==="grid"));
      textButton.setAttribute("aria-pressed",String(next==="text"));
      const result=block.querySelector(".result");if(result)result.remove();
      if(next==="grid")sizeGrid();
    }
    function sizeGrid(){
      if(!gridWrap.isConnected)return;
      const available=Math.max(280,gridWrap.getBoundingClientRect().width)-12;
      const size=Math.max(22,Math.min(39,Math.floor((available-2*(item.width-1))/item.width)));
      grid.style.setProperty("--cell-size",size+"px");
    }
    add(block,toggles,status,gridLayout,textWrap,actions);
    updateProgress();selectEntry(item.entries[0],false);switchMode("grid");
    if(typeof ResizeObserver!=="undefined")new ResizeObserver(sizeGrid).observe(gridWrap);
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
  function renderGlossary(g) {
    const area=$("atl-final-glossary"),list=$("atl-term-list"),count=$("atl-term-count");
    const search=$("atl-term-search"),group=$("atl-term-group");
    if(!area||!list||!count||!search||!group)return;
    if(!g||g.entries.length<40)throw Error("Vocabolario incompleto");
    const link=area.querySelector("[data-atl-glossary-page]");
    if(link)link.hidden=!document.body.dataset.moduleBase;
    g.categories.forEach(name=>{const option=el("option","",name);option.value=name;add(group,option)});
    const normalize=(value)=>String(value||"").normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLocaleLowerCase("it").trim();
    function apply(){
      const term=normalize(search.value),category=group.value;
      const matches=g.entries.filter(t=>(!category||t.category===category)&&
        (!term||normalize(t.term+" "+t.definition+" "+t.classroom_example).includes(term)));
      list.replaceChildren();
      count.textContent=matches.length+" voci trovate su "+g.entries.length;
      if(!matches.length){
        add(list,paragraph("Nessun termine corrisponde alla ricerca. Prova una parola più generale.","glossary-empty"));return;
      }
      matches.forEach(item=>{
        const card=el("article","term-card");
        add(card,el("div","term-group",item.category),heading("h3",item.term),
          paragraph(item.definition),add(el("div","term-example"),
            el("b","","Nella pratica scolastica"),paragraph(item.classroom_example)));
        if(item.source)add(card,external(item.source,"Approfondisci dalla fonte"));
        add(list,card);
      });
    }
    search.addEventListener("input",apply);
    group.addEventListener("change",apply);
    apply();
    area.hidden=false;
  }
  function courseInAction(){
    const p=section("DIDATTICA APPLICATA","Questo corso mette in pratica ciò che insegna");
    add(p,paragraph("Non si limita a descrivere l'IA: il modo stesso in cui studi è un modello didattico. L'IA è oggetto di analisi e uno strumento facoltativo per produrre bozze, mentre spiegazione, confronto e giudizio rimangono tuoi."));
    const steps=el("div","applied-pedagogy");
    [
      ["Problema concreto","Parti da una situazione che un docente riconosce"],
      ["Spiegazione narrativa","Comprendi la teoria attraverso una storia coerente e fonti"],
      ["Esempio svolto","Osservi un output simulato e che cosa correggere"],
      ["Laboratorio","Scrivi un prompt, oppure lavori sul materiale senza IA"],
      ["Verifica e revisione","Ricevi feedback, correggi e trasferisci la scelta in classe"]
    ].forEach(([title,desc],i)=>{
      const cell=el("div","applied-step");
      add(cell,el("span","",String(i+1).padStart(2,"0")),el("b","",title),paragraph(desc));add(steps,cell);
    });
    add(p,steps,paragraph("Il percorso non attiva in segreto un'intelligenza artificiale: gli esempi sono materiali formativi preparati e verificabili. Quando vorrai sperimentare con un sistema esterno, usane uno autorizzato, evitando dati personali degli studenti.","subtle"));
    return p;
  }

  /* A practical exercise in every module. All processing is local: these
     are deterministic teacher-led demonstrations, NOT live AI models. */
  function professionalStudio(story){
    const f=story.focus_experience;
    if(!f)return el("div");
    const sectionBox=section("METTI IN PRATICA",f.label);
    sectionBox.className+=" competency-studio";
    sectionBox.id="atl-competence";
    add(sectionBox,paragraph("Un'esperienza da integrare nei due laboratori già previsti: non richiede ore aggiuntive né un account.","subtle"));
    add(sectionBox,add(el("div","competency-context"),
      el("b","","Il problema professionale"),paragraph(f.context),
      el("b","","Il risultato da raggiungere"),paragraph(f.objective)));
    const steps=el("details","competency-steps");
    add(steps,el("summary","","Come si svolge · "+f.steps.length+" passaggi"),list(f.steps,true));
    add(sectionBox,steps);

    if(f.type==="model_test"){
      const demo=el("div","competency-interaction demo-model");
      add(demo,heading("h4","Quale regola generalizza sui nuovi esempi?"),
        paragraph("Il gioco usa otto schede inventate per ricavare una regola di maggioranza e quattro casi non visti per metterla alla prova. Non addestra un vero modello linguistico.","subtle"));
      const field=el("fieldset","competency-field");
      add(field,el("legend","","Quale caratteristica deve usare la regola?"));
      ["color","shape"].forEach((kind,i)=>{
        const lab=el("label","choice");
        const inp=el("input");inp.type="radio";inp.name="demo-feature";inp.value=kind;
        if(i===0)inp.checked=true;
        add(lab,inp,el("span","",kind==="color"?"Colore: blu o rosso":"Forma: triangolo o cerchio"));
        add(field,lab);
      });
      const results=el("div","model-results");
      add(demo,field,control("Prova le quattro schede nuove",()=>{
        const key=field.querySelector("input:checked").value;
        const mapped={};
        f.demo.training.forEach(ex=>{
          const value=ex[key];mapped[value]??={};mapped[value][ex.label]=(mapped[value][ex.label]||0)+1;
        });
        const predict=ex=>{
          const votes=mapped[ex[key]]||{};
          return Object.keys(votes).sort((a,b)=>votes[b]-votes[a]||a.localeCompare(b))[0]||"nessuna";
        };
        const grid=el("div","model-test-grid");
        let correct=0;
        f.demo.test.forEach((ex,i)=>{
          const pred=predict(ex),ok=pred===ex.label;
          if(ok)correct++;
          const row=el("div","model-test-card"+(ok?" model-correct":" model-wrong"));
          add(row,el("span","model-icon",""+(ex.shape==="triangolo"?"△":"◯")),
            el("b","","Caso nuovo "+(i+1)),
            paragraph(ex.shape+" "+ex.color+" · previsione: "+pred+" · "+(ok?"corretta":"da correggere")));
          add(grid,row);
        });
        results.replaceChildren(grid);
        feedback(demo,"Risultato su dati nuovi: "+correct+"/4. Sul training entrambe le regole sembravano corrette; solo il test rivela se la caratteristica scelta generalizza. È un gioco con regole fisse, non un LLM.",correct===4);
      }),results);
      add(sectionBox,demo);
    }
    if(f.type==="multimedia_design"){
      const studio=el("div","competency-interaction media-creator");

      const guide=story.generative_model_guide;
      if(guide){
        const panel=el("section","model-selection-guide");
        add(panel,el("div","model-selection-eyebrow","PRIMA DI GENERARE"),
          heading("h4",guide.heading),paragraph(guide.introduction),
          paragraph(guide.no_absolute_winner,"subtle"));
        const chooser=el("div","model-choice-controls");
        const label=el("label","media-label","Che cosa vuoi progettare?");
        label.htmlFor="atl-model-media";
        const kind=el("select","media-select");kind.id="atl-model-media";
        guide.rows.forEach((item,i)=>{const op=el("option","",item.name);op.value=String(i);add(kind,op)});
        const details=el("div","model-choice-detail");
        const rationale=el("textarea","competency-reason");
        rationale.rows=3;
        rationale.maxLength=500;
        rationale.placeholder="Perché useresti questa soluzione? Indica la prova da verificare e un limite da conoscere";
        rationale.setAttribute("aria-label","Motivazione della scelta del modello o dello strumento");
        function showModel(){
          const item=guide.rows[Number(kind.value)]||guide.rows[0];
          details.replaceChildren();
          add(details,heading("h5",item.name));
          const cols=el("div","model-choice-columns");
          const mk=(title,items)=>{
            const box=el("div","model-choice-column");
            add(box,el("b","",title),list(items));
            return box;
          };
          add(cols,mk("Modelli o famiglie",item.model_examples),
            mk("Applicazioni o strumenti",item.product_examples));
          add(details,cols,
            add(el("div","model-choice-why"),el("b","","Quando possono aiutare"),paragraph(item.why)),
            add(el("div","model-choice-verify"),el("b","","Cosa controllare"),paragraph(item.review)),
            add(el("div","model-source-links"),
              external(item.source,"Documentazione ufficiale"),
              external(item.other_source,"Altra fonte pertinente")));
          rationale.value="";
        }
        kind.value="0";kind.addEventListener("change",showModel);showModel();
        const rationaleLabel=el("label","media-label","Scrivi la tua decisione e un criterio di verifica");
        rationale.id="atl-model-rationale";rationaleLabel.htmlFor=rationale.id;
        add(chooser,label,kind,details,rationaleLabel,rationale,
          control("Confronta la mia scelta",()=>{
            const text=rationale.value.trim();
            if(text.length<35){feedback(chooser,"Motiva la scelta con almeno una frase su obiettivo, controllo e limiti.");return}
            feedback(chooser,"Buona prima ipotesi. Ora confronta due alternative con lo stesso brief. Verifica fedeltà al contenuto, correggibilità, licenze, accessibilità, privacy, costo e piano senza IA. Il nome del prodotto non è una garanzia di efficacia.",true);
          }));
        add(panel,chooser);
        const criteria=el("details","model-criteria");
        add(criteria,el("summary","","Sei criteri per confrontare le alternative"),list(guide.decision_criteria,true));
        add(panel,criteria);
        add(studio,panel);
      }
      const openStudio=el("a","studio-open-action","Apri il laboratorio completo · crea ed esporta il tuo kit ↗");
      openStudio.href="./laboratorio-multimediale/";
      add(studio,openStudio);
      add(studio,heading("h4","Studio multimediale · costruisci lo storyboard"),
        paragraph("Prima definisci l'apprendimento e la fonte, poi scegli come raccontarlo. La traccia è costruita nel tuo browser: nessuna IA viene interrogata e nessun dato viene inviato.","subtle"));
      const form=el("div","media-brief");
      const inputs=[
        ["Destinatari","Seconda media"],
        ["Obiettivo osservabile","Distinguere un evento meteorologico da una tendenza climatica"],
        ["Concetto da spiegare","Un giorno di freddo non basta per descrivere il clima"],
        ["Fonte da verificare","Inserirò una fonte scientifica verificata prima della pubblicazione"]
      ];
      const fields={};
      inputs.forEach(([title,value],i)=>{
        const lab=el("label","media-label",title);
        const input=el("input","media-input");input.type="text";input.value=value;input.maxLength=250;
        input.id="media-input-"+i;lab.htmlFor=input.id;
        fields[i]=input;
        add(form,lab,input);
      });
      const formatLabel=el("label","media-label","Formato principale");
      const select=el("select","media-select");
      [["slide","Slide"],["audio","Podcast / audio"],["video","Microvideo"],["interactive","Scelta interattiva"]].forEach(([val,title])=>{
        const op=el("option","",title);op.value=val;add(select,op);
      });
      select.id="media-kind";formatLabel.htmlFor=select.id;
      add(form,formatLabel,select);add(studio,form);
      const output=el("div","media-storyboard-output");
      let generated="";
      add(studio,control("Costruisci la scaletta didattica",()=>{
        const audience=fields[0].value.trim(),goal=fields[1].value.trim(),
        concept=fields[2].value.trim(),source=fields[3].value.trim();
        if(!audience||!goal||!concept||!source){
          feedback(studio,"Compila tutti e quattro i campi prima di creare la scaletta.");return;
        }
        const kind=select.value;
        const blueprint=story.media_blueprints.find(x=>x.kind===kind);
        const act=kind==="interactive"?"Decisione 1 → feedback motivato → secondo tentativo":
          kind==="audio"?"Voce 1: dubbio · Voce 2: prova · Trascrizione integrale":
          kind==="video"?"Scena 1: dubbio · Scena 2: evidenza · Scena 3: verifica, con sottotitoli":
          "Slide 1: dubbio · Slide 2: evidenza · Slide 3: verifica";
        generated="DESTINATARI: "+audience+"\nOBIETTIVO: "+goal+
          "\nCONCETTO: "+concept+"\nFONTE DA CONTROLLARE: "+source+
          "\nFORMATO: "+select.selectedOptions[0].textContent+
          (guide?"\nOPZIONI DI MODELLO/SERVIZIO DA CONFRONTARE: "+(guide.rows[Number(studio.querySelector("#atl-model-media")?.value||0)]||guide.rows[0]).model_examples.join("; "):"")+
          "\nSTORYBOARD: "+act+"\nDOMANDA AGLI STUDENTI: Che cosa puoi concludere dalle prove disponibili?"+
          "\nFEEDBACK: Chiedi quale fonte manca, spiega il criterio e invita alla revisione."+
          "\nACCESSIBILITÀ: "+blueprint.accessibility+
          "\nCONTROLLO: accuratezza, carico cognitivo, licenze, rappresentazioni equivalenti e alternativa senza IA.";
        output.replaceChildren(
          heading("h5","Scaletta da verificare e adattare"),
          el("pre","media-generated",generated),
          paragraph("È un modello di progettazione compilato con i tuoi dati, non un prodotto audio o video né un testo generato da IA.","subtle"));
        feedback(studio,"Scaletta costruita localmente. Controlla fonti, consegne e accessibilità prima di utilizzarla.",true);
      }),control("Copia la scaletta",async()=>{
        if(!generated){feedback(studio,"Crea prima la scaletta.");return}
        try{await navigator.clipboard.writeText(generated);feedback(studio,"Scaletta copiata.",true)}
        catch(_){feedback(studio,"Seleziona manualmente la scaletta per copiarla: resta visibile qui sotto.")}
      },"secondary"),output);
      const principles=el("div","media-principles");
      add(principles,heading("h4","Sei decisioni per una risorsa che fa imparare"));
      story.multimedia_design_principles.forEach((p,i)=>{
        const cell=el("article","media-principle-card");
        add(cell,el("span","",String(i+1).padStart(2,"0")),
          heading("h5",p.name),paragraph(p.why),el("small","",p.do));
        add(principles,cell);
      });
      add(sectionBox,studio,principles);
    }
    if(f.type==="branching_path"){
      const branch=el("div","competency-interaction practice-branch");
      add(branch,heading("h4","Tre scelte, tre conseguenze"),
        paragraph("Prova uno scenario ramificato con feedback deterministico: il codice segue regole decise dal docente, non usa un tutor IA.","subtle"));
      const result=el("div","branch-feedback");
      f.branches.forEach((item,i)=>{
        const b=control(item.choice,()=>{
          result.replaceChildren(
            el("b","","Conseguenza della scelta "+(i+1)),
            paragraph(item.feedback),
            paragraph("Per correggere o approfondire, torna all'affermazione iniziale e confronta il documento originale.","subtle"));
        },"secondary");
        add(branch,b);
      });
      add(branch,result);add(sectionBox,branch);
    }
    if(f.type==="decision_matrix"||f.type==="inclusive_feedback"){
      const demo=el("div","competency-interaction option-board");
      if(f.type==="decision_matrix"){
        add(demo,heading("h4","Quale soluzione sceglieresti?"));
        const sel=el("select","competency-select");
        ["Attività senza IA","Assistente generalista","Assistente su documenti","Editor multimediale"].forEach(s=>{const op=el("option","",s);add(sel,op)});
        const reason=el("textarea","competency-reason");reason.rows=3;reason.placeholder="Motiva la scelta con obiettivo, dati, limiti e una prova di apprendimento";
        reason.setAttribute("aria-label","Motivazione della scelta didattica");
        add(demo,sel,reason,control("Verifica i miei criteri",()=>{
          if(reason.value.trim().length<35){feedback(demo,"Spiega il motivo in almeno una frase completa e indica come verificheresti la scelta.");return}
          feedback(demo,"Confronta la tua scelta con la matrice: competenza osservabile, affidabilità, privacy e autorizzazioni, accessibilità, costi, tempo di revisione e piano senza IA. Se un vincolo sui dati non è rispettato, la scelta va esclusa.");
        }));
      }else{
        add(demo,heading("h4","Stessa competenza, più modalità"),
          paragraph("Scegli quale prova vuoi progettare, poi confrontala con criteri uguali per tutti.","subtle"));
        ["Testo con scaletta","Mappa descritta e commentata","Esposizione orale con appunti"].forEach((name,i)=>{
          add(demo,control(name,()=>feedback(demo,
            "Modalità "+(i+1)+": mantieni sempre correttezza delle cause, pertinenza delle prove e possibilità di revisione. Non dedurre diagnosi o capacità fisse dalla scelta del formato.",true),"secondary"));
        });
      }
      add(sectionBox,demo);
    }
    const prompt=el("details","studio-prompt");
    const bar=el("div","lab-prompt-head");
    add(bar,el("strong","","Prompt da adattare"));
    add(prompt,el("summary","","Leggi il prompt completo"),bar,add(el("pre","lab-prompt-code"),el("code","",f.prompt)));
    add(sectionBox,prompt);
    const checklist=el("div","studio-checklist");
    add(checklist,heading("h4","Prima di consegnare"));
    f.criteria.forEach((t,i)=>{
      const label=el("label","studio-check");
      const check=el("input");check.type="checkbox";
      add(label,check,el("span","",t));add(checklist,label);
    });
    const artifact=el("p","competency-deliverable");add(artifact,el("b","","Portfolio: "),el("span","",f.deliverable));
    add(sectionBox,checklist,artifact);
    const item={...f.quiz,id:"focus-"+story.id};
    add(sectionBox,singleChoice(item,1));
    const refs=el("div","studio-references");
    add(refs,heading("h4","Per approfondire"));
    f.references.forEach(x=>add(refs,external(x.url,x.title)));
    add(sectionBox,refs);
    return sectionBox;
  }


  /* Disclosure-first reading: short mobile/desktop pages with intact learning objects. */
  function revealCourseSection(targetId,scroll=true){
    const target=$(targetId);
    if(!target)return;
    const fold=target.closest(".course-fold");
    if(fold){
      const article=$("module-content");
      article?.querySelectorAll(".course-fold[open]").forEach(other=>{
        if(other!==fold)other.open=false;
      });
      fold.open=true;
    }
    if(scroll)(fold||target).scrollIntoView({block:"start",behavior:"smooth"});
  }
  function organiseCourseSections(root){
    const panels=[...root.querySelectorAll(":scope > section.panel")];
    if(!panels.length)return;
    const picker=el("div","course-section-picker");
    const label=el("label","", "Vai alla sezione");
    const select=el("select","course-section-select");
    select.id="atl-section-select";
    label.htmlFor=select.id;
    add(picker,label,select);
    panels.forEach((panel,i)=>{
      const targetId=panel.id||"atl-extra-section-"+String(i+1).padStart(2,"0");
      panel.id=targetId;
      const h=panel.querySelector(":scope > h3");
      const eyebrow=panel.querySelector(":scope > .section-kicker");
      const title=h?.textContent?.trim()||"Attività";
      const fold=el("details","course-fold");
      fold.dataset.section=targetId;
      const heading=el("summary","course-fold-heading");
      add(heading,
        el("span","course-fold-number",String(i+1).padStart(2,"0")),
        add(el("span","course-fold-label"),el("strong","",title),el("small","",eyebrow?.textContent||"")),
        el("span","course-fold-arrow","⌄"));
      panel.replaceWith(fold);
      add(fold,heading,panel);
      if(i===0)fold.open=true;
      const option=el("option","",String(i+1).padStart(2,"0")+" · "+title);
      option.value=targetId;
      add(select,option);
      fold.addEventListener("toggle",()=>{
        if(!fold.open)return;
        root.querySelectorAll(".course-fold[open]").forEach(other=>{
          if(other!==fold)other.open=false;
        });
        select.value=targetId;
      });
    });
    select.addEventListener("change",()=>revealCourseSection(select.value,true));
    root.insertBefore(picker,root.querySelector(".course-fold"));
  }
  function render() {
    const m=state.course.modules[state.index],
          a=state.bank.modules.find(q=>q.module_id===m.id),
          story=state.narrative.modules.find(q=>q.id===m.id),
          decision=state.scenarios.modules.find(q=>q.module_id===m.id);
    if(!m||!a||!story||!decision)throw Error("Il modulo non è completo");
    document.documentElement.style.setProperty("--accent",accent[m.accent]||"#1159ea");
    Array.from($("module-nav").children).forEach((b,i)=>b.setAttribute("aria-current",String(i===state.index)));
    const root=$("module-content");root.replaceChildren();
    const hero=el("header","module-hero");
    add(hero,el("div","kicker","PERCORSO DOCENTI · MODULO "+String(state.index+1).padStart(2,"0")+" / 05"),
      heading("h2",m.title),
      paragraph(story.subtitle,"module-subtitle"),
      add(el("div","module-meta"),el("span","","Studio autonomo"),el("span","","2 laboratori guidati"),el("span","","4 ore indicative")));
    add(root,hero);
    const roadmap=el("nav","course-session-map");
    roadmap.setAttribute("aria-label","Attività del modulo");
    const parts=[
      ["Video e orientamento","#atl-start","00"],
      ["Lettura di approfondimento","#atl-theory","01"],
      ["Laboratori","#atl-labs","02"],
      ["Verifica e riflessione","#atl-quiz","03"]
    ];
    parts.forEach(([label,url,num])=>{
      const a=el("a","course-session-step");
      a.href=url;
      add(a,el("span","course-session-number",num),el("span","",label));
      add(roadmap,a);
    });
    roadmap.querySelectorAll("a[href^='#']").forEach(link=>{
      link.addEventListener("click",event=>{
        event.preventDefault();revealCourseSection(link.getAttribute("href").slice(1));
      });
    });
    const quick=el("details","course-roadmap-disclosure");
    add(quick,el("summary","","Percorso rapido · 4 attività"),roadmap);
    add(root,quick);

    const welcome=section("COME INIZIARE","Qui impari anche da solo");
    welcome.id="atl-start";
    add(welcome,paragraph("Puoi studiare senza un formatore e senza conoscenze di programmazione. Segui il racconto, svolgi i laboratori usando soltanto esempi inventati, controlla i risultati e verifica la comprensione. Non serve un account per leggere il corso."));
    const startSteps=el("div","self-study-steps");
    [
      ["01","Leggi","Comincia dalla storia e dalle spiegazioni. Se incontri parole nuove, consulta il glossario"],
      ["02","Sperimenta","Copia il prompt pronto in uno strumento autorizzato, oppure analizza l'esempio simulato"],
      ["03","Verifica","Correggi la bozza e confronta le risposte nelle attività interattive"]
    ].forEach(([no,title,description])=>{
      const card=el("div","self-study-step");
      add(card,el("span","self-step-no",no),el("b","",title),paragraph(description));add(startSteps,card);
    });
    add(welcome,startSteps);
    const goals=el("div","study-goals");
    add(goals,heading("h4","Dopo questa lezione saprai"),
      list(m.outcomes));
    add(welcome,goals);
    add(root,welcome,courseInAction(),conceptProbe(decision));

    const theory=section("LETTURA DI APPROFONDIMENTO","Una storia da seguire, non una successione di definizioni");
    theory.id="atl-theory";
    add(theory,paragraph(story.lead,"narrative-intro"));
    story.chapters.forEach((chapter,i)=>{
      const segment=el("section","narrative-chapter");
      add(segment,heading("h4",chapter.heading));
      chapter.text.split(/\n\n+/).forEach(text=>add(segment,paragraph(text)));
      if(chapter.transition)add(segment,paragraph(chapter.transition,"narrative-bridge"));
      add(theory,segment);
    });
    const pedagogy=el("div","pedagogy-note");
    add(pedagogy,heading("h4","Un riferimento pedagogico da approfondire"),
      paragraph(m.theory.pedagogical_reference.name+" — "+m.theory.pedagogical_reference.insight),
      paragraph("Si tratta di una parafrasi didattica, non di una citazione letterale.","subtle"),
      external(m.theory.pedagogical_reference.source,"Leggi il riferimento"));
    add(theory,pedagogy);add(root,theory);

    const glossary=section("PAROLE CHIARE","Un piccolo vocabolario per orientarsi");
    glossary.id="atl-terms";
    add(glossary,paragraph("Non occorre conoscere in anticipo queste espressioni. Puoi tornare al glossario in qualunque momento.","subtle"));
    const gridGloss=el("dl","glossary-grid");
    story.glossary.forEach(([term,definition])=>{
      const item=el("div","glossary-item");add(item,el("dt","",term),el("dd","",definition));add(gridGloss,item);
    });
    add(glossary,gridGloss);add(root,glossary);

    const method=section("PROPOSTA DI METODO","Come può aiutarci il metodo MANZO AI");
    method.id="atl-method";
    add(method,paragraph("MANZO AI propone sette domande per progettare, usare e controllare l'IA con senso didattico. È un percorso operativo sviluppato dal progetto MANZO AI: non è un obbligo, non sostituisce l'esperienza del docente e non è una teoria già validata attraverso studi sperimentali."));
    const methodGrid=el("div","method-steps");
    const descriptions=[
      "Che problema concreto devo affrontare?",
      "A quale classe e obiettivo mi rivolgo?",
      "Quali errori, dati o barriere devo prevenire?",
      "Che cosa devo chiarire prima di procedere?",
      "Quale attività e quale prompt possono aiutarmi?",
      "Come controllo fatti, accessibilità e apprendimento?",
      "Che cosa consegno e di quali limiti sono responsabile?"
    ];
    state.course.methodology.seven_steps.forEach((s,i)=>{
      const step=el("div","method-step");
      add(step,el("span","",String(i+1).padStart(2,"0")),el("b","",s.label),
        el("small","",descriptions[i]));add(methodGrid,step);
    });
    add(method,methodGrid,paragraph("Puoi modificare o non usare uno strumento IA se non risponde al bisogno didattico. Questo è un risultato professionale, non un errore.","subtle"));
    add(root,method);

    const labs=section("APPLICARE","Laboratori da fare, non soltanto da leggere");
    labs.id="atl-labs";
    add(labs,paragraph("Sei tu il partecipante. Ogni laboratorio contiene situazione, obiettivo, passi numerati, prompt pronto, esempio simulato e controllo. Puoi usare carta e penna: non è obbligatorio accedere a un sistema esterno.","subtle"));
    const cards=el("div","case-grid");
    story.labs.forEach((lab,i)=>{
      const card=el("article","case-card lab-card");
      add(card,el("div","lab-art","0"+(i+1)+" / LABORATORIO"),
        heading("h4",lab.title),paragraph(lab.situation),
        add(el("div","lab-goal"),el("b","","Che cosa devi ottenere"),paragraph(lab.goal)));
      const steps=el("div","lab-steps");
      add(steps,heading("h5","Che cosa fare, passo dopo passo"),list(lab.steps,true));
      add(card,steps);
      const promptSection=el("div","lab-prompt");
      const bar=el("div","lab-prompt-head");
      add(bar,el("strong","","Prompt pronto da provare"),
        control("Copia il prompt",async()=>{
          try{
            if(!navigator.clipboard?.writeText)throw Error("clipboard unsupported");
            await navigator.clipboard.writeText(lab.prompt);
            feedback(promptSection,"Prompt copiato. Personalizzalo solo con dati inventati.",true);
          }catch(_){feedback(promptSection,"Seleziona e copia il testo manualmente. Il prompt rimane leggibile qui sotto.");}
        },"secondary"));
      add(promptSection,bar,add(el("pre","lab-prompt-code"),el("code","",lab.prompt)),
        paragraph("Non hai uno strumento autorizzato? Usa l'esempio simulato qui sotto per completare ugualmente il laboratorio.","subtle"));
      add(card,promptSection);
      const example=el("details","lab-example");
      add(example,el("summary","","Guarda un esempio svolto (dopo aver provato)"),
        paragraph("Esempio creato per la lezione, non risultato di un assistente interrogato in diretta.","subtle"),
        el("blockquote","",lab.sample));
      add(card,example);
      const review=el("div","lab-review");
      add(review,heading("h5","Controlla la qualità del risultato"),paragraph(lab.check),
        el("p","lab-deliverable","Da conservare nel tuo portfolio: "+lab.deliverable));
      add(card,review);add(cards,card);
    });
    add(labs,cards);
    add(labs,professionalStudio(story));
    const link=el("a","full-lesson-link","Apri la lezione completa in formato lettura");
    const moduleNumber=String(state.index+1).padStart(2,"0");
    link.href=document.body.dataset.moduleBase ? document.body.dataset.moduleBase+moduleNumber+"/" : "../it/module-"+moduleNumber+".md";
    link.target=document.body.dataset.moduleBase?"_self":"_blank";link.rel="noopener noreferrer";
    add(labs,paragraph("Preferisci leggere tutto come un capitolo continuo? Apri la versione integrale, con fonti e istruzioni anche per chi studia in autonomia.","subtle"),link);
    add(root,labs);

    const simulation=branchingSimulation(decision);
    simulation.id="atl-decision";
    add(root,simulation);

    const assess=section("VALUTARE","Verifica ciò che hai imparato");
    assess.id="atl-quiz";
    add(assess,paragraph("Dopo le attività, rispondi alle domande e completa il cruciverba. Il feedback appare soltanto dopo il tuo tentativo. Nessun voto o avanzamento viene registrato.","subtle"));
    m.checkpoint.forEach((q,i)=>add(assess,singleChoice(q,i+1)));
    add(assess,multiChoice(a.multi_select),scenario(a.decision_scenario),matching(a.matching),crossword(a.crossword));
    const performance=el("div","assessment-block");
    add(performance,heading("h4","Il tuo compito di conclusione"),
      paragraph(a.authentic_task.portfolio_artifact),
      paragraph("Prepara il materiale nel tuo documento personale, usando dati inventati; confronta quello che hai prodotto con l'obiettivo iniziale.","subtle"),
      heading("h4","Una domanda da portare in classe"),paragraph(a.exit_ticket.question));
    add(assess,performance);add(root,assess);

    const sources=section("APPROFONDIRE","Fonti e letture per continuare");
    sources.id="atl-sources";
    const links=el("div","source-list");
    m.theory.sources.forEach((s,i)=>add(links,external(s.url,(i+1)+". "+s.title)));
    add(sources,paragraph("Le fonti aiutano a distinguere i principi di ricerca dalle proposte operative di MANZO AI. Le situazioni dei laboratori sono esercitazioni inventate, non dati di ricerca."),links);
    add(root,sources);
    const bridge=story.bridge_to_next;
    if(bridge){
      const closing=section("PER CONTINUARE","Il prossimo passo nasce da ciò che hai imparato");
      closing.className+=" course-next-section";
      add(closing,paragraph(bridge.back,"course-next-story"),
        add(el("div","course-next-question"),el("b","","Riflessione"),paragraph(bridge.prompt)));
      if(state.index<state.course.modules.length-1){
        const nextButton=control("Prosegui · "+state.course.modules[state.index+1].title,()=>{
          state.index++;render();
          $("module-content").scrollIntoView({block:"start",behavior:"auto"});
        });
        nextButton.className+=" course-next-action";
        add(closing,nextButton);
      }else{
        add(closing,paragraph("Hai attraversato tutte le letture. Scegli un problema della tua didattica, prepara una proposta verificabile e consulta il vocabolario quando incontri un termine nuovo.","subtle"));
      }
      add(root,closing);
    }
    organiseCourseSections(root);
    // Deep links should also reveal content initially hidden in a section.
    const hash=decodeURIComponent(location.hash||"").replace(/^#/,"");
    if(hash&&$(hash)?.closest(".course-fold"))revealCourseSection(hash,false);
    root.focus({preventScroll:true});
  }
  function init(course,bank,scenarios,narrative,glossary) {
    if(!course||!bank||course.modules.length!==5||bank.modules.length!==5)throw Error("Contenuti formativi incompleti");
    const isEditorial=course.published===false&&course.status==="editorial_draft";
    const isPublic=course.published===true&&course.status==="public_beta"&&document.body.dataset.courseDataBase;
    if(!isEditorial&&!isPublic)throw Error("Stato di pubblicazione non riconosciuto");
    if(!scenarios||scenarios.modules.length!==5)throw Error("Simulazioni didattiche incomplete");
    if(!narrative||narrative.modules.length!==5)throw Error("Materiali narrativi mancanti");
    state.course=course;state.bank=bank;state.scenarios=scenarios;state.narrative=narrative;state.glossary=glossary;
    const nav=$("module-nav");
    course.modules.forEach((m,i)=>{
      const story=narrative.modules.find(t=>t.id===m.id);
      const entry=el("div","module-nav-entry");
      const b=el("button","nav-button");b.type="button";
      add(b,el("span","nav-number",String(i+1).padStart(2,"0")),
        el("span","nav-text",m.title));
      b.addEventListener("click",()=>{state.index=i;render();
        $("module-content").scrollIntoView({block:"start",behavior:"auto"})});
      add(entry,b);
      const details=el("details","module-outline");
      const summary=el("summary","","Che cosa farai · 4 attività");
      add(details,summary);
      const items=el("ol","module-outline-items");
      [
        {name:"Lettura di approfondimento",time:"48 min",target:"atl-theory"},
        {name:"Laboratorio · Prima sperimentazione",time:"72 min",target:"atl-labs"},
        {name:"Laboratorio · Revisione",time:"72 min",target:"atl-labs"},
        {name:"Verifica e riflessione",time:"48 min",target:"atl-quiz"}
      ].forEach((activity,j)=>{
        const a=el("a","module-outline-link");
        a.href="#"+activity.target;
        add(a,el("span","",activity.name),el("small","",activity.time));
        a.addEventListener("click",ev=>{
          ev.preventDefault();state.index=i;render();
          revealCourseSection(activity.target);
        });
        add(items,add(el("li"),a));
      });
      add(details,items);
      add(entry,details);add(nav,entry);
    });
    const sidebar=document.querySelector("#experience .course-side");
    if(sidebar&&!sidebar.querySelector(".course-side-disclosure")){
      const disclosure=el("details","course-side-disclosure");
      const summary=el("summary","course-side-disclosure-title","Scegli il modulo e consulta le risorse");
      const contents=[...sidebar.children];
      sidebar.append(disclosure);
      add(disclosure,summary,...contents);
      const responsive=window.matchMedia("(max-width:800px)");
      const setSidebar=()=>{disclosure.open=!responsive.matches};
      setSidebar();
      if(responsive.addEventListener)responsive.addEventListener("change",setSidebar);
      else if(responsive.addListener)responsive.addListener(setSidebar);
    }
    $("experience").hidden=false;$("notice").hidden=true;render();renderGlossary(glossary);
  }
  const dataBase=document.body.dataset.courseDataBase||"../it/";
  Promise.all([
    fetch(dataBase+"course.json").then(r=>{if(!r.ok)throw Error("corso HTTP "+r.status);return r.json()}),
    fetch(dataBase+"assessment-bank.json").then(r=>{if(!r.ok)throw Error("verifiche HTTP "+r.status);return r.json()}),
    fetch(dataBase+"scenarios.json").then(r=>{if(!r.ok)throw Error("simulazioni HTTP "+r.status);return r.json()}),
    fetch(dataBase+"narrative.json").then(r=>{if(!r.ok)throw Error("narrazione HTTP "+r.status);return r.json()}),
    fetch(dataBase+"glossary.json").then(r=>{if(!r.ok)throw Error("vocabolario HTTP "+r.status);return r.json()})
  ]).then(d=>init(d[0],d[1],d[2],d[3],d[4])).catch(err=>{
    $("notice").textContent="Anteprima non disponibile: "+err.message+". Apri con un server HTTP locale dalla radice del repository; non usare file://.";
    $("notice").className="wrap notice";
  });
})();
