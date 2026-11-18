"""Contract tests for the MANZO AI conversational home publisher.

Runs without network, fake AI backend, third-party packages or a real site archive.
"""
from __future__ import annotations
import importlib.util
from pathlib import Path
import tempfile
import unittest

PUBLISHER=Path(__file__).resolve().parents[1]/"publish-home-conversational.py"
spec=importlib.util.spec_from_file_location("publish_home_conversational",PUBLISHER)
assert spec and spec.loader
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

CAT=("verify","coding","fundamentals","prompt","verify","workflow")
LOCALES={"it":"academy","en":"academy","es":"academia"}
HALLUCINATION={"it":"it/impara/allucinazioni-ai-verificabilita","en":"en/learn/ai-hallucinations-verification","es":"es/aprende/alucinaciones-ia-verificacion"}

def make_site(root):
 (root/"index.html").write_text("<html><body>LANGUAGE GATEWAY IT EN ES</body></html>",encoding="utf-8")
 teacher=root/"it/formazione/ia-per-la-didattica/inizia/index.html"
 teacher.parent.mkdir(parents=True,exist_ok=True)
 teacher.write_text("Mission Studio real route",encoding="utf-8")
 for lang,academy in LOCALES.items():
  home=root/lang/"index.html"
  home.parent.mkdir(parents=True,exist_ok=True)
  home.write_text(
   '<html><head><title>Original HOME</title></head><body>'
   '<main><section class="home-hero"><h1>Legacy home hero remains</h1>'
   '<div class="searchbox"><input aria-label="Search"></div>'
   '<aside class="ma-product-scene">Legacy scene remains</aside></section>'
   '<section class="ma-home-showcase">Original Academy remains</section></main>'
   '</body></html>',encoding="utf-8")
  hallucination=root/HALLUCINATION[lang]/"index.html"
  hallucination.parent.mkdir(parents=True,exist_ok=True)
  hallucination.write_text("Real AI hallucinations course",encoding="utf-8")
  academy_cards=[]
  for i,category in enumerate(CAT):
   route=f"/manzo-ai/{lang}/learn/demo-{i+1}/"
   destination=root/lang/"learn"/f"demo-{i+1}"/"index.html"
   destination.parent.mkdir(parents=True,exist_ok=True)
   destination.write_text("Real Academy lesson",encoding="utf-8")
   academy_cards.append(
    f'<article data-ma-course-card="1" data-ma-category="{category}">'
    f'<h3>Lesson {i+1}</h3><a href="{route}">Open</a></article>'
   )
  academy_page=root/lang/academy/"index.html"
  academy_page.parent.mkdir(parents=True,exist_ok=True)
  academy_page.write_text("<html><body>"+''.join(academy_cards)+"</body></html>",encoding="utf-8")

class ConversationalHomeContracts(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory()
  self.root=Path(self.tmp.name)/"_site"
  self.root.mkdir()
  make_site(self.root)
 def tearDown(self):
  self.tmp.cleanup()
 def test_insert_all_locales_preserving_language_gateway(self):
  original=(self.root/"index.html").read_bytes()
  module.apply(self.root)
  module.apply(self.root,verify_only=True)
  self.assertEqual(original,(self.root/"index.html").read_bytes())
  for lang in LOCALES:
   text=(self.root/lang/"index.html").read_text(encoding="utf-8")
   self.assertIn("Legacy home hero remains",text)
   self.assertIn("Original Academy remains",text)
   self.assertIn('class="searchbox"',text)
   self.assertIn("Legacy scene remains",text)
   self.assertLess(text.index(module.MARKER),text.index('class="ma-product-scene"'),"Mobile must see the discovery before the decorative scene")
   self.assertEqual(text.count(module.MARKER),1)
   self.assertEqual(text.count('data-ma-home-discovery-asset="v1"'),2)
   self.assertEqual(text.count('data-ma-intent='),4)
   self.assertIn(f'href="/manzo-ai/{HALLUCINATION[lang]}/"',text)
   self.assertIn(f'href="/manzo-ai/{lang}/learn/demo-4/"',text)
   self.assertIn(f'href="/manzo-ai/{lang}/learn/demo-1/"',text)
   self.assertIn(f'href="/manzo-ai/{lang}/learn/demo-3/"',text)
   self.assertIn(f'href="/manzo-ai/{lang}/learn/demo-2/"',text)
   self.assertNotIn("Fake AI assistant",text)
  with self.assertRaisesRegex(RuntimeError,"Duplicate"):
   module.apply(self.root)
 def test_missing_real_hallucinations_course_blocks_release(self):
  (self.root/HALLUCINATION["it"]/'index.html').unlink()
  with self.assertRaisesRegex(RuntimeError,"Missing published destination"):
   module.apply(self.root)
 def test_missing_academy_category_blocks_release(self):
  academy=self.root/"it/academy/index.html"
  academy.write_text(academy.read_text().replace('data-ma-category="prompt"','data-ma-category="misc"'),encoding="utf-8")
  with self.assertRaisesRegex(RuntimeError,"Learning taxonomy missing"):
   module.apply(self.root)
 def test_escapes_untrusted_academy_destination(self):
  academy=self.root/"it/academy/index.html"
  html=academy.read_text(encoding="utf-8")
  academy.write_text(html.replace('/manzo-ai/it/learn/demo-4/',"javascript:alert(1)"),encoding="utf-8")
  with self.assertRaisesRegex(RuntimeError,"Unexpected Academy route"):
   module.apply(self.root)

if __name__=="__main__":
 unittest.main()
