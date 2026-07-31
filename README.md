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

Input is structured memory supplied by your application:

```json
{
  "content": "I keep returning to memory and structure.",
  "labels": ["memory", "structure"],
  "source_id": "note_001"
}
```

Output is a Context Pack:

```json
{
  "returning_memories": ["memory / structure returned"],
  "recurring_structures": ["Bridge: memory <-> structure"],
  "unresolved_tensions": ["memory / similarity"],
  "evidence_summary": {
    "unique_source_count": 2,
    "contextual_recurrence_count": 5
  }
}
```

The demo uses curated examples, but the product boundary is broader: any caller can provide structured memories from forms, logs, human review, rules, or another extraction layer.

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

It receives caller-supplied structured memory fragments and builds a compact Context Pack containing:

- active memories;
- returning structures;
- recurring structures;
- unresolved tensions;
- structural connections;
- evidence identity summary.

The Context Pack is reference material for downstream systems. It is not a final response and not a command to an LLM.

## What this repository is not

SO Memory Engine is not:

- an LLM;
- a chatbot;
- a natural-language parser;
- an embedding model;
- a vector database;
- a summarizer;
- a hidden ontology;
- a semantic-merge layer.

The Engine preserves supplied structure. It does not correct bad extraction automatically.

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
        bridge_potential=0.8,
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

## Evidence count names

Current alpha names expose two levels of evidence breadth:

| Field | Meaning |
| --- | --- |
| `independent_source_count` | Kernel trace fragment breadth. |
| `unique_source_count` | Caller-level unique `source_id` breadth. |
| `contextual_recurrence_count` | Repeated overlay/context exposure. |

The names may become clearer in a future version, but they are kept stable for this alpha API.

## Input boundary

The Engine expects structured memory. Your application owns extraction.

A production system may create MemoryUnits from forms, logs, human review, rules, another parser, or a future paid extractor. This repository intentionally keeps that boundary clear so Engine behavior is not confused with extraction quality.

## Current free/demo boundary

The free public repository demonstrates the Engine itself using caller-supplied structured memories.

It does not claim production extraction from arbitrary raw conversations. That problem belongs to a separate extractor layer.

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