from __future__ import annotations

from .kernel_bridge import ensure_kernel_import_path

ensure_kernel_import_path()

try:
    from so_memory import MemoryFragment, MemoryKernel, MemoryRelation  # noqa: E402
except ModuleNotFoundError as exc:  # pragma: no cover - exercised by installation environment
    if exc.name != "so_memory":
        raise
    raise ModuleNotFoundError(
        "SO Memory Engine requires SO Memory Kernel. "
        "For local development, clone SO_Memory_Kernel next to SO_Memory_Engine and run: "
        "py -3 -m pip install -e ..\\SO_Memory_Kernel"
    ) from exc

from .models import EngineMemory, EngineRelation, MemoryEngineInput


def relation_to_kernel_relation(relation: EngineRelation) -> MemoryRelation:
    return MemoryRelation(
        source=relation.source,
        target=relation.target,
        relation_type=relation.relation_type,
        strength=relation.strength,
        directed=relation.directed,
    )


def engine_memory_to_kernel_fragment(memory: EngineMemory, *, phase: str = "past") -> MemoryFragment:
    metadata = dict(memory.metadata)
    metadata.setdefault("phase", phase)
    return MemoryFragment(
        id=memory.id,
        content=memory.content,
        labels=list(memory.labels),
        relations=[relation_to_kernel_relation(relation) for relation in memory.relations],
        space_id=memory.space_id,
        importance=memory.importance,
        persistence=memory.persistence,
        valence=memory.valence,
        arousal=memory.arousal,
        certainty=memory.certainty,
        novelty=memory.novelty,
        abstraction=memory.abstraction,
        bridge_potential=memory.bridge_potential,
        tension_score=memory.tension_score,
        gap_score=memory.gap_score,
        source_id=memory.source_id,
        created_at=memory.created_at,
        metadata=metadata,
    )


def current_input_to_kernel_fragment(engine_input: MemoryEngineInput) -> MemoryFragment:
    return MemoryFragment(
        id=engine_input.current_id,
        content=engine_input.current_message,
        labels=list(engine_input.current_labels),
        relations=[relation_to_kernel_relation(relation) for relation in engine_input.current_relations],
        space_id=engine_input.space_id,
        importance=0.7,
        persistence=0.7,
        novelty=0.6,
        abstraction=0.6,
        bridge_potential=0.0,
        tension_score=0.0,
        gap_score=0.0,
        metadata={"phase": "current"},
    )


class KernelRunner:
    def __init__(self, kernel: MemoryKernel | None = None) -> None:
        self.kernel = kernel or MemoryKernel()

    def run(self, engine_input: MemoryEngineInput):
        fragments = [engine_memory_to_kernel_fragment(memory, phase="past") for memory in engine_input.memories]
        fragments.append(current_input_to_kernel_fragment(engine_input))
        return self.kernel.run(fragments)
