# End-to-End Demo

SO Extractor Free exists to answer the first adoption question:

> How do I turn a conversation log into SO Memory Engine input?

The demo path is intentionally small and inspectable.

```text
sample conversation log
    -> SO Extractor Free
    -> MemoryUnit candidates
    -> validation report
    -> EngineMemory-compatible objects
    -> SO Memory Engine
    -> Context Pack
```

## Run

From `SO_Extractor`:

```bash
py -3 examples\conversation_log_demo.py
py -3 examples\chatgpt_export_like_demo.py
py -3 examples\end_to_end_engine_demo.py
```

On non-Windows systems:

```bash
python examples/conversation_log_demo.py
python examples/chatgpt_export_like_demo.py
python examples/end_to_end_engine_demo.py
```

## What the first demo proves

`conversation_log_demo.py` proves that a simple conversation log can be loaded, converted into MemoryUnits, validated, and exported as EngineMemory-compatible JSON.

It writes generated files under `sample_outputs/`.

These generated outputs are ignored by Git.


## ChatGPT export-like demo

`chatgpt_export_like_demo.py` shows how a small ChatGPT-style mapping can be normalized into the same message model before extraction.

This is convenience support for the public demo. It is not a guarantee that every historical ChatGPT export variant is fully covered.

## What the end-to-end demo proves

`end_to_end_engine_demo.py` proves that the extracted MemoryUnits can be passed into SO Memory Engine and converted into a Context Pack.

The demo should produce at least one active or returning memory on the included sample.

## What this does not prove

The demo does not prove:

- high-accuracy natural-language extraction
- production parser quality
- robust canonical memory generation
- superiority over LLM extractors
- superiority over specialized NLP systems
- correct interpretation of arbitrary conversation logs

It only proves the public entry path:

```text
conversation log -> MemoryUnit -> EngineMemory -> Context Pack
```

## Why this matters

SO Memory Engine begins after structure exists.

Without an entry path, developers must invent their own conversion layer before they can even try the Engine on conversation logs.

SO Extractor Free provides that minimal entry path while leaving higher-quality extraction, source-span retention, advanced validation, and canonical memory candidates for future Pro work.
