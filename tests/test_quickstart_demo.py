from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class QuickstartDemoTests(unittest.TestCase):
    def test_quickstart_demo_runs_and_shows_engine_value(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "examples" / "quickstart_demo.py")],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        stdout = completed.stdout
        self.assertIn("SO Memory Engine quickstart", stdout)
        self.assertIn("Active memories selected for context", stdout)
        self.assertIn("Returning structures", stdout)
        self.assertIn("Recurring structures", stdout)
        self.assertIn("Unresolved tensions", stdout)
        self.assertIn("Evidence identity", stdout)
        self.assertIn("Context Pack role", stdout)
        self.assertIn("unique source count", stdout)
        self.assertNotIn("Core output", stdout)


if __name__ == "__main__":
    unittest.main()
