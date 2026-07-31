from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class CompleteQuickstartTests(unittest.TestCase):
    def test_top_level_quickstart_runs_engine_only_demo(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "quickstart.py")],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("SO Memory Engine quickstart", completed.stdout)
        self.assertIn("curated MemoryUnits", completed.stdout)
        self.assertIn("No extractor, LLM, embedding model, or external API is used.", completed.stdout)
        self.assertIn("outputs", completed.stdout)
        self.assertTrue((PROJECT_ROOT / "outputs" / "engine_quickstart" / "context_pack.txt").exists())
        self.assertTrue((PROJECT_ROOT / "outputs" / "engine_quickstart" / "context_pack.json").exists())
        self.assertTrue((PROJECT_ROOT / "outputs" / "engine_quickstart" / "engine_result.json").exists())


if __name__ == "__main__":
    unittest.main()