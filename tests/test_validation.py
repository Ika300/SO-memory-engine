from __future__ import annotations

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from so_memory_engine import EngineMemory, EngineRelation, MemoryEngine, MemoryEngineValidationError


class ValidationTests(unittest.TestCase):
    def test_empty_current_message_rejected(self) -> None:
        with self.assertRaises(MemoryEngineValidationError):
            MemoryEngine().build_context(current_message="", memories=[])

    def test_duplicate_memory_id_rejected(self) -> None:
        with self.assertRaises(MemoryEngineValidationError):
            MemoryEngine().build_context(
                current_message="current",
                memories=[
                    EngineMemory(id="m1", content="one", labels=["one"]),
                    EngineMemory(id="m1", content="two", labels=["two"]),
                ],
            )

    def test_current_id_conflict_rejected(self) -> None:
        with self.assertRaises(MemoryEngineValidationError):
            MemoryEngine().build_context(
                current_message="current",
                current_id="m1",
                memories=[EngineMemory(id="m1", content="past", labels=["past"])],
            )

    def test_memory_relation_endpoint_must_reference_label(self) -> None:
        with self.assertRaises(MemoryEngineValidationError):
            MemoryEngine().build_context(
                current_message="current",
                memories=[
                    EngineMemory(
                        id="m1",
                        content="past",
                        labels=["memory"],
                        relations=[EngineRelation("memory", "missing", "bridge", 0.8, False)],
                    )
                ],
            )

    def test_current_relation_endpoint_must_reference_current_label(self) -> None:
        with self.assertRaises(MemoryEngineValidationError):
            MemoryEngine().build_context(
                current_message="current",
                current_labels=["memory"],
                current_relations=[EngineRelation("memory", "missing", "bridge", 0.8, False)],
                memories=[],
            )

    def test_relation_without_labels_rejected(self) -> None:
        with self.assertRaises(MemoryEngineValidationError):
            MemoryEngine().build_context(
                current_message="current",
                memories=[
                    EngineMemory(
                        id="m1",
                        content="past",
                        relations=[EngineRelation("a", "b", "bridge", 0.8, False)],
                    )
                ],
            )

    def test_score_must_be_float_in_range(self) -> None:
        with self.assertRaises(MemoryEngineValidationError):
            MemoryEngine().build_context(
                current_message="current",
                memories=[EngineMemory(id="m1", content="past", labels=["past"], importance=1.2)],
            )

    def test_invalid_relation_type_rejected(self) -> None:
        with self.assertRaises(MemoryEngineValidationError):
            MemoryEngine().build_context(
                current_message="current",
                current_labels=["a", "b"],
                current_relations=[EngineRelation("a", "b", "invented", 0.8, False)],
                memories=[],
            )

    def test_valid_input_still_runs(self) -> None:
        result = MemoryEngine().build_context(
            current_message="memory returns",
            current_labels=["memory", "return"],
            current_relations=[EngineRelation("memory", "return", "bridge", 0.8, False)],
            memories=[
                EngineMemory(
                    id="m1",
                    content="past memory returns",
                    labels=["memory", "return"],
                    relations=[EngineRelation("memory", "return", "bridge", 0.8, False)],
                    bridge_potential=0.8,
                )
            ],
        )
        self.assertGreaterEqual(len(result.returning_memories), 1)


if __name__ == "__main__":
    unittest.main()
