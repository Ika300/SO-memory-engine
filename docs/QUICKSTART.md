# Quickstart

This guide shows the smallest useful SO Memory Engine flow.

SO Memory Engine does not parse natural language. Your application gives it the current message, prior memory fragments, and caller-owned structural labels/relations.

## Fastest path

From the repository root:

```bash
py -3 quickstart.py
```

On non-Windows systems:

```bash
python quickstart.py
```

The Engine receives caller-supplied structured memories. The demo uses curated examples so the Engine behavior is visible immediately.

It does not use:

- an extractor;
- an LLM;
- embeddings;
- external APIs.

The quickstart writes:

```text
outputs/engine_quickstart/context_pack.txt
outputs/engine_quickstart/context_pack.json
outputs/engine_quickstart/engine_result.json
```

## 1. Create an Engine

```python
from so_memory_engine import EngineMemory, EngineRelation, MemoryEngine

engine = MemoryEngine()
```

## 2. Prepare prior memories

A memory fragment can contain trace text plus structure supplied by your application.

```python
memories = [
    EngineMemory(
        id="m1",
        content="Earlier note about memory and structure.",
        labels=["memory", "structure"],
        relations=[
            EngineRelation("memory", "structure", "bridge", 0.8, False),
        ],
        bridge_potential=0.8,
        source_id="note_001",
    )
]
```

Important: labels are not inferred by the Engine. If your app supplies labels, they are treated as caller-owned structure.

## 3. Build context for a current message

```python
result = engine.build_context(
    current_message="I keep returning to memory and structure.",
    current_labels=["memory", "structure"],
    current_relations=[
        EngineRelation("memory", "structure", "bridge", 0.8, False),
    ],
    memories=memories,
)
```

## 4. Use the Context Pack

```python
prompt_reference = result.context_pack.to_prompt_text()
json_data = result.to_dict()
```

The Context Pack is reference material. It is not a final response, and it is not a command to an LLM.

## 5. Read the result

Useful fields:

- `active_memories`: memories activated by current structure
- `returning_memories`: past structures that became relevant again
- `recurring_structures`: repeated structural identities
- `unresolved_tensions`: tension candidates
- `structural_connections`: bridge/chain/star connection candidates
- `evidence_summary`: evidence breadth and recurrence

## 6. Validation behavior

Invalid input is rejected before the Kernel runs.

```python
from so_memory_engine import MemoryEngineValidationError
```

Common validation errors include:

- empty current message
- duplicate memory ids
- relation endpoints that do not reference labels
- unsupported relation types
- scores outside `0.0` to `1.0`
- valence outside `-1.0` to `1.0`

## Boundary

The Engine starts after structure exists.

If raw conversations need to become MemoryUnits, that is an extractor problem, not an Engine problem. Keeping this boundary clear prevents weak extraction from being mistaken for weak Engine behavior.