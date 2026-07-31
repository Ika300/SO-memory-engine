from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class ConversationMessage:
    id: str
    role: str
    text: str
    conversation_id: str = "default"
    source_id: str | None = None
    created_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class MemoryRelationUnit:
    source: str
    target: str
    relation_type: str = "association"
    strength: float = 0.5
    directed: bool = True
    evidence_message_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class MemoryUnit:
    id: str
    content: str
    labels: list[str]
    relations: list[MemoryRelationUnit] = field(default_factory=list)
    source_id: str | None = None
    conversation_id: str = "default"
    message_ids: list[str] = field(default_factory=list)
    extraction_method: str = "rule_based_free"
    confidence: float = 0.5
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
    created_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["relations"] = [relation.to_dict() for relation in self.relations]
        return data