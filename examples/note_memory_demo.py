from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from demo_utils import write_demo_outputs
from so_memory_engine import EngineMemory, EngineRelation, MemoryEngine


def main() -> None:
    engine = MemoryEngine()
    memories = [
        EngineMemory(
            id="note_001",
            content="A note says that writing should preserve unfinished questions rather than compress them into conclusions.",
            labels=["writing", "unfinished questions", "conclusions"],
            relations=[
                EngineRelation("writing", "unfinished questions", "support", 0.8, True),
                EngineRelation("unfinished questions", "conclusions", "tension", 0.8, False),
            ],
            tension_score=0.8,
            persistence=0.8,
        ),
        EngineMemory(
            id="note_002",
            content="Another note connects research notes with return, repetition, and slow structural development.",
            labels=["research notes", "return", "repetition", "development"],
            relations=[
                EngineRelation("research notes", "return", "bridge", 0.8, False),
                EngineRelation("repetition", "development", "support", 0.7, True),
            ],
            bridge_potential=0.8,
            persistence=0.8,
        ),
    ]

    result = engine.build_context(
        current_message="This new note again feels unfinished, but maybe that unfinished quality matters.",
        current_labels=["unfinished questions", "writing", "return"],
        current_relations=[
            EngineRelation("writing", "unfinished questions", "support", 0.8, True),
            EngineRelation("unfinished questions", "return", "association", 0.7, False),
        ],
        memories=memories,
    )

    print("Note app memory demo")
    print("====================")
    print("A note app can use the Engine to show what old structure is active again.")
    print()
    print(result.context_pack.to_prompt_text())
    json_path, text_path = write_demo_outputs("note_memory_demo", result, PROJECT_ROOT)
    print()
    print(f"Saved JSON: {json_path}")
    print(f"Saved text: {text_path}")


if __name__ == "__main__":
    main()
