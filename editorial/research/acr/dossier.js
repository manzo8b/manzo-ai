/* MANZO AI ACR dossier: progressive enhancement only; no analytics, tracking, network requests. */
(() => {
  'use strict';
  const root = document.querySelector('[data-acr-dossier]');
  if (!root) return;
  root.classList.add('acr-enhanced');
  const steps = Array.from(root.querySelectorAll('[data-demo-step]'));
  const title = root.querySelector('[data-demo-title]');
  const description = root.querySelector('[data-demo-description]');
  const status = root.querySelector('[data-demo-status]');
  const code = root.querySelector('[data-demo-code]');
  const flag = root.querySelector('[data-demo-flag]');
  let records = [];
  try { records = JSON.parse(root.querySelector('#acr-demo-data')?.textContent || '[]'); } catch { records = []; }
  const render = i => {
    const r = records[i];
    if (!r) return;
    steps.forEach((button,index) => button.setAttribute('aria-pressed',String(index === i)));
    title.textContent = r.title; description.textContent = r.description;
    status.textContent = r.status; code.textContent = r.code; flag.textContent = r.flag;
  };
  steps.forEach((button,i) => button.addEventListener('click',() => render(i)));
  if (records.length) render(0);
  const targets = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) {
    targets.forEach(el => el.classList.add('visible'));
  } else {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('visible'); observer.unobserve(entry.target); }
    }), { threshold: .08, rootMargin: '0px 0px -28px 0px' });
    targets.forEach(el => observer.observe(el));
  }
})();
