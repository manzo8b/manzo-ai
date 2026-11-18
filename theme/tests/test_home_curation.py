"""Offline fixtures for inclusive homepage, four themes, full Academy and About pages."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
def load(name):
 spec=importlib.util.spec_from_file_location(name.replace("-","_"),ROOT/name)
 assert spec and spec.loader
 module=importlib.util.module_from_spec(spec)
 spec.loader.exec_module(module)
 return module

curate=load("publish-home-curation.py")
about=load("publish-about.py")
def page(path,text):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(text,encoding="utf-8")

class HomeCurationContracts(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory()
  self.site=Path(self.tmp.name)/"_site"
  self.site.mkdir()
  page(self.site/"index.html",'''<!doctype html><html lang="it_IT"><head>
<title>Choose a language</title></head><body>
<a href="/manzo-ai/it/"><span>Explore</span></a>
<a href="/manzo-ai/en/"><span>Explore</span></a>
<a href="/manzo-ai/es/"><span>Explore</span></a></body></html>''')
  page(self.site/"it/formazione/ia-per-la-didattica/inizia/index.html","Real teacher mission")
  for lang,academy in (("it","academy"),("en","academy"),("es","academia")):
   prefix=f"/manzo-ai/{lang}/"
   urls=[
    prefix+"learn/fundamentals/",prefix+"prompt/first/",
    "/manzo-ai/"+{"it":"it/impara/allucinazioni-ai-verificabilita/","en":"en/learn/ai-hallucinations-verification/","es":"es/aprende/alucinaciones-ia-verificacion/"}[lang],
    prefix+"learn/coding/"
   ]
   page(self.site/lang/academy/"index.html","Real Academy")
   for route in urls:page(self.site/route.removeprefix("/manzo-ai/")/"index.html","Real course")
   cards=''.join(
    f'<a class="ma-discovery-choice" href="{url}" data-ma-intent="{i}">Goal {i}</a>'
    for i,url in enumerate(urls)
   )
   page(self.site/lang/"index.html",f'''<html><head><title>Home {lang}</title></head><body>
<aside class="rail"><div class="nav-title">Old links</div><a class="nav-link" href="{prefix}">Home</a></aside>
<main><section class="home-hero"><h1>Cosa vuoi capire oggi?</h1>
<p>Percorsi accessibili per comprendere</p>
<div class="searchbox"><input aria-label="Search"></div>
<div data-ma-home-discovery="v1" class="ma-discovery">{cards}
<p data-ma-discovery-live class="sr-only" role="status" aria-live="polite"></p></div>
<aside data-ma-home-scene="1" class="ma-product-scene"><div>Unhelpful Product Lab</div></aside>
</section><div class="ma-home-showcase">Six original cards</div></main></body></html>''')
  about.apply(self.site)
 def tearDown(self):self.tmp.cleanup()

 def test_language_gate_and_three_teacher_first_homes(self):
  curate.run(self.site)
  curate.run(self.site,verify_only=True)
  portal=(self.site/"index.html").read_text(encoding="utf-8")
  self.assertIn('lang="it"',portal)
  self.assertIn("Scegli la lingua · Choose a language · Elige idioma",portal)
  self.assertIn("<span>Esplora</span>",portal)
  self.assertIn("<span>Explore</span>",portal)
  self.assertIn("<span>Explorar</span>",portal)
  for lang,route in about.ROUTES.items():
   page_html=(self.site/lang/"index.html").read_text(encoding="utf-8")
   self.assertIn(curate.COPY[lang]["hero"],page_html)
   self.assertIn('data-ma-home-curation="v2"',page_html)
   self.assertIn('data-ma-home-primary-nav="v2"',page_html)
   self.assertEqual(page_html.count('data-ma-intent='),4)
   self.assertEqual(page_html.count('class="ma-home-primary-nav"'),1)
   self.assertIn('data-ma-home-featured="v1"',page_html)
   self.assertEqual(page_html.count('class="ma-topic-card '),4)
   self.assertEqual(page_html.count('class="ma-product-scene"'),0)
   self.assertEqual(page_html.count('<a href="/manzo-ai/'),7)
   self.assertIn(f'href="/manzo-ai/{lang}/{route}/"',page_html)
   self.assertIn("Six original cards",page_html)
   self.assertIn("Allucinazioni" if lang=="it" else ("hallucinations" if lang=="en" else "Alucinaciones"),page_html)
   self.assertIn('class="searchbox"',page_html)
   self.assertIn("Marcelo Javier Fernandez Caballero",page_html)
   self.assertEqual(page_html.count("Unhelpful Product Lab"),0)
   about_html=(self.site/lang/route/"index.html").read_text(encoding="utf-8")
   self.assertIn("data-manzo-about",about_html)
   self.assertIn("independent" if lang=="en" else ("independiente" if lang=="es" else "indipendente"),about_html.lower())
  with self.assertRaisesRegex(RuntimeError,"Repeated home curation"):
   curate.run(self.site)

 def test_duplicate_destination_blocks_publication(self):
  target=self.site/"en/index.html"
  doc=target.read_text(encoding="utf-8")
  doc=doc.replace('/manzo-ai/en/learn/ai-hallucinations-verification/', '/manzo-ai/en/prompt/first/')
  target.write_text(doc,encoding="utf-8")
  with self.assertRaisesRegex(RuntimeError,"duplicate destinations"):
   curate.run(self.site)

 def test_scene_missing_blocks_risky_mutation(self):
  target=self.site/"es/index.html"
  doc=target.read_text(encoding="utf-8")
  doc=doc.replace('data-ma-home-scene="1"','data-scene-unknown="1"')
  target.write_text(doc,encoding="utf-8")
  with self.assertRaisesRegex(RuntimeError,"Legacy scene changed"):
   curate.run(self.site)

 def test_about_pages_have_distinct_locales_without_fake_accreditation(self):
  about.apply(self.site,verify_only=True)
  for lang,route in about.ROUTES.items():
   text=(self.site/lang/route/"index.html").read_text(encoding="utf-8")
   self.assertIn("Marcelo Javier Fernandez Caballero",text)
   self.assertNotIn("ISO-certified",text)
   self.assertIn(f'lang="{lang}"',text)

if __name__=="__main__":unittest.main()
