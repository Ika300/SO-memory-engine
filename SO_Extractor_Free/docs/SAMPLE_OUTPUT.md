# Sample Output

SO Extractor Free is meant to make the first trial obvious.

The basic flow is:

```text
conversation log
    -> normalized messages
    -> MemoryUnit candidates
    -> validation report
    -> EngineMemory-compatible JSON
    -> optional SO Memory Engine Context Pack
```

Generated files are written under `sample_outputs/` and are intentionally ignored by Git.

## Basic conversation demo

Run:

```bash
py -3 examples\conversation_log_demo.py
```

Expected shape:

```text
SO Extractor conversation log demo
==================================
messages loaded: 4
memory units: 3
valid units: 3/3
issues: 0
```

The useful generated files are:

- `sample_outputs/memory_units.json`
- `sample_outputs/engine_memories.json`
- `sample_outputs/validation_report.md`

## ChatGPT export-like demo

Run:

```bash
py -3 examples\chatgpt_export_like_demo.py
```

Expected shape:

```text
SO Extractor ChatGPT export-like demo
=====================================
messages loaded: 4
memory units: 3
valid units: 3/3
issues: 0
```

The useful generated files are:

- `sample_outputs/chatgpt_export_like/normalized_messages.json`
- `sample_outputs/chatgpt_export_like/memory_units.json`
- `sample_outputs/chatgpt_export_like/engine_memories.json`
- `sample_outputs/chatgpt_export_like/validation_report.md`

## End-to-end Engine demo

Run after installing SO Memory Kernel and SO Memory Engine locally:

```bash
py -3 examples\end_to_end_engine_demo.py
```

Expected shape:

```text
SO Extractor end-to-end Engine demo
===================================
memory units: 3
active memories: 1
returning memories: 1
recurring structures: 0
```

The exact Context Pack text may evolve with SO Memory Engine, but the demo should show that extracted MemoryUnits can reach the Engine and produce active or returning memory context.

## Honest boundary

This sample output proves the path works.

It does not prove high-accuracy natural-language extraction, production readiness, or semantic correctness.

SO Extractor Free preserves supplied and extracted structure. It does not correct bad extraction automatically.