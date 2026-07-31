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

from run_comparative_benchmarks import run_comparative_benchmarks


class ComparativeBenchmarkTests(unittest.TestCase):
    def test_comparative_benchmarks_pass(self) -> None:
        results = run_comparative_benchmarks()
        self.assertEqual(len(results), 3)
        failures = {result.name: result.failures for result in results if not result.passed}
        self.assertEqual(failures, {})

    def test_same_source_case_keeps_recurrence_separate_from_source_breadth(self) -> None:
        results = {result.name: result for result in run_comparative_benchmarks()}
        same_source = results["evidence_identity_same_source"]
        self.assertLess(
            same_source.metrics["so_unique_source_count"],
            same_source.metrics["so_contextual_recurrence_count"],
        )

    def test_independent_source_case_exposes_broader_source_breadth(self) -> None:
        results = {result.name: result for result in run_comparative_benchmarks()}
        independent = results["evidence_identity_independent_sources"]
        self.assertGreaterEqual(independent.metrics["so_unique_source_count"], 5)

    def test_comparative_runner_script_runs(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "benchmarks" / "run_comparative_benchmarks.py")],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("SO Memory Engine comparative benchmarks", completed.stdout)
        self.assertIn("Evidence Identity", completed.stdout)
        self.assertIn("3 passed, 0 failed, 3 total", completed.stdout)
        self.assertIn("no embeddings or LLM calls", completed.stdout)


if __name__ == "__main__":
    unittest.main()
