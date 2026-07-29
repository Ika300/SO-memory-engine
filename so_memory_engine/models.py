from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def _return_candidate_to_dict(candidate: Any) -> dict[str, Any]:
    return {
        "label": candidate.label,
        "return_score": candidate.return_score,
        "current_fragment_ids": list(candidate.current_fragment_ids),
        "past_fragment_ids": list(candidate.past_fragment_ids),
        "shared_pattern_identity_keys": list(candidate.shared_pattern_identity_keys),
        "shared_nodes": list(candidate.shared_nodes),
        "connection_reason": candidate.connection_reason,
        "caution": candidate.caution,
    }


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class EngineRelation:
    """Caller-supplied structural relation for Engine input.

    The Engine does not infer relations from language.
    """

    source: str
    target: str
    relation_type: str = "association"
    strength: float = 0.5
    directed: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class EngineMemory:
    """Application-facing memory item.

    `content` is trace text. `labels` and `relations` are caller-supplied
    structure. If labels are omitted, the underlying Kernel preserves content as
    a single structural anchor.
    """

    id: str
    content: str
    labels: list[str] = field(default_factory=list)
    relations: list[EngineRelation] = field(default_factory=list)
    source_id: str | None = None
    space_id: str = "default"
    importance: float = 0.5
    persistence: float = 0.5
    valence: float = 0.0
    arousal: float = 0.5
    certainty: float = 0.5
    novelty: float = 0.5
    abstraction: float = 0.5
    bridge_potential: float = 0.0
    tension_score: float = 0.0
    gap_score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["relations"] = [relation.to_dict() for relation in self.relations]
        return data


@dataclass(slots=True)
class MemoryEngineInput:
    current_message: str
    memories: list[EngineMemory]
    current_labels: list[str] = field(default_factory=list)
    current_relations: list[EngineRelation] = field(default_factory=list)
    current_id: str = "current"
    space_id: str = "default"

    def to_dict(self) -> dict[str, Any]:
        return {
            "current_message": self.current_message,
            "memories": [memory.to_dict() for memory in self.memories],
            "current_labels": list(self.current_labels),
            "current_relations": [relation.to_dict() for relation in self.current_relations],
            "current_id": self.current_id,
            "space_id": self.space_id,
        }


@dataclass(slots=True)
class ActiveMemory:
    fragment_id: str
    content: str
    labels: list[str]
    activation_reason: str
    pattern_identity_keys: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class RecurringStructure:
    identity_key: str
    pattern_type: str
    center_candidate: str
    member_nodes: list[str]
    occurrence_count: int
    independent_source_count: int
    contextual_recurrence_count: int
    source_fragment_ids: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class UnresolvedTension:
    label: str
    member_nodes: list[str]
    source_fragment_ids: list[str]
    occurrence_count: int
    caution: str = "Tension candidate only; not a conclusion."

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class StructuralConnection:
    label: str
    member_nodes: list[str]
    source_fragment_ids: list[str]
    occurrence_count: int
    caution: str = "Connection candidate only; not a semantic merge."

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class EvidenceSummary:
    independent_source_count: int
    contextual_recurrence_count: int
    independent_source_fragment_ids: list[str]
    contextual_recurrence_overlay_ids: list[str]
    unique_source_ids: list[str] = field(default_factory=list)

    @property
    def unique_source_count(self) -> int:
        return len(self.unique_source_ids)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["unique_source_count"] = self.unique_source_count
        return data


@dataclass(slots=True)
class ContextPack:
    """LLM-facing memory map.

    This is reference material, not a final response and not a command to the
    language model.
    """

    current_message: str
    active_memories: list[ActiveMemory]
    returning_memories: list[Any]
    recurring_structures: list[RecurringStructure]
    unresolved_tensions: list[UnresolvedTension]
    structural_connections: list[StructuralConnection]
    evidence_summary: EvidenceSummary
    caution: str = (
        "Use this as structural memory context only. Do not invent user history, "
        "do not treat candidates as facts, and do not collapse distinct evidence."
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "current_message": self.current_message,
            "active_memories": [memory.to_dict() for memory in self.active_memories],
            "returning_memories": [_return_candidate_to_dict(item) for item in self.returning_memories],
            "recurring_structures": [item.to_dict() for item in self.recurring_structures],
            "unresolved_tensions": [item.to_dict() for item in self.unresolved_tensions],
            "structural_connections": [item.to_dict() for item in self.structural_connections],
            "evidence_summary": self.evidence_summary.to_dict(),
            "caution": self.caution,
        }

    def to_prompt_text(self) -> str:
        lines: list[str] = []
        lines.append("STRUCTURAL MEMORY CONTEXT")
        lines.append("This is optional grounding for an AI response, not the response itself.")
        lines.append("")
        lines.append(f"Current message: {self.current_message}")
        lines.append("")
        lines.append("Evidence summary:")
        lines.append(f"- independent fragment count: {self.evidence_summary.independent_source_count}")
        lines.append(f"- unique source count: {self.evidence_summary.unique_source_count}")
        lines.append(f"- contextual recurrence count: {self.evidence_summary.contextual_recurrence_count}")
        if self.active_memories:
            lines.append("")
            lines.append("Active memories:")
            for memory in self.active_memories:
                label_text = ", ".join(memory.labels) if memory.labels else memory.content
                lines.append(f"- {label_text}: {memory.activation_reason}")
        if self.returning_memories:
            lines.append("")
            lines.append("Returning structures:")
            for item in self.returning_memories:
                lines.append(f"- {item.label}: {item.connection_reason}")
        if self.recurring_structures:
            lines.append("")
            lines.append("Recurring structures:")
            for item in self.recurring_structures:
                nodes = " / ".join(item.member_nodes)
                lines.append(
                    f"- {item.pattern_type} around {item.center_candidate}: {nodes} "
                    f"(occurrences={item.occurrence_count})"
                )
        if self.unresolved_tensions:
            lines.append("")
            lines.append("Unresolved tensions:")
            for tension in self.unresolved_tensions:
                lines.append(f"- {tension.label}: {' / '.join(tension.member_nodes)}")
        if self.structural_connections:
            lines.append("")
            lines.append("Structural connections:")
            for connection in self.structural_connections:
                lines.append(f"- {connection.label}: {' / '.join(connection.member_nodes)}")
        lines.append("")
        lines.append(f"Caution: {self.caution}")
        return "\n".join(lines)


@dataclass(slots=True)
class MemoryEngineResult:
    context_pack: ContextPack
    active_memories: list[ActiveMemory]
    returning_memories: list[Any]
    recurring_structures: list[RecurringStructure]
    unresolved_tensions: list[UnresolvedTension]
    structural_connections: list[StructuralConnection]
    evidence_summary: EvidenceSummary
    kernel_result: Any

    def to_dict(self) -> dict[str, Any]:
        return {
            "context_pack": self.context_pack.to_dict(),
            "active_memories": [memory.to_dict() for memory in self.active_memories],
            "returning_memories": [_return_candidate_to_dict(item) for item in self.returning_memories],
            "recurring_structures": [item.to_dict() for item in self.recurring_structures],
            "unresolved_tensions": [item.to_dict() for item in self.unresolved_tensions],
            "structural_connections": [item.to_dict() for item in self.structural_connections],
            "evidence_summary": self.evidence_summary.to_dict(),
            "has_insight": self.kernel_result.has_insight,
        }
