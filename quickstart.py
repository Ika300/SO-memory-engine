from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent
EXTRACTOR_ROOT = PROJECT_ROOT / "SO_Extractor_Free"
KERNEL_ROOT = PROJECT_ROOT.parent / "SO_Memory_Kernel"

for candidate in [PROJECT_ROOT, EXTRACTOR_ROOT, KERNEL_ROOT]:
    if candidate.exists() and str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from so_extractor import extract_memory_units, load_conversation_json, memory_unit_to_engine_memory_dict, validate_memory_units
from so_memory_engine import EngineMemory, EngineRelation, MemoryEngine

DEFAULT_INPUT = EXTRACTOR_ROOT / "sample_inputs" / "conversation_log.json"
DEFAULT_CURRENT_MESSAGE = "I want to work independently, but income stability worries me again."
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "free_trial"


def _engine_memory_from_dict(data: dict[str, Any]) -> EngineMemory:
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


def _write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _current_unit_from_message(message: str):
    # The current message goes through the same transparent Free Extractor path
    # as historical messages. This keeps the public demo honest: no hidden
    # hand-authored labels for the current turn.
    from so_extractor import ConversationMessage

    units = extract_memory_units([
        ConversationMessage(
            id="current_message",
            role="user",
            text=message,
            conversation_id="current",
            source_id="current_message",
        )
    ])
    if not units:
        raise ValueError("current message produced no MemoryUnit; provide a clearer current message")
    current_unit = units[0]
    current_unit.id = "current_memory_unit"
    current_unit.message_ids = ["current_message"]
    return current_unit


def run_pipeline(input_path: Path, current_message: str, output_dir: Path) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)

    messages = load_conversation_json(input_path)
    historical_units = extract_memory_units(messages)
    current_unit = _current_unit_from_message(current_message)
    report = validate_memory_units(historical_units + [current_unit])
    if report.has_errors:
        print(report.to_markdown())
        return 1

    engine_memory_dicts = [memory_unit_to_engine_memory_dict(unit) for unit in historical_units]
    current_dict = memory_unit_to_engine_memory_dict(current_unit)
    memories = [_engine_memory_from_dict(data) for data in engine_memory_dicts]
    current_relations = [EngineRelation(**relation) for relation in current_dict["relations"]]

    result = MemoryEngine().build_context(
        current_message=current_message,
        current_labels=list(current_dict["labels"]),
        current_relations=current_relations,
        memories=memories,
    )

    _write_json(output_dir / "01_normalized_messages.json", [message.to_dict() for message in messages])
    _write_json(output_dir / "02_memory_units.json", [unit.to_dict() for unit in historical_units])
    (output_dir / "03_validation_report.md").write_text(report.to_markdown(), encoding="utf-8")
    _write_json(output_dir / "04_engine_memories.json", engine_memory_dicts)
    _write_json(output_dir / "05_current_memory_unit.json", current_unit.to_dict())
    _write_json(output_dir / "06_context_pack.json", result.context_pack.to_dict())
    (output_dir / "07_context_pack.txt").write_text(result.context_pack.to_prompt_text(), encoding="utf-8")
    _write_json(output_dir / "08_engine_result.json", result.to_dict())

    print("SO Memory Engine + Extractor Free quickstart")
    print("============================================")
    print(f"input: {input_path}")
    print(f"current message: {current_message}")
    print(f"historical messages loaded: {len(messages)}")
    print(f"historical memory units: {len(historical_units)}")
    print(f"current labels: {', '.join(current_dict['labels']) or '<none>'}")
    print(f"active memories: {len(result.active_memories)}")
    print(f"returning memories: {len(result.returning_memories)}")
    print(f"recurring structures: {len(result.recurring_structures)}")
    print(f"unique source count: {result.evidence_summary.unique_source_count}")
    print(f"contextual recurrence count: {result.evidence_summary.contextual_recurrence_count}")
    print()
    print("Done.")
    print(f"Open: {output_dir / '07_context_pack.txt'}")
    print(f"Inspect the full pipeline: {output_dir}")
    print()
    print("Boundary: Extractor Free is transparent and rule-based. It proves the path, not production parsing quality.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the complete SO free pipeline: conversation log -> Extractor Free -> Engine -> Context Pack.")
    parser.add_argument("input", nargs="?", default=str(DEFAULT_INPUT), help="Path to a simple conversation JSON file. Defaults to the bundled sample.")
    parser.add_argument("--current", default=DEFAULT_CURRENT_MESSAGE, help="Current user message to structure and compare against the historical log.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for generated pipeline outputs.")
    args = parser.parse_args()

    return run_pipeline(Path(args.input), args.current, Path(args.output_dir))


if __name__ == "__main__":
    raise SystemExit(main())