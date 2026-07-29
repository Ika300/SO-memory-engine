from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "examples") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "examples"))

from demo_utils import write_demo_outputs
from evaluation_cases import all_evaluation_cases


def main() -> None:
    print("SO Memory Engine evaluation cases")
    print("=================================")
    for case in all_evaluation_cases():
        result = case.run()
        json_path, text_path = write_demo_outputs(f"evaluation_{case.name}", result, PROJECT_ROOT)
        print()
        print(case.name)
        print("-" * len(case.name))
        print(case.purpose)
        print(f"active memories: {len(result.active_memories)}")
        print(f"returning memories: {len(result.returning_memories)}")
        print(f"recurring structures: {len(result.recurring_structures)}")
        print(f"unresolved tensions: {len(result.unresolved_tensions)}")
        print(f"structural connections: {len(result.structural_connections)}")
        print(f"independent fragment count: {result.evidence_summary.independent_source_count}")
        print(f"unique source count: {result.evidence_summary.unique_source_count}")
        print(f"contextual recurrence count: {result.evidence_summary.contextual_recurrence_count}")
        print(f"saved json: {json_path}")
        print(f"saved text: {text_path}")


if __name__ == "__main__":
    main()
