from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from demo_utils import write_demo_outputs
from so_memory_engine import EngineMemory, EngineRelation, MemoryEngine


def main() -> None:
    memories = [
        EngineMemory(
            id="m1",
            content="The user keeps returning to memory and structure as a way to avoid flattening meaning.",
            labels=["memory", "structure", "meaning"],
            relations=[
                EngineRelation("memory", "structure", relation_type="bridge", strength=0.8, directed=False),
                EngineRelation("structure", "meaning", relation_type="support", strength=0.7, directed=True),
            ],
            importance=0.8,
            persistence=0.8,
            bridge_potential=0.8,
            source_id="note_001",
        ),
        EngineMemory(
            id="m2",
            content="The user distrusts approximate semantic merging because it can distort the original structure.",
            labels=["approximation", "distortion", "structure"],
            relations=[
                EngineRelation("approximation", "distortion", relation_type="cause", strength=0.8, directed=True),
                EngineRelation("distortion", "structure", relation_type="tension", strength=0.8, directed=True),
            ],
            importance=0.8,
            persistence=0.7,
            valence=-0.4,
            tension_score=0.8,
            source_id="note_002",
        ),
        EngineMemory(
            id="m3",
            content="The user wants AI memory to preserve repetition, tension, connection, and return.",
            labels=["memory", "repetition", "tension", "return"],
            relations=[
                EngineRelation("memory", "return", relation_type="support", strength=0.7, directed=True),
                EngineRelation("repetition", "tension", relation_type="association", strength=0.6, directed=False),
            ],
            importance=0.7,
            persistence=0.8,
            source_id="note_003",
        ),
    ]

    engine = MemoryEngine()
    result = engine.build_context(
        current_message="I keep coming back to the difference between memory and similarity.",
        memories=memories,
        current_labels=["memory", "similarity", "structure"],
        current_relations=[
            EngineRelation("memory", "similarity", relation_type="tension", strength=0.8, directed=False),
            EngineRelation("memory", "structure", relation_type="bridge", strength=0.8, directed=False),
        ],
    )

    print("SO Memory Engine demo")
    print("=====================")
    print()
    print(result.context_pack.to_prompt_text())
    print()
    print("Counts")
    print("------")
    print(f"active memories: {len(result.active_memories)}")
    print(f"returning memories: {len(result.returning_memories)}")
    print(f"recurring structures: {len(result.recurring_structures)}")
    print(f"unresolved tensions: {len(result.unresolved_tensions)}")
    print(f"structural connections: {len(result.structural_connections)}")
    json_path, text_path = write_demo_outputs("llm_memory_engine_demo", result, PROJECT_ROOT)
    print()
    print(f"Saved JSON: {json_path}")
    print(f"Saved text: {text_path}")


if __name__ == "__main__":
    main()
