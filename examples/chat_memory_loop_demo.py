from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from demo_utils import write_demo_outputs
from so_memory_engine import EngineMemory, EngineRelation, MemoryEngine


def render_assistant_context(question: str, context_text: str) -> str:
    return (
        "A chat app would answer the latest message first, then use this "
        "structural memory context only when it helps.\n\n"
        f"Latest user message: {question}\n\n"
        "Memory context available to the LLM:\n"
        f"{context_text}"
    )


def main() -> None:
    engine = MemoryEngine()
    memories = [
        EngineMemory(
            id="chat_001",
            content="User said memory should preserve difference instead of flattening everything into similarity.",
            labels=["memory", "difference", "similarity"],
            relations=[
                EngineRelation("memory", "difference", "support", 0.8, True),
                EngineRelation("difference", "similarity", "tension", 0.8, False),
            ],
            importance=0.8,
            persistence=0.8,
            tension_score=0.8,
        ),
        EngineMemory(
            id="chat_002",
            content="User returned to the idea that structure should guide AI memory without becoming a summarizer.",
            labels=["structure", "memory", "summary"],
            relations=[
                EngineRelation("structure", "memory", "bridge", 0.8, False),
                EngineRelation("memory", "summary", "contrast", 0.7, True),
            ],
            bridge_potential=0.8,
            importance=0.7,
            persistence=0.8,
        ),
    ]

    latest_message = "I still think memory and similarity should not be treated as the same thing."
    result = engine.build_context(
        current_message=latest_message,
        current_labels=["memory", "similarity", "difference"],
        current_relations=[
            EngineRelation("memory", "similarity", "tension", 0.8, False),
            EngineRelation("memory", "difference", "support", 0.8, True),
        ],
        memories=memories,
    )

    print("Chat memory loop demo")
    print("=====================")
    print(render_assistant_context(latest_message, result.context_pack.to_prompt_text()))
    json_path, text_path = write_demo_outputs("chat_memory_loop_demo", result, PROJECT_ROOT)
    print()
    print(f"Saved JSON: {json_path}")
    print(f"Saved text: {text_path}")


if __name__ == "__main__":
    main()
