# SO Memory Engine

[![tests](https://github.com/Ika300/SO-memory-engine/actions/workflows/tests.yml/badge.svg)](https://github.com/Ika300/SO-memory-engine/actions/workflows/tests.yml)

**Structural memory context for AI agents and applications.**

```text
caller-supplied structured memories
    -> SO Memory Engine
    -> Context Pack
    -> your own LLM / agent / application
```

SO Memory Engine does not parse natural language, include an LLM, call external APIs, or use embeddings. It starts after structure exists.

Vector memory retrieves what is similar.  
SO Memory Engine observes what returns.

This repository is currently an alpha prototype.

## What goes in, what comes out

Simplified input:

```json
{
  "id": "m1",
  "content": "I keep returning to memory and structure.",
  "labels": ["memory", "structure"],
  "source_id": "note_001"
}
```

Simplified Context Pack output:

```json
{
  "returning_memories": ["memory / structure returned"],
  "recurring_structures": ["Bridge: memory <-> structure"],
  "unresolved_tensions": ["memory / similarity"],
  "evidence_summary": {
    "trace_fragment_count": 3,
    "unique_source_count": 2,
    "contextual_recurrence_count": 5
  }
}
```

The demo uses curated examples, but the Engine accepts any caller-supplied structured memories.

## Why Context Packs matter

A normal memory system may retrieve similar text. SO Memory Engine is meant to surface structural context.

Example:

```text
Past memory A: the user wants independence.
Past memory B: the user worries about stable income.
Current message: the user is considering leaving a job.
```

The useful context is not just "job" or "income" similarity. The useful context may be:

```text
returning structure: independence
unresolved tension: independence <-> income stability
```

That is the kind of structural context an external LLM or agent can use without SO itself becoming the LLM.

## 30-second idea

Repetition is not corroboration.

```text
Memory situation:
The same claim appears 5 times,
but all 5 appearances came from one source.

Naive interpretation:
5 supporting pieces of evidence

SO Memory Engine context:
1 unique source
5 contextual recurrences
```

Both facts matter. They should not be collapsed into one number.

## Quickstart

Clone this repository:

```bash
git clone https://github.com/Ika300/SO-memory-engine.git
cd SO-memory-engine
```

Install locally:

```bash
py -3 -m pip install -e .
```

Then run the Engine-only demo:

```bash
py -3 quickstart.py
```

On non-Windows systems:

```bash
python -m pip install -e .
python quickstart.py
```

`pip install -e .` installs SO Memory Kernel from its GitHub repository.

If that fails, see [Installation](docs/INSTALLATION.md) for the manual sibling-repository setup.

The quickstart writes outputs to:

```text
outputs/engine_quickstart/context_pack.txt
outputs/engine_quickstart/context_pack.json
outputs/engine_quickstart/engine_result.json
```

See:

- [Quickstart](docs/QUICKSTART.md)
- [Installation](docs/INSTALLATION.md)
- [Engine API](docs/ENGINE_API.md)
- [Integration Guide](docs/INTEGRATION_GUIDE.md)
- [Benchmarks](docs/BENCHMARKS.md)

## What this repository is

SO Memory Engine is a structural context construction layer.

It receives caller-supplied `EngineMemory` objects or equivalent structured memory data and builds a compact Context Pack containing:

- active memories;
- returning structures;
- recurring structures;
- unresolved tensions;
- structural connections;
- evidence identity summary.

The Context Pack is reference material for downstream systems. It is not a final response and not a command to an LLM.

## What this repository is not

It does not perform extraction, storage, semantic search, or response generation.

The Engine treats supplied structure as caller-owned input and does not reinterpret it automatically.

## Minimal Python example

```python
from so_memory_engine import EngineMemory, EngineRelation, MemoryEngine

memories = [
    EngineMemory(
        id="m1",
        content="Earlier note about memory and structure.",
        labels=["memory", "structure"],
        relations=[
            EngineRelation("memory", "structure", "bridge", 0.8, False),
        ],
        source_id="note_001",
    )
]

result = MemoryEngine().build_context(
    current_message="I keep returning to memory and structure.",
    current_labels=["memory", "structure"],
    current_relations=[
        EngineRelation("memory", "structure", "bridge", 0.8, False),
    ],
    memories=memories,
)

print(result.context_pack.to_prompt_text())
```

## Repository scope

The Engine expects `EngineMemory` objects or equivalent structured memory data. A MemoryUnit is represented in this API as an `EngineMemory` object.

A production system may create structured memories from forms, logs, human review, rules, another parser, or another extraction layer.

`current_message` is preserved as trace text. The Engine does not infer structure from it.

## Benchmarks

Run:

```bash
py -3 benchmarks\run_benchmarks.py
py -3 benchmarks\run_comparative_benchmarks.py
```

The benchmarks focus on structural-memory behavior rather than vector-search speed:

- structure recurrence;
- evidence independence;
- conflict/tension visibility;
- noise behavior;
- context construction.

## Kernel dependency

SO Memory Engine depends on SO Memory Kernel.

The default install path now pulls Kernel directly from GitHub:

```bash
py -3 -m pip install -e .
```

For local Kernel development, see [Installation](docs/INSTALLATION.md).

## License

See [LICENSE](LICENSE).