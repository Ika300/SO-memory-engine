from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if (PROJECT_ROOT.parent / "so_memory_engine").exists():
    ENGINE_ROOT = PROJECT_ROOT.parent
else:
    ENGINE_ROOT = PROJECT_ROOT.parent / "SO_Memory_Engine"
KERNEL_ROOT = PROJECT_ROOT.parent / "SO_Memory_Kernel"
for candidate in [PROJECT_ROOT, ENGINE_ROOT, KERNEL_ROOT]:
    if candidate.exists() and str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from so_extractor import extract_memory_units, load_conversation_json, memory_unit_to_engine_memory_dict, validate_memory_units
from so_memory_engine import EngineMemory, EngineRelation, MemoryEngine


def _engine_memory_from_dict(data: dict) -> EngineMemory:
    return EngineMemory(
        id=data["id"],
        content=data["content"],
        labels=list(data["labels"]),
        relations=[EngineRelation(**relation) for relation in data["relations"]],
        source_id=data.get("source_id"),
        space_id=data.get("space_id", "default"),
        importance=float(data.get("importance", 0.5)),
        persistence=float(data.get("persistence", 0.5)),
        valence=float(data.get("valence", 0.0)),
        arousal=float(data.get("arousal", 0.5)),
        certainty=float(data.get("certainty", 0.5)),
        novelty=float(data.get("novelty", 0.5)),
        abstraction=float(data.get("abstraction", 0.5)),
        bridge_potential=float(data.get("bridge_potential", 0.0)),
        tension_score=float(data.get("tension_score", 0.0)),
        gap_score=float(data.get("gap_score", 0.0)),
        metadata=dict(data.get("metadata", {})),
    )


def main() -> int:
    input_path = PROJECT_ROOT / "sample_inputs" / "conversation_log.json"
    messages = load_conversation_json(input_path)
    units = extract_memory_units(messages)
    report = validate_memory_units(units)
    if report.has_errors:
        print(report.to_markdown())
        return 1

    memories = [_engine_memory_from_dict(memory_unit_to_engine_memory_dict(unit)) for unit in units]
    result = MemoryEngine().build_context(
        current_message="I am thinking again about independence, work, and income stability.",
        current_labels=["work", "independently", "income", "stability"],
        current_relations=[EngineRelation("work", "independently", "tension", 0.7, False)],
        memories=memories,
    )

    print("SO Extractor end-to-end Engine demo")
    print("===================================")
    print(f"memory units: {len(units)}")
    print(f"active memories: {len(result.active_memories)}")
    print(f"returning memories: {len(result.returning_memories)}")
    print(f"recurring structures: {len(result.recurring_structures)}")
    print(f"unique source count: {result.evidence_summary.unique_source_count}")
    print(f"contextual recurrence count: {result.evidence_summary.contextual_recurrence_count}")
    print()
    print(result.context_pack.to_prompt_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())