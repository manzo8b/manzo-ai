"use strict";
/* MANZO AI — multimedia production studio.
   Everything stays in this browser tab until the teacher exports a local file.
   No AI API, tracking, server upload, accounts or automatic evaluation. */
(function(){
  const $=id=>document.getElementById(id);
  const form=$("studio-form");
  const phases=[...document.querySelectorAll(".studio-phase")];
  const buttons=[...document.querySelectorAll("#studio-steps button")];
  const maxImage=2.5*1024*1024,maxAudio=8*1024*1024;
  const files={images:[null,null,null],audio:null};
  const defaultScenes=[
    {title:"Il dubbio: oggi fa freddo",body:"Un episodio meteorologico descrive ciò che osserviamo in un momento. Basta un giorno per capire una tendenza?",visual:"Un paesaggio invernale immaginario, senza persone identificabili e senza dati inventati.",alt:"Paesaggio invernale illustrativo che introduce la domanda sulla differenza tra meteo e clima"},
    {title:"Quale prova ci serve?",body:"Per parlare di tendenze climatiche dobbiamo esaminare misure affidabili raccolte nel tempo, non una sola giornata.",visual:"Confronto concettuale tra una singola osservazione e una serie nel tempo, senza inventare numeri.",alt:"Schema concettuale che distingue una osservazione singola da una serie temporale verificabile"},
    {title:"La prova: cosa puoi concludere?",body:"Spiega quale informazione manca e quale fonte consulteresti per verificare un'affermazione sul clima.",visual:"Due domande a contrasto: «che cosa so?» e «quale dato mi manca?».",alt:"Due domande per verificare quali dati sono disponibili e quali fonti sono ancora necessarie"}
  ];
  let phase=0;
  const rules={
    slides:[
      ["ChatGPT Images / modelli GPT Image","Immagini illustrative e loro revisione; controlla i dettagli e non presentarle come fotografie documentali.","https://help.openai.com/en/articles/11084440-images-in-chatgpt"],
      ["Gemini Nano Banana","Immagini generative e modifiche visive; confronta lo stesso brief con risultati alternativi.","https://gemini.google/overview/image-generation/"],
      ["Canva o un editor di slide","Montaggio, tipografia, leggibilità e presentazione del lavoro; non equivale a un modello generativo.","https://www.canva.com/help/generate-with-dreamlab/"]],
    audio:[
      ["NotebookLM / Gemini Notebook","Panoramica audio e dialoghi basati su fonti inserite; le affermazioni devono essere riascoltate e verificate.","https://notebooklm.google.com/"],
      ["Registrazione a due voci","Una registrazione originale fatta dai docenti è una valida alternativa senza IA; aggiungi una trascrizione.","https://udlguidelines.cast.org/"]],
    video:[
      ["Google Veo","Modelli generativi per clip illustrative, da valutare per fedeltà, anomalie e condizioni d'uso.","https://deepmind.google/models/veo/"],
      ["Editor video / storyboard","Montaggio e sottotitoli di materiali propri: la sceneggiatura deve precedere gli effetti.","https://www.canva.com/help/generate-with-dreamlab/"]],
    interactive:[
      ["H5P Branching Scenario","Attività con percorsi e feedback progettati dall'insegnante: non è automaticamente un tutor IA.","https://h5p.org/branching-scenario"],
      ["Kit HTML locale di MANZO AI","Tre slide, script e verifica a regole esportabili anche senza un account.","https://manzo8b.github.io/manzo-ai/it/formazione/ia-per-la-didattica/"]]
  };
  function msg(message,ok){const area=$("studio-status");area.textContent=message;area.style.color=ok?"#087b5e":"#a14b25"}
  function switchPhase(index){
    if(index<0||index>=phases.length)return;
    phase=index;
    phases.forEach((node,i)=>{node.hidden=i!==phase});
    buttons.forEach((b,i)=>{if(i===phase)b.setAttribute("aria-current","step");else b.removeAttribute("aria-current")});
    $("studio-progress-text").textContent="Fase "+(phase+1)+" di 5";
    $("studio-progress-fill").style.width=((phase+1)/5*100)+"%";
    $("studio-prev").disabled=phase===0;
    $("studio-next").textContent=phase===4?"Controlla la consegna":"Continua →";
    if(phase===4)renderPreview();
    msg("",true);
  }
  buttons.forEach(b=>b.addEventListener("click",()=>switchPhase(Number(b.dataset.go))));
  $("studio-prev").addEventListener("click",()=>switchPhase(phase-1));
  $("studio-next").addEventListener("click",()=>{
    if(phase===0&&!validateBasics())return;
    if(phase===2&&!validateScenes())return;
    if(phase===3&&!validateProduction())return;
    if(phase===4){checkDelivery();return}
    switchPhase(phase+1);
  });
  function value(name){return String(form.elements[name]?.value||"").trim()}
  function sceneValue(i,name){return String(document.querySelector('[data-scene="'+i+'"] [data-field="'+name+'"]')?.value||"").trim()}
  function validateBasics(){
    for(const name of ["title","audience","goal","source"]){if(!value(name)){msg("Compila argomento, destinatari, obiettivo e fonte prima di continuare.");return false}}
    return true;
  }
  function validateScenes(){
    for(let i=0;i<3;i++){
      if(!sceneValue(i,"title")||!sceneValue(i,"body")){
        msg("Ogni scena richiede almeno un titolo e una spiegazione.");return false;
      }
      if(files.images[i]&&!sceneValue(i,"alt")){msg("Inserisci una descrizione alternativa per tutte le immagini allegate.");return false}
    }
    return true;
  }
  function validateProduction(){
    for(const name of ["script","quiz_question","answer_a","answer_b","answer_c","feedback_correct","feedback_wrong"]){
      if(!value(name)){msg("Completa il dialogo, le tre risposte e i due feedback.");return false}
    }
    return true;
  }
  function collect(){
    return {
      schema:"manzo-ai-multimedia-studio-v1",
      title:value("title"),audience:value("audience"),goal:value("goal"),
      minutes:value("minutes"),prerequisites:value("prerequisites"),
      source:value("source"),constraints:value("constraints"),
      medium:value("medium"),model_reason:value("model_reason"),
      scenes:[0,1,2].map(i=>({
        title:sceneValue(i,"title"),body:sceneValue(i,"body"),visual:sceneValue(i,"visual"),
        alt:sceneValue(i,"alt"),image:files.images[i]
      })),
      speakers:[value("speaker_a"),value("speaker_b")],
      script:value("script"),audio:files.audio,
      quiz:{question:value("quiz_question"),options:[value("answer_a"),value("answer_b"),value("answer_c")],
        correct:Number(value("correct")),good:value("feedback_correct"),retry:value("feedback_wrong")},
      quality:[...form.querySelectorAll('input[name="quality"]')].filter(x=>x.checked).map(x=>x.value)
    };
  }
  function renderModels(){
    const dest=$("studio-models");
    dest.replaceChildren();
    for(const [name,description,url] of rules[value("medium")]||rules.slides){
      const card=document.createElement("article");card.className="studio-model-card";
      const title=document.createElement("strong");title.textContent=name;
      const copy=document.createElement("p");copy.textContent=description;
      const link=document.createElement("a");link.href=url;link.target="_blank";link.rel="noopener noreferrer";link.textContent="Documentazione ufficiale ↗";
      card.append(title,copy,link);dest.append(card);
    }
  }
  $("studio-medium").addEventListener("change",renderModels);
  renderModels();
  function setField(el,name,val){el.dataset.field=name;el.value=val}
  function sceneEditor(i,data){
    const box=document.createElement("section");box.className="studio-scene-editor";box.dataset.scene=String(i);
    const h=document.createElement("h3");h.textContent="SCENA "+(i+1)+" / "+(["IL PROBLEMA","LA SPIEGAZIONE","LA VERIFICA"][i]);box.append(h);
    const fields=[
      ["title","Titolo della scena","text"],
      ["body","Testo da leggere nella slide","textarea"],
      ["visual","Descrizione visiva o prompt per il modello","textarea"],
      ["alt","Testo alternativo dell'immagine","text"]
    ];
    for(const [name,labelText,kind] of fields){
      const label=document.createElement("label");label.textContent=labelText;
      const input=document.createElement(kind==="textarea"?"textarea":"input");
      if(kind==="textarea")input.rows=name==="body"?3:2;else input.type="text";
      input.maxLength=name==="body"?900:340;
      setField(input,name,data[name]||"");
      label.append(input);box.append(label);
    }
    const label=document.createElement("label");label.textContent="Immagine originale o generata con diritti d'uso (JPG, PNG, WebP; massimo 2,5 MB)";
    const image=document.createElement("input");image.type="file";image.accept=".jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp";
    image.setAttribute("aria-label","Immagine per la scena "+(i+1));
    const status=document.createElement("div");status.className="studio-file-state";status.textContent=files.images[i]?"Immagine caricata nel progetto":"Nessuna immagine inserita (la scena userà una scheda testuale)";
    image.addEventListener("change",async()=>{
      const file=image.files?.[0];if(!file)return;
      if(!["image/png","image/jpeg","image/webp"].includes(file.type)||file.size>maxImage){
        msg("Usa JPG, PNG o WebP con dimensione massima 2,5 MB. L'immagine non è stata importata.");image.value="";return}
      try{files.images[i]=await asDataURL(file);status.textContent="Immagine pronta: "+file.name;msg("Immagine acquisita soltanto nel browser.",true)}
      catch(_){msg("L'immagine non può essere letta.");image.value=""}
    });
    label.append(image);box.append(label,status);
    return box;
  }
  function renderScenes(data){
    const target=$("studio-scenes");target.replaceChildren();
    data.forEach((s,i)=>target.append(sceneEditor(i,s)));
  }
  renderScenes(defaultScenes);
  function asDataURL(file){
    return new Promise((resolve,reject)=>{
      const fr=new FileReader();
      fr.onload=()=>resolve(String(fr.result));
      fr.onerror=()=>reject(new Error("File non leggibile"));
      fr.readAsDataURL(file);
    });
  }
  $("studio-audio").addEventListener("change",async e=>{
    const file=e.target.files?.[0];if(!file)return;
    const types=["audio/mpeg","audio/mp4","audio/ogg","audio/wav","audio/x-wav"];
    if(!types.includes(file.type)||file.size>maxAudio){msg("Audio non valido: usa MP3, M4A, OGG o WAV sotto 8 MB.");e.target.value="";return}
    try{files.audio=await asDataURL(file);$("studio-audio-state").textContent="Traccia audio pronta: "+file.name;msg("Audio acquisito in memoria nel tuo browser.",true)}
    catch(_){msg("Impossibile leggere la traccia audio.")}
  });
  function renderPreview(){
    const p=collect(),root=$("studio-preview");root.replaceChildren();
    const heading=document.createElement("h3");heading.textContent=p.title||"Titolo ancora da definire";
    const text=document.createElement("p");
    text.textContent="Destinatari: "+p.audience+" · "+p.minutes+" minuti · "+(p.audio?"Audio incluso":"Copione disponibile senza registrazione");
    root.append(heading,text);
    const grid=document.createElement("div");grid.className="studio-preview-grid";
    p.scenes.forEach((scene,i)=>{
      const card=document.createElement("div");card.className="studio-preview-card";
      const count=document.createElement("span");count.textContent="SCENA "+(i+1);
      const title=document.createElement("b");title.textContent=scene.title;
      const copy=document.createElement("p");copy.textContent=scene.body.slice(0,165);
      if(scene.image){
        const image=new Image();image.src=scene.image;image.alt=scene.alt;
        card.append(image);
      }
      card.append(count,title,copy);grid.append(card);
    });
    root.append(grid);
    const q=document.createElement("p");q.textContent="Verifica: "+p.quiz.question;root.append(q);
  }
  function checkDelivery(){
    if(!validateBasics()||!validateScenes()||!validateProduction())return false;
    const missing=[...form.querySelectorAll('input[name="quality"]')].filter(x=>!x.checked);
    if(missing.length){msg("Per consegnare, completa la checklist: mancano "+missing.length+" controlli.");return false}
    msg("Kit controllato: puoi esportare l'HTML autonomo e il progetto modificabile.",true);return true;
  }
  function fileDownload(filename,data,mime){
    const blob=new Blob([data],{type:mime}),url=URL.createObjectURL(blob);
    const a=document.createElement("a");a.href=url;a.download=filename;document.body.append(a);a.click();a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),30000);
  }
  function safeFilename(title){return String(title||"lezione").normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[^a-z0-9]+/gi,"-").replace(/^-|-$/g,"").slice(0,55)||"lezione"}
  function escapeHtml(s){return String(s??"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;")}
  function validData(mimeValue,kind){
    if(typeof mimeValue!=="string")return null;
    const regex=kind==="audio"?/^data:audio\/(?:mpeg|mp4|ogg|wav|x-wav);base64,[a-z0-9+/=]+$/i:
      /^data:image\/(?:jpeg|png|webp);base64,[a-z0-9+/=]+$/i;
    return mimeValue.length<=16*1024*1024&&regex.test(mimeValue)?mimeValue:null;
  }
  function exportedHTML(p){
    const safe={
      ...p,
      scenes:p.scenes.map(x=>({...x,image:validData(x.image,"image")})),
      audio:validData(p.audio,"audio")
    };
    const embedded=JSON.stringify(safe).replace(/</g,"\\u003c");
    const style=String.raw`
:root{--deep:#173b70;--blue:#155bd9}*{box-sizing:border-box}body{margin:0;background:#f1f6fd;color:#254567;font:16px/1.6 system-ui,-apple-system,sans-serif}button{font:inherit;cursor:pointer}button:focus-visible,input:focus-visible{outline:3px solid #e98a41;outline-offset:3px}main{max-width:1040px;margin:auto;padding:24px}.intro{background:#fff;border:1px solid #d4e3ef;border-radius:17px;padding:24px;margin-bottom:20px}.eyebrow{font-weight:800;color:#145fc8;letter-spacing:.12em;font-size:.72rem}h1{font-size:clamp(1.6rem,4vw,2.5rem);line-height:1.17;letter-spacing:-.04em;color:#153d69}.intro p,.note{color:#4b6581}.slide{background:linear-gradient(145deg,#133d74,#112c55);color:#fff;border-radius:19px;min-height:350px;padding:clamp(25px,5vw,53px);display:flex;flex-direction:column;align-items:start;justify-content:center}.slide h2{font-size:clamp(1.5rem,4vw,2.8rem);line-height:1.16;color:#fff;letter-spacing:-.04em}.slide p{font-size:clamp(.98rem,2vw,1.2rem);max-width:750px}.slide img{max-width:100%;max-height:440px;object-fit:contain;border-radius:12px;margin-bottom:15px}.slide small{color:#f7c878}.slide[hidden]{display:none}.controls{display:flex;justify-content:space-between;align-items:center;gap:15px;padding:18px 0}.controls button,.quiz button{background:#155cd5;color:white;border:0;border-radius:11px;padding:10px 17px;font-weight:780}.controls button:disabled{opacity:.4}.card{margin-top:21px;border:1px solid #d3e3f3;background:#fff;padding:22px;border-radius:16px}.card h2{font-size:1.33rem;color:#15426d}.transcript{white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.8;background:#f6f9fd;padding:17px;border-radius:11px}.quiz label{display:block;padding:11px;border-radius:10px;border:1px solid #d0e2f0;margin:8px 0}.quiz input{margin-right:10px}.quiz-feedback{margin-top:12px;background:#e8f8f2;color:#145940;padding:13px;border-radius:10px}.quiz-feedback:empty{display:none}.note{font-size:.82rem;line-height:1.75}.card audio{max-width:100%;width:100%;margin-bottom:15px}@media print{body{background:white}.controls,.quiz button{display:none!important}.slide{break-after:page;page-break-after:always;min-height:78vh;print-color-adjust:exact;-webkit-print-color-adjust:exact}.slide[hidden]{display:flex!important}.card{break-inside:avoid}main{max-width:none}}`; 
    const reader=String.raw`
(function(){"use strict";
const data=JSON.parse(document.getElementById("kit-data").textContent);
const place=document.getElementById("slides"),counter=document.getElementById("slide-counter");
let current=0;
function el(tag,text){const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n}
data.scenes.forEach((s,i)=>{const sect=el("section");sect.className="slide";sect.setAttribute("aria-label","Scena "+(i+1));
 if(s.image&&/^data:image\/(?:jpeg|png|webp);base64,/i.test(s.image)){const im=el("img");im.src=s.image;im.alt=s.alt||"";sect.append(im)}
 const num=el("small","SCENA "+(i+1)+" / "+data.scenes.length);
 const title=el("h2",s.title);const body=el("p",s.body);sect.append(num,title,body);place.append(sect)});
const slides=[...place.children];
function update(){slides.forEach((e,i)=>{e.hidden=i!==current});counter.textContent=(current+1)+" / "+slides.length;
 document.getElementById("prev").disabled=current===0;document.getElementById("next").disabled=current===slides.length-1}
document.getElementById("prev").addEventListener("click",()=>{current=Math.max(0,current-1);update()});
document.getElementById("next").addEventListener("click",()=>{current=Math.min(slides.length-1,current+1);update()});
update();
document.getElementById("transcript").textContent=data.script;
if(data.audio&&/^data:audio\/(?:mpeg|mp4|ogg|wav|x-wav);base64,/i.test(data.audio)){const audio=el("audio");audio.controls=true;audio.preload="none";audio.src=data.audio;document.getElementById("recording").append(audio)}
document.getElementById("quiz-title").textContent=data.quiz.question;
const answers=document.getElementById("quiz-answers");
data.quiz.options.forEach((option,i)=>{const label=el("label");const input=el("input");input.type="radio";input.name="answer";input.value=String(i);label.append(input,el("span",option));answers.append(label)});
document.getElementById("evaluate").addEventListener("click",()=>{const picked=answers.querySelector("input:checked");const res=document.getElementById("result");res.textContent=!picked?"Seleziona una risposta per ricevere il feedback.":Number(picked.value)===data.quiz.correct?data.quiz.good:data.quiz.retry});
})();`; 
    return '<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'+
      '<title>'+escapeHtml(p.title)+' · Microlezione</title><style>'+style+'</style></head><body><main>'+
      '<header class="intro"><div class="eyebrow">MICROLEZIONE · MANZO AI TEACHING LAB</div><h1>'+escapeHtml(p.title)+'</h1>'+
      '<p><strong>Destinatari:</strong> '+escapeHtml(p.audience)+' · '+escapeHtml(p.minutes)+' minuti</p>'+
      '<p><strong>Obiettivo:</strong> '+escapeHtml(p.goal)+'</p>'+
      '<p><strong>Fonte da verificare:</strong> '+escapeHtml(p.source)+'</p>'+
      '</header><div id="slides" aria-label="Presentazione di tre scene"></div>'+
      '<nav class="controls" aria-label="Navigazione delle scene"><button id="prev" type="button">← Precedente</button><span id="slide-counter" aria-live="polite"></span><button id="next" type="button">Successiva →</button></nav>'+
      '<section class="card"><h2>Copione e trascrizione</h2><div id="recording"></div><div class="transcript" id="transcript"></div></section>'+
      '<section class="card quiz"><h2>Verifica di apprendimento</h2><p id="quiz-title"></p><div id="quiz-answers"></div><button id="evaluate" type="button">Controlla la risposta</button><div id="result" class="quiz-feedback" role="status" aria-live="polite"></div></section>'+
      '<section class="card"><h2>Indicazioni didattiche</h2><p><strong>Prerequisiti:</strong> '+escapeHtml(p.prerequisites)+'</p>'+
      '<p><strong>Accessibilità e vincoli:</strong> '+escapeHtml(p.constraints)+'</p>'+
      '<p><strong>Scelta dello strumento:</strong> '+escapeHtml(p.model_reason)+'</p></section>'+
      '<p class="note">Materiali preparati dal docente con il laboratorio MANZO AI. Verificare contenuti, licenze, accessibilità e privacy prima dell’uso con studenti. Il lettore non invia dati a server e non assegna voti.</p>'+
      '</main><script type="application/json" id="kit-data">'+embedded+'</script><script>'+reader+'</script></body></html>';
  }
  $("studio-download-html").addEventListener("click",()=>{
    if(!checkDelivery())return;
    const p=collect();
    fileDownload("MANZO-AI-microlezione-"+safeFilename(p.title)+".html",exportedHTML(p),"text/html;charset=utf-8");
    msg("Microlezione HTML esportata. Aprila anche senza connessione Internet.",true);
  });
  $("studio-download-json").addEventListener("click",()=>{
    if(!validateBasics()||!validateScenes()||!validateProduction())return;
    const p=collect();
    fileDownload("MANZO-AI-progetto-"+safeFilename(p.title)+".json",JSON.stringify(p,null,2),"application/json;charset=utf-8");
    msg("Progetto modificabile salvato: potrai reimportarlo in questa pagina.",true);
  });
  $("studio-print").addEventListener("click",()=>{
    if(!checkDelivery())return;
    const blob=new Blob([exportedHTML(collect())],{type:"text/html;charset=utf-8"}),url=URL.createObjectURL(blob);
    const win=window.open(url,"_blank","noopener");
    if(!win)msg("Il browser ha bloccato l'anteprima. Esporta l'HTML e aprilo, poi usa Stampa → Salva come PDF.");
    else msg("Anteprima aperta: usa Stampa → Salva come PDF dal browser.",true);
  });
  $("studio-import").addEventListener("change",async e=>{
    const file=e.target.files?.[0];if(!file)return;
    if(file.size>12*1024*1024){msg("Il progetto supera il limite di 12 MB per l'importazione.");return}
    try{
      const p=JSON.parse(await file.text());
      if(p.schema!=="manzo-ai-multimedia-studio-v1"||!Array.isArray(p.scenes)||p.scenes.length!==3||
        !p.quiz||!Array.isArray(p.quiz.options)||p.quiz.options.length!==3)throw Error("Formato non riconosciuto");
      const fields=["title","audience","goal","minutes","prerequisites","source","constraints","medium","model_reason","speaker_a","speaker_b","script","quiz_question","answer_a","answer_b","answer_c","correct","feedback_correct","feedback_wrong"];
      const entries={...p,quiz_question:p.quiz.question,answer_a:p.quiz.options[0],answer_b:p.quiz.options[1],answer_c:p.quiz.options[2],
        correct:String(p.quiz.correct),feedback_correct:p.quiz.good,feedback_wrong:p.quiz.retry,
        speaker_a:p.speakers?.[0],speaker_b:p.speakers?.[1]};
      for(const name of fields){
        const field=form.elements[name];if(!field)continue;
        let v=String(entries[name]??"").slice(0,field.maxLength>0?field.maxLength:9000);
        if(field.tagName==="SELECT"&&!Array.from(field.options).some(o=>o.value===v))continue;
        field.value=v;
      }
      files.images=p.scenes.map(s=>validData(s.image,"image"));
      files.audio=validData(p.audio,"audio");
      renderScenes(p.scenes.map(s=>({title:String(s.title||"").slice(0,340),body:String(s.body||"").slice(0,900),
        visual:String(s.visual||"").slice(0,340),alt:String(s.alt||"").slice(0,340)})));
      for(const box of form.querySelectorAll('input[name="quality"]'))box.checked=Array.isArray(p.quality)&&p.quality.includes(box.value);
      $("studio-audio-state").textContent=files.audio?"Registrazione recuperata dal progetto":"Nessuna registrazione nel progetto";
      renderModels();switchPhase(0);msg("Progetto importato correttamente. Controlla i dati prima dell'esportazione.",true);
    }catch(_){msg("Progetto non valido: importa un JSON creato da questo laboratorio.")}
    e.target.value="";
  });
  switchPhase(0);
})();
