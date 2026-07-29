from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "examples") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "examples"))

from evaluation_cases import (
    all_evaluation_cases,
    direction_preservation_case,
    independent_sources_case,
    noise_no_return_case,
    reactivation_case,
    same_source_repetition_case,
)


class EvaluationCaseTests(unittest.TestCase):
    def test_all_evaluation_cases_run(self) -> None:
        cases = all_evaluation_cases()
        self.assertEqual(len(cases), 5)
        for case in cases:
            result = case.run()
            self.assertEqual(result.context_pack.current_message, case.current_message)
            self.assertIsInstance(result.to_dict(), dict)

    def test_same_source_repetition_creates_recurring_structure(self) -> None:
        result = same_source_repetition_case().run()
        self.assertGreaterEqual(len(result.recurring_structures), 1)
        self.assertGreaterEqual(result.evidence_summary.contextual_recurrence_count, 1)

    def test_independent_sources_expose_more_source_breadth_than_same_source_case(self) -> None:
        same_result = same_source_repetition_case().run()
        independent_result = independent_sources_case().run()
        self.assertGreaterEqual(
            independent_result.evidence_summary.independent_source_count,
            same_result.evidence_summary.independent_source_count,
        )
        self.assertGreaterEqual(len(independent_result.active_memories), 1)

    def test_reactivation_case_returns_prior_memory(self) -> None:
        result = reactivation_case().run()
        self.assertGreaterEqual(len(result.returning_memories), 1)
        active_ids = {memory.fragment_id for memory in result.active_memories}
        self.assertIn("reactivation_past", active_ids)

    def test_noise_case_does_not_create_return_or_active_memory(self) -> None:
        result = noise_no_return_case().run()
        self.assertEqual(result.returning_memories, [])
        self.assertEqual(result.active_memories, [])

    def test_reversed_direction_does_not_reactivate_exact_pattern_identity(self) -> None:
        result = direction_preservation_case().run()
        self.assertEqual(result.returning_memories, [])
        self.assertEqual(result.active_memories, [])

    def test_evaluation_runner_script_runs(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "examples" / "run_evaluation_cases.py")],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("SO Memory Engine evaluation cases", completed.stdout)
        self.assertIn("same_source_repetition", completed.stdout)
        self.assertIn("direction_preservation", completed.stdout)


if __name__ == "__main__":
    unittest.main()
