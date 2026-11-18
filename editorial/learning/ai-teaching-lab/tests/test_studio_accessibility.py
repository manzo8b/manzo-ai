"""Regression checks for studio landmarks and scripts containing exported HTML."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[4]
SPEC = importlib.util.spec_from_file_location("studio_publisher", ROOT / "theme/publish-ai-teaching-lab.py")
PUBLISHER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PUBLISHER)


class StudioAccessibilityTests(unittest.TestCase):
    def test_exported_html_in_script_remains_untouched(self):
        script = '<script>const exported="<html><head></head><body><main>Kit</main></body></html>";</script>'
        original = '<html><head><title>Studio</title></head><body class="tool"><main class="activity">Task</main>' + script + '</body></html>'
        result = PUBLISHER.accessible_studio(original, "workspace")
        self.assertIn(script, result)
        self.assertEqual(result.count('href="../studio-accessibility.css"'), 1)
        self.assertIn('<body class="tool" data-atl-tool="workspace">', result)
        self.assertIn('<main class="activity" id="atl-studio-main" tabindex="-1">', result)
        self.assertIn('href="#atl-studio-main"', result)

    def test_existing_main_id_and_attributes_are_preserved(self):
        original = '<html><head></head><body><main id="activity" class="work">Task</main></body></html>'
        result = PUBLISHER.accessible_studio(original, "image")
        self.assertIn('<main id="activity" class="work" tabindex="-1">', result)
        self.assertIn('href="#activity"', result)
        self.assertNotIn('id="atl-studio-main"', result)

    def test_multiple_main_landmarks_are_rejected(self):
        original = '<html><head></head><body><main>One</main><main>Two</main></body></html>'
        with self.assertRaisesRegex(RuntimeError, "Unexpected standalone studio structure"):
            PUBLISHER.accessible_studio(original, "video")


if __name__ == "__main__":
    unittest.main()
