from __future__ import annotations

from dataclasses import dataclass

from so_memory_engine import EngineMemory, EngineRelation, MemoryEngine, MemoryEngineResult


@dataclass(slots=True)
class EvaluationCase:
    name: str
    purpose: str
    current_message: str
    current_labels: list[str]
    current_relations: list[EngineRelation]
    memories: list[EngineMemory]

    def run(self) -> MemoryEngineResult:
        return MemoryEngine().build_context(
            current_message=self.current_message,
            current_labels=self.current_labels,
            current_relations=self.current_relations,
            memories=self.memories,
        )


def same_source_repetition_case() -> EvaluationCase:
    return EvaluationCase(
        name="same_source_repetition",
        purpose="A single source repeats the same structure across memory fragments.",
        current_message="The same memory-structure bridge is back again.",
        current_labels=["memory", "structure"],
        current_relations=[EngineRelation("memory", "structure", "bridge", 0.8, False)],
        memories=[
            EngineMemory(
                id="same_1",
                content="The first note connects memory and structure.",
                labels=["memory", "structure"],
                relations=[EngineRelation("memory", "structure", "bridge", 0.8, False)],
                bridge_potential=0.8,
                source_id="single_source",
            ),
            EngineMemory(
                id="same_2",
                content="The second note repeats memory and structure from the same origin.",
                labels=["memory", "structure"],
                relations=[EngineRelation("memory", "structure", "bridge", 0.8, False)],
                bridge_potential=0.8,
                source_id="single_source",
            ),
        ],
    )


def independent_sources_case() -> EvaluationCase:
    return EvaluationCase(
        name="independent_sources",
        purpose="Different source origins supply the same structural bridge.",
        current_message="Memory and structure are returning from several sources.",
        current_labels=["memory", "structure"],
        current_relations=[EngineRelation("memory", "structure", "bridge", 0.8, False)],
        memories=[
            EngineMemory(
                id="independent_1",
                content="Source A connects memory and structure.",
                labels=["memory", "structure"],
                relations=[EngineRelation("memory", "structure", "bridge", 0.8, False)],
                bridge_potential=0.8,
                source_id="source_a",
            ),
            EngineMemory(
                id="independent_2",
                content="Source B independently connects memory and structure.",
                labels=["memory", "structure"],
                relations=[EngineRelation("memory", "structure", "bridge", 0.8, False)],
                bridge_potential=0.8,
                source_id="source_b",
            ),
        ],
    )


def reactivation_case() -> EvaluationCase:
    return EvaluationCase(
        name="reactivation",
        purpose="The current message reactivates a prior exact structural identity.",
        current_message="The old structure-meaning bridge has returned.",
        current_labels=["structure", "meaning"],
        current_relations=[EngineRelation("structure", "meaning", "bridge", 0.8, False)],
        memories=[
            EngineMemory(
                id="reactivation_past",
                content="A prior memory connected structure and meaning.",
                labels=["structure", "meaning"],
                relations=[EngineRelation("structure", "meaning", "bridge", 0.8, False)],
                bridge_potential=0.8,
            )
        ],
    )


def noise_no_return_case() -> EvaluationCase:
    return EvaluationCase(
        name="noise_no_return",
        purpose="Unrelated labels should not create Return candidates by semantic guessing.",
        current_message="Alpha appears now.",
        current_labels=["alpha"],
        current_relations=[],
        memories=[
            EngineMemory(id="noise_1", content="Beta memory", labels=["beta"]),
            EngineMemory(id="noise_2", content="Gamma memory", labels=["gamma"]),
            EngineMemory(id="noise_3", content="Delta memory", labels=["delta"]),
        ],
    )


def direction_preservation_case() -> EvaluationCase:
    return EvaluationCase(
        name="direction_preservation",
        purpose="Reversed directed relations should not collapse into the same structural identity.",
        current_message="Structure now supports memory in the reverse direction.",
        current_labels=["structure", "memory"],
        current_relations=[EngineRelation("structure", "memory", "support", 0.8, True)],
        memories=[
            EngineMemory(
                id="direction_1",
                content="Past memory supported structure.",
                labels=["memory", "structure"],
                relations=[EngineRelation("memory", "structure", "support", 0.8, True)],
            )
        ],
    )


def all_evaluation_cases() -> list[EvaluationCase]:
    return [
        same_source_repetition_case(),
        independent_sources_case(),
        reactivation_case(),
        noise_no_return_case(),
        direction_preservation_case(),
    ]
