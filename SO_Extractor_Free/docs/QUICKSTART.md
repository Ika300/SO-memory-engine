# Quickstart

This is the smallest useful SO Extractor Free path.

## 1. Run the free extractor demo

```bash
cd C:\Users\Ika300\Desktop\SO_Memory_Engine
py -3 SO_Extractor_Free\examples\conversation_log_demo.py
```

This creates:

- `sample_outputs/memory_units.json`
- `sample_outputs/engine_memories.json`
- `sample_outputs/validation_report.md`

## 2. Try the ChatGPT export-like demo

```bash
py -3 SO_Extractor_Free\examples\chatgpt_export_like_demo.py
```

This creates:

- `sample_outputs/chatgpt_export_like/normalized_messages.json`
- `sample_outputs/chatgpt_export_like/memory_units.json`
- `sample_outputs/chatgpt_export_like/engine_memories.json`
- `sample_outputs/chatgpt_export_like/validation_report.md`

## 3. Run the Engine demo

This requires the expected local layout:

```text
Desktop/
  SO_Memory_Kernel/
  SO_Memory_Engine/
    SO_Extractor_Free/
```

Then run:

```bash
py -3 SO_Extractor_Free\examples\end_to_end_engine_demo.py
```

## Where this fits

```text
Memory Store
    -> Retriever or exported log
    -> SO Extractor Free
    -> SO Memory Engine
    -> Context Pack
    -> LLM or agent
```

## Important boundary

SO Extractor Free is a transparent entry path.

It does not claim production extraction quality.

It does not silently merge meanings.

It does not hide evidence.