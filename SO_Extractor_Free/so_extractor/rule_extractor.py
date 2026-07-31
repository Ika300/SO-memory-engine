from __future__ import annotations

import re
from collections import Counter

from .models import ConversationMessage, MemoryRelationUnit, MemoryUnit

WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_'-]*")
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "then", "so", "to", "of", "in", "on", "for", "with",
    "is", "are", "am", "be", "been", "being", "it", "this", "that", "these", "those", "i", "you", "we",
    "they", "he", "she", "my", "your", "our", "their", "me", "us", "them", "do", "does", "did", "not",
    "want", "need", "think", "feel", "keep", "really", "just", "still", "again", "about", "because",
}
TENSION_MARKERS = {"but", "however", "although", "though", "yet", "worry", "worried", "fear", "afraid", "conflict"}
GOAL_MARKERS = {"want", "need", "goal", "plan", "try", "build", "start", "continue"}
CONSTRAINT_MARKERS = {"cannot", "can't", "hard", "difficult", "risk", "constraint", "limited", "worry", "worried"}


def extract_labels(text: str, *, max_labels: int = 6) -> list[str]:
    words = [word.lower().strip("'-") for word in WORD_RE.findall(text)]
    candidates = [word for word in words if len(word) >= 4 and word not in STOPWORDS]
    counts = Counter(candidates)
    labels = [word for word, _ in counts.most_common(max_labels)]
    return labels


def _relation_type(text: str) -> str:
    words = {word.lower().strip("'-") for word in WORD_RE.findall(text)}
    if words & TENSION_MARKERS:
        return "tension"
    if words & CONSTRAINT_MARKERS:
        return "contrast"
    if words & GOAL_MARKERS:
        return "support"
    return "association"


def extract_memory_units(messages: list[ConversationMessage]) -> list[MemoryUnit]:
    units: list[MemoryUnit] = []
    for index, message in enumerate(messages):
        if message.role.lower() == "assistant":
            continue
        text = message.text.strip()
        if not text:
            continue
        labels = extract_labels(text)
        relations: list[MemoryRelationUnit] = []
        relation_type = _relation_type(text)
        if len(labels) >= 2:
            relations.append(
                MemoryRelationUnit(
                    source=labels[0],
                    target=labels[1],
                    relation_type=relation_type,
                    strength=0.7 if relation_type != "association" else 0.5,
                    directed=relation_type in {"support", "contrast"},
                    evidence_message_ids=[message.id],
                )
            )
        tension_score = 0.72 if relation_type == "tension" else 0.0
        bridge_potential = 0.65 if relation_type == "association" and len(labels) >= 2 else 0.0
        units.append(
            MemoryUnit(
                id=f"memory_unit_{index:04d}",
                content=text,
                labels=labels,
                relations=relations,
                source_id=message.source_id or message.id,
                conversation_id=message.conversation_id,
                message_ids=[message.id],
                confidence=0.45,
                importance=0.55,
                persistence=0.55,
                certainty=0.45,
                novelty=0.5,
                abstraction=0.45,
                bridge_potential=bridge_potential,
                tension_score=tension_score,
                metadata={
                    "role": message.role,
                    "extractor_limit": "transparent rule-based demo; not high-accuracy parsing",
                },
            )
        )
    return units