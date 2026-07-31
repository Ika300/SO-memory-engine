from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from so_memory_engine import EngineMemory, EngineRelation, MemoryEngine


def _labels(labels: list[str]) -> str:
    return " / ".join(labels) if labels else "unlabeled"


def main() -> None:
    memories = [
        EngineMemory(
            id="note_001",
            content="Earlier, the user connected memory with structure instead of similarity.",
            labels=["memory", "structure", "similarity"],
            relations=[
                EngineRelation("memory", "structure", "bridge", 0.8, False),
                EngineRelation("memory", "similarity", "tension", 0.8, False),
            ],
            bridge_potential=0.8,
            tension_score=0.8,
            source_id="source_memory_design",
        ),
        EngineMemory(
            id="note_002",
            content="A later note returned to the idea that structure protects meaning from being flattened.",
            labels=["structure", "meaning", "flattening"],
            relations=[
                EngineRelation("structure", "meaning", "support", 0.7, True),
                EngineRelation("flattening", "meaning", "tension", 0.7, True),
            ],
            tension_score=0.7,
            source_id="source_memory_design",
        ),
        EngineMemory(
            id="note_003",
            content="An unrelated note about coffee, weather, and errands should remain background noise.",
            labels=["coffee", "weather", "errands"],
            source_id="source_noise",
        ),
    ]

    result = MemoryEngine().build_context(
        current_message="I keep coming back to why memory should not be just similarity search.",
        current_labels=["memory", "similarity", "structure"],
        current_relations=[
            EngineRelation("memory", "similarity", "tension", 0.8, False),
            EngineRelation("memory", "structure", "bridge", 0.8, False),
        ],
        memories=memories,
    )

    evidence = result.evidence_summary

    print("SO Memory Engine quickstart")
    print("===========================")
    print()
    print("Current message:")
    print("  I keep coming back to why memory should not be just similarity search.")
    print()
    print("Active memories selected for context:")
    if result.active_memories:
        for memory in result.active_memories:
            print(f"  - {memory.fragment_id}: {_labels(memory.labels)}")
    else:
        print("  - none")
    print()
    print("Returning structures:")
    if result.returning_memories:
        for item in result.returning_memories:
            print(f"  - {item.label}")
    else:
        print("  - none")
    print()
    print("Recurring structures:")
    if result.recurring_structures:
        for structure in result.recurring_structures:
            print(
                f"  - {structure.pattern_type}: {_labels(structure.member_nodes)} "
                f"(occurrences={structure.occurrence_count})"
            )
    else:
        print("  - none")
    print()
    print("Unresolved tensions:")
    if result.unresolved_tensions:
        for tension in result.unresolved_tensions[:3]:
            print(f"  - {_labels(tension.member_nodes)}")
    else:
        print("  - none")
    print()
    print("Evidence identity:")
    print(f"  - trace fragment count: {evidence.trace_fragment_count}")
    print(f"  - unique source count: {evidence.unique_source_count}")
    print(f"  - contextual recurrence count: {evidence.contextual_recurrence_count}")
    print()
    print("Context Pack role:")
    print("  This is structural memory context for an AI app.")
    print("  It is not the final LLM response and not a semantic search result.")


if __name__ == "__main__":
    main()
