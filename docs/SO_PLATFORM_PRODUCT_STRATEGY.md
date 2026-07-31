# SO Platform Product Strategy

This document fixes the product boundary for SO Memory Engine and future SO Memory Pro work.

The purpose is to prevent the platform from becoming a mixed pile of Engine logic, extraction logic, parser research, sales promises, and LLM prompt templates.

## 1. Core platform shape

The public repository should show the Engine first.

```text
curated MemoryUnits
        ->
SO Memory Engine
        ->
Context Pack
        ->
user's own LLM / agent / application
```

The Engine starts after structure exists. It does not parse raw natural language.

## 2. Free product position

The free public product is the Engine.

Free should show:

- how structured memory enters the Engine;
- how returning structures are observed;
- how recurring structures are surfaced;
- how unresolved tensions remain visible;
- how evidence identity separates source breadth from contextual recurrence;
- how a Context Pack is constructed.

Free should not make a weak extractor the user's first experience. A poor extraction experience can make the Engine look weak before users reach the actual Engine behavior.

## 3. Paid product position

Paid value should come from the full Pro package:

```text
SO Extractor Pro
        +
SO Memory Engine Pro
```

Pro should make real logs Engine-ready and then build production-quality Context Packs.

## 4. Engine responsibility

SO Memory Engine is responsible for observing caller-supplied structure.

It should continue to provide:

- active memories;
- returning memories;
- recurring structures;
- unresolved tensions;
- structural connections;
- evidence identity;
- Context Pack output;
- traceability into Kernel output.

It should not become:

- a natural-language parser;
- a chatbot;
- a vector database;
- a storage layer;
- a UI;
- a hidden semantic dictionary;
- a fuzzy semantic merge system;
- an LLM wrapper.

## 5. Extractor responsibility

Extraction is a separate layer.

An extractor turns raw input into Engine-ready MemoryUnits. It should preserve evidence and uncertainty.

Extractor Pro should eventually handle:

- source/message/span modeling;
- candidate extraction;
- evidence binding;
- validation;
- review queue output;
- readiness reporting;
- provenance manifests;
- MemoryUnit export.

## 6. Engine Pro responsibility

Engine Pro should be upgraded early, before the paid extractor and packaging become too dependent on the free Engine shape.

Engine Pro candidates:

- evidence identity quality;
- context pack audit metadata;
- current-state reconstruction support;
- conflict/tension detail;
- noise rejection diagnostics;
- context pack profiles;
- production diagnostics.

Engine Pro must still preserve SO identity:

- no hidden dictionary;
- no approximate semantic merge;
- no LLM-invented memory;
- no treating similarity as identity;
- no suppressing repetition merely because it repeats;
- no validation-as-truth claim.

## 7. LLM boundary

SO products should not include an LLM.

The system may produce Context Packs that external LLMs or agents can use, but the product itself should remain a structural-memory engine and extractor package.

This keeps the value clear:

```text
SO builds structural context.
The user's own LLM or application uses that context.
```

## 8. Public vs paid boundary

### Public / Free

- Engine source;
- curated MemoryUnit quickstart;
- tests;
- benchmarks;
- integration docs;
- clear input boundary.

### Paid / Pro

- Extractor Pro;
- Engine Pro;
- stronger evidence handling;
- readiness reports;
- review queue;
- provenance manifests;
- advanced context audit;
- honest benchmarks;
- paid setup and integration docs.

## 9. Benchmark principle

Benchmarks must not be faked or cherry-picked.

SO should be evaluated where it is meant to be strong:

- Structure Recurrence;
- Evidence Independence;
- Conflict Detection;
- Context Pack Utility;
- Noise Rejection;
- Current State Reconstruction.

Benchmarks should show failures as well as successes.

## 10. Current roadmap

1. Keep the public repository Engine-first.
2. Remove weak extractor experience from the public main path.
3. Build Pro workspace separately.
4. Upgrade Engine Pro foundation early.
5. Build Extractor Pro MVP.
6. Integrate Extractor Pro and Engine Pro.
7. Benchmark honestly.
8. Package the paid product only after behavior is understood.

## Closing position

The free repository should make one thing clear:

> SO Memory Engine is useful when structure already exists.

The paid product should answer the next problem:

> How do I turn real logs into reliable SO-ready structural memory, and then build better Context Packs from it?