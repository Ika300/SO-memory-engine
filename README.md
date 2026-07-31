# SO Memory Engine

[![tests](https://github.com/Ika300/SO-memory-engine/actions/workflows/tests.yml/badge.svg)](https://github.com/Ika300/SO-memory-engine/actions/workflows/tests.yml)

**A structural context construction layer for AI memory.**

Vector memory retrieves what is similar.  
SO Memory Engine observes what returns.

SO Memory Engine builds compact Context Packs from caller-supplied structured memory fragments. It does not call an LLM, use embeddings, use semantic dictionaries, or perform fuzzy semantic merging.

This repository is currently an alpha prototype.

## 30-second idea

Repetition is not corroboration.

```text
Memory situation:
The same claim appears 5 times,
but all 5 appearances came from one source.

Naive interpretation:
5 supporting pieces of evidence

SO Memory Engine context:
1 independent source
5 contextual recurrences
```

Both facts matter. They should not be collapsed into one number.

## Installation

Alpha local installation uses editable installs for both Kernel and Engine.

```bash
py -3 -m pip install -e ..\SO_Memory_Kernel
py -3 -m pip install -e .
```

See [Installation](docs/INSTALLATION.md).

## Try it in one command

From this repository:

```bash
py -3 examples\quickstart_demo.py
```

On non-Windows systems, use:

```bash
python examples/quickstart_demo.py
```

You should see output like:

```text
SO Memory Engine quickstart
===========================

Active memories selected for context:
  - note_001: memory / structure / similarity
  - note_002: structure / meaning / flattening

Returning structures:
  - Tension:flattening
  - Bridge:memory<->structure
  - Tension:memory

Recurring structures:
  - Bridge: memory / structure (occurrences=5)

Evidence identity:
  - independent fragment count: 3
  - unique source count: 2
  - contextual recurrence count: 5
```

The point is stable: the Engine returns structural memory context, not a generated answer.

## What problem does it solve?

Most AI memory systems begin with similarity search:

> Which old text is closest to the current message?

SO Memory Engine asks different questions:

> What structure is returning?  
> Which relation keeps appearing?  
> Is this evidence independent, or the same evidence encountered repeatedly?  
> What unresolved tension or connection should be available as context?

The result is not a final assistant response. It is a Context Pack that an AI application can pass to an LLM as optional grounding.

## What it is

SO Memory Engine is:

- a structural context construction layer for AI memory
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

## Where does structure come from?

SO Memory Engine is agnostic about how structure is produced.

Structured memory may come from:

- application events and metadata
- user-defined labels and relations
- rule-based parsers
- LLM structured output
- knowledge graphs
- external extraction systems
- SO-based structural extraction systems

The Engine begins after structure exists.

This boundary is intentional. The public Engine does not claim to understand arbitrary natural language by itself. It accepts structured fragments and reconstructs structural memory context from them.

## Relationship to vector retrieval

SO Memory Engine does not need to be positioned as an enemy of vector search.

```text
Vector retrieval finds candidates.
SO reconstructs structural context.
```

A practical AI system may use vector retrieval to narrow a large memory store, then use SO Memory Engine to separate recurrence, source evidence, unresolved tension, and structural return inside the candidate set.

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
- **Contextual recurrence evidence**: how many contexts exposed it?

This distinction matters because the same structure seen many times is not the same as many independent sources saying the same thing. Both are useful, but they should remain distinguishable.

## What the current tests prove

Current measured status:

```text
Engine tests: 35/35 passed
Behavioral benchmarks: 6/6 passed
Comparative benchmarks: 3/3 passed
External API calls: 0
Embeddings required: No
LLM required: No
```

These tests prove that the alpha Engine preserves its intended structural behaviors on the included test cases and can separate source evidence from contextual recurrence in the included Evidence Identity comparison.

They do not prove that SO Memory Engine improves every AI application, outperforms all retrieval systems, or handles arbitrary natural language extraction by itself.

## Demos

```bash
py -3 examples\quickstart_demo.py
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
py -3 benchmarks\run_comparative_benchmarks.py
```

Engine benchmarks are behavioral benchmarks. They test memory properties such as structural recurrence, evidence identity, structural return, noise rejection, and direction preservation.

Comparative benchmarks currently focus on Evidence Identity using transparent recent-memory and keyword-overlap baselines. They do not use embeddings or LLM calls.

## Documentation

- [Installation](docs/INSTALLATION.md)
- [Quickstart](docs/QUICKSTART.md)
- [Engine API](docs/ENGINE_API.md)
- [Integration Guide](docs/INTEGRATION_GUIDE.md)
- [Benchmarks](docs/BENCHMARKS.md)
- [Benchmark Strategy](docs/BENCHMARK_STRATEGY.md)
- [Comparative Benchmarks](docs/COMPARATIVE_BENCHMARKS.md)
- [Evaluation Principles](docs/EVALUATION_PRINCIPLES.md)
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

Alpha prototype. The core API, validation, examples, evaluation cases, behavioral benchmarks, and serialization are in place. Public release packaging and install flow are not finalized yet.
