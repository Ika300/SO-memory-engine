from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class CompleteQuickstartTests(unittest.TestCase):
    def test_top_level_quickstart_runs_complete_free_pipeline(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "quickstart.py")],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("SO Memory Engine + Extractor Free quickstart", completed.stdout)
        self.assertIn("historical memory units", completed.stdout)
        self.assertIn("Open:", completed.stdout)
        self.assertTrue((PROJECT_ROOT / "outputs" / "free_trial" / "07_context_pack.txt").exists())
        self.assertTrue((PROJECT_ROOT / "outputs" / "free_trial" / "05_current_memory_unit.json").exists())

    def test_top_level_quickstart_accepts_custom_current_message(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(PROJECT_ROOT / "quickstart.py"),
                "--current",
                "I keep returning to work, money, and independence.",
            ],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("current labels:", completed.stdout)
        self.assertIn("Inspect the full pipeline", completed.stdout)


if __name__ == "__main__":
    unittest.main()