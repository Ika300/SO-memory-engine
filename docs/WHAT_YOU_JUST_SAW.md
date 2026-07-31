# What You Just Saw

The complete free quickstart is not a chatbot demo.

It shows the structural-memory pipeline before an LLM generates a response.

```text
conversation log
    -> SO Extractor Free
    -> MemoryUnit candidates
    -> SO Memory Engine
    -> Context Pack
```

## 1. The input conversation was normalized

The quickstart begins with a small conversation JSON file.

The default sample lives at:

```text
SO_Extractor_Free/sample_inputs/conversation_log.json
```

You can pass your own file:

```bash
py -3 quickstart.py my_conversation.json
```

## 2. Extractor Free created MemoryUnits

SO Extractor Free turns user messages into transparent rule-based MemoryUnit candidates.

It creates:

- content
- labels
- relation candidates
- source ids
- message ids
- simple scores

This is intentionally not a high-accuracy parser.

The generated file is:

```text
outputs/free_trial/02_memory_units.json
```

## 3. The current message was also extracted

The current message is not hand-labeled in the quickstart.

It goes through the same Free Extractor path and becomes:

```text
outputs/free_trial/05_current_memory_unit.json
```

This keeps the demo honest: the public free path shows how the system behaves with the simple extractor it actually ships with.

## 4. The Engine received structure, not raw magic

SO Memory Engine does not directly understand arbitrary prose.

It receives structured memory:

- labels
- relations
- source identity
- scores
- metadata

Then it reconstructs structural memory context.

The Engine input is visible at:

```text
outputs/free_trial/04_engine_memories.json
```

## 5. The output is a Context Pack

The final output is not an assistant answer.

It is structured memory context that an AI app, agent, or LLM can use.

Open:

```text
outputs/free_trial/07_context_pack.txt
```

The JSON version is:

```text
outputs/free_trial/06_context_pack.json
```

## 6. What this proves

The quickstart proves the free path works:

```text
conversation log -> Extractor Free -> EngineMemory -> Context Pack
```

It does not prove production-grade extraction quality.

It does not prove arbitrary natural-language understanding.

It does not use embeddings, LLM calls, hidden semantic dictionaries, or silent approximate merging.

## 7. Why it matters

Most memory systems retrieve similar old text.

SO Memory Engine exposes structural context such as:

- returning memory
- repeated structure
- independent source evidence
- contextual recurrence
- unresolved tensions
- structural connections

That context can help an LLM respond with memory without letting the LLM invent that memory.