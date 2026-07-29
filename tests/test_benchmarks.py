from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "benchmarks") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "benchmarks"))

from run_benchmarks import run_benchmarks


class EngineBenchmarkTests(unittest.TestCase):
    def test_engine_benchmarks_pass(self) -> None:
        results = run_benchmarks()
        self.assertEqual(len(results), 6)
        failures = {result.name: result.failures for result in results if not result.passed}
        self.assertEqual(failures, {})

    def test_benchmark_runner_script_runs(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "benchmarks" / "run_benchmarks.py")],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("SO Memory Engine benchmarks", completed.stdout)
        self.assertIn("same_source_repetition", completed.stdout)
        self.assertIn("mixed_scale_30_fragments", completed.stdout)
        self.assertIn("6 passed, 0 failed, 6 total", completed.stdout)


if __name__ == "__main__":
    unittest.main()
