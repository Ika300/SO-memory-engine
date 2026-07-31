# SO Memory Engine

[![tests](https://github.com/Ika300/SO-memory-engine/actions/workflows/tests.yml/badge.svg)](https://github.com/Ika300/SO-memory-engine/actions/workflows/tests.yml)

**Structural memory context for AI agents and applications.**

```text
curated MemoryUnits
    -> SO Memory Engine
    -> Context Pack
    -> your own LLM / agent / application
```

SO Memory Engine does not parse natural language, include an LLM, call external APIs, or use embeddings. It starts after structure exists.

Vector memory retrieves what is similar.  
SO Memory Engine observes what returns.

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

## Quickstart

First-time local setup requires SO Memory Kernel next to this repository.

Recommended layout:

```text
Desktop/
  SO_Memory_Kernel/
  SO_Memory_Engine/
```

Install locally:

```bash
py -3 -m pip install -e ..\SO_Memory_Kernel
py -3 -m pip install -e .
```

Then run the Engine-only demo:

```bash
py -3 quickstart.py
```

Or on non-Windows systems:

```bash
python quickstart.py
```

The quickstart uses curated MemoryUnits so the Engine behavior is visible immediately. It writes outputs to:

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

## Input boundary

The Engine expects structured memory. Your application owns extraction.

A production system may create MemoryUnits from forms, logs, human review, rules, another parser, or a future paid extractor. This repository intentionally keeps that boundary clear so Engine behavior is not confused with extraction quality.

## Current free/demo boundary

The free public repository demonstrates the Engine itself using curated MemoryUnits.

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

During alpha development, install Kernel locally from the sibling repository:

```bash
py -3 -m pip install -e ..\SO_Memory_Kernel
```

See [Installation](docs/INSTALLATION.md) for details.

## License

See [LICENSE](LICENSE).