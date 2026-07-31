# Engine + Extractor Free Trial

This repository contains two parts:

```text
SO Memory Engine
    = structural context construction layer

SO Extractor Free
    = small entry path that turns simple conversation logs into EngineMemory-compatible JSON
```

The Extractor is included under:

```text
SO_Extractor_Free/
```

## Why both are here

SO Memory Engine begins after structure exists.

New users usually ask:

> How do I turn my conversation logs into Engine input?

SO Extractor Free provides a minimal answer for trials.

## Run the full free trial

Start with the one-command quickstart:

```bash
py -3 quickstart.py
```

Then inspect `outputs/free_trial/07_context_pack.txt`.

The individual demos are also available from the repository root:

```bash
py -3 SO_Extractor_Free\examples\conversation_log_demo.py
py -3 SO_Extractor_Free\examples\chatgpt_export_like_demo.py
py -3 SO_Extractor_Free\examples\end_to_end_engine_demo.py
```

On non-Windows systems:

```bash
python SO_Extractor_Free/examples/conversation_log_demo.py
python SO_Extractor_Free/examples/chatgpt_export_like_demo.py
python SO_Extractor_Free/examples/end_to_end_engine_demo.py
```

## Boundary

SO Extractor Free is intentionally simple.

It does not call an LLM, use embeddings, perform hidden semantic merging, or claim production extraction quality.

It exists so developers can quickly see the path:

```text
conversation log
    -> SO Extractor Free
    -> EngineMemory-compatible JSON
    -> SO Memory Engine
    -> Context Pack
```

Higher-quality extraction belongs to future SO Extractor Pro work.