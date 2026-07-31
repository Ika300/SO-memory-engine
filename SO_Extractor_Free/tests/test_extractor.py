from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from so_extractor import extract_labels, extract_memory_units, load_chatgpt_export_like_json, load_conversation_json, memory_unit_to_engine_memory_dict, validate_memory_units


class ExtractorTests(unittest.TestCase):
    def test_load_conversation_json(self) -> None:
        messages = load_conversation_json(PROJECT_ROOT / "sample_inputs" / "conversation_log.json")
        self.assertEqual(len(messages), 4)
        self.assertEqual(messages[0].role, "user")

    def test_load_chatgpt_export_like_json(self) -> None:
        messages = load_chatgpt_export_like_json(PROJECT_ROOT / "sample_inputs" / "chatgpt_export_like.json")
        self.assertEqual(len(messages), 4)
        self.assertEqual(messages[0].role, "user")
        self.assertEqual(messages[0].conversation_id, "chatgpt_like_conversation_001")
        self.assertEqual(messages[0].source_id, "chatgpt_export_like_sample")

    def test_chatgpt_export_like_demo_runs(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "examples" / "chatgpt_export_like_demo.py")],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("SO Extractor ChatGPT export-like demo", completed.stdout)
        self.assertIn("valid units", completed.stdout)

    def test_extract_labels_is_transparent_word_based(self) -> None:
        labels = extract_labels("I want independent work but income stability worries me.")
        self.assertIn("independent", labels)
        self.assertIn("income", labels)

    def test_extract_memory_units_skips_assistant_messages(self) -> None:
        messages = load_conversation_json(PROJECT_ROOT / "sample_inputs" / "conversation_log.json")
        units = extract_memory_units(messages)
        self.assertEqual(len(units), 3)
        self.assertTrue(all(unit.source_id for unit in units))

    def test_validation_passes_sample_units(self) -> None:
        units = extract_memory_units(load_conversation_json(PROJECT_ROOT / "sample_inputs" / "conversation_log.json"))
        report = validate_memory_units(units)
        self.assertFalse(report.has_errors)
        self.assertEqual(report.valid_units, len(units))

    def test_engine_export_shape(self) -> None:
        units = extract_memory_units(load_conversation_json(PROJECT_ROOT / "sample_inputs" / "conversation_log.json"))
        data = memory_unit_to_engine_memory_dict(units[0])
        self.assertIn("labels", data)
        self.assertIn("relations", data)
        self.assertIn("source_id", data)
        self.assertIn("metadata", data)

    def test_conversation_log_demo_runs(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "examples" / "conversation_log_demo.py")],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("SO Extractor conversation log demo", completed.stdout)
        self.assertIn("valid units", completed.stdout)

    def test_end_to_end_engine_demo_runs(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "examples" / "end_to_end_engine_demo.py")],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("SO Extractor end-to-end Engine demo", completed.stdout)
        self.assertIn("active memories", completed.stdout)
        self.assertIn("STRUCTURAL MEMORY CONTEXT", completed.stdout)


if __name__ == "__main__":
    unittest.main()
