from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import ConversationMessage, utc_now_iso


def _metadata_without(item: dict[str, Any], excluded: set[str]) -> dict[str, Any]:
    return {key: value for key, value in item.items() if key not in excluded}


def load_conversation_json(path: str | Path) -> list[ConversationMessage]:
    """Load a simple conversation JSON file.

    Supported shapes:
    - list of message objects
    - {"messages": [...]}

    Required per message:
    - id or message_id
    - role
    - text or content
    """

    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        conversation_id = str(data.get("conversation_id", data.get("id", "default")))
        raw_messages = data.get("messages", [])
    elif isinstance(data, list):
        conversation_id = "default"
        raw_messages = data
    else:
        raise ValueError("conversation JSON must be a list or an object with messages")

    messages: list[ConversationMessage] = []
    for index, item in enumerate(raw_messages):
        if not isinstance(item, dict):
            raise ValueError(f"message at index {index} must be an object")
        message_id = str(item.get("id", item.get("message_id", f"message_{index:04d}")))
        role = str(item.get("role", "unknown"))
        text = str(item.get("text", item.get("content", "")))
        source_id = item.get("source_id")
        created_at = str(item.get("created_at", item.get("timestamp", ""))) or None
        messages.append(
            ConversationMessage(
                id=message_id,
                role=role,
                text=text,
                conversation_id=str(item.get("conversation_id", conversation_id)),
                source_id=str(source_id) if source_id else message_id,
                created_at=created_at or utc_now_iso(),
                metadata=_metadata_without(
                    item,
                    {"id", "message_id", "role", "text", "content", "source_id", "created_at", "timestamp", "conversation_id"},
                ),
            )
        )
    return messages


def _iso_from_unix(value: Any) -> str | None:
    if value is None:
        return None
    try:
        return datetime.fromtimestamp(float(value), timezone.utc).isoformat()
    except (TypeError, ValueError, OSError):
        return None


def _chatgpt_parts_to_text(parts: Any) -> str:
    if isinstance(parts, str):
        return parts
    if not isinstance(parts, list):
        return ""
    text_parts: list[str] = []
    for part in parts:
        if isinstance(part, str):
            text_parts.append(part)
        elif isinstance(part, dict) and isinstance(part.get("text"), str):
            text_parts.append(part["text"])
    return "\n".join(piece.strip() for piece in text_parts if piece.strip()).strip()


def _load_chatgpt_mapping(conversation: dict[str, Any], *, fallback_conversation_id: str) -> list[ConversationMessage]:
    mapping = conversation.get("mapping")
    if not isinstance(mapping, dict):
        return []

    conversation_id = str(conversation.get("id", fallback_conversation_id))
    source_id = str(conversation.get("source_id", conversation_id))
    rows: list[tuple[float, str, ConversationMessage]] = []

    for node_id, node in mapping.items():
        if not isinstance(node, dict):
            continue
        message = node.get("message")
        if not isinstance(message, dict):
            continue
        author = message.get("author", {})
        role = str(author.get("role", "unknown")) if isinstance(author, dict) else "unknown"
        content = message.get("content", {})
        parts = content.get("parts", []) if isinstance(content, dict) else []
        text = _chatgpt_parts_to_text(parts)
        if not text:
            continue
        message_id = str(message.get("id", node_id))
        created_at = _iso_from_unix(message.get("create_time")) or utc_now_iso()
        order = float(message.get("create_time") or 0.0)
        rows.append(
            (
                order,
                message_id,
                ConversationMessage(
                    id=message_id,
                    role=role,
                    text=text,
                    conversation_id=conversation_id,
                    source_id=source_id,
                    created_at=created_at,
                    metadata={
                        "chatgpt_node_id": str(node_id),
                        "loader": "chatgpt_export_like",
                        "title": conversation.get("title"),
                    },
                ),
            )
        )

    rows.sort(key=lambda row: (row[0], row[1]))
    return [row[2] for row in rows]


def load_chatgpt_export_like_json(path: str | Path) -> list[ConversationMessage]:
    """Load a small ChatGPT-export-like JSON file.

    This is intentionally a convenience loader, not a full guarantee for every
    historical ChatGPT export variant. It supports:

    - a single object with a ChatGPT-style mapping
    - {"conversations": [{"mapping": ...}, ...]}
    - a list of conversation objects with mappings
    - simple {"messages": [...]} files as a fallback
    """

    data = json.loads(Path(path).read_text(encoding="utf-8"))

    if isinstance(data, dict) and "messages" in data:
        return load_conversation_json(path)

    conversations: list[dict[str, Any]]
    if isinstance(data, dict) and isinstance(data.get("conversations"), list):
        conversations = [item for item in data["conversations"] if isinstance(item, dict)]
    elif isinstance(data, dict) and isinstance(data.get("mapping"), dict):
        conversations = [data]
    elif isinstance(data, list):
        conversations = [item for item in data if isinstance(item, dict) and isinstance(item.get("mapping"), dict)]
    else:
        raise ValueError("ChatGPT export-like JSON must contain mapping data or messages")

    messages: list[ConversationMessage] = []
    for index, conversation in enumerate(conversations):
        messages.extend(_load_chatgpt_mapping(conversation, fallback_conversation_id=f"chatgpt_like_{index:04d}"))
    return messages