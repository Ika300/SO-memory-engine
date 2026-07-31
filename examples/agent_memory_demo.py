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
            id="agent_001",
            content="The agent repeatedly fails when task planning ignores unresolved blockers.",
            labels=["task planning", "blocker", "failure"],
            relations=[
                EngineRelation("task planning", "blocker", "tension", 0.8, True),
                EngineRelation("blocker", "failure", "cause", 0.8, True),
            ],
            tension_score=0.8,
            importance=0.8,
        ),
        EngineMemory(
            id="agent_002",
            content="The agent improved when blockers were preserved as structural memory instead of overwritten by new steps.",
            labels=["blocker", "structural memory", "new steps"],
            relations=[
                EngineRelation("blocker", "structural memory", "support", 0.8, True),
                EngineRelation("structural memory", "new steps", "dependency", 0.7, True),
            ],
            importance=0.8,
            persistence=0.8,
        ),
        EngineMemory(
            id="agent_003",
            content="A repeated deployment issue returned after several unrelated tasks.",
            labels=["deployment", "return", "unrelated tasks"],
            relations=[
                EngineRelation("deployment", "return", "association", 0.7, False),
                EngineRelation("return", "unrelated tasks", "contrast", 0.6, True),
            ],
            persistence=0.7,
        ),
    ]

    result = engine.build_context(
        current_message="Before choosing the next action, check whether this blocker has returned before.",
        current_labels=["blocker", "return", "task planning"],
        current_relations=[
            EngineRelation("blocker", "return", "association", 0.8, False),
            EngineRelation("task planning", "blocker", "dependency", 0.8, True),
        ],
        memories=memories,
    )

    print("Agent memory demo")
    print("=================")
    print("An agent should not only retrieve similar tasks. It should notice returning blockers.")
    print()
    print(result.context_pack.to_prompt_text())
    json_path, text_path = write_demo_outputs("agent_memory_demo", result, PROJECT_ROOT)
    print()
    print(f"Saved JSON: {json_path}")
    print(f"Saved text: {text_path}")


if __name__ == "__main__":
    main()
