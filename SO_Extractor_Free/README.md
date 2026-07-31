# SO Extractor Free

Free entry-path extractor bundled with SO Memory Engine.

SO Extractor Free turns small conversation logs into structured MemoryUnits, validates them, and exports EngineMemory-compatible JSON.

This project is intentionally simple. It is not SO Extractor Pro and it is not a high-accuracy natural-language parser.

## Where it fits

```text
Memory Store
    -> Retriever or exported log
    -> SO Extractor Free
    -> SO Memory Engine
    -> Context Pack
    -> LLM or agent
```

SO Extractor Free is the small conversion layer before SO Memory Engine.

## Why this exists

SO Memory Engine begins after structure exists.

Many users will ask:

> How do I turn my conversation logs into Engine input?

SO Extractor Free provides a minimal answer:

```text
conversation log
    -> basic rule extractor
    -> MemoryUnit
    -> validation report
    -> EngineMemory JSON
    -> SO Memory Engine demo
```

## What it does

- loads simple JSON conversation logs
- loads small ChatGPT export-like mapping samples
- creates transparent rule-based MemoryUnits
- preserves source ids and message ids
- creates simple labels and relation candidates
- validates required fields
- exports EngineMemory-compatible dictionaries
- can run an end-to-end demo with SO Memory Engine

## What it does not do

- no LLM calls
- no embeddings
- no hidden semantic dictionary
- no high-accuracy parser claim
- no automatic perfect memory extraction
- no silent semantic merging
- no Canonical Memory production feature
- no full guarantee for every ChatGPT export variant

## 3-minute trial from the repository root

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

## Install for local development

From the repository root:

```bash
py -3 -m pip install -e .
py -3 -m pip install -e SO_Extractor_Free
```

## Strategic boundary

Free Extractor is an entry path. It helps users try SO Memory Engine.

Extractor Pro, if developed, should improve input quality through better relation extraction, span retention, canonical memory candidates, advanced validation, Engine-readiness reports, and possibly Engine Pro improvements when real Pro needs require them.

| Area | Free | Pro direction |
| --- | --- | --- |
| Goal | quick trial | production-quality input pipeline |
| Extraction | transparent rules | stronger structural extraction |
| Source evidence | message-level source id | source spans, evidence snippets, uncertainty |
| Canonical memory | not included | candidates only, with preserved evidence |
| Engine | public SO Memory Engine | Engine Pro only if needed |
| Claim | entry path | operational quality |

SO preserves supplied structure; it does not magically correct semantic extraction errors.

## Documentation

- [Quickstart](docs/QUICKSTART.md)
- [Input Schema](docs/INPUT_SCHEMA.md)
- [End-to-End Demo](docs/END_TO_END_DEMO.md)
- [LLM Structured Output](docs/LLM_STRUCTURED_OUTPUT.md)
- [Free Extractor Limits](docs/FREE_EXTRACTOR_LIMITS.md)
- [Sample Output](docs/SAMPLE_OUTPUT.md)
- [Free vs Pro Boundary](docs/FREE_VS_PRO.md)
- [Roadmap](docs/ROADMAP.md)