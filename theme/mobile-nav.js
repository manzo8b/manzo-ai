/* MANZO AI | Mobile navigation v1.0 — progressive enhancement, no external dependencies */
(() => {
  'use strict';
  const PREFIX = '/manzo-ai/';
  const lang = (location.pathname.match(/^\/manzo-ai\/(it|es|en)(?:\/|$)/) || [])[1] || 'it';
  const isPortal = location.pathname === PREFIX || location.pathname === PREFIX.slice(0,-1);
  const copy = {
    it: {home:'Home',portal:'Home generale · Lingue',choose:'Scegli la lingua',menu:'Menu',close:'Chiudi menu',navigation:'Esplora MANZO AI',sections:'Sezioni',languages:'Lingue',back:'Torna alla scelta della lingua',academy:'AI Academy',practice:'Prompt Mastery',lab:'Laboratorio tecnico',critical:'Pensiero critico',resources:'Risorse',media:'Video e slide'},
    es: {home:'Inicio',portal:'Inicio general · Idiomas',choose:'Elegir idioma',menu:'Menú',close:'Cerrar menú',navigation:'Explorar MANZO AI',sections:'Secciones',languages:'Idiomas',back:'Volver a elegir idioma',academy:'AI Academia',practice:'Prompt Mastery',lab:'Laboratorio técnico',critical:'Pensamiento crítico',resources:'Recursos',media:'Vídeos y diapositivas'},
    en: {home:'Home',portal:'Main home · Languages',choose:'Choose language',menu:'Menu',close:'Close menu',navigation:'Explore MANZO AI',sections:'Sections',languages:'Languages',back:'Back to language selection',academy:'AI Academy',practice:'Prompt Mastery',lab:'Technical lab',critical:'Critical thinking',resources:'Resources',media:'Videos and slides'}
  }[lang];
  const base = PREFIX + lang + '/';
  const fallback = {
    it:[['AI Academy','academy/'],['Prompt Mastery','prompt-mastery/che-cos-e-un-prompt/'],['Laboratorio tecnico','prompt-mastery/laboratorio-tecnico/'],['Pensiero critico','pensiero-critico/'],['Risorse','risorse/'],['Video e slide','video-e-slide/']],
    es:[['AI Academia','academia/'],['Prompt Mastery','prompt-mastery/que-es-un-prompt/'],['Laboratorio técnico','prompt-mastery/laboratorio-tecnico/'],['Pensamiento crítico','pensamiento-critico/'],['Recursos','recursos/'],['Vídeos y diapositivas','videos-y-diapositivas/']],
    en:[['AI Academy','academy/'],['Prompt Mastery','prompt-mastery/what-is-a-prompt/'],['Technical lab','prompt-mastery/technical-lab/'],['Critical thinking','critical-thinking/'],['Resources','resources/'],['Videos and slides','videos-and-slides/']]
  }[lang];
  const url = (href) => new URL(href, location.origin);
  const sameSite = (href) => {
    try {const u=url(href);return u.origin===location.origin && u.pathname.startsWith(PREFIX);} catch{return false;}
  };
  const node=(tag,className,textContent)=>{
    const el=document.createElement(tag);
    if(className)el.className=className;
    if(textContent!==undefined)el.textContent=textContent;
    return el;
  };
  const anchor=(href, label, className)=>{
    const a=node('a',className,label);
    a.href=href;
    if(url(href).pathname===location.pathname) a.setAttribute('aria-current','page');
    return a;
  };
  const rail=document.querySelector('.rail');
  // Desktop and tablet: a direct, recognizable return to the central language hub.
  if(rail && !rail.querySelector('[data-manzo-portal-link]') && !isPortal){
    const home=anchor(PREFIX,copy.portal,'manzo-global-home');
    home.dataset.manzoPortalLink='1';
    const railBottom=rail.querySelector('.rail-bottom');
    if(railBottom)railBottom.prepend(home);
    else rail.append(home);
  }
  const bar=node('div','manzo-mobile-bar');
  bar.dataset.manzoMobile='1';
  const brand=anchor(base,'MANZO AI','manzo-mobile-brand');
  brand.setAttribute('aria-label','MANZO AI · '+copy.home);
  const mark=node('img','manzo-mobile-mark');
  mark.src=PREFIX+'assets/manzo-mark.svg';mark.alt='';mark.width=27;mark.height=27;
  brand.prepend(mark);
  const center=anchor(PREFIX,copy.choose,'manzo-mobile-portal');
  center.title=copy.portal;
  center.setAttribute('aria-label',copy.portal);
  const burger=node('button','manzo-mobile-toggle');
  burger.type='button';burger.setAttribute('aria-expanded','false');burger.setAttribute('aria-haspopup','dialog');
  const hamburger=node('span','manzo-mobile-hamburger');hamburger.setAttribute('aria-hidden','true');
  for(let i=0;i<3;i++)hamburger.append(node('i'));
  burger.append(hamburger,node('span','manzo-mobile-menu-label',copy.menu));
  bar.append(brand,center,burger);

  const shade=node('button','manzo-mobile-scrim');
  shade.type='button';shade.tabIndex=-1;shade.setAttribute('aria-label',copy.close);shade.setAttribute('aria-hidden','true');
  const drawer=node('aside','manzo-mobile-drawer'); drawer.id='manzo-mobile-drawer';
  drawer.setAttribute('role','dialog');drawer.setAttribute('aria-modal','true');drawer.setAttribute('aria-label',copy.navigation);
  drawer.setAttribute('aria-hidden','true');drawer.inert=true;
  burger.setAttribute('aria-controls',drawer.id);
  const header=node('div','manzo-mobile-drawer-head');
  const heading=node('div','manzo-mobile-drawer-heading');
  heading.append(node('strong','', 'MANZO AI'),node('span','',copy.navigation));
  const close=node('button','manzo-mobile-close','×');close.type='button';close.setAttribute('aria-label',copy.close);
  header.append(heading,close);
  const routeGroup=node('div','manzo-mobile-quick');
  routeGroup.append(anchor(base,'⌂  '+copy.home,'manzo-mobile-quick-home'),anchor(PREFIX,'◈  '+copy.portal,'manzo-mobile-quick-portal'));
  const title=node('h2','manzo-mobile-navtitle',copy.sections);
  const nav=node('nav','manzo-mobile-nav');nav.setAttribute('aria-label',copy.navigation);

  // Preserve the original site's sections when available; fallback supports editorial pages.
  const originals=rail ? [...rail.querySelectorAll('.nav-title, .nav-link')]: [];
  const groups=[];
  let current={name:copy.sections,links:[]};
  const normalized=(p)=>p.replace(/\/index\.html$/,'/').replace(/\/?$/,'/');
  const seen=new Set();
  for(const el of originals){
    if(el.matches('.nav-title')){
      if(current.links.length)groups.push(current);
      current={name:el.textContent.trim()||copy.sections,links:[]};
      continue;
    }
    const href=el.getAttribute('href'),label=(el.textContent||'').trim().replace(/\s+/g,' ');
    if(!href || !label || !sameSite(href)) continue;
    const link=url(href),path=normalized(link.pathname);
    if(seen.has(path) || path===PREFIX)continue;
    seen.add(path);
    current.links.push({href:link.pathname+link.search+link.hash,label,active:normalized(location.pathname)===path});
  }
  if(current.links.length)groups.push(current);
  if(groups.length===0){
    const links=fallback.map(([label,route])=>({label,href:base+route,active:normalized(location.pathname)===normalized(base+route)}));
    groups.push({name:copy.sections,links});
  }
  // Accordion groups keep a complex educational catalog scannable on a small display.
  groups.forEach((group,index)=>{
    const detail=node('details','manzo-mobile-group');
    detail.open=index===0 || group.links.some(x=>x.active);
    const summary=node('summary','manzo-mobile-group-title',group.name);
    const entries=node('div','manzo-mobile-group-links');
    group.links.forEach(item=>{
      const link=anchor(item.href,item.label,'manzo-mobile-navlink');
      if(item.active)link.setAttribute('aria-current','page');
      entries.append(link);
    });
    detail.append(summary,entries);nav.append(detail);
  });
  const footer=node('div','manzo-mobile-drawer-footer');
  footer.append(node('h2','manzo-mobile-navtitle',copy.languages));
  const choices=node('div','manzo-mobile-lang');
  [['it','Italiano'],['es','Español'],['en','English']].forEach(([key,label])=>{
    const a=anchor(PREFIX+key+'/',label,'manzo-mobile-lang-link');
    a.lang=key;if(key===lang&&!isPortal)a.setAttribute('aria-current','page');
    choices.append(a);
  });
  footer.append(choices,anchor(PREFIX,copy.back,'manzo-mobile-back'));
  drawer.append(header,routeGroup,title,nav,footer);
  const mount=document.querySelector('.shell') || document.querySelector('main') || document.body.firstElementChild;
  if(mount && mount.parentNode===document.body)document.body.insertBefore(bar,mount);
  else document.body.prepend(bar);
  document.body.append(shade,drawer);
  let wasFocused=null;
  let opened=false;
  function setOpen(value,restore=true){
    opened=!!value;
    document.body.classList.toggle('manzo-mobile-open',opened);
    burger.setAttribute('aria-expanded',String(opened));
    drawer.setAttribute('aria-hidden',String(!opened));
    drawer.inert=!opened;
    document.documentElement.style.overflow=opened?'hidden':'';
    if(opened){wasFocused=document.activeElement;close.focus({preventScroll:true});}
    else if(restore && wasFocused && wasFocused.isConnected){wasFocused.focus({preventScroll:true});}
  }
  burger.addEventListener('click',()=>setOpen(!opened));
  close.addEventListener('click',()=>setOpen(false));
  shade.addEventListener('click',()=>setOpen(false));
  drawer.addEventListener('click',event=>{if(event.target.closest('a'))setOpen(false,false);});
  document.addEventListener('keydown',event=>{
    if(!opened)return;
    if(event.key==='Escape'){event.preventDefault();setOpen(false);return;}
    if(event.key!=='Tab')return;
    const focusables=[...drawer.querySelectorAll('a[href],button:not([disabled]),summary,[tabindex]:not([tabindex="-1"])')].filter(e=>!e.closest('details:not([open])') && e.getClientRects().length);
    if(!focusables.length)return;
    const first=focusables[0],last=focusables[focusables.length-1];
    if(event.shiftKey && document.activeElement===first){event.preventDefault();last.focus();}
    else if(!event.shiftKey && document.activeElement===last){event.preventDefault();first.focus();}
  });
  const mq=window.matchMedia('(min-width: 761px)');
  const desktop=()=>{if(mq.matches && opened)setOpen(false,false);};
  if(mq.addEventListener)mq.addEventListener('change',desktop);
  else mq.addListener(desktop);
  // On central portal, prioritize choosing a language; the full menu remains available.
  if(isPortal)brand.href=PREFIX;
})();
