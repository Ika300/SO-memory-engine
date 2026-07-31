# Engine API

SO Memory Engine is the AI-app-facing layer above SO Memory Kernel.

It prepares structural memory context for an application or LLM without parsing natural language, calling an LLM, or using semantic dictionaries.

## Basic use

```python
from so_memory_engine import EngineMemory, EngineRelation, MemoryEngine

engine = MemoryEngine()

result = engine.build_context(
    current_message="I keep returning to memory and structure.",
    current_labels=["memory", "structure"],
    current_relations=[
        EngineRelation("memory", "structure", "bridge", 0.8, False),
    ],
    memories=[
        EngineMemory(
            id="m1",
            content="Earlier note about memory and structure.",
            labels=["memory", "structure"],
            relations=[
                EngineRelation("memory", "structure", "bridge", 0.8, False),
            ],
            bridge_potential=0.8,
        ),
    ],
)

print(result.context_pack.to_prompt_text())
print(result.to_dict())
```

## Input objects

### EngineMemory

Application-facing memory item.

Required fields:

- `id`
- `content`

Common optional fields:

- `labels`
- `relations`
- `source_id`
- `space_id`
- score fields such as `importance`, `persistence`, `novelty`, `tension_score`
- `metadata`

The Engine does not infer labels. If labels are supplied, they are caller-owned structure. If labels are omitted, the underlying Kernel preserves content as a single anchor.

If relations are supplied, labels must also be supplied and relation endpoints must reference existing labels.

### EngineRelation

Caller-supplied relation between labels.

Fields:

- `source`
- `target`
- `relation_type`
- `strength`
- `directed`

Allowed relation types:

- `support`
- `cause`
- `contrast`
- `tension`
- `bridge`
- `association`
- `dependency`

### MemoryEngineInput

Optional wrapper for full input.

Fields:

- `current_message`
- `memories`
- `current_labels`
- `current_relations`
- `current_id`
- `space_id`

`current_id` must not conflict with any memory id.

If `current_relations` are supplied, `current_labels` must also be supplied and relation endpoints must reference existing current labels.

## Validation

The Engine validates input before calling SO Memory Kernel.

It rejects:

- empty current message
- duplicate memory ids
- `current_id` conflicts
- empty ids or labels
- relation endpoints that do not reference labels
- relations without labels
- unsupported relation types
- scores outside their allowed ranges
- non-float score values
- valence outside `-1.0` to `1.0`

Validation raises:

```python
from so_memory_engine import MemoryEngineValidationError
```

## Output objects

### MemoryEngineResult

Top-level Engine result.

Fields:

- `context_pack`
- `active_memories`
- `returning_memories`
- `recurring_structures`
- `unresolved_tensions`
- `structural_connections`
- `evidence_summary`
- `kernel_result`

Use `result.to_dict()` for JSON-safe output.

### EvidenceSummary

`evidence_summary` includes both fragment-level and source-id-level evidence views:

| Field | Meaning |
| --- | --- |
| `independent_source_count` | Kernel trace fragment breadth. |
| `unique_source_count` | Engine-level unique `source_id` breadth. |
| `unique_source_ids` | Source ids used for Engine-level breadth. |
| `contextual_recurrence_count` | Repeated overlay/context exposure. |

The current alpha name `independent_source_count` is kept for API stability. Read it as Kernel trace fragment breadth, not caller-level source-id breadth.

This matters because the Engine must distinguish:

- the same source seen many times
- multiple independent sources

### ContextPack

LLM-facing structural memory context.

Use:

```python
result.context_pack.to_prompt_text()
result.context_pack.to_dict()
```

The prompt text is optional reference material for an LLM. It is not the final response and not a command.

## Output persistence

Demos use `examples/demo_utils.py` to save:

- JSON result under `outputs/*.json`
- prompt text under `outputs/*.txt`

This is only demo support. The Engine itself does not own storage.

## Boundary

The Engine must not:

- modify Spiral Orbit Core
- change SO formulas, thresholds, Pattern types, or pipeline structure
- infer natural-language meaning by hidden dictionary
- perform approximate semantic merging
- call an LLM
- invent user history

Kernel observes structure.
Engine prepares context.
LLM generates language.
Application owns storage and UX.
