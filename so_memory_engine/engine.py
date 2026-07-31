from __future__ import annotations

from .adapter import KernelRunner
from .context_pack import build_context_pack
from .models import MemoryEngineInput, MemoryEngineResult
from .validation import validate_engine_input


class MemoryEngine:
    """AI-app-facing structural memory engine.

    The Engine wraps SO Memory Kernel output into a compact Context Pack. It does
    not parse natural language, call an LLM, or alter Spiral Orbit Core behavior.
    """

    def __init__(self, runner: KernelRunner | None = None) -> None:
        self.runner = runner or KernelRunner()

    def build_context(
        self,
        engine_input: MemoryEngineInput | None = None,
        *,
        current_message: str | None = None,
        memories=None,
        current_labels: list[str] | None = None,
        current_relations: list | None = None,
        current_id: str = "current",
        space_id: str = "default",
    ) -> MemoryEngineResult:
        if engine_input is None:
            if current_message is None:
                raise ValueError("current_message is required when engine_input is not supplied")
            engine_input = MemoryEngineInput(
                current_message=current_message,
                memories=list(memories or []),
                current_labels=list(current_labels or []),
                current_relations=list(current_relations or []),
                current_id=current_id,
                space_id=space_id,
            )
        validate_engine_input(engine_input)
        kernel_result = self.runner.run(engine_input)
        context_pack = build_context_pack(
            engine_input.current_message,
            engine_input.memories,
            kernel_result,
        )
        return MemoryEngineResult(
            context_pack=context_pack,
            active_memories=context_pack.active_memories,
            returning_memories=context_pack.returning_memories,
            recurring_structures=context_pack.recurring_structures,
            unresolved_tensions=context_pack.unresolved_tensions,
            structural_connections=context_pack.structural_connections,
            evidence_summary=context_pack.evidence_summary,
            kernel_result=kernel_result,
        )
