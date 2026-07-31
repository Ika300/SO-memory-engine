from __future__ import annotations

import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from so_extractor import export_engine_memories, extract_memory_units, load_chatgpt_export_like_json, validate_memory_units


def main() -> int:
    input_path = PROJECT_ROOT / "sample_inputs" / "chatgpt_export_like.json"
    output_dir = PROJECT_ROOT / "sample_outputs" / "chatgpt_export_like"
    output_dir.mkdir(parents=True, exist_ok=True)

    messages = load_chatgpt_export_like_json(input_path)
    units = extract_memory_units(messages)
    report = validate_memory_units(units)

    normalized_messages_path = output_dir / "normalized_messages.json"
    memory_units_path = output_dir / "memory_units.json"
    engine_memories_path = output_dir / "engine_memories.json"
    report_path = output_dir / "validation_report.md"

    normalized_messages_path.write_text(
        json.dumps([message.to_dict() for message in messages], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    memory_units_path.write_text(
        json.dumps([unit.to_dict() for unit in units], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    export_engine_memories(units, engine_memories_path)
    report_path.write_text(report.to_markdown(), encoding="utf-8")

    print("SO Extractor ChatGPT export-like demo")
    print("=====================================")
    print(f"messages loaded: {len(messages)}")
    print(f"memory units: {len(units)}")
    print(f"valid units: {report.valid_units}/{report.total_units}")
    print(f"issues: {len(report.issues)}")
    print(f"normalized messages json: {normalized_messages_path}")
    print(f"memory units json: {memory_units_path}")
    print(f"engine memories json: {engine_memories_path}")
    print(f"validation report: {report_path}")
    print()
    print("Caution: this is an export-like convenience demo, not full ChatGPT export coverage.")
    return 1 if report.has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())