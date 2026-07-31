from __future__ import annotations

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from so_memory_engine import EngineMemory, EngineRelation, MemoryEngine, MemoryEngineInput


class MemoryEngineTests(unittest.TestCase):
    def test_build_context_returns_context_pack_without_llm(self) -> None:
        engine = MemoryEngine()
        result = engine.build_context(
            current_message="memory returns to structure",
            current_labels=["memory", "structure"],
            current_relations=[EngineRelation("memory", "structure", "bridge", 0.8, False)],
            memories=[
                EngineMemory(
                    id="m1",
                    content="memory and structure appeared before",
                    labels=["memory", "structure"],
                    relations=[EngineRelation("memory", "structure", "bridge", 0.8, False)],
                    bridge_potential=0.8,
                ),
            ],
        )
        self.assertEqual(result.context_pack.current_message, "memory returns to structure")
        self.assertIn("STRUCTURAL MEMORY CONTEXT", result.context_pack.to_prompt_text())

    def test_current_structure_can_reactivate_past_memory(self) -> None:
        engine = MemoryEngine()
        result = engine.build_context(
            MemoryEngineInput(
                current_message="structure and meaning are returning",
                current_labels=["structure", "meaning"],
                current_relations=[EngineRelation("structure", "meaning", "bridge", 0.8, False)],
                memories=[
                    EngineMemory(
                        id="past_1",
                        content="old memory about structure and meaning",
                        labels=["structure", "meaning"],
                        relations=[EngineRelation("structure", "meaning", "bridge", 0.8, False)],
                        bridge_potential=0.8,
                    )
                ],
            )
        )
        active_ids = {memory.fragment_id for memory in result.active_memories}
        self.assertIn("past_1", active_ids)
        self.assertGreaterEqual(len(result.returning_memories), 1)

    def test_evidence_summary_distinguishes_counts(self) -> None:
        engine = MemoryEngine()
        result = engine.build_context(
            current_message="memory and structure again",
            current_labels=["memory", "structure"],
            current_relations=[EngineRelation("memory", "structure", "bridge", 0.8, False)],
            memories=[
                EngineMemory(
                    id="m1",
                    content="first source",
                    labels=["memory", "structure"],
                    relations=[EngineRelation("memory", "structure", "bridge", 0.8, False)],
                    bridge_potential=0.8,
                    source_id="source_a",
                ),
                EngineMemory(
                    id="m2",
                    content="second source",
                    labels=["memory", "structure"],
                    relations=[EngineRelation("memory", "structure", "bridge", 0.8, False)],
                    bridge_potential=0.8,
                    source_id="source_b",
                ),
            ],
        )
        self.assertGreaterEqual(result.evidence_summary.trace_fragment_count, 1)
        self.assertGreaterEqual(result.evidence_summary.contextual_recurrence_count, 1)

    def test_no_semantic_dictionary_is_used_for_unrelated_labels(self) -> None:
        engine = MemoryEngine()
        result = engine.build_context(
            current_message="alpha current",
            current_labels=["alpha"],
            memories=[
                EngineMemory(id="m1", content="beta past", labels=["beta"]),
                EngineMemory(id="m2", content="gamma past", labels=["gamma"]),
            ],
        )
        self.assertEqual(result.returning_memories, [])
        self.assertEqual(result.active_memories, [])

    def test_context_pack_caution_preserves_boundary(self) -> None:
        engine = MemoryEngine()
        result = engine.build_context(
            current_message="memory",
            current_labels=["memory"],
            memories=[EngineMemory(id="m1", content="memory", labels=["memory"])],
        )
        self.assertIn("Do not invent user history", result.context_pack.caution)
        self.assertIn("not the response itself", result.context_pack.to_prompt_text())


if __name__ == "__main__":
    unittest.main()
