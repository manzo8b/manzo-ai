import unittest
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[2]
PUBLISHER = ROOT / "theme" / "publish-prompt-video.py"
BASE = ROOT / "site-v0.7.zip"


class PromptMasteryRouteRegression(unittest.TestCase):
    def test_video_call_to_action_points_to_an_existing_lesson(self):
        source = PUBLISHER.read_text(encoding="utf-8")
        expected = "/manzo-ai/it/prompt-mastery/che-cos-e-un-prompt/"
        self.assertIn(f'href="{expected}"', source)
        self.assertNotIn('href="/manzo-ai/it/prompt-mastery/"', source)

    def test_target_exists_in_published_base_archive(self):
        with ZipFile(BASE) as release:
            members = {member.lstrip("./") for member in release.namelist()}
        self.assertIn("it/prompt-mastery/che-cos-e-un-prompt/index.html", members)


if __name__ == "__main__":
    unittest.main()
