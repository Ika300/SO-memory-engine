# SO Memory Engine

**Structural memory context for AI applications.**

Vector memory retrieves what is similar.  
SO Memory Engine observes what returns.

SO Memory Engine is an application-facing memory layer built above [SO Memory Kernel](https://github.com/Ika300/so-memory-kernel). It prepares compact, traceable memory context for an AI app without using embeddings, semantic dictionaries, fuzzy merging, or LLM calls.

This repository is currently a local development prototype.

## What problem does it solve?

Most AI memory systems begin with similarity search:

> Which old text is closest to the current message?

SO Memory Engine asks a different question:

> What structure is returning?  
> Which relation keeps appearing?  
> Is this evidence independent, or the same evidence encountered repeatedly?  
> What unresolved tension or connection should be available as context?

The result is not a generated answer. It is a **Context Pack** that an AI application can use as optional grounding.

## What it is

SO Memory Engine is:

- a memory-context preparation layer
- a bridge between application memory and SO Memory Kernel
- a way to expose recurrence, return, tension, connection, and evidence history
- a tool for giving an LLM structured memory without letting the LLM invent that memory

## What it is not

SO Memory Engine is not:

- an LLM
- a chatbot
- a vector database
- a semantic search engine
- a natural-language parser
- a hidden ontology or concept dictionary
- a fuzzy merge system
- a storage layer

The caller supplies structure. The Engine preserves and organizes it.

## Architecture

```text
Application / Agent / Chat App
        ↓
caller-supplied MemoryFragments
        ↓
SO Memory Engine
        ↓
SO Memory Kernel
        ↓
Context Pack
        ↓
LLM or application logic
```

Boundary rule:

```text
Kernel observes structure.
Engine prepares context.
LLM generates language.
Application owns storage and UX.
```

## Quickstart

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
            source_id="note_001",
        ),
    ],
)

print(result.context_pack.to_prompt_text())
```

See [docs/QUICKSTART.md](docs/QUICKSTART.md) for a fuller walkthrough.

## What the Engine returns

A `MemoryEngineResult` contains:

- `context_pack` — LLM-facing memory context
- `active_memories` — prior fragments structurally activated by the current input
- `returning_memories` — past structures reactivated by current structure
- `recurring_structures` — repeated structural identities
- `unresolved_tensions` — tension candidates, not conclusions
- `structural_connections` — bridge/chain/star connection candidates
- `evidence_summary` — independent source evidence and contextual recurrence evidence
- `kernel_result` — raw Kernel result for traceability

Use `result.to_dict()` for JSON-safe output.

## Evidence identity

The Engine preserves two different evidence views:

- **Independent source evidence**: who supplied the structure?
- **Contextual recurrence evidence**: how many overlay contexts exposed it?

This distinction matters because the same structure seen many times is not the same as many independent sources saying the same thing. Both are useful, but they should remain distinguishable.

## Demos

```bash
py -3 examples\llm_memory_engine_demo.py
py -3 examples\chat_memory_loop_demo.py
py -3 examples\agent_memory_demo.py
py -3 examples\note_memory_demo.py
py -3 examples\run_evaluation_cases.py
```

Demo outputs are saved under `outputs/` as JSON and text files.

## Benchmarks

```bash
py -3 benchmarks\run_benchmarks.py
```

Engine benchmarks are behavioral benchmarks. They test memory properties such as Return, evidence identity, noise separation, and direction preservation.

## Documentation

- [Quickstart](docs/QUICKSTART.md)
- [Engine API](docs/ENGINE_API.md)
- [Integration Guide](docs/INTEGRATION_GUIDE.md)
- [Benchmarks](docs/BENCHMARKS.md)
- [AI App Demos](docs/AI_APP_DEMOS.md)
- [Evaluation Cases](docs/EVALUATION_CASES.md)
- [Kernel / Engine Boundary](docs/KERNEL_ENGINE_BOUNDARY.md)
- [Public / Private Boundary](docs/PUBLIC_PRIVATE_BOUNDARY.md)
- [Public Release Checklist](docs/PUBLIC_RELEASE_CHECKLIST.md)
- [Release Strategy](docs/RELEASE_STRATEGY.md)
- [GitHub Publication Steps](docs/GITHUB_PUBLICATION_STEPS.md)
- [Engine Design](docs/ENGINE_DESIGN.md)

## Tests

```bash
py -3 -m unittest discover -s tests -p '*test*.py' -v
```

## Current status

Local development prototype. The core API, validation, examples, evaluation cases, benchmarks, and serialization are in place. Public release packaging is not finalized yet.
