import tempfile
from pathlib import Path
import unittest

from audit_release import scan, internal_reference


def html(locale="it", robots="index,follow", links=""):
    return f"""<!doctype html><html lang="{locale}"><head>
<title>Test page</title><meta name="robots" content="{robots}">
<link rel="canonical" href="https://manzo8b.github.io/manzo-ai/it/">
<link rel="alternate" hreflang="en" href="https://manzo8b.github.io/manzo-ai/en/">
</head><body><main><h1>Test</h1>{links}</main></body></html>"""


class RenderedSiteAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.site = Path(self.tmp.name) / "_site"
        self.site.mkdir()

    def write(self, name, value):
        target = self.site / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(value, encoding="utf-8")
        return target

    def test_complete_site_inventory_and_private_noindex(self):
        self.write("index.html", html(links='<a href="/manzo-ai/it/">IT</a>'))
        self.write("it/index.html", html(links='<link href="/manzo-ai/assets/main.css" rel="stylesheet">'))
        self.write("en/index.html", html("en"))
        self.write("it/prodotto/learning-b2b/accesso/index.html",
                   html(robots="noindex,nofollow", links='<a href="/manzo-ai/it/">Home</a>'))
        self.write("assets/main.css", "body{background:white}")
        found = scan(self.site)
        self.assertEqual(found["summary"]["html_pages"], 4)
        self.assertEqual(found["summary"]["asset_files"], 1)
        self.assertEqual(found["summary"]["noindex_pages"], 1)
        self.assertEqual(found["summary"]["auth_noindex_violations"], 0)
        self.assertEqual(found["summary"]["missing_reference_pages"], 0)
        self.assertEqual(found["summary"]["locales"], ["en", "it"])
        self.assertTrue(next(x for x in found["pages"] if "accesso" in x["path"])["private_noindex_ok"])

    def test_missing_link_is_reported_not_assumed_present(self):
        self.write("it/index.html", html(links='<img src="/manzo-ai/assets/missing.webp">'))
        found = scan(self.site)
        self.assertEqual(found["summary"]["missing_reference_pages"], 1)
        self.assertEqual(found["missing_internal_references"][0]["paths"], ["assets/missing.webp"])

    def test_auth_page_without_noindex_is_blocker(self):
        self.write("it/prodotto/learning-b2b/accesso/index.html", html())
        found = scan(self.site)
        self.assertEqual(found["summary"]["auth_noindex_violations"], 1)

    def test_external_links_fragments_and_locale_paths(self):
        self.assertIsNone(internal_reference("https://example.org/path", "it/index.html"))
        self.assertIsNone(internal_reference("#section", "it/index.html"))
        self.assertIsNone(internal_reference("/other-project/path", "it/index.html"))
        self.assertEqual(internal_reference("/manzo-ai/en/?lang=en", "it/index.html"), "en/index.html")
        self.assertEqual(internal_reference("../assets/file.svg", "it/index.html"), "assets/file.svg")


if __name__ == "__main__":
    unittest.main()
