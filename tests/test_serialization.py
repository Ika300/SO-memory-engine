from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "examples") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "examples"))

from demo_utils import write_demo_outputs
from so_memory_engine import EngineMemory, EngineRelation, MemoryEngine


class SerializationTests(unittest.TestCase):
    def build_result(self):
        engine = MemoryEngine()
        return engine.build_context(
            current_message="memory and structure return",
            current_labels=["memory", "structure"],
            current_relations=[EngineRelation("memory", "structure", "bridge", 0.8, False)],
            memories=[
                EngineMemory(
                    id="m1",
                    content="past memory and structure",
                    labels=["memory", "structure"],
                    relations=[EngineRelation("memory", "structure", "bridge", 0.8, False)],
                    bridge_potential=0.8,
                )
            ],
        )

    def test_context_pack_to_dict_is_json_serializable(self) -> None:
        result = self.build_result()
        payload = result.context_pack.to_dict()
        encoded = json.dumps(payload, ensure_ascii=False)
        self.assertIn("current_message", payload)
        self.assertIn("active_memories", payload)
        self.assertIn("memory and structure return", encoded)

    def test_result_to_dict_is_json_serializable(self) -> None:
        result = self.build_result()
        payload = result.to_dict()
        encoded = json.dumps(payload, ensure_ascii=False)
        self.assertIn("context_pack", payload)
        self.assertIn("has_insight", payload)
        self.assertIn("returning_memories", encoded)

    def test_demo_writer_saves_json_and_text(self) -> None:
        result = self.build_result()
        with tempfile.TemporaryDirectory() as tmpdir:
            json_path, text_path = write_demo_outputs("serialization_test", result, Path(tmpdir))
            self.assertTrue(json_path.exists())
            self.assertTrue(text_path.exists())
            loaded = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(loaded["context_pack"]["current_message"], "memory and structure return")
            self.assertIn("STRUCTURAL MEMORY CONTEXT", text_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
