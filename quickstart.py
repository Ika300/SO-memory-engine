from __future__ import annotations

import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
KERNEL_ROOT = PROJECT_ROOT.parent / "SO_Memory_Kernel"

for candidate in [PROJECT_ROOT, KERNEL_ROOT]:
    if candidate.exists() and str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

try:
    from so_memory_engine import EngineMemory, EngineRelation, MemoryEngine
except ModuleNotFoundError as exc:
    if exc.name in {"so_memory_engine", "so_memory_kernel"}:
        print("SO Memory Engine or SO Memory Kernel is not installed or not importable.")
        print()
        print("Expected alpha layout:")
        print()
        print("  Desktop/")
        print("    SO_Memory_Kernel/")
        print("    SO_Memory_Engine/")
        print()
        print("From SO_Memory_Engine, run:")
        print()
        print("  py -3 -m pip install -e ..\\SO_Memory_Kernel")
        print("  py -3 -m pip install -e .")
        print()
        print("Or run the Windows helper:")
        print()
        print("  setup_engine_demo.bat")
        print()
        print("See docs/INSTALLATION.md for details.")
        raise SystemExit(1) from exc
    raise

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "engine_quickstart"
CURRENT_MESSAGE = "I keep returning to why memory should not be just similarity search."


def _build_curated_memories() -> list[EngineMemory]:
    return [
        EngineMemory(
            id="memory_001",
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
            id="memory_002",
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
            id="memory_003",
            content="A separate project note treated recurring evidence and independent evidence as different things.",
            labels=["evidence", "recurrence", "independence"],
            relations=[
                EngineRelation("recurrence", "independence", "tension", 0.8, False),
                EngineRelation("evidence", "recurrence", "association", 0.7, True),
            ],
            tension_score=0.8,
            source_id="source_evidence_identity",
        ),
        EngineMemory(
            id="memory_004",
            content="An unrelated note about coffee, weather, and errands should remain background noise.",
            labels=["coffee", "weather", "errands"],
            source_id="source_noise",
        ),
    ]


def _write_outputs(result) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "context_pack.txt").write_text(result.context_pack.to_prompt_text(), encoding="utf-8")
    (OUTPUT_DIR / "context_pack.json").write_text(
        json.dumps(result.context_pack.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "engine_result.json").write_text(
        json.dumps(result.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _labels(labels: list[str]) -> str:
    return " / ".join(labels) if labels else "unlabeled"


def main() -> None:
    memories = _build_curated_memories()
    result = MemoryEngine().build_context(
        current_message=CURRENT_MESSAGE,
        current_labels=["memory", "similarity", "structure", "evidence"],
        current_relations=[
            EngineRelation("memory", "similarity", "tension", 0.8, False),
            EngineRelation("memory", "structure", "bridge", 0.8, False),
            EngineRelation("evidence", "memory", "association", 0.7, True),
        ],
        memories=memories,
    )
    _write_outputs(result)

    evidence = result.evidence_summary
    print("SO Memory Engine quickstart")
    print("===========================")
    print()
    print("This demo uses curated MemoryUnits so the Engine behavior is visible immediately.")
    print("No extractor, LLM, embedding model, or external API is used.")
    print()
    print("Current message:")
    print(f"  {CURRENT_MESSAGE}")
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
    print(f"  - independent fragment count: {evidence.independent_source_count}")
    print(f"  - unique source count: {evidence.unique_source_count}")
    print(f"  - contextual recurrence count: {evidence.contextual_recurrence_count}")
    print()
    print("Outputs written to:")
    print(f"  {OUTPUT_DIR / 'context_pack.txt'}")
    print(f"  {OUTPUT_DIR / 'context_pack.json'}")
    print(f"  {OUTPUT_DIR / 'engine_result.json'}")
    print()
    print("Context Pack role:")
    print("  This is structural memory context for an AI app.")
    print("  It is not a final LLM response, not a parser, and not semantic search.")


if __name__ == "__main__":
    main()