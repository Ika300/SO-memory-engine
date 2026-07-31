from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import MemoryUnit


def memory_unit_to_engine_memory_dict(unit: MemoryUnit) -> dict[str, Any]:
    return {
        "id": unit.id,
        "content": unit.content,
        "labels": list(unit.labels),
        "relations": [
            {
                "source": relation.source,
                "target": relation.target,
                "relation_type": relation.relation_type,
                "strength": relation.strength,
                "directed": relation.directed,
            }
            for relation in unit.relations
        ],
        "source_id": unit.source_id,
        "space_id": unit.conversation_id,
        "importance": unit.importance,
        "persistence": unit.persistence,
        "valence": unit.valence,
        "arousal": unit.arousal,
        "certainty": unit.certainty,
        "novelty": unit.novelty,
        "abstraction": unit.abstraction,
        "bridge_potential": unit.bridge_potential,
        "tension_score": unit.tension_score,
        "gap_score": unit.gap_score,
        "created_at": unit.created_at,
        "metadata": {
            **unit.metadata,
            "message_ids": list(unit.message_ids),
            "extraction_method": unit.extraction_method,
            "confidence": unit.confidence,
        },
    }


def export_engine_memories(units: list[MemoryUnit], path: str | Path) -> list[dict[str, Any]]:
    data = [memory_unit_to_engine_memory_dict(unit) for unit in units]
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data