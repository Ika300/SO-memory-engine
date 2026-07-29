from __future__ import annotations

from .models import EngineMemory, EngineRelation, MemoryEngineInput

RELATION_TYPES = frozenset({"support", "cause", "contrast", "tension", "bridge", "association", "dependency"})


class MemoryEngineValidationError(ValueError):
    """Raised when Engine input is unsafe or incomplete."""


def _require_non_empty_string(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MemoryEngineValidationError(f"{name} must be a non-empty string")
    return value


def _require_unit_score(name: str, value: float) -> float:
    if not isinstance(value, float):
        raise MemoryEngineValidationError(f"{name} must be a float")
    if not 0.0 <= value <= 1.0:
        raise MemoryEngineValidationError(f"{name} must be from 0.0 to 1.0")
    return value


def _require_valence(value: float) -> float:
    if not isinstance(value, float):
        raise MemoryEngineValidationError("valence must be a float")
    if not -1.0 <= value <= 1.0:
        raise MemoryEngineValidationError("valence must be from -1.0 to 1.0")
    return value


def validate_relation(relation: EngineRelation, *, allowed_labels: set[str], owner: str) -> None:
    _require_non_empty_string(f"{owner}.relation.source", relation.source)
    _require_non_empty_string(f"{owner}.relation.target", relation.target)
    if relation.relation_type not in RELATION_TYPES:
        raise MemoryEngineValidationError(
            f"{owner}.relation_type has unsupported value: {relation.relation_type}"
        )
    _require_unit_score(f"{owner}.relation.strength", relation.strength)
    if not isinstance(relation.directed, bool):
        raise MemoryEngineValidationError(f"{owner}.relation.directed must be a bool")
    if relation.source not in allowed_labels:
        raise MemoryEngineValidationError(
            f"{owner}.relation.source must reference an existing label: {relation.source}"
        )
    if relation.target not in allowed_labels:
        raise MemoryEngineValidationError(
            f"{owner}.relation.target must reference an existing label: {relation.target}"
        )


def validate_memory(memory: EngineMemory) -> None:
    _require_non_empty_string("memory.id", memory.id)
    _require_non_empty_string("memory.content", memory.content)
    _require_non_empty_string("memory.space_id", memory.space_id)
    for score_name in [
        "importance",
        "persistence",
        "arousal",
        "certainty",
        "novelty",
        "abstraction",
        "bridge_potential",
        "tension_score",
        "gap_score",
    ]:
        _require_unit_score(f"memory.{score_name}", getattr(memory, score_name))
    _require_valence(memory.valence)

    labels = [_require_non_empty_string("memory.label", label).strip() for label in memory.labels]
    if len(set(labels)) != len(labels):
        raise MemoryEngineValidationError(f"memory.labels must be unique for memory id: {memory.id}")
    if memory.relations and not labels:
        raise MemoryEngineValidationError(
            f"memory.relations require labels for memory id: {memory.id}"
        )
    allowed_labels = set(labels)
    for relation in memory.relations:
        validate_relation(relation, allowed_labels=allowed_labels, owner=f"memory[{memory.id}]")


def validate_engine_input(engine_input: MemoryEngineInput) -> None:
    _require_non_empty_string("current_message", engine_input.current_message)
    _require_non_empty_string("current_id", engine_input.current_id)
    _require_non_empty_string("space_id", engine_input.space_id)

    seen_ids: set[str] = {engine_input.current_id}
    for memory in engine_input.memories:
        validate_memory(memory)
        if memory.id in seen_ids:
            raise MemoryEngineValidationError(f"memory id conflicts with another id: {memory.id}")
        seen_ids.add(memory.id)

    current_labels = [
        _require_non_empty_string("current_label", label).strip()
        for label in engine_input.current_labels
    ]
    if len(set(current_labels)) != len(current_labels):
        raise MemoryEngineValidationError("current_labels must be unique")
    if engine_input.current_relations and not current_labels:
        raise MemoryEngineValidationError("current_relations require current_labels")
    allowed_current_labels = set(current_labels)
    for relation in engine_input.current_relations:
        validate_relation(relation, allowed_labels=allowed_current_labels, owner="current")
